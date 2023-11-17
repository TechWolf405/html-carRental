document.getElementById('carForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Create a plain JavaScript object
    const carData = {
        make: document.getElementById('make').value,
        model: document.getElementById('model').value,
        year: parseInt(document.getElementById('year').value),
        rental_rate_per_day: parseFloat(document.getElementById('rental_rate_per_day').value),
        availability: parseInt(document.getElementById('availability').value),
    };

    // Send a POST request to the FastAPI endpoint
    fetch('/submit_car', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(carData)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data); // Display success message or handle response
        // You can add further logic here based on the server response
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
