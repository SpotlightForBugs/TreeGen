import sys
from os import environ
import math
import easygui
import random

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame  # skipcq FLK-E402

uuids = []


class Node:
    def __init__(self, name, parent=None, word=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.word = word

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
                new_node = Node(letter, parent=node, word=word)
                node.children.append(new_node)
                node = new_node


def generate_uuid():
    if len(uuids) == 0:
        uuids.append(0)
        return 0
    uuid = uuids[len(uuids) - 1] + 1
    uuids.append(uuid)
    return uuid


def update_wordlist(param):
    if len(word_list) == 0:
        word_list.append(param)
    else:
        for i in range(len(word_list)):
            if param[0] == word_list[i][0]:
                word_list[i] = param
                break
            if i == len(word_list) - 1:
                word_list.append(param)


class VisualNode:
    def __init__(self, name, x, y, uuid, word=""):
        self.name = name
        self.x = x
        self.y = y
        self.word = word
        self.is_complete_word = False
        self.uuid = uuid
        update_wordlist([self.uuid, self])

    def set_word(self, word, is_complete_word=False):
        self.word = word
        self.is_complete_word = is_complete_word
        if is_complete_word:
            self.draw()
        update_wordlist([self.uuid, self])

    def transform(self, scale, tree_offset_x, tree_offset_y):
        self.x = int(self.x * scale + tree_offset_x)

        self.y = int(self.y * scale + tree_offset_y)
        update_wordlist([self.uuid, self])

    def draw(self):
        if self.is_complete_word:
            color = pygame.color.THECOLORS['green']
        else:
            color = (0, 0, 0)  # Black for other nodes

        text_surface = font.render(self.name, True, color)
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        pygame.draw.circle(screen, WHITE, (self.x, self.y), 20)
        screen.blit(text_surface, text_rect)


def find_clicked_node(x, y, word_list):
    nearest_node = None
    min_distance = float('inf')
    max_y_offset = 10
    max_x_offset = 10

    for node_tuple in word_list:
        node = node_tuple[1]
        distance = math.sqrt((x - node.x) ** 2 + (y - node.y) ** 2)
        if distance < min_distance and abs(x - node.x) < max_x_offset and abs(y - node.y) < max_y_offset:
            min_distance = distance
            nearest_node = node

    return nearest_node


def render_visual_tree(node, x, y, spacing, scale, tree_offset_x, tree_offset_y):
    visual_node = VisualNode(
        node.name, x, y, uuid=generate_uuid(), word=node.word)
    visual_node.set_word(node.word)

    visual_node.transform(scale, tree_offset_x, tree_offset_y)

    visual_node.draw()

    child_x = x - spacing // 2
    child_y = y + 500

    for child in node.children:
        child_visual_node = VisualNode(
            child.name, child_x, child_y, uuid=generate_uuid(), word=child.word)

        child_visual_node.transform(scale, tree_offset_x, tree_offset_y)
        if child_visual_node.word == autocomplete_word_beginning:
            line_color = pygame.color.THECOLORS['green']
        elif autocomplete_word_beginning[:len(child_visual_node.word)] == child_visual_node.word[
                                                                        :len(autocomplete_word_beginning)]:

            line_color = pygame.color.THECOLORS['yellow']

        else:
            line_color = pygame.color.THECOLORS['black']

        pygame.draw.line(screen, line_color, (visual_node.x, visual_node.y + 20),
                         (child_visual_node.x, child_visual_node.y),
                         2)

        render_visual_tree(child, child_x, child_y, spacing //
                           2, scale, tree_offset_x, tree_offset_y)
        child_x += spacing


# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode(
    (screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Word Tree Visualization")

# Define font
font_name = "Monospace"
font = pygame.font.SysFont(font_name, 20)

try:
    # load the wordlist from the file words.txt
    with open("words.txt", mode="r", encoding="utf-8") as f:
        words = f.read().splitlines()
except FileNotFoundError:
    print("File words.txt not found!")
    input("Press Enter to continue...")
    sys.exit()

# Create the word tree
word_tree = WordTree()

for word in words:
    word_tree.insert_word(word.lower())

# Initialize zoom and panning
scale = 1.0
tree_offset_x = 0
tree_offset_y = 0

# word_list
word_list = []

text_to_render = [0, 0, ""]

changed = True
last_word = ""
inputbox = False
show_autocomplete = True
# Main loop
running = True
while running:

    if show_autocomplete:
        inputbox = easygui.enterbox(
            "Enter a word to autocomplete", "Autocomplete")

    if inputbox:
        autocomplete_word_beginning = inputbox
        last_word = autocomplete_word_beginning
        show_autocomplete = False
    else:
        if last_word:
            autocomplete_word_beginning = last_word
        else:
            autocomplete_word_beginning = ""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(
                (event.w, event.h), pygame.RESIZABLE)
            changed = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up (zoom in)
                scale *= 1.1
                changed = True
            elif event.button == 5:  # Scroll down (zoom out)
                scale /= 1.1
                changed = True
            if event.button == 1:  # Left mouse button click
                x, y = event.pos
                changed = True
                clicked_node: VisualNode = find_clicked_node(x, y, word_list)
                if clicked_node:

                    possible_words = []
                    for node in word_list:
                        if node[1].word:
                            if str(node[1].word).startswith(clicked_node.word):
                                possible_words.append(node[1].word)

                    # render those next to the mouse cursors click position
                    res = []
                    [res.append(x) for x in possible_words if x not in res]

                    text_to_render = [
                        x, y, "Possible words: " + ", ".join(res)]

                changed = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        tree_offset_x += 10
        changed = True
    if keys[pygame.K_RIGHT]:
        tree_offset_x -= 10
        changed = True
    if keys[pygame.K_UP]:
        tree_offset_y += 10
        changed = True
    if keys[pygame.K_DOWN]:
        tree_offset_y -= 10
        changed = True
    if keys[pygame.K_TAB]:
        show_autocomplete = not show_autocomplete
        changed = True

    if changed:
        screen.fill(WHITE)
        render_visual_tree(word_tree.root, screen_width // 2,
                           100, 400, scale, tree_offset_x, tree_offset_y)
        if text_to_render[2] != "":
            text_surface = font.render(text_to_render[2], True, BLACK)
            text_rect = text_surface.get_rect(
                center=(text_to_render[0], text_to_render[1]))
            text_to_render = [0, 0, ""]
            screen.blit(text_surface, text_rect)
        pygame.display.flip()

        for node in word_list:
            if str(node[1].word).startswith(autocomplete_word_beginning):
                selected_node: VisualNode = node[1]
                selected_node.set_word(selected_node.word, True)

        changed = False

# Quit Pygame
pygame.quit()
sys.exit()
