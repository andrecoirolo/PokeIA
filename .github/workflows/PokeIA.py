import numpy as np
import pandas as pd
from pyboy import PyBoy

# Inicializa o emulador com a ROM de Pokémon
rom_path = 'C:\\Users\\andre\\Desktop\\Python\\Projeto_PokeIA\\PokemonBlue.gb'
pyboy = PyBoy(rom_path, sound=True)

# Listas para armazenar os dados
tile_matrices_bg = []
tile_matrices_win = []
sprites_info = []

# Loop para capturar o estado do jogo e simular a interação automática
for i in range(1000):
    pyboy.button_press("A")  # Pressiona o botão A
    pyboy.tick()  # Avança um frame do emulador
    pyboy.button_release("A")  # Solta o botão A
    pyboy.tick()  # Avança um frame do emulador

    # A cada 500 iterações, capturamos o estado do jogo
    if i % 500 == 0:
        # Acessa o objeto TileMap para o background e janela
        tilemap_bg = pyboy.tilemap_background
        tilemap_win = pyboy.tilemap_window

        # Captura a matriz completa do mapa de tiles do background e janela
        tile_matrix_bg = tilemap_bg[0:32, 0:32]
        tile_matrix_win = tilemap_win[0:32, 0:32]

        # Captura informações dos sprites
        sprites = [pyboy.get_sprite(idx) for idx in range(40) if pyboy.get_sprite(idx).on_screen]

        # Adiciona os dados às listas
        tile_matrices_bg.append(tile_matrix_bg)
        tile_matrices_win.append(tile_matrix_win)
        sprites_info.append(sprites)

# Converte listas para arrays NumPy e salva
np.save('C:\\Users\\andre\\Desktop\\Python\\Projeto_PokeIA\\screenshots\\tile_matrices_bg.npy', np.array(tile_matrices_bg))
np.save('C:\\Users\\andre\\Desktop\\Python\\Projeto_PokeIA\\screenshots\\tile_matrices_win.npy', np.array(tile_matrices_win))
np.save('C:\\Users\\andre\\Desktop\\Python\\Projeto_PokeIA\\screenshots\\sprites_info.npy', np.array(sprites_info, dtype=object))

# Fecha o emulador
pyboy.stop()
