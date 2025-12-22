# IMPORTS
import random
import pygame
import os
import math

# CONSTANTS
SIZE_MAP = 11
NUMBER_DEFAULT = 0
NUMBER_COFFRE = 1
NUMBER_GOUFFRE = -1
TILE_SIZE = 20 # Pixel
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# CLASS GAME
class Game:
    def __init__(self, screen_coef=60, fps=60):
        self.screen_size = (16 * screen_coef, 9 * screen_coef)
        self.debug(f"screen size {self.screen_size}")

        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Chasse au trésor Zig et Sharko")

        pygame.init()
        self.clock = pygame.time.Clock()

        self.fps = fps
        self.debug(f"FPS {self.fps}")
        self.controls = {}
        self.pressed = {}

        self.MENU = "starting"
        self.GAME = "game"
        self.WIN = "win"
        self.LOOSE = "loose"

        self.state = self.MENU

        coef = 4
        self.TILE_W = 70 * coef
        self.TILE_H = 30 * coef

        self.grid_offset_x = 0
        self.grid_offset_y = 0
        self.PERSPECTIVE = 100

        self.SPACE_BETWEEN = 50
        self.ROW_DEPTH = self.SPACE_BETWEEN

        self.base_offset_x = self.screen_size[0] // 2 - (self.TILE_W - self.SPACE_BETWEEN - self.PERSPECTIVE // 2) // 2
        self.base_offset_y = self.screen_size[1] // 2

        self.annimation_level = 15
        self.init_img()

    # INIT FUNC
    def init_var(self):
        self.grid = self.new_grid()

        self.pos_player = (len(self.grid) - 1, len(self.grid) // 2)
        self.pos_discovered = set()
        self.old_pos = tuple(self.pos_player)
        self.annimation_state = self.annimation_level
        self.can_move = True
        pass

    def init_img(self):
        self.menu_image = pygame.image.load(
            os.path.join(ASSETS_DIR, "start_screen.jpg")
        ).convert_alpha()
        self.menu_image = pygame.transform.scale(self.menu_image, self.screen_size)
        self.menu_rect = self.menu_image.get_rect(
            center=self.screen.get_rect().center
        )

        self.font = pygame.font.Font(None, 36)
        self.menu_text = self.font.render(
            "Press SPACE to start", True, (255, 255, 255)
        )
        self.menu_text_rect = self.menu_text.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() - 50)
        )

        self.zig_wait_img = pygame.image.load(
            os.path.join(ASSETS_DIR, "zig_wait.png")
        ).convert_alpha()

        self.zig_wait_img = pygame.transform.scale(
            self.zig_wait_img,
            (self.TILE_H * 1.5, self.TILE_W)
        )

        self.zig_wait_rect = self.zig_wait_img.get_rect(
            center=self.screen.get_rect().center
        )

        self.zig_walk_img = pygame.image.load(
            os.path.join(ASSETS_DIR, "zig_walk.png")
        ).convert_alpha()

        self.zig_walk_img = pygame.transform.scale(
            self.zig_walk_img,
            (self.TILE_H * 1.5, self.TILE_W)
        )

        self.zig_walk_rect = self.zig_walk_img.get_rect(
            center=self.screen.get_rect().center
        )

        self.zig_walk_reverse_img = pygame.transform.flip(
            self.zig_walk_img,
            True,
            False
        )

    # FONCTION LOGIQUES
    def new_grid(self, size=SIZE_MAP):
        """
        Crée une nouvelle grille de jeu.
        Args:
            size (int): La taille de la grille (par défaut SIZE_MAP).
        Returns:
            list: Une grille de taille SIZE_MAP x SIZE_MAP remplie de zéros.
        """
        grid = [[NUMBER_DEFAULT for _ in range(size)] for _ in range(size)]
        self.placerCoffres(grid)
        self.placerGouffres(grid)
        return grid

    def placerGouffres(self, grille, nombre_gouffres=10, value=-1):
        """
        Place des gouffres aléatoirement dans la grille.
        Args:
            grille (list): La grille de jeu.
            nombre_gouffres (int): Le nombre de gouffres à placer.
        """
        size = len(grille)
        placed = 0
        while placed < nombre_gouffres:
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
            if grille[x][y] == NUMBER_DEFAULT:
                grille[x][y] = value
                placed += 1

    def placerCoffres(self, grille, nombre_coffres=3, value=1, size_coffres=2):
        """
        Place des coffres aléatoirement dans la grille.
        Args:
            grille (list): La grille de jeu.
            nombre_coffres (int): Le nombre de gouffres à placer.
        """
        size = len(grille)
        placed = 0
        while placed < nombre_coffres:
            can_place = True

            x = random.randint(0, size - 2)
            y = random.randint(0, size - 2)
            for _ in range(size_coffres):
                if grille[x][y] != NUMBER_DEFAULT or grille[x + _][y] != NUMBER_DEFAULT or grille[x][y + _] != NUMBER_DEFAULT or grille[x + _][y + _] != NUMBER_DEFAULT:
                    can_place = False

            if can_place:
                for _ in range(size_coffres):
                    grille[x + _][y] = value
                    grille[x][y + _] = value
                    grille[x + _][y + _] = value
                placed += 1

    def afficherGrille(self, grille):
        """
        Affiche la grille de jeu dans la console.
        Args:
            grille (list): La grille à afficher.
        """
        for i in range(len(grille)):
            print("-" * (len(grille[i]) * 4 + 1), i)
            for col_index, cell in enumerate(grille[i]):

                if (i, col_index) == self.pos_player:
                    print(f"| P ", end="")
                elif (i, col_index) in self.pos_discovered:
                    if cell == NUMBER_COFFRE:
                        print("| C ", end="")
                    elif cell == NUMBER_GOUFFRE:
                        print("| G ", end="")
                    else:
                        print("|   ", end="")
                else:
                    print("| ? ", end="")

            print("|")
        print("-" * (len(grille[0]) * 4 + 1))

    # JEU
    def render(self):
        self.screen.fill((30, 30, 30))
        if self.state == self.MENU:
            self.screen.blit(self.menu_image, self.menu_rect)

            alpha = int(128 + 127 * math.sin(pygame.time.get_ticks() * 0.005))
            text = self.menu_text.copy()
            text.set_alpha(alpha)
            self.screen.blit(text, self.menu_text_rect)
        elif self.state == self.GAME:

            self.screen.fill((150, 255, 240))
            self.draw_grid_perspective()
            
            if self.can_move:
                self.screen.blit(self.zig_wait_img, self.zig_wait_rect)
            else:
                self.screen.blit(self.zig_walk_img, self.zig_walk_rect)

        pygame.display.flip()

    def draw_grid_perspective(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.draw_void(x, y)

                color = (0, 180, 0)
                
                if self.is_discovered((y, x)):
                    if self.grid[y][x] == -1:
                        color = (180, 0, 0)
                    elif self.grid[y][x] == 1:
                        color = (0, 0, 180)
                    else:  
                        color = (150, 130, 90)
                self.draw_tile_perspective(x, y, color)

    def draw_tile_perspective(self, x, y, color=(0, 180, 0)):
        ox = self.grid_offset_x
        oy = self.grid_offset_y

        px = ox + x * self.TILE_W + x * self.SPACE_BETWEEN
        py = oy + y * (self.TILE_H + self.ROW_DEPTH)

        top_w = self.TILE_W
        bottom_w = self.TILE_W - self.PERSPECTIVE

        poly = [
            (px, py),
            (px + top_w, py),
            (px + bottom_w, py + self.TILE_H),
            (px + (bottom_w - top_w), py + self.TILE_H),
        ]

        pygame.draw.polygon(self.screen, color, poly)
        pygame.draw.polygon(self.screen, (0, 100, 0), poly, 1)

    def draw_void(self, x, y):
        ox = self.grid_offset_x
        oy = self.grid_offset_y

        px = ox + x * self.TILE_W + x * self.SPACE_BETWEEN
        py = oy + y * (self.TILE_H + self.ROW_DEPTH) + self.TILE_H

        shadow_b = [
            (px - self.PERSPECTIVE, py),
            (px + self.TILE_W - self.PERSPECTIVE, py),
            (px + self.TILE_W - self.PERSPECTIVE, py + self.TILE_H + self.ROW_DEPTH),
            (px - self.PERSPECTIVE, py + self.TILE_H + self.ROW_DEPTH),
        ]

        pygame.draw.polygon(self.screen, (30, 90, 30), shadow_b)

        px = ox + x * self.TILE_W + x * self.SPACE_BETWEEN
        py = oy + y * (self.TILE_H + self.ROW_DEPTH)

        shadow_r = [
            (px + self.TILE_W, py),
            (px + self.TILE_W, py + self.TILE_H + self.ROW_DEPTH),
            (px + self.TILE_W - self.PERSPECTIVE, py + self.TILE_H * 2 + self.ROW_DEPTH),
            (px + self.TILE_W - self.PERSPECTIVE, py + self.TILE_H),
        ]

        pygame.draw.polygon(self.screen, (30, 140, 30), shadow_r)

    def is_discovered(self, pos):
        for pos_d in self.pos_discovered:
            if pos_d == pos:
                return True
        return False    

    def update(self, dt):
        if self.state == self.MENU:
            if self.is_press("space"):
                self.state = self.GAME

                self.init_var()
        if self.state == self.GAME:
            if self.can_move:
                if self.is_press("down"):
                    self.pressed["down"] = True
                else:
                    if self.pressed.get("down", False):
                        self.pos_player = (min(SIZE_MAP - 1, self.pos_player[0] + 1), self.pos_player[1])
                    self.pressed["down"] = False

                if self.is_press("up"):
                    self.pressed["up"] = True
                else:
                    if self.pressed.get("up", False):
                        self.pos_player = (max(0, self.pos_player[0] - 1), self.pos_player[1])
                    self.pressed["up"] = False
                    
                if self.is_press("right"):
                    self.pressed["right"] = True
                else:
                    if self.pressed.get("right", False):
                        self.pos_player = (self.pos_player[0], min(SIZE_MAP - 1, self.pos_player[1] + 1))
                    self.pressed["right"] = False
                    
                if self.is_press("left"):
                    self.pressed["left"] = True
                else:
                    if self.pressed.get("left", False):
                        self.pos_player = (self.pos_player[0], max(0, self.pos_player[1] - 1))
                    self.pressed["left"] = False

                if self.is_press("space"):
                    self.pressed["space"] = True
                else:
                    if self.pressed.get("space", False):
                        self.pos_discovered.add(self.pos_player)
                    self.pressed["space"] = False

            self.set_to()
                
    def set_to(self):
        if self.old_pos != self.pos_player:
            self.can_move = False

            if self.annimation_state > 0:
                t = (self.annimation_level - self.annimation_state) / self.annimation_level

                y_start = self.old_pos[0] * (self.TILE_H + self.ROW_DEPTH)
                x_start = self.old_pos[1] * (self.TILE_W + self.SPACE_BETWEEN)

                y_target = self.pos_player[0] * (self.TILE_H + self.ROW_DEPTH)
                x_target = self.pos_player[1] * (self.TILE_W + self.SPACE_BETWEEN)

                y_offent = y_start + (y_target - y_start) * t
                x_offent = x_start + (x_target - x_start) * t

                self.annimation_state -= 1
            else:
                y_offent = self.pos_player[0] * (self.TILE_H + self.ROW_DEPTH)
                x_offent = self.pos_player[1] * (self.TILE_W + self.SPACE_BETWEEN)

                self.old_pos = tuple(self.pos_player)
                self.annimation_state = self.annimation_level


            self.grid_offset_x = -x_offent + self.base_offset_x
            self.grid_offset_y = -y_offent + self.base_offset_y
        else:
            y_offent = self.pos_player[0] * (self.TILE_H + self.ROW_DEPTH)
            x_offent = self.pos_player[1] * (self.TILE_W + self.SPACE_BETWEEN)

            self.grid_offset_x = -x_offent + self.base_offset_x
            self.grid_offset_y = -y_offent + self.base_offset_y

            self.can_move = True
        pass
    
    # EVENT PYGAME
    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                if event.key == pygame.K_LEFT:
                    self.controls['left'] = True
                if event.key == pygame.K_RIGHT:
                    self.controls['right'] = True
                if event.key == pygame.K_UP:
                    self.controls['up'] = True
                if event.key == pygame.K_DOWN:
                    self.controls['down'] = True
                if event.key == pygame.K_SPACE:
                    self.controls['space'] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.controls['left'] = False
                if event.key == pygame.K_RIGHT:
                    self.controls['right'] = False
                if event.key == pygame.K_UP:
                    self.controls['up'] = False
                if event.key == pygame.K_DOWN:
                    self.controls['down'] = False
                if event.key == pygame.K_SPACE:
                    self.controls['space'] = False

    def is_press(self, key):
        return self.controls.get(key, False)

    # START GAME
    def start(self):
        running = True
        while running:
            if self.handle_event():
                running = False
                self.debug("Exit game")
                break
            
            dt = self.clock.tick(60)
            self.update(dt)

            self.render()
            self.clock.tick(self.fps)
        pygame.quit()

    #DEBUG FUNC
    def debug(self, line :str):
        print(f"[DEBUG] {line}")

if __name__ == "__main__":
    game = Game(60)
    game.start()