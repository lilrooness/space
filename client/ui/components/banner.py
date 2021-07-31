import pygame.draw

from client.const import scheme

ANCHOR_CENTER = 1
ANCHOR_RIGHT = 2
ANCHOR_LEFT = 3

def banner(screen, x, y, text, font, padding=2, top=0, left=0, anchor=ANCHOR_CENTER):
    width, height = font.size(text)

    x = x

    if anchor == ANCHOR_CENTER:
        x = x - width/2 - padding + left
    elif anchor == ANCHOR_LEFT:
        x = x
    elif anchor == ANCHOR_RIGHT:
        x = x + width/2 - padding + left

    rect = pygame.Rect(
        x,
        y - height - padding + top,
        width + padding*2,
        height + padding*2,
    )
    pygame.draw.rect(screen, scheme["banner_background"], rect)
    instructionImage = font.render(text, True, scheme["banner_foreground"])
    textPos = (rect.x + padding + left, rect.y + padding)
    screen.blit(instructionImage, textPos)
    return rect