$(document).ready(function () {
    $('#id_part').on('change', function (e) {
        this.form.submit();
    });
});