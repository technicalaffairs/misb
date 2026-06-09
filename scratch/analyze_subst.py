import re
from html.parser import HTMLParser

class SubParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.current_row = []
        self.current_cell = ""
        self.current_links = []
        self.rows = []
        self.table_count = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == "table":
            self.in_table = True
        elif tag == "tr" and self.in_table:
            self.current_row = []
        elif tag in ("td", "th") and self.in_table:
            self.current_cell = ""
            self.current_links = []
        elif tag == "a" and self.in_table:
            attrs_dict = dict(attrs)
            if "href" in attrs_dict:
                self.current_links.append(attrs_dict["href"])

    def handle_data(self, data):
        if self.in_table:
            self.current_cell += data

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "table":
            self.in_table = False
        elif tag == "tr" and self.in_table:
            self.rows.append((self.current_row, self.current_links))
        elif tag in ("td", "th") and self.in_table:
            cell_text = self.current_cell.strip()
            cell_text = " ".join(cell_text.split())
            self.current_row.append((cell_text, list(self.current_links)))
            self.current_cell = ""
            self.current_links = []

file_path = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\Ar_ad_subst.htm"

with open(file_path, "r", encoding="windows-1252", errors="ignore") as f:
    html_content = f.read()

html_content = re.sub(r"<!--.*?-->", "", html_content, flags=re.DOTALL)

parser = SubParser()
parser.feed(html_content)

for idx, (cells, links) in enumerate(parser.rows):
    all_text = " ".join([c[0] for c in cells])
    # Extract any document code like CB-xxx, T-xxx, BB-xxx, DS-xxx, B-xxx, Ch-xxx
    codes = re.findall(r'[a-zA-Z]+-\d+-\w+', all_text)
    if not codes:
        codes = re.findall(r'[a-zA-Z]+-\d+', all_text)
    
    print(f"Row {idx:2d} | Codes: {str(codes):20s} | Links: {links} | Text snippet: {all_text[:60]}")
