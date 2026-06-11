# Organizador de Pelada - Ranking com Árvore AVL

## 1. Visão Geral
Esta aplicação é a continuação do "Organizador de Pelada", agora implementando a estrutura de dados **Árvore AVL**. O objetivo é demonstrar a eficiência da AVL (balanceamento dinâmico e buscas/inserções em tempo O(log N)) no contexto de um Leaderboard/Ranking de jogadores.

## 2. Arquitetura
- **Backend:** Python com FastAPI. 
- **Frontend:** HTML, CSS e Vanilla JavaScript.
- **Armazenamento:** Os dados persistentes virão de um arquivo JSON (ou gerador de dados em memória) contendo os jogadores. A Árvore AVL residirá inteiramente na memória RAM do servidor FastAPI, sendo reconstruída sob demanda.

## 3. Estruturas de Dados

### 3.1. Modelo do Jogador
Cada jogador possuirá as seguintes propriedades:
- `id` (string ou int)
- `nome` (string)
- `gols` (int)
- `assistencias` (int)
- `minutos_jogados` (int)

### 3.2. Árvore AVL
A Árvore AVL será a estrutura central para a ordenação e exibição do ranking.
- **Chave do Nó (`key`):** Será definida dinamicamente. Pode ser o número de gols, o número de assistências ou o tempo em quadra. 
- **Valor do Nó (`value`):** Uma lista de `Jogadores`. Como vários jogadores podem ter a mesma quantidade de gols (chaves duplicadas), agruparemos todos eles no mesmo nó.
- **Propriedade de Balanceamento (`altura`):** Cada nó rastreia sua altura para calcular o Fator de Balanceamento e executar as rotações (LL, RR, LR, RL) quando necessário.

## 4. Fluxo de Dados e Funcionalidades

### 4.1. Construção Dinâmica da Árvore
O usuário no frontend poderá escolher o critério do ranking via um seletor (Dropdown/Select): "Gols", "Assistências" ou "Minutos Jogados".
Ao alterar a seleção, o Frontend fará uma requisição para a API. O Backend então:
1. Destruirá a instância atual da árvore.
2. Iterará sobre todos os jogadores carregados e fará a inserção (O(log N)) de cada um na nova AVL, utilizando o critério escolhido como chave.
3. Retornará o sucesso da operação.

### 4.2. Geração do Ranking (Percurso)
Para exibir o ranking na tela, o Frontend solicitará os dados processados da árvore.
O Backend realizará um **Percurso In-Order Reverso** (Visita a subárvore Direita, visita a Raiz, visita a subárvore Esquerda). Isso garante que as chaves de maior valor (ex: jogadores com mais gols) apareçam primeiro no JSON de resposta. O frontend pegará essa lista plana já ordenada para popular a tabela.

### 4.3. Manipulação de Dados
O sistema permitirá:
- **Inserir novo jogador:** O jogador é adicionado à lista base e também inserido na AVL atual. Se a chave não existir, cria-se um nó; se existir, faz-se o append na lista de valores do nó. A inserção acionará o balanceamento, se aplicável.
- **Atualizar estatísticas:** Se um jogador tiver sua pontuação alterada, ele será removido da AVL, terá o dado atualizado, e será reinserido para manter a propriedade e o balanceamento.
- **Remover jogador:** O jogador será buscado na AVL e removido. Caso o nó fique vazio (era o único jogador com aquela pontuação), o nó inteiro é deletado, o que pode engatilhar uma rotação de balanceamento.

## 5. Visualização de Eventos
Embora não haja renderização gráfica da árvore na UI padrão, as rotações (Left-Left, Right-Right, etc.) serão logadas no console do servidor ou enviadas como notificações para o frontend para fins didáticos.

## 6. Testes e Validação
- Os testes deverão certificar que, após uma carga de 2500 jogadores e manipulação de pontuações, a propriedade da AVL (Fator de balanceamento entre -1, 0, 1) é rigorosamente mantida em todos os nós.
- Deve-se confirmar que o In-Order reverso realmente retorna os dados em ordem estritamente decrescente em todos os cenários de chaves de ordenação.
