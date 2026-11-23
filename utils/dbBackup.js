const fs = require('fs');
const path = require('path');
const mongoose = require('mongoose');
const { sendTelegramAlert } = require('./telegramAlert');

async function runDailyBackup() {
  try {
    if (mongoose.connection.readyState !== 1) {
      console.warn('⚠️ MongoDB not connected, skipping backup.');
      return;
    }

    const backupDir = path.join(__dirname, '..', 'backups');
    if (!fs.existsSync(backupDir)) {
      fs.mkdirSync(backupDir, { recursive: true });
    }

    const timestamp = new Date().toISOString().split('T')[0];
    const backupFile = path.join(backupDir, `backup-${timestamp}.json`);

    const db = mongoose.connection.db;
    const collectionsToBackup = ['users', 'contactmessages', 'traplogs', 'forensiclogs', 'toolsuggestions'];
    const backupData = {
      createdAt: new Date().toISOString(),
      collections: {}
    };

    for (const colName of collectionsToBackup) {
      try {
        const docs = await db.collection(colName).find({}).limit(1000).toArray();
        backupData.collections[colName] = docs;
      } catch (colErr) {
        backupData.collections[colName] = [];
      }
    }

    const jsonString = JSON.stringify(backupData, null, 2);
    fs.writeFileSync(backupFile, jsonString, 'utf8');
    const sizeKb = Math.round(jsonString.length / 1024);

    console.log(`💾 Daily MongoDB backup created successfully: ${backupFile} (${sizeKb} KB)`);

    // Retain last 30 daily backups (30-day retention window)
    const files = fs.readdirSync(backupDir)
      .filter(f => f.startsWith('backup-') && f.endsWith('.json'))
      .sort();
    if (files.length > 30) {
      const toDelete = files.slice(0, files.length - 30);
      for (const oldFile of toDelete) {
        fs.unlinkSync(path.join(backupDir, oldFile));
      }
    }

    sendTelegramAlert(`💾 <b>Daily Database Backup Completed!</b>\n\n📅 <b>Date:</b> ${timestamp}\n📦 <b>Size:</b> ${sizeKb} KB\n📂 <b>Snapshot:</b> users, contactmessages, traplogs\n🛡️ <b>Retention:</b> 30 Days Rolling Window`);
  } catch (err) {
    console.error('❌ Daily database backup error:', err.message);
  }
}

module.exports = { runDailyBackup };
