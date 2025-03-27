import pytest
from fastapi import status
from datetime import datetime, timedelta

@pytest.fixture
def workflow_data():
    return {
        "article": {
            "title": "AI自动生成的文章",
            "content": "",  # 将由AI生成
            "category_id": 1,
            "status": "draft"
        },
        "content_generation": {
            "prompt": "写一篇关于人工智能的文章",
            "max_tokens": 1000
        },
        "image_generation": {
            "prompt": "未来科技感的人工智能图片",
            "size": "512x512"
        },
        "account": {
            "name": "测试公众号",
            "appid": "wx123456789",
            "app_secret": "abcdef123456789"
        },
        "schedule": {
            "scheduled_time": (datetime.now() + timedelta(hours=1)).isoformat()
        }
    }

def test_complete_article_workflow(client, workflow_data):
    """测试完整的文章工作流程"""
    # 1. 使用AI生成文章内容
    content_response = client.post("/api/ai/generate-content", json=workflow_data["content_generation"])
    assert content_response.status_code == status.HTTP_200_OK
    generated_content = content_response.json()["content"]
    workflow_data["article"]["content"] = generated_content
    
    # 2. 创建文章
    article_response = client.post("/api/articles/", json=workflow_data["article"])
    assert article_response.status_code == status.HTTP_201_CREATED
    article_id = article_response.json()["id"]
    
    # 3. 生成配图
    image_response = client.post("/api/ai/generate-image", json=workflow_data["image_generation"])
    assert image_response.status_code == status.HTTP_200_OK
    image_url = image_response.json()["image_url"]
    
    # 4. 更新文章，添加配图
    update_response = client.put(
        f"/api/articles/{article_id}",
        json={"image_url": image_url}
    )
    assert update_response.status_code == status.HTTP_200_OK
    
    # 5. 授权公众号
    account_response = client.post("/api/accounts/authorize", json=workflow_data["account"])
    assert account_response.status_code == status.HTTP_201_CREATED
    account_id = account_response.json()["id"]
    
    # 6. 创建发布计划
    schedule_data = workflow_data["schedule"].copy()
    schedule_data.update({
        "article_id": article_id,
        "account_id": account_id
    })
    schedule_response = client.post("/api/publish/schedule", json=schedule_data)
    assert schedule_response.status_code == status.HTTP_201_CREATED
    
    # 7. 检查文章状态
    article_status_response = client.get(f"/api/articles/{article_id}")
    assert article_status_response.status_code == status.HTTP_200_OK
    assert article_status_response.json()["status"] == "scheduled"