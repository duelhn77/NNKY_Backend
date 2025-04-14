# app/quickdiagnose.py
from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import JSONResponse
import openai, aiofiles, os, re, base64
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image
from sqlalchemy.orm import Session
from fastapi import Depends
from db_control.connect import engine
from db_control.mymodels import QuickDiagnosis
from db_control.crud import create_quick_diagnosis
from db_control.auth import verify_access_token
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session, sessionmaker  



router = APIRouter()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def sanitize_filename(filename: str) -> str:
    return re.sub(r"[\\/*?\"<>|:]", "_", filename)

@router.post("/diagnose")
async def diagnose(
    file: UploadFile = File(...),
    prompt: str = Form(...),
    token: str = Form(None),
    db: Session = Depends(get_db)
):
    # 保存処理
    safe_time = datetime.utcnow().isoformat().replace(":", "_").replace(".", "_")
    safe_name = sanitize_filename(file.filename)
    filename = f"{safe_time}_{safe_name}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    with open(file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded_image}"}}
            ]}
        ],
        max_tokens=1000
    )

    result_text = response.choices[0].message.content

    # ✅ ユーザーIDをトークンから取得してDB保存（認証していない場合はNone）
    user_id = None
    if token:
        payload = verify_access_token(token)
        if payload:
            email = payload.get("sub")
            from db_control.crud import find_user_by_email
            user = find_user_by_email(email)
            user_id = user.user_id if user else None

    # ✅ DBへ診断結果を保存
    create_quick_diagnosis(db=db, user_id=user_id, result_summary=result_text)

    return JSONResponse({
        "image_url": f"/uploads/{filename}",
        "result": result_text
    })


@router.post("/recommend")
async def recommend(prompt: str = Form(...)):
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt + " 回答はわかりやすく、実際の商品名を挙げてください。"}],
        max_tokens=1000,
    )
    return JSONResponse({"result": response.choices[0].message.content})

@router.get("/all-diagnoses")
def get_all_diagnoses(db: Session = Depends(get_db)):
    diagnoses = db.query(QuickDiagnosis).order_by(QuickDiagnosis.created_at.desc()).all()
    return [
        {
            "id": d.quick_diagnosis_id,
            "user_id": d.user_id,
            "result": d.result_summary[:80],  # 結果が長いとき先頭だけ
            "created_at": d.created_at.isoformat()
        }
        for d in diagnoses
    ]

