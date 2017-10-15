jQuery(function ($) {
  var form = $('#listing-form');
  if (form.length === 0) {
    return;
  }

  var makeInput = form.find('#id_make');
  var modelInput = form.find('#id_model');

  makeInput.on('change', function () {
    $.ajax({
      url: '/sale/fetch-models/' + $(this).val() + '/',
      success: function (data) {
        modelInput
          .html('<option value=""></option>')
          .prop('disabled', Object.keys(data).length === 0);

        $.each(data, function (index, text) {
          modelInput.append($('<option></option>').val(index).html(text));
        });
      }
    });

    return false;
  });
});
