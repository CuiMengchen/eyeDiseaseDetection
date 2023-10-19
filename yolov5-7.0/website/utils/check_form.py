def is_null(username, password, age):
    if username == "" or password == "" or age == "":
        return True
    else:
        return False


def check_session(session):
    if "username" in session.keys():
        user_info = {
            "name": session["username"],
            "age": session["age"]
        }
        return user_info
    else:
        return None
