var fs = require('fs')

var MSYSTEM = process.env['MSYSTEM2'];

return (MSYSTEM === 'MINGW64');
