const fs = require('fs');

async function testFileIO() {
  try {
    const dummyPdf = Buffer.from('%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> /MediaBox [0 0 612 792] /Contents 5 0 R >>\nendobj\n4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n5 0 obj\n<< /Length 44 >>\nstream\nBT\n/F1 24 Tf\n100 700 Td\n(Hello World) Tj\nET\nendstream\nendobj\nxref\n0 6\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000219 00000 n \n0000000307 00000 n \ntrailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n402\n%%EOF');
    
    const formData = new globalThis.FormData();
    formData.append('file', new Blob([dummyPdf], { type: 'application/pdf' }), 'test.pdf');

    console.log("Uploading to file.io...");
    const response = await fetch('https://file.io', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      console.log("Response not OK:", response.status, response.statusText);
      const text = await response.text();
      console.log("Response text:", text);
      return;
    }
    const data = await response.json();
    console.log("Success! URL:", data.link);
  } catch (err) {
    console.error("Error:", err);
  }
}

testFileIO();
