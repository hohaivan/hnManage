     // Get input field
    var input = document.getElementById("my-filter");

    // Add an event listener to the input field
    input.addEventListener("input", function() {
      // Get the input value
      var value = this.value.toLowerCase();

      // Loop through each table row
      var rows = document.getElementsByClassName("tr-filter");
      for (var i = 0; i < rows.length; i++) {
        var text = rows[i].textContent.toLowerCase();
        if (text.indexOf(value) !== -1) {
          rows[i].style.display = "table-row";
        } else {
          rows[i].style.display = "none";
        }
      }
    });



