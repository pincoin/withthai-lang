$(document).ready(function () {
    let content2 = $('#content2');

    content2.html(content2.html().replace(
        /([\u0E00-\u0E7F]+)/g,
        function (x) {
            return '<span class="thai-font">' + x + '</span>'
        }
    ));
});
