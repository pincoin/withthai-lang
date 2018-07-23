$(document).ready(function () {
    let content3 = $('#content1');

    content3.html(content3.html().replace(
        /([\u0E00-\u0E7F]+)/g,
        function (x) {
            return '<span class="thai-font">' + x + '</span>'
        }
    ));
});
