var fs = require('fs');
var execSync = require('child_process').execSync;

var MSYSTEM = process.env['MSYSTEM'];

if (MSYSTEM === 'MINGW64') {
  try {
    execSync(`sh util/msys64_preinstall.sh`, {stdio:'ignore'});
    process.stdout.write('true');
  } catch(err) {
    return false;
  }
} else {
  return false;
}
