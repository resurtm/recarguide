jQuery(function ($) {
  var form = $('#listing-form');
  if (form.length === 0) {
    return;
  }

  var makeInput = form.find('#id_make');
  var modelInput = form.find('#id_model');

  if (makeInput.val().length > 0 && modelInput.find('option[value!=""]').length > 0) {
    modelInput.prop('disabled', false);
  }

  makeInput.on('change', function () {
    if (makeInput.val().length === 0) {
      modelInput
        .html('<option value=""></option>')
        .prop('disabled', true);
      return;
    }

    $.ajax({
      url: '/sale/fetch-models/' + makeInput.val() + '/',
      success: function (data) {
        modelInput
          .html('<option value=""></option>')
          .prop('disabled', Object.keys(data).length === 0);

        $.each(data, function (index, name) {
          modelInput.append($('<option></option>').val(index).html(name));
        });
      }
    });
  });
});
