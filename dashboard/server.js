import express from 'express';
import cors from 'cors';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.join(__dirname, '..');

const app = express();
app.use(cors());

// Expose the entire project root as static files, so we can load images/PDFs directly by their relative path
app.use('/raw', express.static(PROJECT_ROOT));

// Helper: Recursively walk directory
function walkDir(dir, skipDirs = []) {
  let results = [];
  const list = fs.readdirSync(dir);
  list.forEach(file => {
    // Skip hidden files/dirs and explicitly skipped dirs
    if (file.startsWith('.')) return;
    
    const fullPath = path.join(dir, file);
    const relPath = path.relative(PROJECT_ROOT, fullPath);
    
    // Skip the dashboard folder itself and node_modules
    if (relPath.startsWith('dashboard') || relPath.includes('node_modules')) return;
    
    const stat = fs.statSync(fullPath);
    if (stat && stat.isDirectory()) {
      results = results.concat(walkDir(fullPath, skipDirs));
    } else {
      results.push(relPath);
    }
  });
  return results;
}

app.get('/api/inventory', (req, res) => {
  try {
    const allFiles = walkDir(PROJECT_ROOT);
    
    const inventory = {
      manuscript: [],
      pdf: [],
      figures: [],
      tables: [],
      code: [],
      audit: [],
      other: []
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

    res.json(inventory);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/file', (req, res) => {
  const relPath = req.query.path;
  if (!relPath) return res.status(400).json({ error: 'Missing path parameter' });

  // Prevent directory traversal attacks
  const fullPath = path.join(PROJECT_ROOT, relPath);
  if (!fullPath.startsWith(PROJECT_ROOT)) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  try {
    const content = fs.readFileSync(fullPath, 'utf8');
    res.send(content);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/search', (req, res) => {
  const query = req.query.q?.toLowerCase();
  if (!query) return res.json([]);

  try {
    const allFiles = walkDir(PROJECT_ROOT);
    const results = [];

    allFiles.forEach(relPath => {
      const ext = path.extname(relPath).toLowerCase();
      // Only search text-based files
      if (['.md', '.py', '.js', '.ts', '.csv', '.txt'].includes(ext)) {
        try {
          const content = fs.readFileSync(path.join(PROJECT_ROOT, relPath), 'utf8');
          if (content.toLowerCase().includes(query)) {
            // Find context snippet
            const lines = content.split('\n');
            const matches = [];
            for (let i = 0; i < lines.length; i++) {
              if (lines[i].toLowerCase().includes(query)) {
                matches.push({
                  lineNum: i + 1,
                  content: lines[i].trim()
                });
                if (matches.length > 3) break; // Limit snippets
              }
            }
            results.push({
              path: relPath,
              matches
            });
          }
        } catch (e) {
          // ignore read errors for binary/locked files
        }
      }
    });

    res.json(results);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/conflicts', (req, res) => {
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

  try {
    const allFiles = walkDir(PROJECT_ROOT);
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
                  path: relPath,
                  lineNum: i + 1,
                  line: line.trim(),
                  term: ct.term,
                  issue: ct.issue
                });
              }
            });
          });
        } catch (e) {}
      }
    });

    res.json(conflicts);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

if (process.env.NODE_ENV !== 'production' && !process.env.VERCEL) {
  const PORT = process.env.PORT || 3001;
  app.listen(PORT, () => {
    console.log(`Backend API running on http://localhost:${PORT}`);
  });
}

export default app;
