var office_ids = [];
var sum_login_total = 0;
var sum_login_total_users = 0;
var sum_login_total_male_users = 0;
var sum_login_total_female_users = 0;
var sum_nispottikritto_nothi = 0;
var sum_upokarvogi = 0;
var sum_note_nisponno = 0;
var sum_potrojari = 0;
var offices_id_name_map = {};
$(document).ready(function () {
  $("#fromdate_datepicker").datepicker({
    dateFormat: "dd-mm-yy",
  });
  $("#todate_datepicker").datepicker({
    dateFormat: "dd-mm-yy",
  });

  $("form#report_summary").submit(function (e) {
    e.preventDefault();
    var data = $("form#report_summary").serialize();

    $.ajax({
      url: $(this).attr("action"),
      type: "GET",
      data: data,
      success: function (data) {
        clear_table();
        drawTable(data);
      },
      cache: false,
      processData: true,
      error: handleError,
    });
  });

  $("#download_as_csv").click(tableToCSV);
});

function clear_table() {
  $("#table_data").empty();
}

function handleError(jqXHR, error_type, exception_object) {
  clear_table();
  console.log(error_type);
}

function drawTable(data) {
  office_ids = data["office_ids"];
  var reports = data["reports"];
  sum_login_total = data["sum_login_total"];
  sum_login_total_users = data["sum_login_total_users"];
  sum_login_total_male_users = data["sum_login_total_male_users"];
  sum_login_total_female_users = data["sum_login_total_female_users"];
  sum_nispottikritto_nothi = data["sum_nispottikritto_nothi"];
  sum_upokarvogi = data["sum_upokarvogi"];
  sum_note_nisponno = data["sum_note_nisponno"];
  sum_potrojari = data["sum_potrojari"];
  offices_id_name_map = data["offices_id_name_map"];

  for (let i = 0; i < office_ids.length; i++) {
    var office_id = office_ids[i];
    var row = `<tr>
        <th scope="row">${office_id}</th>
        <td id=${office_id}_name></td>
        <td id=${office_id}_login_total>0</td>
        <td id=${office_id}_login_total_users>0</td>
        <td id=${office_id}_login_total_male_users>0</td>
        <td id=${office_id}_login_total_female_users>0</td>
        <td id=${office_id}_nispottikritto_nothi>0</td>
        <td id=${office_id}_upokarvogi>0</td>
        <td id=${office_id}_note_nisponno>0</td>
        <td id=${office_id}_potrojari>0</td>
      </tr>`;
    $("#table_data").append(row);
  }

  for (const [report_type, report] of Object.entries(reports)) {
    for (const [office_id, counts] of Object.entries(report)) {
      var element_id = "#" + office_id + "_" + report_type;
      $(element_id).text(counts);
    }
  }
  for (const [office_id, office_name] of Object.entries(offices_id_name_map)) {
    var element_id = "#" + office_id + "_" + "name";
    $(element_id).text(office_name);
  }
  $("#total_summary .total_office").text(office_ids.length);
  $("#total_summary .login_total").text(sum_login_total);
  $("#total_summary .login_total_users").text(sum_login_total_users);
  $("#total_summary .login_total_male_users").text(sum_login_total_male_users);
  $("#total_summary .login_total_female_users").text(
    sum_login_total_female_users
  );
  $("#total_summary .nispottikritto_nothi").text(sum_nispottikritto_nothi);
  $("#total_summary .upokarvogi").text(sum_upokarvogi);
  $("#total_summary .note_nisponno").text(sum_note_nisponno);
  $("#total_summary .potrojari").text(sum_potrojari);
  $("#total_summary").css("display", "");
}

function tableToCSV() {
  var csv_data = [];
  var header_row = [
    "মোট অফিস",
    "অফিসের নাম",
    "মোট লগইন",
    "মোট লগইন ব্যবহারকারী",
    "মোট লগইন ব্যবহারকারী (পুরুষ)",
    "মোট লগইন ব্যবহারকারী (মহিলা)",
    "নিষ্পত্তিকৃত নথি",
    "উপকারভোগী",
    "নোট নিষ্পন্ন",
    "পত্রজারি",
  ];
  csv_data.push(header_row.join(","));
  $("tr", "#table_data").each(function (index) {
    var csvrow = [];
    $("th, td", this).each(function (index) {
      // csvrow.push($(this).text());
      csvrow.push($(this).text().split(",").join("     "));
      // console.log($(this).text());
    });
    csv_data.push(csvrow.join(","));
  });
  csv_data.push(["", "", ""].join(","));
  csv_data.push(["", "", ""].join(","));
  csv_data.push(["", "", ""].join(","));
  var footer_row = ["", "সর্বমোট অফিস", office_ids.length];
  csv_data.push(footer_row.join(","));
  csv_data.push(["", "সর্বমোট লগিন", sum_login_total].join(","));
  csv_data.push(
    ["", "সর্বমোট লগিন ব্যবহারকারী", sum_login_total_users].join(",")
  );
  csv_data.push(
    ["", "সর্বমোট লগিন ব্যবহারকারী (পুরুষ)", sum_login_total_male_users].join(
      ","
    )
  );
  csv_data.push(["", "নিষ্পত্তিকৃত নথি", sum_nispottikritto_nothi].join(","));
  csv_data.push(["", "উপকারভোগী", sum_upokarvogi].join(","));
  csv_data.push(["", "নোট নিষ্পন্ন", sum_note_nisponno].join(","));
  csv_data.push(["", "পত্রজারি", sum_potrojari].join(","));
  csv_data = csv_data.join("\n");
  downloadCSVFile(csv_data);
}

function downloadCSVFile(csv_data) {
  CSVFile = new Blob([csv_data], { type: "text/csv" });

  var temp_link = document.createElement("a");
  var today = new Date();
  var date =
    today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate();
  var time = today.getHours() + "_" + today.getMinutes();
  var file_name = "report_" + date + "_" + time + ".csv";
  temp_link.download = file_name;
  var url = window.URL.createObjectURL(CSVFile);
  temp_link.href = url;

  temp_link.style.display = "none";
  document.body.appendChild(temp_link);

  temp_link.click();
  document.body.removeChild(temp_link);
}
