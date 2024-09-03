import numpy as np
import gym
from gym import spaces
from pyboy import PyBoy
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

# Configuração para habilitar/desabilitar a interface gráfica
enable_gui = True  # Altere para False para desativar a interface gráfica

# Caminho para a ROM de Pokémon Blue
rom_path = 'C:\\Users\\andre\\Desktop\\Python\\Projeto_PokeIA\\PokemonBlue.gb'

# Caminho para o arquivo de log
log_file_path = 'C:\\Users\\andre\\Desktop\\Python\\Projeto_PokeIA\\output_log.txt'

# Abrir o arquivo de log
log_file = open(log_file_path, 'w')

# Função personalizada para imprimir no terminal e no arquivo de log
def print_and_log(message, log_file):
    print(message)
    log_file.write(message + "\n")
    log_file.flush()

# Função para capturar o estado do jogo
def get_game_state(pyboy, reward_total):
    memory = pyboy.memory  # Acessar a memória diretamente

    # Criar um array de estado com os valores de interesse, incluindo recompensa total
    state = np.array([
        memory[0xD16D],  # player_hp
        memory[0xD023],  # player_max_hp
        memory[0xCFE7],  # enemy_hp
        memory[0xD057],  # battle_state
        memory[0xD362],  # x_coord
        memory[0xD361],  # y_coord
        memory[0xD35E],  # map_id
        memory[0xD356],  # badge_count
        reward_total     # incluir recompensa total no estado observado
    ], dtype=np.uint8)
    
    return state

# Classe para gerenciar recompensas
class RewardSystem:
    def __init__(self, env_id):
        self.visited_locations = set()  # Armazena as áreas já visitadas
        self.reward_total = 0
        self.env_id = env_id  # Identificador do ambiente

    def calculate_reward(self, current_state):
        reward = 0

        # Recompensa de Exploração
        location = (current_state[6], current_state[4], current_state[5])  # (map_id, x_coord, y_coord)
        if location not in self.visited_locations:
            reward += 10  # Atribuir uma recompensa ao encontrar uma nova área
            self.visited_locations.add(location)

        # Atualizar o total de recompensa acumulada
        previous_total = self.reward_total
        self.reward_total += reward

        # Checagem de diminuição inesperada
        if self.reward_total < previous_total:
            print_and_log(f"Erro: Recompensa total diminuiu no Ambiente {self.env_id}! Recompensa Total Anterior: {previous_total}, Nova Recompensa Total: {self.reward_total}", log_file)

        if reward != 0:
            # Mostrar o estado atual e a recompensa
            print_and_log(f"Ambiente {self.env_id} - Estado Atual: {current_state}, Recompensa: {reward}, Recompensa Total: {self.reward_total}", log_file)

        return reward

# Classe de ambiente customizado do Gym
class PokemonEnv(gym.Env):
    def __init__(self, env_id):
        super(PokemonEnv, self).__init__()

        # Define o tipo de janela com base em enable_gui
        self.pyboy = PyBoy(rom_path, window="headless", sound=False)
        self.pyboy.set_emulation_speed(40)

        # Define o espaço de ação e observação
        self.action_space = spaces.Discrete(8)  # 8 ações disponíveis agora
        self.observation_space = spaces.Box(low=0, high=255, shape=(9,), dtype=np.uint8)  # Inclui recompensa total

        # Inicializa o sistema de recompensa com um ID de ambiente
        self.reward_system = RewardSystem(env_id)

        # Inicializa o contador de ticks
        self.tick_count = 0
        self.max_ticks = 30000  # Define o número máximo de ticks

    def step(self, action):
        # Mapeia a ação para os controles do jogo
        self._take_action(action)

        # Avança o estado do jogo
        self.pyboy.tick()
        self.tick_count += 1

        # Obtém o estado do jogo, incluindo a recompensa total
        state = get_game_state(self.pyboy, self.reward_system.reward_total)

        # Calcula a recompensa
        reward = self.reward_system.calculate_reward(state)

        # Define a condição de fim como o número máximo de ticks
        done = self.tick_count >= self.max_ticks

        # Retorna o estado, recompensa, done, e info
        return state, reward, done, {}

    def reset(self):
        self.pyboy.stop()
        self.pyboy = PyBoy(rom_path, window="SDL2", sound=False)
        self.pyboy.set_emulation_speed(40)
        self.tick_count = 0  # Resetar contador de ticks
        initial_state = get_game_state(self.pyboy, self.reward_system.reward_total)
        return initial_state

    def _take_action(self, action):
        # Define as ações possíveis
        actions = ["A", "B", "START", "SELECT", "UP", "DOWN", "LEFT", "RIGHT"]

        # Executa a ação escolhida
        button = actions[action]
        self.pyboy.button_press(button)
        self.pyboy.tick()
        self.pyboy.button_release(button)
        self.pyboy.tick()

    def close(self):
        self.pyboy.stop()

# Função para criar o ambiente com ID
def make_env(env_id):
    def _init():
        return PokemonEnv(env_id)
    return _init

# Criação de múltiplas instâncias do ambiente usando DummyVecEnv
num_envs = 4  # Número de instâncias paralelas
envs = DummyVecEnv([make_env(i) for i in range(num_envs)])

# Criação do modelo de AR usando PPO
model = PPO("MlpPolicy", envs, verbose=1)

# Treinamento do modelo
model.learn(total_timesteps=100000)  # Ajuste o número de timesteps conforme necessário

# Salvando o modelo treinado
model.save("C:\\Users\\andre\\Desktop\\Python\\Projeto_PokeIA\\ppo_pokemon_parallel")

# Fechar o ambiente após o treinamento
envs.close()

# Carregar o modelo treinado para teste
model = PPO.load("C:\\Users\\andre\\Desktop\\Python\\Projeto_PokeIA\\ppo_pokemon_parallel")

# Testar com as instâncias paralelas
obs = envs.reset()

# Loop para testar o agente
for _ in range(1000):
    action, _states = model.predict(obs)
    obs, rewards, dones, infos = envs.step(action)
    if any(dones):
        print_and_log("Jogo terminado em uma das instâncias.", log_file)
        break

# Fecha o arquivo de log
log_file.close()
