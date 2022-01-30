// let year_select = document.querySelector('.year_select');
// console.log('year_select: ', year_select);

// year_select.addEventListener('change', handleYearSelect);


function handleYearSelect(event){
  console.log('handle year select');
  let year = event.target.value;
  if (year.length > 4){
    return;
  }
  $.getJSON( `report/${year}/`, function( data ) {
    drawReport(data, year);
  });
  return;
}


function drawReport(data, year=null){

  if (year){
    document.querySelector(".current_year").innerHTML = "Report year: " + year;
  }
  else {
    const d = new Date();
    let year = d.getFullYear();
    // document.querySelector(".current_year").innerHTML = "Report year: " + year;
  }

  cleanTableData();
  regenerateTable(data);

  return;
}

function regenerateTable(data){
  for (key in data){
    let value = data[key];
    var month = value.month.month;
    for (k in value){
      if (k == 'month' || k == 'year' || k == 'id' || k == 'uuid' || k == 'created' || k == 'updated' || k == 'creator'){
        console.log("");
      }
      else {
          let v = value[k];
          var element_class = "." + k + "_" + month;
          var el = document.querySelector(element_class)
          if (el){
            el.innerHTML = v;
          }
      }
    }
  }

  return;
}


function cleanTableData(){
  let report_attribute =[
    'total_office',
    'nispotti_krito_nothi',
    'total_upokarvogi',
    'total_nothi_users_male',
    'total_nothi_users_female',
    'total_mobile_app_users',
    'total_nisponno',
    'total_potrojari']

  let years = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

  report_attribute.forEach(function(value1, index, array){
    years.forEach(function(value2, index, array){
      let value3 = "." + value1 + "_" + value2;
      var el = document.querySelector(value3);
      el.innerHTML = null;
    })
  })

  return;
}


 $(document).ready(function () {
   // $.getJSON( "report/", function( data ) {
   //   drawReport(data);
   // });
   console.log('monthly report js loaded');
 });
