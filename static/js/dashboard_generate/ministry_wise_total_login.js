$(document).ready(function () {
  Highcharts.chart("container2", {
    chart: {
      type: "pie",
      inverted: true,
      height: 500,
    },
    title: {
      align: "left",
      text: "মন্ত্রনালয় ভিত্তিক লগইনের হার",
    },
    subtitle: {
      align: "left",
      text: "",
    },
    accessibility: {
      announceNewData: {
        enabled: true,
      },
    },
    xAxis: {
      type: "category",
    },
    yAxis: {
      title: {
        text: "লগইন সংখ্যা",
      },
    },
    credits: {
      enabled: false,
    },
    legend: {
      enabled: false,
    },
    plotOptions: {
      pie: {
        allowPointSelect: true,
        cursor: "pointer",
        dataLabels: {
          enabled: true,
          format:
            "<b>{point.name}</b>: {point.percentage:.1f}% লগইন : {point.y} ",
        },
      },
    },

    tooltip: {
      headerFormat: '<span style="font-size:11px"></span>',
      pointFormat: '<span style="color:{point.color}"><b>{point.y}</b><br/>',
    },

    series: [
      {
        name: "Ministry Login",
        colorByPoint: true,
        data: ministry_general_series(ministry_map),
      },
    ],
  });
});
