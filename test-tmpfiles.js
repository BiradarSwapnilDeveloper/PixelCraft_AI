const fs = require('fs');

async function testTmpFiles() {
  try {
    const dummyPdf = Buffer.from('%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> /MediaBox [0 0 612 792] /Contents 5 0 R >>\nendobj\n4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n5 0 obj\n<< /Length 44 >>\nstream\nBT\n/F1 24 Tf\n100 700 Td\n(Hello World) Tj\nET\nendstream\nendobj\nxref\n0 6\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000219 00000 n \n0000000307 00000 n \ntrailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n402\n%%EOF');
    
    const formData = new globalThis.FormData();
    formData.append('file', new Blob([dummyPdf], { type: 'application/pdf' }), 'test.pdf');

    console.log("Uploading to tmpfiles.org...");
    const response = await fetch('https://tmpfiles.org/api/v1/upload', {
      method: 'POST',
      body: formData,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
      }
    });

    if (!response.ok) {
      console.log("Response not OK:", response.status, response.statusText);
      return;
    }
    const data = await response.json();
    console.log("Success! URL:", data.data.url);
    // tmpfiles.org returns a download page. We can rewrite it to direct link by adding dl/
    const directUrl = data.data.url.replace('tmpfiles.org/', 'tmpfiles.org/dl/');
    console.log("Direct URL:", directUrl);
  } catch (err) {
    console.error("Error:", err);
  }
}

testTmpFiles();
