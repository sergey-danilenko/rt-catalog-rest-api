def format_phone_num(num: str) -> str:
    if not num.isdigit():
        return num
    return f"{num[0]}-{num[1:4]}-{num[4:7]}-{num[7:9]}-{num[9:]}"
