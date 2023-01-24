
import pygame
from pygame import gfxdraw
import random, cv2, numpy, math


width = 800
height = 700
fps = 60
global showhitboxes
showhitboxes = False
showAsteroidSpawn = True

## initialize pygame and create window
pygame.init()
pygame.mixer.init()  ## For sound
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()  

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
  

def rotate(image, rect, angle):
    """Rotate the image while keeping its center."""
    # Rotate the original image without modifying it.
    new_image = pygame.transform.rotate(image, angle)
    # Get a new rect with the center of the old rect.
    rect = new_image.get_rect(center=rect.center)
    return new_image, rect
    
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.

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
        
    def update(self, screen):
        newPosition = self.velocity + self.position
        
        gfxdraw.line(screen, int(self.position.x), int(self.position.y), int(newPosition.x + (self.velocity.x * 1.7)), int(newPosition.y + (self.velocity.y * 1.7)), (255, 255, 255))
        self.position = newPosition
        self.rect.center = self.position
        if showhitboxes == True:
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)
        
        
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
    global showhitboxes, showAsteroidSpawn
    ## Game loop
    player = Player()
    playerGroup = pygame.sprite.Group(player)
    running = True
    shots = []
    asteroids = pygame.sprite.Group()
    shotCounter = 0
    canShoot = True

    while running:

    
        dt = clock.tick(fps)  
        shotCounter += 1
        if shotCounter > 30:  
            shotCounter = 0
            canShoot = True 
        for event in pygame.event.get():        

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    if showhitboxes == True:
                        showhitboxes = False
                    else:
                        showhitboxes = True
                if event.key == pygame.K_i:
                    if showAsteroidSpawn == True:
                        showAsteroidSpawn = False
                    else:
                        showAsteroidSpawn = True
                    

        keys = pygame.key.get_pressed()
        rotateaccel = 0
        if keys[pygame.K_a]:
            rotateaccel += .04 * dt
        if keys[pygame.K_d]:
            rotateaccel -= .04 * dt
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
        
        if random.randint(1, 40) == 1:
            asteroids.add(Asteroid(playerGroup, screen))
        
        screen.fill((0, 0, 0))
        for i in playerGroup:
            if showhitboxes == True:
                pygame.draw.rect(screen, (255, 255, 255), i.rect, 1)
        asteroids.update(screen)
        for asteroid in asteroids:
            if pygame.Rect.colliderect(asteroid.rect, player.rect):
                running = False
            for i in shots:
                if pygame.Rect.colliderect(asteroid.rect, i.rect):
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
                
        asteroids.draw(screen)
        for shot in shots:
            shot.update(screen)               
        playerGroup.update(rotateaccel, screen)
        pygame.display.flip()       
while True:
    main()
pygame.quit()