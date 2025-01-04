document.addEventListener('DOMContentLoaded', function() {
    // Family Registration
    document.getElementById('registerFamilyForm').addEventListener('submit', function(event) {
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
                document.getElementById('registerFamilyForm').reset(); // Reset form fields
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('responseMessageFamily').innerText = 'Error registering family.';
        });
    });

    // Person Registration
    const registerPersonForm = document.getElementById('registerPersonForm');
    if (registerPersonForm) {
        registerPersonForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the default form submission

            // Clear previous response message
            document.getElementById('responseMessagePerson').innerText = '';

            // Gather form data
            const familyId = document.getElementById('family_id').value;
            const name = document.getElementById('name').value;
            const stickerName = document.getElementById('sticker_name').value;
            const isAdult = document.getElementById('is_adult').value;

            // Fetch API call to register person
            fetch('/register_person', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    family_id: familyId,
                    name: name,
                    sticker_name: stickerName,
                    is_adult: isAdult
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    document.getElementById('responseMessagePerson').innerText = data.error; // Display error message
                } else {
                    document.getElementById('responseMessagePerson').innerText = data.message; // Display success message
                    registerPersonForm.reset(); // Reset form fields
                }
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('responseMessagePerson').innerText = 'Error registering person.';
            });
        });
    } else {
        console.error("The registerPersonForm was not found in the DOM.");
    }
});
