"""
constants file
"""

permission = {
    "login": 1,
    "vote": 2,
    "admin": 4,
}

role = {
    "user": permission["login"] | permission["vote"],
    "admin": permission["login"] | permission["vote"] | permission["admin"],
}
