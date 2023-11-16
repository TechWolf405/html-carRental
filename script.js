document.getElementById('customerForm').addEventListener('submit', function(event) {
    event.preventDefault();
  
    const formData = new FormData(this);
    const customerData = {
      name: formData.get('name'),
      email: formData.get('email'),
      phone: formData.get('phone')
    };
  
    fetch('/addCustomer', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(customerData)
    })
    .then(response => response.text())
    .then(data => {
      console.log(data); // Display success message
      fetchCustomers(); // Fetch and display updated customer list
    })
    .catch(error => {
      console.error('Error:', error);
    });
  });
  
  function fetchCustomers() {
    fetch('/customers')
      .then(response => response.json())
      .then(data => {
        const customerListDiv = document.getElementById('customerList');
        customerListDiv.innerHTML = ''; // Clear previous data
        data.forEach(customer => {
          const customerInfo = document.createElement('div');
          customerInfo.innerHTML = `<strong>Name:</strong> ${customer.name}, <strong>Email:</strong> ${customer.email}, <strong>Phone:</strong> ${customer.phone}`;
          customerListDiv.appendChild(customerInfo);
        });
      })
      .catch(error => {
        console.error('Error fetching customers:', error);
      });
  }
  
  // Fetch and display customers when the page loads
  fetchCustomers();
   