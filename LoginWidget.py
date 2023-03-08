import pygame


class InputLogin(pygame.sprite.Sprite):
    def __init__(self, w_widget=200, h_widget=100, w_screen=1080, h_screen=600):
        super(InputLogin, self).__init__()
        left, top = (w_screen - w_widget) // 2, (h_screen - h_widget) // 2
        self.rect = pygame.Rect((left, top, w_widget, h_widget))
        self.image = pygame.Surface((w_widget, h_widget), pygame.SRCALPHA, 32)
        self.image.fill("grey")
        self.font_size = 15 * h_widget // 100
        self.font = pygame.font.Font(None, self.font_size)
        self.login = ''
        self.text = self.font.render(self.login, True, "black")
        self.limit = self.rect.w - self.font_size * 2

    def update(self, event=None, **kwargs):  # type of event is pygame.KEYDOWN
        if not event:  # unicode, key, mod, scancode, window
            return
        if event.key == 8:  # backspace
            self.login = self.login[:-1]
        elif event.key == 32:
            if len(self.login):
                self.login += event.unicode
        elif event.key not in (9, ):
            self.login += event.unicode
        text = self.font.render(self.login, True, "black")
        if text.get_width() > self.limit:
            self.login = self.login[:-1]
            return
        self.text = text
        self.image.fill("grey")
        self.image.blit(self.text, (self.font_size, 3 * self.font_size))


def main():  # just for test
    pygame.init()
    size = (1080, 600)
    screen = pygame.display.set_mode(size)
    sprites = pygame.sprite.Group()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                sprites.add(InputLogin())
            if event.type == pygame.KEYDOWN:
                sprites.update(event=event)
        screen.fill("black")
        sprites.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
