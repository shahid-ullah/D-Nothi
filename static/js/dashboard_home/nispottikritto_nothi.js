$(document).ready(function () {
  var xValues = [
    "jan",
    "Feb",
    "Mar",
    "Aprl",
    "May",
    "June",
    "July",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
  ];

  new Chart("nispottikritto_nothi", {
    type: "line",
    data: {
      labels: xValues,
      datasets: [
        {
          label: "2016",
          data: [860, 1140, 1060, 2080],
          borderColor: "black",
          fill: true,
        },
        {
          label: "2017",
          data: [860, 1140, 1060, 1060],
          borderColor: "red",
          fill: true,
        },
        {
          label: "2018",
          data: [1600, 1700, 1700, 1900, 2000, 2700, 4000, 5000, 6000, 7000],
          borderColor: "green",
          fill: true,
        },
        {
          label: "2019",
          data: [300, 700, 2000, 5000, 6000, 4000],
          borderColor: "blue",
          fill: true,
        },
      ],
    },
    options: {
      legend: {
        display: true,
        position: "right",
      },
      title: {
        display: true,
        text: "নিষ্পত্তিকৃত নথি",
      },
      animations: {
        tension: {
          duration: 1000,
          easing: "linear",
          from: 1,
          to: 0,
          loop: true,
        },
      },
    },
  });
});
