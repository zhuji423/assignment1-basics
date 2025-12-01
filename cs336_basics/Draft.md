<!--
 * #!/usr/bin/env python3
 * # -*- coding: utf-8 -*-
 * """
 * @@File: @File    : $TM_FILENAME
 * @@Author: @Author  : Yangdeqian(yangdeqian@baidu.com)
 * @@Time: @Time    : $CURRENT_YEAR/$CURRENT_MONTH/$CURRENT_DATE
 * @@Desc: @Desc    : 
 * """
-->
#学习目标：

# Problem (unicode1): Understanding Unicode

## (a) What Unicode character does chr(0) return?

> chr(0)
> '\x00'
> print(chr(0))

> "this" + chr(0) + "str"
> 'this\x00str'
> print("this" + chr(0) + "str")
> thisstr


## (b) How does this character’s string representation (__repr__()) differ from its printed representation?
chr调用的主要是用的是repr，用于给调试人员看，而print用的是str，用于给用户看。