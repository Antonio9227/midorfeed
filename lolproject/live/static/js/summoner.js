buttons = document.getElementsByClassName("navli");
frames = document.getElementsByTagName("iframe");

function select(n) {
    for (i = 0; i < buttons.length; i++) {
        if (i == n) {
            buttons[i].className = "navli navactive";
            frames[i].className = "activeFrame";
            if (!frames[i].getAttribute('src'))
                frames[i].setAttribute('src', frames[i].getAttribute('a-src'));
        } else {
            buttons[i].className = "navli";
            frames[i].className = "inactiveFrame";
        }
    }
}