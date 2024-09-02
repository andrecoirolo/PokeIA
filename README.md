Agora que os passos básicos do projeto já foram implementados (rodar emulação e construção de um sistema de armazenamento da informação, precisamos decidir qual sistema de incremento 





- Algoritmos Genéticos e Seleção Natural
   
  Uma das abordagens que usa a ideia de selecionar as melhores execuções para continuar rodando é baseada em algoritmos genéticos, que simulam processos de evolução natural:

    População Inicial: Um grupo inicial de agentes (soluções) é gerado de forma aleatória.
    Avaliação: Cada agente executa a tarefa, e uma pontuação ou fitness é atribuída com base no desempenho.
    Seleção: Os melhores agentes (com maior pontuação) são selecionados para passar seus "genes" para a próxima geração.
    Crossover: Combina características de dois ou mais agentes selecionados para criar novos agentes.
    Mutação: Pequenas alterações aleatórias são introduzidas em alguns agentes para garantir diversidade e evitar mínimos locais.
    Iteração: Esse processo é repetido por muitas gerações, com cada nova geração sendo composta por agentes melhores (teoricamente) que a anterior.

- Passos para Implementar Algoritmos Genéticos e Seleção Natural:
  
  Passo 1: Definir os Parâmetros de Sucesso (Critérios de Avaliação)
  Antes de mais nada, precisamos definir claramente o que significa "sucesso" no contexto do jogo Pokémon Blue. Esses parâmetros serão usados para avaliar o desempenho de cada agente. Aqui estão algumas sugestões:
  
    Exploração de Novas Áreas: O agente recebe pontos quando descobre novas áreas no jogo.
    Subida de Experiência: O agente recebe pontos por pontos experiência ganha por cada um dos seus 6 Pokémons.
    # Tempo de Sobrevivência: O tempo que o agente sobrevive sem ser derrotado pode ser um indicador de um bom desempenho.
    # Derrotar Ginasios: A cada ginasio derrotado o agente recebe mais pontos.
    # Derrotar Elite 4: A cada membro da Elite 4 derrotado ganha mais pontos.
  
  Passo 2: Implementar a Extração de Dados para Avaliar o Desempenho
Para avaliar o desempenho de cada agente, precisamos capturar e armazenar dados relevantes durante as execuções do jogo.

  Passo 3: Implementar o Algoritmo Genético
    Vamos criar um sistema para simular a evolução. Os agentes que obtêm as maiores pontuações em termos de critérios de sucesso serão selecionados para "reproduzir" a próxima geração. A reprodução pode incluir "cruzamento" de estratégias e "mutações" para introduzir variações.
    
    Estrutura do Algoritmo Genético
    Inicialização da População: Crie uma população inicial de agentes com diferentes estratégias. No início, você pode começar com estratégias aleatórias.
    
    Avaliação da População: Cada agente é executado no ambiente, e sua pontuação é calculada com base nos critérios definidos.
    
    Seleção: Selecionar os melhores agentes com base nas pontuações.
    
    Reprodução (Crossover e Mutação): Use as melhores estratégias para criar novos agentes. Combine aspectos de diferentes agentes (crossover) e faça pequenas alterações aleatórias (mutação).
    
    Iteração: Repita o processo para várias gerações.









Próximas melhorias:

Medir e Rankear as Runs: Atribuir pontuações a cada execução com base no desempenho (como número de novas áreas exploradas, níveis ganhos, batalhas vencidas).

Selecionar as Melhores Runs: Escolher as top X runs com base na pontuação.

Treinar Novos Agentes com Base nos Melhores: Usar os parâmetros dos melhores agentes para inicializar novos agentes, potencialmente introduzindo pequenas mutações ou variações para explorar o espaço de soluções.

Repetir: Continuar o ciclo de execução, avaliação, seleção, e treino.

Executar Múltiplas Runs: Treinar o agente várias vezes, cada run usando um conjunto inicial de parâmetros diferentes (ou simplesmente começando do zero).

Gravação e Reprodução: O projeto suportar gravação e reprodução de partidas, útil para testar e avaliar o desempenho da IA.


Bibliografia:

Para encotrar os slots de memória para cada item do jogo:
https://datacrystal.tcrf.net/wiki/Pokémon_Red_and_Blue/RAM_map#Joypad_simulation
