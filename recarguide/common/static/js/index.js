require('bootstrap-loader');
require('font-awesome/scss/font-awesome.scss');

require('../sass/main.scss');

require('imports-loader?define=>false!jquery-ui/ui/widget.js');
require('imports-loader?define=>false!blueimp-load-image/js/load-image.all.min.js');
require('imports-loader?define=>false!blueimp-canvas-to-blob/js/canvas-to-blob.js');
require('imports-loader?define=>false!blueimp-file-upload/js/jquery.iframe-transport.js');
require('imports-loader?define=>false!blueimp-file-upload/js/jquery.fileupload.js');
require('imports-loader?define=>false!blueimp-file-upload/js/jquery.fileupload-process.js');
require('imports-loader?define=>false!blueimp-file-upload/js/jquery.fileupload-image.js');
// require('imports-loader?define=>false!blueimp-file-upload/js/jquery.fileupload-audio.js');
// require('imports-loader?define=>false!blueimp-file-upload/js/jquery.fileupload-video.js');
require('imports-loader?define=>false!blueimp-file-upload/js/jquery.fileupload-validate.js');

require('./utils');
require('./package-selector');
require('./sale-make-model-fields');
require('./sale-category-fields');
require('./sale-photos');
