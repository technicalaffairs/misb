import os
import re
from bs4 import BeautifulSoup

filepath = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_about\Ar_about.htm"
with open(filepath, "r", encoding="windows-1256", errors="ignore") as f:
    html = f.read()

# Strip FrontPage comments and premature closings
html_clean = re.sub(r'<!\[if[^\]]*\]>', '', html, flags=re.IGNORECASE)
html_clean = re.sub(r'<!\[endif\]>', '', html_clean, flags=re.IGNORECASE)
html_clean = re.sub(r'</body[^>]*>', '', html_clean, flags=re.IGNORECASE)
html_clean = re.sub(r'</html[^>]*>', '', html_clean, flags=re.IGNORECASE)

soup = BeautifulSoup(html_clean, "html.parser")
tables = soup.find_all("table")
print(f"Found {len(tables)} tables:")
for i, t in enumerate(tables):
    print(f"Table {i}: id={t.get('id')}, class={t.get('class')}, rows={len(t.find_all('tr'))}")

# Let's see what is outside tables
# We decompose the tables
for t in tables:
    t.decompose()

print("\nContent remaining in body:")
print(str(soup.body)[:500])
