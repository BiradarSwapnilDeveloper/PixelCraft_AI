import os
import sys

def add_tool_to_index():
    index_path = r"d:\AI tools Website\public\index.html"
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if tool already exists
    if "ai-dubbing.html" in content:
        print("Tool already exists in index.html")
        return

    # Find the end of the tools grid to insert the new tool card
    # A good place to insert it is after the "Digital Fingerprint Wiper" or at the end of the "ai" cat
    card_html = """
        <!-- AI VIDEO/AUDIO DUBBING TOOL -->
        <a href="tools/ai-dubbing.html" class="tool-card premium-floating-card" data-cat="ai" style="position: relative; padding-bottom: 20px; border: 1px solid rgba(236, 72, 153, 0.4); box-shadow: 0 0 15px rgba(236, 72, 153, 0.1); background: linear-gradient(145deg, #2e1026, #3b0f2d);">
          <div class="tool-badge" style="background: #ec4899; color: white; font-weight: bold; position: absolute; top: -10px; right: 0px;">✨ NEW</div>
          <div class="tool-icon" style="font-size: 2.8rem; text-shadow: 0 0 15px rgba(236, 72, 153, 0.4); margin-top: 15px;">🎙️</div>
          <h3 style="color: #f9a8d4; font-size: 1.3rem;">AI Audio & Video Dubbing</h3>
          <p style="font-size: 0.95rem; color: var(--text-muted); font-weight: 400; line-height: 1.6;">
            Dub any audio or video into multiple languages instantly using advanced AI voice cloning and translation. 
          </p>
          <div class="tool-arrow default-launch-btn" style="font-weight: bold; margin-top: auto; color: #f9a8d4;">Launch Tool →</div>
        </a>
"""
    
    # We will inject this before the Closing of tools-grid.
    # Searching for <div class="tools-grid" id="tools-grid">
    if '<div class="tools-grid" id="tools-grid">' in content:
        split_point = content.find('<div class="tools-grid" id="tools-grid">') + len('<div class="tools-grid" id="tools-grid">')
        new_content = content[:split_point] + "\n" + card_html + content[split_point:]
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Added tool card to index.html")
    else:
        print("Could not find tools grid in index.html")

def add_endpoint_to_server():
    server_path = r"d:\AI tools Website\server.js"
    with open(server_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if "/api/dub-media" in content:
        print("Endpoint already exists in server.js")
        return

    endpoint_code = """
// ===== AI VIDEO/AUDIO DUBBING ENDPOINT (MOCKUP FOR NOW) =====
const dubUpload = multer({ 
    storage: multer.memoryStorage(),
    limits: { fileSize: 100 * 1024 * 1024 } // 100MB limit for video/audio
});

app.post('/api/dub-media', dubUpload.single('file'), async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ error: "No file uploaded" });
        }
        
        const { targetLanguage } = req.body;
        if (!targetLanguage) {
            return res.status(400).json({ error: "Target language is required" });
        }

        console.log(`Received dubbing request for file: ${req.file.originalname} to ${targetLanguage}`);
        
        // TODO: Integrate actual API here (e.g. ElevenLabs / HuggingFace SeamlessM4T)
        // using req.file.buffer
        
        // Mock processing delay
        await new Promise(resolve => setTimeout(resolve, 3000));

        // For this mockup, we'll just return the original file as the "dubbed" file
        // In reality, you'd return the processed audio/video buffer from the API
        const base64Media = req.file.buffer.toString('base64');
        const mimeType = req.file.mimetype;
        
        res.json({ 
            success: true, 
            message: `Successfully dubbed into ${targetLanguage}`,
            mediaUrl: `data:${mimeType};base64,${base64Media}` 
        });

    } catch (err) {
        console.error("AI Dubbing Error:", err.message);
        res.status(500).json({ error: "Failed to process media dubbing" });
    }
});
"""
    # Insert it before the Catch-All or at the end
    # Let's insert it before `app.use('/tools',` or before `app.get('/website-evolution-report.html'`
    insert_str = "// Technical Evolution Report Routes"
    if insert_str in content:
        new_content = content.replace(insert_str, endpoint_code + "\n" + insert_str)
        with open(server_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Added endpoint to server.js")
    else:
        print("Could not find place to insert in server.js")

if __name__ == "__main__":
    add_tool_to_index()
    add_endpoint_to_server()
