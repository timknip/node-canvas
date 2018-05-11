var fs = require('fs');
var execSync = require('child_process').execSync;

var MSYSTEM = process.env['MSYSTEM'];

if (MSYSTEM === 'MINGW64') {
  try {
    execSync('bash util/bundle.sh');
    execSync('rm depends*');
  } catch(err) {
    console.error(err);
  }
}
