
function showOrderResults(chart) {
    // myChart.data.labels.pop()
    myChart.update()
}

function submitWater(evt) {
    evt.preventDefault();

    var formInputs = {
        'drink': $('#qty-field').val(),
    };

    $.post("/add-water", 
           formInputs,
           showOrderResults);
}

$("#add-water").on("submit", submitWater);