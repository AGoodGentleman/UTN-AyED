"""Rogue Fortress.
Controles:
- WASD o flechas: mover/atacar.
- E o Espacio: hablar con un mercader si esta cerca.
- 1, 2, 3: comprar en la tienda.
- ESC: volver/cerrar pantalla actual.
- TAB: ver referencias.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from random import Random
from typing import Iterable

try:
    import pygame
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Pygame no esta instalado. Instalalo con: py -m pip install pygame"
    ) from exc


Position = tuple[int, int]
Color = tuple[int, int, int]


MAP_SIZE = 100
VIEW_SIZE = 12
TILE_SIZE = 48
GRID_LEFT = 32
GRID_TOP = 104
GRID_PIXELS = VIEW_SIZE * TILE_SIZE
PANEL_LEFT = GRID_LEFT + GRID_PIXELS + 24
PANEL_WIDTH = 336
WINDOW_WIDTH = PANEL_LEFT + PANEL_WIDTH + 32
WINDOW_HEIGHT = GRID_TOP + GRID_PIXELS + 40
FPS = 60

STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_SHOP = "shop"
STATE_WIN = "win"
STATE_LOSE = "lose"

TIER_EASY = "facil"
TIER_MEDIUM = "medio"
TIER_BOSS = "jefe"

MAX_PLAYER_HP = 100
STARTING_GOLD = 100
ENEMY_AGGRO_RADIUS = 7
REQUIRED_NORMAL_KILLS = 20
GENERATED_EASY_ENEMIES = 20
GENERATED_MEDIUM_ENEMIES = 20
MERCHANT_COUNT = 3

WEAPON_NAMES = ["Daga", "Espada corta", "Lanza reforzada", "Hoja runica"]
WEAPON_DAMAGE = [(10, 20), (20, 30), (30, 40), (40, 50)]
WEAPON_COSTS = [100, 200, 300]

ARMOR_NAMES = ["Ropa comun", "Cuero", "Cota de malla", "Placas"]
ARMOR_BLOCK = [0, 6, 8, 10]
ARMOR_COSTS = [150, 300, 450]

HEAL_COST = 50
HEAL_AMOUNT = 25
PASSIVE_HEAL_AMOUNT = 1
PASSIVE_HEAL_EVERY_STEPS = 3
PASSIVE_HEAL_CAP = 50


COLORS: dict[str, Color] = {
    "background": (12, 16, 21),
    "panel": (22, 28, 36),
    "panel_light": (35, 43, 53),
    "text": (232, 235, 229),
    "muted": (151, 160, 169),
    "accent": (239, 190, 96),
    "danger": (221, 91, 86),
    "good": (104, 196, 127),
    "water": (49, 111, 164),
    "ground": (57, 70, 48),
    "forest": (40, 83, 52),
    "mountain": (93, 96, 104),
    "cave": (79, 67, 85),
    "house": (111, 78, 58),
    "grid": (74, 83, 89),
}


@dataclass(frozen=True)
class TileSpec:
    key: str
    symbol: str
    name: str
    walkable: bool
    foreground: Color
    background: Color


@dataclass(frozen=True)
class EnemyTemplate:
    name: str
    symbol: str
    tier: str
    hp_range: tuple[int, int]
    attack_range: tuple[int, int]
    reward_range: tuple[int, int]
    color: Color


@dataclass
class Enemy:
    name: str
    symbol: str
    tier: str
    position: Position
    hp: int
    max_hp: int
    attack_range: tuple[int, int]
    reward_range: tuple[int, int]
    color: Color


@dataclass
class Item:
    name: str
    symbol: str
    kind: str
    amount: int
    position: Position
    color: Color


@dataclass
class Player:
    position: Position
    hp: int = MAX_PLAYER_HP
    gold: int = STARTING_GOLD
    weapon_level: int = 0
    armor_level: int = 0
    has_amulet: bool = False
    score_bonus: int = 0

    @property
    def weapon_name(self) -> str:
        return WEAPON_NAMES[self.weapon_level]

    @property
    def armor_name(self) -> str:
        return ARMOR_NAMES[self.armor_level]

    @property
    def final_score(self) -> int:
        return max(self.hp, 0) + self.gold * 2 + self.score_bonus


@dataclass
class Button:
    rect: pygame.Rect
    text: str
    action: str


TILES: dict[str, TileSpec] = {
    "ground": TileSpec(
        "ground", ".", "Llanura", True, (180, 188, 168), COLORS["ground"]
    ),
    "forest": TileSpec(
        "forest", "↑", "Bosque", True, (97, 176, 105), COLORS["forest"]
    ),
    "water": TileSpec(
        "water", "≈", "Agua", False, (155, 202, 230), COLORS["water"]
    ),
    "mountain": TileSpec(
        "mountain", "^", "Montaña", False, (199, 201, 205), COLORS["mountain"]
    ),
    "cave": TileSpec(
        "cave", "∩", "Cueva", True, (201, 179, 230), COLORS["cave"]
    ),
    "house": TileSpec(
        "house", "⌂", "Casa", False, (230, 186, 129), COLORS["house"]
    ),
}


EASY_ENEMIES: tuple[EnemyTemplate, ...] = (
    EnemyTemplate("Rata", "r", TIER_EASY, (26, 34), (4, 8), (14, 23), (206, 143, 105)),
    EnemyTemplate("Murcielago", "b", TIER_EASY, (24, 32), (5, 9), (14, 24), (181, 127, 214)),
    EnemyTemplate("Slime", "s", TIER_EASY, (30, 40), (4, 7), (16, 27), (115, 211, 145)),
    EnemyTemplate("Lobo", "w", TIER_EASY, (34, 44), (6, 10), (19, 31), (210, 210, 185)),
    EnemyTemplate("No muerto", "z", TIER_EASY, (36, 46), (5, 10), (22, 35), (148, 197, 190)),
)

MEDIUM_ENEMIES: tuple[EnemyTemplate, ...] = (
    EnemyTemplate("Lobo alfa", "W", TIER_MEDIUM, (62, 74), (12, 18), (48, 70), (238, 220, 155)),
    EnemyTemplate("Mago", "ô", TIER_MEDIUM, (54, 68), (13, 20), (55, 80), (174, 159, 236)),
    EnemyTemplate("Caballero", "k", TIER_MEDIUM, (72, 88), (11, 17), (58, 84), (205, 211, 220)),
    EnemyTemplate("Asesino", "a", TIER_MEDIUM, (56, 70), (14, 22), (58, 90), (224, 118, 129)),
    EnemyTemplate("Elemental", "e", TIER_MEDIUM, (68, 82), (12, 20), (60, 92), (112, 201, 221)),
)

BOSS_TEMPLATE = EnemyTemplate(
    "Baldur",
    "B",
    TIER_BOSS,
    (165, 165),
    (20, 31),
    (190, 260),
    (255, 104, 96),
)

OMINOUS_MESSAGES: dict[int, str] = {
    10: "El mapa queda demasiado silencioso.",
    9: "Una presencia observa desde las cuevas.",
    8: "El aire se vuelve pesado.",
    7: "Las aguas golpean la costa con violencia.",
    6: "Algo antiguo despierta bajo la fortaleza.",
    5: "Baldur esta cerca.",
}

GOLD_PICKUP_MESSAGES: tuple[str, ...] = (
    "Encuentras una bolsa gastada. Oro +{amount}.",
    "Las monedas tintinean en tu mochila. Oro +{amount}.",
    "Rescatas oro entre el barro. Oro +{amount}.",
    "Un brillo delata unas monedas sueltas. Oro +{amount}.",
    "Guardas unas piezas antiguas. Oro +{amount}.",
)

TREASURE_PICKUP_MESSAGES: tuple[str, ...] = (
    "Abres un cofre olvidado. Oro +{amount}.",
    "Encuentras joyas de una expedicion perdida. Oro +{amount}.",
    "El tesoro pesa mas que una promesa. Oro +{amount}.",
    "Entre polvo y runas aparece una reliquia valiosa. Oro +{amount}.",
    "Saqueas un cadáver intacto. Oro +{amount}.",
)

HEALTH_PICKUP_MESSAGES: tuple[str, ...] = (
    "Bebes un tonico tibio. Vida +{amount}.",
    "Una venda limpia te devuelve el pulso. Vida +{amount}.",
    "Respiras hondo y sigues en pie. Vida +{amount}.",
    "Un pequeno altar calma tus heridas. Vida +{amount}.",
    "La energia vuelve a tus manos. Vida +{amount}.",
)


def clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def manhattan(a: Position, b: Position) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def neighbors4(position: Position) -> Iterable[Position]:
    x, y = position
    yield x + 1, y
    yield x - 1, y
    yield x, y + 1
    yield x, y - 1


class RogueFortress:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.rng = Random()
        self.running = True
        self.state = STATE_MENU
        self.world: list[list[str]] = []
        self.caves: list[Position] = []
        self.player = Player((MAP_SIZE // 2, MAP_SIZE // 2))
        self.enemies: list[Enemy] = []
        self.items: list[Item] = []
        self.merchant_positions: list[Position] = []
        self.boss_spawned = False
        self.boss_defeated = False
        self.normal_kills = 0
        self.announced_thresholds: set[int] = set()
        self.steps_since_passive_heal = 0
        self.show_help = False
        self.log: list[str] = []
        self.final_title = ""
        self.final_message = ""

        self.title_font = pygame.font.SysFont("consolas", 52, bold=True)
        self.subtitle_font = pygame.font.SysFont("consolas", 28, bold=True)
        self.body_font = pygame.font.SysFont("consolas", 20)
        self.small_font = pygame.font.SysFont("consolas", 16)
        self.tile_font = pygame.font.SysFont("consolas", 30, bold=True)

        self.menu_buttons = [
            Button(pygame.Rect(WINDOW_WIDTH // 2 - 110, 365, 220, 52), "Jugar", "play"),
            Button(pygame.Rect(WINDOW_WIDTH // 2 - 110, 435, 220, 52), "Salir", "quit"),
        ]
        self.end_buttons = [
            Button(pygame.Rect(WINDOW_WIDTH // 2 - 120, 470, 240, 52), "Reintentar", "restart"),
            Button(pygame.Rect(WINDOW_WIDTH // 2 - 120, 540, 240, 52), "Salir", "quit"),
        ]

    def reset_game(self) -> None:
        self.world = self.generate_world()
        start = self.find_start_position()
        self.player = Player(start)
        self.enemies = []
        self.items = []
        self.boss_spawned = False
        self.boss_defeated = False
        self.normal_kills = 0
        self.announced_thresholds = set()
        self.steps_since_passive_heal = 0
        self.show_help = False
        self.log = [
            "Llegas a una isla rodeada de agua.",
            "Derrota a los enemigos y preparate para Baldur.",
        ]
        self.merchant_positions = []
        for _ in range(MERCHANT_COUNT):
            self.merchant_positions.append(self.random_empty_position(min_distance=4))
        self.place_items()
        self.place_enemies()
        self.state = STATE_PLAYING

    def generate_world(self) -> list[list[str]]:
        world = [["ground" for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
        caves: list[Position] = []

        for index in range(MAP_SIZE):
            world[0][index] = "water"
            world[MAP_SIZE - 1][index] = "water"
            world[index][0] = "water"
            world[index][MAP_SIZE - 1] = "water"

        self.paint_clusters(world, "water", clusters=10, steps=42)
        self.paint_clusters(world, "mountain", clusters=9, steps=36)

        for _ in range(520):
            x = self.rng.randrange(2, MAP_SIZE - 2)
            y = self.rng.randrange(2, MAP_SIZE - 2)
            if world[y][x] == "ground":
                world[y][x] = "forest"

        for _ in range(12):
            position = self.random_map_position()
            if world[position[1]][position[0]] == "ground":
                world[position[1]][position[0]] = "house"

        for _ in range(8):
            position = self.random_map_position()
            x, y = position
            if world[y][x] in {"ground", "forest"}:
                world[y][x] = "cave"
                caves.append(position)

        center = MAP_SIZE // 2
        for y in range(center - 2, center + 3):
            for x in range(center - 2, center + 3):
                world[y][x] = "ground"

        self.caves = caves
        return world

    def paint_clusters(
        self, world: list[list[str]], tile_key: str, clusters: int, steps: int
    ) -> None:
        for _ in range(clusters):
            x, y = self.random_map_position()
            for _ in range(steps):
                if 1 <= x < MAP_SIZE - 1 and 1 <= y < MAP_SIZE - 1:
                    world[y][x] = tile_key
                direction = self.rng.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
                x = clamp(x + direction[0], 1, MAP_SIZE - 2)
                y = clamp(y + direction[1], 1, MAP_SIZE - 2)

    def random_map_position(self) -> Position:
        return (
            self.rng.randrange(2, MAP_SIZE - 2),
            self.rng.randrange(2, MAP_SIZE - 2),
        )

    def find_start_position(self) -> Position:
        center = (MAP_SIZE // 2, MAP_SIZE // 2)
        if self.is_walkable(center):
            return center

        for radius in range(1, 10):
            for y in range(center[1] - radius, center[1] + radius + 1):
                for x in range(center[0] - radius, center[0] + radius + 1):
                    position = (x, y)
                    if self.in_bounds(position) and self.is_walkable(position):
                        return position
        return center

    def place_enemies(self) -> None:
        for _ in range(GENERATED_EASY_ENEMIES):
            self.enemies.append(self.make_enemy(self.rng.choice(EASY_ENEMIES), 10))
        for _ in range(GENERATED_MEDIUM_ENEMIES):
            self.enemies.append(self.make_enemy(self.rng.choice(MEDIUM_ENEMIES), 14))

    def make_enemy(self, template: EnemyTemplate, min_distance: int) -> Enemy:
        hp = self.rng.randint(*template.hp_range)
        return Enemy(
            name=template.name,
            symbol=template.symbol,
            tier=template.tier,
            position=self.random_empty_position(min_distance=min_distance),
            hp=hp,
            max_hp=hp,
            attack_range=template.attack_range,
            reward_range=template.reward_range,
            color=template.color,
        )

    def place_items(self) -> None:
        for _ in range(34):
            self.items.append(
                Item(
                    "Oro",
                    "$",
                    "gold",
                    self.rng.randint(8, 22),
                    self.random_empty_position(min_distance=2),
                    (248, 207, 99),
                )
            )
        for _ in range(10):
            self.items.append(
                Item(
                    "Vida",
                    "+",
                    "health",
                    self.rng.randint(10, 18),
                    self.random_empty_position(min_distance=3),
                    (255, 116, 126),
                )
            )
        for _ in range(7):
            self.items.append(
                Item(
                    "Tesoro",
                    "o",
                    "treasure",
                    self.rng.randint(38, 72),
                    self.random_empty_position(min_distance=5),
                    (133, 213, 234),
                )
            )

    def random_empty_position(self, min_distance: int = 0) -> Position:
        occupied = self.occupied_positions()
        for _ in range(7000):
            position = self.random_map_position()
            if position in occupied:
                continue
            if manhattan(position, self.player.position) < min_distance:
                continue
            if self.is_walkable(position):
                return position
        raise RuntimeError("No se encontro una posicion libre en el mapa.")

    def occupied_positions(self) -> set[Position]:
        occupied = {self.player.position}
        occupied.update(enemy.position for enemy in self.enemies)
        occupied.update(item.position for item in self.items)
        occupied.update(self.merchant_positions)
        return occupied

    def in_bounds(self, position: Position) -> bool:
        x, y = position
        return 0 <= x < MAP_SIZE and 0 <= y < MAP_SIZE

    def is_walkable(self, position: Position) -> bool:
        if not self.in_bounds(position):
            return False
        x, y = position
        return TILES[self.world[y][x]].walkable

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.running = False
            return

        if self.state == STATE_MENU:
            self.handle_menu_event(event)
        elif self.state == STATE_PLAYING:
            self.handle_playing_event(event)
        elif self.state == STATE_SHOP:
            self.handle_shop_event(event)
        elif self.state in {STATE_WIN, STATE_LOSE}:
            self.handle_end_event(event)

    def handle_menu_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in {pygame.K_RETURN, pygame.K_SPACE}:
                self.reset_game()
            elif event.key == pygame.K_ESCAPE:
                self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            action = self.clicked_button(self.menu_buttons, event.pos)
            if action == "play":
                self.reset_game()
            elif action == "quit":
                self.running = False

    def handle_playing_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_TAB:
            self.show_help = not self.show_help
            return

        if self.show_help:
            if event.key == pygame.K_ESCAPE:
                self.show_help = False
            return

        movement_keys = {
            pygame.K_UP: (0, -1),
            pygame.K_w: (0, -1),
            pygame.K_DOWN: (0, 1),
            pygame.K_s: (0, 1),
            pygame.K_LEFT: (-1, 0),
            pygame.K_a: (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_d: (1, 0),
        }

        if event.key in movement_keys:
            dx, dy = movement_keys[event.key]
            self.move_player(dx, dy)
        elif event.key in {pygame.K_e, pygame.K_SPACE}:
            self.try_open_shop()
        elif event.key == pygame.K_ESCAPE:
            self.state = STATE_MENU

    def handle_shop_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            self.state = STATE_PLAYING
            self.add_log("Te alejas del mercader.")
        elif event.key == pygame.K_1:
            self.buy_weapon()
        elif event.key == pygame.K_2:
            self.buy_armor()
        elif event.key == pygame.K_3:
            self.buy_healing()

    def handle_end_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in {pygame.K_RETURN, pygame.K_r, pygame.K_SPACE}:
                self.reset_game()
            elif event.key in {pygame.K_ESCAPE, pygame.K_q}:
                self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            action = self.clicked_button(self.end_buttons, event.pos)
            if action == "restart":
                self.reset_game()
            elif action == "quit":
                self.running = False

    def clicked_button(self, buttons: list[Button], position: Position) -> str | None:
        for button in buttons:
            if button.rect.collidepoint(position):
                return button.action
        return None

    def move_player(self, dx: int, dy: int) -> None:
        self.log.clear()
        target = (self.player.position[0] + dx, self.player.position[1] + dy)
        if not self.is_walkable(target):
            self.add_log("No puedes avanzar por ese terreno.")
            return

        enemy = self.enemy_at(target)
        if enemy is not None:
            self.player_attack(enemy)
            if self.state == STATE_PLAYING:
                self.enemy_turn()
            return

        if target in self.merchant_positions:
            self.show_help = False
            self.state = STATE_SHOP
            self.add_log("El mercader abre su tienda.")
            return

        self.player.position = target
        item = self.item_at(target)
        if item is not None:
            self.collect_item(item)

        if self.state == STATE_PLAYING:
            self.enemy_turn()
        if self.state == STATE_PLAYING:
            self.apply_passive_healing()

    def try_open_shop(self) -> None:
        merchant_nearby = any(
            manhattan(self.player.position, merchant_position) <= 1
            for merchant_position in self.merchant_positions
        )
        if merchant_nearby:
            self.show_help = False
            self.state = STATE_SHOP
            self.add_log("El mercader muestra sus mejoras.")
        else:
            self.add_log("No hay ningun mercader cerca.")

    def apply_passive_healing(self) -> None:
        if self.state != STATE_PLAYING:
            return
        if self.player.hp <= 0 or self.player.hp >= PASSIVE_HEAL_CAP:
            return

        self.steps_since_passive_heal += 1
        if self.steps_since_passive_heal < PASSIVE_HEAL_EVERY_STEPS:
            return

        self.steps_since_passive_heal = 0
        recovered = min(PASSIVE_HEAL_AMOUNT, PASSIVE_HEAL_CAP - self.player.hp)
        self.player.hp += recovered
        self.add_log(f"Recuperacion pasiva: vida +{recovered}.")

    def buy_weapon(self) -> None:
        if self.player.weapon_level >= 3:
            self.add_log("Tu arma ya esta al maximo.")
            return
        cost = WEAPON_COSTS[self.player.weapon_level]
        if self.player.gold < cost:
            self.add_log(f"Necesitas {cost} de oro para mejorar el arma.")
            return
        self.player.gold -= cost
        self.player.weapon_level += 1
        self.add_log(f"Compraste {self.player.weapon_name}.")
        self.try_spawn_boss()

    def buy_armor(self) -> None:
        if self.player.armor_level >= 3:
            self.add_log("Tu armadura ya esta al maximo.")
            return
        cost = ARMOR_COSTS[self.player.armor_level]
        if self.player.gold < cost:
            self.add_log(f"Necesitas {cost} de oro para mejorar la armadura.")
            return
        self.player.gold -= cost
        self.player.armor_level += 1
        self.add_log(f"Compraste {self.player.armor_name}.")
        self.try_spawn_boss()

    def buy_healing(self) -> None:
        if self.player.hp >= MAX_PLAYER_HP:
            self.add_log("No puedes comprar curacion porque tienes la vida completa.")
            return
        if self.player.gold < HEAL_COST:
            self.add_log(f"Necesitas {HEAL_COST} de oro para curarte.")
            return
        self.player.gold -= HEAL_COST
        self.player.hp = min(MAX_PLAYER_HP, self.player.hp + HEAL_AMOUNT)
        self.add_log(f"Recuperaste {HEAL_AMOUNT} de vida.")

    def player_attack(self, enemy: Enemy) -> None:
        damage = self.rng.randint(*WEAPON_DAMAGE[self.player.weapon_level])
        enemy.hp -= damage
        self.add_log(f"Atacas a {enemy.name}: -{damage} HP.")

        if enemy.hp <= 0:
            self.defeat_enemy(enemy)
            return

        retaliation = self.rng.randint(*enemy.attack_range)
        self.damage_player(retaliation, enemy.name)

    def defeat_enemy(self, enemy: Enemy) -> None:
        reward = self.rng.randint(*enemy.reward_range)
        self.player.gold += reward
        self.enemies.remove(enemy)

        if enemy.tier == TIER_BOSS:
            self.boss_defeated = True
            self.player.has_amulet = True
            self.player.score_bonus += 1000
            self.add_log(f"Derrotaste a Baldur y ganaste {reward} de oro.")
            self.add_log("Bonus +1000. El amuleto te da una vida extra.")
        else:
            self.normal_kills += 1
            self.add_log(f"Derrotaste a {enemy.name}. Oro +{reward}.")
            self.announce_progress()
            self.try_spawn_boss()

        self.check_victory()

    def damage_player(self, raw_damage: int, source: str) -> None:
        blocked = ARMOR_BLOCK[self.player.armor_level]
        damage = max(1, raw_damage - blocked)
        self.player.hp -= damage
        self.add_log(f"{source} te golpea: -{damage} HP.")

        if self.player.hp > 0:
            return

        if self.player.has_amulet:
            self.player.has_amulet = False
            self.player.hp = 50
            self.add_log("El Amuleto de Baldur te devuelve a la pelea.")
            return

        self.finish_game(False)

    def enemy_turn(self) -> None:
        occupied = {enemy.position for enemy in self.enemies}
        for enemy in list(self.enemies):
            if self.state != STATE_PLAYING:
                return

            distance = manhattan(enemy.position, self.player.position)
            if distance == 1:
                self.damage_player(self.rng.randint(*enemy.attack_range), enemy.name)
                continue

            is_boss = enemy.tier == TIER_BOSS
            can_chase = is_boss or distance <= ENEMY_AGGRO_RADIUS
            move_chance = 1.0 if is_boss else 0.65
            if can_chase and self.rng.random() < move_chance:
                if is_boss:
                    next_position = self.next_boss_step(enemy, occupied)
                else:
                    next_position = self.next_enemy_step(enemy, occupied)
                if next_position is not None:
                    occupied.remove(enemy.position)
                    enemy.position = next_position
                    occupied.add(enemy.position)

    def next_boss_step(
        self, enemy: Enemy, occupied: set[Position]
    ) -> Position | None:
        start = enemy.position
        goal = self.player.position
        blocked = set(occupied)
        blocked.discard(start)
        visited = {start}
        queue = deque([(start, None)])

        while queue:
            current, first_step = queue.popleft()
            for position in neighbors4(current):
                if position in visited or not self.in_bounds(position):
                    continue

                step = first_step if first_step is not None else position
                if position == goal:
                    return step

                if position in blocked or position in self.merchant_positions:
                    continue
                if not self.is_walkable(position):
                    continue

                visited.add(position)
                queue.append((position, step))

        return self.next_enemy_step(enemy, occupied)

    def next_enemy_step(
        self, enemy: Enemy, occupied: set[Position]
    ) -> Position | None:
        candidates = list(neighbors4(enemy.position))
        self.rng.shuffle(candidates)
        candidates.sort(key=lambda position: manhattan(position, self.player.position))

        for position in candidates:
            if position == self.player.position:
                continue
            if position in occupied or position in self.merchant_positions:
                continue
            if self.is_walkable(position):
                return position
        return None

    def announce_progress(self) -> None:
        remaining = self.required_normal_remaining()
        if remaining in OMINOUS_MESSAGES and remaining not in self.announced_thresholds:
            self.announced_thresholds.add(remaining)
            self.add_log(OMINOUS_MESSAGES[remaining])

    def try_spawn_boss(self) -> None:
        if self.boss_spawned:
            return

        remaining = self.required_normal_remaining()
        well_equipped = self.player.weapon_level >= 2 and self.player.armor_level >= 2
        should_spawn = remaining <= 3 or (remaining <= 5 and well_equipped)
        if not should_spawn:
            return

        hp = BOSS_TEMPLATE.hp_range[0]
        self.enemies.append(
            Enemy(
                name=BOSS_TEMPLATE.name,
                symbol=BOSS_TEMPLATE.symbol,
                tier=BOSS_TEMPLATE.tier,
                position=self.boss_spawn_position(),
                hp=hp,
                max_hp=hp,
                attack_range=BOSS_TEMPLATE.attack_range,
                reward_range=BOSS_TEMPLATE.reward_range,
                color=BOSS_TEMPLATE.color,
            )
        )
        self.boss_spawned = True
        self.add_log("Baldur emerge de una cueva y empieza a seguirte.")

    def boss_spawn_position(self) -> Position:
        usable_caves = [
            position
            for position in self.caves
            if position not in self.occupied_positions()
            and manhattan(position, self.player.position) >= 8
            and self.is_walkable(position)
        ]
        if usable_caves:
            return self.rng.choice(usable_caves)
        return self.random_empty_position(min_distance=10)

    def normal_enemy_count(self) -> int:
        return sum(1 for enemy in self.enemies if enemy.tier != TIER_BOSS)

    def required_normal_remaining(self) -> int:
        return max(0, REQUIRED_NORMAL_KILLS - self.normal_kills)

    def check_victory(self) -> None:
        if self.required_normal_remaining() == 0 and self.boss_defeated:
            self.finish_game(True)

    def finish_game(self, won: bool) -> None:
        if won:
            self.state = STATE_WIN
            self.final_title = "Victoria"
            self.final_message = "Cumpliste el objetivo y Baldur cae."
        else:
            self.state = STATE_LOSE
            self.final_title = "Derrota"
            self.final_message = "Tu expedicion termina en la isla."

    def enemy_at(self, position: Position) -> Enemy | None:
        for enemy in self.enemies:
            if enemy.position == position:
                return enemy
        return None

    def item_at(self, position: Position) -> Item | None:
        for item in self.items:
            if item.position == position:
                return item
        return None

    def collect_item(self, item: Item) -> None:
        if item.kind == "gold":
            self.player.gold += item.amount
            message = self.rng.choice(GOLD_PICKUP_MESSAGES)
            self.add_log(message.format(amount=item.amount))
        elif item.kind == "treasure":
            self.player.gold += item.amount
            message = self.rng.choice(TREASURE_PICKUP_MESSAGES)
            self.add_log(message.format(amount=item.amount))
        elif item.kind == "health":
            previous_hp = self.player.hp
            self.player.hp = min(MAX_PLAYER_HP, self.player.hp + item.amount)
            recovered = self.player.hp - previous_hp
            message = self.rng.choice(HEALTH_PICKUP_MESSAGES)
            self.add_log(message.format(amount=recovered))
        self.items.remove(item)

    def add_log(self, message: str) -> None:
        self.log.append(message)
        if len(self.log) > 10:
            self.log = self.log[-10:]

    def draw(self) -> None:
        self.screen.fill(COLORS["background"])
        if self.state == STATE_MENU:
            self.draw_menu()
        elif self.state in {STATE_PLAYING, STATE_SHOP}:
            self.draw_game()
            if self.state == STATE_SHOP:
                self.draw_shop_overlay()
        elif self.state in {STATE_WIN, STATE_LOSE}:
            self.draw_end_screen()

    def draw_menu(self) -> None:
        self.draw_ascii_background()
        title = self.title_font.render("ROGUE FORTRESS", True, COLORS["accent"])
        subtitle = self.body_font.render(
            "Roguelike por grilla: combate, economia y exploracion",
            True,
            COLORS["text"],
        )
        self.screen.blit(title, title.get_rect(center=(WINDOW_WIDTH // 2, 210)))
        self.screen.blit(subtitle, subtitle.get_rect(center=(WINDOW_WIDTH // 2, 270)))

        hint_lines = [
            "Derrota 20 enemigos normales para forzar la aparicion de Baldur.",
            "El oro sirve como puntaje y como recurso para comprar mejoras.",
        ]
        y = 310
        for line in hint_lines:
            rendered = self.small_font.render(line, True, COLORS["muted"])
            self.screen.blit(rendered, rendered.get_rect(center=(WINDOW_WIDTH // 2, y)))
            y += 24

        for button in self.menu_buttons:
            self.draw_button(button)

    def draw_ascii_background(self) -> None:
        glyphs = ".T^~$+rbsWmak"
        for row in range(0, WINDOW_HEIGHT, 32):
            for col in range(0, WINDOW_WIDTH, 32):
                symbol = glyphs[(row // 32 + col // 32) % len(glyphs)]
                color = (26, 34, 42) if (row + col) % 64 == 0 else (20, 27, 34)
                rendered = self.small_font.render(symbol, True, color)
                self.screen.blit(rendered, (col, row))

    def draw_game(self) -> None:
        self.draw_header()
        self.draw_map_view()
        self.draw_panel()
        if self.show_help:
            self.draw_help_overlay()

    def draw_header(self) -> None:
        title = self.subtitle_font.render("Rogue Fortress", True, COLORS["accent"])
        self.screen.blit(title, (GRID_LEFT, 34))
        coordinates = f"Posicion: {self.player.position[0]}, {self.player.position[1]}"
        rendered = self.small_font.render(coordinates, True, COLORS["muted"])
        self.screen.blit(rendered, (GRID_LEFT, 70))

    def camera_origin(self) -> Position:
        player_x, player_y = self.player.position
        return (
            clamp(player_x - VIEW_SIZE // 2, 0, MAP_SIZE - VIEW_SIZE),
            clamp(player_y - VIEW_SIZE // 2, 0, MAP_SIZE - VIEW_SIZE),
        )

    def draw_map_view(self) -> None:
        camera_x, camera_y = self.camera_origin()
        for row in range(VIEW_SIZE):
            for col in range(VIEW_SIZE):
                world_position = (camera_x + col, camera_y + row)
                rect = pygame.Rect(
                    GRID_LEFT + col * TILE_SIZE,
                    GRID_TOP + row * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE,
                )
                self.draw_tile(rect, world_position)

        border = pygame.Rect(GRID_LEFT, GRID_TOP, GRID_PIXELS, GRID_PIXELS)
        pygame.draw.rect(self.screen, COLORS["accent"], border, 2)

    def draw_tile(self, rect: pygame.Rect, position: Position) -> None:
        tile = TILES[self.world[position[1]][position[0]]]
        pygame.draw.rect(self.screen, tile.background, rect)
        pygame.draw.rect(self.screen, COLORS["grid"], rect, 1)

        symbol = tile.symbol
        color = tile.foreground

        item = self.item_at(position)
        enemy = self.enemy_at(position)
        if item is not None:
            symbol = item.symbol
            color = item.color
        if position in self.merchant_positions:
            symbol = "&"
            color = COLORS["accent"]
        if enemy is not None:
            symbol = enemy.symbol
            color = enemy.color
        if position == self.player.position:
            symbol = "@"
            color = COLORS["text"]

        rendered = self.tile_font.render(symbol, True, color)
        self.screen.blit(rendered, rendered.get_rect(center=rect.center))

    def draw_panel(self) -> None:
        panel_rect = pygame.Rect(PANEL_LEFT, GRID_TOP, PANEL_WIDTH, GRID_PIXELS)
        pygame.draw.rect(self.screen, COLORS["panel"], panel_rect, border_radius=6)
        pygame.draw.rect(self.screen, COLORS["grid"], panel_rect, 1, border_radius=6)

        text_x = PANEL_LEFT + 18
        y = GRID_TOP + 18
        y = self.draw_panel_line("Jugador", text_x, y, COLORS["accent"], True)
        stats = [
            f"Vida: {self.player.hp}/{MAX_PLAYER_HP}",
            f"Oro: {self.player.gold}",
            f"Puntaje: {self.player.final_score}",
            f"Arma: {self.player.weapon_name}",
            f"Armadura: {self.player.armor_name}",
            f"Amuleto: {'si' if self.player.has_amulet else 'no'}",
        ]
        for line in stats:
            y = self.draw_panel_line(line, text_x, y, COLORS["text"])

        y += 12
        y = self.draw_panel_line("Mundo", text_x, y, COLORS["accent"], True)
        boss_status = "vivo" if self.boss_spawned and not self.boss_defeated else "oculto"
        if self.boss_defeated:
            boss_status = "derrotado"
        world_stats = [
            f"Objetivo normal: {min(self.normal_kills, REQUIRED_NORMAL_KILLS)}/{REQUIRED_NORMAL_KILLS}",
            f"Normales vivos: {self.normal_enemy_count()}",
            f"Baldur: {boss_status}",
            f"Mercaderes: {len(self.merchant_positions)} (&)",
        ]
        for line in world_stats:
            y = self.draw_panel_line(line, text_x, y, COLORS["text"])

        y += 12
        y = self.draw_panel_line("Registro", text_x, y, COLORS["accent"], True)
        controls_y = GRID_TOP + GRID_PIXELS - 88
        log_bottom = controls_y - 12
        max_log_lines = max(1, (log_bottom - y) // 21)
        wrapped_log: list[str] = []
        for message in self.log[-7:]:
            wrapped_log.extend(self.wrap_text(message, 34))
        for line in wrapped_log[-max_log_lines:]:
            y = self.draw_panel_line(line, text_x, y, COLORS["muted"])

        y = controls_y
        controls = ["WASD/flechas: mover", "E/Espacio: tienda", "TAB: simbolos", "ESC: menu"]
        for line in controls:
            y = self.draw_panel_line(line, text_x, y, COLORS["muted"])

    def draw_panel_line(
        self, text: str, x: int, y: int, color: Color, bold: bool = False
    ) -> int:
        font = self.body_font if bold else self.small_font
        rendered = font.render(text, True, color)
        self.screen.blit(rendered, (x, y))
        return y + (26 if bold else 21)

    def draw_help_overlay(self) -> None:
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 145))
        self.screen.blit(overlay, (0, 0))

        width = min(780, WINDOW_WIDTH - 96)
        height = min(540, WINDOW_HEIGHT - 120)
        rect = pygame.Rect(
            (WINDOW_WIDTH - width) // 2,
            (WINDOW_HEIGHT - height) // 2,
            width,
            height,
        )
        pygame.draw.rect(self.screen, COLORS["panel"], rect, border_radius=8)
        pygame.draw.rect(self.screen, COLORS["accent"], rect, 2, border_radius=8)

        title = self.subtitle_font.render("Simbolos y reglas", True, COLORS["accent"])
        self.screen.blit(title, (rect.left + 28, rect.top + 22))

        left_rows = [
            ("@", "Jugador: moverse y atacar por choque.", COLORS["text"]),
            (".", "Llanura transitable.", (180, 188, 168)),
            ("T", "Bosque transitable.", (97, 176, 105)),
            ("~", "Agua: bloquea el paso.", (155, 202, 230)),
            ("^", "Montana: bloquea el paso.", (199, 201, 205)),
            ("U", "Cueva: posible salida de Baldur.", (201, 179, 230)),
            ("H", "Casa: obstaculo.", (230, 186, 129)),
            ("&", "Mercader: mejoras y curacion.", COLORS["accent"]),
            ("$", "Oro: compras y puntaje.", (248, 207, 99)),
            ("o", "Tesoro: recompensa alta.", (133, 213, 234)),
            ("+", "Vida: cura al recoger.", (255, 116, 126)),
        ]
        right_rows = [
            ("r b s w z", "Enemigos faciles.", COLORS["danger"]),
            ("W m k a e", "Enemigos medios.", COLORS["danger"]),
            ("B", "Baldur: jefe que rastrea tu posicion.", (255, 104, 96)),
            ("Objetivo", "20 normales + Baldur.", COLORS["text"]),
            ("Arma", "Aumenta el dano causado.", COLORS["text"]),
            ("Armadura", "Reduce el dano recibido.", COLORS["text"]),
            (
                "Pasiva",
                f"+{PASSIVE_HEAL_AMOUNT} vida/{PASSIVE_HEAL_EVERY_STEPS} pasos hasta {PASSIVE_HEAL_CAP}.",
                COLORS["text"],
            ),
            ("Puntaje", "Vida + oro*2 + bonus.", COLORS["text"]),
            ("TAB/ESC", "Cerrar esta ventana.", COLORS["muted"]),
        ]

        left_x = rect.left + 32
        right_x = rect.left + rect.width // 2 + 16
        y_start = rect.top + 78

        section = self.body_font.render("Mapa", True, COLORS["accent"])
        self.screen.blit(section, (left_x, y_start - 32))
        section = self.body_font.render("Combate", True, COLORS["accent"])
        self.screen.blit(section, (right_x, y_start - 32))

        y = y_start
        for symbol, description, color in left_rows:
            rendered_symbol = self.body_font.render(symbol, True, color)
            rendered_text = self.small_font.render(description, True, COLORS["text"])
            self.screen.blit(rendered_symbol, (left_x, y))
            self.screen.blit(rendered_text, (left_x + 54, y + 3))
            y += 28

        y = y_start
        for symbol, description, color in right_rows:
            rendered_symbol = self.small_font.render(symbol, True, color)
            rendered_text = self.small_font.render(description, True, COLORS["text"])
            self.screen.blit(rendered_symbol, (right_x, y + 3))
            self.screen.blit(rendered_text, (right_x + 104, y + 3))
            y += 28

    def draw_shop_overlay(self) -> None:
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 155))
        self.screen.blit(overlay, (0, 0))

        rect = pygame.Rect(WINDOW_WIDTH // 2 - 245, 130, 490, 430)
        pygame.draw.rect(self.screen, COLORS["panel"], rect, border_radius=8)
        pygame.draw.rect(self.screen, COLORS["accent"], rect, 2, border_radius=8)

        title = self.subtitle_font.render("Mercader", True, COLORS["accent"])
        self.screen.blit(title, title.get_rect(center=(WINDOW_WIDTH // 2, 170)))

        weapon_text = self.next_upgrade_text(
            "1", "Arma", self.player.weapon_level, WEAPON_NAMES, WEAPON_COSTS
        )
        armor_text = self.next_upgrade_text(
            "2", "Armadura", self.player.armor_level, ARMOR_NAMES, ARMOR_COSTS
        )
        heal_text = f"3 - Curar {HEAL_AMOUNT} de vida: {HEAL_COST} oro"

        lines = [
            f"Oro disponible: {self.player.gold}",
            "",
            weapon_text,
            armor_text,
            heal_text,
            "",
            "ESC - cerrar tienda",
        ]
        y = 220
        for line in lines:
            color = COLORS["text"] if line else COLORS["muted"]
            rendered = self.body_font.render(line, True, color)
            self.screen.blit(rendered, (WINDOW_WIDTH // 2 - 190, y))
            y += 38 if line else 18

    def next_upgrade_text(
        self, key: str, label: str, level: int, names: list[str], costs: list[int]
    ) -> str:
        if level >= 3:
            return f"{key} - {label}: maximo ({names[level]})"
        return f"{key} - {label}: {names[level + 1]} por {costs[level]} oro"

    def draw_end_screen(self) -> None:
        self.draw_ascii_background()
        title_color = COLORS["good"] if self.state == STATE_WIN else COLORS["danger"]
        title = self.title_font.render(self.final_title, True, title_color)
        self.screen.blit(title, title.get_rect(center=(WINDOW_WIDTH // 2, 185)))

        message = self.body_font.render(self.final_message, True, COLORS["text"])
        self.screen.blit(message, message.get_rect(center=(WINDOW_WIDTH // 2, 250)))

        results = [
            f"Puntuacion final: {self.player.final_score}",
            f"Oro restante: {self.player.gold}",
            f"Vida restante: {max(self.player.hp, 0)}",
            f"Arma final: {self.player.weapon_name}",
            f"Armadura final: {self.player.armor_name}",
        ]
        y = 310
        for line in results:
            rendered = self.body_font.render(line, True, COLORS["text"])
            self.screen.blit(rendered, rendered.get_rect(center=(WINDOW_WIDTH // 2, y)))
            y += 31

        for button in self.end_buttons:
            self.draw_button(button)

    def draw_button(self, button: Button) -> None:
        mouse_position = pygame.mouse.get_pos()
        is_hovered = button.rect.collidepoint(mouse_position)
        fill = COLORS["panel_light"] if is_hovered else COLORS["panel"]
        outline = COLORS["accent"] if is_hovered else COLORS["grid"]

        pygame.draw.rect(self.screen, fill, button.rect, border_radius=6)
        pygame.draw.rect(self.screen, outline, button.rect, 2, border_radius=6)
        rendered = self.body_font.render(button.text, True, COLORS["text"])
        self.screen.blit(rendered, rendered.get_rect(center=button.rect.center))

    def wrap_text(self, text: str, max_chars: int) -> list[str]:
        words = text.split()
        if not words:
            return [""]

        lines: list[str] = []
        current = words[0]
        for word in words[1:]:
            if len(current) + len(word) + 1 > max_chars:
                lines.append(current)
                current = word
            else:
                current = f"{current} {word}"
        lines.append(current)
        return lines


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Rogue Fortress")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    game = RogueFortress(screen)

    while game.running:
        for event in pygame.event.get():
            game.handle_event(event)
        game.draw()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
