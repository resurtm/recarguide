jQuery(function ($) {
  var field = $('#sale-photos');
  if (field.length === 0) {
    return;
  }

  field.fileupload({
    url: '/sale/upload-photos/',
    done: function (e, data) {
      console.log(data);
      $.each(data.result.files, function (index, file) {
        console.log(file);
      });
    }
  });
});
