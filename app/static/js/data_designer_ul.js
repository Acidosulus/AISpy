
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
      $(`#agreements_points_lable`).text('Договора - Точки учета');
      //get_source
      $.ajax({
        url: '/designer_ul_get_source',
        method: 'post',
        dataType: 'html',
        data: {text: 'Текст'},
        success: function(data){
          var counter = 0;
          ClearSourceData()
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


async function GetDataFromClipboard(){
  return await navigator.clipboard.readText();
}


async function InsertDataAgreementsFromClipboard() {
  let insertedtext = await GetDataFromClipboard();
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

async function InsertDataPointsFromClipboard() {
  let insertedtext = await GetDataFromClipboard();
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



function AddData_Agreement_name(){
  $.ajax({
    url: '/designer_ul_add_data',
    method: 'post',
    dataType: 'json',
    data: JSON.stringify({type:'agreement_names'}),
    success: function(data){
      GetSourceFromServer();
    }});
}



if ($('#report_designer_ul').length) {
  GetSourceFromServer();
}



async function AskText(){

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

  return await AskText_promise;
}