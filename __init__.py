"""
desktop_control - 屏幕控制模块
用于 OpenClaw 的桌面自动化控制

使用方法:
    from desktop_control import DesktopController
    dc = DesktopController(failsafe=True)

依赖安装 (Windows PowerShell):
    python -m pip install pyautogui pillow opencv-python pygetwindow pyperclip
"""

import pyautogui
import time
import logging
from typing import Tuple, Optional, List

# Configure pyautogui for maximum responsiveness
pyautogui.MINIMUM_DURATION = 0
pyautogui.MINIMUM_SLEEP = 0
pyautogui.PAUSE = 0

# Silent logger
_log = logging.getLogger("desktop_control")
_log.setLevel(logging.WARNING)
if not _log.handlers:
    _handler = logging.StreamHandler()
    _handler.setLevel(logging.WARNING)
    _log.addHandler(_handler)


class DesktopController:
    """
    桌面自动化控制器 - 鼠标、键盘、屏幕、窗口、剪贴板全功能

    安全机制:
    - FAILSAFE: 鼠标移动到屏幕四角任意一角会立即停止所有操作
    - is_safe(): 检查当前是否安全继续
    """

    def __init__(self, failsafe: bool = True):
        pyautogui.FAILSAFE = failsafe
        self.screen_width, self.screen_height = pyautogui.size()
        self._failsafe = failsafe

    # ─── 鼠标 ───────────────────────────────────────────────

    def move_mouse(self, x: int, y: int, duration: float = 0):
        """移动鼠标到绝对坐标"""
        pyautogui.moveTo(x, y, duration=duration,
                         tween=pyautogui.easeInOutQuad if duration > 0 else None)

    def move_relative(self, dx: int, dy: int, duration: float = 0):
        """相对移动鼠标"""
        pyautogui.move(dx, dy, duration=duration)

    def click(self, x: int = None, y: int = None, button: str = 'left', clicks: int = 1):
        """点击 (x,y) 为 None 时点击当前位置"""
        pyautogui.click(x=x, y=y, clicks=clicks, button=button)

    def double_click(self, x: int = None, y: int = None):
        """双击"""
        self.click(x, y, clicks=2)

    def right_click(self, x: int = None, y: int = None):
        """右键点击"""
        self.click(x, y, button='right')

    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.5):
        """拖拽从 (start_x,start_y) 到 (end_x,end_y)"""
        pyautogui.moveTo(start_x, start_y)
        time.sleep(0.05)
        pyautogui.drag(end_x - start_x, end_y - start_y, duration=duration, button='left')

    def scroll(self, clicks: int):
        """滚动鼠标，正=上，负=下"""
        pyautogui.scroll(clicks)

    def get_mouse_position(self) -> Tuple[int, int]:
        """获取当前鼠标坐标 (x, y)"""
        pos = pyautogui.position()
        return (pos.x, pos.y)

    # ─── 键盘 ───────────────────────────────────────────────

    def type_text(self, text: str, interval: float = 0):
        """输入文本，interval=0 瞬间输入"""
        pyautogui.write(text, interval=interval)

    def press(self, key: str):
        """按下一个键 (enter/tab/escape/space/backspace/delete 等)"""
        pyautogui.press(key)

    def hotkey(self, *keys):
        """组合键，如 dc.hotkey('ctrl','c') 即 Ctrl+C"""
        pyautogui.hotkey(*keys)

    def key_down(self, key: str):
        """按住按键"""
        pyautogui.keyDown(key)

    def key_up(self, key: str):
        """释放按键"""
        pyautogui.keyUp(key)

    # ─── 屏幕 ───────────────────────────────────────────────

    def screenshot(self, region: Tuple[int, int, int, int] = None,
                  filename: str = None):
        """
        截图
        region: (left, top, width, height) 可选，只截取区域
        filename: 保存路径，为 None 时返回 PIL Image 对象
        """
        img = pyautogui.screenshot(region=region)
        if filename:
            img.save(filename)
        return img

    def get_pixel_color(self, x: int, y: int) -> Tuple[int, int, int]:
        """获取指定坐标的像素 RGB 颜色"""
        return pyautogui.pixel(x, y)

    def find_on_screen(self, image_path: str, confidence: float = 0.8,
                       region: Tuple[int, int, int, int] = None):
        """
        找图匹配 - 在屏幕上查找指定图片的位置
        用于等待弹窗、按钮出现等场景
        返回: Box (left, top, width, height) 或 None
        """
        return pyautogui.locateOnScreen(image_path, confidence=confidence, region=region)

    def wait_for_image(self, image_path: str, timeout: float = 10,
                       confidence: float = 0.8, interval: float = 0.5):
        """
        等待图片出现在屏幕上
        timeout: 最长等待秒数
        interval: 每次检测的间隔
        返回: True 找到 / False 超时
        """
        start = time.time()
        while time.time() - start < timeout:
            pos = self.find_on_screen(image_path, confidence=confidence)
            if pos:
                return pos
            time.sleep(interval)
        return None

    def get_screen_size(self) -> Tuple[int, int]:
        """获取屏幕分辨率 (width, height)"""
        return (self.screen_width, self.screen_height)

    # ─── 窗口 ───────────────────────────────────────────────

    def get_all_windows(self) -> List[str]:
        """获取所有窗口标题列表"""
        try:
            import pygetwindow as gw
            return [w for w in gw.getAllTitles() if w.strip()]
        except Exception:
            return []

    def activate_window(self, title_substring: str) -> bool:
        """激活窗口（部分匹配标题）"""
        try:
            import pygetwindow as gw
            wins = gw.getWindowsWithTitle(title_substring)
            if wins:
                wins[0].activate()
                return True
        except Exception:
            pass
        return False

    def get_active_window(self) -> str:
        """获取当前活动窗口标题"""
        try:
            import pygetwindow as gw
            w = gw.getActiveWindow()
            return w.title if w else None
        except Exception:
            return None

    def close_window(self, title_substring: str) -> bool:
        """关闭窗口（部分匹配标题）"""
        try:
            import pygetwindow as gw
            wins = gw.getWindowsWithTitle(title_substring)
            if wins:
                wins[0].close()
                return True
        except Exception:
            pass
        return False

    # ─── 剪贴板 ───────────────────────────────────────────────

    def copy_to_clipboard(self, text: str):
        """复制文本到剪贴板"""
        try:
            import pyperclip
            pyperclip.copy(text)
        except Exception:
            pass

    def get_from_clipboard(self) -> str:
        """从剪贴板获取文本"""
        try:
            import pyperclip
            return pyperclip.paste()
        except Exception:
            return ""

    # ─── 工具 ───────────────────────────────────────────────

    def pause(self, seconds: float):
        """等待指定秒数"""
        time.sleep(seconds)

    def is_safe(self) -> bool:
        """检查是否安全（鼠标不在四角角）"""
        if not self._failsafe:
            return True
        x, y = self.get_mouse_position()
        corners = [(0, 0), (self.screen_width - 1, 0),
                   (0, self.screen_height - 1),
                   (self.screen_width - 1, self.screen_height - 1)]
        for cx, cy in corners:
            if abs(x - cx) <= 5 and abs(y - cy) <= 5:
                return False
        return True


# ─── 全局快捷函数 ───────────────────────────────────────

def get_controller() -> DesktopController:
    """获取全局控制器实例"""
    global _dc
    if '_dc' not in globals():
        globals()['_dc'] = DesktopController()
    return globals()['_dc']


def move_mouse(x: int, y: int, duration: float = 0):
    get_controller().move_mouse(x, y, duration)

def click(x: int = None, y: int = None):
    get_controller().click(x, y)

def screenshot(filename: str = None):
    return get_controller().screenshot(filename=filename)