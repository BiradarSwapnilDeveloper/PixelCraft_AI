const fs = require('fs');
const path = require('path');

const publicDir = path.join(__dirname, '..', 'public');

const adsenseMeta = '<meta name="google-adsense-account" content="ca-pub-3788374704176398">';
const adsenseScript = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3788374704176398"\n     crossorigin="anonymous" id="adsense-script"></script>';

const adsenseBlock = `\n  <!-- Google AdSense -->\n  ${adsenseMeta}\n  ${adsenseScript}\n`;

function getHtmlFiles(dir) {
  let results = [];
  const list = fs.readdirSync(dir);
  list.forEach(file => {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);
    if (stat && stat.isDirectory()) {
      results = results.concat(getHtmlFiles(fullPath));
    } else if (file.endsWith('.html')) {
      results.push(fullPath);
    }
  });
  return results;
}

const files = getHtmlFiles(publicDir);
console.log(`Found ${files.length} HTML files in public directory.`);

let updatedCount = 0;

files.forEach(filePath => {
  let content = fs.readFileSync(filePath, 'utf8');

  // 1. Clean out any previous AdSense comments, meta tags, and script tags
  content = content.replace(/<!--\s*Google AdSense\s*-->\s*/gi, '');
  content = content.replace(/<meta\s+name=["']google-adsense-account["'][^>]*>\s*/gi, '');
  content = content.replace(/<script\b[^>]*src=["']https:\/\/pagead2\.googlesyndication\.com\/[^"']*["'][^>]*>[\s\S]*?<\/script>\s*/gi, '');

  // 2. Insert the fresh AdSense block right inside <head>
  if (/<head\b[^>]*>/i.test(content)) {
    content = content.replace(/(<head\b[^>]*>)/i, `$1${adsenseBlock}`);
    fs.writeFileSync(filePath, content, 'utf8');
    updatedCount++;
    console.log(`✅ Injected AdSense into: ${path.relative(publicDir, filePath)}`);
  } else {
    console.warn(`⚠️ No <head> tag found in: ${filePath}`);
  }
});

console.log(`\n🎉 Successfully injected AdSense into ${updatedCount}/${files.length} HTML files.`);
