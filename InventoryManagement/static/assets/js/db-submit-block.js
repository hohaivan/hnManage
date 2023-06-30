document.addEventListener('DOMContentLoaded', function() {
        var form = document.querySelector('form');
        var submitBtn = document.querySelector('input[type="submit"]');

        form.addEventListener('submit', function() {
            submitBtn.disabled = true;
            setTimeout(function() {
                submitBtn.disabled = false;
            }, 5000);
        });
    });