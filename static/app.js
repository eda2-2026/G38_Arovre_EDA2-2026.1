document.addEventListener('DOMContentLoaded', () => {
    const tbody = document.getElementById('ranking-tbody');
    const form = document.getElementById('add-player-form');
    const selectCriterio = document.getElementById('criterio');
    const feedback = document.getElementById('form-feedback');
    const statusContainer = document.getElementById('status-container');
    const btnBuscar = document.getElementById('btn-buscar');
    const btnLimparBusca = document.getElementById('btn-limpar-busca');
    const inputBusca = document.getElementById('busca-nome');

    async function fetchRanking(searchName = '') {
        const criterio = selectCriterio.value;
        let url = `/api/ranking?criterio=${criterio}`;
        
        try {
            const response = await fetch(url);
            const result = await response.json();
            let players = result.ranking;
            
            if (searchName) {
                players = players.filter(p => p.nome.toLowerCase().includes(searchName.toLowerCase()));
                statusContainer.innerHTML = `<div style="color: var(--primary-color)">Resultados da busca por: "${searchName}"</div>`;
                btnLimparBusca.style.display = 'block';
            } else {
                statusContainer.innerHTML = `
                    <div style="color: var(--primary-color)">Ranking atualizado por ${criterio.replace('_', ' ')}</div>
                `;
                btnLimparBusca.style.display = 'none';
            }
            
            renderTable(players);
        } catch (error) {
            console.error('Erro ao buscar ranking:', error);
            showFeedback('Erro ao carregar o ranking.', 'error');
        }
    }

    function renderTable(players) {
        tbody.innerHTML = '';
        
        if (players.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align: center;">Nenhum jogador encontrado.</td></tr>';
            return;
        }

        players.forEach((player, index) => {
            const tr = document.createElement('tr');
            
            tr.innerHTML = `
                <td><span class="pos-badge">${index + 1}º</span></td>
                <td><strong>${player.nome}</strong></td>
                <td>${player.gols}</td>
                <td>${player.assistencias}</td>
                <td>${player.minutos_jogados}min</td>
                <td>
                    <button class="btn-delete btn-danger" data-id="${player.id}" style="padding: 0.25rem 0.5rem; font-size: 0.85rem; width: auto;">
                        Remover
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });

        // Adicionar eventos aos botões de remoção
        document.querySelectorAll('.btn-delete').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const id = e.target.getAttribute('data-id');
                if (confirm('Deseja realmente remover este jogador?')) {
                    await deletePlayer(id);
                }
            });
        });
    }

    async function deletePlayer(id) {
        try {
            const response = await fetch(`/api/players/${id}`, {
                method: 'DELETE'
            });
            if (response.ok) {
                fetchRanking(inputBusca.value.trim());
            } else {
                const data = await response.json();
                alert(`Erro: ${data.detail}`);
            }
        } catch (error) {
            console.error('Erro:', error);
            alert('Erro na comunicação com o servidor.');
        }
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const btnSubmit = form.querySelector('button[type="submit"]');
        const nome = document.getElementById('nome').value.trim();
        const gols = parseInt(document.getElementById('gols').value);
        const assistencias = parseInt(document.getElementById('assistencias').value);
        const minutos = parseInt(document.getElementById('minutos').value);

        if (!nome) {
            showFeedback("Adicione um nome!", 'error');
            return;
        }

        btnSubmit.disabled = true;
        btnSubmit.textContent = 'Adicionando...';

        const id = Date.now().toString();

        try {
            const response = await fetch('/api/players', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    id, 
                    nome, 
                    gols, 
                    assistencias, 
                    minutos_jogados: minutos 
                })
            });

            const data = await response.json();

            if (response.ok) {
                showFeedback(data.message, 'success');
                form.reset();
                fetchRanking(); 
            } else {
                showFeedback(data.detail, 'error');
            }
        } catch (error) {
            console.error('Erro ao adicionar jogador:', error);
            showFeedback('Erro de conexão com o servidor.', 'error');
        } finally {
            btnSubmit.disabled = false;
            btnSubmit.textContent = 'Adicionar ao Ranking';
        }
    });

    selectCriterio.addEventListener('change', () => fetchRanking(inputBusca.value.trim()));

    btnBuscar.addEventListener('click', () => {
        fetchRanking(inputBusca.value.trim());
    });

    inputBusca.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            fetchRanking(inputBusca.value.trim());
        }
    });

    btnLimparBusca.addEventListener('click', () => {
        inputBusca.value = '';
        fetchRanking();
    });

    function showFeedback(mensagem, tipo) {
        feedback.textContent = mensagem;
        feedback.className = `feedback ${tipo}`;
        setTimeout(() => {
            feedback.textContent = '';
            feedback.className = 'feedback';
        }, 4000);
    }

    // Carregamento inicial
    fetchRanking();
});
