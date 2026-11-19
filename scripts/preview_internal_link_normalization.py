import os
import re

def preview_normalizations():
    public_dir = 'public'
    files_modified = {}
    
    for root, _, files in os.walk(public_dir):
        for f in files:
            if not f.endswith('.html') or f.endswith('.bak'):
                continue
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                
            # Patterns to match:
            # 1. href="../index.html#tools" -> href="/#tools"
            # 2. href="../index.html#features" -> href="/#features"
            # 3. href="../index.html" -> href="/"
            # 4. href="index.html#tools" (on non-index.html pages) -> href="/#tools"
            # 5. href="index.html#features" (on non-index.html pages) -> href="/#features"
            # 6. href="index.html" (on non-index.html pages) -> href="/"
            # 7. href="./index.html" -> href="/"
            
            changes = []
            
            # Subdirectory relative links
            if '../index.html#tools' in content:
                changes.append(('../index.html#tools', '/#tools', content.count('../index.html#tools')))
            if '../index.html#features' in content:
                changes.append(('../index.html#features', '/#features', content.count('../index.html#features')))
            if '../index.html' in content:
                # Count only bare ../index.html not followed by #
                bare_count = len(re.findall(r'\.\./index\.html(?![#])', content))
                if bare_count > 0:
                    changes.append(('../index.html', '/', bare_count))
                    
            if f != 'index.html':
                if 'index.html#tools' in content:
                    changes.append(('index.html#tools', '/#tools', content.count('index.html#tools')))
                if 'index.html#features' in content:
                    changes.append(('index.html#features', '/#features', content.count('index.html#features')))
                bare_root = len(re.findall(r'(?<!\.\./)index\.html(?![#])', content))
                if bare_root > 0:
                    changes.append(('index.html', '/', bare_root))
                    
            if changes:
                files_modified[fp] = changes
                
    print(f"Total files requiring normalization: {len(files_modified)}")
    for fp, ch in sorted(files_modified.items()):
        print(f"\n{fp}:")
        for orig, repl, cnt in ch:
            print(f"  [{cnt}x] {orig} -> {repl}")

if __name__ == '__main__':
    preview_normalizations()
