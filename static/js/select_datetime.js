const dateGrid = document.getElementById('date-grid');
        const currentMonthDisplay = document.querySelector('.current-month');
        const prevMonthBtn = document.getElementById('prev-month');
        const nextMonthBtn = document.getElementById('next-month');
        const startTimeInput = document.getElementById('start-time');
        const endTimeInput = document.getElementById('end-time');
        const selectedDateDisplay = document.getElementById('selected-date-display');
        const selectedTimeRangeDisplay = document.getElementById('selected-time-range');
        const durationDisplay = document.getElementById('duration-display');
        const clearSelectionBtn = document.getElementById('clear-selection');
        const nextButton = document.getElementById('next-button');
        const selectedDateInput = document.getElementById('selected-date-input');

        // Variables to manage calendar state
        let currentMonth = new Date().getMonth();
        let currentYear = new Date().getFullYear();
        let selectedDate = null;

        /**
         * Renders the calendar grid for the current month and year.
         */
        function renderCalendar() {
            dateGrid.innerHTML = '';
            
            const monthNames = [
                'January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'
            ];
            
            currentMonthDisplay.textContent = `${monthNames[currentMonth]} ${currentYear}`;

            const firstDayOfMonth = new Date(currentYear, currentMonth, 1).getDay();
            const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

            const today = new Date();
            today.setHours(0, 0, 0, 0);

            // Calculate the maximum selectable date (today + 4 days)
            const maxSelectableDate = new Date(today);
            maxSelectableDate.setDate(today.getDate() + 4);
            maxSelectableDate.setHours(0, 0, 0, 0);

            // Add empty cells for days before the first day of the month
            for (let i = 0; i < firstDayOfMonth; i++) {
                const emptyCell = document.createElement('div');
                emptyCell.classList.add('date-cell', 'empty');
                dateGrid.appendChild(emptyCell);
            }

            // Add date cells for each day of the month
            for (let day = 1; day <= daysInMonth; day++) {
                const dateCell = document.createElement('div');
                dateCell.classList.add('date-cell');
                dateCell.textContent = day;

                // Create a proper date object for this specific day
                const cellDate = new Date(currentYear, currentMonth, day);
                cellDate.setHours(0, 0, 0, 0);

                // Store the date data on the cell element for accurate retrieval
                dateCell.dataset.year = currentYear;
                dateCell.dataset.month = currentMonth;
                dateCell.dataset.day = day;

                // Add classes based on date status
                if (cellDate < today || cellDate > maxSelectableDate) {
                    dateCell.classList.add('past-date');
                } else if (cellDate.getTime() === today.getTime()) {
                    dateCell.classList.add('today');
                }

                // Check if this date is currently selected
                if (selectedDate && 
                    selectedDate.getFullYear() === currentYear && 
                    selectedDate.getMonth() === currentMonth && 
                    selectedDate.getDate() === day) {
                    dateCell.classList.add('selected');
                }

                // Attach click listener
                dateCell.addEventListener('click', function() {
                    if (!this.classList.contains('empty') && !this.classList.contains('past-date')) {
                        // Remove previous selection
                        const previouslySelected = dateGrid.querySelector('.date-cell.selected');
                        if (previouslySelected) {
                            previouslySelected.classList.remove('selected');
                        }

                        // Add selection to current cell
                        this.classList.add('selected');
                        
                        // Create the selected date using the data attributes
                        selectedDate = new Date(
                            parseInt(this.dataset.year),
                            parseInt(this.dataset.month),
                            parseInt(this.dataset.day)
                        );

                        // Update displays
                        updateDateDisplay();
                        updateNextButtonState();
                    }
                });

                dateGrid.appendChild(dateCell);
            }
        }

        /**
         * Updates the selected date display and hidden input
         */
        function updateDateDisplay() {
            if (selectedDate) {
                const options = { 
                    weekday: 'short', 
                    year: 'numeric', 
                    month: 'short', 
                    day: 'numeric' 
                };
                selectedDateDisplay.textContent = selectedDate.toLocaleDateString('en-US', options);
                
                // Format date as YYYY-MM-DD for form submission
                const year = selectedDate.getFullYear();
                const month = String(selectedDate.getMonth() + 1).padStart(2, '0');
                const day = String(selectedDate.getDate()).padStart(2, '0');
                selectedDateInput.value = `${year}-${month}-${day}`;
                
                console.log('Selected date:', selectedDate);
                console.log('Form value:', selectedDateInput.value);
            }
        }

        /**
         * Updates the displayed selected time range and duration.
         */
        function updateTimeDisplay() {
            const startTime = startTimeInput.value;
            const endTime = endTimeInput.value;

            if (startTime && endTime) {
                selectedTimeRangeDisplay.textContent = `${formatTime(startTime)} - ${formatTime(endTime)}`;

                // Calculate duration
                const [startHour, startMinute] = startTime.split(':').map(Number);
                const [endHour, endMinute] = endTime.split(':').map(Number);

                const startTotalMinutes = startHour * 60 + startMinute;
                const endTotalMinutes = endHour * 60 + endMinute;

                if (endTotalMinutes <= startTotalMinutes) {
                    durationDisplay.textContent = 'Invalid (End time must be after start time)';
                    return;
                }

                const durationMinutes = endTotalMinutes - startTotalMinutes;
                const hours = Math.floor(durationMinutes / 60);
                const minutes = durationMinutes % 60;
                
                if (hours > 0) {
                    durationDisplay.textContent = `${hours}h ${minutes}m`;
                } else {
                    durationDisplay.textContent = `${minutes} minutes`;
                }
            } else {
                selectedTimeRangeDisplay.textContent = 'Not selected';
                durationDisplay.textContent = '0 minutes';
            }
            updateNextButtonState();
        }

        /**
         * Formats a 24-hour time string to 12-hour format
         */
        function formatTime(timeString) {
            const [hour, minute] = timeString.split(':').map(Number);
            const period = hour >= 12 ? 'PM' : 'AM';
            const displayHour = hour === 0 ? 12 : hour > 12 ? hour - 12 : hour;
            return `${displayHour}:${minute.toString().padStart(2, '0')} ${period}`;
        }

        /**
         * Updates the next button state based on selections
         */
        function updateNextButtonState() {
            const isDateSelected = selectedDate !== null;
            const isStartTimeSelected = startTimeInput.value !== '';
            const isEndTimeSelected = endTimeInput.value !== '';

            let isTimeRangeValid = false;
            if (isStartTimeSelected && isEndTimeSelected) {
                const [startHour, startMinute] = startTimeInput.value.split(':').map(Number);
                const [endHour, endMinute] = endTimeInput.value.split(':').map(Number);
                
                const startTotalMinutes = startHour * 60 + startMinute;
                const endTotalMinutes = endHour * 60 + endMinute;

                isTimeRangeValid = endTotalMinutes > startTotalMinutes;
            }

            if (isDateSelected && isTimeRangeValid) {
                nextButton.classList.remove('disabled');
                nextButton.disabled = false;
            } else {
                nextButton.classList.add('disabled');
                nextButton.disabled = true;
            }
        }

        /**
         * Clears all selections
         */
        function clearSelection() {
            // Clear date selection
            const previouslySelected = dateGrid.querySelector('.date-cell.selected');
            if (previouslySelected) {
                previouslySelected.classList.remove('selected');
            }
            selectedDate = null;
            selectedDateDisplay.textContent = 'None';
            selectedDateInput.value = '';

            // Clear time selection
            startTimeInput.value = '';
            endTimeInput.value = '';
            selectedTimeRangeDisplay.textContent = 'Not selected';
            durationDisplay.textContent = '0 minutes';

            updateNextButtonState();
        }

        // Event Listeners
        document.addEventListener('DOMContentLoaded', function() {
            renderCalendar();
            updateTimeDisplay();
            updateNextButtonState();
        });

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

        startTimeInput.addEventListener('change', updateTimeDisplay);
        endTimeInput.addEventListener('change', updateTimeDisplay);
        startTimeInput.addEventListener('input', updateTimeDisplay);
        endTimeInput.addEventListener('input', updateTimeDisplay);

        clearSelectionBtn.addEventListener('click', clearSelection);

        document.getElementById('booking-form').addEventListener('submit', function(e) {
            e.preventDefault();
             this.submit()
            
        });