import re

with open('public/blog/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

links = re.findall(r'href=[\'"]([^\'"]+\.html)[\'"]', content)
print(f"Total HTML links found in public/blog/index.html: {len(links)}")
blog_article_links = [l for l in sorted(set(links)) if not l.startswith('../') and l != 'index.html']
print(f"Unique Blog Article Links ({len(blog_article_links)}):")
for l in blog_article_links:
    print(' -', l)
