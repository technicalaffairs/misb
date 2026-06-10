import urllib.request
url = 'https://technicalaffairs.github.io/MPIS/arabic_web/Ar_gen_docs/Ar_Gas%20Turbines_docs%20Page.htm'
try:
    with urllib.request.urlopen(url) as response:
        b = response.read()
        print('Live byte size:', len(b))
        idx = b.find(b'<h1 style="color: #d9534f')
        if idx != -1:
            print('Found H1 on live site:')
            print(b[idx:idx+200])
        else:
            print('Not found')
except Exception as e:
    print(e)
