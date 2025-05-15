document.addEventListener('DOMContentLoaded', function() {
    const hallButtons = document.querySelectorAll('.hall-btn');
    const selectedHallDisplay = document.getElementById('selected-hall');
    const nextButton = document.getElementById('next-button');
    let currentlySelected = null;

    hallButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from previously selected button
            if (currentlySelected) {
                currentlySelected.classList.remove('active');
            }
            
            // Add active class to newly selected button
            this.classList.add('active');
            currentlySelected = this;
            
            // Update the display
            const selectedHall = this.dataset.hall;
            selectedHallDisplay.textContent = selectedHall;
            
            // Enable the Next button
            nextButton.disabled = false;
            
            // Store the selection in localStorage
            localStorage.setItem('selectedHall', selectedHall);
        });
    });

    nextButton.addEventListener('click', function() {
        if (currentlySelected) {
            // Here you would typically redirect to the next page
            // For now, we'll just show an alert
            alert(`Proceeding with ${currentlySelected.dataset.hall} selected`);
            // window.location.href = "next-page.html";
        }
    });
});