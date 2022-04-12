import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models
from alembic import command

# for run need hardcode
# SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:admin@localhost/fastapi'                                                                    
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)
#            with alembic no need this command to generate 
@pytest.fixture()
def session():  
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    # run our code before we run our test
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)   
    # run our code after our test finishes

@pytest.fixture
def test_user2(session):
    user_data = {"email": "morteza1@gmail.com",
                 "password": "admin"}
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == 201
    
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user(session):
    user_data = {"email": "morteza@gmail.com",
                 "password": "admin"}
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == 201
    
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user2['id']
    }]
    
    def create_post_model(post):
        return models.Post(**post)
    
    # map(func, posts_data)
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    
    session.add_all(posts)
    # == hard coded
    # session.add_all([models.Post(title="first title", content="first content",owner_id=test_user['id']),
    #                  models.Post(title="2nd title", content="2nd content",owner_id=test_user['id']),
    #                  models.Post(title="3rd title", content="3rd content",owner_id=test_user['id']),
    #                  ])
    session.commit()
    
    posts = session.query(models.Post).all()
    return posts