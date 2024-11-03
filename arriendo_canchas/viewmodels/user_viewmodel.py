# viewmodels/user_viewmodel.py

class UserViewModel:
    def __init__(self):
        self.user = None  # Aquí almacenaremos el usuario autenticado

    def set_user(self, user_data):
        self.user = user_data

    def get_user(self):
        return self.user

    def is_authenticated(self):
        return self.user is not None

    def logout(self):
        self.user = None
