$('#ai_form').submit(function (e) {
    e.preventDefault();
    var csrfToken = $('[name=csrfmiddlewaretoken]').val();
    $('#priority, #department').prop('disabled', true);
    $('button').prop('disabled', true);
    $('#loading').show();

    $.ajax({
        url: '/call_ai',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ description: $('#description').val() }),
        beforeSend: function (xhr) {
            // Set CSRF token in the request header
            xhr.setRequestHeader('X-CSRFToken', csrfToken);
        },
        success: function (data) {
            $('#priority').val(data.priority);
            $('#department').val(data.department);
        },
        error: function (err) {
            console.error('Error:', err);
        },
        complete: function () {
            // Re-enable selects after request finishes (success or error)
            $('#loading').hide();
            $('#priority, #department').prop('disabled', false);
            $('button').prop('disabled', false);

        }
    });
});