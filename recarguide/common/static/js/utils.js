jQuery(function ($) {
  $('input, select, textarea').each(function () {
    $(this).removeAttr('required');
  });

  $('[data-toggle="popover"]').popover();
});
