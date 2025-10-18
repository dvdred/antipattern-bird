# ===============  AntiPattern Bird Epic Game  ===============
# Made with Lulz by dvdred@gmail.com
# GPL3 rules

import sys, os, pathlib
from pathlib import Path
import pygame
import pygame.freetype
import random
import time

pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
WIDTH, HEIGHT = 500, 750
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE) # finestra ridimensionabile
WIN = pygame.Surface((WIDTH, HEIGHT)) # surface logica su cui continui a disegnare
pygame.display.set_caption("AntiPattern Bird Epic Game")

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

icon_path      = get_resource_path('icon32.png')
jump_sound     = get_resource_path('jump.wav')
point_sound    = get_resource_path('point.wav')
rainbow_sound  = get_resource_path('rainbow.wav')
lifeup_sound   = get_resource_path('lifeup.wav')
lifedown_sound = get_resource_path('lifedown.wav')
font_emoji     = get_resource_path('DejaVuSansMono.ttf')

ICON = pygame.image.load(icon_path)
pygame.display.set_icon(ICON)

S_JUMP     = pygame.mixer.Sound(jump_sound)
S_POINT    = pygame.mixer.Sound(point_sound)
S_RAINBOW  = pygame.mixer.Sound(rainbow_sound)
S_LIFEUP   = pygame.mixer.Sound(lifeup_sound)
S_LIFEDOWN = pygame.mixer.Sound(lifedown_sound)

for snd in (S_JUMP, S_POINT, S_RAINBOW, S_LIFEUP, S_LIFEDOWN):
    if snd:
        snd.set_volume(0.5)

LIGHT_COLORS = [(173, 216, 230), (175, 238, 238), (255, 218, 185),
                (230, 230, 250), (240, 248, 255)]

BIRD_COLORS = [
    (255, 204,  51),  # Saffron
    (255, 127,  80),  # Coral
    ( 65, 105, 225),  # Royal Blue
    ( 34, 139,  34),  # Forest Green
    (218, 165,  32),  # Goldenrod
    (147, 112, 219),  # Medium Purple
    (180,   0,   0)   # Blood Red
]                                

PIPE_COLORS = [
    (0, 100, 0),     # 1
    (139, 69, 19),   # 2
    (64, 64, 64),    # 3
    (139, 0, 0),     # 4
    (85, 107, 47),   # 5
    (72, 61, 139),   # 6
    (25, 25, 112),   # 7
    (0, 0, 139),     # 8
    (47, 79, 79),    # 9
    (34, 139, 34),   #10
    (105, 105, 105), #11
    (70, 130, 180),  #12
    (0, 139, 139),   #13
    (160, 82, 45)    #14
]
LAND_COLORS  = [(101,67,33), (204,204,0), (15,5,135)]

GRAVITY   = 0.25
JUMP      = -6
PIPE_W    = 70
PIPE_GAP  = 150
PIPE_FREQ = 1500
MAX_LIVES = 6
INVULN_MS = 2000
DEMO_ALPHA = 60

RAINBOW_MIN_MS = 20_000
RAINBOW_MAX_MS = 45_000
RAINBOW_POINTS = 3
RAINBOW_COLORS = [(255,0,0), (255,127,0), (255,255,0),
                  (0,255,0), (0,0,255), (75,0,130)]

ZEBRA_COLORS = [(0,0,0), (255,255,255)]
ZEBRA_DURATION_MS = 8_000
SPEED_MULTIPLIER = 1.5
ZEBRA_POINTS_MULT = 2

LVL2_TIME = 90_000
LVL3_TIME = 150_000

WIN_TIME = 240_000   # 4 minuti
#WIN_TIME = 30_000   # DEBUG
GAME_OVER_WAIT_MS = 2000   # antidolorifico 2 s
BONUS_WIN = 50
BONUS_WIN_MAX = 100
DEBUG_MODE = False
FLASH_MS = 150
FLASH_COLOR = (255,255,255)

TEXT_LIST = [
"Design_By_Committee", "Warm_Bodies", "Analysis_Paralysis",
"Stovepipe_System", "Smoke_and_Mirrors", "Mushroom_Management",
"Death_March", "Elephant_in_the_Room", "Boat_Anchor", "Busy_Waiting",
"Action_at_a_Distance", "Caching_Failure", "Accumulate_and_Fire",
"Code_Smell", "Lava_Flow", "Accidental_Complexity", "Big_ball_of_Mud",
"Blind_Faith", "Code_Momentum", "DLL_Hell", "Vendor_Lock-in",
"Input_Kludge", "Double-Checked_Locking", "Interface_Bloat",
"Continuous_Obsolescence", "Abstraction_Inversion", "Kitchen_Sink",
"Magic_Number", "God_Object", "Premature_Optimization", "Poltergeist",
"Feature_Creep", "Yo-Yo_Problem", "Cargo_Cult_Programming",
"Copy_and_Paste_Programming", "Magic_Pushbutton", "Ambiguous_Viewpoint",
"Reinventing_the_wheel", "Reinventing_the_Square_Wheel", "Fencepost",
"Software_Bloat", "Spaghetti_Code", "Hard_Code", "Soft_Code", "Dead_End"
]

class Particle:
    def __init__(self, x, y, color=(255, 255, 255)):
        self.x, self.y = x, y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 0)
        self.life = 30
        self.color = color  # <-- AGGIUNTO
    def update(self):
        self.x += self.vx; self.y += self.vy; self.life -= 1
    def draw(self, surf):
        if self.life > 0:
            pygame.draw.circle(surf, self.color,  # <-- MODIFICATO (era (255, 255, 255))
                               (int(self.x), int(self.y)), 3)

class Cloud:
    # palette possibili (sceglierne una a caso per ogni nuvola)
    PALETTES = [
        [(255, 255, 255)],                           # bianco puro
        [(255, 250, 250), (255, 228, 225)],          # rosa-avorio
        [(255, 255, 240), (250, 250, 220)],          # giallo spento
        [(240, 248, 255), (176, 196, 222)],          # azzurro-crema
        [(211, 211, 211), (169, 169, 169)]           # grigi
    ]

    def __init__(self, x, y, size, speed, opacity):
        self.x, self.y, self.speed = x, y, speed
        self.size       = random.randint(35, 90)            # raggio di riferimento
        self.opacity    = random.randint(70, 160)           # più tenue
        self.palette    = random.choice(self.PALETTES)

        # Crea una nuvola più realistica con cerchi sovrapposti
        self.bubbles = []
        base_r = self.size // 2  # raggio base
        
        # Cerchio centrale (più grande)
        col = random.choice(self.palette) + (self.opacity,)
        self.bubbles.append((0, 0, int(base_r * 1.2), col))
        
        # Cerchi laterali (sinistra e destra)
        num_side = random.randint(2, 3)
        for i in range(num_side):
            # Lato sinistro
            offx = -base_r + random.randint(-10, 10)
            offy = random.randint(-base_r // 3, base_r // 3)
            r = int(base_r * random.uniform(0.7, 1.0))
            col = random.choice(self.palette) + (self.opacity,)
            self.bubbles.append((offx, offy, r, col))
            
            # Lato destro
            offx = base_r + random.randint(-10, 10)
            offy = random.randint(-base_r // 3, base_r // 3)
            r = int(base_r * random.uniform(0.7, 1.0))
            col = random.choice(self.palette) + (self.opacity,)
            self.bubbles.append((offx, offy, r, col))
        
        # Cerchi superiori (per dare volume)
        num_top = random.randint(1, 2)
        for i in range(num_top):
            offx = random.randint(-base_r // 2, base_r // 2)
            offy = -base_r // 2 + random.randint(-5, 5)
            r = int(base_r * random.uniform(0.6, 0.9))
            col = random.choice(self.palette) + (self.opacity,)
            self.bubbles.append((offx, offy, r, col))

        # bounding-box superficie
        max_right  = max(offx + r for offx, _, r, _ in self.bubbles) + 5
        max_bottom = max(offy + r for _, offy, r, _ in self.bubbles) + 5
        min_left   = min(offx - r for offx, _, r, _ in self.bubbles)
        min_top    = min(offy - r for _, offy, r, _ in self.bubbles)
        
        self.surf_w = max_right - min_left + 10
        self.surf_h = max_bottom - min_top + 10
        self.offset_x = -min_left + 5
        self.offset_y = -min_top + 5
        
        self.surface = pygame.Surface((self.surf_w, self.surf_h), pygame.SRCALPHA)
        self._render_shape()

    def _render_shape(self):
        for offx, offy, r, col in self.bubbles:
            cx = self.offset_x + offx
            cy = self.offset_y + offy
            pygame.draw.circle(self.surface, col, (cx, cy), r)

    def update(self):
        self.x -= self.speed
        if self.x < -self.surf_w:
            # rigenera anche aspetto quando rientra
            self.x = WIDTH + random.randint(50, 250)
            self.y = random.randint(30, HEIGHT - 250)
            self.__init__(self.x, self.y, self.size, self.speed, self.opacity)

    def draw(self, surf):
        surf.blit(self.surface, (int(self.x), int(self.y)))

class Bird:
    def __init__(self):
        self.x, self.y = 50, HEIGHT // 2
        self.vel = 0
        self.size = 30
        self.shape = random.choice(['square', 'circle', 'triangle', 'diamond'])
        self.color = random.choice(BIRD_COLORS)
        self.alpha = 255

    def reset_position(self):
        self.y, self.vel = HEIGHT // 2, 0

    def jump(self):
        self.vel = JUMP
        if S_JUMP:
            S_JUMP.play()

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel
        if self.y < 0:
            self.y, self.vel = 0, 0
        if self.y > HEIGHT - 50 - self.size:
            self.y, self.vel = HEIGHT - 50 - self.size, 0

    def set_transparent(self, alpha):
        self.alpha = alpha

    def draw(self, surf):
        temp = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        if self.shape == 'square':
            temp.fill((*self.color, self.alpha))
        elif self.shape == 'circle':
            pygame.draw.circle(temp, (*self.color, self.alpha),
                               (self.size // 2, self.size // 2), self.size // 2)
        elif self.shape == 'diamond':
            pts = [(self.size // 2, 0), (self.size, self.size // 2),
                   (self.size // 2, self.size), (0, self.size // 2)]
            pygame.draw.polygon(temp, (*self.color, self.alpha), pts)
        else:  # triangle
            pts = [(self.size // 2, 0), (0, self.size), (self.size, self.size)]
            pygame.draw.polygon(temp, (*self.color, self.alpha), pts)
        surf.blit(temp, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def randomize_shape(self, exclude_current=True):
        shapes = ['square', 'circle', 'triangle', 'diamond']
        if exclude_current and self.shape in shapes:
            shapes.remove(self.shape)
        self.shape = random.choice(shapes)

    def randomize_color(self, exclude_current=True):
        colors = random.choice(BIRD_COLORS)
        if exclude_current and self.color in colors:
            shapes.remove(self.color)
        self.color = colors

class Pipe:
    def __init__(self, x, text=None):
        self.x = x
        self.height = random.randint(150, 400)
        self.color  = random.choice(PIPE_COLORS)
        self.passed = False
        self.is_rainbow = False
        self.is_zebra   = False
        self.text = random.choice(TEXT_LIST) if text is None else text

    def update(self, speed=3):
        self.x -= speed

    def draw(self, surf, alpha=255):
        top = pygame.Surface((PIPE_W, self.height), pygame.SRCALPHA)
        top.fill((*self.color, alpha))
        surf.blit(top, (self.x, 0))
        font_small = pygame.font.SysFont("ubuntumono", 24) or pygame.font.SysFont("Arial", 24) or pygame.font.SysFont(None, 24)
        lines = [self.text[i:i+2] for i in range(0, len(self.text), 2)]
        total_h = len(lines) * 24
        start_y = max(5, (self.height - total_h) // 2)
        for i, line in enumerate(lines):
            y_line = start_y + i * 24
            if y_line + 24 > self.height - 5:
                continue
            txt = font_small.render(line, True, (255,255,255))
            x_txt = self.x + (PIPE_W - txt.get_width()) // 2
            if txt.get_width() <= PIPE_W - 4:
                surf.blit(txt, (x_txt, y_line))

        bot_h = HEIGHT - self.height - PIPE_GAP - 50
        bottom = pygame.Surface((PIPE_W, bot_h), pygame.SRCALPHA)
        bottom.fill((*self.color, alpha))
        surf.blit(bottom, (self.x, self.height + PIPE_GAP))
        start_y_bot = max(5, (bot_h - total_h) // 2)
        for i, line in enumerate(lines):
            y_line = start_y_bot + i * 24
            if y_line + 24 > bot_h - 5:
                continue
            txt = font_small.render(line, True, (255,255,255))
            x_txt = self.x + (PIPE_W - txt.get_width()) // 2
            if txt.get_width() <= PIPE_W - 4:
                surf.blit(txt, (x_txt, self.height + PIPE_GAP + 5 + y_line))

    def collide(self, bird):
        b  = bird.get_rect()
        t  = pygame.Rect(self.x, 0, PIPE_W, self.height)
        bo = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_W,
                         HEIGHT - self.height - PIPE_GAP - 50)
        return b.colliderect(t) or b.colliderect(bo)

class RainbowPipe(Pipe):
    def __init__(self, x):
        super().__init__(x, text="")
        self.rainbow = RAINBOW_COLORS
        self.passed = False
        self.is_rainbow = True

    def draw(self, surf, alpha=255):
        strip_w = PIPE_W // len(self.rainbow)
        for i, col in enumerate(self.rainbow):
            x_band = self.x + i * strip_w
            band = pygame.Surface((strip_w, self.height), pygame.SRCALPHA)
            band.fill((*col, alpha))
            surf.blit(band, (x_band, 0))
        bot_h = HEIGHT - self.height - PIPE_GAP - 50
        for i, col in enumerate(self.rainbow):
            x_band = self.x + i * strip_w
            band = pygame.Surface((strip_w, bot_h), pygame.SRCALPHA)
            band.fill((*col, alpha))
            surf.blit(band, (x_band, self.height + PIPE_GAP))

class ZebraPipe(Pipe):
    def __init__(self, x):
        super().__init__(x, text="")
        self.colors = ZEBRA_COLORS
        self.passed = False
        self.is_zebra = True

    def draw(self, surf, alpha=255):
        strip_w = PIPE_W // 2
        for i, col in enumerate(self.colors):
            x_band = self.x + i * strip_w
            band = pygame.Surface((strip_w, self.height), pygame.SRCALPHA)
            band.fill((*col, alpha))
            surf.blit(band, (x_band, 0))
        bot_h = HEIGHT - self.height - PIPE_GAP - 50
        for i, col in enumerate(self.colors):
            x_band = self.x + i * strip_w
            band = pygame.Surface((strip_w, bot_h), pygame.SRCALPHA)
            band.fill((*col, alpha))
            surf.blit(band, (x_band, self.height + PIPE_GAP))
# ==============================================================
#                      FUNZIONI UI
# ==============================================================
def draw_land(surf, color):
    pygame.draw.rect(surf, color, (0, HEIGHT-50, WIDTH, 50))

def draw_score(surf, score):
    surf.blit(pygame.font.SysFont(None, 36).render(f"Score: {score}", True, (0,0,0)),
              (WIDTH-150, 10))

def draw_lives(surf, lives):
    surf.blit((pygame.font.Font(font_emoji, 28) or pygame.font.SysFont(None, 28)).render("❤ "*lives, True, (255,0,0)),
              (10, 10))

def draw_level(surf, lvl):
    txt = pygame.font.SysFont(None, 32).render(f"Level {lvl}", True, (0,0,0))
    surf.blit(txt, (10, 50))

def draw_game_over(surf, best, score, bonus_score):
    font_big   = pygame.font.SysFont("ubuntumono", 48) or pygame.font.SysFont("Arial", 48) or pygame.font.SysFont(None, 48)
    font_small = pygame.font.SysFont("ubuntumono", 24) or pygame.font.SysFont("Arial", 24) or pygame.font.SysFont(None, 24)
    txt1 = font_big.render("Game Over", True, (255, 0, 0))
    rect1 = txt1.get_rect(center=(WIDTH//2, HEIGHT//2 - 120))
    surf.blit(txt1, rect1)
    txt_scorelvl = font_big.render(f"Bonus: {bonus_score}", True, (0, 0, 0))
    rect_scorelvl = txt_scorelvl.get_rect(center=(WIDTH//2, HEIGHT//2 - 70))
    surf.blit(txt_scorelvl, rect_scorelvl)
    txt_score = font_big.render(f"Score: {score}", True, (0, 0, 0))
    rect_score = txt_score.get_rect(center=(WIDTH//2, HEIGHT//2 - 20))
    surf.blit(txt_score, rect_score)
    txt_best = font_big.render(f"Best: {best}", True, (0, 0, 0))
    rect_best = txt_best.get_rect(center=(WIDTH//2, HEIGHT//2 + 30))
    surf.blit(txt_best, rect_best)
    txt3 = font_small.render("SPACE=restart  O=change bird  Q=quit", True, (0, 0, 0))
    rect3 = txt3.get_rect(center=(WIDTH//2, HEIGHT//2 + 70))
    surf.blit(txt3, rect3)

def draw_win_screen(surf, sc, bonus):
    font_big = pygame.font.SysFont("ubuntumono", 48) or pygame.font.SysFont("Arial", 48) or pygame.font.SysFont(None, 48)
    font_med = pygame.font.SysFont("ubuntumono", 32) or pygame.font.SysFont("Arial", 32) or pygame.font.SysFont(None, 32)
    txt1 = font_big.render("YOU WON!", True, (0, 85, 0))
    rect1 = txt1.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
    surf.blit(txt1, rect1)
    txt_sc = font_med.render(f"Points: {sc}  (bonus {bonus})", True, (0, 0, 0))
    rect_sc = txt_sc.get_rect(center=(WIDTH//2, HEIGHT//2 - 45))
    surf.blit(txt_sc, rect_sc)
    txt3 = font_med.render("SPACE = continue    Q = quit", True, (0, 0, 0))
    rect3 = txt3.get_rect(center=(WIDTH//2, HEIGHT//2 + 20))
    surf.blit(txt3, rect3)

def draw_start_screen(surf, demo_pipes, demo_land, bg_color):
    surf.fill(bg_color)
    for p in demo_pipes:
        p.draw(surf, alpha=DEMO_ALPHA)
    land = pygame.Surface((WIDTH, 50), pygame.SRCALPHA)
    land.fill((*demo_land, DEMO_ALPHA))
    surf.blit(land, (0, HEIGHT-50))
    font_big = pygame.font.SysFont("ubuntumono", 48, bold=True) or pygame.font.SysFont("Arial", 48, bold=True) or pygame.font.SysFont(None, 48, bold=True)
    title1 = font_big.render("AntiPattern Bird", True, (0, 0, 0))
    title2 = font_big.render("Epic Game", True, (0, 0, 0))
    rect1, rect2 = title1.get_rect(center=(WIDTH//2, HEIGHT//2 - 60)),\
                   title2.get_rect(center=(WIDTH//2, HEIGHT//2 - 10))
    surf.blit(title1, rect1); surf.blit(title2, rect2)
    inst = pygame.font.SysFont(None, 24).render("Press START o SPACE", True, (255, 255, 255))
    btn  = pygame.Rect(0, 0, 230, 45)
    btn.center = (WIDTH//2, HEIGHT//2 + 40)
    pygame.draw.rect(surf, (70, 130, 180), btn, border_radius=10)
    surf.blit(inst, inst.get_rect(center=btn.center))

def draw_shape_selection_menu(surf, bg_color, current_shape, current_color, debug_mode):
    surf.fill(bg_color)
    
    font_title = pygame.font.SysFont("ubuntumono", 40, bold=True) or pygame.font.SysFont(None, 40)
    font_label = pygame.font.SysFont("ubuntumono", 24) or pygame.font.SysFont(None, 24)
    font_small = pygame.font.SysFont("ubuntumono", 18) or pygame.font.SysFont(None, 18)
    font_number = pygame.font.SysFont("ubuntumono", 20, bold=True) or pygame.font.SysFont(None, 20)
    
    title = font_title.render("Choose your bird", True, (0, 0, 0))
    surf.blit(title, title.get_rect(center=(WIDTH//2, 50)))
    
    # Sezione FORMA
    subtitle1 = font_label.render("SHAPE:", True, (0, 0, 0))
    surf.blit(subtitle1, (50, 100))
    
    shapes = [
        ('square', 'Square', 140, '1'),
        ('circle', 'Circle', 190, '2'),
        ('triangle', 'Triangle', 240, '3'),
        ('diamond', 'Diamond', 290, '4'),
        ('random', 'Random', 340, '5')
    ]
    
    shape_buttons = []
    for shape_id, label, y_pos, key_num in shapes:
        btn = pygame.Rect(110, y_pos, 180, 40)
        color = (70, 130, 180) if current_shape != shape_id else (50, 200, 50)
        pygame.draw.rect(surf, color, btn, border_radius=8)
        
        # Numero della scelta
        num_txt = font_number.render(key_num, True, (0, 0, 0))
        surf.blit(num_txt, (btn.left - 25, btn.centery - 10))
        
        txt = font_label.render(label, True, (255, 255, 255))
        surf.blit(txt, txt.get_rect(center=btn.center))
        
        # Freccetta indicatore
        if current_shape == shape_id:
            font_arrow = pygame.font.Font(font_emoji, 24) or font_label
            arrow = font_arrow.render("→", True, (255, 0, 0))
            surf.blit(arrow, (btn.left - 50, btn.centery - 12))
        
        # Preview forma
        if shape_id != 'random':
            preview_size = 25
            preview_x = btn.right + 15
            preview_y = btn.centery - preview_size // 2
            preview_surf = pygame.Surface((preview_size, preview_size), pygame.SRCALPHA)
            col = (255, 204, 51)
            
            if shape_id == 'square':
                preview_surf.fill(col)
            elif shape_id == 'circle':
                pygame.draw.circle(preview_surf, col, (preview_size//2, preview_size//2), preview_size//2)
            elif shape_id == 'triangle':
                pts = [(preview_size//2, 0), (0, preview_size), (preview_size, preview_size)]
                pygame.draw.polygon(preview_surf, col, pts)
            elif shape_id == 'diamond':
                pts = [(preview_size//2, 0), (preview_size, preview_size//2),
                       (preview_size//2, preview_size), (0, preview_size//2)]
                pygame.draw.polygon(preview_surf, col, pts)
            
            surf.blit(preview_surf, (preview_x, preview_y))
        else:
            question = font_label.render("?", True, (255, 204, 51))
            surf.blit(question, (btn.right + 20, btn.centery - 12))
        
        shape_buttons.append((btn, shape_id))
    
    # Sezione COLORE
    subtitle2 = font_label.render("COLOR:", True, (0, 0, 0))
    surf.blit(subtitle2, (50, 400))
    
    colors = [
        ('saffron', 'Saffron', 440, BIRD_COLORS[0], 'Q'),
        ('coral', 'Coral', 490, BIRD_COLORS[1], 'W'),
        ('blue', 'Blue', 540, BIRD_COLORS[2], 'E'),
        ('green', 'Green', 590, BIRD_COLORS[3], 'R'),
        ('random', 'Random', 640, None, 'T')
    ]
    
    color_buttons = []
    for color_id, label, y_pos, rgb, key_letter in colors:
        btn = pygame.Rect(110, y_pos, 180, 40)
        btn_color = (70, 130, 180) if current_color != color_id else (50, 200, 50)
        pygame.draw.rect(surf, btn_color, btn, border_radius=8)
        
        # Lettera della scelta
        letter_txt = font_number.render(key_letter, True, (0, 0, 0))
        surf.blit(letter_txt, (btn.left - 25, btn.centery - 10))
        
        txt = font_label.render(label, True, (255, 255, 255))
        surf.blit(txt, txt.get_rect(center=btn.center))
        
        # Freccetta indicatore
        if current_color == color_id:
            font_arrow = pygame.font.Font(font_emoji, 24) or font_label
            arrow = font_arrow.render("→", True, (255, 0, 0))
            surf.blit(arrow, (btn.left - 50, btn.centery - 12))
        
        # Preview colore
        if rgb:
            preview_rect = pygame.Rect(btn.right + 15, btn.centery - 12, 25, 25)
            pygame.draw.rect(surf, rgb, preview_rect)
            pygame.draw.rect(surf, (0, 0, 0), preview_rect, 2)
        else:
            question = font_label.render("?", True, (255, 204, 51))
            surf.blit(question, (btn.right + 20, btn.centery - 12))
        
        color_buttons.append((btn, color_id))
    
    # ============ DEBUG MODE: Bottone compatto in alto a destra ============
    debug_btn = pygame.Rect(WIDTH - 160, 100, 150, 35)
    debug_color = (200, 50, 50) if debug_mode else (100, 100, 100)
    pygame.draw.rect(surf, debug_color, debug_btn, border_radius=8)
    
    debug_status = "ON" if debug_mode else "OFF"
    # Usa il font emoji come per i cuori
    font_debug = pygame.font.Font(font_emoji, 18) or font_small  # <-- CAMBIATO
    debug_txt = font_debug.render(f"⚙️ Debug: {debug_status}", True, (255, 255, 255))
    surf.blit(debug_txt, debug_txt.get_rect(center=debug_btn.center))
    
    # Tasto D sopra il bottone
    letter_txt = font_number.render("D", True, (0, 0, 0))
    surf.blit(letter_txt, (debug_btn.centerx - 7, debug_btn.top - 25))
    # =======================================================================
    
    # Istruzioni (spostate più in alto)
    hint1 = font_small.render("Use numbers/letters or click to select", True, (100, 100, 100))
    surf.blit(hint1, hint1.get_rect(center=(WIDTH//2, HEIGHT - 40)))
    hint2 = font_small.render("Press SPACE to start", True, (100, 100, 100))
    surf.blit(hint2, hint2.get_rect(center=(WIDTH//2, HEIGHT - 20)))
    
    return shape_buttons, color_buttons, debug_btn  # <-- RESTITUISCE ANCHE debug_btn

def draw_pause_overlay(surf):
    font = pygame.font.SysFont("ubuntumono", 56) or pygame.font.SysFont("Arial", 56) or pygame.font.SysFont(None, 56)
    txt  = font.render("PAUSE", True, (40, 40, 40))
    rect = txt.get_rect(center=(WIDTH//2, HEIGHT//2 - 20))
    surf.blit(txt, rect)
    txt2 = pygame.font.SysFont(None, 28).render("Pess P to continue", True, (60,60,60))
    rect2= txt2.get_rect(center=(WIDTH//2, HEIGHT//2 + 25))
    surf.blit(txt2, rect2)

def draw_zebra_active(surf, ms_left):
    font = pygame.font.SysFont("ubuntumono", 26) or pygame.font.SysFont("Arial", 26) or pygame.font.SysFont(None, 26)
    txt = font.render(f"ZEBRA SPEED! {max(0, ms_left//1000)}s", True, (255, 0, 0))
    rect = txt.get_rect(center=(WIDTH//2, 40))
    surf.blit(txt, rect)

def draw_debug_info(surf, base_speed, speed_lvl, zebra_active, cur_speed, game_time_ms):
    """Mostra informazioni di debug sulla velocità e tempo di gioco"""
    font_debug = pygame.font.SysFont("ubuntumono", 18) or pygame.font.SysFont("Arial", 18) or pygame.font.SysFont(None, 18)
    
    # Background semi-trasparente (aumentato per fare spazio al tempo)
    debug_bg = pygame.Surface((250, 110), pygame.SRCALPHA)
    debug_bg.fill((0, 0, 0, 180))
    surf.blit(debug_bg, (10, HEIGHT - 170))
    
    # Informazioni
    y_offset = HEIGHT - 165
    
    txt1 = font_debug.render(f"DEBUG MODE", True, (255, 255, 0))
    surf.blit(txt1, (15, y_offset))
    
    # Tempo di gioco (converti ms in mm:ss)
    total_seconds = game_time_ms // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    txt_time = font_debug.render(f"Game Time: {minutes:02d}:{seconds:02d}", True, (100, 200, 255))
    surf.blit(txt_time, (15, y_offset + 20))
    
    txt2 = font_debug.render(f"Base Speed: {base_speed:.1f}", True, (255, 255, 255))
    surf.blit(txt2, (15, y_offset + 40))
    
    txt3 = font_debug.render(f"Level Mult: {speed_lvl:.1f}x", True, (255, 255, 255))
    surf.blit(txt3, (15, y_offset + 60))
    
    zebra_mult = SPEED_MULTIPLIER if zebra_active else 1.0
    color_zebra = (255, 100, 100) if zebra_active else (255, 255, 255)
    txt4 = font_debug.render(f"Zebra Mult: {zebra_mult:.1f}x", True, color_zebra)
    surf.blit(txt4, (15, y_offset + 80))
    
    # Velocità finale evidenziata
    txt5 = font_debug.render(f"SPEED: {cur_speed:.2f}", True, (0, 255, 0))
    surf.blit(txt5, (160, y_offset + 40))

def present(surf):
    # surf è la surface logica (WIN) 500x750
    screen = pygame.display.get_surface()
    sw, sh = screen.get_size()

    # calcola fattore di scala mantenendo l'aspect ratio
    scale = min(sw / WIDTH, sh / HEIGHT)
    new_w, new_h = max(1, int(WIDTH * scale)), max(1, int(HEIGHT * scale))

    # ridimensiona (smoothscale per qualità; usa scale se vuoi più performance)
    if new_w == WIDTH and new_h == HEIGHT:
        scaled = surf
    else:
        try:
            scaled = pygame.transform.smoothscale(surf, (new_w, new_h))
        except pygame.error:
            scaled = pygame.transform.scale(surf, (new_w, new_h))

    # letterbox: riempi tutto lo schermo (nero) e centra l'immagine scalata
    screen.fill((0, 0, 0))
    ox = (sw - new_w) // 2
    oy = (sh - new_h) // 2
    screen.blit(scaled, (ox, oy))
    pygame.display.flip()
# ==============================================================
#                          MAIN
# ==============================================================
def main():
    # Variabili per gestire il tempo di pausa
    pause_start = 0
    total_paused_time = 0
    
    def game_time():
        """Restituisce il tempo di gioco escludendo le pause"""
        if paused:
            # Durante la pausa, ritorna il tempo congelato
            return pause_start - total_paused_time
        else:
            return pygame.time.get_ticks() - total_paused_time
    
    clock = pygame.time.Clock()
    bg_color   = random.choice(LIGHT_COLORS)
    land_color = random.choice(LAND_COLORS)

    bird  = Bird()
    pipes, score, best, lives = [], 0, 0, 3
    running, playing = True, False
    waiting_restart  = False
    selecting_shape = False
    debug_mode = False
    
    # Selezioni correnti nel menu (quelle evidenziate)
    current_shape_selection = 'random'
    current_color_selection = 'random'
    # Selezioni confermate (quelle effettivamente usate in partita)
    confirmed_shape = 'random'
    confirmed_color = 'random'
    # Selezioni correnti nel menu (quelle evidenziate)
    current_shape_selection = 'random'
    current_color_selection = 'random'
    # Selezioni confermate (quelle effettivamente usate in partita)
    confirmed_shape = 'random'
    confirmed_color = 'random'
    # Liste dei bottoni (persistenti tra i frame)
    shape_buttons = []
    color_buttons = []
    debug_btn = pygame.Rect(0, 0, 0, 0)
    invuln_time, last_pipe = 0, pygame.time.get_ticks()
    game_over_start = 0   # timestamp game-over

    paused      = False
    flash_until = 0

    # carica best score
    best = 0   # volatile: non persistente fra esecuzioni


    tn = 1
    next_life_threshold = 5 * tn * (tn + 1) // 2

    demo_pipes, demo_last_pipe = [], pygame.time.get_ticks()
    demo_land      = random.choice(LAND_COLORS)
    start_bg_color = random.choice(LIGHT_COLORS)
    rainbow_next   = pygame.time.get_ticks() + random.randint(RAINBOW_MIN_MS, RAINBOW_MAX_MS)

    particles = []

# ----- ZEBRA TIMER -----
    zebra_until      = 0
    zebra_next_min   = pygame.time.get_ticks() + 60_000
    zebra_pending    = False
    base_speed       = 3

# ----- LIVELLI -----
    level_timer      = 0
    speed_lvl        = 1.0
    score_lvl        = 1
    bonus_score      = 0

# ----- VITTORIA -----
    won            = False
    won_waiting    = False
    bonus_win      = 0

 # ====== AGGIUNGI QUESTO BLOCO DOPO L'INIZIALIZZAZIONE DELLE VARIABILI ======
    # Inizializzazione nuvole
    clouds_layer1 = []  # Strato più lontano (più lento)
    clouds_layer2 = []  # Strato più vicino (più veloce)
    
    # Crea nuvole per il primo strato (più lontane)
    for _ in range(3):
        cloud = Cloud(
            x=random.randint(0, WIDTH),
            y=random.randint(50, HEIGHT - 250),
            size=random.randint(40, 70),
            speed=random.uniform(0.3, 0.8),
            opacity=random.randint(80, 120)
        )
        clouds_layer1.append(cloud)
    
    # Crea nuvole per il secondo strato (più vicine)
    for _ in range(4):
        cloud = Cloud(
            x=random.randint(0, WIDTH),
            y=random.randint(50, HEIGHT - 200),
            size=random.randint(60, 100),
            speed=random.uniform(1.0, 1.8),
            opacity=random.randint(150, 200)
        )
        clouds_layer2.append(cloud)
    # ===========================================================================

# -------------------- GAME LOOP --------------------
    while running:
        dt = clock.tick(60)
        if paused:
            pygame.mixer.pause()
        else:
            pygame.mixer.unpause()

        now = game_time() if playing else pygame.time.get_ticks()

# -------- INPUT --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and selecting_shape:
                mouse_pos = event.pos
                screen = pygame.display.get_surface()
                sw, sh = screen.get_size()
                scale = min(sw / WIDTH, sh / HEIGHT)
                new_w, new_h = int(WIDTH * scale), int(HEIGHT * scale)
                ox, oy = (sw - new_w) // 2, (sh - new_h) // 2
                
                log_x = (mouse_pos[0] - ox) / scale
                log_y = (mouse_pos[1] - oy) / scale
                
                # Controlla click su forme
                for btn, shape_id in shape_buttons:
                    if btn.collidepoint(log_x, log_y):
                        current_shape_selection = shape_id
                        break
                
                # Controlla click su colori
                for btn, color_id in color_buttons:
                    if btn.collidepoint(log_x, log_y):
                        current_color_selection = color_id
                        break
                # Controlla click su debug mode  # <-- NUOVO
                if debug_btn.collidepoint(log_x, log_y):
                    debug_mode = not debug_mode
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and playing and not waiting_restart:
                    if not paused:  # Sta per andare in pausa
                        pause_start = pygame.time.get_ticks()
                    else:  # Sta per uscire dalla pausa
                        total_paused_time += pygame.time.get_ticks() - pause_start
                    paused = not paused
                    break
                
                if waiting_restart:
                    # distinguiamo vittoria da game over
                    if won_waiting: # Vittoria
                        if event.key == pygame.K_SPACE:
                            # Torna al menu di selezione dopo vittoria
                            won_waiting = False
                            waiting_restart = False
                            total_paused_time = 0
                            pause_start = 0
                            playing = False
                            selecting_shape = True
                            current_shape_selection = 'random'
                            current_color_selection = 'random'
                            bird.reset_position()
                            pipes.clear()
                            particles.clear()
                            won = False
                            # Aumenta difficoltà base per la prossima partita
                            base_speed = min(6, base_speed + 0.5)
                        elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                            running = False
                    else:  # game over normale
                        if event.key == pygame.K_SPACE:
                            if not won_waiting and now - game_over_start < GAME_OVER_WAIT_MS:
                                continue   # ignora space finché non sono passati 2 s
                            waiting_restart = False
                            total_paused_time = 0
                            pause_start = 0
                            bird.reset_position()
                            
                            # Riapplica forma e colore confermati
                            if confirmed_shape != 'random':
                                bird.shape = confirmed_shape
                            else:
                                bird.randomize_shape(exclude_current=False)
                            
                            if confirmed_color == 'random':
                                bird.randomize_color(exclude_current=False)
                            elif confirmed_color == 'saffron':
                                bird.color = BIRD_COLORS[0]
                            elif confirmed_color == 'coral':
                                bird.color = BIRD_COLORS[1]
                            elif confirmed_color == 'blue':
                                bird.color = BIRD_COLORS[2]
                            elif confirmed_color == 'green':
                                bird.color = BIRD_COLORS[3]
                            
                            pipes.clear(); score = 0; lives = 3; bonus_score=0
                            base_speed = 3  # <-- RESET velocità base dopo game over
                            invuln_time = 0; last_pipe = now; tn = 1
                            next_life_threshold = 5 * tn * (tn + 1) // 2
                            bg_color   = random.choice(LIGHT_COLORS)
                            land_color = random.choice(LAND_COLORS)
                            rainbow_next = now + random.randint(RAINBOW_MIN_MS, RAINBOW_MAX_MS)
                            zebra_next_min = now + 60_000
                            zebra_until = 0; zebra_pending = False
                            level_timer = 0; speed_lvl = 1.0; score_lvl = 1
                            won = False; won_waiting = False
                            particles.clear(); playing = True
                        elif event.key == pygame.K_o:  # <-- NUOVO: torna al menu selezione
                            if not won_waiting and now - game_over_start < GAME_OVER_WAIT_MS:
                                continue   # ignora O finché non sono passati 2 s
                            waiting_restart = False
                            total_paused_time = 0
                            pause_start = 0
                            selecting_shape = True
                            current_shape_selection = confirmed_shape  # Mantiene l'ultima scelta
                            current_color_selection = confirmed_color  # Mantiene l'ultima scelta
                            bird.reset_position()
                            pipes.clear()
                            particles.clear()
                            score = 0
                            lives = 3
                            bonus_score = 0
                            base_speed = 3
                            won = False
                            won_waiting = False    
                        elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                            running = False
                else:  # non in attesa: gioco fermo o in corso
                    if not playing and not selecting_shape and event.key == pygame.K_SPACE:
                        selecting_shape = True  # <-- Vai al menu selezione invece di iniziare subito
                    elif selecting_shape:
                        # Navigazione forme (tasti 1-5)
                        if event.key == pygame.K_1:
                            current_shape_selection = 'square'
                        elif event.key == pygame.K_2:
                            current_shape_selection = 'circle'
                        elif event.key == pygame.K_3:
                            current_shape_selection = 'triangle'
                        elif event.key == pygame.K_4:
                            current_shape_selection = 'diamond'
                        elif event.key == pygame.K_5:
                            current_shape_selection = 'random'
                        
                        # Navigazione colori (tasti Q, W, E, R, T)
                        elif event.key == pygame.K_q:
                            current_color_selection = 'saffron'
                        elif event.key == pygame.K_w:
                            current_color_selection = 'coral'
                        elif event.key == pygame.K_e:
                            current_color_selection = 'blue'
                        elif event.key == pygame.K_r:
                            current_color_selection = 'green'
                        elif event.key == pygame.K_t:
                            current_color_selection = 'random'
                        # Toggle Debug Mode
                        elif event.key == pygame.K_d:
                            debug_mode = not debug_mode
                        # Conferma con SPACE
                        elif event.key == pygame.K_SPACE:
                            # Salva le selezioni confermate
                            confirmed_shape = current_shape_selection
                            confirmed_color = current_color_selection
                            selecting_shape = False
                            total_paused_time = 0
                            pause_start = 0

                            # Applica forma
                            if confirmed_shape != 'random':
                                bird.shape = confirmed_shape
                            else:
                                bird.randomize_shape(exclude_current=False)
                            
                            # Applica colore
                            if confirmed_color == 'random':
                                bird.randomize_color(exclude_current=False)
                            elif confirmed_color == 'saffron':
                                bird.color = BIRD_COLORS[0]
                            elif confirmed_color == 'coral':
                                bird.color = BIRD_COLORS[1]
                            elif confirmed_color == 'blue':
                                bird.color = BIRD_COLORS[2]
                            elif confirmed_color == 'green':
                                bird.color = BIRD_COLORS[3]
                            
                            # Inizia partita
                            playing = True
                            bird.reset_position(); pipes.clear(); score = 0; lives = 3
                            invuln_time = 0; last_pipe = now; tn = 1
                            next_life_threshold = 5 * tn * (tn + 1) // 2
                            bg_color   = random.choice(LIGHT_COLORS)
                            land_color = random.choice(LAND_COLORS)
                            rainbow_next = now + random.randint(RAINBOW_MIN_MS, RAINBOW_MAX_MS)
                            zebra_next_min = now + 60_000
                            zebra_until = 0; zebra_pending = False
                            level_timer = 0; speed_lvl = 1.0; score_lvl = 1
                            won = False; won_waiting = False
                            particles.clear()
                    elif playing and event.key == pygame.K_SPACE and not paused:
                        bird.jump()
                        for _ in range(5):
                            particles.append(Particle(bird.x + bird.size//2,
                                                    bird.y + bird.size,
                                                    bird.color))  # <-- AGGIUNTO bird.color
                    elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                        running = False
                    elif event.type == pygame.VIDEORESIZE:
                        pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

# ------------- fine input -------------

# --------- UPDATE DEMO ----------
        if not playing and not waiting_restart:
            for cloud in clouds_layer1:
                cloud.update()
            for cloud in clouds_layer2:
                cloud.update()
            if now - demo_last_pipe > PIPE_FREQ:
                if now >= rainbow_next:
                    demo_pipes.append(RainbowPipe(WIDTH))
                    rainbow_next = now + random.randint(RAINBOW_MIN_MS, RAINBOW_MAX_MS)
                else:
                    demo_pipes.append(Pipe(WIDTH))
                demo_last_pipe = now
            for p in demo_pipes[:]:
                p.update(speed=2)
                if p.x + PIPE_W < 0:
                    demo_pipes.remove(p)

# --------- LOGICA GIOCO ----------
        if playing and not paused:
            for cloud in clouds_layer1:
                cloud.update()
            for cloud in clouds_layer2:
                cloud.update()
            if invuln_time > 0:
                invuln_time = max(0, invuln_time - dt)
                bird.set_transparent(128 if (invuln_time // 100) % 2 else 180)
            else:
                bird.set_transparent(255)

            bird.update()

# ----- aggiorna timer livello -----
            level_timer += dt
            if level_timer >= WIN_TIME and not won:               # 4 minuti
                won = True
                bonus_win = BONUS_WIN
                if lives == MAX_LIVES:
                    bonus_win += BONUS_WIN_MAX
                score += bonus_win
                if score > best:
                    best = score
                won_waiting = True
                waiting_restart = True
                playing = False
            elif level_timer >= LVL3_TIME and speed_lvl < 2.0:    # 150s -> lvl3
                speed_lvl = 2.0; score_lvl = 3
            elif level_timer >= LVL2_TIME and speed_lvl < 1.5:    # 90s -> lvl2
                speed_lvl = 1.5; score_lvl = 2

# ---- zebra/minuto timer ----
            if now >= zebra_next_min:
                zebra_pending = True
                zebra_next_min = now + 60_000

# ---- speed istantanea (livello + zebra) ----
            cur_speed = base_speed * speed_lvl * (SPEED_MULTIPLIER if now < zebra_until else 1)

            if now - last_pipe > PIPE_FREQ:
                last_pipe = now
                if zebra_pending:
                    pipes.append(ZebraPipe(WIDTH))
                    zebra_pending = False
                elif now >= rainbow_next:
                    pipes.append(RainbowPipe(WIDTH))
                    rainbow_next = now + random.randint(RAINBOW_MIN_MS, RAINBOW_MAX_MS)
                else:
                    pipes.append(Pipe(WIDTH))

            if invuln_time == 0:
                collided_this_frame = False

                # 1. Collisione con i tubi
                for p in pipes[:]:
                    if p.collide(bird):
                        collided_this_frame = True
                        break
                
                # 2. Collisione con pavimento/soffitto
                if not collided_this_frame and (bird.y >= HEIGHT - 50 - bird.size or bird.y <= 0):
                    collided_this_frame = True

                # Se è avvenuta una collisione di qualsiasi tipo, applica le penalità
                if collided_this_frame:
                    lives -= 1
                    invuln_time = INVULN_MS
                    bird.reset_position()
                    if S_LIFEDOWN:
                        S_LIFEDOWN.play()
                    if lives <= 0:
                        playing = False
                        waiting_restart = True
                        game_over_start = now
                        
                        # Calcolo bonus di fine partita
                        lvl_bonus = 0
                        if speed_lvl >= 2.0:   # Raggiunto il Livello 3
                            lvl_bonus = 30
                        elif speed_lvl >= 1.5: # Raggiunto il Livello 2
                            lvl_bonus = 15
                        score += lvl_bonus
                        bonus_score += lvl_bonus

                        if score > best:
                            best = score
                
                # 3. Se NON c'è stata collisione, controlla per il punteggio
                else:
                    for p in pipes:
                        if not p.passed and p.x + PIPE_W < bird.x:
                            p.passed = True
                            pts = 1
                            if getattr(p, 'is_rainbow', False):
                                pts = RAINBOW_POINTS
                                flash_until = now + FLASH_MS
                                S_RAINBOW.play()
                            elif getattr(p, 'is_zebra', False):
                                pts = 2
                                zebra_until = now + ZEBRA_DURATION_MS
                                flash_until = now + FLASH_MS
                                S_RAINBOW.play()
                            else:
                                S_POINT.play()
                            
                            pts *= score_lvl
                            if now < zebra_until: # La zebra mode è attiva dopo aver passato un tubo zebra
                                pts *= ZEBRA_POINTS_MULT
                            
                            score += int(pts)
                            if score > best:
                                best = score
                            break # Assegna punti solo per un tubo alla volta

            # Gestione punti vita extra
            if score >= next_life_threshold:
                if lives < MAX_LIVES:
                    lives += 1
                    if S_LIFEUP:
                        S_LIFEUP.play()
                tn += 1
                next_life_threshold = 5 * tn * (tn + 1) // 2

            # Aggiorna posizione tubi (fuori dal blocco di collisione)
            for p in pipes[:]:
                p.update(speed=int(cur_speed))
                if p.x + PIPE_W < 0:
                    pipes.remove(p)

            for p in particles[:]:
                p.update()
                if p.life <= 0:
                    particles.remove(p)
# -------------------- DRAW --------------------
        if not playing:
            if won_waiting:
                draw_win_screen(WIN, score, bonus_win)
            elif waiting_restart:
                WIN.fill(bg_color)
                # Disegna nuvole anche nella schermata game over
                for cloud in clouds_layer1:
                    cloud.draw(WIN)
                for cloud in clouds_layer2:
                    cloud.draw(WIN)
                bird.reset_position()
                bird.randomize_shape(exclude_current=True)
                bird.randomize_color(exclude_current=True)
                draw_game_over(WIN, best, score, bonus_score)
            elif selecting_shape:
                new_shape_btns, new_color_btns, debug_btn = draw_shape_selection_menu(
                    WIN, bg_color, current_shape_selection, current_color_selection, debug_mode
                )
                shape_buttons = new_shape_btns
                color_buttons = new_color_btns
            else:
                draw_start_screen(WIN, demo_pipes, demo_land, start_bg_color)
                for cloud in clouds_layer1:
                    cloud.draw(WIN)
                for cloud in clouds_layer2:
                    cloud.draw(WIN)
        else:
            WIN.fill(bg_color)
            
            # Disegna prima lo strato lontano (più lento)
            for cloud in clouds_layer1:
                cloud.draw(WIN)
            
            # Poi disegna lo strato vicino (più veloce)
            for cloud in clouds_layer2:
                cloud.draw(WIN)
                
            for p in pipes:
                p.draw(WIN)
            bird.draw(WIN)
            draw_land(WIN, land_color)
            draw_score(WIN, score)
            draw_lives(WIN, lives)
            draw_level(WIN, 1 if score_lvl==1 else (2 if score_lvl==2 else 3))
            for p in particles:
                p.draw(WIN)
            if now < zebra_until:
                draw_zebra_active(WIN, zebra_until - now)
            if debug_mode:
                draw_debug_info(WIN, base_speed, speed_lvl, now < zebra_until, cur_speed, level_timer)

        if paused:
            draw_pause_overlay(WIN)

        if flash_until > now:
            elapsed = now - (flash_until - FLASH_MS)
            alpha = max(0, min(255, 255 * (1 - elapsed / FLASH_MS)))
            flash = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flash.fill((*FLASH_COLOR, int(alpha)))   
            WIN.blit(flash, (0, 0))

        present(WIN)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()