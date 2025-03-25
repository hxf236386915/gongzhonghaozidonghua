from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.session import get_db
from app.services.content import ContentService
from app.schemas.content import (
    ContentResponse,
    ContentListResponse,
    ContentQualityResponse,
    ContentHistoryResponse,
    ContentStatus
)

router = APIRouter()

@router.post("/content/url", response_model=ContentResponse)
async def create_content_from_url(
    url: str,
    db: Session = Depends(get_db)
):
    """从URL创建内容"""
    try:
        service = ContentService(db)
        content = await service.create_content_from_url(url)
        return {"input": content, "generated": None}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/content/file", response_model=ContentResponse)
async def create_content_from_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """从文件创建内容"""
    try:
        # 保存上传的文件
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        service = ContentService(db)
        content = await service.create_content_from_file(file_path)
        return {"input": content, "generated": None}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/content/manual", response_model=ContentResponse)
def create_content_manual(
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    """手动创建内容"""
    try:
        service = ContentService(db)
        content_input = service.create_content_manual(content)
        return {"input": content_input, "generated": None}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/content/{input_id}/generate", response_model=ContentResponse)
async def generate_content(
    input_id: int,
    model_name: str,
    model_params: dict,
    db: Session = Depends(get_db)
):
    """生成内容"""
    try:
        service = ContentService(db)
        content = await service.generate_content(input_id, model_name, model_params)
        return {"input": content.input_content, "generated": content}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/content/{content_id}/evaluate", response_model=ContentQualityResponse)
def evaluate_content(
    content_id: int,
    scores: dict,
    tags: List[str],
    db: Session = Depends(get_db)
):
    """评估内容质量"""
    try:
        service = ContentService(db)
        quality = service.evaluate_content_quality(content_id, scores, tags)
        return {"content_id": content_id, "quality": quality}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/content", response_model=ContentListResponse)
def get_content_list(
    skip: int = 0,
    limit: int = 10,
    status: Optional[ContentStatus] = None,
    db: Session = Depends(get_db)
):
    """获取内容列表"""
    try:
        service = ContentService(db)
        result = service.get_content_list(skip, limit, status)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/content/{content_id}/history", response_model=ContentHistoryResponse)
def get_content_history(
    content_id: int,
    db: Session = Depends(get_db)
):
    """获取内容历史记录"""
    try:
        service = ContentService(db)
        history = service.get_content_history(content_id)
        return {"content_id": content_id, "history": history}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/content/{content_id}", response_model=ContentResponse)
def update_content(
    content_id: int,
    title: Optional[str] = None,
    content: Optional[str] = None,
    status: Optional[ContentStatus] = None,
    db: Session = Depends(get_db)
):
    """更新内容"""
    try:
        service = ContentService(db)
        updated_content = service.update_content(content_id, title, content, status)
        return {"input": updated_content.input_content, "generated": updated_content}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 