$(document).ready(function () {
  Highcharts.chart("mobileOperatorContainer", {
    chart: {
      type: "pie",
      height: "300px",
      options3d: {
        enabled: true,
        alpha: 45,
      },
    },
    title: {
      text: "",
    },
    subtitle: {
      text: "",
    },
    plotOptions: {
      pie: {
        innerSize: 100,
        depth: 45,
      },
    },
    series: [
      {
        name: "Delivered amount",
        data: [
          ["GP", 72857],
          ["BL", 14615],
          ["Robi", 9983],
          ["TeleTalk", 6326],
          ["Airtel", 4722],
          ["Others", 1582],
        ],
      },
    ],
  });
});
