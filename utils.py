from typing import List, Dict
import re
from collections import Counter

def extract_keywords(text: str) -> List[str]:
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    words_to_be_ignored = {"the","and","for","with","this","that","from","have","has",
                 "are","was","were","but","not","you","your","about","into",
                 "will","shall","would","could","there","their","they"}
    words = [w for w in words if w not in words_to_be_ignored]
    counter = Counter(words)
    return [w for w, _ in counter.most_common(3)]