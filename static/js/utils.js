MONTH_NAME_MAP = {
  1: "January",
  2: "February",
  3: "March",
  4: "April",
  5: "May",
  6: "June",
  7: "July",
  8: "August",
  9: "September",
  10: "October",
  11: "November",
  12: "December",
};

ministry_id_to_name_map = {
  1: "রাষ্ট্রপতির কার্যালয়",
  3: "প্রধানমন্ত্রীর কার্যালয়",
  4: "মন্ত্রিপরিষদ বিভাগ",
  5: "জনপ্রশাসন মন্ত্রণালয়",
  6: "সশস্র বাহিনী বিভাগ",
  7: "অর্থ মন্ত্রণালয়",
  10: "আইন, বিচার ও সংসদ বিষয়ক মন্ত্রণালয় ",
  12: "কৃষি মন্ত্রণালয়",
  13: "খাদ্য মন্ত্রণালয়",
  14: "ডাক, টেলিযোগাযোগ ও তথ্যপ্রযুক্তি মন্ত্রণালয়",
  15: "তথ্য ও সম্প্রচার মন্ত্রণালয়",
  16: "ধর্ম বিষয়ক মন্ত্রণালয়",
  17: "নির্বাচন কমিশন সচিবালয় ",
  18: "নৌ-পরিবহন মন্ত্রণালয়",
  19: "পররাষ্ট্র মন্ত্রণালয়",
  20: "পরিকল্পনা মন্ত্রণালয়",
  22: "পরিবেশ, বন ও জলবায়ু পরিবর্তন মন্ত্রণালয়",
  23: "প্রতিরক্ষা মন্ত্রণালয়",
  24: "বস্ত্র ও পাট মন্ত্রণালয়",
  25: "গৃহায়ন ও গণপূর্ত মন্ত্রণালয়",
  26: "বাণিজ্য মন্ত্রণালয়",
  27: "বিদ্যুৎ, জ্বালানি ও খনিজ সম্পদ মন্ত্রণালয়",
  29: "পার্বত্য চট্টগ্রাম বিষয়ক মন্ত্রণালয়",
  30: "বেসামরিক বিমান পরিবহন ও পর্যটন মন্ত্রণালয়",
  31: "ভূমি মন্ত্রণালয়",
  32: "মহিলা ও শিশু বিষয়ক মন্ত্রণালয়",
  33: "মৎস্য ও প্রাণিসম্পদ মন্ত্রণালয়",
  34: "যুব ও ক্রীড়া মন্ত্রণালয়",
  36: "শিল্প মন্ত্রণালয়",
  37: "শিক্ষা মন্ত্রণালয়",
  38: "প্রাথমিক ও গণশিক্ষা মন্ত্রণালয়",
  39: "বিজ্ঞান ও প্রযুক্তি মন্ত্রণালয়",
  40: "শ্রম ও কর্মসংস্থান মন্ত্রণালয়",
  41: "সমাজকল্যাণ মন্ত্রণালয়",
  42: "পানি সম্পদ মন্ত্রণালয়",
  43: "সংস্কৃতি বিষয়ক মন্ত্রণালয়",
  44: "স্বরাষ্ট্র মন্ত্রণালয়",
  45: "স্বাস্থ্য ও পরিবার কল্যাণ মন্ত্রণালয়",
  46: "স্থানীয় সরকার, পল্লী উন্নয়ন ও সমবায় মন্ত্রণালয়",
  48: "মুক্তিযুদ্ধ বিষয়ক মন্ত্রণালয়",
  49: "প্রবাসী কল্যাণ ও বৈদেশিক কর্মসংস্থান মন্ত্রণালয়",
  51: "দুর্যোগ ব্যবস্থাপনা ও ত্রাণ মন্ত্রণালয়",
  54: "রেলপথ মন্ত্রণালয়",
  55: "জন বিভাগ, রাষ্ট্রপতির কার্যালয়",
  56: "সুপ্রিম কোর্ট",
  57: "তথ্য ও যোগাযোগ প্রযুক্তি বিভাগ",
  58: "সড়ক পরিবহন ও সেতু মন্ত্রণালয়",
  59: "সেতু বিভাগ",
  60: "সড়ক পরিবহন ও মহাসড়ক বিভাগ",
  62: "বাংলাদেশ জাতীয় সংসদ",
  63: "ডেমো মন্ত্রণালয়",
  64: "টেস্ট মন্ত্রনালয় ১",
};

function generateGeneralSeries(maps_data, name = "") {
  general_series = [];
  general_series_dictionary = {
    name: name,
    colorByPoint: true,
    data: [],
  };
  general_series_data = [];
  for (const [key, value] of Object.entries(maps_data)) {
    temp_dict = {
      name: key,
      y: value,
      drilldown: key,
    };
    general_series_data.push(temp_dict);
  }
  general_series_dictionary["data"] = general_series_data;

  general_series = [general_series_dictionary];

  return general_series;
}
// {# console.log(generateGeneralSeries(year_map, name="Offices Added in years")); #}

function generateDrilldownSeries(year_map, month_map, day_map) {
  var drilldown_series = [];
  for (const [year, value] of Object.entries(year_map)) {
    dict = {
      id: year,
      data: [],
    };
    var month_dict = month_map[year];
    for (const [month, value] of Object.entries(month_dict)) {
      temp_dict = {};
      // {# temp_dict['name'] = month; #}
      temp_dict["name"] = MONTH_NAME_MAP[month];
      temp_dict["y"] = value;
      temp_dict["drilldown"] = year + month;
      dict["data"].push(temp_dict);

      // {# nested drilldown series #}
      var day_dict = day_map[year][month];
      id = year + month;
      nst_dict = {
        id: id,
        data: [],
      };
      for (const [day, value] of Object.entries(day_dict)) {
        // {# console.log(day, value); #}
        nst_dict["data"].push([day, value]);
      }
      drilldown_series.push(nst_dict);
    }
    drilldown_series.push(dict);
  }
  return drilldown_series;
}

function generate_general_series(raw_data_map) {
  series_data = [];
  for (key in raw_data_map) {
    data_object = {};
    data_object.name = key;
    data_object.y = raw_data_map[key];
    data_object.drilldown = key;
    series_data.push(data_object);
  }

  return series_data;
}

function ministry_general_series(raw_data) {
  series_data = [];
  for (key in raw_data) {
    var data_object = {};
    var ministry_name = ministry_id_to_name_map[key];
    if (ministry_name == undefined) {
      data_object.name = key;
    } else {
      data_object.name = ministry_name;
    }
    data_object.y = raw_data[key];
    data_object.drilldown = null;
    series_data.push(data_object);
  }

  return series_data;
}
