
function convertToArray(obj) {
    return Object.keys(obj).map(function (key) {
        return obj[key];
    });
}
var ctx = document.getElementById('myChart');
var datas = JSON.parse('{"pred_prob_cOPN": 0.7451652680682596, "pred_prob_cCON": 0.4583873144197018, "pred_prob_cEXT": 0.423620078378728, "pred_prob_cAGR": 0.5312039927185738, "pred_prob_cNEU": 0.37376760941448656}')
datas = convertToArray(datas)
var myChart = new Chart(ctx, {
    type: 'bar',
    data : {
        labels: ["OPN", "CON", "EXT", "AGR", "NEU"],
        datasets: [
            {
                fillColor: "rgb(30, 144, 255)",
                strokeColor: "rgb(30, 144, 255)",
                highlightFill: "rgb(22, 108, 192)",
                highlightStroke: "rgb(22, 108, 192)",
                data: datas

            }
        ]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});