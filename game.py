import pygame, sys
from scripts.entities import PhysicsEntity, Player
from scripts.utils import *
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):
       pygame.init()
       pygame.mixer.pre_init(0, -16, 2, 1024)

       self.width = 640
       self.height = 480
       pygame.display.set_caption("Game")
       self.screen = pygame.display.set_mode((self.width, self.height))
       self.display = pygame.Surface((320, 240))

       self.clock = pygame.time.Clock()
       self.mouvement = [False, False]

#-----------------------Load Data (kan loader data dyali (background,playey_image...) )-------------------------------------------------------
       self.assets = {
           'player' : load_img('player2.png'),
           'grass' : load_img('tiles/1.png'),
           'stone' : load_img('tiles/2.png'),
           'background' : load_img('1.png'),
           'player/idle' : Animation(load_images('animation/idle'), img_dur=10),
           'player/run' : Animation(load_images('animation/run'), img_dur=4),
           'player/jump' : Animation(load_images('animation/jump'), img_dur=4),
           'cave' : load_images('Parallax')
       }
       self.cave_sfx = pygame.mixer.Sound('sfx/cave-sfx2.wav')
       self.cave_sfx.set_volume(0.03)
       self.run_sfx = pygame.mixer.Sound('sfx/dirt2.wav')
       self.run_sfx.set_volume(0.02)
#--------------------------------------------------------------------------------------
#------------------------------------objects (object mn kola classe gadinah)--------------------------------------------
       self.player = Player(self, (250, -50), (16,25))
       self.tilemap = Tilemap(self, 16)
       self.scroll = [0, 0]
       self.sky_scroll = 0

    def sky_parallax(self):
        for x in range(20):
            self.display.blit(self.assets['cave'][7], ((320 * x) - self.scroll[0] * 0.2 ,0))
            self.display.blit(self.assets['cave'][6], ((320 * x) - self.scroll[0] * 0.4,20))
            self.display.blit(self.assets['cave'][5], ((320 * x) - self.scroll[0] * 0.5,30))
            self.display.blit(self.assets['cave'][4], ((320 * x) - self.scroll[0] * 0.6,40))
            self.display.blit(self.assets['cave'][3], ((320 * x) - self.scroll[0] * 0.7,0))
            self.display.blit(self.assets['cave'][1], ((320 * x) - self.scroll[0] * 0.9,20))

    #---------------------------------------------------------------------------------------
    def run(self):
        while True:
            self.display.fill((0,0,0))
            self.cave_sfx.play(-1, fade_ms=2000)
            self.sky_parallax()
            self.sky_scroll += (self.mouvement[1] - self.mouvement[0])

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 20
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 20
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)
            self.player.update(self.tilemap, (self.mouvement[1] - self.mouvement[0], 0))
            self.player.render(self.display, 'player', offset=render_scroll)

#-------------------------Keys Handling (les Buttons dyal lclavier likan7rk behom)-----------------------------------------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.mouvement[0] = True
                        self.run_sfx.play(-1)
                    if event.key == pygame.K_RIGHT:
                        self.mouvement[1] = True
                        self.run_sfx.play(-1)
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] -= 3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.mouvement[0] = False
                        self.run_sfx.stop()
                    if event.key == pygame.K_RIGHT:
                        self.mouvement[1] = False
                        self.run_sfx.stop()
# ------------------------------------------------------------------------------------
            # transform scale fonction katkhlik tkbr screen dyalk
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()),  (0,0))
            pygame.display.flip()
            # hna kat fixer fps dyalk fkola frame per second
            self.clock.tick(60)

Game().run()
