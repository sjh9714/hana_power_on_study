# ============================================================
# Redis
# ============================================================

import redis

# JSON 변환
import json


# ============================================================
# Redis 연결
# ============================================================

redis_client = redis.Redis(

    host="localhost",

    port=6379,

    db=0,

    decode_responses=True
)


# ============================================================
# 고객 상태 조회
# ============================================================

def get_customer_state(cc_num):

    # Redis Key
    key = f"customer:{cc_num}"

    # 데이터 조회
    data = redis_client.get(key)

    # 없으면 None
    if data is None:
        return None

    # JSON → dict 변환
    return json.loads(data)


# ============================================================
# 고객 상태 저장
# ============================================================

def save_customer_state(

    cc_num,
    state

):

    # Redis Key
    key = f"customer:{cc_num}"

    # dict → JSON 변환 후 저장
    redis_client.set(

        key,

        json.dumps(state)
    )