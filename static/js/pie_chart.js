"use strict";
    
function updateChart1(results){
    //rader chart of zipcodes
    let ctx = document.getElementById("pieChart").getContext('2d');
    let myChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: results['postal'], 
            datasets: [{
                label: "Zipcode",
                data: results['qty'], 
                backgroundColor: [
                        // 'rgba(255, 99, 132, 0.2)',
                        // 'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)',
                    ],
                borderColor: [
                        // 'rgba(255, 99, 132, 1)',
                        // 'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)',
                    ], 
        }],
    },
        options: {
            scale: {
                ticks: {
                    min: 0,
                    }
                } 
            }
    });
}

function updateChartInfo1(evt){
    evt.preventDefault();

    $.get('/pie-chart.json', updateChart1);
}

$('#pie-chart').on('submit', updateChartInfo1)

function firstLoad(evt){
    // evt.preventDefault();

    $.get('/pie-chart.json', updateChart1);
}

$(document).ready(function(){
    $.get('/pie-chart.json', firstLoad);
});