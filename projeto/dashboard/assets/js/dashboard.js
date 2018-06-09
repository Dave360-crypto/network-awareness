$(document).ready(function(){
    var ws = new WebSocket("ws://127.0.0.1:1234/ws");
    var probs;


    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });

    var chart = Highcharts.chart('live', {
            chart: {
                type: 'spline',
                animation: Highcharts.svg, // don't animate in old IE
                marginRight: 10
            },
            title: {
                text: ''
            },
            xAxis: {
                type: 'datetime',
                tickPixelInterval: 150
            },
            yAxis: {
                title: {
                    text: 'Probability'
                },
                plotLines: [{
                    min: 0,
                    max: 100
                }]
            },
            tooltip: {
                formatter: function () {
                    return '<b>' + this.series.name + '</b><br/>' +
                        Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                        Highcharts.numberFormat(this.y, 2);
                }
            },
            legend: {
                enabled: false
            },
            exporting: {
                enabled: false
            },
            series: [
                {
                    name: 'Mining',
                    color: '#FF4A55',
                    data: []
                },
                {
                    name: 'Others',
                    color: '#87CB16',
                    data: []
                }
            ]
        });

    ws.onmessage = function (event) {
        probs = JSON.parse(event.data);

        if (probs[0]+probs[1]===0){
            $("#waiting").show();
        }else if (probs[0]>=probs[1]){
            // found mining
            $("#foundMining").show();
            $("#foundSafe").hide();
            $("#waiting").hide();
        }else{
            // found safe
            $("#foundSafe").show();
            $("#foundMining").hide();
            $("#waiting").hide();
        }

        // update highchart series

        var x = (new Date()).getTime(), // current time
            y1 = probs[0],
            y2 = probs[1];

        // y1
        var series = chart.series[0],
            shift = series.data.length > 20; // shift if the series is
                                             // longer than 20

        chart.series[0].addPoint([x, y1], true, shift);

        // y2
        series = chart.series[1];
        shift = series.data.length > 20; // shift if the series is
                                             // longer than 20
        chart.series[1].addPoint([x, y2], true, shift);
    };

});
