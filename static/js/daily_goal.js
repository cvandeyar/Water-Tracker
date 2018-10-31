// 'use strict';

// function updateGoal(result){
//     // alert('entry successful');
//     // debugger;
//     console.log('hi stranger');
//     $('#daily_goal')[0].innerText = result
//     console.log('yay we made it');
// }

// function submitWater(evt){
//     evt.preventDefault();
//     console.log('hello');

//     let formInputs = {
//         'drink': $('#qty-field').val(),
//     };

//     console.log('created form inputs');

//     $.post('/add-water', 
//             formInputs, 
//             updateGoal);
// }

// $('#add-water').on('submit', submitWater);

/////////////////////////////////////////////

// 'use strict';

// // const getIPInfo = async () => {
// //     const response = await fetch("https://ipinfo.io/json?token=IP_token")
// //     const data = await response.json()
// //     return data;
// //     }

// function updateGoal(result){
//     // debugger;
//     console.log('hi stranger');
//     $('#daily_goal')[0].innerText = result
//     console.log('yay we made it');

// }
// async function submitWater(evt) {
//     evt.preventDefault();
//     console.log('entered submit water');
//     const data = await getIPInfo();
//     console.log('called getIPInfo');
//     let formInputs = {
//         "drink": $("#qty-field").val(),
//         "postal": data['postal'],
//     };

//     $.post("/add-water", 
//        formInputs,
//        updateGoal);
// };
// $("#add-water").on("submit", submitWater);
