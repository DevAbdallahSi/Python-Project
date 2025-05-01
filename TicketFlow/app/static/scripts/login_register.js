
$('#show-register').on('click', function () {
    $('#login-section').fadeOut(300, function () {
        $('#register-section').fadeIn(300);
    });
});

$('#show-login').on('click', function () {
    $('#register-section').fadeOut(300, function () {
        $('#login-section').fadeIn(300);
    });
});