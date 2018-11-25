from scene import Scene
import pygame
import sys


class Application(object):
    def __init__(self):
        self.scene = Scene()


pygame.init()
app = Application()

running = True
while running:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if i.type == pygame.KEYDOWN:
            if pygame.key.get_mods() == pygame.KMOD_NONE:
                if i.key == pygame.K_w:
                    app.scene.handle_move({'keysym': 'w'})
                elif i.key == pygame.K_s:
                    app.scene.handle_move({'keysym': 's'})
                elif i.key == pygame.K_a:
                    app.scene.handle_move({'keysym': 'a'})
                elif i.key == pygame.K_d:
                    app.scene.handle_move({'keysym': 'd'})
                elif i.key == pygame.K_q:
                    app.scene.handle_move({'keysym': 'q'})
                elif i.key == pygame.K_e:
                    app.scene.handle_move({'keysym': 'e'})
                elif i.key == pygame.K_KP_PLUS:
                    app.scene.handle_zoom({'keysym': '+'})
                elif i.key == pygame.K_KP_MINUS:
                    app.scene.handle_zoom({'keysym': '-'})
                elif i.key == pygame.K_RETURN:
                    app.scene.reset()

            if pygame.key.get_mods() & pygame.KMOD_CTRL:
                if i.key == pygame.K_w:
                    app.scene.handle_turn({'keysym': 'w'})
                elif i.key == pygame.K_s:
                    app.scene.handle_turn({'keysym': 's'})
                elif i.key == pygame.K_a:
                    app.scene.handle_turn({'keysym': 'a'})
                elif i.key == pygame.K_d:
                    app.scene.handle_turn({'keysym': 'd'})
                elif i.key == pygame.K_q:
                    app.scene.handle_turn({'keysym': 'q'})
                elif i.key == pygame.K_e:
                    app.scene.handle_turn({'keysym': 'e'})

    pygame.display.update()

