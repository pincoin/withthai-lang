$(document).ready(function () {
    let content1 = $('#content1');

    content1.html(content1.html().replace(
        /([\u0E00-\u0E7F]+)/g,
        function (x) {
            return '<span class="thai-font">' + x + '</span>'
        }
    ));
});
