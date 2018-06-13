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
                    text: '(%) Probability of being Mining'
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
            series: []
        });


    var shift = false;

    ws.onmessage = function (event) {
        probs = JSON.parse(event.data);

        var safe = true;
        var waiting = true;

        for (var port in probs) {
            if (probs.hasOwnProperty(port)) {
                if(port==="0" || port===0){
                    return;
                }

                // if has enough data
                var found = false;
                var i=0;

                for(; i<chart.series.length; i++){
                    if(chart.series[i]["name"]===port){
                        found = true;
                        break;
                    }
                }

                var prob = 0;

                if(!found){
                    chart.addSeries({
                        name: port,
                        data: []
                    });
                }

                if(probs[port].hasOwnProperty("Mining")){
                    // se não encontrou e tem mining, adicionar
                    prob = probs[port]["Mining"];
                    waiting = false;
                }else{
                    // se não encontrou e não tem mining, stand
                    prob = 0;
                }

                shift = (shift || (chart.series[i].data.length > 20)); // shift if the series is longer than 20

                chart.series[i].addPoint([(new Date()).getTime(), prob], true, shift);

                safe = (safe && (prob<=50));
            }
        }

        if(waiting){
            $("#waiting").show();
        }else if(safe){
            // found safe
            $("#foundSafe").show();
            $("#foundMining").hide();
            $("#waiting").hide();
        }else if(!safe){
            // found mining
            $("#foundMining").show();
            $("#foundSafe").hide();
            $("#waiting").hide();
        }
    };

});
