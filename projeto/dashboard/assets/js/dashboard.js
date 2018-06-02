var dashboard = dashboard || {};
var ws = new WebSocket("ws://127.0.0.1:1234/");
var probs;

dashboard.initPieChart = function () {

    ws.onmessage = function (event) {
        probs = JSON.parse(event.data);

        var optionsPreferences = {
            donut: true,
            donutWidth: 40,
            startAngle: 0,
            total: 100,
            showLabel: false,
            axisX: {
                showGrid: false
            }
        };

        Chartist.Pie('#chartPreferences', optionsPreferences);

        Chartist.Pie('#chartPreferences', {
          labels: [probs[0]+'%', probs[1]+'%'],
          series: [probs[0],probs[1]]
        });
    };
}