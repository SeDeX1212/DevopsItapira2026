import pygame
import networkx as nx
import random
from collections import deque

pygame.init()

# Configurações
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Visualizador BFS e DFS")

font = pygame.font.SysFont("Arial", 22)
big_font = pygame.font.SysFont("Arial", 30)

clock = pygame.time.Clock()

# Cores
WHITE = (240, 240, 240)
BLACK = (30, 30, 30)
GREEN = (50, 220, 80)
YELLOW = (255, 200, 0)
RED = (220, 50, 50)
BLUE = (70, 120, 255)
GRAY = (120, 120, 120)

# ---------------------
# GERAÇÃO DO GRAFO
# ---------------------

NUM_NODES = 12

graph = nx.random_labeled_tree(NUM_NODES)

positions = nx.spring_layout(
    graph,
    seed=42,
    scale=250
)

for node in positions:
    positions[node] = (
        int(positions[node][0] + WIDTH // 2 - 150),
        int(positions[node][1] + HEIGHT // 2)
    )

# ---------------------
# ESTADO
# ---------------------

visited = set()
frontier = []
current = None

algorithm = None
running_search = False

queue = deque()
stack = []

step_timer = 0
STEP_DELAY = 800

start_node = 0

# ---------------------
# BUSCAS
# ---------------------

def start_bfs():

    global visited, frontier, current
    global queue, stack
    global running_search, algorithm

    visited = set()
    current = None

    queue = deque([start_node])
    frontier = list(queue)

    running_search = True
    algorithm = "BFS"


def start_dfs():

    global visited, frontier, current
    global queue, stack
    global running_search, algorithm

    visited = set()
    current = None

    stack = [start_node]
    frontier = list(stack)

    running_search = True
    algorithm = "DFS"


def bfs_step():

    global current, running_search, frontier

    if not queue:
        running_search = False
        return

    current = queue.popleft()

    if current not in visited:

        visited.add(current)

        for neighbor in graph.neighbors(current):

            if neighbor not in visited and neighbor not in queue:
                queue.append(neighbor)

    frontier = list(queue)


def dfs_step():

    global current, running_search, frontier

    if not stack:
        running_search = False
        return

    current = stack.pop()

    if current not in visited:

        visited.add(current)

        neighbors = list(graph.neighbors(current))
        neighbors.reverse()

        for neighbor in neighbors:

            if neighbor not in visited:
                stack.append(neighbor)

    frontier = list(stack)


# ---------------------
# DESENHO
# ---------------------

def draw_graph():

    # Arestas
    for edge in graph.edges():

        a = positions[edge[0]]
        b = positions[edge[1]]

        pygame.draw.line(screen, GRAY, a, b, 3)

    # Nós
    for node in graph.nodes():

        x, y = positions[node]

        color = WHITE

        if node in visited:
            color = GREEN

        if node in frontier:
            color = YELLOW

        if node == current:
            color = RED

        pygame.draw.circle(screen, color, (x, y), 30)
        pygame.draw.circle(screen, BLACK, (x, y), 30, 2)

        txt = font.render(str(node), True, BLACK)

        screen.blit(
            txt,
            txt.get_rect(center=(x, y))
        )


def draw_info():

    pygame.draw.rect(
        screen,
        (40, 40, 40),
        (900, 0, 300, HEIGHT)
    )

    title = big_font.render("CONTROLE", True, WHITE)
    screen.blit(title, (980, 20))

    text = font.render(
        "B = BFS | D = DFS | R = Novo Grafo",
        True,
        WHITE
    )

    screen.blit(text, (915, 80))

    algo = font.render(
        f"Algoritmo: {algorithm}",
        True,
        WHITE
    )

    screen.blit(algo, (930, 140))

    atual = font.render(
        f"Nó Atual: {current}",
        True,
        WHITE
    )

    screen.blit(atual, (930, 180))

    label = "Fila" if algorithm == "BFS" else "Pilha"

    estrutura = font.render(
        f"{label}:",
        True,
        WHITE
    )

    screen.blit(estrutura, (930, 250))

    y = 290

    for item in frontier:

        pygame.draw.rect(
            screen,
            BLUE,
            (940, y, 60, 40),
            border_radius=8
        )

        txt = font.render(
            str(item),
            True,
            WHITE
        )

        screen.blit(txt, (965, y + 8))

        y += 50


# ---------------------
# LOOP
# ---------------------

running = True

while running:

    dt = clock.tick(60)

    screen.fill((20, 20, 20))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_b:
                start_bfs()

            elif event.key == pygame.K_d:
                start_dfs()

            elif event.key == pygame.K_r:

                graph = nx.random_labeled_tree(NUM_NODES)

                positions = nx.spring_layout(
                    graph,
                    seed=random.randint(0, 9999),
                    scale=250
                )

                for node in positions:
                    positions[node] = (
                        int(positions[node][0] + WIDTH//2 - 150),
                        int(positions[node][1] + HEIGHT//2)
                    )

                visited.clear()
                frontier.clear()
                current = None
                running_search = False

    if running_search:

        step_timer += dt

        if step_timer >= STEP_DELAY:

            step_timer = 0

            if algorithm == "BFS":
                bfs_step()

            else:
                dfs_step()

    draw_graph()
    draw_info()

    pygame.display.flip()

pygame.quit()