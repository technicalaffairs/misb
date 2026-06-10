import urllib.request
import re
url = 'https://technicalaffairs.github.io/MPIS/arabic_web/Ar_gen_docs/Ar_Gas%20Turbines_docs%20Page.htm'
try:
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('windows-1256', errors='ignore')
        nav = re.search(r'<nav class="main-nav">(.*?)</nav>', html, re.DOTALL)
        if nav:
            print('Buttons count:', nav.group(1).count('<a '))
        else:
            print('No nav found')
except Exception as e:
    print(e)
