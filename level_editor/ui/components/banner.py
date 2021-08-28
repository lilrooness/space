import pygame.draw

from client.const import scheme

ANCHOR_CENTER = 1
ANCHOR_RIGHT = 2
ANCHOR_LEFT = 3
ANCHOR_TOPLEFT = 4

def banner(
        screen,
        x,
        y,
        text,
        font,
        padding=2,
        top=0,
        left=0,
        anchor=ANCHOR_CENTER,
        background_color=None,
        foregound_color=None,
    ):
    width, height = font.size(text)

    if not background_color:
        background_color = scheme["banner_background"]

    if not foregound_color:
        foregound_color = scheme["banner_foreground"]

    x = x
    y = y - height - padding + top

    if anchor == ANCHOR_CENTER:
        x = x - width/2 - padding + left
    elif anchor == ANCHOR_LEFT:
        x = x - padding + left
    elif anchor == ANCHOR_RIGHT:
        x = x - width - padding + left
    elif anchor == ANCHOR_TOPLEFT:
        y = y + height + padding + top
        x = x

    rect = pygame.Rect(
        x,
        y,
        width + padding*2,
        height + padding*2,
    )
    pygame.draw.rect(screen, background_color, rect)
    instructionImage = font.render(text, True, foregound_color)
    textPos = (rect.x + padding + left, rect.y + padding)
    screen.blit(instructionImage, textPos)
    return rect
