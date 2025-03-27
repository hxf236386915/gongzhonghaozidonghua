import pytest
from fastapi import status
from datetime import datetime, timedelta

@pytest.fixture
def account_data():
    return {
        "name": "测试公众号",
        "appid": "wx123456789",
        "app_secret": "abcdef123456789"
    }

@pytest.fixture
def publish_schedule_data():
    return {
        "article_id": 1,
        "account_id": 1,
        "scheduled_time": (datetime.now() + timedelta(hours=1)).isoformat()
    }

def test_authorize_account(client, account_data):
    """测试公众号授权"""
    response = client.post("/api/accounts/authorize", json=account_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == account_data["name"]
    assert "access_token" in data
    assert "refresh_token" in data

def test_refresh_token(client, account_data):
    """测试刷新访问令牌"""
    # 先创建一个授权账号
    auth_response = client.post("/api/accounts/authorize", json=account_data)
    account_id = auth_response.json()["id"]
    
    # 刷新令牌
    response = client.post(f"/api/accounts/{account_id}/refresh-token")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

def test_upload_material(client, account_data):
    """测试上传素材"""
    # 先创建一个授权账号
    auth_response = client.post("/api/accounts/authorize", json=account_data)
    account_id = auth_response.json()["id"]
    
    # 上传图片素材
    files = {"file": ("test.jpg", b"fake image content", "image/jpeg")}
    response = client.post(
        f"/api/accounts/{account_id}/materials",
        files=files,
        data={"type": "image"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "media_id" in data

def test_schedule_publish(client, account_data, publish_schedule_data):
    """测试定时发布"""
    # 先创建一个授权账号
    auth_response = client.post("/api/accounts/authorize", json=account_data)
    account_id = auth_response.json()["id"]
    
    # 创建发布计划
    response = client.post("/api/publish/schedule", json=publish_schedule_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["status"] == "scheduled"
    assert "scheduled_time" in data

def test_get_publish_history(client, account_data, publish_schedule_data):
    """测试获取发布历史"""
    # 先创建一个授权账号和发布计划
    auth_response = client.post("/api/accounts/authorize", json=account_data)
    account_id = auth_response.json()["id"]
    client.post("/api/publish/schedule", json=publish_schedule_data)
    
    # 获取发布历史
    response = client.get(f"/api/accounts/{account_id}/publish-history")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_cancel_scheduled_publish(client, account_data, publish_schedule_data):
    """测试取消定时发布"""
    # 先创建一个授权账号和发布计划
    auth_response = client.post("/api/accounts/authorize", json=account_data)
    schedule_response = client.post("/api/publish/schedule", json=publish_schedule_data)
    schedule_id = schedule_response.json()["id"]
    
    # 取消发布计划
    response = client.delete(f"/api/publish/schedule/{schedule_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # 确认计划已被取消
    get_response = client.get(f"/api/publish/schedule/{schedule_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND)