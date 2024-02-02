
const closeModal = function () {
    document.getElementById('mform').classList.add("hidden");
};

// close modal when the Esc key is pressed
document.addEventListener("keydown", function (e) {
  if (e.key === "Escape" && !document.getElementById('mform').classList.contains("hidden")) {
    closeModal();
  }
});

// open modal function
async function openModal(uri_for_get_JSON) {
    document.getElementById('mform').classList.remove("hidden");
    await FillOutModalForm(uri_for_get_JSON);
  };


async function asyncRequest (uri, method, data, debug=false){
    let response_promise = await fetch(uri, {method: method, headers: { 'Content-Type': 'application/json;charset=utf-8' }, body: JSON.stringify(data) } )
    console.log('Response:')
    console.log(response_promise);
    return response_promise.json();
}

async function FillOutModalForm(uri_for_get_JSON){
    const str_card_begin = `<div class="card text-secondary-emphasis bg-secondary-subtle border border-secondary-subtle rounded-3" style="padding: 1em;">`;
    const str_card_end = `</div>`;



    let answer = await asyncRequest(uri_for_get_JSON, `POST`, {});
    console.log('FillOutModalForm')
    console.log(answer);
    var source = answer;
    const rootNode = document.getElementById('mform');
    rootNode.innerHTML = "";
    if (source.title!=null){
      rootNode.insertAdjacentHTML(`beforeend`,`<h1 class="p-3 text-primary-emphasis bg-primary-subtle border border-primary-subtle rounded-3">${source.title}</h1><hr><hr>`);
    }
    if (source.parameters!=null){
      for (let section of source.parameters){
        console.log(section);
  
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
    let organization_id = document.getElementById(`row_id`).dataset.row_id;
    console.log('organization_id:'+organization_id);
  
    let answer = await asyncRequest(`/get_organization_data/${organization_id}`, `POST`, {});
    
    console.log(answer);
  
    document.getElementById("Краткое название").value = answer.org_short_name;
    document.getElementById("Полное название").value = answer.org_name;
  
  }

/*

{
  let answer = await asyncRequest(`${APIServer}/get_syllable_full_data/`, `POST`, {command:``, comment:``, data:`${document.body.dataset.word}`});
  console.log(answer)
  document.body.dataset.syllable_id = answer.syllable_id;
  document.getElementById(`id_transcription`).value = answer.transcription
  document.getElementById(`id_translations`).value = answer.translations
  for (var example of answer.examples) {
                                        AddExamplToNewSyllablePage(document.getElementById(`id_examples`), example.example, example.translate, example.rowid, getRandomInt(1000000000000, 9999999999999));
                                      }
*/