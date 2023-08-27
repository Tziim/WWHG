$('#paymentModal').on('show.bs.modal', function () {
    // Show loading spinner
    $('.modal-body').html('<div class="text-center"><div class="spinner-border" role="status"></div> Processing...</div>');

    // Simulate payment processing for 2-3 seconds
    setTimeout(function () {
        // Replace the loading spinner with the payment complete message
        $('.modal-body').html('<h5>Order Confirmed</h5>');
    }, 2000); // 2 seconds
});