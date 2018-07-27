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

    $('#collapseLink1').on('touchstart click', "small", function (e) {
        if (e.type === 'touchstart') {
            $(this).off('click');
        }
        toggle_text($(this));
    });

    $('#collapseLink2').on('touchstart click', "small", function (e) {
        if (e.type === 'touchstart') {
            $(this).off('click');
        }
        toggle_text($(this));
    });

    $('#collapseLink3').on('touchstart click', "small", function (e) {
        if (e.type === 'touchstart') {
            $(this).off('click');
        }
        toggle_text($(this));
    });
});