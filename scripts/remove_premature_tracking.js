const fs = require('fs');
const path = require('path');

const publicDir = path.join(__dirname, '..', 'public');

function getHtmlFiles(dir) {
  let results = [];
  const list = fs.readdirSync(dir);
  list.forEach(file => {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);
    if (stat && stat.isDirectory()) {
      results = results.concat(getHtmlFiles(fullPath));
    } else if (file.endsWith('.html') && !file.endsWith('.bak')) {
      results.push(fullPath);
    }
  });
  return results;
}

const files = getHtmlFiles(publicDir);
console.log(`Found ${files.length} HTML files to process.`);

let processedCount = 0;

files.forEach(filePath => {
  let content = fs.readFileSync(filePath, 'utf8');
  const original = content;

  // 1. Remove Google tag (gtag.js) block
  content = content.replace(/\s*<!--\s*Google tag \(gtag\.js\)\s*-->\s*<script\b[^>]*src=["']https:\/\/www\.googletagmanager\.com\/gtag\/js\?id=[^"']*["'][^>]*>[\s\S]*?<\/script>\s*<script>[\s\S]*?gtag\(['"]config['"],\s*['"]G-[A-Z0-9]+['"]\);\s*<\/script>/gi, '');

  // Catch any alternative formatting of gtag block
  content = content.replace(/<script\b[^>]*src=["']https:\/\/www\.googletagmanager\.com\/gtag\/js\?id=[^"']*["'][^>]*>[\s\S]*?<\/script>\s*/gi, '');
  content = content.replace(/<script>[\s\r\n]*window\.dataLayer[\s\S]*?gtag\(['"]config['"],\s*['"]G-[A-Z0-9]+['"]\);[\s\r\n]*<\/script>\s*/gi, '');

  // 2. Remove AdSense script tag (keeping the meta tag if present)
  content = content.replace(/\s*<script\b[^>]*src=["']https:\/\/pagead2\.googlesyndication\.com\/pagead\/js\/adsbygoogle\.js\?client=ca-pub-[0-9]+["'][^>]*><\/script>/gi, '');

  // Clean up duplicate empty comments if any
  content = content.replace(/<!--\s*Google tag \(gtag\.js\)\s*-->\s*/gi, '');

  if (content !== original) {
    fs.writeFileSync(filePath, content, 'utf8');
    processedCount++;
    console.log(`✅ Stripped premature tracking from: ${path.relative(publicDir, filePath)}`);
  } else {
    console.log(`ℹ️ No changes needed in: ${path.relative(publicDir, filePath)}`);
  }
});

console.log(`\n🎉 Processed ${processedCount}/${files.length} HTML files.`);
