# 🎹 Runaway - Finger Piano (Modular HUD Edition)

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-green?style=flat-square&logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand_Tracking-orange?style=flat-square)
![Pygame](https://img.shields.io/badge/Pygame-Audio_Engine-yellow?style=flat-square)

Um piano virtual tocado no ar através de visão computacional! Este projeto permite que você toque a introdução de **"Runaway" do Kanye West** utilizando apenas os movimentos dos seus dedos em frente à webcam.


---

## 🏗️ Arquitetura do Projeto

O sistema monolítico foi dividido em componentes especialistas para facilitar a leitura e escalabilidade:

```text
📦 runaway-finger-piano
 ┣ 📜 main.py       # Entry-point: Orquestra o loop principal do vídeo e do jogo.
 ┣ 📜 config.py     # Central de configurações: Frequências, cores, constantes e layout.
 ┣ 📜 vision.py     # Inteligência Artificial: Download do modelo e tracking da mão (MediaPipe).
 ┣ 📜 audio.py      # Motor de Som: Geração matemática das ondas e integração com Pygame.
 ┣ 📜 ui.py         # Renderização: Desenho de HUDs dinâmicos, osciloscópio e botões com OpenCV.
 ┣ 📜 requirements.txt
 ┗ 📜 .gitignore
