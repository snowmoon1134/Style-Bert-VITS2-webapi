import logging
import sys
from datetime import datetime
from pathlib import Path

class MyLogger:
    def __init__(self, name: str = "emotional_text_to_speech"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # 既存のハンドラをクリア
        self.logger.handlers = []
        
        # フォーマットを設定
        formatter = logging.Formatter(
            '%(asctime)s %(filename)s:%(lineno)d %(message)s',
            datefmt='%Y/%m/%d %H:%M:%S'
        )
        
        # ストリームハンドラを設定
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def warning(self, message: str):
        self.logger.warning(message)
    
    def error(self, message: str):
        self.logger.error(message)
    
    def debug(self, message: str):
        self.logger.debug(message)
    
    def critical(self, message: str):
        self.logger.critical(message) 