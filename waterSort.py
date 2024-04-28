# import modules
import pygame
import random
import copy

# initialize pygame
pygame.init()

# setup game variables
WIDTH = 500
HEIGHT = 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Water Sort Puzzle Game!')

fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 24)
new_game = True
# random level have 10-14 tubes, always two empty
tubes = 10
tube_colors = []

# generate new level when initialized
def generate_start():
    tubes_number = random.randint(10, 14)
    tube_colors = []
    available_colors = []
    for i in range(tubes_number):
        tube_colors.append([])
        if i < tubes_number - 2:
            for j in range(4):
                available_colors.append(i)
    for i in range(tubes_number - 2):
        for j in range(4):
            color = random.choice(available_colors)
            tube_colors[i].append(color)
            available_colors.remove(color)
    print(tube_colors, tubes_number)
    return tubes_number, tube_colors

# draw tubes
def draw_tubes(tubes, tube_colors):
    tube_width = 50
    tube_height = 400
    tube_gap = 20
    top_margin = 50
    left_margin = (WIDTH - tube_width * tubes - tube_gap * (tubes - 1)) // 2

    tubes_rects = []
    for i in range(tubes):
        x = left_margin + (tube_width + tube_gap) * i
        y = top_margin
        pygame.draw.rect(screen, 'white', (x, y, tube_width, tube_height))  # draw tube outline
        pygame.draw.rect(screen, 'gray', (x + 5, y + 5, tube_width - 10, tube_height - 10))  # draw tube fill

        for j, color_index in enumerate(tube_colors[i]):
            color = get_color(color_index)
            pygame.draw.rect(screen, color, (x + 5, y + 5 + (tube_height - 10) * j // 4, tube_width - 10, (tube_height - 10) // 4))

        tubes_rects.append(pygame.Rect(x, y, tube_width, tube_height))
    
    return tubes_rects

# helper function to get color based on index
def get_color(index):
    if index == 0:
        return 'red'
    elif index == 1:
        return 'green'
    elif index == 2:
        return 'blue'
    elif index == 3:
        return 'yellow'
    else:
        return 'black'  # fallback color



# main game loop
run = True
while run:
    screen.fill('black')
    timer.tick(fps)

    # Generate new board/tubes
    if new_game:
        tubes, tube_colors = generate_start()
        initial_colors = copy.deepcopy(tube_colors)
        new_game = False
    else:
        tubes_rects = draw_tubes(tubes, tube_colors)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the player clicked on a tube
            for i, tube_rect in enumerate(tubes_rects):
                if tube_rect.collidepoint(event.pos):
                    if selected_tube is None:
                        selected_tube = i
                    elif selected_tube != i:
                        # Check if the tubes can be poured into each other
                        if can_pour(tube_colors[selected_tube], tube_colors[i]):
                            pour(selected_tube, i, tube_colors)
                        selected_tube = None

    pygame.display.flip()

pygame.quit()
