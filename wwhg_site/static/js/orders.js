// orders.js

// Function to open the popup window
function openPopup(orderId) {
    // You can customize the popup appearance and content here
    const popupContent = `
        <div class="popup-content">
            <h2>Order Details</h2>
            <p>Order ID: ${orderId}</p>
            <!-- Add more order details here -->
        </div>
    `;

    // Create a new window with the popup content
    const popupWindow = window.open('', 'OrderPopup', 'width=400,height=300');
    popupWindow.document.write(popupContent);
}

// Add click event listeners to each order row
const orderRows = document.querySelectorAll('.order-row');
orderRows.forEach(row => {
    const orderId = row.getAttribute('data-order-id');
    row.addEventListener('click', () => openPopup(orderId));
});
