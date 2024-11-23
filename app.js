const inputbox = document.getElementById("input-box");
const lista = document.getElementById("lista");

function addTarefa(){
    
if(inputbox.value === '') {
    alert ("Adicione uma Tarefa")
} else {
    let li = document.createElement("li");
    li.innerHTML = inputbox.value;
    lista.appendChild(li);
    let button = document.createElement("button");
    button.innerHTML = "<i class='bx bxs-trash bx-tada'></i>";
    li.appendChild(button);
}
    inputbox.value = "";
    salvar();
}

lista.addEventListener("click", function(e) {
    if (e.target.tagName == "LI") {
        e.target.classlist.toggle("escolhido");
        salvar();

    } else if (e.target.tagName == "BUTTON"){
        e.target.parentElement.remove();
        salvar();
    }

}, false);

function salvar(){
    localStorage.setItem("data", lista.innerHTML);
}
function showTask(){
    lista.innerHTML = localStorage.getItem("data");
}
showTask();