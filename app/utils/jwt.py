"""
@ coding : utf-8 
@Time    : 2025/10/25 11:52
@Author  : admin
@Project : fastapi_wms
@File    : jwt.py
@Software: PyCharm
@Notes   : 返回用户登录token
"""
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict

# secret key 和算法
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 # token有效期

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None)-> Dict:
    """生成JWT token"""
    to_encode = data.copy()
    # 设置令牌过期时间
    expire = datetime.now(tz=timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": int(expire.timestamp())}) # 设置过期时间
    # 生成token
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # 转换北京时间 utc+8
    beijing_tz = timezone(timedelta(hours=+8))
    expire_bj = expire.astimezone(beijing_tz)

    return {
        "access_token": encode_jwt,
        "token_type": "bearer",
        "expires": expire_bj.isoformat(),
    }

def verify_access_token(token: str)-> Optional[Dict]:
    """验证JWT令牌并返回解码后的数据"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise JWTError(f"令牌验证失败：{e}")

