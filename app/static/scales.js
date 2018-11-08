const currentScale = document.querySelector('.js-current-scale');
currentScale.innerHTML = ' ';

const scaleSubmit = document.querySelector('.js-scale-submit');

scaleSubmit.innerHTML = 'Start';

scaleSubmit.addEventListener('click', function (event) {
    scaleSubmit.innerHTML = 'Next Scale';
    event.preventDefault();
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

    // show scale
    currentScale.innerHTML = scale
}
