import sys
import os
import random
import math
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QPixmap, QColor

# --- Settings ---
MAX_BUBBLES = 20
SPAWN_INTERVAL_MS = 1200
SIZE = 175
SPEED = [3.5, 6.0]
# ------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Bubble:
    def __init__(self, texture_filenames, screen_width, screen_height):
        chosen_filename = random.choice(texture_filenames)
        full_path = os.path.join(BASE_DIR, chosen_filename)
        
        self.base_pixmap = QPixmap(full_path)
        
        if self.base_pixmap.isNull():
            print(f"Error file not found: {full_path}")
            sys.exit(1)
        
        self.size = SIZE
        self.radius = self.size / 2
        
        self.base_pixmap = self.base_pixmap.scaled(
            self.size, self.size, 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
        )
        
        spawn_edge = random.choice([0, 1])
        
        if spawn_edge == 0:  
            self.x = -self.size + 5
            self.y = random.uniform(50, screen_height - self.size - 50)
            self.dx = random.uniform(SPEED[0], SPEED[1])
            self.dy = random.uniform(-1.5, 1.5)
        else:                
            self.x = random.uniform(50, screen_width - self.size - 50)
            self.y = screen_height - 5
            self.dx = random.uniform(-2.5, 2.5)
            self.dy = random.uniform(-6.0, -3.5) 
        
        self.hue = random.randint(0, 360)
        self.hue_speed = random.uniform(1.0, 2.0) 
        self.mass = self.radius ** 2

    def move(self, screen_width, screen_height):
        self.x += self.dx
        self.y += self.dy
        self.hue = (self.hue + self.hue_speed) % 360
        
        if self.x <= 0 and self.dx < 0:
            self.dx = abs(self.dx)
        elif self.x >= screen_width - self.size and self.dx > 0:
            self.dx = -abs(self.dx)
            
        if self.y <= 0 and self.dy < 0:
            self.dy = abs(self.dy)
        elif self.y >= screen_height - self.size and self.dy > 0:
            self.dy = -abs(self.dy)

    def check_collision(self, other):
        x1, y1 = self.x + self.radius, self.y + self.radius
        x2, y2 = other.x + other.radius, other.y + other.radius
        
        dx = x2 - x1
        dy = y2 - y1
        distance = math.hypot(dx, dy)
        min_dist = self.radius + other.radius
        
        if distance < min_dist and distance > 0:
            nx = dx / distance
            ny = dy / distance
            
            overlap = min_dist - distance
            self.x -= nx * overlap * 0.5
            self.y -= ny * overlap * 0.5
            other.x += nx * overlap * 0.5
            other.y += ny * overlap * 0.5
            
            kx = self.dx - other.dx
            ky = self.dy - other.dy
            p = 2 * (nx * kx + ny * ky) / (self.mass + other.mass)
            
            self.dx -= p * other.mass * nx
            self.dy -= p * other.mass * ny
            other.dx += p * self.mass * nx
            other.dy += p * self.mass * ny

class ScreensaverOverlay(QWidget):
    def __init__(self):
        super().__init__()
        
        self.texture_filenames = ['bubble-blue.png', 'bubble-purple.png', 'bubble-red.png']
        self.bubbles = [] 
        
        self.init_window()
        
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(16) 
        
        self.spawn_timer = QTimer(self)
        self.spawn_timer.timeout.connect(self.spawn_bubble)
        self.spawn_timer.start(SPAWN_INTERVAL_MS)
        
        self.spawn_bubble()
        
        self.close_timer = QTimer(self)
        self.close_timer.setSingleShot(True)
        self.close_timer.timeout.connect(self.close)

    def init_window(self):
        screen = QApplication.primaryScreen().geometry()
        self.screen_w = screen.width()
        self.screen_h = screen.height()
        
        self.setGeometry(0, 0, self.screen_w, self.screen_h)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.WindowTransparentForInput
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)

    def spawn_bubble(self):
        if len(self.bubbles) < MAX_BUBBLES:
            new_bubble = Bubble(self.texture_filenames, self.screen_w, self.screen_h)
            self.bubbles.append(new_bubble)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        for bubble in self.bubbles:
            buffer = QPixmap(bubble.base_pixmap.size())
            buffer.fill(Qt.GlobalColor.transparent)
            
            buf_painter = QPainter(buffer)
            buf_painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            color = QColor.fromHsv(int(bubble.hue), 165, 255, 255)
            buf_painter.fillRect(buffer.rect(), color)
            
            buf_painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
            buf_painter.drawPixmap(0, 0, bubble.base_pixmap)
            buf_painter.end()
            
            painter.drawPixmap(int(bubble.x), int(bubble.y), buffer)

    def update_animation(self):
        for bubble in self.bubbles:
            bubble.move(self.screen_w, self.screen_h)
            
        for i in range(len(self.bubbles)):
            for j in range(i + 1, len(self.bubbles)):
                self.bubbles[i].check_collision(self.bubbles[j])
                
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    overlay = ScreensaverOverlay()
    overlay.show()
    sys.exit(app.exec())
