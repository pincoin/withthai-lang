$(document).ready(function () {
    // beautify thai
    document.body.innerHTML = document.body.innerHTML.replace(
        /([\u0E00-\u0E7F]+)/g,
        function (x) {
            return '<span class="thai-font">' + x + '</span>'
        }
    );
});
