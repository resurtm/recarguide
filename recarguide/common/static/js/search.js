jQuery(function ($) {
  var filter = $('#search-filter');
  if (filter.length === 0) {
    return;
  }

  filter.on('click', '.facet-group .show-more', function (e) {
    e.preventDefault();
    var link = $(this);
    var group = link.closest('.facet-group');
    group.find('[hidden]').removeAttr('hidden');
    link.remove();
    return false;
  });

  filter.find('.ranged-slider').each(function () {
    var node = $(this);
    var form = node.closest('form');
    var parent = node.closest('.filter-group');

    var min = parseInt(node.attr('data-min'), 10);
    var max = parseInt(node.attr('data-max'), 10);
    var key = node.attr('data-key');

    if (min !== -1 && max !== -1) {
      var currentValue = form.find('[name=' + key + ']').val();
      if (currentValue.length > 0) {
        currentValue = currentValue.split('-');
        currentValue[0] = parseInt(currentValue[0], 10);
        currentValue[1] = parseInt(currentValue[1], 10);
        if (currentValue[0] === min && currentValue[1] === max) {
          currentValue = [min, max];
        }
      } else {
        currentValue = [min, max];
      }
      setValues(currentValue[0], currentValue[1]);
    } else {
      parent.find('small').removeAttr('hidden');
    }

    if (min !== max && min !== -1 && max !== -1) {
      node.slider({
        range: true,
        min: min,
        max: max,
        values: [currentValue[0], currentValue[1]],
        slide: function (event, ui) {
          setValues(ui.values[0], ui.values[1]);
        }
      });
    }

    function setValues(min, max) {
      parent.find('.ranged-value').text(min + '—' + max);
      form.find('[name=' + key + ']').val(min + '-' + max);
    }
  });
});
