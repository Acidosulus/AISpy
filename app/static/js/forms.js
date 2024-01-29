
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
function openModal() {
    document.getElementById('mform').classList.remove("hidden");
  };


function FillOutModalForm(){
    
}