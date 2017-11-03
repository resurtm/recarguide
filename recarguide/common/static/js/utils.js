jQuery(function ($) {
  // todo: remove this on release
  $('input, select, textarea').each(function () {
    $(this).removeAttr('required');
  });

  $('[data-toggle="popover"]').popover();
});
