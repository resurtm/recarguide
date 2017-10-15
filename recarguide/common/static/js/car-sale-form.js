jQuery(function ($) {
  var form = $('#package-plan-selector-form');
  if (form.length === 0) {
    return;
  }

  var idField = form.find('[name=package_plan_id]');

  form.on('click', 'button', function () {
    idField.val($(this).data('id'));
    form.submit();
  });

  form.on('submit', function (e) {
    return idField.val().length > 0;
  });
});
