// Current displayed month and year
let currentMonth = new Date().getMonth();
let currentYear = new Date().getFullYear();
let selectedDate = null; // Stores Date object
let startTime = '';
let endTime = '';

// DOM Elements
const dateGrid = document.getElementById('date-grid');
const currentMonthDisplay = document.querySelector('.current-month');
const prevMonthBtn = document.getElementById('prev-month');
const nextMonthBtn = document.getElementById('next-month');
const clearSelectionBtn = document.getElementById('clear-selection');
const startTimeInput = document.getElementById('start-time');
const endTimeInput = document.getElementById('end-time');
const selectedDateDisplay = document.getElementById('selected-date-display');
const selectedTimeRangeDisplay = document.getElementById('selected-time-range');
const durationDisplay = document.getElementById('duration-display');
const nextButton = document.getElementById('next-button');

// Functions
function renderCalendar() {
    dateGrid.innerHTML = '';
    
    // Update month header
    const monthNames = ["January", "February", "March", "April", "May", "June",
                        "July", "August", "September", "October", "November", "December"];
    currentMonthDisplay.textContent = `${monthNames[currentMonth]} ${currentYear}`;
    
    // Get first day of month and total days
    const firstDay = new Date(currentYear, currentMonth, 1).getDay();
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
    
    // Add empty cells for days before first day of month
    for (let i = 0; i < firstDay; i++) {
        const emptyCell = document.createElement('div');
        emptyCell.className = 'date-cell empty';
        dateGrid.appendChild(emptyCell);
    }
    
    // Add date cells
    const today = new Date();
    // Normalize today to start of day for comparison
    const todayStart = new Date(today.getFullYear(), today.getMonth(), today.getDate());

    // Calculate the end of the 5-day selectable window (today + 4 days)
    const fiveDaysFromTodayEnd = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 4); 
    fiveDaysFromTodayEnd.setHours(23, 59, 59, 999); // Set to end of the 5th day

    for (let day = 1; day <= daysInMonth; day++) {
        const dateCell = document.createElement('div');
        dateCell.className = 'date-cell';
        dateCell.textContent = day;
        
        const cellDate = new Date(currentYear, currentMonth, day);
        // Normalize cellDate to start of day for comparison
        const cellDateStart = new Date(currentYear, currentMonth, day);

        // Highlight today
        if (cellDateStart.toDateString() === todayStart.toDateString()) {
            dateCell.classList.add('today');
        }
        
        // Check if this date is selected
        if (selectedDate && 
            cellDateStart.toDateString() === new Date(selectedDate.getFullYear(), selectedDate.getMonth(), selectedDate.getDate()).toDateString()) {
            dateCell.classList.add('selected');
        }
        
        // Check if date is in the past OR beyond the 5-day selectable window
        if (cellDateStart < todayStart || cellDateStart > fiveDaysFromTodayEnd) {
            dateCell.classList.add('past-date'); // Using past-date class for both disabled categories
        } else {
            // Add click event for future dates within the 5-day window
            dateCell.addEventListener('click', function() {
                selectedDate = new Date(currentYear, currentMonth, day);
                renderCalendar(); // Re-render to update selection highlight
                updateDisplay(); // Update display for selected date
            });
        }
        
        dateGrid.appendChild(dateCell);
    }
    updateDisplay(); // Update display after calendar renders (in case a date was pre-selected or cleared)
    checkFormValidity();
}

function calculateDuration(start, end) {
    if (!start || !end) return '0 minutes';

    const [startHour, startMinute] = start.split(':').map(Number);
    const [endHour, endMinute] = end.split(':').map(Number);

    const startDate = new Date();
    startDate.setHours(startHour, startMinute, 0, 0);

    const endDate = new Date();
    endDate.setHours(endHour, endMinute, 0, 0);

    if (endDate < startDate) {
        // If end time is before start time (e.g., 5 PM start, 2 PM end)
        return 'Invalid (End < Start)';
    }

    const durationMs = endDate - startDate;
    const durationMinutes = Math.floor(durationMs / (1000 * 60));

    const hours = Math.floor(durationMinutes / 60);
    const minutes = durationMinutes % 60;

    if (hours > 0 && minutes > 0) {
        return `${hours} hour${hours > 1 ? 's' : ''} ${minutes} minute${minutes > 1 ? 's' : ''}`;
    } else if (hours > 0) {
        return `${hours} hour${hours > 1 ? 's' : ''}`;
    } else {
        return `${minutes} minute${minutes > 1 ? 's' : ''}`;
    }
}

function updateDisplay() {
    if (selectedDate) {
        selectedDateDisplay.textContent = selectedDate.toDateString();
    } else {
        selectedDateDisplay.textContent = 'None';
    }

    const duration = calculateDuration(startTime, endTime);
    if (startTime && endTime) {
        selectedTimeRangeDisplay.textContent = `${formatTime(startTime)} - ${formatTime(endTime)}`;
        durationDisplay.textContent = duration;
    } else {
        selectedTimeRangeDisplay.textContent = 'Not selected';
        durationDisplay.textContent = '0 minutes';
    }
    checkFormValidity();
}

function formatTime(timeString) {
    const [hour, minute] = timeString.split(':');
    const h = parseInt(hour);
    const ampm = h >= 12 ? 'PM' : 'AM';
    const formattedHour = h % 12 || 12; // Convert 0 to 12 for 12-hour format
    return `${formattedHour}:${minute} ${ampm}`;
}

function checkFormValidity() {
    const isDateSelected = selectedDate !== null;
    const isTimeSelected = startTimeInput.value && endTimeInput.value;
    const isTimeValid = calculateDuration(startTimeInput.value, endTimeInput.value) !== 'Invalid (End < Start)' &&
                        calculateDuration(startTimeInput.value, endTimeInput.value) !== '0 minutes'; // Also check if duration is non-zero

    if (isDateSelected && isTimeSelected && isTimeValid) {
        nextButton.classList.remove('disabled');
        nextButton.classList.remove('cursor-not-allowed', 'opacity-50');
        nextButton.classList.add('cursor-pointer');
    } else {
        nextButton.classList.add('disabled');
        nextButton.classList.add('cursor-not-allowed', 'opacity-50');
        nextButton.classList.remove('cursor-pointer');
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Retrieve values from sessionStorage if they exist (for navigation)
    const storedDate = sessionStorage.getItem('selectedDate');
    if (storedDate) {
        const tempDate = new Date(storedDate);
        const today = new Date();
        const todayStart = new Date(today.getFullYear(), today.getMonth(), today.getDate());
        const fiveDaysFromTodayEnd = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 4);
        fiveDaysFromTodayEnd.setHours(23, 59, 59, 999);

        // Only restore selectedDate if it's within the valid 5-day window
        if (tempDate >= todayStart && tempDate <= fiveDaysFromTodayEnd) {
            selectedDate = tempDate;
            currentMonth = selectedDate.getMonth();
            currentYear = selectedDate.getFullYear();
        } else {
            sessionStorage.removeItem('selectedDate'); // Clear invalid stored date
        }
    }

    startTime = sessionStorage.getItem('startTime') || '';
    endTime = sessionStorage.getItem('endTime') || '';
    
    if(startTime) startTimeInput.value = startTime;
    if(endTime) endTimeInput.value = endTime;

    renderCalendar(); // Initial render

    prevMonthBtn.addEventListener('click', function() {
        currentMonth--;
        if (currentMonth < 0) {
            currentMonth = 11;
            currentYear--;
        }
        renderCalendar();
    });
    
    nextMonthBtn.addEventListener('click', function() {
        currentMonth++;
        if (currentMonth > 11) {
            currentMonth = 0;
            currentYear++;
        }
        renderCalendar();
    });
    
    startTimeInput.addEventListener('change', function() {
        startTime = this.value;
        updateDisplay();
    });
    
    endTimeInput.addEventListener('change', function() {
        endTime = this.value;
        updateDisplay();
    });

    clearSelectionBtn.addEventListener('click', function() {
        selectedDate = null;
        startTime = '';
        endTime = '';
        startTimeInput.value = '';
        endTimeInput.value = '';
        sessionStorage.removeItem('selectedDate');
        sessionStorage.removeItem('startTime');
        sessionStorage.removeItem('endTime');
        renderCalendar();
        updateDisplay();
    });

    // Store selections in sessionStorage before navigating to hall.html
    nextButton.addEventListener('click', function(event) {
        if (nextButton.classList.contains('disabled')) {
            event.preventDefault(); // Prevent navigation if button is disabled
            alert('Please select a valid date and time range.');
            return;
        }
        sessionStorage.setItem('selectedDate', selectedDate.toISOString());
        sessionStorage.setItem('startTime', startTime);
        sessionStorage.setItem('endTime', endTime);
        // The href will handle navigation to hall.html
    });
});
