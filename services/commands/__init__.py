"""
命令系統模組

統一的命令處理系統，包含:
- parsers: 參數解析器
- handlers: 命令處理器
- config: 命令配置
- processor: 統一處理入口
"""
from .processor import parse_command, handle_command, process_message
from .config import COMMAND_CONFIG, get_command_list

__all__ = [
    'parse_command',
    'handle_command',
    'process_message',
    'COMMAND_CONFIG',
    'get_command_list'
]
