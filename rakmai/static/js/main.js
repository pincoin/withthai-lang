$(document).ready(function () {
    $('#id_part').on('change', function (e) {
        this.form.submit();
    });

    $('#collapse0').on('hidden.bs.collapse', function () {
        $('#collapseLink0').html('<i class="fa fa-plus fa-fw"></i>');
    }).on('show.bs.collapse', function () {
        $('#collapseLink0').html('<i class="fa fa-minus fa-fw"></i>');
    });

    $('#collapse1').on('hidden.bs.collapse', function () {
        $('#collapseLink1').html('<i class="fa fa-plus fa-fw"></i>');
    }).on('show.bs.collapse', function () {
        $('#collapseLink1').html('<i class="fa fa-minus fa-fw"></i>');
    });

    $('#collapse2').on('hidden.bs.collapse', function () {
        $('#collapseLink2').html('<i class="fa fa-plus fa-fw"></i>');
    }).on('show.bs.collapse', function () {
        $('#collapseLink2').html('<i class="fa fa-minus fa-fw"></i>');
    });

    $('#collapse3').on('hidden.bs.collapse', function () {
        $('#collapseLink3').html('<i class="fa fa-plus fa-fw"></i>');
    }).on('show.bs.collapse', function () {
        $('#collapseLink3').html('<i class="fa fa-minus fa-fw"></i>');
    });

    if ($(window).width() < 767) {
        $('#collapse0').each(function () {
            $(this).addClass('collapse');
        })
    }
});