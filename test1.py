import re

text = "máy_bay nào đến thành_phố huế lúc 13 : 30hr ?"
text = re.sub(r'\b(\d+)\s*:\s*(\d+hr)\b', r'\1:\2', text)
print(text)