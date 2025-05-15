document.addEventListener('DOMContentLoaded', function() {
    const startTimeInput = document.getElementById('start-time');
    const endTimeInput = document.getElementById('end-time');
    const selectedTimeRange = document.getElementById('selected-time-range');
    const durationDisplay = document.getElementById('duration-display');
    const nextButton = document.getElementById('next-button');

    // Set default times (8:00 AM and 6:00 PM)
    startTimeInput.value = '08:00';
    endTimeInput.value = '18:00';
    updateTimeDisplay();

    // Event listeners
    startTimeInput.addEventListener('change', function() {
        if (endTimeInput.value && this.value > endTimeInput.value) {
            endTimeInput.value = this.value;
        }
        updateTimeDisplay();
    });

    endTimeInput.addEventListener('change', function() {
        if (startTimeInput.value && this.value < startTimeInput.value) {
            this.value = startTimeInput.value;
        }
        updateTimeDisplay();
    });

    nextButton.addEventListener('click', function() {
        // Here you would typically proceed to the next step
        alert(`Proceeding with time range: ${selectedTimeRange.textContent}`);
        // window.location.href = "next-page.html";
    });

    function updateTimeDisplay() {
        const startTime = startTimeInput.value;
        const endTime = endTimeInput.value;
        
        if (startTime && endTime) {
            // Display the selected time range
            selectedTimeRange.textContent = `${formatTime(startTime)} to ${formatTime(endTime)}`;
            
            // Calculate and display duration
            const duration = calculateDuration(startTime, endTime);
            durationDisplay.textContent = duration;
            
            // Enable the Next button
            nextButton.disabled = false;
        } else {
            nextButton.disabled = true;
        }
    }

    function formatTime(timeString) {
        const [hours, minutes] = timeString.split(':');
        const hourNum = parseInt(hours, 10);
        const ampm = hourNum >= 12 ? 'PM' : 'AM';
        const hour12 = hourNum % 12 || 12;
        return `${hour12}:${minutes.padStart(2, '0')} ${ampm}`;
    }

    function calculateDuration(start, end) {
        const startDate = new Date(`2000-01-01T${start}`);
        const endDate = new Date(`2000-01-01T${end}`);
        
        // Handle case where end time is next day (though our max is 6PM)
        if (endDate < startDate) {
            endDate.setDate(endDate.getDate() + 1);
        }
        
        const diffMs = endDate - startDate;
        const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
        const diffMinutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
        
        // Format duration
        if (diffHours > 0) {
            return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ${diffMinutes} minute${diffMinutes !== 1 ? 's' : ''}`;
        } else {
            return `${diffMinutes} minute${diffMinutes !== 1 ? 's' : ''}`;
        }
    }
});