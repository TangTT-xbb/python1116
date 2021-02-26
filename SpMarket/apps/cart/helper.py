
def json_msg(code,msg=None,data=None):
    """
    封装json消息
    code 0 正确
    其他为错误
    """
    return {"code":code,"errmsg":msg,"data":data}