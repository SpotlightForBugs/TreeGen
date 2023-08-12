import pygame
import sys


class Node:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []

    def add_child(self, child):
        self.children.append(child)


class WordTree:
    def __init__(self):
        self.root = Node('')

    def insert_word(self, word):
        node = self.root
        for letter in word:
            found = False
            for child in node.children:
                if child.name == letter:
                    node = child
                    found = True
                    break
            if not found:
                new_node = Node(letter, parent=node)
                node.children.append(new_node)
                node = new_node


class VisualNode:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.word = ""
        self.is_complete_word = False

    def set_word(self, word, is_complete_word):
        self.word = word
        self.is_complete_word = is_complete_word

    def transform(self, scale, tree_offset_x, tree_offset_y):
        self.x = int(self.x * scale + tree_offset_x)
        self.y = int(self.y * scale + tree_offset_y)

    def draw(self):
        if self.is_complete_word:
            color = (0, 255, 0)  # Green for complete words
        else:
            color = (0, 0, 0)    # Black for other nodes

        text_surface = font.render(self.name, True, color)
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        pygame.draw.circle(screen, WHITE, (self.x, self.y), 20)
        screen.blit(text_surface, text_rect)


def find_clicked_node(node, x, y, scale, offset_x, offset_y):
    # Recursive function to find the clicked node
    pass


def get_possible_words(node):
    # Function to return possible words based on the clicked node
    # Implement your logic here
    pass


def render_visual_tree(node, x, y, spacing, scale, tree_offset_x, tree_offset_y):
    visual_node = VisualNode(node.name, x, y)
    visual_node.transform(scale, tree_offset_x, tree_offset_y)
    visual_node.draw()

    child_x = x - spacing // 2
    child_y = y + 100

    for child in node.children:
        child_visual_node = VisualNode(child.name, child_x, child_y)
        child_visual_node.transform(scale, tree_offset_x, tree_offset_y)

        pygame.draw.line(screen, BLACK, (visual_node.x, visual_node.y + 20), (child_visual_node.x, child_visual_node.y), 2)
        render_visual_tree(child, child_x, child_y, spacing // 2, scale, tree_offset_x, tree_offset_y)
        child_x += spacing



# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Word Tree Visualization")

# Define font
font = pygame.font.Font(None, 24)

# Beispiel Wörterliste
words = ["Hundefutter", "Roberto", "Roboter", "Huhn"]

# Create the word tree
word_tree = WordTree()

for word in words:
    word_tree.insert_word(word)

# Initialize zoom and panning
scale = 1.0
tree_offset_x = 0
tree_offset_y = 0

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up (zoom in)
                scale *= 1.1
            elif event.button == 5:  # Scroll down (zoom out)
                scale /= 1.1
            elif event.button == 1:  # Left mouse button click
                x, y = event.pos
                clicked_node = find_clicked_node(word_tree.root, x, y, scale, tree_offset_x, tree_offset_y)
                if clicked_node:
                    print("Clicked Node:", clicked_node.word)
                    print("Can Form Words:", get_possible_words(clicked_node))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        tree_offset_x += 10
    if keys[pygame.K_RIGHT]:
        tree_offset_x -= 10
    if keys[pygame.K_UP]:
        tree_offset_y += 10
    if keys[pygame.K_DOWN]:
        tree_offset_y -= 10

    screen.fill(WHITE)
    render_visual_tree(word_tree.root, screen_width // 2, 100, 400, scale, tree_offset_x, tree_offset_y)
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()