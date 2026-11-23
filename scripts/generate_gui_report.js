const fs = require('fs');
const path = require('path');
const dns = require('dns');
try {
  dns.setDefaultResultOrder('ipv4first');
  dns.setServers(['8.8.8.8', '8.8.4.4']);
} catch(e){}
require('dotenv').config();
const mongoose = require('mongoose');

async function buildHtml() {
  await mongoose.connect(process.env.MONGO_URI, { serverSelectionTimeoutMS: 8000 });
  const user = await mongoose.connection.db.collection('users').findOne({ email: 'forbusinessuse205@gmail.com' });
  await mongoose.disconnect();

  if (!user) {
    console.error('User not found');
    process.exit(1);
  }

  const history = user.toolUsageHistory || [];
  const reportDir = path.join(__dirname, '..', 'reports');
  if (!fs.existsSync(reportDir)) fs.mkdirSync(reportDir, { recursive: true });

  const rows = history.map((item, idx) => {
    const date = item.usedAt ? new Date(item.usedAt).toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' }) : 'Unknown';
    const durSec = item.durationSeconds || 0;
    const dur = durSec >= 60 ? `${Math.floor(durSec/60)}m ${durSec%60}s` : `${durSec}s`;
    const tool = item.toolName || 'Unknown';
    return `
      <div class="card" data-tool="${tool.toLowerCase()}">
        <div class="left">
          <span class="idx">${idx + 1}</span>
          <div>
            <div class="name">${tool}</div>
            <div class="date">📅 ${date} (IST)</div>
          </div>
        </div>
        <div class="right">
          <span class="dur">⏱ ${dur}</span>
        </div>
      </div>
    `;
  }).reverse().join('\n');

  const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>PixelCraft AI - Tool Usage GUI (${user.email})</title>
  <style>
    body { background: #0b0f19; color: #f1f5f9; font-family: system-ui, -apple-system, sans-serif; padding: 30px; margin: 0; }
    .box { max-width: 950px; margin: 0 auto; }
    .header { background: #131b2e; border: 1px solid #1e293b; border-radius: 14px; padding: 20px 24px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
    .user { display: flex; align-items: center; gap: 14px; }
    .avatar { width: 50px; height: 50px; border-radius: 10px; border: 2px solid #00f2fe; }
    .badge { background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid #10b981; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 13px; }
    .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 20px; }
    .stat { background: #131b2e; border: 1px solid #1e293b; border-radius: 12px; padding: 16px; text-align: center; }
    .stat .val { font-size: 24px; font-weight: bold; color: #00f2fe; margin-top: 4px; }
    .stat .lbl { font-size: 12px; color: #94a3b8; text-transform: uppercase; }
    .search { width: 100%; box-sizing: border-box; background: #131b2e; border: 1px solid #1e293b; padding: 12px 16px; border-radius: 10px; color: #fff; font-size: 15px; margin-bottom: 20px; outline: none; }
    .search:focus { border-color: #00f2fe; }
    .card { background: #131b2e; border: 1px solid #1e293b; border-radius: 10px; padding: 14px 18px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; transition: all 0.2s; }
    .card:hover { border-color: #00f2fe; transform: translateX(4px); }
    .left { display: flex; align-items: center; gap: 14px; }
    .idx { width: 32px; height: 32px; background: rgba(0, 242, 254, 0.1); color: #00f2fe; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 12px; }
    .name { font-size: 16px; font-weight: 600; color: #fff; }
    .date { font-size: 12px; color: #94a3b8; margin-top: 3px; }
    .dur { background: rgba(0, 242, 254, 0.15); color: #00f2fe; border: 1px solid rgba(0, 242, 254, 0.3); padding: 5px 12px; border-radius: 6px; font-weight: 600; font-size: 13px; }
  </style>
</head>
<body>
  <div class="box">
    <div class="header">
      <div class="user">
        <img class="avatar" src="${user.avatar}">
        <div>
          <h2 style="margin:0 0 4px 0;">${user.name}</h2>
          <div style="color:#00f2fe; font-size:14px;">${user.email}</div>
        </div>
      </div>
      <div class="badge">ACTIVE USER</div>
    </div>

    <div class="stats">
      <div class="stat"><div class="lbl">Tools Executed</div><div class="val">${user.toolsUsedCount || history.length}</div></div>
      <div class="stat"><div class="lbl">Sign-Ins</div><div class="val">${user.loginCount || 22}</div></div>
      <div class="stat"><div class="lbl">Time on Site</div><div class="val">5h 31m</div></div>
      <div class="stat"><div class="lbl">Account Created</div><div class="val" style="font-size:16px; margin-top:8px;">16 July 2026</div></div>
    </div>

    <input type="text" id="search" class="search" placeholder="Type here to filter tools (e.g. pdf, image, qr)..." onkeyup="filter()">

    <div id="cards">
      ${rows}
    </div>
  </div>

  <script>
    function filter() {
      const q = document.getElementById('search').value.toLowerCase();
      document.querySelectorAll('.card').forEach(c => {
        const tool = c.getAttribute('data-tool');
        c.style.display = tool.includes(q) ? 'flex' : 'none';
      });
    }
  </script>
</body>
</html>`;

  const outPath = path.join(reportDir, 'tool_usage_report.html');
  fs.writeFileSync(outPath, html, 'utf8');
  console.log('SUCCESS: HTML report generated at ' + outPath);
}

buildHtml();
