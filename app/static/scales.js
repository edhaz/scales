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
        currentScale.innerHTML = "Well done!";
        document.getElementById('test').innerHTML =
            '<p><a href="#" id="finished">SAVE</a></p>';
        document.querySelector('.js-info').innerHTML = "<h4>That's all the scales for today, come back tomorrow.</h4>";
        return;
    }
    // get (random) scale
    const scale = scales.pop();

    // show scale
    currentScale.innerHTML = scale
}
