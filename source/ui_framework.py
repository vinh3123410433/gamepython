import pygame
import math
import time
import os

# ==============================================================================
# MODERN UI SYSTEM - COLOR PALETTE & DESIGN TOKENS
# ==============================================================================
COLORS = {
    # Backgrounds & Glass
    'bg_dark': (15, 23, 42),               # #0F172A Slate 900
    'bg_panel': (15, 23, 42, 220),         # Semi-transparent dark
    'bg_card': (30, 41, 59, 230),          # #1E293B Slate 800
    'bg_card_hover': (51, 65, 85, 240),    # #334155 Slate 700
    'overlay_dark': (10, 15, 28, 190),     # Backdrop modal overlay

    # Borders & Outlines
    'border_subtle': (51, 65, 85, 180),
    'border_light': (100, 116, 139, 200),
    'border_highlight': (148, 163, 184, 230),

    # Primary Gold / Amber (Currency, Ranks, Highlights)
    'gold': (245, 158, 11),                # #F59E0B
    'gold_light': (251, 191, 36),          # #FBBF24
    'gold_glow': (245, 158, 11, 70),
    'gold_dark': (180, 110, 6),

    # Vitality / Health (Crimson / Rose)
    'red': (239, 68, 68),                  # #EF4444
    'red_light': (248, 113, 113),          # #F87171
    'red_glow': (239, 68, 68, 80),
    'red_dark': (153, 27, 27),

    # Success / Green (Active, Ready, Buy)
    'green': (16, 185, 129),               # #10B981
    'green_light': (52, 211, 153),         # #34D399
    'green_glow': (16, 185, 129, 80),
    'green_dark': (6, 95, 70),

    # Cyan / Arcane (EXP, Mana, Info, Technology)
    'cyan': (14, 165, 233),                # #0EA5E9
    'cyan_light': (56, 189, 248),          # #38BDF8
    'cyan_glow': (14, 165, 233, 80),
    'cyan_dark': (7, 89, 133),

    # Purple / Mystic (Special Power, Hail)
    'purple': (139, 92, 246),              # #8B5CF6
    'purple_light': (167, 139, 250),       # #A78BFA
    'purple_glow': (139, 92, 246, 80),

    # Neutrals
    'white': (255, 255, 255),
    'text_primary': (248, 250, 252),       # #F8FAFC
    'text_secondary': (203, 213, 225),     # #CBD5E1
    'text_muted': (148, 163, 184),         # #94A3B8
    'text_dim': (100, 116, 139),           # #64748B
    'black': (0, 0, 0),
}

# ==============================================================================
# FONT MANAGER WITH HIGH-QUALITY FALLBACKS
# ==============================================================================
_FONT_CACHE = {}

def get_font(size, bold=True):
    key = (size, bold)
    if key in _FONT_CACHE:
        return _FONT_CACHE[key]
    
    font_names = ['segoeui', 'tahoma', 'trebuchetms', 'arial']
    font = None
    for name in font_names:
        try:
            font = pygame.font.SysFont(name, size, bold=bold)
            if font:
                break
        except Exception:
            pass
    
    if font is None:
        font = pygame.font.Font(None, size)
    
    _FONT_CACHE[key] = font
    return font

# ==============================================================================
# DRAWING HELPERS (GLASSMORPHISM, ROUNDED RECTS, GLOW)
# ==============================================================================
def draw_rounded_rect(surface, color, rect, radius=8, border_color=None, border_width=1):
    rect = pygame.Rect(rect)
    if len(color) == 4 and color[3] < 255:
        shape_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect(), border_radius=radius)
        if border_color and border_width > 0:
            pygame.draw.rect(shape_surf, border_color, shape_surf.get_rect(), width=border_width, border_radius=radius)
        surface.blit(shape_surf, rect.topleft)
    else:
        pygame.draw.rect(surface, color[:3], rect, border_radius=radius)
        if border_color and border_width > 0:
            pygame.draw.rect(surface, border_color, rect, width=border_width, border_radius=radius)

def draw_glass_card(surface, rect, radius=12, bg_color=None, border_color=None, border_width=1):
    if bg_color is None:
        bg_color = COLORS['bg_card']
    if border_color is None:
        border_color = COLORS['border_subtle']
    
    rect = pygame.Rect(rect)
    card_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(card_surf, bg_color, card_surf.get_rect(), border_radius=radius)
    
    # Subtle top highlight line for 3D glass look
    highlight_color = (255, 255, 255, 30)
    highlight_rect = pygame.Rect(radius, 1, max(1, rect.width - radius * 2), 1)
    pygame.draw.rect(card_surf, highlight_color, highlight_rect)
    
    if border_color and border_width > 0:
        pygame.draw.rect(card_surf, border_color, card_surf.get_rect(), width=border_width, border_radius=radius)
    
    surface.blit(card_surf, rect.topleft)

def draw_text_with_shadow(surface, text, font, color, pos, align='center', shadow_color=(0, 0, 0, 180), offset=(1, 2)):
    rendered = font.render(str(text), True, color)
    w, h = rendered.get_size()
    
    x, y = pos
    if align == 'center':
        draw_x = x - w // 2
        draw_y = y - h // 2
    elif align == 'midleft':
        draw_x = x
        draw_y = y - h // 2
    elif align == 'midright':
        draw_x = x - w
        draw_y = y - h // 2
    elif align == 'topleft':
        draw_x = x
        draw_y = y
    elif align == 'topright':
        draw_x = x - w
        draw_y = y
    else:
        draw_x = x
        draw_y = y

    # Shadow
    if shadow_color:
        shadow_surf = font.render(str(text), True, shadow_color[:3])
        if len(shadow_color) == 4 and shadow_color[3] < 255:
            shadow_surf.set_alpha(shadow_color[3])
        surface.blit(shadow_surf, (draw_x + offset[0], draw_y + offset[1]))
    
    surface.blit(rendered, (draw_x, draw_y))
    return pygame.Rect(draw_x, draw_y, w, h)

# ==============================================================================
# UI ICONS (Using high quality PNG assets from buttons/png/ with procedural fallback)
# ==============================================================================
_ICON_CACHE = {}
_PNG_ICON_MAP = {
    'play': 'buttons/png/Icon/Play.png',
    'pause': 'buttons/png/Icon/Pause.png',
    'sound_on': 'buttons/png/Icon/SoundOn.png',
    'sound_off': 'buttons/png/Icon/SoundOff.png',
    'home': 'buttons/png/Icon/Home.png',
    'replay': 'buttons/png/Icon/Replay.png',
    'restart': 'buttons/png/Icon/Replay.png',
    'arrow_left': 'buttons/png/Icon/ArrowLeft.png',
    'back': 'buttons/png/Icon/ArrowLeft.png',
    'arrow_right': 'buttons/png/Icon/ArrowRight.png',
    'close': 'buttons/png/Icon/Cross.png',
    'cross': 'buttons/png/Icon/Cross.png',
    'heart': 'buttons/png/Icon/Heart.png',
    'hp': 'buttons/png/Icon/Heart.png',
    'shield': 'buttons/png/Icon/Shield.png',
    'star': 'buttons/png/Icon/Star.png',
    'spark': 'buttons/png/Icon/Spark.png',
    'meteor': 'buttons/png/Icon/Spark.png',
    'gold': 'buttons/png/Counter/Icon/Money.png',
    'money': 'buttons/png/Counter/Icon/Money.png',
    'coin': 'buttons/png/Counter/Icon/Money.png',
}

def get_png_icon(icon_type, size, color=None):
    if icon_type not in _PNG_ICON_MAP:
        return None
    cache_key = (icon_type, size, tuple(color) if color else None)
    if cache_key in _ICON_CACHE:
        return _ICON_CACHE[cache_key]

    file_path = _PNG_ICON_MAP[icon_type]
    if not os.path.exists(file_path):
        return None

    try:
        raw_img = pygame.image.load(file_path).convert_alpha()
        orig_w, orig_h = raw_img.get_size()
        scale = size / max(orig_w, orig_h)
        new_w = max(1, int(orig_w * scale))
        new_h = max(1, int(orig_h * scale))
        scaled = pygame.transform.smoothscale(raw_img, (new_w, new_h))

        if icon_type in ('gold', 'money', 'coin') or color is None:
            _ICON_CACHE[cache_key] = scaled
            return scaled

        # Tint silhouette to target color preserving antialiased alpha channel
        tinted = pygame.Surface((new_w, new_h), pygame.SRCALPHA)
        tinted.fill(color[:3] + (255,))
        alpha_arr = pygame.surfarray.pixels_alpha(scaled)
        target_alpha = pygame.surfarray.pixels_alpha(tinted)
        target_alpha[:] = alpha_arr[:]
        del alpha_arr
        del target_alpha

        _ICON_CACHE[cache_key] = tinted
        return tinted
    except Exception:
        return None

def draw_icon(surface, icon_type, center_x, center_y, size=20, color=(255, 255, 255)):
    cx, cy = int(center_x), int(center_y)
    r = size // 2

    # Check for PNG icon asset first
    png_icon = get_png_icon(icon_type, size, color)
    if png_icon is not None:
        surface.blit(png_icon, png_icon.get_rect(center=(cx, cy)))
        return

    if icon_type == 'heart':
        # Smooth red heart
        pts = [
            (cx, cy + r - 2),
            (cx - r, cy - 2),
            (cx - r, cy - r // 2),
            (cx - r // 2, cy - r),
            (cx, cy - r // 3),
            (cx + r // 2, cy - r),
            (cx + r, cy - r // 2),
            (cx + r, cy - 2)
        ]
        pygame.draw.polygon(surface, color, pts)
        # Inner gloss shine
        pygame.draw.circle(surface, (255, 255, 255, 160) if len(color) == 4 else (255, 200, 200), (cx - r // 3, cy - r // 3), max(1, r // 4))

    elif icon_type == 'coin':
        # Gold coin with rim and shine
        pygame.draw.circle(surface, COLORS['gold'], (cx, cy), r)
        pygame.draw.circle(surface, COLORS['gold_dark'], (cx, cy), r, width=max(1, r // 6))
        pygame.draw.circle(surface, COLORS['gold_light'], (cx, cy), max(1, r - 3), width=max(1, r // 8))
        font = get_font(max(10, int(size * 0.7)), bold=True)
        t = font.render("$", True, (130, 75, 5))
        surface.blit(t, t.get_rect(center=(cx, cy)))

    elif icon_type == 'star':
        # 5-pointed star
        points = []
        for i in range(10):
            rad = math.radians(i * 36 - 90)
            radius = r if i % 2 == 0 else r * 0.45
            points.append((cx + radius * math.cos(rad), cy + radius * math.sin(rad)))
        pygame.draw.polygon(surface, color, points)

    elif icon_type == 'meteor':
        # Meteor / Fireball icon
        tail_pts = [(cx - r, cy + r), (cx, cy - r), (cx + r, cy + r), (cx, cy + r // 2)]
        pygame.draw.polygon(surface, (255, 140, 0), tail_pts)
        pygame.draw.circle(surface, (255, 80, 0), (cx, cy + r // 3), int(r * 0.6))
        pygame.draw.circle(surface, (255, 230, 100), (cx, cy + r // 3), int(r * 0.35))

    elif icon_type == 'trophy':
        # Gold trophy cup
        cup_rect = pygame.Rect(cx - r * 0.6, cy - r * 0.7, r * 1.2, r * 0.9)
        pygame.draw.rect(surface, COLORS['gold'], cup_rect, border_bottom_left_radius=int(r * 0.6), border_bottom_right_radius=int(r * 0.6))
        # Stem and base
        pygame.draw.rect(surface, COLORS['gold_light'], (cx - r * 0.2, cy + r * 0.2, r * 0.4, r * 0.4))
        pygame.draw.rect(surface, COLORS['gold_dark'], (cx - r * 0.7, cy + r * 0.6, r * 1.4, r * 0.25), border_radius=2)
        # Handles
        pygame.draw.circle(surface, COLORS['gold'], (int(cx - r * 0.65), int(cy - r * 0.25)), max(2, int(r * 0.3)), width=2)
        pygame.draw.circle(surface, COLORS['gold'], (int(cx + r * 0.65), int(cy - r * 0.25)), max(2, int(r * 0.3)), width=2)

    elif icon_type == 'sound_on':
        # Speaker
        pts = [(cx - r // 2, cy - r // 4), (cx - r // 4, cy - r // 4), (cx + r // 5, cy - r // 2), 
               (cx + r // 5, cy + r // 2), (cx - r // 4, cy + r // 4), (cx - r // 2, cy + r // 4)]
        pygame.draw.polygon(surface, color, pts)
        # Sound waves
        pygame.draw.arc(surface, color, (cx - r // 4, cy - r // 2, r, r), -math.pi / 3, math.pi / 3, width=2)
        pygame.draw.arc(surface, color, (cx - r // 2, cy - r * 0.7, r * 1.5, r * 1.4), -math.pi / 3, math.pi / 3, width=2)

    elif icon_type == 'sound_off':
        # Speaker
        pts = [(cx - r // 2, cy - r // 4), (cx - r // 4, cy - r // 4), (cx + r // 5, cy - r // 2), 
               (cx + r // 5, cy + r // 2), (cx - r // 4, cy + r // 4), (cx - r // 2, cy + r // 4)]
        pygame.draw.polygon(surface, color, pts)
        # Cross X
        off = int(r * 0.4)
        pygame.draw.line(surface, COLORS['red_light'], (cx + off, cy - off), (cx + off + r // 2, cy + off), 2)
        pygame.draw.line(surface, COLORS['red_light'], (cx + off, cy + off), (cx + off + r // 2, cy - off), 2)

    elif icon_type == 'pause':
        bar_w = max(2, r // 3)
        bar_h = int(r * 1.2)
        gap = max(2, r // 4)
        pygame.draw.rect(surface, color, (cx - gap - bar_w, cy - bar_h // 2, bar_w, bar_h), border_radius=2)
        pygame.draw.rect(surface, color, (cx + gap, cy - bar_h // 2, bar_w, bar_h), border_radius=2)

    elif icon_type == 'play':
        pts = [(cx - r // 2, cy - r * 0.7), (cx + r * 0.7, cy), (cx - r // 2, cy + r * 0.7)]
        pygame.draw.polygon(surface, color, pts)

    elif icon_type == 'speed':
        # Double chevron forward
        w = r * 0.6
        pts1 = [(cx - r * 0.6, cy - r * 0.6), (cx, cy), (cx - r * 0.6, cy + r * 0.6)]
        pts2 = [(cx, cy - r * 0.6), (cx + r * 0.6, cy), (cx, cy + r * 0.6)]
        pygame.draw.lines(surface, color, False, pts1, width=3)
        pygame.draw.lines(surface, color, False, pts2, width=3)

    elif icon_type == 'arrow_left':
        pts = [(cx + r * 0.4, cy - r * 0.6), (cx - r * 0.4, cy), (cx + r * 0.4, cy + r * 0.6)]
        pygame.draw.lines(surface, color, False, pts, width=3)

    elif icon_type == 'close':
        off = int(r * 0.6)
        pygame.draw.line(surface, color, (cx - off, cy - off), (cx + off, cy + off), width=3)
        pygame.draw.line(surface, color, (cx - off, cy + off), (cx + off, cy - off), width=3)

    elif icon_type == 'shield':
        pts = [
            (cx, cy - r),
            (cx + r * 0.8, cy - r * 0.5),
            (cx + r * 0.6, cy + r * 0.5),
            (cx, cy + r),
            (cx - r * 0.6, cy + r * 0.5),
            (cx - r * 0.8, cy - r * 0.5)
        ]
        pygame.draw.polygon(surface, color, pts)
        pygame.draw.polygon(surface, (255, 255, 255, 100), pts, width=2)

    elif icon_type == 'wave':
        # Skull or wavy combat marker
        pygame.draw.circle(surface, color, (cx, cy - r // 4), int(r * 0.65))
        pygame.draw.rect(surface, color, (cx - r // 3, cy, r * 2 // 3, r // 2), border_radius=2)
        # Eye sockets
        pygame.draw.circle(surface, (20, 20, 30), (cx - r // 4, cy - r // 4), max(1, r // 6))
        pygame.draw.circle(surface, (20, 20, 30), (cx + r // 4, cy - r // 4), max(1, r // 6))

    else:
        # Default dot
        pygame.draw.circle(surface, color, (cx, cy), r // 2)

# ==============================================================================
# PROGRESS BAR WITH SMOOTH INTERPOLATION & GLOW
# ==============================================================================
def draw_modern_bar(surface, rect, current, max_val, fill_color, bg_color=None, border_color=None, 
                    radius=6, label=None, icon=None):
    rect = pygame.Rect(rect)
    if bg_color is None:
        bg_color = (20, 30, 48, 230)
    if border_color is None:
        border_color = (60, 80, 110, 200)

    # Background channel
    draw_rounded_rect(surface, bg_color, rect, radius=radius, border_color=border_color, border_width=1)
    
    # Fill calculation
    ratio = max(0.0, min(1.0, current / max(1, max_val)))
    fill_width = int((rect.width - 2) * ratio)
    
    if fill_width > 4:
        fill_rect = pygame.Rect(rect.x + 1, rect.y + 1, fill_width, rect.height - 2)
        # Gradient effect (top lighter, bottom darker)
        fill_surf = pygame.Surface(fill_rect.size, pygame.SRCALPHA)
        c_light = tuple(min(255, c + 35) for c in fill_color[:3])
        c_dark = tuple(max(0, c - 25) for c in fill_color[:3])
        
        pygame.draw.rect(fill_surf, fill_color, fill_surf.get_rect(), border_radius=radius)
        # Top gloss strip
        gloss_rect = pygame.Rect(0, 0, fill_width, max(1, fill_rect.height // 2))
        gloss_color = (255, 255, 255, 45)
        pygame.draw.rect(fill_surf, gloss_color, gloss_rect, border_top_left_radius=radius, border_top_right_radius=radius)
        surface.blit(fill_surf, fill_rect.topleft)

    # Optional icon
    icon_offset = 0
    if icon:
        draw_icon(surface, icon, rect.x + 14, rect.centery, size=rect.height - 6)
        icon_offset = 18

    # Optional text label
    if label:
        font = get_font(max(11, int(rect.height * 0.65)), bold=True)
        draw_text_with_shadow(surface, label, font, COLORS['white'], (rect.centerx + icon_offset // 2, rect.centery), align='center')

# ==============================================================================
# MODERN INTERACTIVE BUTTON
# ==============================================================================
class ModernButton:
    def __init__(self, rect, text, icon=None, style='primary', font_size=18, radius=8, tooltip=None, enabled=True):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.icon = icon
        self.style = style
        self.font_size = font_size
        self.radius = radius
        self.tooltip = tooltip
        self.enabled = enabled
        
        # State & Animation
        self.is_hovered = False
        self.is_pressed = False
        self.hover_progress = 0.0  # 0.0 to 1.0 smooth float
        self.click_cooldown = 0
        
    def set_enabled(self, enabled):
        self.enabled = enabled

    def update(self, mouse_pos, dt=0.033):
        if not self.enabled:
            self.is_hovered = False
            self.is_pressed = False
            self._pressed_inside = False
            self.hover_progress = 0.0
            return

        self.is_hovered = self.rect.collidepoint(mouse_pos)
        target_hover = 1.0 if self.is_hovered else 0.0
        # Smooth interpolation
        speed = 10.0
        self.hover_progress += (target_hover - self.hover_progress) * min(1.0, speed * dt)

        # Real-time mouse pressed state detection
        mouse_pressed = pygame.mouse.get_pressed()[0]
        if not mouse_pressed:
            self.is_pressed = False
            self._pressed_inside = False
        elif self.is_hovered and getattr(self, '_pressed_inside', False):
            self.is_pressed = True
        elif not self.is_hovered:
            self.is_pressed = False
        
    def draw(self, surface, mouse_pos=None):
        if mouse_pos:
            self.update(mouse_pos)

        # Style colors
        if not self.enabled:
            bg_col = (40, 50, 65, 180)
            border_col = (70, 80, 95, 150)
            text_col = COLORS['text_dim']
            icon_col = COLORS['text_dim']
        elif self.style == 'primary':  # Gold
            # Blend normal to hover
            r = int(COLORS['gold'][0] + (COLORS['gold_light'][0] - COLORS['gold'][0]) * self.hover_progress)
            g = int(COLORS['gold'][1] + (COLORS['gold_light'][1] - COLORS['gold'][1]) * self.hover_progress)
            b = int(COLORS['gold'][2] + (COLORS['gold_light'][2] - COLORS['gold'][2]) * self.hover_progress)
            bg_col = (r, g, b)
            border_col = (255, 230, 140) if self.hover_progress > 0.5 else (180, 110, 6)
            text_col = (20, 15, 5)  # Dark crisp text for gold button
            icon_col = (20, 15, 5)
        elif self.style == 'success':  # Green
            r = int(COLORS['green'][0] + (COLORS['green_light'][0] - COLORS['green'][0]) * self.hover_progress)
            g = int(COLORS['green'][1] + (COLORS['green_light'][1] - COLORS['green'][1]) * self.hover_progress)
            b = int(COLORS['green'][2] + (COLORS['green_light'][2] - COLORS['green'][2]) * self.hover_progress)
            bg_col = (r, g, b)
            border_col = (110, 235, 180) if self.hover_progress > 0.5 else (6, 95, 70)
            text_col = (5, 25, 15)
            icon_col = (5, 25, 15)
        elif self.style == 'danger':  # Red
            r = int(COLORS['red'][0] + (COLORS['red_light'][0] - COLORS['red'][0]) * self.hover_progress)
            g = int(COLORS['red'][1] + (COLORS['red_light'][1] - COLORS['red'][1]) * self.hover_progress)
            b = int(COLORS['red'][2] + (COLORS['red_light'][2] - COLORS['red'][2]) * self.hover_progress)
            bg_col = (r, g, b)
            border_col = (255, 180, 180) if self.hover_progress > 0.5 else (153, 27, 27)
            text_col = COLORS['white']
            icon_col = COLORS['white']
        elif self.style == 'cyan':  # Cyan
            r = int(COLORS['cyan'][0] + (COLORS['cyan_light'][0] - COLORS['cyan'][0]) * self.hover_progress)
            g = int(COLORS['cyan'][1] + (COLORS['cyan_light'][1] - COLORS['cyan'][1]) * self.hover_progress)
            b = int(COLORS['cyan'][2] + (COLORS['cyan_light'][2] - COLORS['cyan'][2]) * self.hover_progress)
            bg_col = (r, g, b)
            border_col = (180, 230, 255) if self.hover_progress > 0.5 else (7, 89, 133)
            text_col = (5, 20, 35)
            icon_col = (5, 20, 35)
        elif self.style == 'purple':  # Purple
            r = int(COLORS['purple'][0] + (COLORS['purple_light'][0] - COLORS['purple'][0]) * self.hover_progress)
            g = int(COLORS['purple'][1] + (COLORS['purple_light'][1] - COLORS['purple'][1]) * self.hover_progress)
            b = int(COLORS['purple'][2] + (COLORS['purple_light'][2] - COLORS['purple'][2]) * self.hover_progress)
            bg_col = (r, g, b)
            border_col = (220, 200, 255) if self.hover_progress > 0.5 else (90, 40, 180)
            text_col = COLORS['white']
            icon_col = COLORS['white']
        elif self.style == 'glass':  # Dark slate glass
            alpha = int(180 + 50 * self.hover_progress)
            bg_col = (25, 35, 55, alpha)
            border_col = (56, 189, 248, int(120 + 120 * self.hover_progress))
            text_col = COLORS['white'] if self.hover_progress > 0.3 else COLORS['text_secondary']
            icon_col = COLORS['cyan_light'] if self.hover_progress > 0.3 else COLORS['text_muted']
        else:  # Secondary / Neutral
            bg_col = (45, 55, 75)
            border_col = COLORS['border_light']
            text_col = COLORS['white']
            icon_col = COLORS['white']

        # Interactive Button Press effect: slightly shrink, shift down, and darken
        draw_rect = self.rect.copy()
        if self.is_pressed and self.enabled:
            # 1. Giảm nhẹ kích thước (~4-5%)
            shrink_w = max(2, int(self.rect.width * 0.04))
            shrink_h = max(2, int(self.rect.height * 0.05))
            draw_rect.x += shrink_w // 2
            draw_rect.width -= shrink_w
            draw_rect.height -= shrink_h
            # 2. Dịch xuống vài pixel (shift down 3px)
            draw_rect.y += shrink_h // 2 + 3
            # 3. Tối nhẹ (darken colors by ~25%)
            bg_col = tuple(max(0, int(c * 0.75)) for c in bg_col[:3]) + (bg_col[3:] if len(bg_col) > 3 else ())
            border_col = tuple(max(0, int(c * 0.70)) for c in border_col[:3]) + (border_col[3:] if len(border_col) > 3 else ())
        elif self.hover_progress > 0.1 and self.enabled:
            # Slight lift on hover
            draw_rect.y -= int(2 * self.hover_progress)

        # Glow behind button on hover (suppressed when pressed)
        if self.hover_progress > 0.1 and self.enabled and not self.is_pressed and self.style in ('primary', 'success', 'danger', 'cyan', 'purple'):
            glow_surf = pygame.Surface((draw_rect.width + 12, draw_rect.height + 12), pygame.SRCALPHA)
            glow_col = bg_col[:3] + (int(70 * self.hover_progress),)
            pygame.draw.rect(glow_surf, glow_col, glow_surf.get_rect(), border_radius=self.radius + 4)
            surface.blit(glow_surf, (draw_rect.x - 6, draw_rect.y - 6))

        # Main button surface
        curr_radius = max(2, self.radius - 1) if self.is_pressed else self.radius
        draw_rounded_rect(surface, bg_col, draw_rect, radius=curr_radius, border_color=border_col, border_width=2 if self.hover_progress > 0.5 else 1)

        # Top shine line for 3D feel (hidden when pressed down)
        if self.enabled and not self.is_pressed:
            shine_surf = pygame.Surface((max(1, draw_rect.width - curr_radius * 2), 1), pygame.SRCALPHA)
            shine_surf.fill((255, 255, 255, int(70 + 60 * self.hover_progress)))
            surface.blit(shine_surf, (draw_rect.x + curr_radius, draw_rect.y + 1))

        # Inner shadow / dark overlay when pressed
        if self.is_pressed and self.enabled:
            shadow_surf = pygame.Surface(draw_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(shadow_surf, (0, 0, 0, 50), shadow_surf.get_rect(), border_radius=curr_radius)
            surface.blit(shadow_surf, draw_rect.topleft)

        # Text and Icon positioning
        font = get_font(self.font_size, bold=True)
        if self.is_pressed and self.enabled:
            t_col = tuple(max(0, int(c * 0.85)) for c in text_col[:3]) + (text_col[3:] if len(text_col) > 3 else ())
            i_col = tuple(max(0, int(c * 0.85)) for c in icon_col[:3]) + (icon_col[3:] if len(icon_col) > 3 else ())
        else:
            t_col = text_col
            i_col = icon_col

        text_surf = font.render(self.text, True, t_col)
        
        if self.icon:
            icon_size = max(14, int(self.font_size * 1.1))
            total_w = icon_size + 8 + text_surf.get_width()
            start_x = draw_rect.centerx - total_w // 2
            
            draw_icon(surface, self.icon, start_x + icon_size // 2, draw_rect.centery, size=icon_size, color=i_col)
            surface.blit(text_surf, (start_x + icon_size + 8, draw_rect.centery - text_surf.get_height() // 2))
        else:
            surface.blit(text_surf, text_surf.get_rect(center=draw_rect.center))

    def handle_event(self, event):
        if not self.enabled:
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                self._pressed_inside = True
                return False
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            was_pressed = self.is_pressed or getattr(self, '_pressed_inside', False)
            self.is_pressed = False
            self._pressed_inside = False
            if was_pressed and self.rect.collidepoint(event.pos):
                try:
                    sound = pygame.mixer.Sound('sounds/click.mp3')
                    sound.set_volume(0.4)
                    sound.play()
                except Exception:
                    pass
                return True
            
        return False

# ==============================================================================
# MODERN SLIDER (For Music & SFX Settings)
# ==============================================================================
class ModernSlider:
    def __init__(self, rect, min_val=0.0, max_val=1.0, current_val=0.5, label='Volume', show_pct=True, on_change=None):
        self.rect = pygame.Rect(rect)
        self.min_val = min_val
        self.max_val = max_val
        self.value = current_val
        self.label = label
        self.show_pct = show_pct
        self.on_change = on_change
        self.is_dragging = False

    def update_value_from_mouse(self, mouse_x):
        track_left = self.rect.x + 120
        track_w = self.rect.width - 170
        ratio = max(0.0, min(1.0, (mouse_x - track_left) / max(1, track_w)))
        self.value = self.min_val + ratio * (self.max_val - self.min_val)
        if self.on_change:
            self.on_change(self.value)

    def draw(self, surface, mouse_pos):
        # Label
        font = get_font(16, bold=True)
        draw_text_with_shadow(surface, self.label, font, COLORS['text_secondary'], (self.rect.x, self.rect.centery), align='midleft')

        # Track bounds
        track_left = self.rect.x + 120
        track_w = self.rect.width - 170
        track_h = 8
        track_y = self.rect.centery - track_h // 2
        track_rect = pygame.Rect(track_left, track_y, track_w, track_h)

        # Draw track background
        draw_rounded_rect(surface, (30, 40, 60), track_rect, radius=4, border_color=COLORS['border_subtle'])

        # Filled portion
        ratio = (self.value - self.min_val) / max(0.001, (self.max_val - self.min_val))
        fill_w = int(track_w * ratio)
        if fill_w > 0:
            fill_rect = pygame.Rect(track_left, track_y, fill_w, track_h)
            draw_rounded_rect(surface, COLORS['cyan'], fill_rect, radius=4)

        # Thumb (Draggable handle)
        thumb_x = track_left + fill_w
        thumb_y = self.rect.centery
        thumb_r = 9
        thumb_color = COLORS['white'] if self.is_dragging or (mouse_pos and math.hypot(mouse_pos[0]-thumb_x, mouse_pos[1]-thumb_y) < 14) else COLORS['cyan_light']
        
        # Glow
        if self.is_dragging:
            pygame.draw.circle(surface, (14, 165, 233, 90), (thumb_x, thumb_y), thumb_r + 4)
        pygame.draw.circle(surface, thumb_color, (thumb_x, thumb_y), thumb_r)
        pygame.draw.circle(surface, COLORS['bg_dark'], (thumb_x, thumb_y), 3)

        # Percentage label
        if self.show_pct:
            pct_text = f"{int(self.value * 100)}%"
            draw_text_with_shadow(surface, pct_text, font, COLORS['gold_light'], (self.rect.right - 10, self.rect.centery), align='midright')

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            track_left = self.rect.x + 120
            track_w = self.rect.width - 170
            hit_box = pygame.Rect(track_left - 10, self.rect.y, track_w + 20, self.rect.height)
            if hit_box.collidepoint(event.pos):
                self.is_dragging = True
                self.update_value_from_mouse(event.pos[0])
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_dragging:
                self.is_dragging = False
                return True
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            self.update_value_from_mouse(event.pos[0])
            return True
        return False

# ==============================================================================
# MODERN TOGGLE SWITCH
# ==============================================================================
class ModernToggle:
    def __init__(self, rect, is_on=True, label='BẬT/TẮT', on_toggle=None):
        self.rect = pygame.Rect(rect)
        self.is_on = is_on
        self.label = label
        self.on_toggle = on_toggle

    def draw(self, surface, mouse_pos):
        font = get_font(16, bold=True)
        draw_text_with_shadow(surface, self.label, font, COLORS['text_secondary'], (self.rect.x, self.rect.centery), align='midleft')

        # Switch pill
        pill_w = 46
        pill_h = 24
        pill_rect = pygame.Rect(self.rect.right - pill_w, self.rect.centery - pill_h // 2, pill_w, pill_h)

        bg_col = COLORS['green'] if self.is_on else (50, 60, 80)
        border_col = COLORS['green_light'] if self.is_on else COLORS['border_light']
        draw_rounded_rect(surface, bg_col, pill_rect, radius=12, border_color=border_col, border_width=1)

        # Circle thumb
        thumb_r = 9
        thumb_x = pill_rect.right - thumb_r - 3 if self.is_on else pill_rect.left + thumb_r + 3
        pygame.draw.circle(surface, COLORS['white'], (thumb_x, pill_rect.centery), thumb_r)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_on = not self.is_on
                try:
                    sound = pygame.mixer.Sound('sounds/click.mp3')
                    sound.set_volume(0.35)
                    sound.play()
                except Exception:
                    pass
                if self.on_toggle:
                    self.on_toggle(self.is_on)
                return True
        return False

# ==============================================================================
# MODERN TOAST NOTIFICATION SYSTEM
# ==============================================================================
class ToastNotification:
    def __init__(self, title, message="", icon="trophy", duration=3.0, border_color=None):
        self.title = title
        self.message = message
        self.icon = icon
        self.duration = duration
        self.start_time = time.time()
        self.border_color = border_color or COLORS['gold']
        self.width = 280
        self.height = 64

    def is_expired(self):
        return (time.time() - self.start_time) > self.duration

    def get_progress(self):
        elapsed = time.time() - self.start_time
        return max(0.0, min(1.0, 1.0 - (elapsed / self.duration)))

    def draw(self, surface, x, y):
        elapsed = time.time() - self.start_time
        # Slide in animation
        slide_offset = 0
        if elapsed < 0.25:
            slide_offset = int((1.0 - elapsed / 0.25) * 80)
        elif elapsed > (self.duration - 0.25):
            slide_offset = int(((elapsed - (self.duration - 0.25)) / 0.25) * 80)

        card_rect = pygame.Rect(x + slide_offset, y, self.width, self.height)
        
        # Glass card
        draw_glass_card(surface, card_rect, radius=10, bg_color=(15, 23, 42, 235), border_color=self.border_color, border_width=2)
        
        # Icon
        draw_icon(surface, self.icon, card_rect.x + 24, card_rect.centery, size=24, color=self.border_color)
        
        # Texts
        title_font = get_font(15, bold=True)
        msg_font = get_font(13, bold=False)
        draw_text_with_shadow(surface, self.title, title_font, COLORS['white'], (card_rect.x + 48, card_rect.y + 12), align='topleft')
        if self.message:
            draw_text_with_shadow(surface, self.message, msg_font, COLORS['text_muted'], (card_rect.x + 48, card_rect.y + 32), align='topleft')

        # Remaining time bar at bottom
        prog = self.get_progress()
        if prog > 0:
            prog_w = int((card_rect.width - 4) * prog)
            bar_rect = pygame.Rect(card_rect.x + 2, card_rect.bottom - 4, prog_w, 2)
            pygame.draw.rect(surface, self.border_color, bar_rect, border_radius=1)
