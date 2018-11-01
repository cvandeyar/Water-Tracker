"use strict";
    
function updateChart1(results){
    console.log(results);
    console.dir(results);   
    let ctx = document.getElementById("pieChart").getContext('2d');
    let myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: results['postal'], 
            datasets: [{
            label: "Zipcode",
            backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                ],
            borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                ],
            data: results['qty'],  
        }],
    },
        options: {
            scales: {
                xAxes: [{
                    stacked: true
                }],
                yAxes: [{
                    stacked: true
                }]
            }
            ,
            animation: {
            duration: 0, // general animation time
        },
        hover: {
            animationDuration: 0, // duration of animations when hovering an item
        },
        responsiveAnimationDuration: 0, // animation duration after a resize
    }
    });
}

function updateChartInfo1(evt){
    evt.preventDefault();
    console.log("hello");

    $.get('/pie-chart.json', updateChart1);

    console.log("hey hey hey");
}

$('#pie-chart').on('submit', updateChartInfo1)

// $(document).ready(function(){
//     $.get('/pie_chart.json', updateChartInfo1);
// });