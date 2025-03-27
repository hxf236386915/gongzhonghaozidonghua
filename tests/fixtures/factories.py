from datetime import datetime, timedelta
from typing import Dict, Any

class TestDataFactory:
    @staticmethod
    def create_article_data(**kwargs) -> Dict[str, Any]:
        """创建文章测试数据"""
        data = {
            "title": "测试文章",
            "content": "这是一篇测试文章的内容",
            "category_id": 1,
            "status": "draft"
        }
        data.update(kwargs)
        return data
    
    @staticmethod
    def create_account_data(**kwargs) -> Dict[str, Any]:
        """创建公众号账号测试数据"""
        data = {
            "name": "测试公众号",
            "appid": "wx123456789",
            "app_secret": "abcdef123456789"
        }
        data.update(kwargs)
        return data
    
    @staticmethod
    def create_content_generation_data(**kwargs) -> Dict[str, Any]:
        """创建内容生成测试数据"""
        data = {
            "prompt": "写一篇关于人工智能的文章",
            "max_tokens": 1000,
            "temperature": 0.7
        }
        data.update(kwargs)
        return data
    
    @staticmethod
    def create_image_generation_data(**kwargs) -> Dict[str, Any]:
        """创建图片生成测试数据"""
        data = {
            "prompt": "一只可爱的猫咪",
            "size": "512x512",
            "style": "realistic"
        }
        data.update(kwargs)
        return data
    
    @staticmethod
    def create_publish_schedule_data(**kwargs) -> Dict[str, Any]:
        """创建发布计划测试数据"""
        data = {
            "article_id": 1,
            "account_id": 1,
            "scheduled_time": (datetime.now() + timedelta(hours=1)).isoformat()
        }
        data.update(kwargs)
        return data