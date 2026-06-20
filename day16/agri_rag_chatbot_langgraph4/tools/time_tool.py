from langchain.tools import tool
from datetime import datetime

@tool
def get_time():
    """
    현재 날짜와 시간을 반환한다.
    """
    print("\n[get_time Tool 실행]")
    
    return str(datetime.now())

