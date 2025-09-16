from fastapi import FastAPI, Query, HTTPException
import sqlite3
from analyzer import analyze_text
import db
from utils import extract_keywords
import docs

app = FastAPI(title="Vipin : Sample project for Jouster")

db.init_db()





@app.post("/analyze", response_model=docs.AnalyzeResponse)
def analyze(req: docs.AnalyzeRequest):
    if not req.text or not req.text.strip():
        raise HTTPException(
            status_code=400,
            detail="The 'text' field is required and cannot be empty."
        )
    result = analyze_text(req.text)

    if "error" in result:
        raise HTTPException(
            status_code=400,
            detail=f"An error occured: {result}"
        )

    summary = result.get("summary")
    structured = result.get("structured_data", {})
    title = structured.get("title")
    topics = ",".join(structured.get("topics", []))
    sentiment = structured.get("sentiment")
    keywords = ",".join(extract_keywords(req.text))

    db.insert_analysis(summary, title, topics, sentiment, keywords)

    # return {
    #     "summary": summary,
    #     "structured_data": structured,
    #     "keywords": keywords.split(","),
    # }
    return {
        "summary": summary,
        "title": title,
        "topics": topics.split(","),
        "sentiment": sentiment,
        "keywords": keywords.split(","),
    }

@app.get("/search", response_model=docs.SearchResponse)
def search(topic: str = Query(...)):
    topic = topic.strip()
    if not topic:
        raise HTTPException(
            status_code=400,
            detail="The 'topic' query parameter cannot be empty."
        )
    results = db.search_analysis(topic)
    return {"results": results}
