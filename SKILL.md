---
name: desktop-control-tuned
description: >
  Automate Windows desktop programmatically — mouse, keyboard, screenshots, image matching,
  window management, clipboard. Use when you need to control the desktop: click buttons,
  fill forms, open files, capture screens, wait for popups. Written in Python.
---

# Desktop Control (Tuned)

Python-based Windows desktop automation for AI agents.

## Installation

```powershell
python -m pip install pyautogui pillow opencv-python pygetwindow pyperclip
```

## Import

```python
from desktop_control import DesktopController
dc = DesktopController()  # FAILSAFE enabled by default
```

> Module location: `C:\Users\Administrator\.openclaw\workspace\desktop_control\`

---

## Mouse

```python
dc.move_mouse(500, 300, duration=0.5)   # Smooth move to (500,300)
dc.click(500, 300)                      # Left click
dc.double_click(500, 300)               # Double click
dc.right_click(500, 300)               # Right click
dc.drag(100, 100, 500, 500)            # Drag from (100,100) to (500,500)
dc.scroll(3)                            # Scroll up 3 clicks
dc.get_mouse_position()                 # Returns (x, y)
```

---

## Keyboard

```python
dc.type_text("Hello World", interval=0)  # Instant text
dc.press("enter")                       # Press Enter
dc.hotkey("ctrl", "s")                  # Ctrl+S
dc.hotkey("alt", "f4")                  # Alt+F4
dc.hotkey("ctrl", "a")                  # Ctrl+A
dc.hotkey("ctrl", "v")                  # Ctrl+V
```

---

## Screen

```python
# Screenshot
img = dc.screenshot()                                     # Returns PIL Image
dc.screenshot(filename="C:/temp/screen.png")                # Save to file
img = dc.screenshot(region=(0, 0, 800, 600))              # Capture region (left, top, width, height)

# Pixel color
r, g, b = dc.get_pixel_color(960, 540)

# Image matching — the core AI-friendly feature
pos = dc.find_on_screen("C:/temp/button.png", confidence=0.85)
if pos:
    cx = pos[0] + pos[2] // 2   # center X
    cy = pos[1] + pos[3] // 2   # center Y
    dc.click(cx, cy)

# Wait for image to appear (waits for popup, loading screen, etc.)
result = dc.wait_for_image("C:/temp/confirm.png", timeout=10, interval=0.5)
if result:
    print("Image appeared!")
else:
    print("Timeout — image never appeared")
```

---

## Window

```python
dc.get_all_windows()       # List all window titles
dc.get_active_window()    # Current active window
dc.activate_window("Notepad")   # Activate window (partial match)
dc.close_window("Notepad")     # Close window
```

---

## Clipboard

```python
dc.copy_to_clipboard("Text to copy")
text = dc.get_from_clipboard()
```

---

## Common Patterns

```python
# Open a file using Win+R
dc.hotkey("win", "r")
dc.type_text("notepad.exe", interval=0)
dc.press("enter")
# OR
import subprocess
subprocess.Popen(["notepad.exe", "test.txt"])
```

```python
# Wait for popup then click "OK"
pos = dc.wait_for_image("C:/temp/ok_button.png", timeout=20)
if pos:
    dc.click(pos[0] + pos[2]//2, pos[1] + pos[3]//2)
    print("Clicked!")
```

```python
# Screenshot + pixel check (verify UI state)
dc.screenshot(filename="C:/temp/screen.png")
r, g, b = dc.get_pixel_color(960, 540)
if (r, g, b) == (30, 90, 170):
    print("Button is blue — state is correct")
```

---

## Safety

- **FAILSAFE**: Move mouse to any screen corner → all operations stop immediately
- `dc.is_safe()` — check if safe to continue
- Always `activate_window()` or click inside the target window before performing actions

---

## Complete Method Reference

| Category | Methods |
|----------|---------|
| Mouse | `move_mouse`, `move_relative`, `click`, `double_click`, `right_click`, `drag`, `scroll`, `get_mouse_position` |
| Keyboard | `type_text`, `press`, `hotkey`, `key_down`, `key_up` |
| Screen | `screenshot`, `get_pixel_color`, `find_on_screen`, `wait_for_image`, `get_screen_size` |
| Window | `get_all_windows`, `activate_window`, `get_active_window`, `close_window` |
| Clipboard | `copy_to_clipboard`, `get_from_clipboard` |
| Utility | `pause(seconds)`, `is_safe()` |