const fs = require('fs');
const path = require('path');
// Uses existing public/js/cookie-consent.js

function walk(d) {
  fs.readdirSync(d).forEach(f => {
    const p = path.join(d,f);
    if(fs.statSync(p).isDirectory()) walk(p);
    else if(p.endsWith('.html')) {
      let content = fs.readFileSync(p, 'utf8');
      
      // Remove GA script block
      content = content.replace(/<!-- Google tag \(gtag\.js\) -->[\s\S]*?gtag\('config',\s*'G-[A-Z0-9]+'\);\s*<\/script>/g, '');
      
      // Remove AdSense script block
      content = content.replace(/<!-- Google AdSense -->[\s\S]*?<script async src="https:\/\/pagead2\.googlesyndication\.com\/pagead\/js\/adsbygoogle\.js\?client=ca-pub-[0-9]+"[^>]*><\/script>/g, '');
      
      // Add cookie consent script if not there
      if(!content.includes('cookie-consent.js')) {
        const relPath = p.replace(path.join(process.cwd(), 'public'), '').replace(/^\\/, '').replace(/^\//, '');
        const depth = relPath.split(path.sep).length - 1;
        const prefix = depth === 0 ? './' : '../'.repeat(depth);
        const scriptTag = `<script src="${prefix}js/cookie-consent.js"></script>\n</body>`;
        content = content.replace('</body>', scriptTag);
      }
      
      fs.writeFileSync(p, content);
    }
  });
}

walk(path.join(process.cwd(), 'public'));
console.log('Cookie consent injected successfully.');
