import json
import bcrypt
import console_handler as ch


class Username:
    username = None


with open("users.json") as user_info:
    user_data = json.load(user_info)

with open("permission.json") as permission_info:
    permission_data = json.load(permission_info)


def register(username, password, confirm):
    ch.clear_console()
    if username == "":
        ch.print_invalid_login()
        return False
    elif username in user_data:
        ch.print_user_exists()
        return False
    elif password != confirm:
        ch.print_password_dont_match()
        return False

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    user_data[username] = hashed.decode('utf-8')
    with open("users.json", "w") as f:
        json.dump(user_data, f, indent=4)

    ch.print_registration_success()
    return True


def login(username, password):
    ch.clear_console()
    if username not in user_data:
        ch.print_user_not_found()
        return False

    stored_hash = user_data[username].encode('utf-8')
    if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        ch.print_login_welcome(username)
        return True
    else:
        ch.print_invalid_credentials()
        return False


def authorization():
    if Username.username is None:
        ch.clear_console()
        ch.print_authorization_failed()
        ch.print_newline()
        return False
    return True


def check_delete_market_permission():
    if Username.username in permission_data:
        if permission_data[Username.username] != "delete":
            ch.clear_console()
            ch.print_permission_failed()
            ch.print_newline()
            return False
    else:
        ch.clear_console()
        ch.print_permission_failed()
        ch.print_newline()
        return False
    return True
