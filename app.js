document.addEventListener('DOMContentLoaded', () => {
    
    document.querySelectorAll('.box').forEach((box) => {
        inicializarBox(box);
    });
});

function inicializarBox(box) {
    const addTarefaBtn = box.querySelector('.addTarefaBtn');
    const inputBoxTarefas = box.querySelector('.inputBoxTarefas');
    const lista = box.querySelector('.lista');

    
    function carregarTarefas() {
        const boxId = box.dataset.id;  
        if (!boxId) {
            console.error('Box não encontrada ou não tem dataset.id');
            return;
        }

        fetch(`http://127.0.0.1:8000/tarefas/${boxId}`)
            .then(response => response.json())
            .then(tarefas => {
                console.log(tarefas);  
                lista.innerHTML = '';  
                if (Array.isArray(tarefas)) {
                    tarefas.forEach(tarefa => {
                        criarTarefa(tarefa.nome_tarefa, tarefa.status_tarefa, tarefa.idtarefas_api);
                    });
                } else {
                    console.error('Formato inválido de resposta:', tarefas);
                }
            })
            .catch(error => console.error('Erro ao carregar tarefas:', error));
    }

    
    carregarTarefas();

    
    function criarTarefa(tarefaNome, feito = false, idTarefa = null) {
        let li = document.createElement('li');
        li.classList.add('tarefaItem');
        if (feito) li.classList.add('feito');
        if (idTarefa) li.dataset.id = idTarefa;

        let iconeFeito = document.createElement('img');
        iconeFeito.src = feito ? 'imagens/cheio.png' : 'imagens/vazio.png';
        iconeFeito.alt = 'Marcar como feito';
        iconeFeito.classList.add('iconeFeito');

        
        iconeFeito.addEventListener('click', () => {
            const novoStatus = li.classList.contains('feito') ? 0 : 1;  
        
            
            li.classList.toggle('feito');
            iconeFeito.src = novoStatus === 1 ? 'imagens/cheio.png' : 'imagens/vazio.png';
        
            
            fetch(`http://127.0.0.1:8000/tarefas/${li.dataset.id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    nome_tarefa: li.querySelector('.textoTarefa').innerText.trim(),  
                    status_tarefa: novoStatus,  
                    box_id: box.dataset.id  
                })
            })
            .then(response => response.json())
            .then(() => {
                console.log('Tarefa atualizada no servidor.');
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

    
    function addTarefa() {
        let tarefaNome = inputBoxTarefas.value.trim(); 
        if (tarefaNome === '') return; 

        const boxId = box.dataset.id; 

        
        fetch('http://127.0.0.1:8000/tarefas', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                nome_tarefa: tarefaNome, 
                status_tarefa: 0, 
                box_id: boxId  
            })
        })
        .then(response => response.json())  
        .then(tarefa => {
            
            criarTarefa(tarefa.nome_tarefa, false, tarefa.idtarefas_api);
            inputBoxTarefas.value = ''; 
        })
        .catch(error => console.error('Erro ao adicionar tarefa:', error));
    }

    
    function editarTarefa(li, textoTarefa) {
        let inputEdicao = document.createElement('input');
        inputEdicao.type = 'text';
        inputEdicao.value = textoTarefa.innerText;
        inputEdicao.classList.add('inputEdicao');

        li.replaceChild(inputEdicao, textoTarefa);

        inputEdicao.addEventListener('blur', () => {
            textoTarefa.innerText = inputEdicao.value.trim();
            li.replaceChild(textoTarefa, inputEdicao);
            atualizarTarefa(li.dataset.id, textoTarefa.innerText.trim());
        });

        inputEdicao.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                textoTarefa.innerText = inputEdicao.value.trim();
                li.replaceChild(textoTarefa, inputEdicao);
                atualizarTarefa(li.dataset.id, textoTarefa.innerText.trim());
            }
        });

        inputEdicao.focus();
    }

    
    function atualizarTarefa(idTarefa, novoNome) {
        
        const tarefa = {
            id: idTarefa,
            nome_tarefa: novoNome,
            status_tarefa: 0, 
            box_id: box.dataset.id 
        };

        fetch(`http://127.0.0.1:8000/tarefas/${tarefa.id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                nome_tarefa: tarefa.nome_tarefa,
                status_tarefa: tarefa.status_tarefa,
                box_id: tarefa.box_id 
            })
        })
        .then(response => response.json())
        .then(() => {
            console.log('Tarefa atualizada com sucesso!');
        })
        .catch(error => console.error('Erro ao atualizar tarefa:', error));
    }

    
    addTarefaBtn.addEventListener('click', addTarefa);

    inputBoxTarefas.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addTarefa();
        }
    });
}
