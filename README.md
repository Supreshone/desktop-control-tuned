# Desktop Control

> 接管 Windows 桌面 — 鼠标、键盘、截图、找图、窗口、剪贴板

Python 模块，专为 OpenClaw / AI Agent 打造，也可独立使用。

## 安装

```powershell
# 安装依赖（一次即可）
python -m pip install pyautogui pillow opencv-python pygetwindow pyperclip

# 或者一键安装全部
pip install pyautogui pillow opencv-python pygetwindow pyperclip
```

## 快速开始

```python
from desktop_control import DesktopController
dc = DesktopController()  # FAILSAFE 启用（鼠标到四角停止）

# 鼠标
dc.move_mouse(960, 540, duration=1.0)   # 平滑移到中心
dc.click(500, 300)                       # 单击
dc.double_click(500, 300)               # 双击
dc.right_click(960, 540)               # 右键

# 键盘
dc.type_text("你好万哥", interval=0)     # 瞬间输入
dc.hotkey("ctrl", "a")                  # Ctrl+A
dc.hotkey("ctrl", "s")                  # Ctrl+S

# 屏幕
img = dc.screenshot(filename="screen.png")                    # 截图保存
r, g, b = dc.get_pixel_color(960, 540)                        # 取色
pos = dc.find_on_screen("confirm_button.png", confidence=0.85)  # 找图
result = dc.wait_for_image("popup.png", timeout=15)           # 等弹窗

# 窗口
dc.activate_window("Notepad")
dc.close_window("Notepad")

# 剪贴板
dc.copy_to_clipboard("要复制的内容")
text = dc.get_from_clipboard()
```

## 找图匹配 — 核心功能

这是 Python 版区别于 PowerShell 版的独家能力：

```python
# 等待弹窗出现，再点击"确定"按钮
pos = dc.wait_for_image("ok_button.png", timeout=20, interval=0.5)
if pos:
    cx = pos[0] + pos[2] // 2
    cy = pos[1] + pos[3] // 2
    dc.click(cx, cy)
    print("按钮已点击")
else:
    print("超时，弹窗未出现")
```

## 安全机制

- **FAILSAFE**：鼠标移到屏幕任意一角，立即停止所有操作
- `dc.is_safe()` 检查当前状态

## 完整文档

[→ 查看 SKILL.md](SKILL.md)