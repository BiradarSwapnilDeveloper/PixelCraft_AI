// Helper script to view MongoDB data directly from terminal
const dns = require('dns');
try {
  dns.setDefaultResultOrder('ipv4first');
  dns.setServers(['8.8.8.8', '8.8.4.4']); // Bypass ISP SRV DNS block
} catch (e) {}

require('dotenv').config();
const mongoose = require('mongoose');

async function main() {
  const collectionArg = process.argv[2] ? process.argv[2].toLowerCase() : null;

  try {
    process.stdout.write('Connecting to MongoDB Atlas...\r');
    await mongoose.connect(process.env.MONGO_URI, { serverSelectionTimeoutMS: 8000 });
    console.log('Connected to Database: pixelcraft (MongoDB Atlas)\n');

    const db = mongoose.connection.db;
    const collections = await db.listCollections().toArray();

    if (!collectionArg) {
      console.log('📊 === COLLECTIONS SUMMARY ===');
      for (const col of collections) {
        const count = await db.collection(col.name).countDocuments();
        console.log(` • ${col.name.padEnd(20)} : ${count} documents`);
      }
      console.log('\n💡 Tip: To view data of a specific collection, run:');
      console.log('   node scripts/view_db.js <collection_name>');
      console.log('   Example: node scripts/view_db.js users\n');
    } else {
      const match = collections.find(c => c.name.toLowerCase() === collectionArg);
      if (!match) {
        console.log(`❌ Collection "${collectionArg}" nahi mili.`);
        console.log('Available collections:', collections.map(c => c.name).join(', '));
      } else {
        const docs = await db.collection(match.name).find({}).sort({ _id: -1 }).limit(10).toArray();
        console.log(`📄 === LATEST DOCUMENTS IN [${match.name}] (Showing up to 10) ===\n`);
        console.log(JSON.stringify(docs, null, 2));
      }
    }

    await mongoose.disconnect();
    process.exit(0);
  } catch (err) {
    console.error('\n❌ MongoDB Connection Error:', err.message);
    process.exit(1);
  }
}

main();
