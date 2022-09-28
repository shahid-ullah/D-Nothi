// Create the chart
$(document).ready(function () {
  let level = 1;
  let first_level_title = "নির্দিষ্ট বছরে যুক্ত মোট ব্যবহারকারী";
  let second_level_title = "নির্দিষ্ট মাসে যুক্ত মোট ব্যবহারকারী";
  let third_level_title = "নির্দিষ্ট দিনে যুক্ত ব্যবহারকারী";

  Highcharts.chart("container", {
    chart: {
      type: "column",
      events: {
        drilldown: function (e) {
          level = level + 1;
          if (level == 1) {
            this.setTitle({ text: first_level_title });
          }
          if (level == 2) {
            this.setTitle({ text: second_level_title });
          }
          if (level == 3) {
            this.setTitle({ text: third_level_title });
          }
        },
        drillup: function (e) {
          level = level - 1;
          if (level == 1) {
            this.setTitle({ text: first_level_title });
          }
          if (level == 2) {
            this.setTitle({ text: second_level_title });
          }
          if (level == 3) {
            this.setTitle({ text: third_level_title });
          }
        },
      },
    },
    title: {
      text: "নির্দিষ্ট বছরে যুক্ত মোট ব্যবহারকারী",
    },
    subtitle: {
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
        text: "নথি ব্যবহারকারী সংখ্যা",
      },
    },
    credits: {
      enabled: false,
    },
    legend: {
      enabled: false,
    },
    plotOptions: {
      series: {
        borderWidth: 0,
        dataLabels: {
          enabled: true,
        },
      },
    },

    tooltip: {
      headerFormat: '<span style="font-size:11px"></span>',
      pointFormat: '<span style="color:{point.color}"><b>{point.y}</b><br/>',
    },

    series: generateGeneralSeries(year_map, "year"),
    drilldown: {
      series: generateDrilldownSeries(year_map, month_map, day_map),
    },
  });

  function user_registration_year_trend() {
    var chart2 = new CanvasJS.Chart("chartContainer", {
      animationEnabled: true,
      title: {
        text: "Company Revenue by Year",
      },
      axisY: {
        title: "Revenue in USD",
        valueFormatString: "#0,,.",
        suffix: "mn",
        prefix: "$",
      },
      data: [
        {
          type: "splineArea",
          color: "rgba(54,158,173,.7)",
          markerSize: 5,
          xValueFormatString: "YYYY",
          yValueFormatString: "$#,##0.##",

          dataPoints: [
            { x: new Date(2016, 0), y: 17203 },
            { x: new Date(2017, 0), y: 43265 },
            { x: new Date(2018, 0), y: 66071 },
            { x: new Date(2019, 0), y: 87733 },
            { x: new Date(2020, 0), y: 100973 },
            { x: new Date(2021, 0), y: 109034 },
          ],
        },
      ],
    });
    chart2.render();
  }

  function birth_day_graph() {
    Highcharts.chart("container2", {
      chart: {
        type: "pie",
        inverted: true,
        height: 500,
      },
      title: {
        align: "left",
        text: "জন্মদিনের হার",
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
          text: "জন্মদিন সংখ্যা",
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
            format: "<b>{point.name}</b>: {point.percentage:.1f}%  ",
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
          data: [
            {
              name: "Saturday",
              y: 13977,
              sliced: true,
              selected: true,
            },
            {
              name: "Sunday",
              y: 14213,
            },
            {
              name: "Monday",
              y: 14390,
            },
            {
              name: "Tuesday",
              y: 14711,
            },
            {
              name: "Wednesday",
              y: 14305,
            },
            {
              name: "Thursday",
              y: 15475,
            },
            {
              name: "Friday",
              y: 14397,
            },
          ],
        },
      ],
    });
  }

  birth_day_graph();
});
