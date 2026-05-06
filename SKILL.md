---
name: desktop-control
description: >
  Automate Windows desktop — mouse, keyboard, screenshots, image recognition,
  window management, clipboard. Use when you need to control the desktop programmatically,
  click buttons, fill forms, open files, capture screens, or wait for popups.
---

# Desktop Control

接管 Windows 桌面。鼠标、键盘、屏幕截图、图像匹配、窗口管理、剪贴板全能。

## 安装依赖

```powershell
python -m pip install pyautogui pillow opencv-python pygetwindow pyperclip
```

## 导入

```python
from desktop_control import DesktopController
dc = DesktopController()  # 默认启用 FAILSAFE（鼠标到四角立即停止）
```

---

## 鼠标

```python
dc.move_mouse(500, 300, duration=0.5)   # 移动到 (500,300)，0.5秒平滑
dc.click(500, 300)                      # 左键单击
dc.double_click(500, 300)               # 双击
dc.right_click(500, 300)                # 右键
dc.drag(100, 100, 500, 500)             # 拖拽
dc.scroll(3)                            # 向上滚3格
dc.get_mouse_position()                 # 返回 (x, y)
```

---

## 键盘

```python
dc.type_text("Hello World", interval=0)  # 瞬间输入
dc.press("enter")                       # 按回车
dc.press("tab")
dc.hotkey("ctrl", "s")                  # Ctrl+S
dc.hotkey("alt", "f4")                  # Alt+F4
dc.hotkey("ctrl", "a")                  # Ctrl+A 全选
dc.hotkey("ctrl", "v")                  # Ctrl+V 粘贴
```

---

## 屏幕

```python
# 截图
img = dc.screenshot()                                     # 返回 PIL Image
dc.screenshot(filename="screen.png")                      # 保存文件
img = dc.screenshot(region=(0, 0, 800, 600))              # 截取区域

# 像素颜色
r, g, b = dc.get_pixel_color(960, 540)

# 找图匹配 — 等待弹窗、等待按钮出现
pos = dc.find_on_screen("button.png", confidence=0.85)
if pos:
    cx = pos[0] + pos[2] // 2  # 中心X
    cy = pos[1] + pos[3] // 2  # 中心Y
    dc.click(cx, cy)

# 等待图片出现（带超时）
result = dc.wait_for_image("confirm.png", timeout=10, interval=0.5)
if result:
    print("弹窗出现了！")
```

---

## 窗口

```python
dc.get_all_windows()       # 所有窗口标题列表
dc.get_active_window()    # 当前活动窗口
dc.activate_window("Notepad")   # 激活窗口（部分匹配）
dc.close_window("Notepad")     # 关闭窗口
```

---

## 剪贴板

```python
dc.copy_to_clipboard("要复制的内容")
text = dc.get_from_clipboard()
```

---

## 常用组合

```python
# 打开文件并输入文字（用 Win+R 方式）
import subprocess, time
filepath = "test.txt"

subprocess.Popen(["notepad.exe", filepath])
time.sleep(1)
dc.type_text("你好！")
```

```python
# 等待弹窗出现再点击按钮
pos = dc.wait_for_image("ok_button.png", timeout=15)
if pos:
    dc.click(pos[0] + pos[2]//2, pos[1] + pos[3]//2)
```

```python
# 截图分析 + 像素验证 UI 状态
import os
os.makedirs("screenshots", exist_ok=True)
dc.screenshot(filename="screenshots/current.png")
r, g, b = dc.get_pixel_color(960, 540)
if (r, g, b) == (30, 90, 170):
    print("按钮是蓝色，状态正确")
```

---

## 安全机制

- **FAILSAFE**：鼠标移动到屏幕任意一角（4个角），立即停止所有操作
- `dc.is_safe()` 检查当前是否处于安全状态
- 操作前确保目标窗口已激活（用 `activate_window` 或先点击窗口内）

---

## 完整方法列表

| 类别 | 方法 |
|------|------|
| 鼠标 | `move_mouse`, `move_relative`, `click`, `double_click`, `right_click`, `drag`, `scroll`, `get_mouse_position` |
| 键盘 | `type_text`, `press`, `hotkey`, `key_down`, `key_up` |
| 屏幕 | `screenshot`, `get_pixel_color`, `find_on_screen`, `wait_for_image`, `get_screen_size` |
| 窗口 | `get_all_windows`, `activate_window`, `get_active_window`, `close_window` |
| 剪贴板 | `copy_to_clipboard`, `get_from_clipboard` |
| 工具 | `pause(seconds)`, `is_safe()` |