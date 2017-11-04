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

  filter.find('.ranged-slider').each(function () {
    var node = $(this);
    var parent = node.closest('.filter-group');
    var min = parseInt(node.attr('data-min'));
    var max = parseInt(node.attr('data-max'));
    if (min !== max) {
      node.slider({
        range: true,
        min: min,
        max: max,
        values: [min, max],
        slide: function (event, ui) {
          parent.find('.ranged-value').text(ui.values[0] + '—' + ui.values[1]);
        }
      });
    }
    parent.find('.ranged-value').text(min + '—' + max);
  });
});
