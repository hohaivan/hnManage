$(document).ready(function() {
function updateTime() {
  var now = new Date();
  var hours = now.getHours();
  var minutes = now.getMinutes();
  var seconds = now.getSeconds();
  
  hours = (hours < 10 ? "0" : "") + hours;
  minutes = (minutes < 10 ? "0" : "") + minutes;
  seconds = (seconds < 10 ? "0" : "") + seconds;
  
  var timeString = hours + ":" + minutes + ":" + seconds;
  
  var clock = document.getElementById("clock");
  clock.innerHTML = timeString;
}

setInterval(updateTime, 1000);

function updateDate() {
  var now = new Date();
  var days = now.getDate();
  var months = now.getMonth()+1;
  var years = now.getFullYear()
  
  days = (days < 10 ? "0" : "") + days;
  months = (months < 10 ? "0" : "") + months;
 
  var dayString = days + "-" + months + ", " + years; 
  var datestr = document.getElementById("clock-date");
  datestr.innerHTML = dayString;
}

setInterval(updateDate, 1000);


});
