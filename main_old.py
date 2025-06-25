# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# FastAPI アプリケーションの初期化
app = FastAPI(title="FastAPI + localLLM Tutorial")

# Hugging FaceのTransformersを利用して、テキスト生成パイプラインを作成
# 小さなモデルとして 'distilgpt2' を使用（初回実行時にモデルがダウンロードされます）
# generator = pipeline("text-generation", model="distilgpt2")

# 日本語が必要な場合は以下
# generator = pipeline("text-generation", model="rinna/japanese-gpt2-medium")
# generator = pipeline("text-generation", model="rinna/japanese-gpt2-small")
# 明示的にトークナイザーを作成（use_fast=False を設定）
tokenizer = AutoTokenizer.from_pretrained("rinna/japanese-gpt2-medium", use_fast=False)
# モデルも明示的にロード（モデルによっては AutoModelForCausalLM や AutoModelForSeq2SeqLM などを使う）
model = AutoModelForCausalLM.from_pretrained("rinna/japanese-gpt2-medium")

# pipeline にトークナイザーとモデルを渡す
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)


# リクエストボディのスキーマ定義
class Prompt(BaseModel):
    prompt: str


# POST エンドポイント /generate を定義
@app.post("/generate")
async def generate_text(data: Prompt):
    try:
        # 入力されたプロンプトに対してテキスト生成を実行
        result = generator(data.prompt, max_length=50, num_return_sequences=1)
        generated_text = result[0]["generated_text"]
        return {"generated_text": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ルートパスの簡単な紹介
@app.get("/")
async def root():
    return {"message": "FastAPI + localLLM Tutorial API"}
