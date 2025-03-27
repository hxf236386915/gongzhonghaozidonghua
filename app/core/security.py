from cryptography.fernet import Fernet
import os
import re
import requests
import aiohttp
from typing import Optional
from dotenv import load_dotenv
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

load_dotenv()

# 使用环境变量中的密钥，如果不存在则生成新的
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key())
fernet = Fernet(ENCRYPTION_KEY)

class APIKeyError(Exception):
    """API密钥相关错误"""
    pass

def encrypt_api_key(api_key: str) -> str:
    """加密API密钥"""
    return fernet.encrypt(api_key.encode()).decode()

def decrypt_api_key(encrypted_api_key: str) -> str:
    """解密API密钥"""
    return fernet.decrypt(encrypted_api_key.encode()).decode()

def _validate_api_key_format(api_key: str) -> bool:
    """验证API密钥格式"""
    # OpenAI API密钥格式
    if re.match(r'^sk-[A-Za-z0-9]{48}$', api_key):
        return True
    # ChatGLM API密钥格式
    if re.match(r'^[A-Za-z0-9]{32}$', api_key):
        return True
    # 文心一言API密钥格式
    if re.match(r'^[A-Za-z0-9]{24}\.[A-Za-z0-9]{24}$', api_key):
        return True
    return False

async def verify_api_connection(api_key: str, endpoint: str) -> tuple[bool, Optional[str]]:
    """验证API连接"""
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, headers=headers, json={"test": True}) as response:
                if response.status == 200:
                    return True, None
                else:
                    return False, f"API connection failed with status {response.status}"
    except Exception as e:
        return False, f"API connection error: {str(e)}"

def verify_api_key(api_key: str, model_type: str = "openai") -> bool:
    """验证API密钥的有效性
    
    Args:
        api_key: API密钥
        model_type: 模型类型 (openai/chatglm/ernie)
    
    Returns:
        bool: 密钥是否有效
    
    Raises:
        APIKeyError: 当密钥格式无效或验证失败时
    """
    try:
        # 验证密钥格式
        if not _validate_api_key_format(api_key):
            raise APIKeyError("Invalid API key format")
        
        # 根据模型类型选择验证端点
        endpoints = {
            "openai": "https://api.openai.com/v1/chat/completions",
            "chatglm": "https://open.bigmodel.cn/api/paas/v3/model-api",
            "ernie": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat"
        }
        
        endpoint = endpoints.get(model_type)
        if not endpoint:
            raise APIKeyError(f"Unsupported model type: {model_type}")
        
        # 验证API连接
        success, error = verify_api_connection(api_key, endpoint)
        if not success:
            raise APIKeyError(f"API key verification failed: {error}")
        
        return True
        
    except APIKeyError as e:
        raise e
    except Exception as e:
        raise APIKeyError(f"API key verification failed: {str(e)}")

def get_model_info(api_key: str, model_type: str) -> dict:
    """获取模型信息
    
    Args:
        api_key: API密钥
        model_type: 模型类型
    
    Returns:
        dict: 包含模型信息的字典
    """
    # 验证API密钥
    verify_api_key(api_key, model_type)
    
    # 根据模型类型返回相应的配置信息
    model_configs = {
        "openai": {
            "max_tokens": 4096,
            "supported_models": ["gpt-3.5-turbo", "gpt-4"],
            "features": ["chat", "completion", "embedding"]
        },
        "chatglm": {
            "max_tokens": 2048,
            "supported_models": ["chatglm-6b", "chatglm-130b"],
            "features": ["chat", "completion"]
        },
        "ernie": {
            "max_tokens": 2000,
            "supported_models": ["ernie-bot", "ernie-bot-turbo"],
            "features": ["chat"]
        }
    }
    
    return model_configs.get(model_type, {})

# 密码上下文配置
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码是否匹配
    
    Args:
        plain_password: 明文密码
        hashed_password: 哈希后的密码
    
    Returns:
        bool: 密码是否匹配
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建JWT访问令牌
    
    Args:
        data: 要编码到令牌中的数据
        expires_delta: 可选的令牌过期时间
    
    Returns:
        str: 编码后的JWT令牌
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, ENCRYPTION_KEY, algorithm="HS256")
    return encoded_jwt