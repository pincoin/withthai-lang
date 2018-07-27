$(document).ready(function () {
    $('#id_part').on('change', function (e) {
        this.form.submit();
    });

    function toggle_text(item) {
        if (item.text() === '[펼치기]') {
            item.text('[접기]');
        } else {
            item.text('[펼치기]');
        }
    }

    $('#collapseLink1').on('click', "small", function (e) {
        toggle_text($(this));
    });

    $('#collapseLink2').on('click', "small", function (e) {
        toggle_text($(this));
    });

    $('#collapseLink3').on('click', "small", function (e) {
        toggle_text($(this));
    });
});