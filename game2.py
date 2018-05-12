import pygame
import random
import os.path

# game constants
SCREENRECT = pygame.Rect(0, 0, 640, 480)

main_dir = '/Users/kitmenzies-wilson/PycharmProjects/first_pygame/' #os.path.split(os.path.abspath(__file__))[0]

def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pygame.get_error()))
    return surface.convert()



class Player(pygame.sprite.Sprite):
    speed = 10
    bounce = 24
    images = []
    alive = True

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=(320,400))#SCREENRECT.midbottom)
        self.origtop = self.rect.top
        self.facing = -1

    def move(self, direction):
        if direction: self.facing = direction
        self.rect.move_ip(direction * self.speed, 0)
        self.rect = self.rect.clamp(SCREENRECT)
        self.rect.top = self.origtop - (self.rect.left // self.bounce % 2)


class Falling_obj(pygame.sprite.Sprite):
    speed = 4
    bounce = 24
    images = []

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        rand_top_left = (SCREENRECT.topright[0]*random.random(),0)
        self.rect = self.image.get_rect(topleft=rand_top_left)
        self.origtop = self.rect.top
        self.facing = -1

    def move(self, direction):
        if direction: self.facing = direction
        self.rect.move_ip(0,direction * self.speed)
        #self.rect = self.rect.clamp(SCREENRECT)
        #self.rect.midtop = self.origtop + (self.rect.top // self.bounce % 2)

def main():
    pygame.init()
    # Set the display mode
    screen = pygame.display.set_mode((640, 400), pygame.HWSURFACE | pygame.DOUBLEBUF)

    # Init game groups and assign to sprite
    all = pygame.sprite.RenderUpdates()
    Player.containers = all
    Falling_obj.containers = all

    #time
    clock = pygame.time.Clock()

    #background
    #create the background, tile the bgd image
    #bgdtile = load_image('background.gif')
    background = pygame.Surface(SCREENRECT.size)
    #for x in range(0, SCREENRECT.width, bgdtile.get_width()):
    #    background.blit(bgdtile, (x, 0))
    #screen.blit(background, (0,0))
    #pygame.display.flip()

    # ims
    tim = load_image('Player1.jpg')
    robbie = load_image('Robbie.jpg')
    #img.set_colorkey((255, 255, 255))
    Player.images = [tim, pygame.transform.flip(tim, 1, 0)]
    Falling_obj.images = [robbie, pygame.transform.flip(robbie, 1, 0)]

    # init sprites
    player = Player()
    falling_obj = Falling_obj()

    while player.alive:

        all.clear(screen,background)

        # draw the scene
        dirty = all.draw(screen)
        pygame.display.update(dirty)

        # quit?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.alive = False

        keystate = pygame.key.get_pressed()

        #Capture user input
        direction = keystate[pygame.K_RIGHT] - keystate[pygame.K_LEFT]
        player.move(direction)

        #Move falling obj
        falling_obj.move(1)

        #Check if obj onscreen
        if not falling_obj.rect.colliderect(SCREENRECT):
            print('You dropped Robbie')
            player.alive=False

        #Check if player caught robbie
        if falling_obj.rect.colliderect(player.rect):
            print('You saved a kick turn')
            falling_obj.kill()
            falling_obj = Falling_obj()


        #cap the framerate
        clock.tick(40)
        #print(clock.get_time())

    print('End game')

if __name__ == '__main__':
    main()
