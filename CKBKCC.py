import pygame
import sys
import pyperclip

pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 850
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 128, 255)
GRAY = (50, 50, 50)

# Fonts
try:
    FONT = pygame.font.Font('OpenDyslexic-Regular.otf', 40)
    SMALL_FONT = pygame.font.Font('OpenDyslexic-Regular.otf', 28)
except:
    FONT = pygame.font.SysFont('Arial', 40)
    SMALL_FONT = pygame.font.SysFont('Arial', 28)

# Layouts
letter_keyboard = [
    "ABCDEF",
    "GHIJKL",
    "MNOPQR",
    "STUVWX",
    "YZC .<"  # C for Clear All, < for Backspace
]

phrase_keyboards = {
    "names": ["Ryan", "Mamie", "Brendan", "Devin", "Poppy"],
    "statements": ["Hi", "Goodbye", "Yes", "No", "I'm feeling sick"],
    "medicines": ["Flexorol", "Tylenol"]
}

shortcuts = ["Ctrl+Z", "Ctrl+C", "Ctrl+V", "Ctrl+X"]
emojis = [":)", ":(", ":/", ":D", ":P", ":O"]

TABS = ["letters", "names", "statements", "medicines", "shortcuts", "emojis"]
tab_index = 0

# State
cursor_x, cursor_y = 0, 0
typed_text = ""

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KCCv5.18.2 Keyboard")

KEY_WIDTH = 90
KEY_HEIGHT = 60
H_PADDING = 300
V_PADDING = 80
V_SPACING = 70

def draw_text_box():
    box_w = H_PADDING - 40
    box_h = HEIGHT - 60
    pygame.draw.rect(screen, GRAY, (20, 30, box_w, box_h), border_radius=10)
    pygame.draw.rect(screen, WHITE, (20, 30, box_w, box_h), 2, border_radius=10)

    words = typed_text.split(' ')
    lines, line = [], ""
    for word in words:
        test = line + word + " "
        if FONT.size(test)[0] < box_w - 20:
            line = test
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)

    y = 40
    for l in lines[-20:]:
        screen.blit(FONT.render(l.strip(), True, WHITE), (30, y))
        y += 40

def draw_footer():
    label = SMALL_FONT.render("KCCv5.18.2", True, GRAY)
    screen.blit(label, (WIDTH - 200, HEIGHT - 40))

def draw_letter_keyboard():
    for y, row in enumerate(letter_keyboard):
        for x, char in enumerate(row):
            rect = pygame.Rect(H_PADDING + x * KEY_WIDTH, V_PADDING + y * V_SPACING, KEY_WIDTH, KEY_HEIGHT)
            if x == cursor_x and y == cursor_y:
                pygame.draw.rect(screen, BLUE, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect, 2)
            screen.blit(FONT.render(char, True, WHITE), (rect.x + 20, rect.y + 10))

def draw_phrase_keyboard():
    category = TABS[tab_index]
    phrases = phrase_keyboards.get(category, [])
    for i, phrase in enumerate(phrases):
        x = H_PADDING + (i % 2) * (KEY_WIDTH * 3 + 20)
        y = V_PADDING + (i // 2) * (KEY_HEIGHT + 20)
        rect = pygame.Rect(x, y, KEY_WIDTH * 3, KEY_HEIGHT)
        if cursor_x == i and cursor_y == 0:
            pygame.draw.rect(screen, BLUE, rect)
        else:
            pygame.draw.rect(screen, WHITE, rect, 2, border_radius=10)
        screen.blit(SMALL_FONT.render(phrase, True, WHITE), (x + 10, y + 10))

def draw_shortcuts():
    for i, sc in enumerate(shortcuts):
        x = H_PADDING
        y = V_PADDING + i * (KEY_HEIGHT + 20)
        rect = pygame.Rect(x, y, KEY_WIDTH * 4, KEY_HEIGHT)
        if cursor_x == i and cursor_y == 0:
            pygame.draw.rect(screen, BLUE, rect)
        else:
            pygame.draw.rect(screen, WHITE, rect, 2)
        screen.blit(SMALL_FONT.render(sc, True, WHITE), (x + 10, y + 10))

def draw_emojis():
    for i, emo in enumerate(emojis):
        x = H_PADDING + (i % 2) * (KEY_WIDTH + 40)
        y = V_PADDING + (i // 2) * (KEY_HEIGHT + 40)
        rect = pygame.Rect(x, y, KEY_WIDTH, KEY_HEIGHT)
        if cursor_x == i and cursor_y == 0:
            pygame.draw.rect(screen, BLUE, rect)
        else:
            pygame.draw.rect(screen, WHITE, rect, 2)
        screen.blit(FONT.render(emo, True, WHITE), (x + 20, rect.y + 10))

def draw():
    screen.fill(BLACK)
    draw_text_box()
    if TABS[tab_index] == "letters":
        draw_letter_keyboard()
    elif TABS[tab_index] in phrase_keyboards:
        draw_phrase_keyboard()
    elif TABS[tab_index] == "shortcuts":
        draw_shortcuts()
    elif TABS[tab_index] == "emojis":
        draw_emojis()
    draw_footer()
    pygame.display.flip()

def handle_selection():
    global typed_text
    tab = TABS[tab_index]

    if tab == "letters":
        selected = letter_keyboard[cursor_y][cursor_x]
        if selected == "<":
            typed_text = typed_text[:-1]
        elif selected == ".":
            typed_text += "."
        elif selected == "C":
            typed_text = ""
        else:
            typed_text += selected

    elif tab in phrase_keyboards:
        phrases = phrase_keyboards[tab]
        if cursor_x < len(phrases):
            typed_text += phrases[cursor_x] + " "

    elif tab == "shortcuts":
        action = shortcuts[cursor_x]
        if action == "Ctrl+C":
            pyperclip.copy(typed_text)
        elif action == "Ctrl+V":
            typed_text += pyperclip.paste()
        elif action == "Ctrl+X":
            pyperclip.copy(typed_text)
            typed_text = ""
        elif action == "Ctrl+Z":
            typed_text = "[Undo not implemented] "

    elif tab == "emojis":
        if cursor_x < len(emojis):
            typed_text += emojis[cursor_x] + " "

while True:
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                cursor_x += 1
                tab = TABS[tab_index]
                if tab == "letters":
                    cursor_x %= len(letter_keyboard[cursor_y])
                elif tab in phrase_keyboards:
                    cursor_x %= len(phrase_keyboards[tab])
                elif tab == "shortcuts":
                    cursor_x %= len(shortcuts)
                elif tab == "emojis":
                    cursor_x %= len(emojis)

            elif event.key == pygame.K_DOWN:
                if TABS[tab_index] == "letters":
                    cursor_y = (cursor_y + 1) % len(letter_keyboard)
                    cursor_x = min(cursor_x, len(letter_keyboard[cursor_y]) - 1)

            elif event.key == pygame.K_RETURN:
                handle_selection()

            elif event.key == pygame.K_BACKQUOTE:
                tab_index = (tab_index + 1) % len(TABS)
                cursor_x = 0
                cursor_y = 0
