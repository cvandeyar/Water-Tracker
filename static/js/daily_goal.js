'use strict';

function updateGoal(result){
    // alert('entry successful');
    $('#daily_goal')[0].outerText = result
}

function submitWater(evt){
    evt.preventDefault();
    console.log('hello');

    let formInputs = {
        'drink': $('#qty-field').val()
    };

    $.post('/add-water', 
            formInputs, 
            updateGoal);
}

$('#add-water').on('submit', submitWater);