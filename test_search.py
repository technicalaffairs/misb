import json
import re
from collections import Counter

# Load index globally
print("Loading search index...")
try:
    with open('search_index.json', 'r', encoding='utf-8') as f:
        SEARCH_INDEX = json.load(f)
    print(f"Loaded {len(SEARCH_INDEX)} files into memory.")
except Exception as e:
    print(f"Error loading index: {e}")
    SEARCH_INDEX = []

def search_site(query: str) -> str:
    """
    يبحث في مستندات وصفحات موقع محطة المحولات عن الكلمات المفتاحية المتعلقة بسؤال المستخدم.
    قم بتمرير الكلمات المفتاحية باللغة العربية أو الإنجليزية إلى هذه الدالة.
    ترجع الدالة أفضل 3 صفحات مطابقة تحتوي على المعلومات مع روابطها.
    """
    if not SEARCH_INDEX:
        return "عذراً، الفهرس غير متاح حالياً."
        
    # Simple keyword scoring
    keywords = set(re.findall(r'\w+', query.lower()))
    if not keywords:
        return "لا توجد كلمات مفتاحية في البحث."
        
    scored_results = []
    
    for doc in SEARCH_INDEX:
        content_lower = doc['content'].lower()
        title_lower = doc['title'].lower()
        
        score = 0
        for kw in keywords:
            if len(kw) < 3: continue # Ignore short words
            score += title_lower.count(kw) * 5 # Title matches are worth more
            score += content_lower.count(kw)
            
        if score > 0:
            scored_results.append((score, doc))
            
    # Sort by score descending
    scored_results.sort(key=lambda x: x[0], reverse=True)
    
    top_results = scored_results[:3]
    
    if not top_results:
        return "لم يتم العثور على أي معلومات حول هذا الموضوع في مستندات الموقع."
        
    result_text = "نتائج البحث في مستندات الموقع:\n\n"
    for idx, (score, doc) in enumerate(top_results):
        # Extract a snippet around the first keyword found
        snippet = doc['content'][:1000] # Just return first 1000 chars for context
        for kw in keywords:
            if len(kw) > 2 and kw in doc['content'].lower():
                pos = doc['content'].lower().find(kw)
                start = max(0, pos - 200)
                end = min(len(doc['content']), pos + 800)
                snippet = doc['content'][start:end]
                break
                
        result_text += f"--- النتيجة {idx+1} ---\n"
        result_text += f"العنوان: {doc['title']}\n"
        result_text += f"مسار الملف: {doc['path']}\n"
        result_text += f"المحتوى: ...{snippet}...\n\n"
        
    return result_text

if __name__ == "__main__":
    print(search_site("مغيرات الجهد"))
    print(search_site("محول"))
