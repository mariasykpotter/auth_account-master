import hashlib


class AuthException(Exception):
    def __init__(self, username = "", user=None):
        super().__init__(username, user)
        self.username = username
        self.user = user


class UsernameAlreadyExists(AuthException):
    def __str__(self):
        return "Username already exists"


class SuperUsernameAlreadyExists(AuthException):
    def __str__(self):
        return "Superusername already exists"


class PasswordTooShort(AuthException):
    def __str__(self):
        return "Password is too short"


class InvalidUsername(AuthException):
    def __str__(self):
        return "There is an invalid username"


class InvalidPassword(AuthException):
    def __str__(self):
        return "There is an invalid password"


class PermissionError(AuthException):
    def __str__(self):
        return "There is a permission error"


class NotLoggedInError(AuthException):
    def __str__(self):
        return "You are not logged in"


class NotPermittedError(AuthException):
    def __str__(self):
        return "Forbidden"


class Unexistingaccount(AuthException):
    def __str__(self):
        return "First sign up, then sign in"


class User:
    def __init__(self, username, password, superuser=False):
        """Create a new user object. The password
        will be encrypted before storing."""
        self.username = username
        self.password = self._encrypt_pw(password)
        self.is_logged_in = False
        self.superuser = superuser

    def _encrypt_pw(self, password):
        """Encrypt the password with the username and return
        the sha digest."""
        hash_string = self.username + password
        hash_string = hash_string.encode("utf8")
        return hashlib.sha256(hash_string).hexdigest()

    def check_password(self, password):
        """Return True if the password is valid for this
        user, false otherwise."""
        encrypted = self._encrypt_pw(password)
        return encrypted == self.password


class Authenticator:
    def __init__(self):
        """Construct an authenticator to manage
        users logging in and out."""
        self.root = {}
        self.users = {}

    def check_root(self):
        if not self.root:
            return False
        else:
            return True

    def add_user(self, username, password, superuser=False):
        if superuser == True:
            if not self.root:
                self.root[username] = User(username, password)
            else:
                print(SuperUsernameAlreadyExists(username))
        if username in self.users:
            print(UsernameAlreadyExists(username))
        if len(password) < 6:
            print(PasswordTooShort(username))
        self.users[username] = User(username, password)

    def login(self, username, password):
        try:
            user = self.users[username]
        except KeyError:
            try:
                raise InvalidUsername(username)
            except:
                print(InvalidUsername(username))
        try:
            if not self.users[username].check_password(password):
                    raise InvalidPassword(username)
            self.users[username].is_logged_in = True
            return True
        except:
            print(InvalidPassword(username))



    def is_logged_in(self, username):
        if username in self.users:
            return self.users[username].is_logged_in
        return False

    def logout(self, username):
        del self.users[username]


class Authorizor:
    def __init__(self, authenticator):
        self.authenticator = authenticator
        self.permissions = {}

    def add_permission(self, perm_name):
        """Create a new permission that users
        can be added to"""
        try:
            perm_set = self.permissions[perm_name]
        except KeyError:
            self.permissions[perm_name] = set()
        else:
            try:
                raise PermissionError("Permission Exists")
            except:
                print(PermissionError("Permission Exists"))

    def permit_user(self, perm_name, username):
        """Grant the given permission to the user"""
        try:
            perm_set = self.permissions[perm_name]
        except KeyError:
            raise PermissionError("Permission does not exist")
        else:
            if username not in self.authenticator.users:
                raise InvalidUsername(username)
            perm_set.add(username)

    def check_permission(self, perm_name, username):
        if not self.authenticator.is_logged_in(username):
            try:
                raise NotLoggedInError(username)
            except:
                print(NotLoggedInError(username))
        try:
            perm_set = self.permissions[perm_name]
        except KeyError:
            try:
                raise PermissionError("Permission does not exist")
            except:
                print(PermissionError("Permission does not exist"))
        else:
            if username not in perm_set:
                try:
                    raise NotPermittedError(username)
                except:
                    print(PermissionError("Permission does not exist"))
            else:
                return True

if __name__ == "__main__":
    authenticator = Authenticator()
    authorizor = Authorizor(authenticator)
    authenticator.add_user("joe", "joepassword")
    authenticator.login("joe", "joepassword")
    authorizor.add_permission("sing")
    authorizor.permit_user("sing","joe")
    print(authorizor.check_permission("sing","joe"))

