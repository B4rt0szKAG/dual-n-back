class WrongPass(Exception):
    pass

class WrongLogin(Exception):
    pass

class TokenAlreadyExists(Exception):
    def __init__(self,token):
        super().__init__()
        self.token = token