import pygame


pygame.font.init()

def scale_image(image, size):
    return pygame.transform.scale(image, (size, size))

def multitext(text, x, y, w, spacing, font, font_size, colour, pos='topleft', antialias=False):
    images = []
    rects = []
    lines = []

    font = pygame.font.SysFont(font, font_size)
    prev = 0
    for i in range(1, len(text)):
        if font.size(text[prev: i])[0] >= w:
            lines.append(text[prev: i-1])
            prev = i-1
    lines.append(text[prev:])
    for line in lines:
        image = font.render(line, antialias, colour)
        images.append(image)

        if pos == 'topleft':
            rect = image.get_rect(topleft = (x, y))
        elif pos == 'topright':
            rect = image.get_rect(topright = (x, y))
        elif pos == 'bottomleft':
            rect = image.get_rect(bottomleft = (x, y))
        elif pos == 'bottomright':
            rect = image.get_rect(bottomright = (x, y))
        rects.append(rect)

        y += spacing
    
    return images, rects
