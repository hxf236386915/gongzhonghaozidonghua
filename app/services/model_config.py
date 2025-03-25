from sqlalchemy.orm import Session
from app.models.model_config import ModelConfig
from app.schemas.model_config import ModelConfigCreate, ModelConfigUpdate
from app.core.security import encrypt_api_key, decrypt_api_key

def create_model_config(db: Session, config: ModelConfigCreate):
    encrypted_api_key = encrypt_api_key(config.api_key)
    db_config = ModelConfig(
        model_name=config.model_name,
        api_key=encrypted_api_key,
        endpoint=config.endpoint,
        parameters=config.parameters
    )
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config

def get_model_config(db: Session, config_id: int):
    return db.query(ModelConfig).filter(ModelConfig.id == config_id).first()

def get_model_configs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ModelConfig).offset(skip).limit(limit).all()

def update_model_config(db: Session, config_id: int, config: ModelConfigUpdate):
    db_config = db.query(ModelConfig).filter(ModelConfig.id == config_id).first()
    if db_config:
        update_data = config.dict(exclude_unset=True)
        if "api_key" in update_data and update_data["api_key"]:
            update_data["api_key"] = encrypt_api_key(update_data["api_key"])
        for key, value in update_data.items():
            setattr(db_config, key, value)
        db.commit()
        db.refresh(db_config)
    return db_config

def delete_model_config(db: Session, config_id: int):
    db_config = db.query(ModelConfig).filter(ModelConfig.id == config_id).first()
    if db_config:
        db.delete(db_config)
        db.commit()
    return db_config

def verify_api_connection(config_id: int):
    # TODO: 实现API连接验证逻辑
    pass 