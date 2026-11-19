import os
import re

def apply_normalization():
    public_dir = 'public'
    modified_count = 0
    total_replacements = 0
    
    for root, _, files in os.walk(public_dir):
        for f in files:
            if not f.endswith('.html') or f.endswith('.bak'):
                continue
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf-8', errors='ignore') as file:
                orig_content = file.read()
                
            content = orig_content
            file_replacements = 0
            
            # 1. Replace relative paths to index.html with anchors first
            if '../index.html#tools' in content:
                cnt = content.count('../index.html#tools')
                content = content.replace('../index.html#tools', '/#tools')
                file_replacements += cnt
            if '../index.html#features' in content:
                cnt = content.count('../index.html#features')
                content = content.replace('../index.html#features', '/#features')
                file_replacements += cnt
            if '../index.html' in content:
                cnt = content.count('../index.html')
                content = content.replace('../index.html', '/')
                file_replacements += cnt
                
            # 2. For non-index.html files, replace root relative index.html
            if f != 'index.html':
                if 'href="index.html#tools"' in content:
                    cnt = content.count('href="index.html#tools"')
                    content = content.replace('href="index.html#tools"', 'href="/#tools"')
                    file_replacements += cnt
                if 'href="index.html#features"' in content:
                    cnt = content.count('href="index.html#features"')
                    content = content.replace('href="index.html#features"', 'href="/#features"')
                    file_replacements += cnt
                if 'href="index.html"' in content:
                    cnt = content.count('href="index.html"')
                    content = content.replace('href="index.html"', 'href="/"')
                    file_replacements += cnt
                if "href='index.html'" in content:
                    cnt = content.count("href='index.html'")
                    content = content.replace("href='index.html'", "href='/'")
                    file_replacements += cnt
                    
            if content != orig_content:
                with open(fp, 'w', encoding='utf-8') as file:
                    file.write(content)
                modified_count += 1
                total_replacements += file_replacements
                print(f"  Normalized {file_replacements} link(s) in {fp}")
                
    print(f"\nDone! Modified {modified_count} files with {total_replacements} canonical link replacements.")

if __name__ == '__main__':
    apply_normalization()
