from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
import json

# ルーターのインポート
from app import user
from app.quickdiagnose import router as quickdiagnose_router

# DB操作用
from db_control import crud, mymodels
from db_control.create_tables import init_db

# アプリケーション作成
app = FastAPI()

# 🔧 テーブル作成（初回起動時のみ有効）
init_db()

# 🌐 CORS設定（フロントエンドとの連携用）
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    FRONTEND_URL
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔗 各種ルーターを登録
app.include_router(user.router)                # ユーザー登録・ログイン
app.include_router(quickdiagnose_router)       # クイック診断

# -------------------------------------
# 🧪 以下は Practical オリジナル機能（顧客管理）
# -------------------------------------

class Customer(BaseModel):
    customer_id: str
    customer_name: str
    age: int
    gender: str


@app.get("/")
def index():
    return {"message": "FastAPI top page!"}


@app.post("/customers")
def create_customer(customer: Customer):
    values = customer.dict()
    crud.myinsert(mymodels.Customers, values)
    result = crud.myselect(mymodels.Customers, values.get("customer_id"))
    return json.loads(result) if result else None


@app.get("/customers")
def read_one_customer(customer_id: str = Query(...)):
    result = crud.myselect(mymodels.Customers, customer_id)
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    return json.loads(result)[0]


@app.get("/allcustomers")
def read_all_customer():
    result = crud.myselectAll(mymodels.Customers)
    return json.loads(result) if result else []


@app.put("/customers")
def update_customer(customer: Customer):
    values = customer.dict()
    crud.myupdate(mymodels.Customers, values)
    result = crud.myselect(mymodels.Customers, values.get("customer_id"))
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    return json.loads(result)[0]


@app.delete("/customers")
def delete_customer(customer_id: str = Query(...)):
    result = crud.mydelete(mymodels.Customers, customer_id)
    if not result:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"customer_id": customer_id, "status": "deleted"}


@app.get("/fetchtest")
def fetchtest():
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    return response.json()

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db_control import auth  # JWT系関数を使うため
from db_control import mymodels  # ユーザーモデルがある場合
from db_control import crud  # DBからユーザーを取得
from jose import JWTError

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 仮のユーザー取得関数（ユーザー名で検索）
def get_user_by_username(username: str):
    result = crud.myselect(mymodels.Users, username)
    if result:
        return result[0]  # パース済みのdictを想定
    return None

# 🔐 ログインしてJWTトークン発行
@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_username(form_data.username)
    if not user or not auth.verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = auth.create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

# 🔒 保護されたルート例
@router.get("/me")
def read_users_me(token: str = Depends(oauth2_scheme)):
    payload = auth.verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"username": payload["sub"]}
