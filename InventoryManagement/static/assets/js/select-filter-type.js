  window.addEventListener('load', adjustInputWidth);

  function adjustInputWidth() {
    var headerCells = document.querySelectorAll('.header-cell');
    var filterInputs = document.querySelectorAll('.filter-input');

    for (var i = 0; i < headerCells.length; i++) {
      filterInputs[i].style.width = headerCells[i].offsetWidth + 'px';
    }
  }
  
  // Check if a value is stored in localStorage and set the selected options accordingly
window.onload = function() {
  var selectedOptions = localStorage.getItem("selectedOptions");
  if (selectedOptions) {
    var selectElements = document.getElementsByClassName("select-filter-type");
    var optionsArray = selectedOptions.split(",");
    for (var i = 0; i < selectElements.length; i++) {
      selectElements[i].value = optionsArray[i];
    }
  }
};

// Store the selected options in localStorage on form submission
document.getElementById("filter-form").addEventListener("submit", function(event) {

  var selectElements = document.getElementsByClassName("select-filter-type");
  var selectedOptions = [];
  for (var i = 0; i < selectElements.length; i++) {
    selectedOptions.push(selectElements[i].value);
  }
  localStorage.setItem("selectedOptions", selectedOptions.join(","));
});