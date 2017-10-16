jQuery(function ($) {
  var form = $('#listing-form');
  if (form.length === 0) {
    return;
  }

  var catInput = form.find('#id_category');
  var subInput = form.find('#id_subcategory');
  var subWrap = subInput.closest('.form-group');

  if (catInput.val().length > 0 && subInput.find('option[value!=""]').length > 0) {
    subInput.prop('disabled', false);
    subWrap.removeClass('d-none');
  }

  catInput.on('change', function () {
    if (catInput.val().length === 0) {
      subInput
        .html('<option value=""></option>')
        .prop('disabled', true);
      subWrap.addClass('d-none');
      return;
    }

    $.ajax({
      url: '/sale/fetch-categories/' + catInput.val() + '/',
      success: function (data) {
        var disabled = Object.keys(data).length === 0;

        subInput
          .html('<option value=""></option>')
          .prop('disabled', disabled);
        subWrap.toggleClass('d-none', disabled);

        $.each(data, function (index, name) {
          subInput.append($('<option></option>').val(index).html(name));
        });
      }
    });
  });
});
