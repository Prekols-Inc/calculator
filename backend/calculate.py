def calculate(expr: str) -> tuple:
    try:
        ans = eval(expr)
        result = True
    except BaseException as e:
        ans = 0 
        result = False
        print(e)
    return (result, ans)
