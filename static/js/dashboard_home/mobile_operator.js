$(document).ready(function () {
  Highcharts.chart("mobileOperatorContainer", {
    credits: {
      enabled: false
    },
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
        name: "Total",
        data: [
          // ["GP", 72857],
          // ["BL", 14615],
          // ["Robi", 9983],
          // ["TeleTalk", 6326],
          // ["Airtel", 4722],
          // ["Others", 1582],
          ["গ্রামীনফোন", 72857],
          ["বাংলালিংক", 14615],
          ["রবি", 9983],
          ["টেলিটক", 6326],
          ["এয়ারটেল", 4722],
          ["অন্যান্য", 1582],

        ],
      },
    ],
  });
});
