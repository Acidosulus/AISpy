
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

async function Add_Parameter_Return_Reconcilation_Act_Dialog_Success(parameter){
  console.log('result:');
  console.log(parameter);
}

async function Add_Parameter_Return_Reconcilation_Act(){
  returnedModalFormJSON = '';
  let dialog_parameter = {"title":"Период возврата акта сверки","backlink":"","parameters":[{"lable":"Месяц","name":"month","type":"listbox","size":12,"data":[{"id":1,"value":"Январь"},{"id":2,"value":"Февраль"},{"id":3,"value":"Март"},{"id":4,"value":"Апрель"},{"id":5,"value":"Май"},{"id":6,"value":"Июнь"},{"id":7,"value":"Июль"},{"id":8,"value":"Август"},{"id":9,"value":"Сентябрь"},{"id":10,"value":"Октябрь"},{"id":11,"value":"Ноябрь"},{"id":12,"value":"Декабрь"}]},{"lable":"Год","name":"year","type":"listbox","default":2024,"size":9,"data":[{"id":2018,"value":2018},{"id":2019,"value":2019},{"id":2020,"value":2020},{"id":2021,"value":2021},{"id":2022,"value":2022},{"id":2023,"value":2023},{"id":2024,"value":2024},{"id":2025,"value":2025},{"id":2026,"value":2026}]}],"success_jscode":"returnJSON","escape_jscode":"closeModal();"};
  let form_answer = await FillOutModalForm(dialog_parameter);
  console.log(form_answer);
  
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


function GetDesdignerULExcelResult(){
  $.ajax({
    url: '/designer_ul_get_excel_result',
    method: 'post',
    dataType: 'binary',
    xhrFields: {
        'responseType': 'blob'
    },
    success: function(response, status, xhr) {
        var downloadUrl = URL.createObjectURL(response);
        var a = document.createElement('a');
        a.href = downloadUrl;
        a.download = 'designer_ul.xlsx';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(downloadUrl);
      }
    }
  );  

}



