import pytest
from jose import jwt
from app import schemas  
from app.config import settings
from .database import client, session

@pytest.fixture
def test_user(client):
    user_data = {"email": "admin@gmail.com",
                 "password": "admin123"}
    res = client.post("/users/", json=user_data)
    
    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

def test_root(client):
    res = client.get("/")
    # print(res.json().get('message'))
    assert res.json().get('message') == 'Hello World successfully deployed from CI/CD pipeline'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post(
         "/users/", json={"email": "admin@gmail.com", "password": "admin123"})
    
    new_user = schemas.UserOut(**res.json()) #pydantic model for schemas of UserOut
    assert  new_user.email == "admin@gmail.com" # for pass this test. need delete data in db for  repeat running
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']}
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, 
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    # print(res.json())
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gamil.com','password123',403),
    ('morteza@gmail.com','wrongpassword',403),
    ('worngemail@gmail.com','wrongpassword',403),
    (None,'password123',422),
    ('morteza@gmail.com',None,422) 
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})    
    
    assert res.status_code == status_code
    # assert res.json()).get('detail') == 'Invalid Credentails'