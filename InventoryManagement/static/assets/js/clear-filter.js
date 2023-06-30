function clearFilters() {
  var inputs = document.getElementsByClassName('filter-input');
  for (var i = 0; i < inputs.length; i++) {
    inputs[i].value = '';
  }

  document.getElementById('filter-form').submit();
}