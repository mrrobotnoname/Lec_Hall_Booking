        $(document).ready(function() {
            $('#deleteYearDepartment').change(function() {
                console.log("heo")
                var faculty = $(this).val();
                var $yearSelect = $('#deleteYear');
                
                $yearSelect.html('<option>Loading...</option>');
                
                $.ajax({
                    url: '/api?action=getYears&faculty=' + faculty,
                    method: 'GET',
                    success: function(years) {
                        $yearSelect.empty();
                        $yearSelect.append('<option value="" disabled selected>Select The Year</option>');
                        years.forEach(function(year) {
                            $yearSelect.append(new Option(year, year));
                        });
                    },
                    error: function() {
                        $yearSelect.html('<option value="" disabled selected>Error loading years</option>');
                    }
                });
            });

            $('form').on('submit', function() {
                var $btn = $(this).find('input[type="submit"]');
                var originalText = $btn.val();
                $btn.val('Processing...').prop('disabled', true);
                

                setTimeout(function() {
                    $btn.val(originalText).prop('disabled', false);
                }, 3000);
            });
            $('.form-card').hover(
                function() {
                    $(this).css('transform', 'translateY(-2px)');
                },
                function() {
                    $(this).css('transform', 'translateY(0)');
                }
            );
        });