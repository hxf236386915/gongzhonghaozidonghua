from sqlalchemy.orm import Session
import re
import base64
import aiohttp
from typing import List, Dict, Optional, Tuple
from bs4 import BeautifulSoup
from app.models.formatting import FormattingTemplate, FormattingRule
from app.schemas.formatting import (
    FormattingTemplateCreate,
    FormattingTemplateUpdate,
    FormattingRuleCreate,
    ImageUpload,
)
from app.utils.image_processor import ImageProcessor

# 创建图片处理器实例
image_processor = ImageProcessor()

class FormattingError(Exception):
    """格式化相关错误"""
    pass

async def download_image(url: str, timeout: int = 10) -> Tuple[bytes, str]:
    """从URL下载图片
    
    Args:
        url: 图片URL
        timeout: 超时时间（秒）
    
    Returns:
        Tuple[bytes, str]: (图片数据, MIME类型)
    
    Raises:
        FormattingError: 下载失败时抛出
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=timeout) as response:
                if response.status != 200:
                    raise FormattingError(f"Failed to download image: HTTP {response.status}")
                
                content_type = response.headers.get("content-type", "")
                if not content_type.startswith("image/"):
                    raise FormattingError(f"Invalid content type: {content_type}")
                
                return await response.read(), content_type
    except aiohttp.ClientError as e:
        raise FormattingError(f"Network error while downloading image: {str(e)}")
    except Exception as e:
        raise FormattingError(f"Failed to download image: {str(e)}")

async def process_image(image: ImageUpload) -> Dict:
    """处理图片上传，支持URL和base64数据"""
    try:
        if image.url:
            # 从URL下载图片
            image_data, content_type = await download_image(str(image.url))
        elif image.base64_data:
            # 解码base64数据
            try:
                image_data = base64.b64decode(image.base64_data)
            except Exception as e:
                raise FormattingError(f"Invalid base64 data: {str(e)}")
        else:
            raise FormattingError("Either url or base64_data must be provided")

        # 使用图片处理器处理图片
        try:
            processed_image = image_processor.process_image(
                image_data,
                optimize=True,
                add_watermark=True,
                watermark_text="微信公众号",
                max_width=image.size.get("width", 800),
                quality=85
            )
        except Exception as e:
            raise FormattingError(f"Image processing failed: {str(e)}")

        return {
            "data": processed_image["data"],
            "position": image.position,
            "alignment": image.alignment,
            "size": processed_image["size"]
        }

    except FormattingError as e:
        raise e
    except Exception as e:
        raise FormattingError(f"Unexpected error during image processing: {str(e)}")

def create_formatting_template(db: Session, template: FormattingTemplateCreate):
    # 如果新模板设置为默认，需要取消其他模板的默认状态
    if template.is_default:
        db.query(FormattingTemplate).filter(
            FormattingTemplate.is_default == True
        ).update({"is_default": False})

    db_template = FormattingTemplate(**template.dict())
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

def get_formatting_template(db: Session, template_id: int):
    return db.query(FormattingTemplate).filter(FormattingTemplate.id == template_id).first()

def get_formatting_templates(db: Session, skip: int = 0, limit: int = 100):
    return db.query(FormattingTemplate).offset(skip).limit(limit).all()

def update_formatting_template(
    db: Session, template_id: int, template: FormattingTemplateUpdate
):
    db_template = db.query(FormattingTemplate).filter(
        FormattingTemplate.id == template_id
    ).first()
    if db_template:
        update_data = template.dict(exclude_unset=True)
        # 如果更新为默认模板，需要取消其他模板的默认状态
        if update_data.get("is_default"):
            db.query(FormattingTemplate).filter(
                FormattingTemplate.id != template_id,
                FormattingTemplate.is_default == True
            ).update({"is_default": False})

        for key, value in update_data.items():
            setattr(db_template, key, value)
        db.commit()
        db.refresh(db_template)
    return db_template

def delete_formatting_template(db: Session, template_id: int):
    db_template = db.query(FormattingTemplate).filter(
        FormattingTemplate.id == template_id
    ).first()
    if db_template:
        db.delete(db_template)
        db.commit()
    return db_template

def create_formatting_rule(db: Session, rule: FormattingRuleCreate):
    db_rule = FormattingRule(**rule.dict())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule

def apply_template(content: str, template: FormattingTemplate, images: List[Dict] = None) -> str:
    """应用排版模板到内容"""
    try:
        # 解析HTML内容
        soup = BeautifulSoup(content, 'html.parser')
        
        # 清理HTML
        for tag in soup.find_all(True):
            # 移除空标签
            if len(tag.get_text(strip=True)) == 0 and not tag.find_all(['img', 'br', 'hr']):
                tag.decompose()
            # 移除样式属性
            if 'style' in tag.attrs:
                del tag.attrs['style']
        
        # 应用HTML结构
        formatted_content = template.html_structure.replace(
            "{content}", str(soup)
        )
        
        # 处理图片
        if images:
            for img in images:
                # 构建图片样式
                style = []
                # 设置尺寸
                style.append(f"width: {img['size']['width']}px")
                if img['size'].get('height'):
                    style.append(f"height: {img['size']['height']}px")
                
                # 设置显示方式
                style.append("display: block")
                
                # 根据对齐方式设置margin
                if img["alignment"] == "center":
                    style.append("margin: 20px auto")
                elif img["alignment"] == "left":
                    style.append("margin: 20px 20px 20px 0")
                else:  # right
                    style.append("margin: 20px 0 20px 20px")
                
                # 添加其他样式
                style.append("max-width: 100%")
                style.append("height: auto")
                
                # 构建img标签
                img_tag = f'<img src="{img["data"]}" style="{"; ".join(style)}" alt="" loading="lazy" />'
                
                # 根据位置插入图片
                if img["position"] == "before":
                    formatted_content = img_tag + formatted_content
                elif img["position"] == "after":
                    formatted_content = formatted_content + img_tag
                else:  # inline
                    # 在段落之间插入图片
                    formatted_content = re.sub(
                        r'(</p>)(?!.*</p>)',
                        r'\1' + img_tag,
                        formatted_content,
                        1
                    )
        
        return formatted_content
        
    except Exception as e:
        raise FormattingError(f"Template application failed: {str(e)}")

async def format_article(
    content: str,
    template: FormattingTemplate,
    images: Optional[List[ImageUpload]] = None
) -> Dict:
    """格式化文章内容"""
    try:
        # 处理图片
        processed_images = []
        if images:
            for image in images:
                processed_image = await process_image(image)
                processed_images.append(processed_image)
        
        # 应用模板
        formatted_html = apply_template(content, template, processed_images)
        
        return {
            "html_content": formatted_html,
            "css_styles": template.css_styles,
            "images": processed_images
        }
        
    except Exception as e:
        raise FormattingError(f"Article formatting failed: {str(e)}") 