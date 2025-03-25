from typing import Optional, List, Dict, Union
from sqlalchemy.orm import Session
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime

from app.models.content import (
    ContentInput, 
    GeneratedContent, 
    ContentQuality,
    ContentHistory,
    InputType,
    ContentStatus,
    ChangeType
)
from app.schemas.content import (
    ContentInputCreate,
    GeneratedContentCreate,
    ContentQualityCreate,
    ContentHistoryCreate
)
from app.core.security import verify_api_key
from app.core.config import settings

class ContentService:
    def __init__(self, db: Session):
        self.db = db

    async def create_content_from_url(self, url: str) -> ContentInput:
        """从URL创建内容"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        raise ValueError(f"Failed to fetch URL: {url}")
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # 提取正文内容
                    content = soup.get_text()
                    
                    # 创建输入记录
                    content_input = ContentInput(
                        input_type=InputType.URL,
                        content=content,
                        source_url=url
                    )
                    self.db.add(content_input)
                    self.db.commit()
                    self.db.refresh(content_input)
                    
                    return content_input
        except Exception as e:
            raise ValueError(f"Error processing URL: {str(e)}")

    async def create_content_from_file(self, file_path: str) -> ContentInput:
        """从文件创建内容"""
        try:
            if not os.path.exists(file_path):
                raise ValueError(f"File not found: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            content_input = ContentInput(
                input_type=InputType.IMPORT,
                content=content,
                file_path=file_path
            )
            self.db.add(content_input)
            self.db.commit()
            self.db.refresh(content_input)
            
            return content_input
        except Exception as e:
            raise ValueError(f"Error processing file: {str(e)}")

    def create_content_manual(self, content: str) -> ContentInput:
        """手动创建内容"""
        try:
            content_input = ContentInput(
                input_type=InputType.MANUAL,
                content=content
            )
            self.db.add(content_input)
            self.db.commit()
            self.db.refresh(content_input)
            
            return content_input
        except Exception as e:
            raise ValueError(f"Error creating content: {str(e)}")

    async def generate_content(
        self,
        input_id: int,
        model_name: str,
        model_params: Dict
    ) -> GeneratedContent:
        """生成内容"""
        try:
            # 获取输入内容
            content_input = self.db.query(ContentInput).filter(
                ContentInput.id == input_id
            ).first()
            if not content_input:
                raise ValueError(f"Content input not found: {input_id}")
            
            # 验证API密钥
            verify_api_key(settings.OPENAI_API_KEY)
            
            # 创建生成内容记录
            generated_content = GeneratedContent(
                input_id=input_id,
                status=ContentStatus.GENERATING,
                model_name=model_name,
                model_params=model_params
            )
            self.db.add(generated_content)
            self.db.commit()
            
            start_time = datetime.now()
            
            try:
                # TODO: 调用大模型API生成内容
                # 这里需要实现具体的生成逻辑
                pass
                
            except Exception as e:
                generated_content.status = ContentStatus.FAILED
                self.db.commit()
                raise ValueError(f"Content generation failed: {str(e)}")
            
            # 更新生成时间和状态
            generation_time = (datetime.now() - start_time).total_seconds()
            generated_content.generation_time = generation_time
            generated_content.status = ContentStatus.COMPLETED
            self.db.commit()
            self.db.refresh(generated_content)
            
            return generated_content
            
        except Exception as e:
            raise ValueError(f"Error generating content: {str(e)}")

    def evaluate_content_quality(
        self,
        content_id: int,
        scores: Dict[str, float],
        tags: List[str]
    ) -> ContentQuality:
        """评估内容质量"""
        try:
            # 验证内容是否存在
            content = self.db.query(GeneratedContent).filter(
                GeneratedContent.id == content_id
            ).first()
            if not content:
                raise ValueError(f"Content not found: {content_id}")
            
            # 创建质量评估记录
            quality = ContentQuality(
                content_id=content_id,
                readability_score=scores.get("readability", 0),
                originality_score=scores.get("originality", 0),
                relevance_score=scores.get("relevance", 0),
                overall_score=sum(scores.values()) / len(scores),
                tags=tags
            )
            self.db.add(quality)
            
            # 记录历史
            history = ContentHistory(
                content_id=content_id,
                change_type=ChangeType.EVALUATE,
                change_details={
                    "scores": scores,
                    "tags": tags
                }
            )
            self.db.add(history)
            
            self.db.commit()
            self.db.refresh(quality)
            
            return quality
            
        except Exception as e:
            raise ValueError(f"Error evaluating content quality: {str(e)}")

    def get_content_history(self, content_id: int) -> List[ContentHistory]:
        """获取内容历史记录"""
        try:
            history = self.db.query(ContentHistory).filter(
                ContentHistory.content_id == content_id
            ).order_by(ContentHistory.created_at.desc()).all()
            
            return history
        except Exception as e:
            raise ValueError(f"Error fetching content history: {str(e)}")

    def get_content_list(
        self,
        skip: int = 0,
        limit: int = 10,
        status: Optional[ContentStatus] = None
    ) -> Dict:
        """获取内容列表"""
        try:
            query = self.db.query(GeneratedContent)
            if status:
                query = query.filter(GeneratedContent.status == status)
            
            total = query.count()
            items = query.offset(skip).limit(limit).all()
            
            return {
                "total": total,
                "items": items
            }
        except Exception as e:
            raise ValueError(f"Error fetching content list: {str(e)}")

    def update_content(
        self,
        content_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
        status: Optional[ContentStatus] = None
    ) -> GeneratedContent:
        """更新内容"""
        try:
            generated_content = self.db.query(GeneratedContent).filter(
                GeneratedContent.id == content_id
            ).first()
            if not generated_content:
                raise ValueError(f"Content not found: {content_id}")
            
            # 记录更新前的版本
            previous_version = {
                "title": generated_content.title,
                "content": generated_content.content,
                "status": generated_content.status
            }
            
            # 更新内容
            if title is not None:
                generated_content.title = title
            if content is not None:
                generated_content.content = content
            if status is not None:
                generated_content.status = status
            
            # 记录历史
            history = ContentHistory(
                content_id=content_id,
                change_type=ChangeType.UPDATE,
                previous_version=previous_version,
                change_details={
                    "title": title if title is not None else generated_content.title,
                    "content": content if content is not None else generated_content.content,
                    "status": status.value if status is not None else generated_content.status.value
                }
            )
            self.db.add(history)
            
            self.db.commit()
            self.db.refresh(generated_content)
            
            return generated_content
            
        except Exception as e:
            raise ValueError(f"Error updating content: {str(e)}") 