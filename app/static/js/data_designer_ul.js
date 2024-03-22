
// add all agreements into list for current_user
function DataDesignerULAddAllAgreements(){
  // add_all_agreements
  $.ajax({
    url: '/designer_ul_add_all_agreements',
    method: 'post',
    dataType: 'html',
    data: {text: 'Текст'},
    success: function(data){
      ClearSourceData()
      GetSourceFromServer();
    }});// add_all_agreements
}

function DataDesignerULAddOpenedAgreements(){
  // add_all_agreements
  $.ajax({
    url: '/designer_ul_add_opened_agreements',
    method: 'post',
    dataType: 'html',
    data: {text: 'Текст'},
    success: function(data){
      ClearSourceData()
      GetSourceFromServer();
    }});// add_all_agreements
}


function ClearSourceDataonServer(){
  $.ajax({
    url: '/designer_ul_clear_data_endpoint',
    method: 'post',
    dataType: 'html',
    data: {text: 'Текст'},
    success: function(data){
      GetSourceFromServer();
    }});
}

function ClearSourceData(){
  $('#agreements_and_points_list').empty();
}


function ClearSourceDataonServerParameters(){
  $.ajax({
    url: '/designer_ul_clear_data_parameters',
    method: 'post',
    dataType: 'html',
    data: {text: 'Текст'},
    success: function(data){
      GetSourceFromServerParameters();
    }});
}

function ClearSourceDataParameters(){
  $('#added_fields_list').empty();
}

// add all points into list for current_user
function DataDesignerULAddAllPoints(){
  // add_all_agreements
  $.ajax({
    url: '/designer_ul_add_all_points',
    method: 'post',
    dataType: 'html',
    data: {text: 'Текст'},
    success: function(data){
      ClearSourceData()
      GetSourceFromServer();
    }});// add_all_agreements
  }

  function DataDesignerULAddAllPointsOfOpenedAgreements(){
    // add_all_agreements
    $.ajax({
      url: '/designer_ul_add_all_points_of_opened_agreements',
      method: 'post',
      dataType: 'html',
      data: {text: 'Текст'},
      success: function(data){
        ClearSourceData()
        GetSourceFromServer();
      }});// add_all_agreements
    }
  
  
function GetSourceFromServer(){
      ClearSourceData();
      $(`#agreements_points_lable`).text('Договора - Точки учета');
      //get_source
      $.ajax({
        url: '/designer_ul_get_source',
        method: 'post',
        dataType: 'html',
        data: '',
        success: function(data){
          var counter = 0;
          for (let row of JSON.parse(data)){
                  $('#agreements_and_points_list').append($('<option>', {
                    value: '',
                    text: `${row.agreement} ${row.point.trim().length>0?'-':''} ${row.point.trim()}`
                }));
                counter++;
          }
          $(`#agreements_points_lable`).text('Договора - Точки учета');
          $(`#agreements_points_lable`).append(` <sup class="text-success">${counter}</sp>`);
        }}); //get_source
}



function GetSourceFromServerParameters(){
  $(`#parameters_lable`).text('Добавляемые поля');
  ClearSourceDataParameters();
  //get_source
  $.ajax({
    url: '/designer_ul_get_source_parameters',
    method: 'post',
    dataType: 'html',
    data: '',
    success: function(data){
      var counter = 0;
      console.log('Добавляемые поля:');
      console.log(data);
      for (let row of JSON.parse(data)){
              $('#added_fields_list').append($('<option>', {
                text: row.name
            }));
            counter++;
      }
      $(`#parameters_lable`).text('Добавляемые поля');
      $(`#parameters_lable`).append(` <sup class="text-success">${counter}</sp>`);
    }}); //get_source
}

async function GetDataFromClipboard(){
  return await navigator.clipboard.readText();
}

async function InsertDataAgreementsFromClipboard_ShowInterface() {
  FillOutModalForm({"title":"Вставьте номера договоров из Excel",
                    "backlink":"",
                    "parameters":[{ "lable":"Номера договоров",
                                    "name":"agreements",
                                    "type":"text",
                                    "default":"",
                                    "size":24,
                                    "data":[]}],
                    "success_jscode":"InsertDataAgreementsFromClipboard($('#agreements').val());closeModal();", "escape_jscode":"closeModal();"});
}

async function InsertDataAgreementsFromClipboard(insertedtext) {
  $.ajax({
    url: '/insert_data_agreements_from_clipboard',
    method: 'post',
    dataType: 'html',
    data: insertedtext,
    success: function(data){
        GetSourceFromServer();
      }
    }); 
}


async function InsertDataPointsFromClipboard_ShowInterface() {
  FillOutModalForm({"title":"Вставьте номера точек учета из Excel",
                    "backlink":"",
                    "parameters":[{ "lable":"Номера Точек Учета",
                                    "name":"points",
                                    "type":"text",
                                    "default":"",
                                    "size":24,
                                    "data":[]}],
                    "success_jscode":"InsertDataPointsFromClipboard($('#points').val());closeModal();", "escape_jscode":"closeModal();"});
}



async function InsertDataPointsFromClipboard(insertedtext) {
  $.ajax({
    url: '/insert_data_points_from_clipboard',
    method: 'post',
    dataType: 'html',
    data: insertedtext,
    success: function(data){
        GetSourceFromServer();
      }
    }); 
}



async function Add_Parameter(jsonParameter){
  $.ajax({
    url: '/designer_ul_add_data',
    method: 'post',
    dataType: 'json',
    data: JSON.stringify(jsonParameter),
    complete: function(data){
      GetSourceFromServerParameters();
    }});

}

function get_month_name(monthNumber){
  const months = [
    "Январь",
    "Февраль",
    "Март",
    "Апрель",
    "Май",
    "Июнь",
    "Июль",
    "Август",
    "Сентябрь",
    "Октябрь",
    "Ноябрь",
    "Декабрь"
  ];

  if (monthNumber >= 1 && monthNumber <= 12) {
      return months[monthNumber - 1];
  } else {
      return "Некорректный номер месяца";
  }
}


function Add_Parameter_Return_Reconcilation_Act(){
  const currentDate = new Date();
  const currentYear = currentDate.getFullYear();
  const currentMonth = currentDate.getMonth() + 1;
  let dialog_parameter = {"title":"Период возврата акта сверки",
                          "backlink":"",
                          "parameters":[{ "lable":"Месяц",
                                          "name":"month",
                                          "type":"listbox",
                                          "default":currentMonth,
                                          "size":12,
                                          "data":[{"id":1,"value":"Январь"},{"id":2,"value":"Февраль"},{"id":3,"value":"Март"},{"id":4,"value":"Апрель"},{"id":5,"value":"Май"},{"id":6,"value":"Июнь"},{"id":7,"value":"Июль"},{"id":8,"value":"Август"},{"id":9,"value":"Сентябрь"},{"id":10,"value":"Октябрь"},{"id":11,"value":"Ноябрь"},{"id":12,"value":"Декабрь"}]},
                                        { "lable":"Год",
                                          "name":"year",
                                          "type":"listbox",
                                          "default":currentYear,
                                          "size":9,
                                          "data":[{"id":2018,"value":2018},{"id":2019,"value":2019},{"id":2020,"value":2020},{"id":2021,"value":2021},{"id":2022,"value":2022},{"id":2023,"value":2023},{"id":2024,"value":2024},{"id":2025,"value":2025},{"id":2026,"value":2026}]}],
                          "success_jscode":"",
                          "escape_jscode":"closeModal();"};
  FillOutModalForm(dialog_parameter);
    document.getElementById("button_modal_dialog_ok").addEventListener("click", () => {
      let result = Ok(JSON.stringify(dialog_parameter));
      console.log(result);
      console.log(result.year);
      console.log(result.month);
      /*console.log(result[0].month);
      console.log(result[1].year);*/
      
      $.ajax({
        url: '/designer_ul_add_data',
        method: 'post',
        dataType: 'json',
        data: JSON.stringify({'type':'agreement_return_of_reconcilation_act', 'name':`Возврат акта сверки за ${get_month_name(result.month)} ${result.year} г.`, 'year':result.year, 'month':result.month}),
        complete: function(data){
          GetSourceFromServerParameters();
        }});
    
    });

}




if ($('#report_designer_ul').length) {
  GetSourceFromServer();
  GetSourceFromServerParameters();
}



async function AskText(){

  FillOutModalForm({"title":"Вставьте номера договоров из Excel",
                    "backlink":"",
                    "parameters":[{ "lable":"Номера договоров",
                                    "name":"agreements",
                                    "type":"text",
                                    "default":"",
                                    "size":24,
                                    "data":[]}],
                    "success_jscode":"console.log($('#agreements').val());closeModal();", "escape_jscode":"console.log('escape');closeModal();"});

  /*
  // Создаётся объект promise
  var AskText_promise = await new Promise((AskText_resolve, AskText_reject) => {
   
      FillOutModalForm({"title":"Вставьте номера договоров из Excel",
                        "backlink":"",
                        "parameters":[{ "lable":"Номера договоров",
                                        "name":"agreements",
                                        "type":"text",
                                        "default":"",
                                        "size":24,
                                        "data":[]}],
                        "success_jscode":"", "escape_jscode":""});

                        $('#button_modal_dialog_ok').on('click', function() {
                          let ctext = AskText_resolve($('#agreements').val());
                          closeModal();
                          return ctext;
                        });

                        $('#button_modal_dialog_escape').on('click', function() {
                          closeModal();
                          return AskText_reject();
                        });

            });
  return AskText_promise;
            */


  
}

function DownloadExcel( url, file_name){
	$.ajax({
		url: url,
		method: 'post',
		dataType: 'binary',
		data:JSON.stringify({file_name:`${file_name}`}),
		xhrFields: {
			'responseType': 'blob'
		},
		success: function(response, status, xhr) {
			var downloadUrl = URL.createObjectURL(response);
			var a = document.createElement('a');
			a.href = downloadUrl;
			a.download = file_name;
			document.body.appendChild(a);
			a.click();
			window.URL.revokeObjectURL(downloadUrl);
		  }
		}
	  );  
}


function GetDesdignerULExcelResult(){
  $.ajax({
    url: '/designer_ul_get_excel_result',
    method: 'post',
    dataType: 'html',
    data: '',
    success: function(data){
      var ul_designer_guid = data
      console.log(ul_designer_guid);

	  timer = setInterval(function() {
        Check_for_file_ready(ul_designer_guid, timer);
      }, 2000);
	}
  })
}


function Check_for_file_ready(uid, timer) {
	$.ajax({
		url: '/Check_Celery_Task_Status',
		method: 'post',
		dataType: 'html',
		data: `{"uid":"${uid}"}`,
		success: function(data){
			if (data.length>0){
				clearInterval(timer);
		  		console.log(`result:${data}`);
				DownloadExcel('/download_report_from_file_store',data);
			}
		}
	})
}

