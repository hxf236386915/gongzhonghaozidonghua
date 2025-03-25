from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.model_config import ModelConfig, ModelConfigCreate, ModelConfigUpdate
from app.services import model_config as model_config_service
from app.db.database import get_db

router = APIRouter()

@router.post("/", response_model=ModelConfig)
def create_model_config(config: ModelConfigCreate, db: Session = Depends(get_db)):
    return model_config_service.create_model_config(db=db, config=config)

@router.get("/{config_id}", response_model=ModelConfig)
def read_model_config(config_id: int, db: Session = Depends(get_db)):
    db_config = model_config_service.get_model_config(db, config_id=config_id)
    if db_config is None:
        raise HTTPException(status_code=404, detail="Model configuration not found")
    return db_config

@router.get("/", response_model=List[ModelConfig])
def read_model_configs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    configs = model_config_service.get_model_configs(db, skip=skip, limit=limit)
    return configs

@router.put("/{config_id}", response_model=ModelConfig)
def update_model_config(config_id: int, config: ModelConfigUpdate, db: Session = Depends(get_db)):
    db_config = model_config_service.update_model_config(db, config_id=config_id, config=config)
    if db_config is None:
        raise HTTPException(status_code=404, detail="Model configuration not found")
    return db_config

@router.delete("/{config_id}", response_model=ModelConfig)
def delete_model_config(config_id: int, db: Session = Depends(get_db)):
    db_config = model_config_service.delete_model_config(db, config_id=config_id)
    if db_config is None:
        raise HTTPException(status_code=404, detail="Model configuration not found")
    return db_config

@router.post("/{config_id}/verify")
def verify_api_connection(config_id: int):
    # TODO: 实现API连接验证
    return {"status": "success", "message": "API connection verified"} 