import pytest
from jose import jwt
from app import schemas  
from app.config import settings
from .database import client, session



# def test_root(client):
#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Hello World'
#     assert res.status_code == 200

def test_create_user(client):
    res = client.post(
         "/users", json={"email": "hello123@gmail.com", "password": "password123"})
    
    new_user = schemas.UserOut(**res.json()) #pydantic model for schemas of UserOut
    assert  new_user.email == "hello123@gmail.com" # for pass this test. need delete data in db for  repeat running
    assert res.status_code == 201

def test_login_user(test_user, client):
    res = client.post(
        "/login", date={"username": test_user['email'], "password": test_user['password']}
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