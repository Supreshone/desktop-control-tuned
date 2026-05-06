# Desktop Control — Tuned Edition

> **Python-powered Windows desktop automation for AI agents**

Mouse, keyboard, screenshots, image recognition, window management, clipboard — all in one Python module, built for OpenClaw and any AI agent that needs to control a Windows desktop.

---

## Features

| Category | Capabilities |
|----------|-------------|
| **Mouse** | Move, click, double-click, right-click, drag, scroll, get position |
| **Keyboard** | Type text, press keys, hotkey combos (Ctrl+C, Alt+F4, etc.), key down/up |
| **Screen** | Full screenshot, region screenshot, pixel color, image matching (`find_on_screen`), wait for image to appear |
| **Window** | List all windows, activate, get active window, close by title |
| **Clipboard** | Copy to / paste from system clipboard |
| **Safety** | Built-in FAILSAFE — move mouse to any screen corner to abort |

---

## Installation

```powershell
# Install dependencies (one-time)
python -m pip install pyautogui pillow opencv-python pygetwindow pyperclip
```

Or install everything at once:

```powershell
pip install pyautogui pillow opencv-python pygetwindow pyperclip
```

> **Note:** This is a Python module, not a shell script. Requires Python 3.8+ on Windows.

---

## Quick Start

```python
from desktop_control import DesktopController

dc = DesktopController()  # FAILSAFE enabled by default

# Mouse movement
dc.move_mouse(960, 540, duration=1.0)   # Smooth move to screen center
dc.click(500, 300)                        # Left click
dc.double_click(500, 300)                # Double click
dc.right_click(960, 540)                 # Right click

# Keyboard
dc.type_text("Hello World", interval=0)    # Instant text input
dc.hotkey("ctrl", "a")                    # Ctrl+A
dc.hotkey("ctrl", "s")                    # Ctrl+S
dc.hotkey("alt", "f4")                    # Close window

# Screenshot
img = dc.screenshot()                                       # Returns PIL Image
dc.screenshot(filename="C:/temp/screen.png")                # Save to file
img = dc.screenshot(region=(0, 0, 800, 600))               # Capture region

# Image matching — wait for popup, then click button
pos = dc.find_on_screen("confirm_button.png", confidence=0.85)
if pos:
    cx = pos[0] + pos[2] // 2   # center X of found image
    cy = pos[1] pos[3] // 2   # center Y
    dc.click(cx, cy)

# Wait for image with timeout (waits for a popup to appear)
result = dc.wait_for_image("popup.png", timeout=15, interval=0.5)
if result:
    print("Popup appeared!")

# Pixel color
r, g, b = dc.get_pixel_color(960, 540)
print(f"Center pixel: RGB({r},{g},{b})")

# Windows
dc.activate_window("Notepad")
dc.close_window("Notepad")

# Clipboard
dc.copy_to_clipboard("Text to copy")
text = dc.get_from_clipboard()
```

---

## Image Matching — The Key Feature

Unlike basic automation tools, this module supports **OpenCV-powered image matching**:

```python
# Wait for a popup dialog to appear, then automatically click "OK"
pos = dc.wait_for_image("ok_button.png", timeout=20, interval=0.5)
if pos:
    dc.click(pos[0] + pos[2]//2, pos[1] + pos[3]//2)
    print("Button clicked!")
else:
    print("Timeout — popup didn't appear")

# Detect if a specific element is on screen
pos = dc.find_on_screen("error_icon.png", confidence=0.9)
if pos:
    print(f"Error icon found at ({pos[0]}, {pos[1]})")
```

This is what makes it suitable for **AI agents** — the agent can wait for a response UI before proceeding to the next step.

---

## Safety

- **FAILSAFE**: Move the mouse to any corner of the screen and all operations stop immediately
- `dc.is_safe()` — check current safety status before running a critical sequence
- All coordinates are absolute (not relative) for predictable behavior

---

## Requirements

- Windows 10/11
- Python 3.8+
- `pyautogui`, `pillow`, `opencv-python`, `pygetwindow`, `pyperclip`

---

## Full Method Reference

### Mouse
`move_mouse(x, y, duration=0)` · `move_relative(dx, dy)` · `click(x, y, button='left', clicks=1)` · `double_click(x, y)` · `right_click(x, y)` · `drag(start_x, start_y, end_x, end_y, duration=0.5)` · `scroll(clicks)` · `get_mouse_position()`

### Keyboard
`type_text(text, interval=0)` · `press(key)` · `hotkey(*keys)` · `key_down(key)` · `key_up(key)`

### Screen
`screenshot(region=None, filename=None)` · `get_pixel_color(x, y)` · `find_on_screen(image_path, confidence=0.8, region=None)` · `wait_for_image(image_path, timeout=10, interval=0.5)` · `get_screen_size()`

### Window
`get_all_windows()` · `activate_window(title_substring)` · `get_active_window()` · `close_window(title_substring)`

### Clipboard
`copy_to_clipboard(text)` · `get_from_clipboard()`

### Utility
`pause(seconds)` · `is_safe()`

---

## OpenClaw Integration

This module is designed as an OpenClaw skill. Drop it into your workspace and import:

```python
from desktop_control import DesktopController
dc = DesktopController()
```

See `SKILL.md` for detailed OpenClaw-specific usage patterns.

---

## License

MIT License — free to use, modify, and distribute.