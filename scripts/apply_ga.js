const fs = require('fs');
const path = require('path');

const publicDir = path.join(__dirname, '..', 'public');

const gaTag = `  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-9EK2GY31YP" id="ga-script"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-9EK2GY31YP');
  </script>
`;

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

  // 1. Remove any existing Google tag comments or scripts
  content = content.replace(/<!--\s*Google tag \(gtag\.js\)\s*-->\s*/gi, '');
  content = content.replace(/<script\b[^>]*src=["']https:\/\/www\.googletagmanager\.com\/gtag\/js\?id=[^"']*["'][^>]*>[\s\S]*?<\/script>\s*/gi, '');
  content = content.replace(/<script>[\s\r\n]*window\.dataLayer[\s\S]*?gtag\('config',\s*['"]G-[A-Z0-9]+['"]\);[\s\r\n]*<\/script>\s*/gi, '');

  // 2. Insert the new Google tag right after <head>
  if (/<head\b[^>]*>/i.test(content)) {
    content = content.replace(/(<head\b[^>]*>)/i, `$1\n${gaTag}`);
    fs.writeFileSync(filePath, content, 'utf8');
    updatedCount++;
    console.log(`✅ Injected GA4 into: ${path.relative(publicDir, filePath)}`);
  } else {
    console.warn(`⚠️ No <head> tag found in: ${filePath}`);
  }
});

console.log(`\n🎉 Successfully updated Google Tag in ${updatedCount}/${files.length} HTML files.`);
