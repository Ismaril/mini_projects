import sys
import random
import hashlib
import cryptography
from cryptography.fernet import Fernet

DATABASE = "encrypted.txt"
SETTINGS = "settings.txt"
CRYPTOGRAPHER: Fernet | None = None


class Constants:
    """
    This class contains constants used in the program. These constants could not be otherwise used
        in "match cases" syntax.
    """

    WRITE_MODE = "w"
    READ_MODE = "r"
    DELETE_MODE = "d"
    SHOW_ENCRYPTION = "e"
    GENERATE_PASSWORDS = "g"
    QUIT = "q"


def convert_to_hash(raw_text: str):
    """
    This function serves as encryption of inputted text.

    param: raw_text: String to be encrypted.

    :returns: string
    """
    # Create a hash object (e.g., SHA-256)
    hash_obj_ = hashlib.sha256()

    # Update the hash object with the data
    hash_obj_.update(raw_text.encode())  # You need to encode the data to bytes

    # Get the hexadecimal representation of the hash
    hash_string_ = hash_obj_.hexdigest()

    return hash_string_


def generate_fernet_key():
    """
    Generate key for Fernet.

    :returns: None
    """

    print("This is your Fernet Key, save it somewhere safe.")
    key = str(Fernet.generate_key())
    print(key[2:-1], end="\n\n")
    operations_separator()


def encrypt(raw_text: str):
    """
    This function serves as encryption of inputted text.

    :param raw_text: String to be encrypted by Fernet.

    :returns: str
    """

    result = CRYPTOGRAPHER.encrypt(bytes(raw_text.encode())).decode()
    return result


def take_master_password():
    """
    Take input from user, compare it later with 'True master password'.

    :returns: str
    """

    result = input("Enter your master password: ").strip()
    hash_result = convert_to_hash(result)
    return hash_result


def decrypt_master_password_from_database():
    """
    This function decrypts master password and returns hash.

    :returns: str
    """
    try:
        with open(DATABASE, Constants.READ_MODE) as f_read:
            read = f_read.readline().encode()
        return CRYPTOGRAPHER.decrypt(bytes(read)).decode()
    except cryptography.fernet.InvalidToken:
        print("You entered wrong key, exiting application.")
        input("Press any key to exit...")
        sys.exit()


def decrypt_whole_text():
    """
    Decrypt whole database text.

    :returns: str
    """
    with open(DATABASE, Constants.READ_MODE) as f_read:
        read = f_read.readlines()
        decrypted = []
        for encryption in read:
            encoded = encryption.encode()
            decoded = CRYPTOGRAPHER.decrypt(bytes(encoded)).decode()
            decrypted.append(str(decoded))
    return "\n".join(decrypted)


def out_of_password_attempts(nr_of_attempts, limit_of_attempts):
    """
    Give a user 3 attempts to get inside.

    :returns: None
    """
    if nr_of_attempts == limit_of_attempts:
        print("You entered incorrect password 3x\n"
              "***Quitting***")
        input("Press any key to exit...")
        sys.exit()


def does_master_password_exist():
    """
    Check if master password exists in the database.

    :returns: bool
    """
    with open(DATABASE, Constants.READ_MODE) as f_read:
        read_line = f_read.readline()
    if read_line:
        return True
    return False


def set_master_password():
    """
    Set new master password if opening the file for the first time.

    :returns: str
    """

    print("Create your new master password.")
    with open(DATABASE, Constants.WRITE_MODE) as f_write:
        master_password = encrypt(take_master_password())
        f_write.write(master_password)
        print("Your new master password was set.\n")
        return master_password


def text_formatting():
    """
    Format string in [Page: XXX, Login: YYY, Password: ZZZ]

    :returns: str
    """
    result = str()
    result += f"[Page: {input('Enter a name of page/program: ')}, "
    result += f"Login: {input('Enter a login: ')}, "
    result += f"Password: {input('Enter a password: ')}]"
    return result


def operate_passwords(mode: str, master_password_user: str | None = None):
    """
    Read all passwords from database.

    :param mode: Mode of operation
    :param master_password_user: Master password entered by user

    :returns: None
    """

    if mode == Constants.READ_MODE:
        print("***Read passwords***")
        print(decrypt_whole_text())
        return
    elif mode == Constants.WRITE_MODE:
        print("***Write passwords***")
        new_data = text_formatting()
        with open(DATABASE, "a") as f_append:
            f_append.write(f"\n{encrypt(new_data)}")
        print("New data successfully added to the database\n")
        return
    elif mode == Constants.DELETE_MODE:
        print("***Delete passwords***")
        list_of_entries = decrypt_whole_text().split("\n")
        print(decrypt_whole_text())
        entry_tobe_deleted = input(
            "Write a name of website/program and delete whole row with it: ")

        with open(DATABASE, Constants.WRITE_MODE) as f_delete:
            for i, item in enumerate(list_of_entries):
                if entry_tobe_deleted in item:
                    print("Found at index:", i)
                    del list_of_entries[i]
                    break
            passwords = "\n".join(list_of_entries[1:])
            f_delete.write(f"{encrypt(master_password_user)}'\n'{encrypt(passwords)}")
            print("Data successfully deleted\n")
        return


def show_encryption():
    """
    Read data in encrypted form from source text file.

    :returns: None
    """
    print("***Displaying encryption***")
    with open(DATABASE, Constants.READ_MODE) as f_read:
        print(f_read.read())


def home_screen():
    """Display options that allow you to operate with program"""
    return input("[Passwords] "
                 "Read (r), "
                 "Write (w), "
                 "Delete (d), "
                 "Encryption (e), "
                 "Generate (g), "
                 "Quit (q): "
                 ).lower()


def is_fernet_key_set():
    """
    Check if Fernet key is set.

    :returns: bool
    """
    with open(SETTINGS, Constants.READ_MODE) as f_read:
        read = f_read.readline()
    if read:
        return True
    return False


def write_down_that_fernet_key_is_set():
    """
    Write down that Fernet key is set.

    :returns: None
    """
    with open(SETTINGS, Constants.WRITE_MODE) as f_write:
        f_write.write("Key set: True")


def user_enters_fernet_key():
    """
    Insert Fernet key.

    :returns: None
    """
    try:
        print("Insert Ferent key to decrypt database")
        global CRYPTOGRAPHER
        key = input("Enter your key: ")
        CRYPTOGRAPHER = Fernet(key.encode())
    except ValueError:
        print("Wrong format of a key.")
        input("Press any key to exit.")
        sys.exit()


def check_if_master_password_is_correct():
    """
    Check if master password is correct.

    :returns: str
    """

    nr_of_attempts: int = 0
    limit_of_attempts: int = 3

    while nr_of_attempts < limit_of_attempts:
        master_password_user = take_master_password()
        if master_password_user == decrypt_master_password_from_database():
            return master_password_user
        nr_of_attempts += 1
        print(f"Incorrect master password, "
              f"you got {limit_of_attempts - nr_of_attempts}/3 attempts left")
        out_of_password_attempts(nr_of_attempts=nr_of_attempts, limit_of_attempts=limit_of_attempts)


def password_operations_loop(master_password_user: str):
    """
    Loop which allows you to operate with passwords

    :param master_password_user: Master password entered by user

    :returns: None
    """

    while True:
        operations_separator()
        home = home_screen()
        match home:
            case Constants.READ_MODE:
                operate_passwords(mode=Constants.READ_MODE)
            case Constants.WRITE_MODE:
                operate_passwords(mode=Constants.WRITE_MODE)
            case Constants.DELETE_MODE:
                operate_passwords(mode=Constants.DELETE_MODE, master_password_user=master_password_user)
            case Constants.SHOW_ENCRYPTION:
                show_encryption()
            case Constants.GENERATE_PASSWORDS:
                nr_of_passwords = int(input("Enter a number of passwords to generate: "))
                len_of_passwords = int(input("Enter a length of passwords to generate: "))
                password_generator(nr_of_passwords, len_of_passwords)
            case Constants.QUIT:
                print("***Quitting***")
                sys.exit()


def operations_separator():
    """
    Separator of operations

    :returns: None
    """
    print("-" * 60)


def password_generator(nr_of_passwords, len_of_passwords):
    """Generate passwords out of all characters of basic ascii table"""
    for _ in range(nr_of_passwords):
        print("".join([chr(random.randint(33, 127)) for _ in range(len_of_passwords)]))


def main():
    """
    Main function which loops and checks user input

    :returns: None
    """
    master_password_is_set: bool = does_master_password_exist()
    master_password_is_entered: bool = False
    ferent_key_is_set: bool = is_fernet_key_set()
    fernet_key_is_entered: bool = False
    master_password_user: str = ""

    if not ferent_key_is_set:
        generate_fernet_key()
        write_down_that_fernet_key_is_set()

    if not fernet_key_is_entered:
        user_enters_fernet_key()
        fernet_key_is_entered += True

    if not master_password_is_set:
        master_password_user += set_master_password()
        master_password_is_set += True
        master_password_is_entered += True

    if not master_password_is_entered:
        master_password_user = check_if_master_password_is_correct()

    password_operations_loop(master_password_user=master_password_user)
