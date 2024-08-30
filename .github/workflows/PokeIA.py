import numpy as np
from pyboy import PyBoy

# Inicializa o emulador com a ROM de Pokémon
rom_path = 'C:\\Users\\andre\\Desktop\\Python\\Projeto_PokeIA\\PokemonBlue.gb'
pyboy = PyBoy(rom_path, sound=True)

# Listas para armazenar os dados e eventos importantes
tile_matrices_bg = []
tile_matrices_win = []
sprites_info = []
exploration_points = []  # Armazena se uma nova área foi descoberta
explored_areas = []  # Lista para armazenar as áreas exploradas

# Endereços de memória para a experiência de cada Pokémon no inventário
pokemon_exp_addresses = [
    (0xD179, 0xD17B),  # Primeiro Pokémon
    (0xD1A5, 0xD1A7),  # Segundo Pokémon
    (0xD1D1, 0xD1D3),  # Terceiro Pokémon
    (0xD1FD, 0xD1FF),  # Quarto Pokémon
    (0xD229, 0xD22B),  # Quinto Pokémon
    (0xD255, 0xD257)   # Sexto Pokémon
]

# Funções auxiliares para avaliar o sucesso
def is_new_area(tile_matrix, explored_areas):
    return not np.any([np.array_equal(tile_matrix, area) for area in explored_areas])

# Função para verificar ganho de experiência para um Pokémon específico
def check_experience_gain(memory, address_range, previous_exp):
    exp_bytes = memory[address_range[0]:address_range[1]+1]  # XP é armazenado em 3 bytes
    current_exp = exp_bytes[0] + (exp_bytes[1] << 8) + (exp_bytes[2] << 16)
    
    exp_gain = current_exp - previous_exp
    return current_exp, exp_gain

# Inicializa valores
previous_exp = [0] * len(pokemon_exp_addresses)  # Lista para armazenar a experiência prévia de cada Pokémon
total_exp_gain = [0] * len(pokemon_exp_addresses)  # Lista para armazenar o ganho total de experiência
new_areas_count = 0  # Contador de novas áreas exploradas
total_score = 0  # Pontuação total

# Loop para capturar o estado do jogo e simular a interação automática
for i in range(5000):
    pyboy.button_press("A")
    pyboy.tick()
    pyboy.button_release("A")
    pyboy.tick()

    if i % 200 == 0:
        tilemap_bg = pyboy.tilemap_background
        tilemap_win = pyboy.tilemap_window

        tile_matrix_bg = tilemap_bg[0:32, 0:32]
        tile_matrix_win = tilemap_win[0:32, 0:32]

        sprites = [pyboy.get_sprite(idx) for idx in range(40) if pyboy.get_sprite(idx).on_screen]

        if is_new_area(tile_matrix_bg, explored_areas):
            exploration_points.append(1)
            explored_areas.append(tile_matrix_bg)
            new_areas_count += 1  # Incrementa o contador de novas áreas
            total_score += 1  # 1 ponto por nova área explorada
        else:
            exploration_points.append(0)

        tile_matrices_bg.append(tile_matrix_bg)
        tile_matrices_win.append(tile_matrix_win)
        sprites_info.append(sprites)

        memory = pyboy.memory
        for idx, (start_addr, end_addr) in enumerate(pokemon_exp_addresses):
            current_exp, exp_gain = check_experience_gain(memory, (start_addr, end_addr), previous_exp[idx])
            
            if exp_gain > 0:
                print(f"Pokémon {idx+1} ganhou {exp_gain} pontos de experiência!")
                total_exp_gain[idx] += exp_gain  # Adiciona ao total
                previous_exp[idx] = current_exp  # Atualiza para o próximo ciclo

# Calcula os pontos de experiência e adiciona à pontuação total
total_exp_points = sum(total_exp_gain) // 100000  # 1 ponto para cada 100.000 pontos de experiência
total_score += total_exp_points

# Imprime o total de experiência ganha por cada Pokémon
for idx, exp_gain in enumerate(total_exp_gain):
    print(f"Total de experiência ganha pelo Pokémon {idx+1}: {exp_gain}")

# Imprime o total de novas áreas exploradas
print(f"Total de novas áreas exploradas: {new_areas_count}")

# Imprime a pontuação total
print(f"Pontuação total: {total_score}")

# Salva os resultados
np.save('C:\\Users\\andre\\Desktop\\Python\\Projeto_PokeIA\\screenshots\\total_exp_gain.npy', np.array(total_exp_gain))  # Salva o total de experiência ganha
np.save('C:\\Users\\andre\\Desktop\\Python\\Projeto_PokeIA\\screenshots\\new_areas_count.npy', np.array(new_areas_count))  # Salva o total de novas áreas exploradas
np.save('C:\\Users\\andre\\Desktop\\Python\\Projeto_PokeIA\\screenshots\\total_score.npy', np.array(total_score))  # Salva a pontuação total

pyboy.stop()
