import random
from pygame.math import Vector2
from settings import *
from entities import Boss


#敌人出现控制
def spawn_enemy(score):
    probability=ENEMY_SPAWN_RATE+score*0.0004
    probability=min(probability,0.05)
    return random.random()<probability

#碰撞函数
def is_collision(obj1,obj2):
    return (obj1.pos.x < obj2.pos.x + obj2.width and
            obj1.pos.x + obj1.width > obj2.pos.x and
            obj1.pos.y < obj2.pos.y + obj2.height and
            obj1.pos.y + obj1.height > obj2.pos.y)

#玩家射击系统
def player_shoot(player, mouse_pos, player_bullets):
    """玩家朝鼠标方向射击"""

    if player.shoot_timer > 0:
        return

    bullet_x = player.pos.x + player.width // 2 - 3
    bullet_y = player.pos.y

    direction = Vector2(mouse_pos[0], mouse_pos[1]) - Vector2(bullet_x, bullet_y)

    if direction.length() != 0:
        direction = direction.normalize()
        bullets = player.shoot(direction)

        for bullet in bullets:
            player_bullets.append(bullet)

            player.shoot_timer = player.shoot_cooldown

#敌人射击系统
def enemy_shoot_at_player(enemy, player, enemy_bullets):
    start_x = enemy.pos.x + enemy.width // 2
    start_y = enemy.pos.y + enemy.height // 2
    target_x = player.pos.x + player.width // 2
    target_y = player.pos.y + player.height // 2
    direction = Vector2(target_x - start_x, target_y - start_y)
    if direction.length() != 0:
        bullet = enemy.shoot(direction.normalize())
        if bullet:
            enemy_bullets.append(bullet)

class GameManager:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.next_level_score = 20

        self.boss_spawned = False
        self.game_win = False

    def add_score(self, amount):
        self.score += amount

    def check_level_up(self, player):
        if self.level<4 and self.score >= self.next_level_score:
            self.level += 1
            self.next_level_score += 20
            self.apply_upgrade(player)

    def apply_upgrade(self, player):
        player.shoot_cooldown = max(
            8, int(player.shoot_cooldown*0.7)
        )

        player.invincible_timer=120

        if self.level==3:
            player.bullet_count=2

        elif self.level==4:
            player.bullet_count=3

        print("当前等级:", self.level, "当前子弹数:", player.bullet_count)


def spawn_boss():
    return Boss()