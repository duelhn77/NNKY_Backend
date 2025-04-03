# app/quickdiagnose.py
from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import JSONResponse
import openai, aiofiles, os, re, base64
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image

router = APIRouter()

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def sanitize_filename(filename: str) -> str:
    return re.sub(r"[\\/*?\"<>|:]", "_", filename)

@router.post("/diagnose")
async def diagnose(file: UploadFile = File(...), prompt: str = Form(...)):
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

    return JSONResponse({
        "image_url": f"/uploads/{filename}",
        "result": response.choices[0].message.content
    })

@router.post("/recommend")
async def recommend(prompt: str = Form(...)):
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt + " 回答はわかりやすく、実際の商品名を挙げてください。"}],
        max_tokens=1000,
    )
    return JSONResponse({"result": response.choices[0].message.content})
