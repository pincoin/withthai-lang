$(document).ready(function () {
    $('#id_part').on('change', function (e) {
        this.form.submit();
    });

    $('#collapse1').on('hidden.bs.collapse', function () {
        $('#collapseLink1').text('[펼치기]');
    }).on('show.bs.collapse', function () {
        $('#collapseLink1').text('[접기]');
    });

    $('#collapse2').on('hidden.bs.collapse', function () {
        $('#collapseLink2').text('[펼치기]');
    }).on('show.bs.collapse', function () {
        $('#collapseLink2').text('[접기]');
    });

    $('#collapse3').on('hidden.bs.collapse', function () {
        $('#collapseLink3').text('[펼치기]');
    }).on('show.bs.collapse', function () {
        $('#collapseLink3').text('[접기]');
    });
});