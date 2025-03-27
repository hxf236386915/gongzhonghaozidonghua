import pytest
from app.models.category import Category

@pytest.fixture
def test_category(db_session):
    category = Category(name="测试分类", description="这是一个测试分类")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category