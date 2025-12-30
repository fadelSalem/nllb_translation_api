from fastapi import FastAPI
from pydantic import BaseModel
import os
from app.utils import detect_source_language, split_article
from app.translator import translate_batch

ROOT_PATH = os.getenv("ROOT_PATH", "")

app = FastAPI(
    title="AI Translation API",
    root_path=ROOT_PATH,
    version="1.0"
)


class TranslateRequest(BaseModel):
    text: str
    target_language: str


@app.post("/translate")
def translate_article(data: TranslateRequest):
    source_lang = detect_source_language(data.text)

    chunks = split_article(data.text)

    translated_chunks = translate_batch(
        texts=chunks,
        src_lang=source_lang,
        tgt_lang=data.target_language
    )

    return {
        "detected_source_language": source_lang,
        "target_language": data.target_language,
        "translated_text": "\n\n".join(translated_chunks)
    }