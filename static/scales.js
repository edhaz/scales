console.log(scales);

const currentScale = document.querySelector('.js-current-scale');
console.dir(currentScale);

const scaleSubmit = document.querySelector('.js-scale-submit');
console.dir(scaleSubmit);

scaleSubmit.addEventListener('click', function (event) {
    event.preventDefault();
    console.log("clicked button");
    updateScale();
});

function updateScale() {
    if (scales.length < 1) {
        // TODO show finished correctly
        currentScale.innerHTML = "That's all the scales for today, well done! Come back tomorrow!";
        return;
    }
    // get (random) scale
    const scale = scales.pop();
    console.log(scale);
    console.log(scales);

    // show scale
    currentScale.innerHTML = scale
}
