## 用于测试一下unicode 里面都有哪些字符

import unicodedata
from collections import Counter

categories  = Counter()
scripts = Counter()
sample_chars = {}

for codepoint in range(0,0x110000):
    ## 将int --> char
    char = chr(codepoint)
    # name = unicodedata.name(char,None) 返回人类可读的描述
    cat = unicodedata.category(char)## 标准化的分类代码
    if cat not in ('Cn', 'Cs') :
        
        categories[cat] += 1
        # print(codepoint, char, name)
        # break

        if cat not in sample_chars:
            sample_chars[cat] = char

for cat, count in categories.most_common():
    # print(f"{cat}:{count:>6} example {sample_chars.get(cat)}
    print(f"{cat}:{count:>6} example {sample_chars.get(cat)}")


print(f"sum {sum(categories.values())}")