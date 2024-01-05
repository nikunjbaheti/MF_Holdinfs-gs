const axios = require('axios');
const fs = require('fs');

async function executeScript() {
  try {
    const response = await axios.get('https://www.rupeevest.com/assets/application-2f79500676a1b61911cb11a9c0c1d5bc8e40775cac17fd2f97a0e78c4083f3ee.js');
    
    // Parse, manipulate, or use the response data as needed
    const outputData = response.data;

    // Write the output to a CSV file
    fs.writeFileSync('output.csv', outputData, 'utf-8');

    console.log('Script executed successfully.');
  } catch (error) {
    console.error('Error executing the script:', error.message);
    process.exit(1);
  }
}

executeScript();
