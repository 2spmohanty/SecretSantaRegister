// register_family.js

document.addEventListener('DOMContentLoaded', function() {
    const registerFamilyForm = document.getElementById('registerFamilyForm');
    if (registerFamilyForm) {
        registerFamilyForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the default form submission
            document.getElementById('responseMessageFamily').innerText = ''; // Clear previous messages

            const familyName = document.getElementById('family_name').value;

            fetch('/register_family', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ family_name: familyName })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    document.getElementById('responseMessageFamily').innerText = data.error; // Display error message
                } else {
                    document.getElementById('responseMessageFamily').innerText = data.message; // Display success message
                    registerFamilyForm.reset(); // Reset form fields
                }
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('responseMessageFamily').innerText = 'Error registering family.';
            });
        });
    } else {
        console.error("The registerFamilyForm was not found in the DOM.");
    }
});
