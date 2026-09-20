const fs = require('fs');
const { execSync } = require('child_process');

const SECRET_PATTERNS = [
  new RegExp('AKIA[0-9A-Z]{16}'), // AWS Access Key ID
  new RegExp('sk-[a-zA-Z0-9]{32,}'), // OpenAI / Stripe Secret Key
  new RegExp('-{5}BEGIN RSA PRIVATE KEY-{5}'), // RSA Private Key
  new RegExp('ghp_[a-zA-Z0-9]{36}'), // GitHub Personal Access Token
  new RegExp('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9\\.') // JWT Token (HS256)
];

console.log('🔍 Running Pre-commit Secret Scanner...');

try {
  // Get staged files
  const stagedFiles = execSync('git diff --cached --name-only --diff-filter=ACM', { encoding: 'utf-8' })
    .split('\n')
    .filter(file => file.trim() !== '');

  let foundSecrets = false;

  stagedFiles.forEach(file => {
    if (fs.existsSync(file)) {
      const content = fs.readFileSync(file, 'utf-8');
      const lines = content.split('\n');

      lines.forEach((line, index) => {
        for (const pattern of SECRET_PATTERNS) {
          if (pattern.test(line)) {
            console.error(`🚨 SECRET DETECTED in ${file} (Line ${index + 1})`);
            console.error(`=> Found pattern matching: ${pattern.toString()}`);
            foundSecrets = true;
          }
        }
      });
    }
  });

  if (foundSecrets) {
    console.error('❌ Commit blocked! Please remove the secrets before committing.');
    process.exit(1); // Block commit
  } else {
    console.log('✅ No secrets found. Proceeding with commit.');
    process.exit(0);
  }
} catch (error) {
  console.error('Error running secret scanner:', error);
  process.exit(1);
}
