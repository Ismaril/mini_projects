import sys
import random
import hashlib
import cryptography
from cryptography.fernet import Fernet

LIMIT_OF_ATTEMPTS = 3

DATABASE = "encrypted.txt"
SETTINGS = "settings.txt"
CRYPTOGRAPHER: Fernet | None = None

READ_PASSWORDS_MSG = "***Read passwords***"
WRITE_PASSWORDS_MSG = "***Write passwords***"
DELETE_PASSWORDS_MSG = "***Delete passwords***"
DISPLAY_ENCRYPTION_MSG = "***Displaying encryption***"
QUITTING_MSG = "***Quitting***"

OPERATIONS_SCREEN = "[Passwords] " \
                    "Read (r), " \
                    "Write (w), " \
                    "Delete (d), " \
                    "Encryption (e), " \
                    "Generate (g), " \
                    "Quit (q): "

SAVE_FERNET_KEY_MSG = "This is your Fernet Key, save it somewhere safe."
ENTER_MASTER_PASSWORD_MSG = "Enter your master password: "
PRESS_ANY_KEY_MSG = "Press Enter to exit..."
WRONG_FERNET_KEY_MSG = "You entered wrong key, exiting application."
INCORRECT_MASTER_PASSWORD_LIMIT_MSG = "You entered incorrect password 3x"
DATA_ADDED_TO_DATABASE_MSG = "New data successfully added to the database\n"
SPECIFY_WHAT_TO_DELETE_MSG = "Write a name of website/program and delete whole row with it: "
DATA_DELETED_FROM_DATABASE_MSG = "Data successfully deleted\n"
INSERT_FERNET_KEY_MSG = "Insert key to decrypt database"
ENTER_FERNET_KEY_MSG = "Enter your key: "
WRONG_FORMAT_OF_FERNET_KEY_MSG = "You entered wrong format of a key."
INCORRECT_MASTER_PASSWORD_MSG = "Incorrect master password, you got"  # Only fraction of the message
ATTEMPTS_LEFT_MSG = "attempts left."  # Only fraction of the message

FERNET_KEY_SET = "Key set: True"


class Constants:
    """
    This class contains constants used in the program. These constants could not be otherwise used
        in "match cases" syntax if they were global and not part of the object like here.
    """

    WRITE_MODE = "w"
    READ_MODE = "r"
    DELETE_MODE = "d"
    SHOW_ENCRYPTION = "e"
    GENERATE_PASSWORDS = "g"
    QUIT = "q"
    NUMBER_OF_PASSWORDS_TO_GENERATE_MSG = "Enter a number of passwords to generate: "
    LENGTH_OF_PASSWORDS_TO_GENERATE_MSG = "Enter a length of passwords to generate: "
    WRONG_FORMAT_DIGIT_EXPECTED_MSG = "Wrong format, digit expected."


def convert_to_hash(raw_text: str):
    """
    This function serves as encryption of inputted text with deterministic results.

    param: raw_text: String to be encrypted.

    :returns: str
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

    print(SAVE_FERNET_KEY_MSG)
    key = str(Fernet.generate_key())
    print(key[2:-1], end="\n\n")
    operations_separator()


def encrypt(raw_text: str):
    """
    This function serves as encryption of inputted text.
    Decryption is possible only with the same key.

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

    result = input(ENTER_MASTER_PASSWORD_MSG).strip()
    hash_result = convert_to_hash(result)
    return hash_result


def exit_application(custom_message: str = None):
    """
    Exit application.

    :returns: None
    """
    print(custom_message)
    input(PRESS_ANY_KEY_MSG)
    sys.exit()


def decrypt_master_password_from_database():
    """
    This function decrypts with Fernet master password and returns hash.

    :returns: str
    """
    try:
        with open(DATABASE, Constants.READ_MODE) as f_read:
            read = f_read.readline().encode()
        return CRYPTOGRAPHER.decrypt(bytes(read)).decode()
    except cryptography.fernet.InvalidToken:
        exit_application(WRONG_FERNET_KEY_MSG)


def decrypt_whole_text():
    """
    Decrypt whole database text with Fernet and return readable text.

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


def out_of_password_attempts(nr_of_attempts):
    """
    Give a user 3 attempts to get inside.

    :returns: None
    """
    if nr_of_attempts == LIMIT_OF_ATTEMPTS:
        exit_application(INCORRECT_MASTER_PASSWORD_LIMIT_MSG)


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
    Set new master password.

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
        print(READ_PASSWORDS_MSG)
        print(decrypt_whole_text())
        return
    elif mode == Constants.WRITE_MODE:
        print(WRITE_PASSWORDS_MSG)
        new_data = text_formatting()
        with open(DATABASE, "a") as f_append:
            f_append.write(f"\n{encrypt(new_data)}")
        print(DATA_ADDED_TO_DATABASE_MSG)
        return
    elif mode == Constants.DELETE_MODE:
        print(DELETE_PASSWORDS_MSG)
        list_of_entries = decrypt_whole_text().split("\n")
        print(decrypt_whole_text())
        entry_tobe_deleted = input(SPECIFY_WHAT_TO_DELETE_MSG)

        with open(DATABASE, Constants.WRITE_MODE) as f_delete:
            for i, item in enumerate(list_of_entries):
                if entry_tobe_deleted in item:
                    print("Found at index:", i)
                    del list_of_entries[i]
                    break
            passwords = "\n".join(list_of_entries[1:])
            f_delete.write(f"{encrypt(master_password_user)}'\n'{encrypt(passwords)}")
            print(DATA_DELETED_FROM_DATABASE_MSG)
        return


def show_encryption():
    """
    Read data in encrypted form from source text file.

    :returns: None
    """
    print(DISPLAY_ENCRYPTION_MSG)
    with open(DATABASE, Constants.READ_MODE) as f_read:
        print(f_read.read())


def home_screen():
    """Display options that allow you to operate with program"""
    return input(OPERATIONS_SCREEN).lower()


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
    Write down to settings file that Fernet key is set.

    :returns: None
    """
    with open(SETTINGS, Constants.WRITE_MODE) as f_write:
        f_write.write(FERNET_KEY_SET)


def let_user_enter_fernet_key():
    """
    Insert Fernet key.

    :returns: None
    """
    try:
        print(INSERT_FERNET_KEY_MSG)
        global CRYPTOGRAPHER
        key = input(ENTER_FERNET_KEY_MSG)
        CRYPTOGRAPHER = Fernet(key.encode())
    except ValueError:
        exit_application(WRONG_FORMAT_OF_FERNET_KEY_MSG)


def check_if_master_password_is_correct():
    """
    Check if master password is correct.

    :returns: str
    """

    nr_of_attempts: int = 0

    while nr_of_attempts < LIMIT_OF_ATTEMPTS:
        master_password_user = take_master_password()
        if master_password_user == decrypt_master_password_from_database():
            return master_password_user
        else:
            nr_of_attempts += 1
            print(INCORRECT_MASTER_PASSWORD_MSG + " "
                  + f"{LIMIT_OF_ATTEMPTS - nr_of_attempts}/{LIMIT_OF_ATTEMPTS}" + " "
                  + ATTEMPTS_LEFT_MSG)
            out_of_password_attempts(nr_of_attempts=nr_of_attempts)


def password_operations_loop(master_password_user: str):
    """
    Loop which allows you to operate with passwords.

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
                operate_passwords(mode=Constants.DELETE_MODE,
                                  master_password_user=master_password_user)
            case Constants.SHOW_ENCRYPTION:
                show_encryption()
            case Constants.GENERATE_PASSWORDS:
                try:
                    nr_of_passwords = int(input(Constants.NUMBER_OF_PASSWORDS_TO_GENERATE_MSG))
                    len_of_passwords = int(input(Constants.LENGTH_OF_PASSWORDS_TO_GENERATE_MSG))
                    password_generator(nr_of_passwords, len_of_passwords)
                except ValueError:
                    print(Constants.WRONG_FORMAT_DIGIT_EXPECTED_MSG)
            case Constants.QUIT:
                print(QUITTING_MSG)
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
        let_user_enter_fernet_key()
        fernet_key_is_entered += True

    if not master_password_is_set:
        master_password_user += set_master_password()
        master_password_is_set += True
        master_password_is_entered += True

    if not master_password_is_entered:
        master_password_user = check_if_master_password_is_correct()

    password_operations_loop(master_password_user=master_password_user)
