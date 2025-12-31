from fastapi import FastAPI, Body
import os
from app.utils import split_article, split_sentences, detect_language_per_sentence
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
    sentences = split_sentences(text)
    detected = detect_language_per_sentence(sentences)

    translated_sentences = []

    for sentence, src_lang in detected:
        chunks = split_article(sentence)
        translated_chunks = translate_batch(
            texts=chunks,
            src_lang=src_lang,
            tgt_lang=target_language
        )
        translated_sentences.append(" ".join(translated_chunks))

    return {
        "detected_source_language": list(set(lang for _, lang in detected)),
        "target_language": target_language,
        "translated_text": " ".join(translated_sentences)
    }