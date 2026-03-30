def len_filter(password:str , min_len=8, max_len=20):
    if min_len <= len(password) <= max_len:
        return True
    return False


def non_ascii_filter(password:str):
    try:
        password.encode('ascii')
    except UnicodeEncodeError:
        return False
    return True


def char_map(password:str):
    map="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+|;:',.<>/?`~"
    for char in password:
        if char not in map:
            return False
    return True

def clean(password:str , batch=1000, batch_flag=False):
    if batch_flag == False:
        if len_filter(password) and non_ascii_filter(password) and char_map(password):
            return password
        else:
            return None
    
    else:
        cleaned_passwords = []
        for pwd in password:
            if len_filter(pwd) and non_ascii_filter(pwd) and char_map(pwd):
                cleaned_passwords.append(pwd)
        return cleaned_passwords