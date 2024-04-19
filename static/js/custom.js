// custom.js
document.addEventListener('DOMContentLoaded', function () {
    // Handle click event on offer details button
    const offerDetailsButtons = document.querySelectorAll('.offer-details-btn');
    offerDetailsButtons.forEach(function (btn) {
        btn.addEventListener('click', function (event) {
            event.preventDefault();
            const offerId = this.getAttribute('data-offer-id');
            fetch(`/offer/details/${offerId}`)
                .then(response => response.json())
                .then(data => {
                    const modalBody = document.getElementById('offerDetailsBody');
                    modalBody.innerHTML = `
                        <p><strong>Title:</strong> ${data.title}</p>
                        <p><strong>Description:</strong> ${data.description}</p>
                        <p><strong>Start Date:</strong> ${data.start_date}</p>
                        <p><strong>End Date:</strong> ${data.end_date}</p>
                    `;
                    $('#offerModal').modal('show'); // Show modal
                })
                .catch(error => console.error('Error fetching offer details:', error));
        });
    });
});
