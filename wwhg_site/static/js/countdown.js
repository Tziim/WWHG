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

function updateHolidayData() {
    $.ajax({
        type: "GET",
        url: "/api/next_holiday/",
        dataType: "json",
        success: function(data) {
            if (data.next_holiday) {
                $('.holiday-name').text(data.next_holiday.name);
                $('.holiday-date').text('Date: ' + data.next_holiday.date);
                targetDate = new Date(data.next_holiday.date).getTime();
            } else if (data.error_message) {
                console.error(data.error_message);  // handle the error in another way if needed
            }
        },
        error: function(error) {
            console.error("There was an error fetching the holiday data:", error);
        }
    });
}

// Fetch the data every hour
setInterval(updateHolidayData, 3600 * 1000);  // 3600 * 1000 milliseconds = 1 hour



