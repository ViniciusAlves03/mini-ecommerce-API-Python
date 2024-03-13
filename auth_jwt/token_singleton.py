from .token import Token
from config import jwt_config

token_creator = Token(
    token_key=jwt_config["TOKEN_KEY"],
    exp_time_min=jwt_config["EXP_TIME_MIN"],
    refresh_time_min=jwt_config["REFRESH_TIME_MIN"]
)

