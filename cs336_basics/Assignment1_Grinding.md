<!--
 * #!/usr/bin/env python3
 * # -*- coding: utf-8 -*-
 * """
 * @@File: @File    : $TM_FILENAME
 * @@Author: @Author  : Yangdeqian(yangdeqian@baidu.com)
 * @@Time: @Time    : $CURRENT_YEAR/$CURRENT_MONTH/$CURRENT_DATE
 * @@Desc: @Desc    :  作业1
 * """
-->
# 学习目标：

# 2.1 The Unicode Standard
- 标准的unicode将字符转化为数字，理论上的最大值为U+10FFFF,约一百万code point，目前已经分配了29.7万
- ASCII（American Standard Code for Information Interchange） 是1960设为英语设计的128字符小字典，Unicode（Universal Character Set） 是1990为全人类设计的百万级别大字典
- **什么是字符**：在 Unicode 语境下，字符是一个**抽象的符号单位**——任何被 Unicode 标准收录并分配了 code point 的符号，都是"一个字符"。
- 字符不等于字节：字符是逻辑单位（有 code point 就是一个字符），字节是存储单位（UTF-8 编码后长度不等）

- ord(ordinal：序数，字符在编码表中的位置) 将字符转化为codepoint（码点）
- chr(character) 将codepoint 转化为 字符

## Unicode 数据探索性分析
## Unicode General Category 完整统计

| 类别代码 | 数量 | 示例 | 类别全称 | 含义说明 |
| --- | --- | --- | --- | --- |
| Co | 137,468 |  | Other, Private Use | 私用区，保留给用户/厂商自定义符号，无标准含义 |
| Lo | 127,004 | ª | Letter, Other | 无大小写区分的字母：CJK汉字、日文假名、阿拉伯文等 |
| So | 6,431 | ¦ | Symbol, Other | 其他符号：Emoji、箭头、图形符号等 |
| Ll | 2,155 | a | Letter, Lowercase | 小写字母：拉丁、希腊、西里尔等文字的小写形式 |
| Mn | 1,839 | ̀ | Mark, Nonspacing | 非间距组合符号：附加在前一字符上的重音、变音符等 |
| Lu | 1,791 | A | Letter, Uppercase | 大写字母：拉丁、希腊、西里尔等文字的大写形式 |
| Sm | 948 | + | Symbol, Math | 数学符号：加减乘除、积分、求和、逻辑运算符等 |
| No | 895 | ² | Number, Other | 其他数字：上标下标数字、分数、圈数字等 |
| Nd | 650 | 0 | Number, Decimal Digit | 十进制数字：各文字系统的 0-9（阿拉伯、印地、泰文等） |
| Po | 593 | ! | Punctuation, Other | 一般标点：句号、逗号、感叹号、问号等 |
| Mc | 443 | ः | Mark, Spacing Combining | 间距组合符号：占据独立空间的组合标记（如梵文元音符号） |
| Lm | 260 | ʰ | Letter, Modifier | 修饰字母：送气符、重音符等修饰发音的字母形符号 |
| Nl | 236 | ᛮ | Number, Letter | 字母数字：用字母表示的数字（罗马数字、卢恩数字等） |
| Cf | 161 | ­ | Other, Format | 格式控制字符：零宽连接符、软连字符等不可见格式符 |
| Sk | 123 | ^ | Symbol, Modifier | 修饰符号：独立的变音符号、重音符号 |
| Ps | 75 | ( | Punctuation, Open | 开括号：各种语言的左括号、左引号 |
| Pe | 73 | ) | Punctuation, Close | 闭括号：各种语言的右括号、右引号 |
| Cc | 65 |  | Other, Control | 控制字符：NULL、换行、制表符等 ASCII 控制码 |
| Sc | 62 | $ | Symbol, Currency | 货币符号：美元、欧元、日元、比特币等 |
| Lt | 31 | ǅ | Letter, Titlecase | 首字母大写：连字符的特殊大写形式（如 Dž, Lj） |
| Pd | 25 | - | Punctuation, Dash | 连接号/破折号：连字符、短破折号、长破折号等 |
| Zs | 17 |   | Separator, Space | 空格分隔符：普通空格、不换行空格、各种宽度空格 |
| Me | 13 | ҈ | Mark, Enclosing | 包围符号：将前一字符包围起来的组合标记 |
| Pi | 12 | « | Punctuation, Initial Quote | 开引号：左双引号、左单引号、左书名号等 |
| Pc | 10 | _ | Punctuation, Connector | 连接标点：下划线等用于连接单词的标点 |
| Pf | 10 | » | Punctuation, Final Quote | 闭引号：右双引号、右单引号、右书名号等 |
| Zl | 1 |  | Separator, Line | 行分隔符：U+2028，专用行分隔控制符 |
| Zp | 1 |  | Separator, Paragraph | 段落分隔符：U+2029，专用段落分隔控制符 |
| **总计** | **281,392** | | | |

## 关键结论

| 结论 | 数据支撑 | 对 Tokenizer 设计的启示 |
| --- | --- | --- |
| 私用区占比最大 | Co = 137,468 (48.9%) | 私用区无标准语义，BPE 训练时通常可忽略或低权重处理 |
| CJK 汉字是字母类主体 | Lo = 127,004，主要是汉字 | 汉字每个都是独立字符，天然适合作为独立 token |
| 真正的语言文字约 14.4 万 | 281,392 - 137,468 = 143,924 | 去掉私用区后，词表规模仍远大于 UTF-8 的 256 字节 |
| Emoji 藏在 So 类别 | So = 6,431 | Emoji 使用频率高，需确保 tokenizer 能正确处理 |
| 大小写字母不对称 | Lu = 1,791, Ll = 2,155 | 小写字母更多，因部分文字只有小写形式 |
| 控制字符数量有限 | Cc = 65, Cf = 161 | 控制字符虽少但影响文本处理，需特殊处理 |
| 数字表示形式多样 | Nd + Nl + No = 1,781 | 不同文字系统有各自数字，tokenizer 需考虑归一化 |

# Problem (unicode1): Understanding Unicode

## (a) What Unicode character does chr(0) return?

> chr(0)

'\x00'
> print(chr(0))


> "this" + chr(0) + "str"

'this\x00str'
> print("this" + chr(0) + "str")

thisstr


## (b) How does this character’s string representation (__repr__()) differ from its printed representation?
chr调用的主要是用的是repr，用于给调试人员看，而print用的是str，用于给用户看。


# 2.2 Unicode encoding

## Inspiration 
- Unicode 定义了映射关系：字符-> 整数（code point），没有定义『怎么存储』
> code point 范围是0-1百万，如何将这里面的整数变为字节
- <span style="color: rgba(255, 179, 0, 1)">将Unicode 字符（28万-13万=15万）转化为一系列的字节</span>
这就是 UTF (Unicode Transformation Format) 要解决的问题。
- 将文本转化为字节的问题

| 特性 | UTF-8 | UTF-16 | UTF-32 |
| --- | --- | --- | --- |
| **编码单元** | 1 字节 | 2 字节 | 4 字节 |
| **字符长度** | 1-4 字节（变长） | 2 或 4 字节（变长） | 固定 4 字节 |
| **ASCII 兼容** | ✅ 完全兼容 | ❌ 不兼容 | ❌ 不兼容 |
| **空间效率（英文）** | ⭐⭐⭐ 最优 | ⭐⭐ 中等 | ⭐ 最差 |
| **空间效率（中文）** | ⭐⭐ 3字节/字 | ⭐⭐⭐ 2字节/字 | ⭐ 4字节/字 |
| **随机访问** | ❌ O(n) | ❌ O(n) | ✅ O(1) |
| **主要应用场景** | Web、文件存储、Linux | Windows API、Java、JavaScript | 内部处理、定长需求 |


- 由字符组成的就是字符串
- UTF-8是存储的方式，1字节是8bit，所以需要将某个字符（码点，0-154997）转化为一系列byte（2-255）
Problem (unicode2): Unicode Encodings (3 points)

(a)问为什么训练tokenizer 都是在UTF-8而不是UTF-16/32？
因为utf8 使用广泛，utf16，32 都有很多冗余

(b)应该是函数将字节数组中的每一个数字都认为是同一个字符进行解码了，不应该单字节的进行编码，遇到中文字符就抓瞎了

(c) 找一个两字节的序列，并不能被转化为任何Unicode 的字符
- 问题转化：希望找到一个两字节的bytes（具体的存储字节），这个bytes 不能被转化为任何str（人看的）

- \x 代表转义十六进制"Hexadecimal"
- `b'\x61'` 等同于 `b'a'`。
- `b'\x0a'` 等同于 换行。
> type("hello") 人看的

<class 'str'>

> type(b"\xe4") （具体的存储字节）

<class 'bytes'>

解答：
找一个合法的 2 字节开头（比如 `0xC2`，二进制 `11000010`），但后面不给它合法的续字节（比如给个空格 `0x20`，二进制 `00100000`）。

```python
# b'\xC2' 说：后面应该来个以10开头的字节！
# b'\x20' 说：我是以00开头的ASCII，嘿嘿。
(b"\xC2\x20").decode("utf-8")
```

请回忆（或查阅）一下 UTF-8 的二进制规则表：
| 字节数 | 格式 (二进制) |
| :--- | :--- |
| 1 字节 | `0xxxxxxx` |
| 2 字节 | **`110xxxxx`** `10xxxxxx` |
| 3 字节 | `1110xxxx` `10xxxxxx` `10xxxxxx` |

| 错误类型 | 典型案例 (Python Bytes) | 报错信息 (Error Message) | 事故原因分析 (Architect's Analysis) |
| :--- | :--- | :--- | :--- |
| **1. 冗余编码**<br>(Overlong Encoding) | `b'\xC0\x00'`<br>或 `b'\xC1\x80'` | `invalid start byte` | **“伪造发票”**<br>`0xC0` 和 `0xC1` 被永久封杀。因为它们作为双字节开头时，只能组合出本该由单字节（ASCII）表示的字符。为了安全（防止绕过过滤），标准规定必须使用最短编码。 |
| **2. 错误的延续**<br>(Invalid Continuation) | `b'\xC2\x20'`<br>(开头好，结尾坏) | `invalid continuation byte` | **“搭档不合”**<br>第一个字节 `0xC2` 是合法的双字节头（期待后面来个 `10xxxxxx`）。但第二个字节 `0x20` (空格) 是个 ASCII (`00xxxxxx`)。解码器读到一半发现格式断了。 |
| **3. 孤立的延续符**<br>(Orphan Continuation) | `b'\x80\x00'` | `invalid start byte` | **“没头苍蝇”**<br>`0x80` (二进制 `10000000`) 被定义为“跟班”（延续字节）。它绝不能出现在开头。没有大哥带路，小弟不能单独行动。 |
| **4. 绝对非法字符**<br>(Illegal Bytes) | `b'\xFF\x00'` | `invalid start byte` | **“违禁品”**<br>`0xFF` 和 `0xFE` 在 UTF-8 标准中没有任何定义，出现在任何位置都是非法的。 |
| **5. 数据截断**<br>(Truncated Data) | `b'\xC2'`<br>(只有一半) | `unexpected end of data` | **“烂尾楼”**<br>`0xC2` 承诺了“后面还有一个字节”，但数据流突然结束了。这通常不是字节本身错了，而是数据没传完。 |



# 2.3 Subword Tokenization


>While byte-level tokenization can alleviate the out-of-vocabulary issues faced by word-level tokenizers, tokenizing text into bytes results in extremely long input sequences

- 单词级别的分词器如果遇到没见过的单词就会出现Out-of-Vocabulary Issues，例如字典中有apple，但是appl，苹果就无法识别
- 字节级别的分词器任何单词都可以识别，但是字典就爆炸了

- word-level model、 character-level model

- 字词分词器是 单词级别分词器(word-level)和字节级别分词器(byte-level)的综合

1. Vocabulary init: 初始化的字典大小就是256
2. Pre-token:将word 通过正则切出来
3. Compute BPE merges: 如果频率一样，选择字典序更大的
    - 所谓的“Break ties by preferring the lexicographically greater pair”，意思就是：当频率一样高时，选那个在字典里排在最后面的 Pair。
4. Special token：开始和结束的token


| 模型类型 (Model Type) | 颗粒度 (Granularity) | 示例 (Example: "Hi 你好") | 词表大小 (Vocabulary Size) | 序列长度 (Sequence Length) | 建筑师评价 (Architect's Note) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Word-level**<br>(单词级) | **整词**<br>(Whole Words) | `["Hi", "你好"]`<br>(2 Tokens) | **巨大** (>100k)<br>容易有 OOV (未登录词) ,新单词容易找不到，| **极短**<br>效率最高，但遇到生僻词就瘫痪 (UNK)。 | **“整块预制板”**<br>建得快，但极其僵化。遇到字典里没有的词，只能留个大窟窿。 |
| **Character-level**<br>(字符级) | **字符**<br>(Unicode Char) | `['H', 'i', ' ', '你', '好']`<br>(5 Tokens) | **两极分化**<br>纯英文: ~100 (极小)<br>含中文: >10万 (巨大且稀疏!) | **很长**<br>英文比 Word 级长 5 倍。<br>中文是 1 字 1 Token。 | **“原子级堆砌”**<br>纯英文还凑合，但一旦引入中文，词表又大、序列又长，两头的缺点都占了。 |
| **Byte-level (Pure)**<br>(纯字节级) | **字节**<br>(UTF-8 Bytes) | `[72, 105, 32, 228, 189, 160, ...]`<br>(9 Tokens)<br>*注: "你"=3 tokens* | **极小固定 (256)**<br>(0x00 - 0xFF)<br>永无 OOV。 | **最长**<br>中文变 3 倍长，Emoji 变 4 倍长。<br>计算量最大。 | **“二进制碎渣”**<br>这是最底层的原材料。虽然彻底消灭了 OOV，但把汉字拆得太碎，模型很难理解语义，训练极慢。 |
| **Subword (BPE)**<br>(现代标准 Byte-level BPE) | **混合**<br>(Adaptive) | `["Hi", " ", "你", "好"]`<br>(4 Tokens) | **适中 (~50k-100k)**<br>人为设定的“黄金平衡点”。 | **适中**<br>常用字合并(1 token)，生僻字拆解(bytes)。 | **“模块化施工”**<br>先把它粉碎成 Bytes (防止 OOV)，再把最常用的碎片粘回去 (保证效率)。**这是目前 LLM 的最优解。** |

- BPE：通过将最常见的部分都给他压缩为同一个token
## 在这节课中，我们需要实现一个byte-level BPE tokenizer


# 2.4 BPE 分词器训练 
- vocabulary init:初始的词表大小是256大小
- pre-tokenization:在做BPE之前，我们通常需要先将字符串切碎，如果不切碎分词器会将"dog!","dog,"都作为不同的token，这是不正确的
- Pre-tokenization = 先粗切 + 统计频次，BPE = 在粗切的块内部做细粒度合并。




## Suspendix

>>> 281,392 - 137,468(python 将起试做两个元组) ===（281, 392-137 ,468）
(281, 255, 468)