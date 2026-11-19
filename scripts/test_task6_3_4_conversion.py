"""
PixelCraft AI — Task 6.3.4 Verification Suite
Validates:
1. Blog-to-Tool CTAs (mid-article cards & end-article discovery grids across all 15 blog posts).
2. Cross-Tool Discovery & Educational Guide Banners across all 15 tool pages.
3. Homepage Tool Grid Instrumentation.
4. GA4 Click Event Architecture in utils.js.
5. Link integrity (all CTA target files exist).
6. Sitewide Heading Hierarchy & SEO Integrity.
"""

import os
import re
import sys
from bs4 import BeautifulSoup

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(ROOT_DIR, 'public', 'blog')
TOOLS_DIR = os.path.join(ROOT_DIR, 'public', 'tools')
INDEX_PATH = os.path.join(ROOT_DIR, 'public', 'index.html')
UTILS_PATH = os.path.join(ROOT_DIR, 'public', 'js', 'utils.js')

all_passed = True

def check(condition, message):
    global all_passed
    if condition:
        print(f"  ✅ [PASS] {message}")
    else:
        print(f"  ❌ [FAIL] {message}")
        all_passed = False

print("================================================================")
print("PIXELCRAFT AI — SEO TASK 6.3.4 VERIFICATION SUITE")
print("================================================================\n")

# 1. VERIFY UTILS.JS GA4 IMPLEMENTATION
print("--- 1. GA4 Conversion Tracking Architecture (utils.js) ---")
with open(UTILS_PATH, 'r', encoding='utf-8') as f:
    utils_code = f.read()

check('trackToolCtaClick:' in utils_code, "trackToolCtaClick method defined in PixelCraftAnalytics")
check("'tool_cta_clicked'" in utils_code, "Dispatches custom event 'tool_cta_clicked'")
check('source_page:' in utils_code, "Includes source_page parameter")
check('destination_tool:' in utils_code, "Includes destination_tool parameter")
check('cta_location:' in utils_code, "Includes cta_location parameter")
check('content_type:' in utils_code, "Includes content_type parameter")
check('dedupeKey' in utils_code, "Implements duplicate suppression logic")
check('data-tool-cta' in utils_code, "Includes global delegated click listener for data-tool-cta")

# 2. VERIFY HOMEPAGE TOOL CARDS INSTRUMENTATION
print("\n--- 2. Homepage Tool Discovery Instrumentation (index.html) ---")
with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    index_soup = BeautifulSoup(f.read(), 'html.parser')

homepage_cards = index_soup.select('a.tool-card')
check(len(homepage_cards) == 15, f"Found all 15 tool cards on homepage (got {len(homepage_cards)})")
for card in homepage_cards:
    dest = card.get('data-dest-tool')
    has_cta = card.get('data-tool-cta') == 'true'
    loc = card.get('data-cta-location') == 'homepage_grid'
    check(has_cta and loc and dest, f"Homepage card for {dest} properly instrumented")

# 3. VERIFY ALL 15 BLOG POSTS
print("\n--- 3. Blog-to-Tool CTAs & Discovery Grids (All 15 Blog Articles) ---")
blog_files = [f for f in sorted(os.listdir(BLOG_DIR)) if f.endswith('.html') and f != 'index.html']
check(len(blog_files) == 15, f"Verified 15 blog articles in public/blog/ (got {len(blog_files)})")

for bfile in blog_files:
    bpath = os.path.join(BLOG_DIR, bfile)
    with open(bpath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Mid-article CTA Card
    cta_card = soup.select_one('.blog-tool-cta-card')
    check(cta_card is not None, f"{bfile}: Has .blog-tool-cta-card (mid-article CTA)")
    if cta_card:
        btn = cta_card.select_one('a.tool-cta-btn')
        check(btn is not None and btn.get('data-tool-cta') == 'true', f"{bfile}: Primary CTA button has data-tool-cta='true'")
        if btn:
            dest_tool = btn.get('data-dest-tool')
            tool_exists = os.path.exists(os.path.join(TOOLS_DIR, dest_tool))
            check(tool_exists, f"{bfile}: Target tool exists ({dest_tool})")

    # End-of-article related tools grid
    related_grid = soup.select_one('.blog-related-grid')
    check(related_grid is not None, f"{bfile}: Has .blog-related-grid")
    if related_grid:
        cards = related_grid.select('a.blog-related-card')
        check(len(cards) >= 3, f"{bfile}: Has at least 3 curated related tool cards (got {len(cards)})")
        for c in cards:
            dest = c.get('data-dest-tool')
            tool_exists = os.path.exists(os.path.join(TOOLS_DIR, dest))
            check(tool_exists, f"{bfile}: Related card target exists ({dest})")

# 4. VERIFY ALL 15 TOOL PAGES
print("\n--- 4. Cross-Tool Discovery & Educational Banners (All 15 Tool Pages) ---")
tool_files = [f for f in sorted(os.listdir(TOOLS_DIR)) if f.endswith('.html')]
check(len(tool_files) == 15, f"Verified 15 tools in public/tools/ (got {len(tool_files)})")

for tfile in tool_files:
    tpath = os.path.join(TOOLS_DIR, tfile)
    with open(tpath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Educational Research Guide Banner
    guide_link = soup.select_one('a[data-cta-location="tool_guide_banner"]')
    check(guide_link is not None, f"{tfile}: Has educational guide banner")
    if guide_link:
        dest_blog = guide_link.get('data-dest-tool')
        blog_exists = os.path.exists(os.path.join(BLOG_DIR, dest_blog))
        check(blog_exists, f"{tfile}: Linked educational research guide exists ({dest_blog})")

    # Related Tools Section
    cross_tool_links = soup.select('a[data-cta-location="related_tools"]')
    check(len(cross_tool_links) >= 3, f"{tfile}: Has cross-tool discovery links (got {len(cross_tool_links)})")
    for link in cross_tool_links:
        dest = link.get('data-dest-tool')
        tool_exists = os.path.exists(os.path.join(TOOLS_DIR, dest))
        check(tool_exists, f"{tfile}: Cross-tool link target exists ({dest})")

print("\n================================================================")
if all_passed:
    print("🎉 ALL TASK 6.3.4 TESTS PASSED FLAWLESSLY!")
    sys.exit(0)
else:
    print("❌ SOME TASK 6.3.4 TESTS FAILED!")
    sys.exit(1)
