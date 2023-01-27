
import pygame
from pygame import gfxdraw
import random, cv2, numpy, math


width = 800
height = 700
fps = 60
global showhitboxes
showhitboxes = False
showAsteroidSpawn = False
AsteroidSpawnRate = 40
modMenu = False
invinsibilityOn = False
renderAstroids = True
## initialize pygame and create window
pygame.init()
pygame.mixer.init()  ## For sound
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()  

pygame.font.init() 
my_font = pygame.font.SysFont('Comic Sans MS', 30)

def random1(x, y):
    while True:
        h = random.randint(x, y) * random.choice([-1, 0.5, -.7, -.8, -.9 -0.5, 0.6, .7, .8, .9, 1])
        if h == 0:
            pass
        else:
            return h
def blitRotate(surf, image, pos, originPos, angle):

    # offset from pivot to center
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    
    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)



    # rotate and blit the image
    surf.blit(rotated_image, rotated_image_rect)
  



def create_neon(surf):
    surf_alpha = surf.convert_alpha()
    rgb = pygame.surfarray.array3d(surf_alpha)
    alpha = pygame.surfarray.array_alpha(surf_alpha).reshape((*rgb.shape[:2], 1))
    image = numpy.concatenate((rgb, alpha), 2)
    cv2.GaussianBlur(image, ksize=(3, 3), sigmaX=10, sigmaY=10, dst=image)
    cv2.blur(image, ksize=(5, 5), dst=image)
    bloom_surf = pygame.image.frombuffer(image.flatten(), image.shape[1::-1], 'RGBA')
    return bloom_surf
class Bullet(pygame.sprite.Sprite):
    def __init__(self, rotation, position):
        super().__init__()
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(0, 0)
        right = math.cos(math.radians(rotation + 270))
        bottom = math.sin(math.radians(rotation + 270))
        self.velocity.x += right * -8
        self.velocity.y += bottom * 8
        self.rect = pygame.rect.Rect(self.position.x, self.position.y, 5, 10)
        self.bad = False
    def update(self, screen):
        newPosition = self.velocity + self.position
        
        gfxdraw.line(screen, int(self.position.x), int(self.position.y), int(newPosition.x + (self.velocity.x * 1.7)), int(newPosition.y + (self.velocity.y * 1.7)), (255, 255, 255))
        self.position = newPosition
        self.rect.center = self.position
        if showhitboxes == True:
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)
        
        
         
def bezier(p0, p1, p2, t):
    px = p0[0]*(1-t)**2 + 2*(1-t)*t*p1[0] + p2[0]*t**2
    py = p0[1]*(1-t)**2 + 2*(1-t)*t*p1[1] + p2[1]*t**2   
    return px, py
class UFO(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.rect.Rect(0, 0, 100, 100)
        self.image = pygame.image.load("UFO.png")     
        self.point1 = (random.randint(0, width), random.randint(0, height))
        self.point2 = (random.randint(0, width), random.randint(0, height))
        self.point3 = (random.randint(0, width), random.randint(0, height))
        self.counter = 0
        self.counter2 = 0
    def update(self):
        self.counter2 += 1
        if self.counter2 == 1:
            self.counter += 1
            self.counter2 = 0
        if self.counter == 101:
            self.counter = 0
            self.point1 = self.point3
            self.point2 = (random.randint(0, width), random.randint(0, height))
            self.point3 = (random.randint(0, width), random.randint(0, height))
        px, py = bezier(self.point1, self.point2, self.point3, self.counter / 100)
            
        self.rect.x = px
        self.rect.y = py
    def shoot(self,playerGroup, group):
        for i in playerGroup:
            bullet = Bullet(math.degrees(math.atan2(i.rect.y - self.rect.y, i.rect.x - self.rect.x)), (self.rect.x, self.rect.y))
            
            bullet.velocity.x = (i.rect.x - self.rect.x ) / 100 
            bullet.velocity.y = (i.rect.y - self.rect.y ) / 100
            dist = math.hypot(bullet.velocity.x * 100, bullet.velocity.y * 100)
            bullet.velocity.x = (bullet.velocity.x / dist) * 500
            bullet.velocity.y = (bullet.velocity.y / dist) * 500
            bullet.bad = True
            group.append(bullet)
            
            
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, sprites, screen, stage=None):
        super().__init__()
        self.stage = stage
        if stage == None:
            self.stage = random.randint(1, 3)
            
        self.preFrame = pygame.Vector2(0, 0)
        if self.stage == 3:
            _temp2 = random.randint(1, 3)
            if _temp2 == 1:
                self.image = pygame.image.load("BigVar1.png")
            elif _temp2 == 2:
                self.image = pygame.image.load("BigVar2.png")
            elif _temp2 == 3:
                self.image = pygame.image.load("BigVar3.png") 
        elif self.stage == 2:
            _temp2 = random.randint(1, 3)
            if _temp2 == 1:
                self.image = pygame.image.load("MedVar1.png")
            elif _temp2 == 2:
                self.image = pygame.image.load("MedVar2.png")
            elif _temp2 == 3:
                self.image = pygame.image.load("MedVar3.png")   
        elif self.stage == 1:
            _temp2 = random.randint(1, 3)
            if _temp2 == 1:
                self.image = pygame.image.load("SmlVar1.png")
            elif _temp2 == 2:
                self.image = pygame.image.load("SmlVar2.png")
            elif _temp2 == 3:
                self.image = pygame.image.load("SmlVar3.png")    
        self.generateLocation(sprites, screen)
    def generateLocation(self, sprites, screen):
        while True:
            if self.stage == 3:
                self.rect = pygame.Rect(random.randint(0, width), random.randint(0, height), 120,120)
                self.velocity = pygame.Vector2(random1(-2, 2), random1(-2, 2))
            elif self.stage == 2:
                self.rect = pygame.Rect(random.randint(0, width), random.randint(0, height), 70, 70)
                self.velocity = pygame.Vector2(random1(-2, 2), random1(-2, 2))
            else:
                self.rect = pygame.Rect(random.randint(0, width), random.randint(0, height), 50, 50)
                self.velocity = pygame.Vector2(random1(-2, 2), random1(-2, 2))
            collided = False
            prevw = self.rect.width
            prevh = self.rect.height
            prevx = self.rect.x
            prevy = self.rect.y
            self.rect.width = 300
            self.rect.height = 300
            self.rect.x -= 100
            self.rect.y -= 100

            for sprite in sprites: 
                if pygame.Rect.colliderect(self.rect, sprite.rect):
                    collided = True
            if collided == False:
                self.rect.width = prevw
                self.rect.height = prevh
                self.rect.x = prevx
                self.rect.y = prevy
                break

            
    def update(self, screen):
        self.preFrame.x = self.rect.x
        self.preFrame.y = self.rect.y
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        if self.rect.x == self.preFrame.x:
            self.velocity.x = random1(-3, 3)
            self.velocity.y = random1(-3, 3)
        if showhitboxes == True:
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)
        if showAsteroidSpawn == True:
            prevw = self.rect.width
            prevh = self.rect.height
            prevx = self.rect.x
            prevy = self.rect.y
            
            self.rect.width = 300
            self.rect.height = 300
            self.rect.x -= 100
            self.rect.y -= 100
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)
            self.rect.width = prevw
            self.rect.height = prevh
            self.rect.x = prevx
            self.rect.y = prevy
        
class Button():
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)
        font = pygame.font.SysFont("Arial", 20)
        text = font.render(self.text, True, (255, 255, 255))
        screen.blit(text, (self.rect.x + 5, self.rect.y + 5))
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 55))
        self.image = pygame.image.load("asteroids-2x - Copy.png")
        self.originalImage = self.image
        self.rect = pygame.Rect(280, 280, 60, 50)
        self.velocity = pygame.Vector2(0, 0)
        self.rotationVelocity = 0
        self.rotationAcceleration = 0
        self.preFrameRotation = 0
        self.postion = pygame.Vector2(280, 280)
    def update(self, rotateaccel, screen):
        self.velocity *= .98
        self.postion += self.velocity
        self.rect.center = self.postion
        self.rotationVelocity += rotateaccel
        self.rotationVelocity *= .95
        self.preFrameRotation += self.rotationVelocity
        blitRotate(screen, self.originalImage, self.postion, pygame.Vector2(45, 30), self.preFrameRotation + 90)
    def shoot(self):
        bullet = Bullet(self.preFrameRotation, self.postion)
        return bullet
    
        
def main():
    #UI elements =============
    hitboxes = Button(10, 10, 80, 30, "Hitboxes")
    spawnhitboxes = Button(10, 50, 140, 30, "Spawn Hitboxes")
    invisibility = Button(10, 90, 100, 30, "Invisibility")
    RenderAsteroid = Button(10, 130, 140, 30, "Render Asteroids")
    
    #globals ------------
    global showhitboxes, showAsteroidSpawn, modMenu, invinsibilityOn, renderAstroids
    ## Game loop
    mouseRect = pygame.Rect(0, 0, 1, 1)
    player = Player()
    playerGroup = pygame.sprite.Group(player)
    running = True
    shots = []
    asteroids = pygame.sprite.Group()
    shotCounter = 0
    canShoot = True
    ufogroup = pygame.sprite.Group()
    score = 0
    scoreText  = my_font.render(str(score), False, (0, 0, 0))
    while running:

        scoreText  = my_font.render(str(score), False, (255, 255, 255))
        dt = clock.tick(fps)  
        shotCounter += 1
        if shotCounter > 30:  
            shotCounter = 0
            canShoot = True 
        for event in pygame.event.get():        

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
            
                if event.key == pygame.K_u:
                    ufogroup.add(UFO())
                if event.key == pygame.K_m:
                    if modMenu == True:
                        modMenu = False
                    else:
                        modMenu = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if modMenu == True:
                    if pygame.Rect.colliderect(mouseRect, hitboxes.rect):
                        if showhitboxes == True:
                            showhitboxes = False
                        else:
                            showhitboxes = True
                    if pygame.Rect.colliderect(mouseRect, spawnhitboxes.rect):
                        if showAsteroidSpawn == True:
                            showAsteroidSpawn = False
                        else:
                            showAsteroidSpawn = True
                    if pygame.Rect.colliderect(mouseRect, invisibility.rect):
                        if invinsibilityOn == True:
                            invinsibilityOn = False
                        else:
                            invinsibilityOn = True
                    if pygame.Rect.colliderect(mouseRect, RenderAsteroid.rect):
                        if renderAstroids == True:
                            renderAstroids = False
                        else:
                            renderAstroids = True

        keys = pygame.key.get_pressed()
        rotateaccel = 0
        if keys[pygame.K_a]:
            rotateaccel += .02 * dt
        if keys[pygame.K_d]:
            rotateaccel -= .02 * dt
        if keys[pygame.K_w]:
            
            right = math.cos(math.radians(player.preFrameRotation + 270))
            bottom = math.sin(math.radians(player.preFrameRotation + 270))
            player.velocity.x += right * -.1
            player.velocity.y += bottom * .1
            
        if keys[pygame.K_SPACE]:
            if canShoot == True:
                shots.append(player.shoot())
                canShoot = False
        if keys[pygame.K_p]:
            asteroids.add(Asteroid(playerGroup, screen)) 
        if score < 10:
            AsteroidSpawnRate = 100
        elif score < 20:
            AsteroidSpawnRate = 80
        elif score < 30:
            AsteroidSpawnRate = 70
        elif score > 30:
            if ufogroup.__len__() == 0:
                ufogroup.add(UFO())
                
        if random.randint(1, AsteroidSpawnRate) == 1:
            asteroids.add(Asteroid(playerGroup, screen))
        
        screen.fill((0, 0, 0))
        if random.randint(1, 100) == 1:
            for i in ufogroup:
                i.shoot(playerGroup, shots)
        if modMenu == True:
            mouseRect.center = pygame.mouse.get_pos()
            hitboxes.draw(screen)
            spawnhitboxes.draw(screen)
            invisibility.draw(screen)
            RenderAsteroid.draw(screen)
        for i in playerGroup:
            if showhitboxes == True:
                pygame.draw.rect(screen, (255, 255, 255), i.rect, 1)
        asteroids.update(screen)
        for asteroid in asteroids:
            if invinsibilityOn == False:
                if pygame.Rect.colliderect(asteroid.rect, player.rect):
                    running = False
            for i in shots:
                if pygame.Rect.colliderect(asteroid.rect, i.rect):
                    score += 1 
                    if asteroid.stage == 1:
                        score += 1
                    shots.remove(i)
                    asteroids.remove(asteroid)
                    if asteroid.stage != 1:
                        asteroid1 = Asteroid(playerGroup, screen, asteroid.stage - 1)
                        asteroid2 = Asteroid(playerGroup, screen, asteroid.stage - 1)
                        asteroids.add(asteroid1)
                        asteroids.add(asteroid2)
                        asteroid1.rect.center = asteroid.rect.center
                        asteroid2.rect.center = asteroid.rect.center

                    i.kill()
                    break
        for i in shots:
            if i.bad == True:
                if pygame.Rect.colliderect(i.rect, player.rect):
                    if invinsibilityOn == False:
                        running = False   
        ufogroup.update()
        ufogroup.draw(screen)
        if showhitboxes == True:
            for i in ufogroup:
                pygame.draw.rect(screen, (255, 255, 255), i.rect, 1)
        if renderAstroids == True:
            asteroids.draw(screen)
        for shot in shots:
            shot.update(screen)               
        playerGroup.update(rotateaccel, screen)
        screen.blit(scoreText, (10, height - 50))
        pygame.display.flip()       
while True:
    main()
pygame.quit()