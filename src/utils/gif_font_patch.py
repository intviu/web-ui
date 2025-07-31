import os
import platform
import subprocess
from typing import Optional
import logging

logger = logging.getLogger(__name__)


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


def apply_gif_font_patch():
    """
    应用GIF字体加载补丁
    通过monkey patching修复browser-use库中的字体加载问题
    """
    try:
        # 导入原始模块
        import browser_use.agent.gif as gif_module
        from PIL import ImageFont
        
        # 保存原始的ImageFont.truetype函数
        original_truetype = ImageFont.truetype
        
        def patched_truetype(font_name, size, **kwargs):
            """
            补丁版本的ImageFont.truetype函数
            自动处理Linux系统上的字体路径问题
            """
            # 如果已经是完整路径，直接使用
            if os.path.isabs(font_name) and os.path.exists(font_name):
                return original_truetype(font_name, size, **kwargs)
            
            # 尝试获取字体路径
            font_path = get_font_path(font_name)
            if font_path:
                logger.debug(f"字体路径映射: {font_name} -> {font_path}")
                return original_truetype(font_path, size, **kwargs)
            else:
                # 如果找不到字体，使用原始逻辑
                logger.warning(f"未找到字体: {font_name}，使用原始逻辑")
                return original_truetype(font_name, size, **kwargs)
        
        # 应用补丁
        ImageFont.truetype = patched_truetype
        
        logger.info("GIF字体加载补丁已应用")
        return True
        
    except ImportError as e:
        logger.error(f"无法应用GIF字体补丁: {e}")
        return False
    except Exception as e:
        logger.error(f"应用GIF字体补丁时出错: {e}")
        return False


def test_patch():
    """测试补丁是否正常工作"""
    from PIL import ImageFont
    
    print("测试字体加载补丁:")
    
    # 测试中文字体
    test_fonts = [
        'Noto Sans CJK SC',
        'Noto Serif CJK SC',
        'DejaVuSans'
    ]
    
    for font_name in test_fonts:
        try:
            font = ImageFont.truetype(font_name, 40)
            print(f"✓ {font_name} -> 加载成功")
        except Exception as e:
            print(f"✗ {font_name} -> 加载失败: {e}")


if __name__ == "__main__":
    # 应用补丁
    if apply_gif_font_patch():
        print("补丁应用成功")
        test_patch()
    else:
        print("补丁应用失败") 