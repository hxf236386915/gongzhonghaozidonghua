import pytest
from fastapi import status

@pytest.fixture
def content_generation_data():
    return {
        "prompt": "写一篇关于人工智能的文章",
        "max_tokens": 1000,
        "temperature": 0.7
    }

@pytest.fixture
def image_generation_data():
    return {
        "prompt": "一只可爱的猫咪",
        "size": "512x512",
        "style": "realistic"
    }

def test_generate_article_content(client, content_generation_data):
    """测试AI生成文章内容"""
    response = client.post("/api/ai/generate-content", json=content_generation_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "content" in data
    assert len(data["content"]) > 0

def test_generate_article_image(client, image_generation_data):
    """测试AI生成文章配图"""
    response = client.post("/api/ai/generate-image", json=image_generation_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "image_url" in data
    assert data["image_url"].startswith("http")

def test_invalid_content_generation(client):
    """测试无效的内容生成请求"""
    invalid_data = {"prompt": ""}
    response = client.post("/api/ai/generate-content", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_invalid_image_generation(client):
    """测试无效的图片生成请求"""
    invalid_data = {"prompt": "", "size": "invalid"}
    response = client.post("/api/ai/generate-image", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_content_generation_rate_limit(client, content_generation_data):
    """测试内容生成的速率限制"""
    # 连续发送多个请求
    for _ in range(5):
        response = client.post("/api/ai/generate-content", json=content_generation_data)
    
    # 第6个请求应该被限制
    response = client.post("/api/ai/generate-content", json=content_generation_data)
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS

def test_image_generation_rate_limit(client, image_generation_data):
    """测试图片生成的速率限制"""
    # 连续发送多个请求
    for _ in range(5):
        response = client.post("/api/ai/generate-image", json=image_generation_data)
    
    # 第6个请求应该被限制
    response = client.post("/api/ai/generate-image", json=image_generation_data)
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS)