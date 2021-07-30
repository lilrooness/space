import pygame.draw

from client.const import scheme

def banner(screen, x, y, text, font, padding=2, top=0, left=0):
    width, height = font.size(text)
    rect = pygame.Rect(
        x - width/2 - padding + left,
        y - height - padding + top,
        width + padding*2,
        height + padding*2,
    )
    pygame.draw.rect(screen, scheme["banner_background"], rect)
    instructionImage = font.render(text, True, scheme["banner_foreground"])
    textPos = (rect.x + padding + left, rect.y + padding)
    screen.blit(instructionImage, textPos)
    return rect