
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
async function openModal() {
    document.getElementById('mform').classList.remove("hidden");

    await FillOutModalForm();
  };


async function asyncRequest (uri, method, data, debug=false){
    let response_promise = await fetch(uri, {method: method, headers: { 'Content-Type': 'application/json;charset=utf-8' }, body: JSON.stringify(data) } )
    console.log('Response:')
    console.log(response_promise);
    return response_promise.json();
}

async function FillOutModalForm(){
    let answer = await asyncRequest(`/test_dialog`, `POST`, {});
    console.log('FillOutModalForm')
    console.log(answer);
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