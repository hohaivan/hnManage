document.addEventListener("DOMContentLoaded", function() {
       var closeButtons = document.getElementsByClassName("close");
	   var closeAuto = document.getElementsByClassName("close-auto");
       for (var i = 0; i < closeButtons.length; i++) {
           closeButtons[i].onclick = function() {
               this.parentElement.style.display = 'none';
           };

           // Add automatic close behavior using closure
           (function(index) {
               setTimeout(function() {
                   closeAuto[index].parentElement.style.display = 'none';
               }, 15000);
           })(i);
       }
   });