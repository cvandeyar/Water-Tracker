
"use strict";

function updateChart(results){
    // console.dir(results);
    let ctx = document.getElementById("lineChart").getContext('2d');
    let myChart = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [{
                    label: 'qty',
                    data: results['qty'],
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                },
                {
                    label: 'goal',
                    data: Array.apply(null, new Array(1000)).map(Number.prototype.valueOf, results['user_goal_oz']),
                    fill: false,
                    radius: 0,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255,99,132,1)',
                }],
            labels: results['time_parameter']
        },

        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    },
                    scaleLabel: {
                         display: true,
                         labelString: 'Qty',
                         fontSize: 20 
                  }
            }]            
        }  
    }
    });
}

function updateChartInfo(evt){
    evt.preventDefault();

    let formInputs = {
        filter_name: $('#stats').val()
    };

    $.get('/line_chart.json', formInputs, updateChart);
}

$('#stat-submit').on('submit', updateChartInfo)


$(document).one('ready', function(){
    let formInputs = {
        filter_name: 'months',
    };
    $.get('/line_chart.json', formInputs, updateChart);
});
