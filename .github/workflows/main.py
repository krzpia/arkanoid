import pygame
from os import path
vec = pygame.math.Vector2
import random
import math
pygame.init()


img_dir = path.join(path.dirname(__file__), 'img')
blocks_normal = pygame.image.load(path.join(img_dir, 'Breakout-004-C.png'))
blocks_wall = pygame.image.load(path.join(img_dir, 'Breakout-009-C.png'))
blocks_hard2 = pygame.image.load(path.join(img_dir, 'Breakout-002-C.png'))
blocks_hard1 = pygame.image.load(path.join(img_dir, 'Breakout-003-C.png'))


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800,600), pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Blockbuster")
        self.running = True
        self.FPS = 0
        self.clock = pygame.time.Clock()
        self.font_arial = pygame.font.match_font("arial")
        self.main_running = True
        self.game_over_loop = True
        self.high_score = 0

    def start_game(self):
        self.main_running = True
        global points
        points = 0
        self.pad = Pad()
        self.ball = Ball()
        #### create spritegroup
        self.all_blocks = pygame.sprite.Group()

        #### create block. for no 1 block for testing purposes
        col_bl = 0
        row_bl = 0
        for i in range (6):
            for ii in range(8):
                col_rand_x = random.randint(0,4)
                col_rand_y = random.randint(0,2)
                rand_type = random.randint(0,6)
                if rand_type == 6:
                    self.all_blocks.add(Block(40+col_bl * 90, 40+row_bl * 35,col_rand_x,col_rand_y,1,0))
                elif rand_type == 5:
                    self.all_blocks.add(Block(40 + col_bl * 90, 40 + row_bl * 35, col_rand_x, col_rand_y, 2,0))
                else:
                    self.all_blocks.add(Block(40+col_bl * 90, 40+row_bl * 35,col_rand_x,col_rand_y,0,0))
                col_bl +=1
            col_bl = 0
            row_bl +=1

        self.wall = Wall()
        self.main_loop()

    def count_fps(self):
        self.FPS = self.clock.get_fps()

    def show_text(self, text, pos, font_type, font_size, color = (255,255,255)):
        font = pygame.font.Font(font_type, font_size)
        text_overlay = font.render(text,True,color)
        self.screen.blit(text_overlay, pos)

    def show_fps(self):
        self.show_text(str(self.FPS),(0,0),self.font_arial,16)

    def show_points(self):
        self.show_text(("PUNKTY: "+str(points)),(700,0),self.font_arial,20,(160,180,255))

    def redraw_screen(self):
        self.screen.fill((10,10,10))
        self.wall.draw(self.screen)
        self.pad.draw(self.screen)
        self.ball.draw(self.screen)
        self.all_blocks.draw(self.screen)
        self.show_points()
        self.show_fps()

    def main_loop(self):
        while self.main_running:
            ##### events
            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            for event in events:
                if event.type == pygame.QUIT:
                    self.main_running = False

            if keys[pygame.K_a]:
                self.pad.move(-1)

            if keys[pygame.K_d]:
                self.pad.move(1)

            ##### updat3
            self.ball.update(self.all_blocks)
            reflection_angle = self.pad.check_collision(self.ball)
            if reflection_angle:
                self.ball.reflect_y()
                ballanglevecold = vec(0, -1)
                ballangleold = ballanglevecold.angle_to(self.ball.velocity)
                self.ball.rotate(reflection_angle)
                ballanglevec = vec(0, -1)
                ballangle = ballanglevec.angle_to(self.ball.velocity)
                if ballangle >85 and ballangle <= 180:
                    ballanglerecover = ballangle - 80
                    self.ball.rotate(-ballanglerecover)
                    print ("BALL ANGLE RECOVER")
                if ballangle <-85 or ballangle > 180:
                    ballanglerecover = (- ballangle) - 80
                    self.ball.rotate(ballanglerecover)
                    print ("BALL ANGLE NEG RECOVER")
                #if self.ball.velocity[1] >=0:
                #    print ("URUCHAMIAM WYJATEK UJEMNEGO KATA!d")
                #    self.ball.rotate(-reflection_angle)


            if not self.ball.check_in_game():
                self.main_running = False
            self.all_blocks.update()
            self.clock.tick()
            self.count_fps()
            ##### draw
            self.redraw_screen()
            pygame.display.flip()

    def game_over(self):
        self.game_over_loop = True
        self.activate_high_score_checker = True
        global points
        while self.game_over_loop:
            ## events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.game_over_loop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        self.start_game()
                        self.activate_high_score_checker = True
            ## update
            self.clock.tick()
            self.count_fps()
            if self.activate_high_score_checker:
                self.high_score_flag = self.check_high_score(points)
                self.activate_high_score_checker = False

            ## draw
            self.screen.fill((0,0,0))
            self.show_text("KONIEC GRY",(280,200),self.font_arial,42)
            self.show_text("Twój wynik to: "+ str(points),(280,260),self.font_arial,36, (150,150,240))
            if self.high_score_flag:
                self.show_text("GRATULACJE, Osiągnąłeś najwyższy wynik!",(120,320),self.font_arial,36,(255,30,30))
            self.show_text("Jeżeli chcesz jeszcze raz, naciśnij N",(150,475),self.font_arial,36)
            pygame.display.flip()

    def check_high_score(self, result):
        self.result = result
        if self.result > self.high_score:
            self.high_score = self.result
            return True
        else:
            return False


class Pad:
    def __init__(self):
        self.surface = pygame.Surface((100, 15), pygame.HWSURFACE | pygame.SRCALPHA)
        self.surface.fill((255,255,255))
        self.rect = self.surface.get_rect()
        self.rect.x = 350
        self.rect.y = 550

    def draw(self, screen):
        screen.blit(self.surface,(self.rect.x, self.rect.y))

    def move(self, vector_x):
        if vector_x >0:
            if self.rect.x < 700:
                self.rect.x += vector_x
        if vector_x <0:
            if self.rect.x >0:
                self.rect.x += vector_x

    def check_collision(self, ball):
        ballrect = pygame.Rect(ball.pos.x, ball.pos.y,ball.radius,ball.radius)
        collision = self.rect.colliderect(ballrect)

        if collision:
            #print ("collision at:" + str(ball.pos.x))
            #print ("pad center at: " + str(self.rect.center[0]))
            addangle = (ball.pos.x - self.rect.center[0])
            if addangle <-30:
                addangle = -30
            if addangle >30:
                addangle = 30
            ballanglevec = vec(0,-1)
            ballangle = ballanglevec.angle_to(ball.velocity)
            print ("PAD COLLISION>>")
            print ("Y VECTOR: "+ str(ball.velocity[1]))
            print ("ballangle: "+ str(int(ballangle)))
            print("addangle: " + str(addangle))
            return addangle
        return False

class Ball:
    def __init__(self):
        posx = random.random()
        negx = - posx
        randomsx = [posx, negx]
        x = random.choice(randomsx)
        y = math.sqrt((1-x**2))
        self.pos = vec(400,400)
        self.velocity = vec(x,-y)
        self.acceleration = vec(0,0)
        self.radius = 6
        self.color = (255,255,255)

    def draw(self, screen):
        pygame.draw.circle(screen,self.color,(int(self.pos.x), int(self.pos.y)),self.radius)

    def update(self, all_blocks):
        self.pos += self.velocity + 0.5 * self.acceleration
        self.check_wall_collision()
        self.check_block_collision(all_blocks)

    def check_wall_collision(self):
        if self.pos.x >= 798 - self.radius and self.pos.y <= 545:
            self.reflect_x()
        if self.pos.x <= 0 + self.radius and self.pos.y <= 545:
            self.reflect_x()
        if self.pos.y <= 20 + self.radius:
            self.reflect_y()

    def check_block_collision(self,all_blocks):
        global points
        n = 0

        def block_hit(all_blocks):
            global points
            if not block.wall_block:
                if block.hard_block:
                    if block.hard_block_destroy():
                        all_blocks.remove(block)
                        points += 1
                else:
                    all_blocks.remove(block)
                    points += 1

        blocks = all_blocks.sprites()
        ballrect = pygame.Rect(self.pos.x, self.pos.y,self.radius,self.radius)
        for block in blocks:
            n += 1
            collision = ballrect.colliderect(block.rect)
            if collision:
                if ballrect.right > block.rect.left and ballrect.left < block.rect.right:
                    if ballrect.top + 1 == block.rect.bottom:
                        print ("SOUTH COLLISION")
                        self.reflect_y()
                        block_hit(all_blocks)
                    if ballrect.bottom == block.rect.top + 1:
                        print ("NORTH COLLISION")
                        self.reflect_y()
                        block_hit(all_blocks)
                if ballrect.bottom > block.rect.top and ballrect.top < block.rect.bottom:
                    if ballrect.right == block.rect.left + 1:
                        print ("EAST COLLISION")
                        self.reflect_x()
                        block_hit(all_blocks)
                    if ballrect.left + 1 == block.rect.right:
                        print ("WEST COLLISION")
                        self.reflect_x()
                        block_hit(all_blocks)


    def reflect_x(self):
        self.velocity = vec(self.velocity.x * -1, self.velocity.y)
        #ballanglevec = vec(0, -1)
        #ballangle = int(ballanglevec.angle_to(self.velocity))
        #print("ballangle after collision: " + str(ballangle))
        #print("------------------------------")

    def reflect_y(self):
        self.velocity = vec(self.velocity.x, self.velocity.y * -1)
        #ballanglevec = vec(0, -1)
        #ballangle = int(ballanglevec.angle_to(self.velocity))
        #print("ballangle after collision: " + str(ballangle))
        #print("------------------------------")

    def rotate(self, angle):
        self.velocity = self.velocity.rotate(angle)
        ballanglevec = vec(0, -1)
        ballangle = int(ballanglevec.angle_to(self.velocity))
        print("ballangle after additional rotation: " + str(ballangle))
        print("------------------------------")

    def check_in_game(self):
        if self.pos.x <0 - self.radius or self.pos.x > 800+self.radius:
            return False
        if self.pos.y < 0 - self.radius or self.pos.y > 600 + self.radius:
            return False
        return True

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, col_x, col_y, hard = False, wall = False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((80,20),pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.image.fill((255,255,255))

        self.texture = pygame.Surface((64,32),pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.texture.blit(blocks_normal,(0,0),(col_x * 64, col_y * 32,64,32))
        self.texture = pygame.transform.scale(self.texture, (80, 20))

        self.texture_h1 = pygame.Surface((64,32),pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.texture_h1.blit(blocks_hard1, (0, 0), (col_x * 64, col_y * 32, 64, 32))
        self.texture_h1 = pygame.transform.scale(self.texture_h1, (80, 20))

        self.texture_h2 = pygame.Surface((64, 32),pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.texture_h2.blit(blocks_hard2, (0, 0), (col_x * 64, col_y * 32, 64, 32))
        self.texture_h2 = pygame.transform.scale(self.texture_h2, (80, 20))

        self.texture_w = pygame.Surface((64, 32,),pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.texture_w.blit(blocks_wall, (0, 0), (col_x * 64, col_y * 32, 64, 32))
        self.texture_w = pygame.transform.scale(self.texture_w, (80, 20))

        self.textures = [self.texture, self.texture_h1, self.texture_h2]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.wall_block = wall
        self.hard_block = hard
        self.reward = False
        if self.wall_block:
            self.image.blit(self.texture_w, (0, 0))
        elif self.hard_block:
            self.image.blit(self.textures[self.hard_block],(0,0))
        else:
            self.image.blit(self.texture,(0,0))

    def hard_block_destroy(self):
        if not self.wall_block:
            self.hard_block -= 1
            self.image.blit(self.textures[self.hard_block],(0,0))
            if self.hard_block < 0:
                return True
            else:
                return False


class Wall:
    def __init__(self):
        self.l1start = vec(0,20)
        self.l1end = vec(798,20)
        self.l2start = vec(0,20)
        self.l2end = vec(0,545)
        self.l3start = vec(798,20)
        self.l3end = vec(798,545)

    def draw(self, screen):
        pygame.draw.line(screen,(15,15,255),self.l1start,self.l1end,2)
        pygame.draw.line(screen, (15, 15, 255), self.l2start, self.l2end, 2)
        pygame.draw.line(screen, (15, 15, 255), self.l3start, self.l3end, 2)


game = Game()
game.start_game()
game.game_over()
pygame.quit()