window.addEventListener( 'beforeunload', function(ev) {
    document.body.style.display = "none";
})

window.onpageshow = function (event) {
    if (event.persisted) {
        window.location.reload();
    }
};
