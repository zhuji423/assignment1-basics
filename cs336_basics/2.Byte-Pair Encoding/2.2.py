
test_string = "hello! こんにちは!안녕하세요"
utf8_encode: bytes = test_string.encode("utf-8")
utf16_encode: bytes = test_string.encode("utf-16")
utf32_encode: bytes = test_string.encode("utf-32")



print("utf8",list(utf8_encode),len(list(utf8_encode)),"\n",
"utf16",list(utf16_encode),len(list(utf16_encode)),"\n",
"utf32",list(utf32_encode),len(list(utf32_encode)))

# 38 utf8 [104, 101, 108, 108, 111, 33, 32, 227, 129, 147, 227, 130, 147, 227, 129, 171, 227, 129, 161, 227, 129, 175, 33, 236, 149, 136, 235, 133, 149, 237, 149, 152, 236, 132, 184, 236, 154, 148] 
# 38 utf16 [255, 254, 104, 0, 101, 0, 108, 0, 108, 0, 111, 0, 33, 0, 32, 0, 83, 48, 147, 48, 107, 48, 97, 48, 111, 48, 33, 0, 72, 197, 85, 177, 88, 213, 56, 193, 148, 198] 
# 76 utf32 [255, 254, 0, 0, 104, 0, 0, 0, 101, 0, 0, 0, 108, 0, 0, 0, 108, 0, 0, 0, 111, 0, 0, 0, 33, 0, 0, 0, 32, 0, 0, 0, 83, 48, 0, 0, 147, 48, 0, 0, 107, 48, 0, 0, 97, 48, 0, 0, 111, 48, 0, 0, 33, 0, 0, 0, 72, 197, 0, 0, 85, 177, 0, 0, 88, 213, 0, 0, 56, 193, 0, 0, 148, 198, 0, 0]


def decode_utf8_bytes_to_str_wrong(bytestring: bytes):
    return "".join([bytes([b]).decode("utf-8") for b in bytestring])

result = decode_utf8_bytes_to_str_wrong("hello,你".encode("utf-8"))

print(f"wrong code:{result}"  )   # utf8_encode