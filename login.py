import hashlib

def signup():
    email = input("Enter email address: ")
    pwd = input("Enter password: ")
    conf_pwd = input("Confirm password: ")
    char_name = input("Character name: ")
    if conf_pwd == pwd:
        enc = conf_pwd.encode()
        hash1 = hashlib.md5(enc).hexdigest()
        with open("credentials.txt", "a") as f:
            f.write(email + ":")
            f.write(char_name + ":")
            f.write(hash1 + "\n")
            f.close()
            print("You have registered successfully!")
    else:
        print("Password is not same as above! \n")



def login():
    email = input("Enter email: ")
    pwd = input("Enter password: ")
    auth = pwd.encode()
    auth_hash = hashlib.md5(auth).hexdigest()
    user_ok = False
    with open("credentials.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            stored_email, char_name, stored_pwd = line.split(":")
            if email == stored_email:
                user_ok = True
                stored_pwd = stored_pwd.replace("\n", "")
                break
        f.close()
        if user_ok and auth_hash == stored_pwd:
            print("{} logged in Successfully!".format(char_name))
        else:
            print("Login failed! \n")


print("********** Login System **********")
print("1.Signup")
print("2.Login")
print("3.Exit")
ch = int(input("Enter your choice: "))
if ch == 1:
    signup()
elif ch == 2:
    login()
elif ch == 3:
   print("A")
else:
    print("Wrong Choice!")
