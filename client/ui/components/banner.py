import pygame.draw

from client.const import scheme

ANCHOR_CENTER = 1
ANCHOR_RIGHT = 2
ANCHOR_LEFT = 3
ANCHOR_TOPLEFT = 4

def banner(screen, x, y, text, font, padding=2, top=0, left=0, anchor=ANCHOR_CENTER, defer_renering=False):
    width, height = font.size(text)

    x = x
    y = y - height - padding + top

    if anchor == ANCHOR_CENTER:
        x = x - width/2 - padding + left
    elif anchor == ANCHOR_LEFT:
        x = x - padding + left
    elif anchor == ANCHOR_RIGHT:
        x = x + width/2 - padding + left
    elif anchor == ANCHOR_TOPLEFT:
        y = y + height + padding + top
        x = x

    rect = pygame.Rect(
        x,
        y,
        width + padding*2,
        height + padding*2,
    )

    instructionImage = font.render(text, True, scheme["banner_foreground"])
    textPos = (rect.x + padding + left, rect.y + padding)

    def render_component():
        pygame.draw.rect(screen, scheme["banner_background"], rect)
        screen.blit(instructionImage, textPos)

    if defer_renering:
        return (rect, render_component)
    else:
        render_component()
        return rect

