import re 

regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'


def check_mail(email):
    return re.search(regex, email) != None

def check_name(uname):
    if len(uname) < 32:
        return re.search("^[A-Za-z0-9_-]*$",uname) != None
    return False

