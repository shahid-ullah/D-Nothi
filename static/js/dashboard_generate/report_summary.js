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
});

function clear_table() {
  $("#nispotti_kritto_nothi").text("");
  $("#upokarvogi").text("");
  $("#note_nisponno").text("");
  $("#potrojari").text("");
  $("#total_login_users").text("");
}

function handleError(jqXHR, error_type, exception_object) {
  clear_table();
  console.log(error_type);
}

function drawTable(data) {
  reports = data["reports"];
  $("#nispotti_kritto_nothi").text(reports["nispottikritto_nothi"]);
  $("#upokarvogi").text(reports["upokarvogi"]);
  $("#note_nisponno").text(reports["note_nisponno"]);
  $("#potrojari").text(reports["potrojari"]);
  $("#total_login_users").text(reports["total_login"]);
  // console.log(data);
}
