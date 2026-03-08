import random
import tkinter as tk


WIDTH = 600
HEIGHT = 700
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 24
ENEMY_WIDTH = 32
ENEMY_HEIGHT = 22
PLAYER_SPEED = 12
BULLET_SPEED = 14
ENEMY_BULLET_SPEED = 7
ENEMY_STEP_X = 14
ENEMY_STEP_Y = 24


class InvaderGame:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Python Invader Game")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#0d1021", highlightthickness=0)
        self.canvas.pack()

        self.score = 0
        self.lives = 3
        self.level = 1
        self.running = True

        self.score_text = self.canvas.create_text(
            12,
            12,
            anchor="nw",
            fill="#f8f8f2",
            font=("Courier", 14, "bold"),
            text=self.status_text(),
        )

        self.keys_pressed: set[str] = set()
        self.player = self.canvas.create_rectangle(
            WIDTH // 2 - PLAYER_WIDTH // 2,
            HEIGHT - 60,
            WIDTH // 2 + PLAYER_WIDTH // 2,
            HEIGHT - 60 + PLAYER_HEIGHT,
            fill="#50fa7b",
            outline="",
        )

        self.player_bullet: int | None = None
        self.enemy_bullets: list[int] = []
        self.enemies: list[int] = []
        self.enemy_direction = 1

        self.create_enemy_wave(rows=4, cols=10)
        self.bind_keys()
        self.game_loop()

    def status_text(self) -> str:
        return f"Score: {self.score}  Lives: {self.lives}  Level: {self.level}"

    def bind_keys(self) -> None:
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)

    def on_key_press(self, event: tk.Event) -> None:
        self.keys_pressed.add(event.keysym)
        if event.keysym == "space" and self.player_bullet is None and self.running:
            x1, y1, x2, y2 = self.canvas.coords(self.player)
            bullet_x = (x1 + x2) / 2
            self.player_bullet = self.canvas.create_rectangle(
                bullet_x - 2,
                y1 - 14,
                bullet_x + 2,
                y1,
                fill="#f1fa8c",
                outline="",
            )

    def on_key_release(self, event: tk.Event) -> None:
        self.keys_pressed.discard(event.keysym)

    def create_enemy_wave(self, rows: int, cols: int) -> None:
        self.enemies.clear()
        top_margin = 90
        left_margin = 80
        h_gap = 44
        v_gap = 36

        colors = ["#ff79c6", "#8be9fd", "#bd93f9", "#ffb86c"]

        for row in range(rows):
            for col in range(cols):
                x = left_margin + col * h_gap
                y = top_margin + row * v_gap
                enemy = self.canvas.create_rectangle(
                    x,
                    y,
                    x + ENEMY_WIDTH,
                    y + ENEMY_HEIGHT,
                    fill=colors[row % len(colors)],
                    outline="",
                )
                self.enemies.append(enemy)

    def move_player(self) -> None:
        if not self.running:
            return

        dx = 0
        if "Left" in self.keys_pressed:
            dx -= PLAYER_SPEED
        if "Right" in self.keys_pressed:
            dx += PLAYER_SPEED

        if dx == 0:
            return

        x1, _, x2, _ = self.canvas.coords(self.player)
        if x1 + dx < 10:
            dx = 10 - x1
        if x2 + dx > WIDTH - 10:
            dx = (WIDTH - 10) - x2

        self.canvas.move(self.player, dx, 0)

    def move_player_bullet(self) -> None:
        if self.player_bullet is None:
            return

        self.canvas.move(self.player_bullet, 0, -BULLET_SPEED)
        x1, y1, x2, y2 = self.canvas.coords(self.player_bullet)

        if y2 < 0:
            self.canvas.delete(self.player_bullet)
            self.player_bullet = None
            return

        for enemy in self.enemies[:]:
            if self.overlap((x1, y1, x2, y2), self.canvas.coords(enemy)):
                self.canvas.delete(enemy)
                self.enemies.remove(enemy)
                self.canvas.delete(self.player_bullet)
                self.player_bullet = None
                self.score += 100
                self.update_status()
                break

    def move_enemies(self) -> None:
        if not self.enemies:
            self.level += 1
            self.update_status()
            self.create_enemy_wave(rows=min(6, 3 + self.level), cols=10)
            return

        xs = [self.canvas.coords(enemy)[0] for enemy in self.enemies]
        xe = [self.canvas.coords(enemy)[2] for enemy in self.enemies]

        shift_down = False
        if max(xe) >= WIDTH - 12 and self.enemy_direction == 1:
            self.enemy_direction = -1
            shift_down = True
        elif min(xs) <= 12 and self.enemy_direction == -1:
            self.enemy_direction = 1
            shift_down = True

        dx = self.enemy_direction * (ENEMY_STEP_X + self.level // 2)
        dy = ENEMY_STEP_Y if shift_down else 0

        for enemy in self.enemies:
            self.canvas.move(enemy, dx, dy)
            _, y1, _, y2 = self.canvas.coords(enemy)
            if y2 >= HEIGHT - 75:
                self.game_over("INVADERS WIN")
                return

    def enemy_fire(self) -> None:
        if not self.running or not self.enemies:
            return

        fire_chance = min(0.03 + self.level * 0.004, 0.1)
        if random.random() > fire_chance:
            return

        enemy = random.choice(self.enemies)
        x1, y1, x2, y2 = self.canvas.coords(enemy)
        bullet_x = (x1 + x2) / 2
        bullet = self.canvas.create_rectangle(
            bullet_x - 2,
            y2,
            bullet_x + 2,
            y2 + 12,
            fill="#ff5555",
            outline="",
        )
        self.enemy_bullets.append(bullet)

    def move_enemy_bullets(self) -> None:
        player_box = self.canvas.coords(self.player)

        for bullet in self.enemy_bullets[:]:
            self.canvas.move(bullet, 0, ENEMY_BULLET_SPEED + self.level // 3)
            x1, y1, x2, y2 = self.canvas.coords(bullet)

            if y1 > HEIGHT:
                self.canvas.delete(bullet)
                self.enemy_bullets.remove(bullet)
                continue

            if self.overlap((x1, y1, x2, y2), player_box):
                self.canvas.delete(bullet)
                self.enemy_bullets.remove(bullet)
                self.lives -= 1
                self.update_status()
                if self.lives <= 0:
                    self.game_over("GAME OVER")
                break

    @staticmethod
    def overlap(a: tuple[float, float, float, float], b: list[float]) -> bool:
        ax1, ay1, ax2, ay2 = a
        bx1, by1, bx2, by2 = b
        return not (ax2 < bx1 or ax1 > bx2 or ay2 < by1 or ay1 > by2)

    def update_status(self) -> None:
        self.canvas.itemconfigure(self.score_text, text=self.status_text())

    def game_over(self, message: str) -> None:
        self.running = False
        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2,
            fill="#f8f8f2",
            font=("Courier", 36, "bold"),
            text=message,
        )
        self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2 + 46,
            fill="#f8f8f2",
            font=("Courier", 16),
            text="Press Esc to quit",
        )
        self.root.bind("<Escape>", lambda _event: self.root.destroy())

    def game_loop(self) -> None:
        if self.running:
            self.move_player()
            self.move_player_bullet()
            self.move_enemies()
            self.enemy_fire()
            self.move_enemy_bullets()
        self.root.after(40, self.game_loop)


def main() -> None:
    root = tk.Tk()
    InvaderGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
