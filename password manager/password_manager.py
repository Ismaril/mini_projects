import sys

from cryptography.fernet import Fernet

KEY = b'wv0Qaap6H4yAZ6A8ohjxI1FtIIOV9FO7fJDQ_sUzpIU='


# TODO: FERNET key should not be within codebase
# TODO: password should not be possible to return back as plain string, when you want to check passwords, compare hashes = passwords should never be visible


class PasswordManager:

    def __init__(self):
        self.f = Fernet(KEY)

    def encrypt(self, x):
        """This function serves as encryption of inputted text"""
        return self.f.encrypt(bytes(x.encode())).decode()

    def decrypt_master_password(self, x):
        with open("encrypted.txt", "r") as f_read:
            read = f_read.readline().encode()
        return self.f.decrypt(bytes(read)).decode()

    def decrypt_whole_text(self):
        with open("encrypted.txt", "r") as f_read:
            read = f_read.readlines()
            decrypted = []
            for encryption in read:
                encoded = encryption.encode()
                decoded = self.f.decrypt(bytes(encoded)).decode()
                decrypted.append(str(decoded))
        return "\n".join(decrypted)

    @staticmethod
    def check_master_password():
        """Take input from user, compare it later with 'True master password' """
        return input("Enter your master password: ").strip()

    @staticmethod
    def incorrect_password(password_true, password_actual, nr_of_attempts):
        """Display message based on number of incorrect password attempts"""
        if password_true != password_actual:
            print(f"Incorrect master password, you got {2 - nr_of_attempts}/3 attempts left")
            return 1

    @staticmethod
    def out_of_password_attempts(nr_of_attempts):
        """Give a user 3 attempts to get inside"""
        if nr_of_attempts == 3:
            print("You entered incorrect password 3x\n"
                  "***Quitting***")
            sys.exit()

    def set_master_password(self):
        """Set new master password if opening the file for the first time"""
        with open("encrypted.txt", "r") as f_read:
            read_line = f_read.readline()
        if not read_line:
            master_password = input("Create your new master password: ").strip()
            with open("encrypted.txt", "w") as f_write:
                f_write.write(self.encrypt(master_password))
                print("Your new master password was set\n")

    @staticmethod
    def text_formatting():
        """Format in [Page: XXX, Login: YYY, Password: ZZZ]"""
        result = str()
        result += f"[Page: {input('Enter a name of page/program: ')}, "
        result += f"Login: {input('Enter a login: ')}, "
        result += f"Password: {input('Enter a password: ')}]"
        return result

    def read_passwords(self):
        """Read all passwords"""
        print("***Read passwords***")
        nr_of_attempts = 0
        while nr_of_attempts < 3:
            master_password = self.check_master_password()
            with open("encrypted.txt", "r") as f_read:
                f_read.read()

            if master_password == self.decrypt_master_password(master_password):
                print(self.decrypt_whole_text())
                break
            nr_of_attempts += self.incorrect_password(self.decrypt_master_password,
                                                      master_password,
                                                      nr_of_attempts)
        self.out_of_password_attempts(nr_of_attempts=nr_of_attempts)

    def write_password(self):
        """Write new entries"""
        print("***Write passwords***")
        nr_of_attempts = 0
        while nr_of_attempts < 3:
            master_password = self.check_master_password()
            if master_password == self.decrypt_master_password(master_password):
                new_data = self.text_formatting()
                with open("encrypted.txt", "a") as f_append:
                    f_append.write(f"\n{self.encrypt(new_data)}")
                print("New data successfully added to the database\n")
                break

            nr_of_attempts += self.incorrect_password(self.decrypt_master_password,
                                                      master_password,
                                                      nr_of_attempts)
        self.out_of_password_attempts(nr_of_attempts=nr_of_attempts)

    def delete_password(self):
        """Delete entries based on specified keyword"""
        print("***Delete passwords***")
        nr_of_attempts = 0

        while nr_of_attempts < 3:
            master_password = self.check_master_password()

            if master_password == self.decrypt_master_password(master_password):
                list_of_entries = self.decrypt_whole_text().split("\n")
                print(self.decrypt_whole_text())
                entry_tobe_deleted = input("Write a name of website/program and delete whole row with it: ")

                with open("encrypted.txt", "w") as f_delete:
                    for i, item in enumerate(list_of_entries):
                        if entry_tobe_deleted in item:
                            print("Found at index:", i)
                            break
                    del list_of_entries[i]
                    del list_of_entries[0]
                    to_string = "\n".join(list_of_entries)
                    f_delete.write(f"{self.encrypt(master_password)}'\n'{self.encrypt(to_string)}")
                print("Data successfully deleted\n")
                break

            nr_of_attempts += self.incorrect_password(self.decrypt_master_password,
                                                      master_password,
                                                      nr_of_attempts)
        self.out_of_password_attempts(nr_of_attempts=nr_of_attempts)

    @staticmethod
    def show_encryption():
        """Read data in encrypted form from source text file"""
        print("***Displaying encryption***")
        with open("encrypted.txt", "r") as f_read:
            print(f_read.read())

    @staticmethod
    def home_screen():
        """Display options that allow you to operate with program"""
        return input("[Passwords] "
                     "Read (r), "
                     "Write (w), "
                     "Delete (d), "
                     "Encr (e), "
                     "Quit (q): "
                     ).lower()

    def main(self):
        while True:
            print("-" * 60)
            home = self.home_screen()
            self.set_master_password()

            if home == "r":
                self.read_passwords()
            elif home == "w":
                self.write_password()
            elif home == "d":
                self.delete_password()
            elif home == "e":
                self.show_encryption()
            elif home == "q":
                print("***Quitting***")
                sys.exit()


if __name__ == '__main__':
    pm = PasswordManager()
    pm.main()

# p*i*c*a
