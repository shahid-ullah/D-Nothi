$(document).ready(function () {
  login_map_json = document.getElementById("stack_bar_chart").textContent;
  login_map = JSON.parse(login_map_json);
  male_list = login_map["male_list"];
  female_list = login_map["female_list"];
  months = login_map["months"];

  var options = {
    series: [
      {
        name: "পুরুষ",
        data: male_list,
      },
      {
        name: "মহিলা",
        data: female_list,
      },
    ],
    chart: {
      type: "bar",
      height: 350,
      stacked: true,
    },
    plotOptions: {
      bar: {
        horizontal: true,
      },
    },
    stroke: {
      width: 1,
      colors: ["#fff"],
    },
    title: {
      text: "পুরুষ, মহিলা লগইন (সর্বশেষ ৫ মাস)",
    },
    xaxis: {
      categories: months,
      labels: {
        formatter: function (val) {
          return val + "K";
        },
      },
    },
    yaxis: {
      title: {
        text: undefined,
      },
    },
    tooltip: {
      y: {
        formatter: function (val) {
          return val + "K";
        },
      },
    },
    fill: {
      opacity: 1,
    },
    legend: {
      position: "top",
      horizontalAlign: "left",
      offsetX: 40,
    },
  };

  var chart = new ApexCharts(
    document.querySelector("#login_stack_bar_chart"),
    options
  );
  chart.render();
});
