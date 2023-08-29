// Calculate the target date and time for the countdown
var targetDate = new Date(document.getElementById('targetDate').dataset.date).getTime();

// Update the countdown every second
var countdown = setInterval(function() {
    var now = new Date().getTime();
    var timeRemaining = targetDate - now;

    // Calculate remaining days, hours, minutes, and seconds
    var days = Math.floor(timeRemaining / (1000 * 60 * 60 * 24));
    var hours = Math.floor((timeRemaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((timeRemaining % (1000 * 60)) / 1000);

    // Update the HTML with the remaining time
    document.getElementById("days").innerText = days;
    document.getElementById("hours").innerText = hours;
    document.getElementById("minutes").innerText = minutes;
    document.getElementById("seconds").innerText = seconds;

    // If the countdown ends, clear the interval
    if (timeRemaining <= 0) {
        clearInterval(countdown);
    }
}, 1000); // Update every second
