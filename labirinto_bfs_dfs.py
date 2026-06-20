import pygame
import random
from collections import deque

# ==========================
# CONFIGURAÇÕES
# ==========================

LARGURA = 1400
ALTURA = 800

COLUNAS = 35
LINHAS = 25
TAMANHO = 28

PAINEL_X = COLUNAS * TAMANHO + 20

FPS = 60
DELAY = 100  # menor = mais rápido

# ==========================
# CORES
# ==========================

FUNDO = (25, 25, 25)
PAREDE = (50, 50, 50)
LIVRE = (220, 220, 220)

VISITADO = (100, 220, 100)
FRONTEIRA = (255, 220, 0)

ATUAL = (255, 80, 80)

INICIO = (50, 150, 255)
OBJETIVO = (180, 0, 255)

GRADE = (150, 150, 150)

# ==========================
# PYGAME
# ==========================

pygame.init()

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Visualizador BFS x DFS")

clock = pygame.time.Clock()

fonte = pygame.font.SysFont("consolas", 22)
fonte_grande = pygame.font.SysFont("consolas", 30)

# ==========================
# LABIRINTO
# ==========================


def gerar_labirinto():

    maze = []

    for y in range(LINHAS):

        linha = []

        for x in range(COLUNAS):

            if random.random() < 0.28:
                linha.append(1)
            else:
                linha.append(0)

        maze.append(linha)

    maze[0][0] = 0
    maze[LINHAS - 1][COLUNAS - 1] = 0

    return maze


maze = gerar_labirinto()

inicio = (0, 0)
objetivo = (COLUNAS - 1, LINHAS - 1)

# ==========================
# ESTADO DA BUSCA
# ==========================

visitados = set()

fronteira = []

pais = {}

algoritmo = None
rodando = False

fila = deque()
pilha = []

atual = None

caminho_final = []

ultimo_passo = 0


# ==========================
# FUNÇÕES DE BUSCA
# ==========================

def resetar_busca():

    global visitados
    global fronteira
    global pais
    global atual
    global caminho_final

    visitados = set()
    fronteira = []
    pais = {}
    atual = None
    caminho_final = []


def iniciar_bfs():

    global fila
    global algoritmo
    global rodando
    global fronteira

    resetar_busca()

    fila = deque([inicio])

    fronteira = list(fila)

    algoritmo = "BFS"
    rodando = True


def iniciar_dfs():

    global pilha
    global algoritmo
    global rodando
    global fronteira

    resetar_busca()

    pilha = [inicio]

    fronteira = list(pilha)

    algoritmo = "DFS"
    rodando = True


def reconstruir_caminho():

    global caminho_final

    caminho_final = []

    atual_local = objetivo

    while atual_local in pais:

        caminho_final.append(atual_local)
        atual_local = pais[atual_local]

    caminho_final.append(inicio)


def vizinhos(pos):

    x, y = pos

    movimentos = [
        (0, -1),
        (0, 1),
        (-1, 0),
        (1, 0)
    ]

    resultado = []

    for dx, dy in movimentos:

        nx = x + dx
        ny = y + dy

        if (
            0 <= nx < COLUNAS
            and 0 <= ny < LINHAS
            and maze[ny][nx] == 0
        ):
            resultado.append((nx, ny))

    return resultado


def passo_bfs():

    global atual
    global rodando
    global fronteira

    if not fila:
        rodando = False
        return

    atual = fila.popleft()

    if atual == objetivo:

        reconstruir_caminho()
        rodando = False
        return

    if atual not in visitados:

        visitados.add(atual)

        for v in vizinhos(atual):

            if v not in visitados and v not in fila:

                pais[v] = atual
                fila.append(v)

    fronteira = list(fila)


def passo_dfs():

    global atual
    global rodando
    global fronteira

    if not pilha:
        rodando = False
        return

    atual = pilha.pop()

    if atual == objetivo:

        reconstruir_caminho()
        rodando = False
        return

    if atual not in visitados:

        visitados.add(atual)

        for v in reversed(vizinhos(atual)):

            if v not in visitados:

                pais[v] = atual
                pilha.append(v)

    fronteira = list(pilha)


# ==========================
# DESENHO
# ==========================

def desenhar_labirinto():

    for y in range(LINHAS):

        for x in range(COLUNAS):

            rect = pygame.Rect(
                x * TAMANHO,
                y * TAMANHO,
                TAMANHO,
                TAMANHO
            )

            cor = LIVRE

            if maze[y][x] == 1:
                cor = PAREDE

            if (x, y) in visitados:
                cor = VISITADO

            if (x, y) in fronteira:
                cor = FRONTEIRA

            if (x, y) in caminho_final:
                cor = (0, 255, 255)

            if (x, y) == inicio:
                cor = INICIO

            if (x, y) == objetivo:
                cor = OBJETIVO

            if (x, y) == atual:
                cor = ATUAL

            pygame.draw.rect(tela, cor, rect)
            pygame.draw.rect(tela, GRADE, rect, 1)


def desenhar_painel():

    pygame.draw.rect(
        tela,
        (35, 35, 35),
        (PAINEL_X, 0, 300, ALTURA)
    )

    y = 20

    titulo = fonte_grande.render(
        "BFS / DFS",
        True,
        (255, 255, 255)
    )

    tela.blit(titulo, (PAINEL_X + 50, y))

    y += 70

    textos = [
        "B - Executar BFS",
        "D - Executar DFS",
        "R - Novo Labirinto",
        "",
        f"Algoritmo: {algoritmo}",
        f"Visitados: {len(visitados)}",
        f"Fronteira: {len(fronteira)}",
        "",
        "Legenda:",
        "Azul = Inicio",
        "Roxo = Objetivo",
        "Amarelo = Fronteira",
        "Verde = Visitado",
        "Vermelho = Atual",
        "Ciano = Caminho"
    ]

    for texto in textos:

        render = fonte.render(
            texto,
            True,
            (255, 255, 255)
        )

        tela.blit(render, (PAINEL_X + 20, y))
        y += 35


# ==========================
# LOOP
# ==========================

executando = True

while executando:

    dt = clock.tick(FPS)

    tela.fill(FUNDO)

    agora = pygame.time.get_ticks()

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            executando = False

        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_b:
                iniciar_bfs()

            elif evento.key == pygame.K_d:
                iniciar_dfs()

            elif evento.key == pygame.K_r:

                maze = gerar_labirinto()

                resetar_busca()

                algoritmo = None
                rodando = False

    if rodando:

        if agora - ultimo_passo > DELAY:

            ultimo_passo = agora

            if algoritmo == "BFS":
                passo_bfs()

            elif algoritmo == "DFS":
                passo_dfs()

    desenhar_labirinto()
    desenhar_painel()

    pygame.display.flip()

pygame.quit()