from typing import List, Optional
from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    text: str 


class AnalyzeResponse(BaseModel):
    summary: Optional[str]
    title: Optional[str]
    topics: List[str]
    sentiment: Optional[str]
    keywords: List[str]


class SearchResultItem(BaseModel):
    summary: Optional[str]
    title: Optional[str]
    topics: List[str]
    sentiment: Optional[str]
    keywords: List[str]

class SearchResponse(BaseModel):
    results: List[SearchResultItem]