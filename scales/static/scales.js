Handlebars.registerHelper('greaterThan', function (value1, value2) {
    return value1 > value2;
})

window.onload = () => {
    const scaleSubmit = document.getElementById('submit-scale');

    scaleSubmit.addEventListener('click', function (event) {
        scaleSubmit.children[0].innerHTML = 'Next Scale';
        event.preventDefault();
        updateScale();
    });

    scaleSubmit.addEventListener("keyup", function (event) {
        if (event.keyIdentifier === 13) {
            event.preventDefault();
            this.click();
        }
    });

    function save() {
        var result = fetch('/practice/save')
            .then(response => {
                return response.status == 200;
            })
            .catch((e) => { return false; });
        return result;
    }

    function updateScale() {
        let scale;
        if (scales.length <= 1) {
            document.getElementById('submit-scale').innerHTML =
                '<a href="/" id="finished" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">Finish and save</a>';
            document.getElementById('finished').onclick = () => {
                if (save()) {
                    window.location.href = "/";
                };
            }
        }
        if (scales.length < 1)
            return;
        scale = scales.pop();
        currentScale = JSON.parse(scale);

        var source = document.getElementById('scale-template').innerHTML;
        var template = Handlebars.compile(source);
        document.getElementById('scale').innerHTML = template({ scale: currentScale })
    }
}