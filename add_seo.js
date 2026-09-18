const fs = require('fs');
const path = require('path');

const seoContent = `
<!-- MASSIVE SEO CONTENT FOR MONETIZATION -->
<section style="max-width: 1200px; margin: 50px auto; padding: 40px; background: rgba(15, 23, 42, 0.5); border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); color: #94a3b8; line-height: 1.8; font-family: 'Inter', sans-serif;">
  <h2 style="color: #f8fafc; font-size: 1.8rem; margin-bottom: 20px;">Comprehensive Guide to Digital Security & Privacy</h2>
  <p style="margin-bottom: 15px;">In the modern digital age, safeguarding your personal and professional data is not just an option—it is an absolute necessity. With the exponential rise in cyber threats, mass surveillance, and automated data scraping, protecting your digital footprint requires advanced, decentralized tools. Our browser-based security suite is engineered to provide military-grade cryptographic protection without compromising on usability or performance. By leveraging cutting-edge WebAssembly (Wasm) architecture, we ensure that every computation, encryption, and metadata sanitation process occurs entirely on your local device. Your sensitive files never traverse the internet, guaranteeing absolute zero-knowledge privacy.</p>
  <p style="margin-bottom: 15px;">Whether you are a journalist operating in hostile environments, a security researcher analyzing malware payloads, or an everyday user looking to reclaim their digital anonymity, our toolset offers unparalleled capabilities. From deep EXIF data wiping that prevents unauthorized location tracking to sophisticated AES-256 steganography that hides critical information in plain sight, our tools are designed to neutralize tracking vectors proactively. We believe that robust digital privacy is a fundamental human right, and our mission is to democratize access to elite cryptographic utilities.</p>
  <p style="margin-bottom: 15px;">Understanding the mechanics of cyber hygiene is critical. For instance, when you share a photograph online, you are often unknowingly broadcasting your precise GPS coordinates, device identifiers, and timestamp data via hidden EXIF and IPTC tags. Threat actors and data brokers harvest this metadata to build comprehensive profiles of your daily habits. By utilizing our Forensic Image Sanitizer, you can surgically strip away these identifiers, embedding a cryptographic seal to ensure the file remains untampered and completely anonymous. Similarly, our steganographic tools employ complex algorithms like LSB (Least Significant Bit) manipulation to weave encrypted messages directly into the fabric of audio and video files, evading even the most rigorous statistical steganalysis.</p>
  <p style="margin-bottom: 15px;">As the landscape of cyber warfare evolves, so do our defensive capabilities. We are constantly researching and deploying next-generation countermeasures to combat emerging threats such as homograph attacks, deepfake proliferation, and AI-driven phishing campaigns. By integrating advanced heuristic scanners and machine learning models directly into your browser, we empower you to detect and neutralize threats in real-time. Stay secure, stay anonymous, and take full control of your digital life with our uncompromising privacy toolset.</p>
  <h3 style="color: #f8fafc; font-size: 1.5rem; margin-bottom: 15px; margin-top: 30px;">Why Client-Side Execution Matters</h3>
  <p>The traditional cloud computing model inherently compromises privacy by requiring data to be transmitted to remote servers. This introduces multiple points of vulnerability: data in transit can be intercepted, and data at rest can be breached or legally subpoenaed. By executing all logic—from image compression and format conversion to complex cryptographic encoding—within the secure sandbox of your web browser, we eliminate these vulnerabilities entirely. Your data is your property, and our tools ensure it stays that way.</p>
</section>
`;

function injectSEO(filePath) {
    let content = fs.readFileSync(filePath, 'utf8');
    
    // Prevent double injection
    if (content.includes('Comprehensive Guide to Digital Security & Privacy')) {
        console.log(`Skipped (already injected): ${filePath}`);
        return;
    }
    
    // Insert right before the footer or before </body>
    if (content.includes('<!-- FOOTER -->')) {
        content = content.replace('<!-- FOOTER -->', seoContent + '\n  <!-- FOOTER -->');
    } else if (content.includes('</main>')) {
        content = content.replace('</main>', seoContent + '\n</main>');
    } else if (content.includes('</body>')) {
        content = content.replace('</body>', seoContent + '\n</body>');
    } else {
        content += seoContent;
    }
    
    fs.writeFileSync(filePath, content);
    console.log(`Injected SEO content into: ${filePath}`);
}

// 1. Inject into index.html
const indexPath = path.join(__dirname, 'public', 'index.html');
if (fs.existsSync(indexPath)) injectSEO(indexPath);

// 2. Inject into all files in public/tools
const toolsDir = path.join(__dirname, 'public', 'tools');
if (fs.existsSync(toolsDir)) {
    const files = fs.readdirSync(toolsDir);
    files.forEach(file => {
        if (file.endsWith('.html')) {
            injectSEO(path.join(toolsDir, file));
        }
    });
}
