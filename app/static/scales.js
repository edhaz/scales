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
    if (scales.length < 2) {
        document.querySelector('.js-submit-button').innerHTML =
            '<p><a href="/" id="finished" class="btn btn-primary">Finish</a></p>';
        eval(document.querySelector('.js-test').innerHTML);
        const scale = scales.pop();
        currentScale.innerHTML = scale;
    } else if (scales.length < 1) {
        currentScale.innerHTML = "Well done!";
        document.querySelector('.js-info').innerHTML = "<h4>That's all the scales for today, come back tomorrow.</h4>";
        return;
    } else {
        // get (random) scale
        const scale = scales.pop();

        // show scale
        currentScale.innerHTML = scale;
    }
}
