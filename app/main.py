from fastapi import FastAPI, Body
import os
from app.utils import detect_source_language, split_article
from app.translator import translate_batch

ROOT_PATH = os.getenv("ROOT_PATH", "")

app = FastAPI(
    title="AI Translation API",
    root_path=ROOT_PATH,
    version="1.0"
)


@app.post("/translate")
def translate_article(
    text: str = Body(..., media_type="text/plain"),
    target_language: str = "eng_Latn"
):
    source_lang = detect_source_language(text)

    chunks = split_article(text)

    translated_chunks = translate_batch(
        texts=chunks,
        src_lang=source_lang,
        tgt_lang=target_language
    )

    return {
        "detected_source_language": source_lang,
        "target_language": target_language,
        "translated_text": "\n\n".join(translated_chunks)
    }