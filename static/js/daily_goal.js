'use strict';

function updateGoal(result){
    // alert('entry successful');
    // debugger;
    console.log('hi stranger');
    console.log('result: ', result)
    $('#daily_goal')[0].innerText = result
    console.log('yay we made it');
}

function submitWater(evt){
    evt.preventDefault();
    console.log('hello');

    let formInputs = {
        'drink': $('#qty-field').val(),
    };

    console.log('created form inputs');

    $.post('/add-water', 
            formInputs, 
            updateGoal);
}

$('#add-water').on('submit', submitWater);