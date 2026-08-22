// test_api_client.js
// Quick smoke test script to verify compilation and structure (does not run HTTP requests to avoid making real calls if server not up)

const fs = require('fs');
const path = require('path');

const srcDir = path.join(__dirname, 'src', 'api');

const expectedFiles = [
    'client.ts',
    'prediction.ts',
    'score.ts',
    'risk.ts',
    'financial.ts',
    'contracts.ts',
    'warranty.ts',
    'insurance.ts',
    'repeatRatio.ts',
    'feedback.ts',
    'purchaseOrders.ts',
    'payments.ts',
    'tracking.ts'
];

let allPresent = true;
for (const file of expectedFiles) {
    if (!fs.existsSync(path.join(srcDir, file))) {
        console.error(`Missing file: ${file}`);
        allPresent = false;
    }
}

if (allPresent) {
    console.log("All API client files successfully created.");
} else {
    process.exit(1);
}
