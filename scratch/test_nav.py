import urllib.request
import re
url = 'https://technicalaffairs.github.io/MPIS/arabic_web/Ar_gen_docs/Ar_Gas%20Turbines_docs%20Page.htm'
try:
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8', errors='ignore')
        if '<nav class="main-nav">' in html:
            print('Nav exists!')
        else:
            print('Nav MISSING!')
            
        nav = re.search(r'<nav.*?</nav>', html, re.DOTALL)
        if nav: print(nav.group(0)[:500])
except Exception as e:
    print(e)
