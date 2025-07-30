import logging
from typing import Dict, Any, Optional
from browser_use.controller.service import Controller
from browser_use.browser.context import BrowserContext
from browser_use.agent.views import ActionResult
from browser_use.controller.views import SearchGoogleAction

logger = logging.getLogger(__name__)


class SearchController(Controller):
    """自定义搜索控制器，支持多种搜索引擎"""
    
    def __init__(self, search_engine: str = "baidu", **kwargs):
        """
        初始化搜索控制器
        
        Args:
            search_engine: 搜索引擎类型，支持 "baidu", "bing", "sogou", "360", "google"
        """
        super().__init__(**kwargs)
        self.search_engine = search_engine.lower()
        self._register_search_actions()
    
    def _register_search_actions(self):
        """注册搜索相关的动作"""
        
        @self.registry.action(
            "Search for information using the configured search engine"
        )
        async def search_web(query: str, browser: BrowserContext):
            """使用配置的搜索引擎进行搜索"""
            try:
                # 根据配置的搜索引擎选择搜索URL
                search_url = self._get_search_url(query)
                
                # 导航到搜索页面
                page = await browser.new_page()
                await page.goto(search_url)
                
                # 等待页面加载
                await page.wait_for_load_state("networkidle")
                
                # 提取搜索结果
                results = await self._extract_search_results(page)
                
                await page.close()
                
                return ActionResult(
                    extracted_content=f"Search results for '{query}':\n{results}",
                    include_in_memory=True
                )
                
            except Exception as e:
                logger.error(f"Search failed: {e}")
                return ActionResult(error=f"Search failed: {str(e)}")
    
    def _get_search_url(self, query: str) -> str:
        """根据搜索引擎类型返回搜索URL"""
        encoded_query = query.replace(" ", "+")
        
        if self.search_engine == "baidu":
            return f"https://www.baidu.com/s?wd={encoded_query}"
        elif self.search_engine == "bing":
            return f"https://cn.bing.com/search?q={encoded_query}"
        elif self.search_engine == "sogou":
            return f"https://www.sogou.com/web?query={encoded_query}"
        elif self.search_engine == "360":
            return f"https://www.so.com/s?q={encoded_query}"
        elif self.search_engine == "google":
            return f"https://www.google.com/search?q={encoded_query}"
        else:
            # 默认使用百度
            return f"https://www.baidu.com/s?wd={encoded_query}"
    
    async def _extract_search_results(self, page) -> str:
        """提取搜索结果"""
        try:
            # 根据不同的搜索引擎提取结果
            if self.search_engine == "baidu":
                return await self._extract_baidu_results(page)
            elif self.search_engine == "bing":
                return await self._extract_bing_results(page)
            elif self.search_engine == "sogou":
                return await self._extract_sogou_results(page)
            elif self.search_engine == "360":
                return await self._extract_360_results(page)
            elif self.search_engine == "google":
                return await self._extract_google_results(page)
            else:
                return await self._extract_baidu_results(page)
        except Exception as e:
            logger.error(f"Failed to extract search results: {e}")
            return f"Failed to extract search results: {str(e)}"
    
    async def _extract_baidu_results(self, page) -> str:
        """提取百度搜索结果"""
        try:
            # 等待搜索结果加载
            await page.wait_for_selector(".result", timeout=10000)
            
            # 提取搜索结果
            results = await page.evaluate("""
                () => {
                    const results = [];
                    const elements = document.querySelectorAll('.result');
                    elements.forEach((el, index) => {
                        if (index < 5) { // 只取前5个结果
                            const titleEl = el.querySelector('h3');
                            const contentEl = el.querySelector('.content-right_8Zs40');
                            const linkEl = el.querySelector('a');
                            
                            if (titleEl && contentEl && linkEl) {
                                results.push({
                                    title: titleEl.textContent.trim(),
                                    content: contentEl.textContent.trim(),
                                    url: linkEl.href
                                });
                            }
                        }
                    });
                    return results;
                }
            """)
            
            # 格式化结果
            formatted_results = []
            for i, result in enumerate(results, 1):
                formatted_results.append(
                    f"{i}. {result['title']}\n"
                    f"   {result['content'][:200]}...\n"
                    f"   URL: {result['url']}\n"
                )
            
            return "\n".join(formatted_results)
            
        except Exception as e:
            logger.error(f"Failed to extract Baidu results: {e}")
            return f"Failed to extract Baidu results: {str(e)}"
    
    async def _extract_bing_results(self, page) -> str:
        """提取必应搜索结果"""
        try:
            await page.wait_for_selector(".b_algo", timeout=10000)
            
            results = await page.evaluate("""
                () => {
                    const results = [];
                    const elements = document.querySelectorAll('.b_algo');
                    elements.forEach((el, index) => {
                        if (index < 5) {
                            const titleEl = el.querySelector('h2 a');
                            const contentEl = el.querySelector('.b_caption p');
                            
                            if (titleEl && contentEl) {
                                results.push({
                                    title: titleEl.textContent.trim(),
                                    content: contentEl.textContent.trim(),
                                    url: titleEl.href
                                });
                            }
                        }
                    });
                    return results;
                }
            """)
            
            formatted_results = []
            for i, result in enumerate(results, 1):
                formatted_results.append(
                    f"{i}. {result['title']}\n"
                    f"   {result['content'][:200]}...\n"
                    f"   URL: {result['url']}\n"
                )
            
            return "\n".join(formatted_results)
            
        except Exception as e:
            logger.error(f"Failed to extract Bing results: {e}")
            return f"Failed to extract Bing results: {str(e)}"
    
    async def _extract_sogou_results(self, page) -> str:
        """提取搜狗搜索结果"""
        try:
            await page.wait_for_selector(".vrwrap", timeout=10000)
            
            results = await page.evaluate("""
                () => {
                    const results = [];
                    const elements = document.querySelectorAll('.vrwrap');
                    elements.forEach((el, index) => {
                        if (index < 5) {
                            const titleEl = el.querySelector('h3 a');
                            const contentEl = el.querySelector('.text');
                            
                            if (titleEl && contentEl) {
                                results.push({
                                    title: titleEl.textContent.trim(),
                                    content: contentEl.textContent.trim(),
                                    url: titleEl.href
                                });
                            }
                        }
                    });
                    return results;
                }
            """)
            
            formatted_results = []
            for i, result in enumerate(results, 1):
                formatted_results.append(
                    f"{i}. {result['title']}\n"
                    f"   {result['content'][:200]}...\n"
                    f"   URL: {result['url']}\n"
                )
            
            return "\n".join(formatted_results)
            
        except Exception as e:
            logger.error(f"Failed to extract Sogou results: {e}")
            return f"Failed to extract Sogou results: {str(e)}"
    
    async def _extract_360_results(self, page) -> str:
        """提取360搜索结果"""
        try:
            await page.wait_for_selector(".res-list", timeout=10000)
            
            results = await page.evaluate("""
                () => {
                    const results = [];
                    const elements = document.querySelectorAll('.res-list');
                    elements.forEach((el, index) => {
                        if (index < 5) {
                            const titleEl = el.querySelector('h3 a');
                            const contentEl = el.querySelector('.res-desc');
                            
                            if (titleEl && contentEl) {
                                results.push({
                                    title: titleEl.textContent.trim(),
                                    content: contentEl.textContent.trim(),
                                    url: titleEl.href
                                });
                            }
                        }
                    });
                    return results;
                }
            """)
            
            formatted_results = []
            for i, result in enumerate(results, 1):
                formatted_results.append(
                    f"{i}. {result['title']}\n"
                    f"   {result['content'][:200]}...\n"
                    f"   URL: {result['url']}\n"
                )
            
            return "\n".join(formatted_results)
            
        except Exception as e:
            logger.error(f"Failed to extract 360 results: {e}")
            return f"Failed to extract 360 results: {str(e)}"
    
    async def _extract_google_results(self, page) -> str:
        """提取Google搜索结果"""
        try:
            await page.wait_for_selector(".g", timeout=10000)
            
            results = await page.evaluate("""
                () => {
                    const results = [];
                    const elements = document.querySelectorAll('.g');
                    elements.forEach((el, index) => {
                        if (index < 5) {
                            const titleEl = el.querySelector('h3');
                            const contentEl = el.querySelector('.VwiC3b');
                            const linkEl = el.querySelector('a');
                            
                            if (titleEl && contentEl && linkEl) {
                                results.push({
                                    title: titleEl.textContent.trim(),
                                    content: contentEl.textContent.trim(),
                                    url: linkEl.href
                                });
                            }
                        }
                    });
                    return results;
                }
            """)
            
            formatted_results = []
            for i, result in enumerate(results, 1):
                formatted_results.append(
                    f"{i}. {result['title']}\n"
                    f"   {result['content'][:200]}...\n"
                    f"   URL: {result['url']}\n"
                )
            
            return "\n".join(formatted_results)
            
        except Exception as e:
            logger.error(f"Failed to extract Google results: {e}")
            return f"Failed to extract Google results: {str(e)}" 