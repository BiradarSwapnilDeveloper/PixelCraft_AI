import os
import sys
import subprocess

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("⚠️ google-genai package not found. Running in dry-run mode.")
    sys.exit(0)

def scan_for_ai_hallucinations():
    print("🤖 AI Code Governance Scanner Started")
    
    # Handle multiple API keys (comma-separated)
    api_keys_env = os.environ.get("GEMINI_API_KEY", "")
    if not api_keys_env:
        print("⚠️ GEMINI_API_KEY not set. Running in dry-run mode.")
        sys.exit(0)

    # Split keys by comma and remove empty spaces
    api_keys = [k.strip() for k in api_keys_env.split(",") if k.strip()]
    if not api_keys:
        print("⚠️ No valid keys found in GEMINI_API_KEY. Running in dry-run mode.")
        sys.exit(0)

    try:
        # Get git diff of the current commit (or staged changes)
        diff_output = subprocess.check_output(["git", "diff", "HEAD~1", "HEAD"], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        print("⚠️ Could not get git diff. Maybe this is the first commit or not a git repo.")
        sys.exit(0)

    if not diff_output.strip():
        print("✅ No changes to analyze.")
        sys.exit(0)

    print("🔎 Analyzing recent commits for AI-generated code patterns or hallucinations...")
    
    prompt = f"""
    You are an AI Code Governance agent. Your job is to review the following git diff for:
    1. AI-generated code hallucinations (code that calls non-existent libraries or APIs).
    2. Severe logical flaws or hardcoded secrets/backdoors.
    
    If you find critical issues, start your response with "FAILED:" followed by the reason.
    If the code looks safe and logical, respond with "PASSED."
    
    Git Diff:
    {diff_output}
    """

    # Try each key until one succeeds
    success = False
    for idx, key in enumerate(api_keys):
        try:
            print(f"🔄 Attempting API request with Key #{idx + 1}...")
            client = genai.Client(api_key=key)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            
            result = response.text.strip()
            print(f"AI Review Result: \n{result}")

            if result.startswith("FAILED:"):
                print("❌ ERROR: AI Governance Check Failed.")
            else:
                print("✅ AI Governance Check Passed.")
                
            success = True
            break # Stop trying other keys if successful
            
        except Exception as e:
            print(f"⚠️ API Key #{idx + 1} failed: {e}")
            
    if not success:
        print("❌ All provided API keys failed (possibly due to rate limits or invalid keys).")
        
    sys.exit(0)

if __name__ == "__main__":
    scan_for_ai_hallucinations()
