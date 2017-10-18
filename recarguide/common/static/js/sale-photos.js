jQuery(function ($) {
  var field = $('#sale-photos');
  if (field.length === 0) {
    return;
  }

  var preview = $('#sale-photos-preview');

  field.fileupload({
    url: '/sale/upload-photos/',
    acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
    maxFileSize: 10000000, // 10 megabytes
    disableImageResize: /Android(?!.*Chrome)|Opera/.test(window.navigator.userAgent),
    previewMaxWidth: 125,
    previewMaxHeight: 125,
    // autoUpload: false,
    previewCrop: true
  })
    .on('fileuploadadd', add)
    .on('fileuploadprocessalways', processalways)
    .on('fileuploadprogressall', progressall)
    .on('fileuploaddone', done)
    .on('fileuploadfail', fail);

  function add(e, data) {
    $.each(data.files, function (index, file) {
      $('<div/>').attr('data-id', generateID(file)).appendTo(preview);
    });
  }

  function processalways(e, data) {
    var index = data.index;
    var file = data.files[index];
    var node = preview.find('[data-id=' + generateID(file) + ']');

    if (node.attr('data-ready') === '1') {
      return;
    }
    node.attr('data-ready', '1');

    if (file.preview) {
      node.prepend(file.preview);
    }
    if (file.error) {
      // todo: mark error here
    }
  }

  function progressall(e, data) {
    console.log('progressall');
    console.log(data);
  }

  function done(e, data) {
    console.log('done');
    console.log(data);
  }

  function fail(e, data) {
    console.log('fail');
    console.log(data);
  }

  function generateID(file) {
    return btoa(file.name + file.lastModified).replace(/[^0-9a-z]/gi, '');
  }
});
