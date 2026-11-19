import re

with open('public/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

links = re.findall(r'href=[\'"]([^\'"]+)[\'"]', content)
print(f"Total hrefs in public/index.html: {len(links)}")
blog_links = [l for l in links if 'blog' in l.lower()]
print(f"Blog links in public/index.html ({len(blog_links)}):")
for l in sorted(set(blog_links)):
    print(' -', l)
