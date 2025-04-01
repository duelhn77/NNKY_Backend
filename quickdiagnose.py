from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import openai
import aiofiles
import os
from datetime import datetime
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import re
import base64
from PIL import Image

# .envファイルから環境変数を読み込み
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントのURLを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def sanitize_filename(filename: str) -> str:
    """Windows非対応の文字を取り除く"""
    filename = re.sub(r"[\\/*?\"<>|:]", "_", filename)
    return filename

@app.post("/diagnose")
async def diagnose(file: UploadFile = File(...), prompt: str = Form(...)):
    safe_time = datetime.utcnow().isoformat().replace(":", "_").replace(".", "_")
    safe_name = sanitize_filename(file.filename)
    filename = f"{safe_time}_{safe_name}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # 画像を保存
    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    # PILで画像をBase64エンコード
    with open(file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    # OpenAI Vision APIの呼び出し（Base64形式で送信）
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{encoded_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=1000
    )

    result_text = response.choices[0].message.content

    return JSONResponse({
        "image_url": f"/uploads/{filename}",
        "result": result_text
    })