import numpy as np
from pyboy import PyBoy
import sys

# Caminho para o arquivo de log
log_file_path = 'C:\\Users\\andre\\Desktop\\Python\\Projeto_PokeIA\\output_log.txt'

# Abrir o arquivo de log
log_file = open(log_file_path, 'w')

# Caminho para a ROM de Pokémon Blue
rom_path = 'C:\\Users\\andre\\Desktop\\Python\\Projeto_PokeIA\\PokemonBlue.gb'

# Inicializa o emulador PyBoy
pyboy = PyBoy(rom_path, sound=False)
pyboy.set_emulation_speed(1)  # Definindo velocidade normal para inspeção manual

# Classe para gerenciar recompensas
class RewardSystem:
    def __init__(self):
        self.visited_locations = set()
        self.reward_total = 0
        self.previous_badge_count = 0
        self.previous_total_experience = 0

    def calculate_reward(self, current_state):
        reward = 0

        # Verificar se o número de insígnias aumentou
        current_badge_count = current_state['badge_count']
        if current_badge_count > self.previous_badge_count:
            reward += 1000
            self.previous_badge_count = current_badge_count

        # Verificar se a experiência total aumentou
        current_total_experience = current_state['total_experience']
        current_battle_state = current_state['battle_state']
        if current_total_experience > self.previous_total_experience:
            if current_battle_state == 2:
                reward += 250  # Recompensa por aumentar experiência em batalha normal
            elif current_battle_state == 1:
                reward += 20  # Recompensa por aumentar experiência em batalha menor
            self.previous_total_experience = current_total_experience

        # Movimentação para novas coordenadas
        location = (current_state['map_id'], current_state['x_coord'], current_state['y_coord'])
        if location not in self.visited_locations:
            reward += 1
            self.visited_locations.add(location)

        self.reward_total += reward
        return reward

# Função para capturar o estado do jogo
def get_game_state(pyboy):
    memory = pyboy.memory

    # Calcular experiência total
    experience_addresses = [
        (0xD179, 0xD17A, 0xD17B),  # Pokémon 1
        (0xD1A5, 0xD1A6, 0xD1A7),  # Pokémon 2
        (0xD1D1, 0xD1D2, 0xD1D3),  # Pokémon 3
        (0xD1FD, 0xD1FE, 0xD1FF),  # Pokémon 4
        (0xD229, 0xD22A, 0xD22B),  # Pokémon 5
        (0xD255, 0xD256, 0xD257)   # Pokémon 6
    ]
    total_experience = 0
    for addr1, addr2, addr3 in experience_addresses:
        total_experience += (memory[addr1] << 16) + (memory[addr2] << 8) + memory[addr3]

    state = {
        'player_hp': memory[0xD16D],
        'player_max_hp': memory[0xD023],
        'enemy_hp': memory[0xCFE7],
        'battle_state': memory[0xD057],
        'x_coord': memory[0xD362],
        'y_coord': memory[0xD361],
        'map_id': memory[0xD35E],
        'badge_count': memory[0xD356],
        'total_experience': total_experience  # Soma da experiência de todos os Pokémon
    }
    return state

# Função personalizada para imprimir no terminal e no arquivo de log
def print_and_log(message, log_file):
    print(message)
    log_file.write(message + "\n")
    log_file.flush()

# Inicializa o sistema de recompensa
reward_system = RewardSystem()

# Loop principal para rodar o jogo e capturar estados
for _ in range(300000):
    pyboy.tick()  # Atualiza o estado do emulador
    current_state = get_game_state(pyboy)  # Captura o estado atual do jogo
    reward = reward_system.calculate_reward(current_state)  # Calcula a recompensa atual
    reward_total = reward_system.reward_total  # Obtém o total acumulado de recompensa
    if reward != 0:
        print_and_log(f"Estado do jogo: {current_state}, Recompensa Atual: {reward}, Recompensa Total: {reward_total}", log_file)

# Fecha o emulador e o arquivo de log
pyboy.stop()
log_file.close()
