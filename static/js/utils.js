MONTH_NAME_MAP = {
  1: 'January',
  2: 'February',
  3: 'March',
  4: 'April',
  5: 'May',
  6: 'June',
  7: 'July',
  8: 'August',
  9: 'September',
  10: 'October',
  11: 'November',
  12: 'December',
}

function generateGeneralSeries(maps_data, name=""){
    general_series = []
    general_series_dictionary = {
      name: name,
      colorByPoint: true,
      data: []
    }
    general_series_data = []
    for (const [key, value] of Object.entries(maps_data)) {
      temp_dict ={
        name: key,
        y: value,
        drilldown: key,
      }
      general_series_data.push(temp_dict)
    }
    general_series_dictionary['data'] = general_series_data

    general_series = [general_series_dictionary]

    return general_series
}
// {# console.log(generateGeneralSeries(year_map, name="Offices Added in years")); #}

function generateDrilldownSeries(year_map, month_map, day_map){
  var drilldown_series = []
  for (const [year, value] of Object.entries(year_map)) {
    dict = {
      id: year,
      data: [],
    }
    var month_dict = month_map[year];
    for (const [month, value] of Object.entries(month_dict)){
      temp_dict = {};
      // {# temp_dict['name'] = month; #}
      temp_dict['name'] = MONTH_NAME_MAP[month];
      temp_dict['y'] = value;
      temp_dict['drilldown'] = year + month;
      dict['data'].push(temp_dict);


      // {# nested drilldown series #}
      var day_dict = day_map[year][month];
      id = year + month;
      nst_dict = {
        id: id,
        data : [],
      }
      for (const [day, value] of Object.entries(day_dict)){
        // {# console.log(day, value); #}
        nst_dict['data'].push([day, value]);
      }
      drilldown_series.push(nst_dict);

    }
    drilldown_series.push(dict)

  }
  return drilldown_series
}
// console.log('Loaded utils.js')
