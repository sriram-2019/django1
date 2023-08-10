<form method="POST" name="register">
    {% csrf_token %}
    <input type="text" name="user">
    <input type="submit" name="mysub" id="mysub">
</form>
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script>
    $(document).ready(function() {
    $('#mysub').click(function(event) {
        event.preventDefault();
        var username = $('input[name="user"]').val();
        if (username == '') {
            alert('Please enter a username');
        } else {
            $.ajax({
                type: 'POST',
                url: '/sucess/',
                data: $('form').serialize(),
                success: function(response) {
                    // Handle the response from the server
                },
                error: function() {
                    alert('There was an error submitting the form');
                }
            });
        }
    });
});
</script>