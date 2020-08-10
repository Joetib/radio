(() => {

    var sliders = document.getElementsByClassName("advert-slider");

    for (slider of sliders) {

        setInterval(() => {
            let first = slider.children[0];
            console.log(first)
            first.classList.add("fade")
            console.log("tried adding")
            setTimeout(() => {
                slider.removeChild(slider.children[0]);
                first.classList.remove("fade")
                slider.appendChild(first);
            }, 500);

        }, 5000);
    }
})();

(() => {
    let parents = document.getElementsByClassName('poca-music-content');
    for (let i = 0; i < parents.length; i++) {
        let p = parents[i]
        let a = p.querySelector(".audioplayer-time.audioplayer-time-duration");
        let b = p.querySelector(".music-meta-data .music-duration")
        b.innerHTML = a.innerHTML
        a.addEventListener('DOMSubtreeModified', function (e) {
            b.innerHTML = a.innerHTML;
        });

    }
})();
