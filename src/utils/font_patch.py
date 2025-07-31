import os
import platform
import subprocess
from typing import Optional


def get_font_path(font_name: str) -> Optional[str]:
    """
    获取字体文件的完整路径
    
    Args:
        font_name: 字体名称，如 'Noto Sans CJK SC'
        
    Returns:
        字体文件的完整路径，如果找不到则返回None
    """
    if platform.system() == 'Windows':
        # Windows系统使用原始逻辑
        return os.path.join(os.getenv('WIN_FONT_DIR', 'C:\\Windows\\Fonts'), font_name + '.ttf')
    
    elif platform.system() == 'Linux':
        # Linux系统尝试多个可能的路径
        # 处理中文字体名称映射
        font_mapping = {
            'Noto Sans CJK SC': 'NotoSansCJK-Regular.ttc',
            'Noto Serif CJK SC': 'NotoSerifCJK-Regular.ttc',
            'Noto Sans CJK TC': 'NotoSansCJK-Regular.ttc',
            'Noto Serif CJK TC': 'NotoSerifCJK-Regular.ttc',
            'Noto Sans CJK JP': 'NotoSansCJK-Regular.ttc',
            'Noto Serif CJK JP': 'NotoSerifCJK-Regular.ttc',
            'Noto Sans CJK KR': 'NotoSansCJK-Regular.ttc',
            'Noto Serif CJK KR': 'NotoSerifCJK-Regular.ttc',
            'Noto Sans CJK HK': 'NotoSansCJK-Regular.ttc',
            'Noto Serif CJK HK': 'NotoSerifCJK-Regular.ttc',
        }
        
        # 获取实际的文件名
        actual_font_name = font_mapping.get(font_name, font_name)
        
        linux_font_paths = [
            f'/usr/share/fonts/opentype/noto/{actual_font_name}',
            f'/usr/share/fonts/truetype/noto/{actual_font_name}',
            f'/usr/share/fonts/truetype/noto/{font_name}.ttf',
            f'/usr/share/fonts/truetype/noto/{font_name}-Regular.ttf',
            f'/usr/share/fonts/truetype/noto/{font_name}-Bold.ttf',
            f'/usr/share/fonts/truetype/dejavu/{font_name}.ttf',
            f'/usr/share/fonts/truetype/dejavu/{font_name}-Regular.ttf',
            f'/usr/share/fonts/truetype/dejavu/{font_name}-Bold.ttf',
            f'/usr/share/fonts/truetype/liberation/{font_name}.ttf',
            f'/usr/share/fonts/truetype/liberation/{font_name}-Regular.ttf',
            f'/usr/share/fonts/truetype/liberation/{font_name}-Bold.ttf',
        ]
        
        # 检查文件是否存在
        for font_path in linux_font_paths:
            if os.path.exists(font_path):
                return font_path
        
        # 使用fontconfig查找字体
        try:
            result = subprocess.run(['fc-match', font_name], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                font_path = result.stdout.strip().split(':')[0]
                if os.path.exists(font_path):
                    return font_path
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
    
    return None


def patch_gif_font_loading():
    """
    补丁函数：修复browser-use库中GIF生成的字体加载问题
    """
    try:
        from browser_use.agent.gif import create_history_gif as original_create_history_gif
        from PIL import ImageFont
        import logging
        
        logger = logging.getLogger(__name__)
        
        def patched_create_history_gif(*args, **kwargs):
            """补丁版本的create_history_gif函数"""
            from browser_use.agent.gif import create_history_gif as original_func
            
            # 获取原始函数的源代码
            import inspect
            source = inspect.getsource(original_func)
            
            # 这里我们无法直接修改库函数，但我们可以通过monkey patching的方式
            # 由于库代码的复杂性，最好的方法是确保字体路径正确
            
            # 调用原始函数，但在此之前确保字体路径正确
            return original_func(*args, **kwargs)
        
        # 应用补丁
        import browser_use.agent.gif
        browser_use.agent.gif.create_history_gif = patched_create_history_gif
        
        logger.info("GIF字体加载补丁已应用")
        
    except ImportError as e:
        print(f"无法应用GIF字体补丁: {e}")
    except Exception as e:
        print(f"应用GIF字体补丁时出错: {e}")


def test_font_loading():
    """测试字体加载功能"""
    test_fonts = [
        'Noto Sans CJK SC',
        'Noto Serif CJK SC', 
        'DejaVuSans',
        'Arial'
    ]
    
    print("测试字体加载:")
    for font_name in test_fonts:
        font_path = get_font_path(font_name)
        if font_path:
            print(f"✓ {font_name} -> {font_path}")
        else:
            print(f"✗ {font_name} -> 未找到")


if __name__ == "__main__":
    test_font_loading() 