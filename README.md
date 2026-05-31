# Bubbles.scr — Python Remake (PyQt6)

**A nostalgic tribute to the legendary Windows screensaver — now in Python.**

Do you love the classic `Bubbles.scr`? Would you like to watch bubbles drift across your screen while you go about your business? Then this repository is for you!

This is **a Python recreation** of the iconic screensaver using **PyQt6** — with real‑time physics, smooth animations, and bubble collisions.

## ✨ Features

- 🫧 Realistic bubble movement and bouncing
- 💥 Bubble collision detection with momentum exchange
- 🖥️ Full‑screen overlay, transparent for input (doesn't interfere with your work)
- ⚙️ Adjustable settings: max bubbles, spawn interval, size, speed
- 🎨 Dynamic hue cycling — bubbles subtly change color over time

## ⚠️ Known Limitation

> **Only 3 bubble textures (colors) are available** — blue, purple, and red.  
> Unlike the original which had more color variations, this remake uses these three base textures with dynamic hue shifting to add visual variety.

*The dynamic hue cycling partially compensates for the limited palette, giving each bubble a gentle color drift over time.*

## 🚀 Getting Started

### Requirements

- Python 3.8+
- PyQt6

### Installation

```bash
pip install PyQt6
git clone https://github.com/podsolnyh122/bubbles-screensaver-clone.git
cd bubbles-screensaver-clone
python Bubbles.py
```

### Customization

Edit the constants at the top of the script:

```python
MAX_BUBBLES = 20          # Maximum bubbles on screen
SPAWN_INTERVAL_MS = 1200  # Milliseconds between new bubbles
SIZE = 175                # Bubble size in pixels
SPEED = [3.5, 6.0]        # Min / max speed
```
## 📁 Assets

Place your bubble textures (PNG with transparency) in the same folder as the script. Default names:

- `bubble-blue.png`
- `bubble-purple.png`
- `bubble-red.png`

## 🙏 Credits

Inspired by the classic Windows `Bubbles.scr` screensaver. This is **not an exact copy** — it's a handmade tribute written from scratch in Python.
