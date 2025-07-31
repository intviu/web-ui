import logging
from typing import List, Optional
from datetime import datetime
from collections import deque


class UILogHandler(logging.Handler):
    """自定义日志处理器，将日志存储到内存中供UI显示"""
    
    def __init__(self, max_logs: int = 1000):
        super().__init__()
        self.max_logs = max_logs
        # 使用deque，它是线程安全的，并且有maxlen参数自动限制大小
        self.logs = deque(maxlen=max_logs)
        
    def emit(self, record):
        """处理日志记录"""
        try:
            # 格式化日志消息
            log_entry = self.format(record)
            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_log = f"[{timestamp}] {log_entry}"
            
            # deque的append操作是线程安全的，不需要锁
            self.logs.append(formatted_log)
                    
        except Exception:
            self.handleError(record)
    
    def get_logs(self, limit: Optional[int] = None) -> str:
        """获取所有日志，返回格式化的字符串"""
        # 转换为列表并切片，这个操作很快
        logs_list = list(self.logs)
        if limit and len(logs_list) > limit:
            logs_list = logs_list[-limit:]
        return "\n".join(logs_list)
    
    def clear_logs(self):
        """清空所有日志"""
        self.logs.clear()
    
    def get_log_count(self) -> int:
        """获取当前日志数量"""
        return len(self.logs)


# 全局日志处理器实例
ui_log_handler = UILogHandler()


def setup_ui_logging():
    """设置UI日志记录"""
    # 设置日志格式
    formatter = logging.Formatter(
        '%(levelname)s - %(name)s - %(message)s'
    )
    ui_log_handler.setFormatter(formatter)
    
    # 获取根日志记录器并添加处理器
    root_logger = logging.getLogger()
    root_logger.addHandler(ui_log_handler)
    
    # 设置根logger的级别
    root_logger.setLevel(logging.INFO)
    
    # 确保所有logger都传播到根logger
    # 这是关键：强制所有logger使用根logger的处理器
    for name in logging.root.manager.loggerDict:
        logger = logging.getLogger(name)
        logger.handlers = []  # 清除所有现有处理器
        logger.propagate = True  # 确保传播到根logger
        logger.setLevel(logging.INFO)
    
    # 特别处理browser_use相关的logger
    browser_use_loggers = [
        'browser_use',
        'browser_use.agent',
        'browser_use.agent.service',
        'browser_use.controller',
        'browser_use.browser',
        'agent'
    ]
    
    for logger_name in browser_use_loggers:
        logger = logging.getLogger(logger_name)
        logger.handlers = []  # 清除现有处理器
        logger.propagate = True  # 确保传播
        logger.setLevel(logging.INFO)
    
    return ui_log_handler


def get_ui_logs(limit: Optional[int] = None) -> str:
    """获取UI日志"""
    return ui_log_handler.get_logs(limit)


def clear_ui_logs():
    """清空UI日志"""
    ui_log_handler.clear_logs() 