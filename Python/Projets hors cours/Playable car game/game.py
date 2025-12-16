import math
import pygame
import time

# --- Entities --------------------------------------------------------------
class Entity:
    def __init__(self, pos, hittable):
        # pos and prev_pos are floats for smooth interpolation
        self.pos = [float(pos[0]), float(pos[1])]
        self.prev_pos = [float(pos[0]), float(pos[1])]
        self.rotation = 0.0  # degrees
        self.hittable = hittable

    def tick_prepare(self):
        # called before we start ticking: save previous state for interpolation
        self.prev_pos[0] = self.pos[0]
        self.prev_pos[1] = self.pos[1]

    def is_hittable(self):
        return self.hittable

    def set_rotation(self, rotation):
        self.rotation = rotation


class Car(Entity):
    def __init__(self, pos, hittable, speed=0.0):
        super().__init__(pos, hittable)
        self.speed = float(speed)             # pixels per second
        self.turn_speed = 120.0               # degrees per second
        self.accel = 200.0                    # pixels per second^2
        self.friction = 100.0                 # pixels per second^2
        self.size = (50, 30)                  # width, height for drawing

    def tick(self, dt, controls):
        # controls: dict with booleans 'left', 'right', 'up', 'down'
        # apply rotation
        if controls.get('left'):
            self.rotation += self.turn_speed * dt
        if controls.get('right'):
            self.rotation -= self.turn_speed * dt

        # apply forward / backward acceleration
        if controls.get('up'):
            # increase forward speed
            self.speed += self.accel * dt
        elif controls.get('down'):
            # reverse acceleration / brake
            self.speed -= self.accel * dt
        else:
            # apply friction towards 0
            if self.speed > 0:
                self.speed = max(0.0, self.speed - self.friction * dt)
            elif self.speed < 0:
                self.speed = min(0.0, self.speed + self.friction * dt)

        # compute displacement from speed & rotation
        rad = math.radians(self.rotation)
        dx = math.cos(rad) * self.speed * dt
        dy = -math.sin(rad) * self.speed * dt  # pygame's y grows downwards
        self.pos[0] += dx
        self.pos[1] += dy

    def draw(self, surface, alpha):
        # interpolate position for smooth rendering
        x = self.prev_pos[0] + (self.pos[0] - self.prev_pos[0]) * alpha
        y = self.prev_pos[1] + (self.pos[1] - self.prev_pos[1]) * alpha

        w, h = self.size
        car_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        car_surf.fill((200, 50, 50))
        # draw a "window" rectangle to see rotation orientation
        pygame.draw.rect(car_surf, (50, 50, 200), (w*0.6, h*0.2, w*0.25, h*0.6))

        rotated = pygame.transform.rotate(car_surf, self.rotation)
        rect = rotated.get_rect(center=(x, y))
        surface.blit(rotated, rect.topleft)


# --- Game -----------------------------------------------------------------
class Game:
    def __init__(self, screen_size=(800, 600), tick_rate=30, frame_rate=60):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Playable 2D Car Game")
        self.clock = pygame.time.Clock()

        self.entities = []
        self.tick_rate = tick_rate
        self.tick_dt = 1.0 / self.tick_rate
        self.frame_rate = frame_rate  # target FPS (0 or None to uncapped)

        # input state
        self.controls = {'left': False, 'right': False, 'up': False, 'down': False}

        # stats for debug
        self._last_fps_update = time.perf_counter()
        self._frame_counter = 0
        self._current_fps = 0

    def add_entity(self, entity):
        self.entities.append(entity)

    def add_car(self, pos, hittable, speed=0.0):
        car = Car(pos, hittable, speed)
        self.add_entity(car)
        return car

    def handle_events(self):
        # process pygame events and update input state
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_LEFT:
                    self.controls['left'] = True
                if event.key == pygame.K_RIGHT:
                    self.controls['right'] = True
                if event.key == pygame.K_UP:
                    self.controls['up'] = True
                if event.key == pygame.K_DOWN:
                    self.controls['down'] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.controls['left'] = False
                if event.key == pygame.K_RIGHT:
                    self.controls['right'] = False
                if event.key == pygame.K_UP:
                    self.controls['up'] = False
                if event.key == pygame.K_DOWN:
                    self.controls['down'] = False
        # keep running
        return True

    def tick(self, dt):
        # prepare entities for interpolation
        for e in self.entities:
            e.tick_prepare()

        # update physics / logic on fixed timestep
        for e in self.entities:
            if isinstance(e, Car):
                e.tick(dt, self.controls)
            # other entity types could be updated here

    def render(self, interpolation_alpha):
        self.screen.fill((30, 30, 30))
        for e in self.entities:
            if isinstance(e, Car):
                e.draw(self.screen, interpolation_alpha)
        pygame.display.flip()

    def update_fps_title(self):
        # update FPS shown in title every ~0.5s
        now = time.perf_counter()
        self._frame_counter += 1
        if now - self._last_fps_update >= 0.5:
            self._current_fps = self._frame_counter / (now - self._last_fps_update)
            pygame.display.set_caption(f"Playable 2D Car Game - FPS: {self._current_fps:.1f}")
            self._last_fps_update = now
            self._frame_counter = 0

    def loop(self):
        running = True
        last_time = time.perf_counter()
        accumulator = 0.0

        while running:
            # time management
            now = time.perf_counter()
            elapsed = now - last_time
            last_time = now
            accumulator += elapsed

            # events (handled once per frame)
            if not self.handle_events():
                running = False
                break

            # fixed timestep updates
            while accumulator >= self.tick_dt:
                self.tick(self.tick_dt)
                accumulator -= self.tick_dt

            # compute interpolation amount for rendering
            alpha = accumulator / self.tick_dt if self.tick_dt > 0 else 0.0
            self.render(alpha)

            # update FPS title occasionally
            self.update_fps_title()

            # cap frame rate if desired (0 or None for uncapped)
            if self.frame_rate and self.frame_rate > 0:
                self.clock.tick(self.frame_rate)
            else:
                self.clock.tick()

        pygame.quit()


# --- Runner ---------------------------------------------------------------
if __name__ == "__main__":
    game = Game(screen_size=(1024, 768), tick_rate=30, frame_rate=60)
    car = game.add_car(pos=[512, 384], hittable=True, speed=0.0)
    game.loop()