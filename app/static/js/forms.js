var forms_zindex=1;

var forms = [];



const closeModal = function () {
    document.getElementById('mform').classList.add("hidden");
};

var border_colors = ["border-primary", "border-secondary", "border-success", "border-danger", "border-warning", "border-info", "border-light", "border-dark", "border-white"];


document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") {
    CloseToplevelDynamicForm();
  }
});

function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}


// open modal function
async function openModal(uri_for_get_JSON) {
    document.getElementById('mform').classList.remove("hidden");
    await FillOutModalForm(uri_for_get_JSON);
  };


async function asyncRequest (uri, method, data, debug=false){
    let response_promise = await fetch(uri, {method: method, headers: { 'Content-Type': 'application/json;charset=utf-8' }, body: JSON.stringify(data) } )
    return response_promise.json();
}

async function FillOutModalForm(uri_for_get_JSON){

    const str_card_begin = `<div class="card text-secondary-emphasis bg-secondary-subtle border border-secondary-subtle rounded-3" style="padding: 1em;">`;
    const str_card_end = `</div>`;

    let answer = await asyncRequest(uri_for_get_JSON, `POST`, {});
    var source = answer;
    const rootNode = document.getElementById('mform');
    rootNode.innerHTML = "";
    if (source.title!=null){
      rootNode.insertAdjacentHTML(`beforeend`,`<h1 class="p-3 text-primary-emphasis bg-primary-subtle border border-primary-subtle rounded-3">${source.title}</h1><hr><hr>`);
    }
    if (source.parameters!=null){
      for (let section of source.parameters){
  
        if (section.type==`edit`){
          rootNode.insertAdjacentHTML(`beforeend`,`${str_card_begin}<div class="row"><div class="col-4"><label for="${section.name}">${section.lable} </label></div><div class="col-8"><input class="container-fluid" autocomplete="off" type="text" name="${section.name}" id="${section.name}" value ="${section.default}"></div>${str_card_end}</div><br>` );
        } //edit
  
        if (section.type==`date`){
          rootNode.insertAdjacentHTML(`beforeend`,`${str_card_begin}<div class="row"><div class="col-4"><label for="${section.name}">${section.lable} </label></div><div class="col-8"><input class="container-fluid" autocomplete="off" type="date" name="${section.name}" id="${section.name}" value ="${section.default}"></div>${str_card_end}</div><br>` );
        } //edit
  
        if (section.type==`checkbox`){
          rootNode.insertAdjacentHTML(`beforeend`,`${str_card_begin}<div class="row"><div class="col-4"><label for="${section.name}">${section.lable}</label></div><div class="col-8"><input autocomplete="off" type="checkbox" name="${section.name}" id="${section.name}" ${Number(section.default)==1?"checked":""}></div>${str_card_end}</div><br>`
          );
        } //checkbox
  
        if (section.type==`text`){
          rootNode.insertAdjacentHTML(`beforeend`, `${str_card_begin}<div class="row"><div class="col-4"><label for="${section.name}">${section.lable} </label></div><div class="col-8"><textarea class="container-fluid" autocomplete="off" name="${section.name}" id="${section.name}" >${section.default}</textarea></div>${str_card_end}</div><br>`
          );
        } //textarea
      if (section.type==`listbox`){
        let st = ``;
        st +=`${str_card_begin}<div class="row"><div class="col-4"><label for="${section.name}">${section.lable} </label>${(section.size!=null?(Number(section.size)>0?'<br>':""):"")}`;
        st +=`</div><div class="col-8"> <select class="container-fluid" name="${section.name}" id="${section.name}" ${(section.size!=null?(Number(section.size)>0?'size="'+section.size+'"':""):"")}>`;
            for (const listelement of section.data){
                  st +=`<option value="${listelement.id}"`+((listelement.id==section.default)?` selected `:``)+`>${listelement.value}</option>`;
                  console.log(listelement.id, section.default, (listelement.id == section.default))
                }
                st += `</select></div>${str_card_end}</div><br>`;
              rootNode.insertAdjacentHTML('beforeend',st);
        } //listbox
      }
    }
    rootNode.insertAdjacentHTML(`beforeend`,`<hr><hr><br><div class="container"> <div class="row"><div class="col-sm-8"><button type="submit" class="btn btn-primary btn-lg btn-block col-6" id="button_modal_dialog_ok">&nbsp&nbsp&nbsp&nbspОк&nbsp&nbsp&nbsp&nbsp</button></div><div class="col-sm-4"><button type="button" class="btn btn-secondary btn-lg btn-block col-12" onclick='closeModal();'>Отмена</button></div></div>`);
    const ok_button = document.getElementById('button_modal_dialog_ok');
    if (source.success_jscode.length>0){
      console.log(`jscode`);
      ok_button.onclick = function() { eval(source.success_jscode); };
    }
    
    if (source.backlink.length>0){
      console.log(`backlink`  );
      rootNode.action = source.backlink;
    }
}


  //  function read intered parameters an sent them on the server
  function Ok(source){
    console.log('Ok function:')
    var result = [];
    if (source.parameters!=null){
    for (let section of source.parameters){
      if (section.type==`edit`){
          foo = {};
          foo[section.name]=document.getElementById(section.name).value;
          result.push(foo);
        }//if (section.type==`edit`)
        if (section.type==`date`){
          foo = {};
          foo[section.name]=document.getElementById(section.name).value;
          result.push(foo);
        }//if (section.type==`edit`)

      if (section.type==`text`){
          foo = {};
          foo[section.name]=document.getElementById(section.name).value;
          result.push(foo);
        }//if (section.type==`text`)
      if (section.type==`checkbox`){
          foo = {};
          foo[section.name]=document.getElementById(section.name).checked;
          result.push(foo);
        }//if (section.type==`checkbox`)
       if (section.type==`listbox`){
          foo = {};
          foo[section.name]=document.getElementById(section.name).value;
          result.push(foo);
        }//if (section.type==`listbox`)
      }//for (let section of source.parameters)
    }//if (source.parameters!=null)
    return result;
  }//function


  async function FillOutOrganizationForm() {
    /*
    let organization_id = document.getElementById(`row_id`).dataset.row_id;
    let answer = await asyncRequest(`/get_organization_data/${organization_id}`, `POST`, {});
    document.getElementById("Организация Краткое название").value = answer.org_short_name;
    document.getElementById("Организация Полное название").value = answer.org_name;
    document.getElementById("Организация ИНН").value = answer.inn;
    document.getElementById("Организация КПП").value = answer.kpp;
    document.getElementById("Организация ОРГН/ОРГИП").value = answer.ogrn;
    */
  }

  function CloseInScreenForm(form_id){
   document.getElementById(form_id).remove();
  }

  function CloseToplevelDynamicForm(){
    nodes = document.getElementsByClassName(`dynamic-form`);
    let maxIndex = -9999999999;
    let toplevelFormId = ``;
    for ( let node of document.getElementsByClassName(`dynamic-form`)){
      if (maxIndex< Number(node.dataset.zindex)){
        maxIndex = Number(node.dataset.zindex);
        toplevelFormId = node.id;
      } //if
    } //for
    if (toplevelFormId.length>0){
      CloseInScreenForm(toplevelFormId);
    }
  }

// run in screen form, fill and show
  function RunInScreenForm (form_name, execute_after_load, request_link) {
    let outerRootElement = document.getElementsByTagName(`body`)[0];
    form_name = form_name + `_${getRandomInt(999999999999999999)}`
    forms_zindex++;
    console.log(forms_zindex);
    outerRootElement.insertAdjacentHTML(
      `beforeEnd`,
      `<div id="${form_name}" style="background-color:#dee2e6;" class="dynamic-form position-absolute top-50 start-50 translate-middle border-5 ${border_colors[forms_zindex%9]}" data-zindex="${forms_zindex}"></div>`);
    
    forms.push(form_name);
    document.getElementById(forms[forms.length-1]).setAttribute(`z-index`, forms_zindex);
   
    let xhr = new XMLHttpRequest();
    xhr.open(`GET`, request_link);
    xhr.send();
    xhr.onload = function() {
      document.getElementById(`${forms[forms.length-1]}`).insertAdjacentHTML(`afterBegin`, xhr.responseText);

      document.getElementById(`${forms[forms.length-1]}`).insertAdjacentHTML(
        `beforeEnd`,
        `<hr><br>
          <div class="row">
            <div class="col-11">
            <!--  <button type="submit" class="btn btn-primary btn-lg btn-block col-6" id="button_modal_dialog_ok">
                &nbsp&nbsp&nbsp&nbspОк&nbsp&nbsp&nbsp&nbsp
               </button>-->
            </div>
            <div class="col-1">
              <button id="${forms[forms.length-1]}_dialog_escape_button" type="button" class="btn btn-secondary btn-lg btn-block col-12" onclick="CloseInScreenForm('${forms[forms.length-1]}');">
                Отмена
              </button>
            </div>`);
      eval(execute_after_load);

      console.log(document.getElementById(`${forms[forms.length-1]}`).getBoundingClientRect().height);
      console.log(document.getElementById(`${forms[forms.length-1]}_dialog_escape_button`).getBoundingClientRect().top);
      console.log(document.getElementById(`${forms[forms.length-1]}_dialog_escape_button`).getBoundingClientRect().height);
      document.getElementById(`${forms[forms.length-1]}`).getBoundingClientRect().height = document.getElementById(`${forms[forms.length-1]}_dialog_escape_button`).getBoundingClientRect().top
                                                                             + document.getElementById(`${forms[forms.length-1]}_dialog_escape_button`).getBoundingClientRect().height + 24;
      let new_form_height = document.getElementById(`${forms[forms.length-1]}_dialog_escape_button`).getBoundingClientRect().top + document.getElementById(`${forms[forms.length-1]}_dialog_escape_button`).getBoundingClientRect().height + 50;
      document.getElementById(`${forms[forms.length-1]}`).setAttribute("style",`height:${new_form_height}px`);
      if (typeof(document.getElementsByClassName('navbar')[0])=='undefined'){
          document.getElementById(`${forms[forms.length-1]}`).setAttribute("style",`top:${25}px`);
          console.log(150);
      }
      else{
        document.getElementById(`${forms[forms.length-1]}`).setAttribute("style",`top:${150}px`);
        console.log(25);
      }
      
    };
 }

 let timerId = setInterval(() => TimerProcceed(), 500);
function TimerProcceed(){
    nodes = document.getElementsByClassName(`dynamic-form`);
    if (nodes.length>0){
      document.getElementsByClassName(`navbar`)[0].classList.add("hidden");

      for (let form of forms)   {
        let   new_form_height = document.getElementById(forms[forms.length-1]).getElementById('dialog_div').getBoundingClientRect().top + document.getElementById(forms[forms.length-1]).getElementById('dialog_div').getBoundingClientRect().height + 50;
              document.getElementById().setAttribute("style",`height:${new_form_height}px`);
      
        console.log('new_form_height: ' + form + '   ' + new_form_height);
      }

    }else{
      document.getElementsByClassName(`navbar`)[0].classList.remove("hidden");
    }

   
 }



