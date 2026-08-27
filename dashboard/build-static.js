import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.join(__dirname, '..');
const PUBLIC_DIR = path.join(__dirname, 'public');
const RAW_DIR = path.join(PUBLIC_DIR, 'raw');
const API_DIR = path.join(PUBLIC_DIR, 'api');

// Helper: Recursively walk directory
function walkDir(dir, skipDirs = []) {
  let results = [];
  const list = fs.readdirSync(dir);
  list.forEach(file => {
    if (file.startsWith('.')) return;
    
    const fullPath = path.join(dir, file);
    const relPath = path.relative(PROJECT_ROOT, fullPath);
    
    // Skip the dashboard folder itself, node_modules, and huge datasets folder
    if (relPath.startsWith('dashboard') || relPath.startsWith('datasets') || relPath.includes('node_modules')) return;
    
    const stat = fs.statSync(fullPath);
    if (stat && stat.isDirectory()) {
      results = results.concat(walkDir(fullPath, skipDirs));
    } else {
      results.push({ relPath, fullPath });
    }
  });
  return results;
}

console.log('Building static assets for Vercel...');

// 1. Create directories
if (!fs.existsSync(RAW_DIR)) fs.mkdirSync(RAW_DIR, { recursive: true });
if (!fs.existsSync(API_DIR)) fs.mkdirSync(API_DIR, { recursive: true });

const allFilesInfo = walkDir(PROJECT_ROOT);

// 2. Build Inventory
const inventory = {
  manuscript: [],
  pdf: [],
  figures: [],
  tables: [],
  code: [],
  audit: [],
  other: []
};

allFilesInfo.forEach(({ relPath }) => {
  const ext = path.extname(relPath).toLowerCase();
  const filename = path.basename(relPath).toLowerCase();
  
  if (ext === '.pdf') {
    inventory.pdf.push(relPath);
  } else if (['.png', '.jpg', '.jpeg', '.svg', '.webp'].includes(ext)) {
    inventory.figures.push(relPath);
  } else if (['.csv', '.xlsx'].includes(ext)) {
    inventory.tables.push(relPath);
  } else if (['.py', '.ipynb', '.js', '.ts', '.r', '.cpp', '.java', '.sh'].includes(ext)) {
    inventory.code.push(relPath);
  } else if (ext === '.md') {
    if (filename.includes('audit') || filename.includes('matrix')) {
      inventory.audit.push(relPath);
    } else if (filename.includes('manuscript') || filename.includes('paper') || filename.includes('draft') || filename.includes('report')) {
      inventory.manuscript.push(relPath);
    } else {
      inventory.other.push(relPath);
    }
  } else {
    inventory.other.push(relPath);
  }
});

fs.writeFileSync(path.join(API_DIR, 'inventory.json'), JSON.stringify(inventory));
console.log('Generated inventory.json');

// 3. Build Search Index
const searchIndex = [];
allFilesInfo.forEach(({ relPath, fullPath }) => {
  const ext = path.extname(relPath).toLowerCase();
  // skip large datasets for search index
  if (relPath.startsWith('datasets') || relPath.includes('package-lock.json')) return;
  
  if (['.md', '.py', '.js', '.ts', '.csv', '.txt'].includes(ext)) {
    try {
      const stat = fs.statSync(fullPath);
      if (stat.size < 500 * 1024) { // Only index files smaller than 500KB
        const content = fs.readFileSync(fullPath, 'utf8');
        searchIndex.push({ path: relPath, content });
      }
    } catch (e) {
      // ignore
    }
  }
});

fs.writeFileSync(path.join(API_DIR, 'search_index.json'), JSON.stringify(searchIndex));
console.log('Generated search_index.json');

// 4. Copy Raw Files
allFilesInfo.forEach(({ relPath, fullPath }) => {
  const destPath = path.join(RAW_DIR, relPath);
  const destDir = path.dirname(destPath);
  
  if (!fs.existsSync(destDir)) {
    fs.mkdirSync(destDir, { recursive: true });
  }
  
  fs.copyFileSync(fullPath, destPath);
});
console.log('Copied raw files to public/raw/');

console.log('Static build complete!');
