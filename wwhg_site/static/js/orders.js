// orders.js
document.addEventListener('DOMContentLoaded', function () {
  const orderButtons = document.querySelectorAll('.order-details-button');
  const popup = document.getElementById('order-popup');
  const popupContent = popup.querySelector('.popup-content');
  const closePopup = popup.querySelector('.close-popup');

  orderButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const orderId = button.getAttribute('data-order-id');
      // Make an AJAX request to retrieve order details and populate popupContent.
      // Once you have the order details, populate popupContent.
      // Finally, show the popup.
      popup.style.display = 'block';
    });
  });

  closePopup.addEventListener('click', () => {
    popup.style.display = 'none';
  });
});


document.getElementById("confirmPaymentButton").addEventListener("click", function () {
    // Redirect to the 'create_order' URL when the button is clicked
    window.location.href = "{% url 'create_order' %}";
});
