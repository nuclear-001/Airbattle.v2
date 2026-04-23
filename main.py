#库调用
import pygame
import random
from settings import *
from entities import Player,Enemy
from entities import PlayerBullet,EnemyBullet
from systems import is_collision,spawn_enemy
from systems import player_shoot, enemy_shoot_at_player
from systems import GameManager,spawn_boss
from pygame.math import Vector2



# 初始化
pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
clock=pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

def draw_center_text(text, y, size=48):

    font_big = pygame.font.SysFont(None, size)

    text_surface = font_big.render(text, True, WHITE)

    text_rect = text_surface.get_rect(center=(WIDTH//2, y))

    screen.blit(text_surface, text_rect)


background_img = pygame.image.load(BACKGROUND_IMAGE_PATH).convert()
background_img = pygame.transform.scale(background_img,(WIDTH,HEIGHT))

# 创建对象
player=Player()
game = GameManager()
enemies=[]
player_bullets=[]
enemy_bullets=[]
boss_bullets=[]

boss=None
game_over=False
game_win=False
game_state="start"


# 主循环
running=True
while running:
    clock.tick(FPS)

    # ==============事件抓取==============
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        if game_state=="start":
            if event.type==pygame.MOUSEBUTTONDOWN:
                game_state="playing"

        elif game_state=="playing":

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    player_shoot(
                        player,
                        pygame.mouse.get_pos(),
                        player_bullets
                    )

        elif game_state == "game_over":

            if event.type == pygame.MOUSEBUTTONDOWN:

                player = Player()
                game = GameManager()

                enemies.clear()
                player_bullets.clear()
                enemy_bullets.clear()
                boss_bullets.clear()

                boss = None

                game_state = "playing"


            elif game_state == "win":

                if event.type == pygame.MOUSEBUTTONDOWN:
                    player = Player()
                    game = GameManager()

                    enemies.clear()
                    player_bullets.clear()
                    enemy_bullets.clear()
                    boss_bullets.clear()

                    boss = None

                    game_state = "playing"



    if game_state=="playing":
        keys=pygame.key.get_pressed()
        player.move(keys)

        # ================== 玩家状态更新 ==================
        if player.shoot_timer > 0:
            player.shoot_timer-=1

        if player.invincible_timer > 0:
            player.invincible_timer -= 1

        # ================Boss触发====================
        if game.score>=BOSS_UNLOCK_SCORE and not game.boss_spawned:
            enemies.clear()
            enemy_bullets.clear()
            boss = spawn_boss()
            game.boss_spawned = True


        # ================== 敌人生成 ==================
        if not game.boss_spawned:
            if spawn_enemy(game.score):
                enemies.append(Enemy())



        # ===========玩家子弹更新===========
        for bullet in player_bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                player_bullets.remove(bullet)

        # =========敌人子弹更新===========
        for bullet in enemy_bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                enemy_bullets.remove(bullet)

        # ==========boss子弹更新===========
        for bullet in boss_bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                boss_bullets.remove(bullet)



        for enemy in enemies[:]:#敌人更新
            enemy.update()

        # ================== Boss更新 ==================
        if boss:
            boss.update()

            new_bullets = boss.shoot()
            for bullet in new_bullets:
                boss_bullets.append(bullet)

        for enemy in enemies:#敌人射击
            enemy_shoot_at_player(enemy, player, enemy_bullets)


        # ============玩家子弹射击敌人============
        for bullet in player_bullets[:]:
            for enemy in enemies[:]:
                if is_collision(bullet, enemy):
                    if bullet in player_bullets:
                        player_bullets.remove(bullet)
                    if enemy in enemies:
                        enemies.remove(enemy)
                    game.add_score(2)
                    break

        # ===========玩家子弹打boss===============
        if boss:
            for bullet in player_bullets[:]:
                if is_collision(bullet, boss):
                    if bullet in player_bullets:
                        player_bullets.remove(bullet)

                    boss.hp -= bullet.damage

                    if boss.hp <= 0:
                        boss = None
                        game_state = "win"

                    break

        # =============敌人子弹射击玩家==============
        for bullet in enemy_bullets[:]:
            if is_collision(bullet, player):

                if player.invincible_timer ==0:
                    player.hp-=2

                if bullet in enemy_bullets:
                    enemy_bullets.remove(bullet)

                if player.hp<=0:
                    running=False

        # ==========boss子弹打玩家=============
        for bullet in boss_bullets[:]:
            if is_collision(bullet, player):

                if player.invincible_timer == 0:
                    player.hp -= bullet.damage

                if bullet in boss_bullets:
                    boss_bullets.remove(bullet)

                if player.hp <= 0:
                    game_state = "game_over"

        # =============敌人撞击玩家=============
        for enemy in enemies[:]:
            if is_collision(enemy,player):
                if player.invincible_timer == 0:
                    player.hp-=10
                    player.invincible_timer = 60
                    enemies.remove(enemy)
                if player.hp <= 0:
                    game_state = "game_over"


        # ================== 升级检测 ==================
        game.check_level_up(player)



    # 绘制
    screen.blit(background_img, (0, 0))
    player.draw(screen)

    # ============敌人绘制============
    for enemy in enemies[:]:
        enemy.draw(screen)

    # =======绘制boss=========
    if boss:
        boss.draw(screen)

    # ============玩家子弹绘制============
    for bullet in player_bullets[:]:
        bullet.draw(screen)
    # =========敌人子弹绘制==========
    for bullet in enemy_bullets[:]:
        bullet.draw(screen)

    # =========绘制敌人子弹==========
    for bullet in boss_bullets[:]:
        bullet.draw(screen)

    # ================= 状态界面 =================

    if game_state == "start":

        screen.blit(background_img, (0, 0))

        draw_center_text("AIR BATTLE", 200, 60)

        draw_center_text("Click to Start", 320, 36)


    elif game_state == "game_over":

        screen.blit(background_img, (0, 0))

        draw_center_text("GAME OVER", 220, 60)

        draw_center_text(f"Score: {game.score}", 300, 40)

        draw_center_text("Click to Restart", 380, 32)


    elif game_state == "win":

        screen.blit(background_img, (0, 0))

        draw_center_text("YOU WIN", 220, 60)

        draw_center_text("Boss Defeated!", 300, 40)

        draw_center_text("Click to Restart", 380, 32)

    # ================== UI ==================
    score_text = font.render(f"Score: {game.score}", True, WHITE)
    level_text = font.render(f"Lv: {game.level}", True, WHITE)
    hp_text = font.render(f"HP: {player.hp}", True, WHITE)

    if boss:
        boss_hp_text = font.render(f"Boss HP: {boss.hp}", True, WHITE)
        screen.blit(boss_hp_text, (10, 100))

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))
    screen.blit(hp_text, (10, 70))

    pygame.display.update()

pygame.quit()





