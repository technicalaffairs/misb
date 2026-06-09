import re
text = '<font color="#FF0000"><big><big><big> <span lang="en-us">Air Heaters</span></big></big></big></font>'
eng_word = 'Air Heaters'
ar_title = 'مسخنات الهواء'

title_regex = re.compile(r'(<big>|<span[^>]*>|<font[^>]*>)\s*(' + re.escape(eng_word) + r'.*?)\s*(</big>|</span>|</font>)', re.IGNORECASE)
def replace_title(m):
    return m.group(1) + ar_title + m.group(3)

print("Original:", text)
new_content = title_regex.sub(replace_title, text)
print("Regex replace 1:", new_content)

# Why didn't it match fully? 
# Because <span lang="en-us">Air Heaters</span> has <span...> then text then </span>
# So it matched <span lang="en-us"> as group 1, Air Heaters as group 2, </span> as group 3.
# But it leaves the outer <big> tags untouched! Which is FINE, the text is replaced.
