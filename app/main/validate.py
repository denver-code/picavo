import re 

regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'


def check_mail(email):
    return re.search(regex, email) != None

def check_name(uname):
    if len(uname) < 32:
        return re.search(" ^[A-Za-z0-9_-]*$",uname) != None
    return False

def check_auth_data(user_obj):
    if user_obj:
        if check_mail(user_obj["email"]):
            if check_name(user_obj["username"]):
                if user_obj["password"] == user_obj["repass"]:
                    if len(user_obj["password"]) > 8:
                        return True
                    else:
                        return "Len password must be > 8"
                else:
                    return "Password don\'t match"
            else:
                return "Invalid username"
        else:
            return "Invalid email"
    else:
        return False