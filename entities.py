import pygame

from pygame.math import Vector2

from settings import *

import random

def load_scaled_image(path, width, height):
    try:
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, (width, height))
        return image
    except:
        return None


class Player:
    def __init__(self):
        self.width=PLAYER_WIDTH
        self.height=PLAYER_HEIGHT
        self.pos = Vector2(WIDTH // 2 - self.width // 2, HEIGHT - 50)
        self.speed=PLAYER_SPEED
        self.hp=PLAYER_START_HP
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
        self.shoot_timer = PLAYER_SHOOT_TIMER
        self.invincible_timer = PLAYER_INVINCIBLE_TIMER
        self.bullet_count=1

        self.image = load_scaled_image(
            PLAYER_IMAGE_PATH,
            self.width,
            self.height
        )

    def move(self,keys):
        if keys[pygame.K_a]:
            self.pos.x-=self.speed
        if keys[pygame.K_d]:
            self.pos.x+=self.speed
        if keys[pygame.K_w]:
            self.pos.y-=self.speed
        if keys[pygame.K_s]:
            self.pos.y+=self.speed

        if self.pos.x<0:
            self.pos.x=0
        if self.pos.x+self.width>WIDTH:
            self.pos.x=WIDTH-self.width
        if self.pos.y<0:
            self.pos.y=0
        if self.pos.y+self.height>HEIGHT:
            self.pos.y=HEIGHT-self.height


    def shoot(self,direction):
        bullet_x=self.pos.x+self.width//2-3
        bullet_y=self.pos.y

        bullets=[]

        if self.bullet_count==1:
            velocity=direction.normalize()*PLAYER_BULLET_SPEED
            bullets.append(
                PlayerBullet(bullet_x, bullet_y, velocity)
            )

        elif self.bullet_count==2:
            left_direction=direction.rotate(-PLAYER_DOUBLE_SHOT_ANGLE).normalize()
            right_direction=direction.rotate(PLAYER_DOUBLE_SHOT_ANGLE).normalize()

            bullets.append(
                PlayerBullet(
                    bullet_x,
                    bullet_y,
                    right_direction * PLAYER_BULLET_SPEED
                )
            )

            bullets.append(
                PlayerBullet(
                    bullet_x,
                    bullet_y,
                    left_direction * PLAYER_BULLET_SPEED
                )
            )



        elif self.bullet_count==3:
            left_direction = direction.rotate(-PLAYER_TRIPLE_SHOT_ANGLE).normalize()

            middle_direction = direction.normalize()

            right_direction = direction.rotate(PLAYER_TRIPLE_SHOT_ANGLE).normalize()

            bullets.append(
                PlayerBullet(
                    bullet_x,
                    bullet_y,
                    left_direction * PLAYER_BULLET_SPEED
                )
            )

            bullets.append(
                PlayerBullet(
                    bullet_x,
                    bullet_y,
                    middle_direction * PLAYER_BULLET_SPEED
                )
            )

            bullets.append(
                PlayerBullet(
                    bullet_x,
                    bullet_y,
                    right_direction * PLAYER_BULLET_SPEED
                )
            )

        return bullets

    def draw(self,screen):
        if self.image:
            screen.blit(self.image, (self.pos.x, self.pos.y))
        else:
            pygame.draw.rect(screen, WHITE, (self.pos.x, self.pos.y, self.width, self.height))


class Enemy:
    def __init__(self):
        self.width=ENEMY_WIDTH
        self.height=ENEMY_HEIGHT
        self.pos=Vector2(random.uniform(0,WIDTH-self.width),-50)
        self.vx=random.uniform(ENEMY_MIN_VX,ENEMY_MAX_VX)
        self.vy=random.uniform(ENEMY_MIN_VY,ENEMY_MAX_VY)
        self.vel=Vector2(self.vx,self.vy)
        self.hp=ENEMY_HP
        self.shoot_cooldown = 0

        self.image = load_scaled_image(
            ENEMY_IMAGE_PATH,
            self.width,
            self.height
        )

    def update(self):
        self.pos+=self.vel

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.pos.x < 0:
            self.pos.x = 0
            self.vel.x *= -1
        if self.pos.x + self.width > WIDTH:
            self.pos.x = WIDTH - self.width
            self.vel.x *= -1
        if self.pos.y < 0:
            self.pos.y = 0
            self.vel.y *= -1
        if self.pos.y + self.height > HEIGHT:
            self.pos.y = HEIGHT - self.height
            self.vel.y *= -1

    def shoot(self,direction):
        if self.shoot_cooldown > 0:
            return None

        bullet_x = self.pos.x + self.width // 2 - 3
        bullet_y = self.pos.y
        velocity = direction.normalize() * ENEMY_BULLET_SPEED
        self.shoot_cooldown = ENEMY_SHOOT_COOLDOWN
        return EnemyBullet(bullet_x, bullet_y, velocity)

    def draw(self,screen):
        if self.image:
            screen.blit(self.image, (self.pos.x, self.pos.y))
        else:
            pygame.draw.rect(screen, RED, (self.pos.x, self.pos.y, self.width, self.height))



class Boss:
    def __init__(self):
        self.width = BOSS_WIDTH
        self.height = BOSS_HEIGHT

        self.pos = Vector2(WIDTH // 2 - self.width // 2, 50)
        self.vel = Vector2(BOSS_SPEED, 0)

        self.hp = BOSS_HP
        self.shoot_timer = 0

        self.image = load_scaled_image(
            BOSS_IMAGE_PATH,
            self.width,
            self.height
        )

    def update(self):
        self.pos += self.vel

        if self.shoot_timer > 0:
            self.shoot_timer -= 1

        if self.pos.x < 0:
            self.pos.x = 0
            self.vel.x *= -1

        if self.pos.x + self.width > WIDTH:
            self.pos.x = WIDTH - self.width
            self.vel.x *= -1

    def shoot(self):
        if self.shoot_timer > 0:
            return []

        bullet_x = self.pos.x + self.width // 2 - 3
        bullet_y = self.pos.y + self.height

        middle_direction = Vector2(0, 1)
        left_outer_direction = middle_direction.rotate(-BOSS_DOUBLE_SPREAD_ANGLE)
        left_inner_direction = middle_direction.rotate(-BOSS_SPREAD_ANGLE)
        right_inner_direction = middle_direction.rotate(BOSS_SPREAD_ANGLE)
        right_outer_direction = middle_direction.rotate(BOSS_DOUBLE_SPREAD_ANGLE)


        bullets = [
            BossBullet(bullet_x, bullet_y, left_outer_direction * BOSS_BULLET_SPEED),
            BossBullet(bullet_x, bullet_y, left_inner_direction * BOSS_BULLET_SPEED),
            BossBullet(bullet_x, bullet_y, middle_direction * BOSS_BULLET_SPEED),
            BossBullet(bullet_x, bullet_y, right_inner_direction * BOSS_BULLET_SPEED),
            BossBullet(bullet_x, bullet_y, right_outer_direction * BOSS_BULLET_SPEED)
        ]

        self.shoot_timer = BOSS_SHOOT_COOLDOWN
        return bullets

    def draw(self,screen):
        if self.image:
            screen.blit(self.image, (self.pos.x, self.pos.y))
        else:
            pygame.draw.rect(screen, (180, 0, 180), (self.pos.x, self.pos.y, self.width, self.height))


class Bullet:
    def __init__(self,x,y,velocity,width,height,color,damage,owner,image_path=None):
        self.pos=Vector2(x,y)
        self.velocity=velocity
        self.width=width
        self.height=height
        self.color=color
        self.damage=damage
        self.owner=owner

        if image_path:
            self.image = load_scaled_image(image_path, self.width, self.height)
        else:
            self.image = None


    def update(self):
        self.pos+=self.velocity

    def draw(self,screen):
        if self.image:
            screen.blit(self.image, (self.pos.x, self.pos.y))
        else:
            pygame.draw.rect(screen,self.color,(self.pos.x,self.pos.y,self.width,self.height))

    def is_off_screen(self):
        return (
                self.pos.y+self.height<0 or
                self.pos.y+self.height>HEIGHT or
                self.pos.x<0 or self.pos.x>WIDTH
        )

class PlayerBullet(Bullet):
    def __init__(self,x,y,velocity):
        super().__init__(
            x=x,
            y=y,
            velocity=velocity,
            width=6,
            height=15,
            color=(255,255,0),
            damage=1,
            owner="player",
            image_path = PLAYER_BULLET_IMAGE_PATH
        )

class EnemyBullet(Bullet):
    def __init__(self,x,y,velocity):
        super().__init__(
            x=x,
            y=y,
            velocity=velocity,
            width=6,
            height=15,
            color=(255, 0, 0),
            damage=1,
            owner="enemy",
        image_path = ENEMY_BULLET_IMAGE_PATH
        )

class BossBullet(Bullet):
    def __init__(self,x,y,velocity):
        super().__init__(
            x=x,
            y=y,
            velocity=velocity,
            width=6,
            height=15,
            color=(255, 0, 0),
            damage=BOSS_BULLET_DAMAGE,
            owner="boss",
        image_path = BOSS_BULLET_IMAGE_PATH
        )




