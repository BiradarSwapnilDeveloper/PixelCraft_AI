import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

with open('public/tools/pdf-to-link.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

wa = soup.find(id='share-wa')
tg = soup.find(id='share-tg')
em = soup.find(id='share-em')

print("=== Share Buttons Markup Verification ===")
print("WhatsApp:", wa)
print("Telegram:", tg)
print("Email:", em)

assert wa is not None, "share-wa not found"
assert tg is not None, "share-tg not found"
assert em is not None, "share-em not found"

assert wa.get('target') == '_blank', "WhatsApp should have target=_blank"
assert wa.get('rel') == ['noopener', 'noreferrer'], "WhatsApp should have rel=noopener noreferrer"

assert tg.get('target') == '_blank', "Telegram should have target=_blank"
assert tg.get('rel') == ['noopener', 'noreferrer'], "Telegram should have rel=noopener noreferrer"

assert em.get('target') is None, "Email should not have target=_blank to prevent empty tab"
assert em.get('rel') == ['noopener', 'noreferrer'], "Email should have rel=noopener noreferrer"

# Check JS showResult function implementation in script
assert 'document.getElementById(\'share-wa\').href = `https://api.whatsapp.com/send?text=${shareText}%0A${encodedUrl}`;' in html
assert 'document.getElementById(\'share-tg\').href = `https://t.me/share/url?url=${encodedUrl}&text=${shareText}`;' in html
assert 'document.getElementById(\'share-em\').href = `mailto:?subject=${encodeURIComponent(\'Shared PDF: \' + filename)}&body=${shareText}%0A%0A${encodedUrl}`;' in html

# Check guard listener
assert 'showToast(\'Please upload a PDF first to generate a share link.\', \'info\');' in html

print("\n✅ All PDF-to-Link social share button checks PASSED!")
