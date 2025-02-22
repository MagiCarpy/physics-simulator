import pygame
import time
import math
import random

class Orb:
    orbs = []
    GRAV_CONSTANT = 6.6743e-11

    def __init__(self, color, x_pos, y_pos, mass, 
                 x_vel=0,y_vel=0,x_acc=0,y_acc=0):
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.x_acc = x_acc
        self.y_acc = y_acc
        self.mass = mass
        self.orbs.append(self)

    @classmethod
    def show_orbs(cls):
        print(cls.orbs)

    def __repr__(self):
        return(f"Orb({self.color}, {self.x_pos}, {self.y_pos})")

    def dist(self, orb):
        return math.sqrt(abs((self.x_pos - orb.x_pos)**2 + (self.y_pos - orb.y_pos)**2))

    def get_xyAcc(self):
        force_xComp = 0
        force_yComp = 0
        for orb in self.orbs:
            if orb == self:
                continue
            try:
                force_angle = math.acos(abs(orb.x_pos-self.x_pos)/(self.dist(orb)))
            except:
                force_angle = 0

            # handle collisions
            if self.dist(orb) >= 5:
                force_mag = self.GRAV_CONSTANT*\
                (self.mass*orb.mass)/(self.dist(orb))**2

                if (orb.x_pos-self.x_pos) < 0:
                    force_xComp -= force_mag*math.cos(force_angle)
                else: 
                    force_xComp += force_mag*math.cos(force_angle)

                if (orb.y_pos-self.y_pos) > 0:
                    force_yComp += force_mag*math.sin(force_angle)
                else:
                    force_yComp -= force_mag*math.sin(force_angle)
            elif self.dist(orb) <= 3.5:
                final_xvel = (orb.mass*orb.x_vel + self.mass*self.x_vel)/(orb.mass+self.mass)
                final_yvel = (orb.mass*orb.x_vel + self.mass*self.x_vel)/(orb.mass+self.mass)
                orb.mass += self.mass
                orb.x_vel = final_xvel
                orb.y_vel = final_yvel
                self.orbs.remove(self)
            else:
                continue

        self.x_acc = force_xComp/self.mass
        self.y_acc = force_yComp/self.mass

        if self.x_acc > max_acc:
            self.x_acc = max_acc
        elif self.x_acc < -max_acc:
            self.x_acc = -max_acc

        if self.y_acc > max_acc:
            self.y_acc = max_acc
        elif self.y_acc < -max_acc:
            self.y_acc = -max_acc

        return (self.x_acc, self.y_acc)
    
    def update_pos(self):
        if (self.x_pos <= 0 or self.x_pos >= SCREEN_SIZE[0]):
            self.x_vel *= -1

        if (self.y_pos <= 0 or self.y_pos >= SCREEN_SIZE[1]):
            self.y_vel *= -1
        
        self.get_xyAcc()
        
        self.x_vel += self.x_acc
        self.x_pos += self.x_vel

        self.y_vel += self.y_acc
        self.y_pos += self.y_vel

        # print(f"{(self.mass):.2e}")
        # print(f"X: {self.x_pos}, {self.x_vel}, {self.x_acc}")
        # print(f"Y: {self.y_pos}, {self.y_vel}, {self.y_acc}")
        # print('-------------------------------')
    
    def draw_orb(self):
        pygame.draw.circle(screen, self.color, (self.x_pos,self.y_pos), 5,0)
        text = font.render(f"{(self.mass):.2e}", True, (255, 255, 255))
        screen.blit(text, (self.x_pos+10,self.y_pos))


if __name__ == "__main__":
    pygame.init()
    SCREEN_SIZE = (1000,1000)
    screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))
    pygame.display.set_caption('Physics Simulator')
    font = pygame.font.SysFont(None, 15) 
    
    max_acc = 10000
    max_vel = 500

    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)

    # Orb((0,255,255), 250, 250, random.randint(int(1e10), int(1e10)))

    for i in range(3):
        color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        Orb(color, random.randint(100,300), random.randint(100,300)
            , random.randint(int(1e8), int(1e9)), 0.02)

    Orb.show_orbs()

    fps = 1000

    def update():
        for orb in Orb.orbs:
            orb.update_pos()
        time.sleep(1/fps)


    running = True
    while running:

        # EXIT Screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                in_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                fin_pos = pygame.mouse.get_pos()
                x_vel = in_pos[0] - fin_pos[0]
                y_vel = in_pos[1] - fin_pos[1]

                if x_vel > max_vel:
                    x_vel = max_vel
                elif x_vel < -max_vel:
                    x_vel = -max_vel

                if y_vel > max_vel:
                    y_vel = max_vel
                elif y_vel < -max_vel:
                    y_vel = -max_vel

                print(f"{x_vel} + {y_vel}")
                color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
                Orb(color, in_pos[0], in_pos[1]
                , random.randint(int(1e8), int(1e9)),x_vel/500, y_vel/500)

        # Update Screen
        screen.fill((0,0,0))
    
        for orb in Orb.orbs:
            orb.draw_orb()
        
        update()
        pygame.display.update()


    pygame.quit()
