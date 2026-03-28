 # 🐦 Flappy Bird com IA (NEAT + Pygame)

Este projeto é uma implementação do clássico **Flappy Bird** em Python utilizando **Pygame**, com suporte a **Inteligência Artificial baseada em NEAT (NeuroEvolution of Augmenting Topologies)**.

O jogo permite dois modos:

* 🎮 **Modo Jogador** — controle manual
* 🤖 **Modo IA** — evolução automática do pássaro

Além disso, o projeto apresenta duas abordagens diferentes de implementação:

* Uma versão mais direta e funcional (`flap_menu.py`)
* Uma versão mais estruturada e organizada (`flap_gemini.py`)

---

## 📂 Arquivos do Projeto

* `flap_menu.py`
  Versão funcional do jogo com:

  * Menu inicial
  * Suporte a modo jogador e IA
  * Estrutura mais direta (procedural + classes)

* `flap_gemini.py`
  Versão mais avançada e organizada:

  * Arquitetura orientada a objetos
  * Separação clara de responsabilidades
  * Melhor organização de configuração e assets
  * Código mais limpo e escalável

---

## ⚙️ Tecnologias Utilizadas

* Python 3.x
* Pygame
* neat-python

---

## 📦 Instalação

Instale as dependências com:

```bash
pip install pygame neat-python
```

---

## ▶️ Como Executar

### 🔹 Rodar versão com menu simples

```bash
python flap_menu.py
```

### 🔹 Rodar versão estruturada (recomendada)

```bash
python flap_gemini.py
```

---

## 🎮 Modos de Jogo

Ao iniciar, você poderá escolher:

* **Modo Jogador**

  * Controle com tecla `ESPAÇO`
* **Modo IA**

  * A IA aprende sozinha usando NEAT
  * Evolui ao longo das gerações

---

## 🧠 Inteligência Artificial (NEAT)

A IA utiliza:

* Redes neurais evolutivas
* Fitness baseado em:

  * Tempo de sobrevivência
  * Pontuação (passar pelos canos)
* Inputs da rede:

  * Altura do pássaro
  * Distância para o topo do cano
  * Distância para a base do cano

---

## 🧩 Estrutura do Código

### 🔹 Entidades principais

* **Passaro**

  * Movimento
  * Física (gravidade, pulo)
  * Animação

* **Cano**

  * Geração aleatória
  * Movimento lateral
  * Colisão

* **Chao**

  * Scroll infinito

---

### 🔹 flap_menu.py

* Estrutura mais simples
* Loop principal direto
* Funções principais:

  * `menu()` → seleção de modo
  * `main()` → loop do jogo
  * `rodar()` → execução do NEAT

---

### 🔹 flap_gemini.py

* Arquitetura mais robusta baseada em classe:

#### 🧱 Classe principal: `FlappyEngine`

Responsável por:

* Inicialização do jogo
* Gerenciamento de estado
* Renderização
* Controle da IA

#### 🔧 Componentes:

* `menu_inicial()` → interface inicial
* `main()` → loop do jogo
* `treinar_ai()` → treinamento com NEAT

#### ⚙️ Config centralizada:

```python
CONFIG = {
    "TELA": {...},
    "CORES": {...},
    "FISICA": {...},
    "ASSETS": "Saved Pictures"
}
```

---

## 🖼️ Assets

As imagens devem estar na pasta:

```bash
Saved Pictures/
```

Arquivos necessários:

* `bg.png`
* `base.png`
* `pipe.png`
* `bird1.png`
* `bird2.png`
* `bird3.png`

---

## 📈 Diferenças entre as versões

| Característica | flap_menu.py | flap_gemini.py      |
| -------------- | ------------ | ------------------- |
| Organização    | Simples      | Avançada            |
| Arquitetura    | Procedural   | Orientada a objetos |
| Escalabilidade | Baixa        | Alta                |
| Legibilidade   | Média        | Alta                |
| Manutenção     | Difícil      | Fácil               |

---

## 🚀 Possíveis melhorias

* Salvar e carregar modelos treinados
* Melhorar UI/UX do menu
* Adicionar efeitos sonoros
* Implementar sistema de ranking
* Ajustar hiperparâmetros do NEAT
* Exportar o melhor agente treinado

---

## 👨‍💻 Objetivo do Projeto

Este projeto foi desenvolvido com foco em:

* Aprender **Pygame**
* Explorar **IA evolutiva (NEAT)**
* Comparar diferentes arquiteturas de código
* Evoluir de um código simples para um mais profissional

---

## 📌 Observações

* O desempenho da IA melhora com o tempo (gerações)
* O treinamento pode ser demorado dependendo da máquina
* Certifique-se de que o arquivo `config.txt` do NEAT está presente

---

## 🏁 Conclusão

Este projeto demonstra na prática:

* Desenvolvimento de jogos com Python
* Aplicação de IA em tempo real
* Evolução de código de nível iniciante para avançado

---

💡 **Dica:** Use o `flap_gemini.py` como base para projetos maiores — ele já segue um padrão mais profissional.
