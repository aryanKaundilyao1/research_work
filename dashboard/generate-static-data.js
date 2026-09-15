import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '..');

// Walk directory recursively
function walkDir(dir) {
  let results = [];
  try {
    if (!fs.existsSync(dir)) return results;
    const list = fs.readdirSync(dir);
    list.forEach(file => {
      if (file.startsWith('.')) return;
      const fullPath = path.join(dir, file);
      const relPath = path.relative(PROJECT_ROOT, fullPath);
      // Skip dashboard, node_modules, datasets (19GB), jasdev, output cache
      if (relPath.startsWith('dashboard') || relPath.includes('node_modules') ||
          relPath.startsWith('datasets') || relPath.startsWith('jasdev') ||
          relPath.includes('__pycache__') || relPath.includes('/cache/') ||
          relPath.includes('/cache2/')) return;
      try {
        const stat = fs.statSync(fullPath);
        if (stat.isDirectory()) {
          results = results.concat(walkDir(fullPath));
        } else {
          results.push(relPath);
        }
      } catch (err) { /* skip unreadable */ }
    });
  } catch (err) {
    console.warn('Could not read directory:', dir);
  }
  return results;
}

// Categorize files into inventory buckets
function buildInventory(allFiles) {
  const inventory = {
    manuscript: [], pdf: [], figures: [], tables: [],
    code: [], audit: [], other: []
  };

  allFiles.forEach(relPath => {
    const ext = path.extname(relPath).toLowerCase();
    const filename = path.basename(relPath).toLowerCase();

    if (ext === '.pdf') {
      inventory.pdf.push(relPath);
    } else if (['.png', '.jpg', '.jpeg', '.svg', '.webp'].includes(ext)) {
      inventory.figures.push(relPath);
    } else if (['.csv', '.xlsx'].includes(ext)) {
      inventory.tables.push(relPath);
    } else if (['.py', '.ipynb', '.js', '.ts', '.r', '.cpp', '.java', '.sh'].includes(ext)) {
      // Skip the generate script itself and package configs
      if (!relPath.startsWith('api/') && !relPath.endsWith('package-lock.json')) {
        inventory.code.push(relPath);
      }
    } else if (ext === '.md') {
      if (filename.includes('audit') || filename.includes('matrix')) {
        inventory.audit.push(relPath);
      } else if (filename.includes('manuscript') || filename.includes('paper') ||
                 filename.includes('draft') || filename.includes('report')) {
        inventory.manuscript.push(relPath);
      } else {
        inventory.other.push(relPath);
      }
    } else if (ext === '.json' || ext === '.pkl' || ext === '.lock') {
      // Skip binary/config files
    } else {
      inventory.other.push(relPath);
    }
  });

  return inventory;
}

// Read manuscript content
function readManuscript() {
  const p = path.join(PROJECT_ROOT, 'reports', 'FINAL_MANUSCRIPT_MASTER.md');
  if (fs.existsSync(p)) return fs.readFileSync(p, 'utf8');
  return '# Manuscript not found\n\nEnsure reports/FINAL_MANUSCRIPT_MASTER.md exists.';
}

// Find audit conflicts
function findConflicts(allFiles) {
  const conflictTerms = [
    { term: "AUC = 0.801", issue: "Old AUC value from previous paper" },
    { term: "N = 30", issue: "Old Dataset B sample size" },
    { term: "N=30", issue: "Old Dataset B sample size" },
    { term: "Beginning phase", issue: "Obsolete phase segmentation" },
    { term: "Middle phase", issue: "Obsolete phase segmentation" },
    { term: "End phase", issue: "Obsolete phase segmentation" },
    { term: "universal generalization", issue: "Unsupported claim" },
    { term: "target-domain adaptation", issue: "Conflicts with zero-shot claim" }
  ];
  const conflicts = [];
  allFiles.forEach(relPath => {
    const ext = path.extname(relPath).toLowerCase();
    if (['.md', '.txt'].includes(ext)) {
      try {
        const content = fs.readFileSync(path.join(PROJECT_ROOT, relPath), 'utf8');
        const lines = content.split('\n');
        conflictTerms.forEach(ct => {
          lines.forEach((line, i) => {
            if (line.includes(ct.term)) {
              conflicts.push({
                path: relPath, lineNum: i + 1,
                line: line.trim().substring(0, 200),
                term: ct.term, issue: ct.issue
              });
            }
          });
        });
      } catch (e) { /* skip */ }
    }
  });
  return conflicts;
}

// Copy static assets (images, PDFs, CSVs, code, markdown) to dashboard/public/raw/
function copyStaticAssets(allFiles) {
  const assetExts = ['.png', '.jpg', '.jpeg', '.svg', '.webp', '.pdf', '.csv', '.md', '.py', '.js', '.sh', '.txt'];
  const publicRawDir = path.join(__dirname, 'public', 'raw');
  let count = 0;

  allFiles.forEach(relPath => {
    const ext = path.extname(relPath).toLowerCase();
    if (assetExts.includes(ext)) {
      const src = path.join(PROJECT_ROOT, relPath);
      const dest = path.join(publicRawDir, relPath);
      fs.mkdirSync(path.dirname(dest), { recursive: true });
      try {
        fs.copyFileSync(src, dest);
        count++;
      } catch (err) { /* skip unreadable */ }
    }
  });
  console.log(`  Copied ${count} static assets to dashboard/public/raw/`);
}

// ── Main ──
console.log('=== Static Data Generator ===');
console.log('Project root:', PROJECT_ROOT);

const allFiles = walkDir(PROJECT_ROOT);
console.log(`Found ${allFiles.length} files`);

const inventory = buildInventory(allFiles);
const manuscriptContent = readManuscript();
const conflicts = findConflicts(allFiles);

// Copy images/PDFs to public/raw
copyStaticAssets(allFiles);

// Write staticData.js
const generatedDir = path.join(__dirname, 'src', 'generated');
fs.mkdirSync(generatedDir, { recursive: true });

const output = `// Auto-generated by generate-static-data.js — DO NOT EDIT MANUALLY
// Generated at: ${new Date().toISOString()}

export const inventory = ${JSON.stringify(inventory, null, 2)};

export const manuscriptContent = ${JSON.stringify(manuscriptContent)};

export const conflicts = ${JSON.stringify(conflicts, null, 2)};
`;

fs.writeFileSync(path.join(generatedDir, 'staticData.js'), output);

console.log('\\nGenerated dashboard/src/generated/staticData.js');
console.log('Inventory summary:');
Object.entries(inventory).forEach(([key, val]) => {
  console.log(`  ${key}: ${val.length} files`);
});
console.log('\\nDone!');
