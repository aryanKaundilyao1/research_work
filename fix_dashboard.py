import re
import os

def fix_file(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r') as f:
        text = f.read()

    text = re.sub(r'0\.739', '0.772', text)
    text = re.sub(r'0\.423', '0.492', text)
    text = re.sub(r'0\.408', '0.492', text)
    text = re.sub(r'\[0\.712,\s*0\.765\]', '[0.643, 0.880]', text)
    text = re.sub(r'0\.9527', '0.980', text)
    text = re.sub(r'Top-20 Jaccard', 'Top-5 Jaccard', text)
    
    with open(filepath, 'w') as f:
        f.write(text)

fix_file('dashboard/src/pages/Results.jsx')
fix_file('dashboard/src/pages/Experiments.jsx')
fix_file('dashboard/src/pages/AuditCenter.jsx')
