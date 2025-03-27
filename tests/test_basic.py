import pytest
from fastapi import status

def test_health_check(client):
    """测试健康检查接口"""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}