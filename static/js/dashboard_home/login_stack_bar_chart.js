$(document).ready(function () {
  function fetch_login_stack_bar() {
    console.log("login stack bar called");
    $.ajax({
      url: "/",
      type: "GET",
      data: {},
      success: function (data) {
        console.log(data);
        male_list = data["male_list"];
        female_list = data["female_list"];
        months = data["months"];
        draw_login_stack_bar(male_list, female_list, months);
      },
      cache: false,
      processdata: true,
    });
  }
  fetch_login_stack_bar();

  function draw_login_stack_bar(male_list, female_list, months) {
    // login_map_json = document.getElementById("stack_bar_chart").textContent;
    // login_map_json = $("#stack_bar_chart").text();
    // login_map = JSON.parse(login_map_json);
    // male_list = login_map["male_list"];
    // female_list = login_map["female_list"];
    // months = login_map["months"];

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
  }
});
