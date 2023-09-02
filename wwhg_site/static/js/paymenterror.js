$('#errorModal').on('show.bs.modal', function () {
    // Show loading spinner
    $('.s-modal-body').html('<div class="text-center"><div class="spinner-border" role="status"></div> Processing...</div>');


    // Close the error modal after 2 seconds
    setTimeout(function () {
        $('.s-modal-body').html('<h4 class="text-center">Sorry!</h4><h5 class="text-center">Please fill in all required fields.</h5>');
    }, 2000); // 2 seconds
});