const axios = require('axios');
const fs = require('fs');

async function executeScript() {
  try {
    const response = await axios.get('https://www.rupeevest.com/assets/application-2f79500676a1b61911cb11a9c0c1d5bc8e40775cac17fd2f97a0e78c4083f3ee.js');
    
    // Save the output to Output.js
    fs.writeFileSync('Output.js', response.data, 'utf-8');

    console.log('Script output saved as Output.js.');

    // Now execute the saved script
    require('./Output.js');

    console.log('Script executed successfully.');
  } catch (error) {
    console.error('Error executing the script:', error.message);
    process.exit(1);
  }
}

executeScript();
