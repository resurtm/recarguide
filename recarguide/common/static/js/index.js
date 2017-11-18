require('bootstrap');
require('font-awesome/scss/font-awesome.scss');
require('jquery-ui/themes/base/slider.css');
require('jquery-ui/themes/base/autocomplete.css');
require('jquery-ui/themes/base/theme.css');

require('../sass/main.scss');

require('jquery-ui/ui/widget');
require('jquery-ui/ui/widgets/slider');
require('jquery-ui/ui/widgets/autocomplete');

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
require('./sale-make-model-trim-fields');
require('./sale-category-fields');
require('./sale-photos');
require('./search');
