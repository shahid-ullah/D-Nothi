var office_ids = [];
var sum_login_total = 0;
var sum_login_total_users = 0;
var sum_login_total_male_users = 0;
var sum_login_total_female_users = 0;
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
  $("#total_summary").css("display", "none");
}

function handleError(jqXHR, error_type, exception_object) {
  clear_table();
  $("#total_summary").css("display", "none");
  console.log(error_type);
}

function drawTable(data) {
  office_ids = data["office_ids"];
  var reports = data["reports"];
  sum_login_total = data["sum_login_total"];
  sum_login_total_users = data["sum_login_total_users"];
  sum_login_total_male_users = data["sum_login_total_male_users"];
  sum_login_total_female_users = data["sum_login_total_female_users"];
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

  $(".total_office").text(office_ids.length);
  $(".login_total").text(sum_login_total);
  $(".login_total_users").text(sum_login_total_users);
  $(".login_total_male_users").text(sum_login_total_male_users);
  $(".login_total_female_users").text(sum_login_total_female_users);
  $("#total_summary").css("display", "");
}

function tableToCSV() {
  var csv_data = [];
  $("tr", "#summary_table").each(function (index) {
    var csvrow = [];
    $("th, td", this).each(function (index) {
      csvrow.push($(this).text().split(",").join("     "));
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
  csv_data.push(
    ["", "সর্বমোট লগিন ব্যবহারকারী (মহিলা)", sum_login_total_female_users].join(
      ","
    )
  );
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
