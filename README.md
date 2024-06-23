
# Projeto Flappy Bird com IA
Este repositório contém um projeto do jogo Flappy Bird desenvolvido em Python utilizando a biblioteca Pygame. O projeto inclui uma implementação de inteligência artificial (IA) com a biblioteca NEAT (NeuroEvolution of Augmenting Topologies) para treinar o pássaro a jogar o jogo autonomamente.

## Arquivos do Projeto
- `dfg.py`: teste do codigo e outras ideias
- `flap_menu.py`: test de implementa o menu inicial do jogo, onde o jogador pode iniciar o jogo, ver pontuações e outras opções.
- `flap_t.py`: codigo original do jogo.
- `novo_flap.py`: Este é o arquivo principal do jogo. Contém a implementação do Flappy Bird com suporte a IA.
## Dependências
Para executar este projeto, você precisará ter o Python instalado em sua máquina, além das seguintes bibliotecas:

- `pygame`: Para a interface gráfica do jogo.
- `neat-python´: Para a implementação da IA.
Você pode instalar essas bibliotecas utilizando o pip:

```bash
pip install pygame neat-python
```
## Como Executar
1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```
2.Execute o jogo:
Você pode iniciar o jogo com a IA configurada para jogar sozinha ou desativar a IA para jogar manualmente. Para isso, ajuste a variável ai_jogando no início do arquivo novo_flap.py:

```python
ai_jogando = False  # Altere para True para ativar a IA
```
Para iniciar o jogo, execute o arquivo `novo_flap.py`:

```bash
python novo_flap.py
```
## Estrutura do Código
### novo_flap.py
- Importações e Inicialização: Configurações iniciais e carregamento de imagens.
- Classes:
  - Passaro: Implementa a lógica e animação do pássaro.
  - Cano: Lógica dos canos, incluindo movimentação e detecção de colisões.
  - Chao: Implementa o chão do jogo, responsável pela rolagem infinita.
- Funções:
  - desenhar_tela: Desenha todos os elementos na tela.
  - main: Função principal que controla o loop do jogo, lida com eventos e atualiza o estado do jogo.
  - rodar: Configura e inicia a evolução da IA utilizando NEAT.
`dfg.py`, `flap_menu.py`, `flap_t.py`
Estes arquivos contém o mesmo código de maneiras diferentes ou outras ideias


