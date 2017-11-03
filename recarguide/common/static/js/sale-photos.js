jQuery(function ($) {
  var field = $('#sale-photos');
  if (field.length === 0) {
    return;
  }

  var preview = $('#sale-photos-preview');
  var listingForm = $('#listing-form');

  field.fileupload({
    url: '/sale/upload-photo/',
    acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
    maxFileSize: 10000000, // 10 megabytes
    disableImageResize: /Android(?!.*Chrome)|Opera/.test(window.navigator.userAgent),
    previewMaxWidth: 125,
    previewMaxHeight: 125,
    previewCrop: true
  })
    .on('fileuploadadd', add)
    .on('fileuploadprocessalways', processAlways)
    .on('fileuploadprogressall', progressAll)
    .on('fileuploaddone', done)
    .on('fileuploadfail', fail);

  function add(e, data) {
    $.each(data.files, function (index, file) {
      $('<div><i class="fa fa-times-circle" aria-hidden="true" title="Delete Photo"></i></div>')
        .attr({'data-local-id': getID(file), 'data-ready': '0', 'data-real-id': ''})
        .appendTo(preview);
    });
  }

  function processAlways(e, data) {
    var file = data.files[data.index];
    var node = preview.find('[data-local-id=' + getID(file) + ']');
    if (node.attr('data-ready') === '1') {
      return;
    }
    node.attr('data-ready', '1');
    if (file.preview) {
      node.append(file.preview);
    }
    if (file.error) {
      // todo: process error here
    }
  }

  function progressAll(e, data) {
    // todo: process progress here
  }

  function done(e, data) {
    var file = data.files[0];
    var node = preview.find('[data-local-id=' + getID(file) + ']');
    node.attr('data-real-id', parseInt(data.result, 10));
  }

  function fail(e, data) {
    // todo: process error here
  }

  function getID(file) {
    return btoa(file.name + file.lastModified).replace(/[^0-9a-z]/gi, '');
  }

  preview.on('click', 'i', function () {
    var node = $(this).closest('div');
    $.ajax({
      url: '/sale/delete-photo/',
      data: {
        id: node.attr('data-real-id'),
        csrfmiddlewaretoken: listingForm.find('[name=csrfmiddlewaretoken]').val()
      },
      method: 'POST',
      success: function (resp) {
        node.remove();
      }
    })
  });
});
