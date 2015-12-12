// f = function() {
//     if (typeof flask_pagedown_converter === "undefined")
//         flask_pagedown_converter = Markdown.getSanitizingConverter().makeHtml;
    
//     var textarea = document.getElementById("flask-pagedown-%(field)s");
//     var preview = document.getElementById("flask-pagedown-%(field)s-preview");
    
//     textarea.onkeyup = function() { 
//         preview.innerHTML = flask_pagedown_converter(textarea.value); 
//         updateMath();
//     }

//     var updateMath = _.debounce(function() {
//         MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
//     }, 300);
    
//     textarea.onkeyup.call(textarea);
// }
// if (document.readyState === 'complete')
//     f();
// else if (window.addEventListener)
//     window.addEventListener("load", f, false);
// else if (window.attachEvent)
//     window.attachEvent("onload", f);
// else
//     f();