
// add all agreements into list for current_user
function DataDesignerULAddAllAgreements(){
  $.ajax({
    url: '/designer_ul_add_all_agreements',
    method: 'post',
    dataType: 'html',
    data: {text: 'Текст'},
    success: function(data){
      alert(data);
    }
    });
}