
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

function GetSourceFromServer(){
      //get_source
      $.ajax({
        url: '/designer_ul_get_source',
        method: 'post',
        dataType: 'html',
        data: {text: 'Текст'},
        success: function(data){
          ClearSourceData()
          for (let row of JSON.parse(data)){
                  $('#agreements_and_points_list').append($('<option>', {
                    value: '',
                    text: `${row.agreement} ${row.point.trim().length>0?'-':''} ${row.point.trim()}`
                }));
          }
        }}); //get_source

}


if ($('#report_designer_ul').length) {

  GetSourceFromServer();
  
}