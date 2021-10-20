import hashlib

class Config:
    def __init__(self, username = '', password = '', server = ''):
        self.username = username
        self.password = hashlib.md5(password.encode('utf-8')).hexdigest()
        self.server = f'https://{server}.battleknight.gameforge.com/'