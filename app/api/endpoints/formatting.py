from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.formatting import (
    FormattingTemplate,
    FormattingTemplateCreate,
    FormattingTemplateUpdate,
    FormattingRule,
    FormattingRuleCreate,
    ImageUpload,
    FormattedContent
)
from app.services import formatting as formatting_service
from app.db.database import get_db
import base64

router = APIRouter()

@router.post("/templates/", response_model=FormattingTemplate)
def create_template(template: FormattingTemplateCreate, db: Session = Depends(get_db)):
    return formatting_service.create_formatting_template(db=db, template=template)

@router.get("/templates/{template_id}", response_model=FormattingTemplate)
def read_template(template_id: int, db: Session = Depends(get_db)):
    db_template = formatting_service.get_formatting_template(db, template_id=template_id)
    if db_template is None:
        raise HTTPException(status_code=404, detail="Template not found")
    return db_template

@router.get("/templates/", response_model=List[FormattingTemplate])
def read_templates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    templates = formatting_service.get_formatting_templates(db, skip=skip, limit=limit)
    return templates

@router.put("/templates/{template_id}", response_model=FormattingTemplate)
def update_template(
    template_id: int, template: FormattingTemplateUpdate, db: Session = Depends(get_db)
):
    db_template = formatting_service.update_formatting_template(
        db, template_id=template_id, template=template
    )
    if db_template is None:
        raise HTTPException(status_code=404, detail="Template not found")
    return db_template

@router.delete("/templates/{template_id}", response_model=FormattingTemplate)
def delete_template(template_id: int, db: Session = Depends(get_db)):
    db_template = formatting_service.delete_formatting_template(db, template_id=template_id)
    if db_template is None:
        raise HTTPException(status_code=404, detail="Template not found")
    return db_template

@router.post("/rules/", response_model=FormattingRule)
def create_rule(rule: FormattingRuleCreate, db: Session = Depends(get_db)):
    return formatting_service.create_formatting_rule(db=db, rule=rule)

@router.post("/format/", response_model=FormattedContent)
async def format_content(
    content: str,
    template_id: int,
    images: Optional[List[ImageUpload]] = None,
    db: Session = Depends(get_db)
):
    template = formatting_service.get_formatting_template(db, template_id=template_id)
    if template is None:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return await formatting_service.format_article(
        content=content,
        template=template,
        images=images
    )

@router.post("/upload-image/")
async def upload_image(
    file: UploadFile = File(...),
    position: str = Form("after"),
    alignment: str = Form("center"),
    width: int = Form(800),
    height: Optional[int] = Form(None),
    optimize: bool = Form(True),
    add_watermark: bool = Form(True),
    watermark_text: Optional[str] = Form(None),
    quality: int = Form(85)
):
    """
    上传并处理图片
    - position: 图片位置 (before/after/inline)
    - alignment: 对齐方式 (left/center/right)
    - width: 图片宽度
    - height: 图片高度（可选）
    - optimize: 是否优化图片
    - add_watermark: 是否添加水印
    - watermark_text: 水印文字
    - quality: 图片质量 (1-100)
    """
    try:
        content = await file.read()
        
        # 验证文件类型
        content_type = file.content_type
        if not content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="File type not allowed. Only images are accepted."
            )
        
        # 创建ImageUpload对象
        image = ImageUpload(
            base64_data=base64.b64encode(content).decode(),
            position=position,
            alignment=alignment,
            size={"width": width, "height": height} if height else {"width": width}
        )
        
        # 处理图片
        result = await formatting_service.process_image(image)
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/optimize-image/")
async def optimize_image(
    file: UploadFile = File(...),
    max_width: int = Form(800),
    quality: int = Form(85),
    format: str = Form("WEBP")
):
    """
    优化图片质量和大小
    - max_width: 最大宽度
    - quality: 压缩质量 (1-100)
    - format: 输出格式 (JPEG/PNG/WEBP)
    """
    try:
        content = await file.read()
        result = await formatting_service.process_image(
            ImageUpload(
                base64_data=base64.b64encode(content).decode(),
                size={"width": max_width}
            )
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch-process-images/")
async def batch_process_images(
    files: List[UploadFile] = File(...),
    position: str = Form("after"),
    alignment: str = Form("center"),
    width: int = Form(800),
    optimize: bool = Form(True),
    add_watermark: bool = Form(True)
):
    """
    批量处理多个图片
    """
    try:
        results = []
        for file in files:
            content = await file.read()
            image = ImageUpload(
                base64_data=base64.b64encode(content).decode(),
                position=position,
                alignment=alignment,
                size={"width": width}
            )
            result = await formatting_service.process_image(image)
            results.append(result)
        return results
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 