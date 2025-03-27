import pytest
from fastapi import status
from app.models.article import Article
from app.schemas.article import ArticleCreate, ArticleUpdate
from tests.fixtures.test_data import test_category

@pytest.fixture
def article_data(test_category):
    return {
        "title": "测试文章",
        "content": "这是一篇测试文章的内容",
        "category_id": test_category.id,
        "status": "draft"
    }

def test_create_article(client, db_session, article_data):
    """测试创建文章"""
    response = client.post("/api/articles/", json=article_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == article_data["title"]
    assert data["content"] == article_data["content"]
    assert data["status"] == "draft"

def test_get_article(client, db_session, article_data):
    """测试获取文章"""
    # 先创建一篇文章
    create_response = client.post("/api/articles/", json=article_data)
    article_id = create_response.json()["id"]
    
    # 获取文章
    response = client.get(f"/api/articles/{article_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == article_data["title"]

def test_update_article(client, db_session, article_data):
    """测试更新文章"""
    # 先创建一篇文章
    create_response = client.post("/api/articles/", json=article_data)
    article_id = create_response.json()["id"]
    
    # 更新文章
    update_data = {"title": "更新后的标题", "content": "更新后的内容"}
    response = client.put(f"/api/articles/{article_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["content"] == update_data["content"]

def test_delete_article(client, db_session, article_data):
    """测试删除文章"""
    # 先创建一篇文章
    create_response = client.post("/api/articles/", json=article_data)
    article_id = create_response.json()["id"]
    
    # 删除文章
    response = client.delete(f"/api/articles/{article_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # 确认文章已被删除
    get_response = client.get(f"/api/articles/{article_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_list_articles(client, db_session, article_data):
    """测试获取文章列表"""
    # 创建多篇文章
    for i in range(3):
        article_data_copy = article_data.copy()
        article_data_copy["title"] = f"文章{i+1}"
        client.post("/api/articles/", json=article_data_copy)
    
    # 获取文章列表
    response = client.get("/api/articles/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 3
    assert all(article["title"].startswith("文章") for article in data)