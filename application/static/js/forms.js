var forms_zindex=50;
// arrays of modal form IDs
var forms = [];

var returnedModalFormJSON = {};

var periods = [ '2022-09',
                '2022-10',
                '2022-11',
                '2022-12',
                '2023-01',
                '2023-02',
                '2023-03',
                '2023-04',
                '2023-05',
                '2023-06',
                '2023-07',
                '2023-08',
                '2023-09',
                '2023-10',
                '2023-11'
              ];

const closeModal = function () {
    document.getElementById('mform').classList.add("hidden");
    document.getElementById('mdiv').classList.add("hidden");
};

var border_colors = ["border-primary", "border-secondary", "border-success", "border-danger", "border-warning", "border-info", "border-dark"];


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
    
    let answer = await asyncRequest(uri_for_get_JSON, `POST`, {});
    var source = answer;

    await FillOutModalForm(source);
  };


async function asyncRequest (uri, method, data, debug=false){
    let response_promise = await fetch(uri, {method: method, headers: { 'Content-Type': 'application/json;charset=utf-8' }, body: JSON.stringify(data) } )
    return response_promise.json();
}

async function FillOutModalForm(source){
    console.log(JSON.stringify(source));
    

    const str_card_begin = `<div class="card text-secondary-emphasis bg-secondary-subtle border border-secondary-subtle rounded-3" style="padding: 1em;">`;
    const str_card_end = `</div>`;

    const rootNode = document.getElementById(source.backlink.length>0?'mform':'mdiv');

    rootNode.classList.remove("hidden");
    rootNode.innerHTML = "";
    if (source.title!=null){
      rootNode.insertAdjacentHTML(`beforeend`,`<h1 class="p-3 text-primary-emphasis bg-primary-subtle border border-primary-subtle rounded-3">${source.title}</h1><hr><hr>`);
    }
    if (source.parameters!=null){
      let counter = 0;
      for (let section of source.parameters){
          if (section.type==`edit`){
          rootNode.insertAdjacentHTML(`beforeend`,`${str_card_begin}<div class="row"><div class="col-4"><label for="${section.name}">${section.lable} </label></div><div class="col-8"><input class="container-fluid" autocomplete="off" type="text" name="${section.name}" id="${section.name}" value ="${section.default}"></div>${str_card_end}</div><br>` );
          if (counter == 0){
            $(`#${section.name}`).focus();
          }
          counter++;
        } //edit
  
        if (section.type==`date`){
          rootNode.insertAdjacentHTML(`beforeend`,`${str_card_begin}<div class="row"><div class="col-4"><label for="${section.name}">${section.lable} </label></div><div class="col-8"><input class="container-fluid" autocomplete="off" type="date" name="${section.name}" id="${section.name}" value ="${section.default}"></div>${str_card_end}</div><br>` );
          if (counter == 0){
            $(`#${section.name}`).focus();
          }
          counter++;
        } //edit
  
        if (section.type==`checkbox`){
          rootNode.insertAdjacentHTML(`beforeend`,`${str_card_begin}<div class="row"><div class="col-4"><label for="${section.name}">${section.lable}</label></div><div class="col-8"><input autocomplete="off" type="checkbox" name="${section.name}" id="${section.name}" ${Number(section.default)==1?"checked":""}></div>${str_card_end}</div><br>`);
          if (counter == 0){
            $(`#${section.name}`).focus();
          }
          counter++;
        } //checkbox
  
        if (section.type==`text`){
          rootNode.insertAdjacentHTML(`beforeend`, `${str_card_begin}<div class="row"><div class="col-4"><label for="${section.name}">${section.lable} </label></div><div class="col-8"><textarea ${(Number(section.size)>0?'rows="'+section.size+'"':'')} class="container-fluid" autocomplete="off" name="${section.name}" id="${section.name}" >${section.default}</textarea></div>${str_card_end}</div><br>`
          );
          if (counter == 0){
            $(`#${section.name}`).focus();
          }
          counter++;
        } //textarea
      if (section.type==`listbox`){
        counter++;
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
    rootNode.insertAdjacentHTML(`beforeend`,`<hr><hr><br><div class="container"> <div class="row"><div class="col-sm-8"><button ${(source.backlink.length>0)?'type="submit"':''} class="btn btn-primary btn-lg btn-block col-6" id="button_modal_dialog_ok">&nbsp&nbsp&nbsp&nbspОк&nbsp&nbsp&nbsp&nbsp</button></div><div class="col-sm-4"><button type="button" class="btn btn-secondary btn-lg btn-block col-12" onclick='closeModal();' id="button_modal_dialog_escape">Отмена</button></div></div>`);
    const ok_button = document.getElementById('button_modal_dialog_ok');
    if (source.success_jscode.length>0){
      console.log(`jscode`);
        ok_button.onclick = function() { eval(source.success_jscode); };
    }
    
    const escape_button = document.getElementById('button_modal_dialog_escape');
    if (source.escape_jscode.length>0){
      console.log(`escape`);
      escape_button.onclick = function() { eval(source.escape_jscode); };
    }

    if (source.backlink.length>0){
      console.log(`backlink`  );
      rootNode.action = source.backlink;
      rootNode.method = 'POST';}
}


  //  function read intered parameters an sent them on the server
  function Ok(source){
    console.log('Ok function:')
    source = JSON.parse(source);
    var result = [];
    var foo = {};
    if (source.parameters!=null){
    for (let section of source.parameters){
      if (section.type==`edit`){
          foo[`${section.name}`]=`${document.getElementById(section.name).value}`;
        }//if (section.type==`edit`)
        if (section.type==`date`){
          foo[`${section.name}`]=`${document.getElementById(section.name).value}`;
        }//if (section.type==`edit`)

      if (section.type==`text`){
          foo[`${section.name}`]=`${document.getElementById(section.name).value}`;
        }//if (section.type==`text`)
      if (section.type==`checkbox`){
          foo[`${section.name}`]=`${document.getElementById(section.name).checked}`;
        }//if (section.type==`checkbox`)
       if (section.type==`listbox`){
          foo[`${section.name}`]=`${document.getElementById(section.name).value}`;
          result.push(foo);
        }//if (section.type==`listbox`)
      }//for (let section of source.parameters)
    }//if (source.parameters!=null)
    return foo;
  }//function


  async function FillOutOrganizationForm() {
    console.log(`FillOutOrganizationForm`);
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
   document.querySelector(`#${form_id}`).remove();
  }

  function CloseToplevelDynamicForm(){
    if (forms.length>0){
      CloseInScreenForm(forms[forms.length - 1]);
      forms.pop();
    }
  }


function onClickToAgreementCalcPeriod(element, agreement_id) {
  console.log(`onClickToAgreementCalcPeriod`);
  console.log(agreement_id);
  $(`#AgreementPeriodsDropDownList`).text ( `расчётный период:  ` + element.text );
  Load_Data_Into_Agreement_Calc_View(agreement_id, element.text);
}

function Load_Data_Into_Agreement_Calc_View(agreement_id, period){
  console.log(agreement_id, period);
  document.getElementById(`agreeemnt_calc_data`).innerHTML=``;
  let xhr = new XMLHttpRequest();
  xhr.open(`GET`, `/agreement_form_part_calc_table/${agreement_id}/${period}`);
  xhr.send();
  xhr.onload = function() {
    document.getElementById(`agreeemnt_calc_data`).insertAdjacentHTML(`afterBegin`, xhr.responseText);
  }
}

function Fill_Agreement_Periods_DropDownList(){
  console.log(`Fill_Agreement_Periods_DropDownList`);
  if (typeof(document.querySelector(`#AgreementPeriodsDropDownListDropMenu`))=='object'){
    document.querySelector(`#AgreementPeriodsDropDownListDropMenu`).innerHTML=``;
    for (let period of periods){
      $(`#AgreementPeriodsDropDownList`).text ( `расчётный период:  ` + period );
      $(`#AgreementPeriodsDropDownListDropMenu`).append(`<li><a class="dropdown-item" href="#" onclick="onClickToAgreementCalcPeriod(this,${document.querySelector(`#AgreementPeriodsDropDownListDropMenu`).dataset.agreementid})">${period}</a></li>`);
    }
  }

}

// run in screen form, fill and show
  function RunInScreenForm (form_name, execute_after_load, request_link) {
    let outerRootElement = document.getElementsByTagName(`body`)[0];
    form_name = form_name + `_${getRandomInt(999999999999999)}`
    forms_zindex++;
    console.log(forms_zindex);
    outerRootElement.insertAdjacentHTML(
      `beforeEnd`,
      `<div id="${form_name}" class="dynamic-form container-fluid border-5 ${border_colors[forms_zindex%9]}" data-zindex="${forms_zindex}"></div>`);

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
              <button id="${forms[forms.length-1]}_dialog_escape_button" type="button" class="btn btn-secondary btn-lg btn-block col-12" onclick="CloseToplevelDynamicForm();">
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
      

 }

}


 let timerId = setInterval(() => TimerProcceed(), 50);
function TimerProcceed(){
    nodes = document.getElementsByClassName(`dynamic-form`);
    if (nodes.length>0){
      for (let form of forms)   {
        let   new_form_height = Math.floor($(`#${forms[forms.length-1]}`).children('#dialog_div').height()) + 220; //Math.floor(document.querySelector(`#${forms[forms.length-1]}`).getBoundingClientRect().top) 
              document.querySelector(`#${forms[forms.length-1]}`).setAttribute("style",`height:${new_form_height}px`);
      }
    }
    else{
    }

   
 }


var Get_Agreements_Search_Result_request_int_progress = 0
 async function Get_Agreements_Search_Result(lc_value){
  if (Get_Agreements_Search_Result_request_int_progress==0){
    if (lc_value.length>3){
            Get_Agreements_Search_Result_request_int_progress = 1
            let response = await fetch('/get_agremments_search_result', {
                                                                    method: 'POST',
                                                                    headers: {
                                                                      'Content-Type': 'application/json;charset=utf-8'
                                                                    },
                                                                    body: JSON.stringify({ search_substring:lc_value
                                                                                          })
                                                                                        }
                                                                    );
              let answer = await response.text();
              $(`#div_for_substitustion_of_search_results`).empty();
              $(`#div_for_substitustion_of_search_results`).append(answer);
              Get_Agreements_Search_Result_request_int_progress = 0
    }
  else $(`#div_for_substitustion_of_search_results`).empty();
  }
}    



function AddMessageIntoLog(message){
	var messageLog = document.getElementById('messageLog');
	if (!document.querySelector(`#message_id_${message.id}`)){
		let str = ``;
		let message_id = `message_id_${message.id}`;
		str += `<div id="${message_id}">`;
		str += `<span class="message_log_datetime">${message.dt.slice(6,25)}</span> `;
		str += (message.link==null? '': `<a href='${message.link}'>`);
		let icon = (message.icon==null,null,(message.icon.includes(`/`)? message.icon: eval(`icons.${message.icon}`)));
		str += (message.icon==null? '' : `<img src="${icon}" width="32" height="32">`);
		str += (message.text==null? '' : `<span ${(message.style==null,'',`class="${message.style}"`)}>&nbsp;&nbsp;&nbsp;${message.text}</span>`)
		str += (message.link==null? '': `</a>`);
		str += '</div>';
		console.log(messageLog.dataset.firstinit);
		if (messageLog.dataset.firstinit!=='true'){
			showPopupMessage(str);
		}
		messageLog.insertAdjacentHTML(`afterbegin`,str);
		document.querySelector(`#${message_id}`).style.animation = 'blink 1s infinite';
		setTimeout(() => {
			document.querySelector(`#${message_id}`).style.animation = '';
		}, 5000); // Stop blinking after 5 seconds
 	}
	 
}



// Функция для обновления журнала сообщений
function updateMessageLog() {
	if (!document.getElementById('messageLog')){ 
		return
	}
	var xhr = new XMLHttpRequest();
	xhr.open('POST', '/message_log', true);
	xhr.onreadystatechange = function() {
		if (xhr.readyState === XMLHttpRequest.DONE) {
			if (xhr.status === 200) {
				var data = JSON.parse(xhr.responseText);
				data.forEach(function(message) {
					AddMessageIntoLog(message);
				});
				document.getElementById('messageLog').dataset.firstinit='false';
			} else{
				clearInterval(messages_timer);
				AddMessageIntoLog({id:-1, link:null, icon:`error`, text:`Ошибка получения данных сервера - обновление журнала приостановлено`})
			}
		}
		
	};
	xhr.send();
}

var icons={	error:`/static/images/error_icon.png`,
			excel:`/static/images/excel_icon.png`,
			info:`/static/images/info_icon.png`,
			table:`/static/images/table_icon.png`};


var messages_timer = setInterval(updateMessageLog, 2000);
updateMessageLog()

function ToggleMessageLogUpDown(change){
	let button = document.querySelector('#message_log_toggle_button');
	let button_fullscreen = document.querySelector('#message_log_toggle_fullscreen_button');
	let log = document.querySelector('#messageLog');
	if (button.dataset.state=='up'){
		button.dataset.state='down';
		button.src='/static/images/arrows_up.png';
		log.style.maxHeight = '0px';
		log.style.height = '0px';
		log.dataset.state= 'down';
		button_fullscreen.style.display = 'none';
	}
	else
	{
		button.dataset.state='up';
		button.src='/static/images/arrows_down.png';
		log.style.maxHeight = '200px';
		log.style.height = '200px';
		log.dataset.state= 'up';
		button_fullscreen.style.display = 'block';
	}
}
function ToggleMessageLogFullscreen(){
	let button = document.querySelector('#message_log_toggle_fullscreen_button');
	let button_updown = document.querySelector('#message_log_toggle_button');
	let log = document.querySelector('#messageLog');
	if (button.dataset.state=='normal'){
		button.dataset.state='fullscreen';
		button.src='/static/images/unfullscreen.png';
		log.style.maxHeight = '100%';
		log.style.height = '100%';
		log.dataset.state= 'fullscreen';
		log.style.zIndex = 999999999999;
		button.style.zIndex = log.style.zIndex + 1;
		button_updown.style.display='none';
	}
	else
	{
		button.dataset.state='normal';
		button.src='/static/images/fullscreen.png';
		log.style.maxHeight = (button_updown.dataset.state=='up'?'200px':'0px');
		log.style.height = (button_updown.dataset.state=='up'?'200px':'0px');
		log.dataset.state= (button_updown.dataset.state=='up'?'up':'down');
		button_updown.style.display='block';
		button.style.zIndex = log.style.zIndex - 1;
		log.style.zIndex = -101;
	}
}




function showPopupMessage(text) {
    // Создаем элемент для всплывающего блока
    const popup = document.createElement('div');
    popup.innerHTML = text;
    popup.style.position = 'fixed';
    popup.style.top = '20px';
    popup.style.right = '20px';
	popup.style.width = 'auto';
    popup.style.padding = '10px';
    popup.style.background = 'rgba(0, 0, 0, 0.7)';
    popup.style.color = '#fff';
    popup.style.borderRadius = '5px';
    popup.style.transition = 'opacity 0.5s';
    document.body.appendChild(popup);

    // Задаем начальную прозрачность блока
    popup.style.opacity = '1';

    // Устанавливаем таймер для исчезновения блока через 10 секунд
    setTimeout(() => {
        // Постепенно уменьшаем прозрачность до 0
        let opacity = 1;
        const interval = setInterval(() => {
            opacity -= 0.1;
            popup.style.opacity = opacity;
            // Когда достигнута нулевая прозрачность, удаляем блок и останавливаем интервал
            if (opacity <= 0) {
                clearInterval(interval);
                document.body.removeChild(popup);
            }
        }, 500); // Каждые 500 миллисекунд (0.5 секунды) изменяем прозрачность
    }, 10000); // Через 10 секунд блок исчезнет
}

