// Função para carregar as tarefas assim que a página é carregada
document.addEventListener('DOMContentLoaded', () => {
    fetch('http://127.0.0.1:8000/tarefas')
        .then(response => response.json())
        .then(tarefas => {
            tarefas.forEach(tarefa => {
                // Aqui, você popula a tarefa em uma box específica
                adicionarTarefaNaBox(tarefa.nome_tarefa, tarefa.idtarefas_api, tarefa.status_tarefa);
            });
        })
        .catch(error => console.error('Erro ao carregar tarefas:', error));
});

// Função para adicionar tarefa na box específica
function adicionarTarefaNaBox(nome, id, status) {
    const box = document.querySelector(`.box[data-id="${id}"]`); // Seleciona a box com o id correto
    const tarefaElement = box.querySelector('.task'); // Encontra o elemento que deve exibir o nome da tarefa
    tarefaElement.textContent = nome; // Atualiza o nome da tarefa na box
}

function inicializarBox(box) {
    const addTarefaBtn = box.querySelector('.addTarefaBtn');
    const inputBoxTarefas = box.querySelector('.inputBoxTarefas');
    const lista = box.querySelector('.lista');

    // Função para carregar tarefas do servidor
    function carregarTarefas() {
        fetch('http://127.0.0.1:8000/tarefas')
            .then(response => response.json())
            .then(tarefas => {
                tarefas.forEach(tarefa => {
                    criarTarefa(tarefa.nome_tarefa, tarefa.status_tarefa === 1, tarefa.idtarefas_api);
                });
            })
            .catch(error => console.error('Erro ao carregar tarefas:', error));
    }

    // Criar elemento de tarefa na lista
    function criarTarefa(tarefaNome, feito = false, idTarefa = null) {
        let li = document.createElement('li');
        li.classList.add('tarefaItem');
        if (feito) li.classList.add('feito');
        if (idTarefa) li.dataset.id = idTarefa;

        let iconeFeito = document.createElement('img');
        iconeFeito.src = feito ? 'imagens/cheio.png' : 'imagens/vazio.png';
        iconeFeito.alt = 'Marcar como feito';
        iconeFeito.classList.add('iconeFeito');

        // Alternar status da tarefa (feito/pendente)
        iconeFeito.addEventListener('click', () => {
            let novoStatus = li.classList.contains('feito') ? 0 : 1;

            fetch(`http://127.0.0.1:8000/tarefas/${li.dataset.id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    nome_tarefa: li.querySelector('.textoTarefa').innerText.trim(),  // Enviar o nome da tarefa
                    status_tarefa: novoStatus  // Enviar o novo status
                })
            })
            .then(response => response.json())
            .then(() => {
                li.classList.toggle('feito');
                iconeFeito.src = novoStatus === 1 ? 'imagens/cheio.png' : 'imagens/vazio.png';
            })
            .catch(error => console.error('Erro ao atualizar a tarefa:', error));
        });

        let textoTarefa = document.createElement('span');
        textoTarefa.classList.add('textoTarefa');
        textoTarefa.innerText = tarefaNome;

        let btnEditar = document.createElement('button');
        btnEditar.classList.add('btnAcao');
        btnEditar.innerHTML = '<i class="bx bxs-pencil"></i>';
        btnEditar.addEventListener('click', () => {
            editarTarefa(li, textoTarefa);
        });

        let btnDeletar = document.createElement('button');
        btnDeletar.classList.add('btnAcao');
        btnDeletar.innerHTML = '<i class="bx bxs-trash bx-tada"></i>';
        btnDeletar.addEventListener('click', () => {
            // Corrigir URL do DELETE:
            fetch(`http://127.0.0.1:8000/tarefas/${li.dataset.id}`, { method: 'DELETE' })
                .then(() => {
                    li.remove();
                })
                .catch(error => console.error('Erro ao excluir tarefa:', error));
        });

        li.prepend(iconeFeito);
        li.appendChild(textoTarefa);
        li.appendChild(btnEditar);
        li.appendChild(btnDeletar);

        lista.appendChild(li);
    }

    // Adicionar nova tarefa
    function addTarefa() {
        let tarefaNome = inputBoxTarefas.value.trim();
        if (tarefaNome === '') return;

        fetch('http://127.0.0.1:8000/tarefas', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome_tarefa: tarefaNome, status_tarefa: 0 })
        })
        .then(response => response.json())
        .then(tarefa => {
            criarTarefa(tarefa.nome_tarefa, false, tarefa.idtarefas_api);
            inputBoxTarefas.value = '';
        })
        .catch(error => console.error('Erro ao adicionar tarefa:', error));
    }

    // Editar tarefa
    function editarTarefa(li, textoTarefa) {
        let inputEdicao = document.createElement('input');
        inputEdicao.type = 'text';
        inputEdicao.value = textoTarefa.innerText;
        inputEdicao.classList.add('inputEdicao');

        // Substituir o texto com o input de edição
        li.replaceChild(inputEdicao, textoTarefa);

        inputEdicao.addEventListener('blur', () => {
            // Verificar se o li ainda existe
            if (li) {
                textoTarefa.innerText = inputEdicao.value.trim();
                li.replaceChild(textoTarefa, inputEdicao);
                atualizarTarefa(li.dataset.id, textoTarefa.innerText.trim());
            }
        });

        inputEdicao.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                // Verificar se o li ainda existe
                if (li) {
                    textoTarefa.innerText = inputEdicao.value.trim();
                    li.replaceChild(textoTarefa, inputEdicao);
                    atualizarTarefa(li.dataset.id, textoTarefa.innerText.trim());
                }
            }
        });

        inputEdicao.focus();
    }

    // Atualizar tarefa no servidor
    function atualizarTarefa(idTarefa, novoNome) {
        fetch(`http://127.0.0.1:8000/tarefas/${idTarefa}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome_tarefa: novoNome, status_tarefa: 0 })
        })
        .then(response => response.json())
        .catch(error => console.error('Erro ao atualizar tarefa:', error));
    }

    // Eventos para adicionar tarefas
    addTarefaBtn.addEventListener('click', addTarefa);

    inputBoxTarefas.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addTarefa();
        }
    });

    carregarTarefas();  // Carregar as tarefas quando a caixa é inicializada
}

// Inicializar todas as caixas
document.querySelectorAll('.box').forEach((box) => {
    inicializarBox(box);
});

