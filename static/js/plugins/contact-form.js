/**
 *
 * -----------------------------------------------------------------------------
 *
 * Template : Fluxi HTML TEMPLATE
 * Author : reacthemes
 * Author URI : https://reactheme.com/ 
 *
 * -----------------------------------------------------------------------------
 *
 **/

(function ($) {
    'use strict';
    // Get the form.
    var form = $('#contact-form');

    // Get the messages div.
    var formMessages = $('#form-messages');

    // Set up an event listener for the contact form.
    $(form).submit(function (e) {
        // Stop the browser from submitting the form.
        e.preventDefault();

        // Serialize the form data.
        var formData = $(form).serialize();

        // Submit the form using AJAX.
        $.ajax({
                type: 'POST',
                url: $(form).attr('action'),
                data: formData
            })
            .done(function (response) {
                // Clear the form.
                $('#name, #email, #message').val('');
                
                // Hide old form messages
                $(formMessages).hide();
                
                // Show success modal
                showSuccessModal();
            })
            .fail(function (data) {
                // Make sure that the formMessages div has the 'error' class.
                $(formMessages).removeClass('success');
                $(formMessages).addClass('error');

                // Set the message text.
                if (data.responseText !== '') {
                    $(formMessages).text(data.responseText);
                } else {
                    $(formMessages).text('Oops! An error occured and your message could not be sent.');
                }
            });
    });

    // Success Modal Functions
    function showSuccessModal() {
        // Try multiple approaches to show modal
        var modal = $('#success-modal');
        
        // Method 1: Add class (our original approach)
        modal.addClass('show');
        
        // Method 2: Direct CSS manipulation as fallback
        modal.css({
            'display': 'flex',
            'opacity': '1',
            'visibility': 'visible',
            'z-index': '999999'
        });
        
        // Method 3: Show with jQuery
        modal.show();
        
        // Auto close after 5 seconds
        setTimeout(function() {
            hideSuccessModal();
        }, 5000);
    }

    function hideSuccessModal() {
        var modal = $('#success-modal');
        modal.removeClass('show');
        modal.css({
            'display': 'none',
            'opacity': '0',
            'visibility': 'hidden'
        });
        modal.hide();
    }

    // Close modal when clicking the close button
    $(document).on('click', '#close-success-modal', function() {
        hideSuccessModal();
    });

    // Close modal when clicking outside of it
    $(document).on('click', '.success-modal-overlay', function(e) {
        if (e.target === this) {
            hideSuccessModal();
        }
    });

    // Close modal with Escape key
    $(document).on('keydown', function(e) {
        if (e.key === 'Escape' && $('#success-modal').hasClass('show')) {
            hideSuccessModal();
        }
    });



})(jQuery);
