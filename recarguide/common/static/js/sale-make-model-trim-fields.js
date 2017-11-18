jQuery(function ($) {
  var form = $('#listing-form');
  if (form.length === 0) {
    return;
  }

  var makeInput = form.find('#id_make');
  var modelInput = form.find('#id_model');

  var trimNameInput = form.find('#id_trim_name');
  var trimIdInput = form.find('#id_trim_id');

  if (makeInput.val().length > 0 && modelInput.find('option[value!=""]').length > 0) {
    modelInput.prop('disabled', false);
    if (modelInput.val().length > 0) {
      trimNameInput.prop('disabled', false);
    }
  }

  makeInput.on('change', function () {
    trimNameInput
      .val('')
      .prop('disabled', true);
    trimIdInput.val('');

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

  modelInput.on('change', function () {
    trimNameInput
      .val('')
      .prop('disabled', modelInput.val().length === 0 || modelInput.find('option[value!=""]').length === 0);
    trimIdInput.val('');
  });

  trimNameInput.autocomplete({
    source: function (request, response) {
      $.ajax({
        url: '/sale/fetch-trims/' + modelInput.val() + '/' + request.term + '/',
        success: function (data) {
          response(data);
        }
      });
    },
    select: function (event, ui) {
      trimIdInput.val(ui.item.id);
    }
  });

  trimNameInput.on('keydown', function () {
    trimIdInput.val('');
  });
});
