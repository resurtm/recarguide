jQuery(function ($) {
  var filter = $('#search-filter');
  if (filter.length === 0) {
    return;
  }

  filter.on('click', '.facet-group .show-more', function (e) {
    e.preventDefault();
    var link = $(this);
    var group = link.closest('.facet-group');
    group.find("[hidden]").removeAttr('hidden');
    link.remove();
    return false;
  });
});
