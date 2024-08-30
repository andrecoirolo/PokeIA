import numpy as np
import gym
from gym import spaces
from pyboy import PyBoy
from stable_baselines3 import DQN

# Definição do ambiente Pokémon Blue
class PokemonBlueEnv(gym.Env):
    def __init__(self):
        super(PokemonBlueEnv, self).__init__()
        self.rom_path = 'C:\\Users\\andre\\Desktop\\Python\\Projeto_PokeIA\\PokemonBlue.gb'
        self.pyboy = PyBoy(self.rom_path, sound=True)
        
        # Definir o espaço de ação e de observação
        self.action_space = spaces.Discrete(8)  # 8 ações possíveis: A, B, start, select, cima, baixo, esquerda, direita
        self.observation_space = spaces.Box(low=0, high=255, shape=(32, 32), dtype=np.uint8)  # Exemplo de espaço de observação

        # Inicializa o estado do ambiente
        self.previous_exp = [0] * 6  # Experiência inicial para cada Pokémon
        self.total_exp_gain = [0] * 6
        self.new_areas_count = 0
        self.explored_areas = []
        self.total_reward = 0  # Contador de recompensa total

    def step(self, action):
        # Define as ações possíveis
        actions = [
            "A", "B", "START", "SELECT", "UP", "DOWN", "LEFT", "RIGHT"
        ]
        
        # Executa a ação escolhida
        button = actions[action]
        self.pyboy.button_press(button)
        self.pyboy.tick()
        self.pyboy.button_release(button)
        self.pyboy.tick()

        # Captura o estado do jogo
        tilemap_bg = self.pyboy.tilemap_background
        tile_matrix_bg = tilemap_bg[0:32, 0:32]

        # Calcular recompensa baseada em exploração
        reward = 0
        if is_new_area(tile_matrix_bg, self.explored_areas):
            self.new_areas_count += 1
            self.explored_areas.append(tile_matrix_bg)
            reward += 1  # Recompensa para nova área explorada

        # Calcular recompensa baseada em experiência
        memory = self.pyboy.memory
        for idx, (start_addr, end_addr) in enumerate(pokemon_exp_addresses):
            current_exp, exp_gain = check_experience_gain(memory, (start_addr, end_addr), self.previous_exp[idx])
            self.total_exp_gain[idx] += exp_gain
            reward += exp_gain // 100000  # Recompensa para cada 100.000 de experiência
            self.previous_exp[idx] = current_exp

        # Adicionar a recompensa ao total acumulado
        self.total_reward += reward

        # Definir se o episódio terminou (pode definir uma condição de término específica)
        done = False

        # Converter o estado para um array NumPy antes de retornar
        state = np.array(tile_matrix_bg, dtype=np.uint8)

        # Retornar o estado atual, recompensa, done, e info
        return state, reward, done, {}

    def reset(self):
        # Reinicia o jogo e retorna o estado inicial
        self.pyboy.stop()
        self.pyboy = PyBoy(self.rom_path, sound=True)
        self.previous_exp = [0] * 6
        self.total_exp_gain = [0] * 6
        self.new_areas_count = 0
        self.explored_areas = []
        self.total_reward = 0  # Reinicia o contador de recompensas totais
        initial_state = np.zeros((32, 32), dtype=np.uint8)  # Estado inicial vazio
        return initial_state

    def render(self, mode='human'):
        pass  # Pode implementar para visualização, se necessário

    def close(self):
        self.pyboy.stop()

# Funções auxiliares para avaliação
def is_new_area(tile_matrix, explored_areas):
    return not np.any([np.array_equal(tile_matrix, area) for area in explored_areas])

def check_experience_gain(memory, address_range, previous_exp):
    exp_bytes = memory[address_range[0]:address_range[1]+1]  # XP é armazenado em 3 bytes
    current_exp = exp_bytes[0] + (exp_bytes[1] << 8) + (exp_bytes[2] << 16)
    exp_gain = current_exp - previous_exp
    return current_exp, exp_gain

# Endereços de memória para a experiência de cada Pokémon no inventário
pokemon_exp_addresses = [
    (0xD179, 0xD17B),  # Primeiro Pokémon
    (0xD1A5, 0xD1A7),  # Segundo Pokémon
    (0xD1D1, 0xD1D3),  # Terceiro Pokémon
    (0xD1FD, 0xD1FF),  # Quarto Pokémon
    (0xD229, 0xD22B),  # Quinto Pokémon
    (0xD255, 0xD257)   # Sexto Pokémon
]

# Inicializa o ambiente
env = PokemonBlueEnv()
obs = env.reset()

# Treinamento com DQN
model = DQN('MlpPolicy', env, verbose=1)

# Treinar o modelo
model.learn(total_timesteps=10000)

# Salvar o modelo treinado
model.save("pokemon_blue_dqn_model")

# Carregar o modelo e testar
model = DQN.load("pokemon_blue_dqn_model")
obs = env.reset()

# Variável para armazenar o total de recompensas ao longo das runs
total_rewards = []

for _ in range(10):  # Execute 10 runs para ver o desempenho
    obs = env.reset()
    total_episode_reward = 0
    for _ in range(1000):
        action, _states = model.predict(obs)
        obs, reward, done, info = env.step(action)
        total_episode_reward += reward
        env.render()  # Pode implementar para ver o progresso, se necessário
        if done:
            break
    total_rewards.append(total_episode_reward)
    print(f"Total de recompensas nesta run: {total_episode_reward}")

# Imprime o total de recompensas de cada run
print(f"Recompensas de todas as runs: {total_rewards}")
print(f"Média de recompensas: {np.mean(total_rewards)}")
