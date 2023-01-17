var m = document.getElementsByClassName("alert");
Array.prototype.forEach.call(m, function(element, index) {
    setTimeout(function(){
        element.classList.add('hide');
    }, 2000 + 2000*index);
    setTimeout(function(){
        element.remove()
    }, 2500 + 2000*index);
});