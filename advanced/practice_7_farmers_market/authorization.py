import json
import bcrypt
import console_handler as ch


class Username:
    username = ""


with open("users.json") as user_info:
    data = json.load(user_info)

authorization_dict = {}


def register(username, password, confirm):
    ch.clear_console()
    if password != confirm:
        ch.print_password_dont_match()
        return False
    if username in data:
        ch.print_user_exists()
        return False

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    data[username] = hashed.decode('utf-8')
    with open("users.json", "w") as f:
        json.dump(data, f, indent=4)

    authorization_dict[username] = "True"
    ch.print_registration_success()
    return True


def login(username, password):
    ch.clear_console()
    if username not in data:
        ch.print_user_not_found()
        return False

    stored_hash = data[username].encode('utf-8')
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        ch.print_login_welcome(username)
        authorization_dict[username] = "True"
        return True
    else:
        ch.print_invalid_credentials()
        return False


def authorization():
    if Username.username == "":
        ch.clear_console()
        ch.print_authorization_failed()
        ch.print_newline()
        return False
    return True
