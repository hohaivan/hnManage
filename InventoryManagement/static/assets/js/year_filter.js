function filterTable() {
  // Get the year value from the input field
  var year = document.getElementById("year").value;

  // Send an AJAX request to the server to get the filtered table data
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "/filter_table/?year=" + year);
  xhr.onload = function() {
    if (xhr.status === 200) {
      // Parse the JSON response and update the table rows
      var filteredData = JSON.parse(xhr.responseText);
      var tableRows = document.getElementById("table-body").rows;
      for (var i = 0; i < tableRows.length; i++) {
        var rowData = filteredData[i];
        for (var j = 0; j < tableRows[i].cells.length; j++) {
          tableRows[i].cells[j].innerHTML = rowData[j];
        }
      }
    }
  };
  xhr.send();
}

// Add an event listener to the input field to call the filterTable function
document.getElementById("year-input").addEventListener("keyup", filterTable);