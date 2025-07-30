#!/usr/bin/env python3
"""
测试搜索引擎配置的脚本
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# 添加项目根目录到Python路径
sys.path.append(".")

from src.controller.custom_controller import CustomController
from src.browser.custom_browser import CustomBrowser
from browser_use.browser.browser import BrowserConfig
from browser_use.browser.context import BrowserContextConfig


async def test_search_engines():
    """测试不同的搜索引擎"""
    
    # 测试的搜索引擎列表
    search_engines = ["baidu", "bing", "sogou", "360"]
    
    for search_engine in search_engines:
        print(f"\n=== 测试搜索引擎: {search_engine} ===")
        
        browser = None
        browser_context = None
        
        try:
            # 创建浏览器实例
            browser = CustomBrowser(
                config=BrowserConfig(
                    headless=True,  # 无头模式
                    new_context_config=BrowserContextConfig(
                        window_width=1280,
                        window_height=1100,
                    )
                )
            )
            
            # 创建浏览器上下文
            browser_context = await browser.new_context(
                config=BrowserContextConfig(
                    save_downloads_path="./tmp/downloads",
                    window_height=1100,
                    window_width=1280,
                )
            )
            
            # 创建控制器
            controller = CustomController(search_engine=search_engine)
            
            # 测试搜索
            test_query = "Python编程教程"
            print(f"搜索查询: {test_query}")
            
            # 执行搜索
            result = await controller.registry.execute_action(
                "search_web",
                {"query": test_query},
                browser=browser_context
            )
            
            if result and hasattr(result, 'extracted_content'):
                print("搜索结果:")
                print(result.extracted_content[:500] + "..." if len(result.extracted_content) > 500 else result.extracted_content)
            else:
                print("搜索失败或没有结果")
                
        except Exception as e:
            print(f"测试 {search_engine} 时出错: {e}")
            
        finally:
            # 清理资源
            if browser_context:
                await browser_context.close()
            if browser:
                await browser.close()
            
        print(f"=== {search_engine} 测试完成 ===\n")


if __name__ == "__main__":
    print("开始测试搜索引擎配置...")
    asyncio.run(test_search_engines())
    print("测试完成!") 