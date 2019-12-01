import sys
import sqlite3
import string
import datetime


class YellowBook:
    __database = None
    __cursor = None
    __conn = None
    __db_name = "PhoneBook"

    def __exit_continue(self, *args):
        if input("{} y/n".format(args)).lower() == 'y':
            self.menu_view()
        else:
            print("Thanks for choosing us!")
            sys.exit(0)

    def __validate_menu_input(self, user_input):
        if str(user_input).isnumeric():
            user_input = int(user_input)
            if 0 < user_input < 7:
                return True
            else:
                return False

    def __validate_name_surname(self, space, data):
        """
            Creates a list composed of elements which are not included into the 'restrictions' list.
            Next, compares  current list and user-entered string lengths.
            If they match each other, so the user-input is correct.

        """
        user_input_list = [x for x in space if x not in string.punctuation]

        if len(user_input_list) == len(space) and (len(space) != 0):
            space = space.capitalize()
            data.append(space.strip())
            return
        else:
            print("Your input was incorrect! This field should consist of letters and digits:\n")
            self.__validate_name_surname(input(), data)

    def __init__(self, db_file):
        self.__database = db_file
        # Creating connection with stored data base
        self.__conn = sqlite3.connect("mydatabase.db")
        # Cursor is a special object stores the result of SELECT command.
        self.__cursor = self.__conn.cursor()
        self.__initate_db()

    def __initate_db(self):

        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS PhoneBook 
        (name text, surname text, phone text, birth_date text, age text, city text, country text)""")

    def add_record(self):
        print("Now lets add new person")
        data = []  # LIST stores all INSERT information

        surname = input("First name: ")
        self.__validate_name_surname(surname, data)

        name = input("Second name: ")
        self.__validate_name_surname(name, data)

        age = input("Age: ")

        while (not age.isdigit()) or (not 0 <= int(age) < 150):
            age = input(
                "\nThis age is incorrect! Please make sure that "
                "\nyour input consists of digits only and the age is correct! "
                "\n( 12 - correct, '-1' - incorrect, 151 - incorrect) ")
        data.append(age)

        # Birth date column
        _ = input("Will you fill the birth date? If 'yes' press 'y'. If no press another.")
        if _ == 'y':
            while True:
                try:
                    date_text = datetime.date(int(input("Birth date Year:")), int(input("Birth date Month:")),
                                              int(input("Birth date Day:")))
                    datetime.datetime.strptime(str(date_text), '%Y-%m-%d')
                    data.append(date_text)
                    print("Successfully")
                    break
                except BaseException:
                    print("Incorrect data format, should be YYYY-MM-DD")
        else:
            data.append('-')

        phone = input("Phone number  without '8' : ")
        while (len(phone) != 10) or (phone.isdigit() is not True) or (phone[0] == 8):
            phone = input("Try again! Input phone number  without '8' : ")
        data.append('8' + phone)

        city = input("City: ")

        while not city.isalnum():
            city = input("City name can't include another symbols besides letters and digits! : ")
        data.append(city.lower().capitalize())

        country = input("Country: ")

        while not country.isalnum():
            country = input("Country name can't include another symbols besides letters and digits! : ")
        data.append(country.lower().capitalize())

        self.__cursor.execute('SELECT EXISTS (SELECT [name],[surname]'
                              ' FROM {0} '
                              ' WHERE [name] = "{1}" and [surname] = "{2}")'.format(self.__db_name, data[0], data[2]))

        flag = self.__cursor.fetchone()  # fetchone returns a tuple with one element

        if flag[0] != 1:
            try:
                self.__cursor.execute("INSERT"
                                      " INTO {0} "
                                      "VALUES (?,?,?,?,?,?,?)".format(self.__db_name), data)

            except Exception as f:
                print("Sorry currently service is unavailable")
                print(f)

        else:
            print(
                " \nThe Yellowbook does not support 2 or more records with similar [First name] and {Second name] fields."
                " \nFill in another Surname.\n ")
            self.__exit_continue("Menu?")

        self.__conn.commit()  # Saves changes in data base

    def menu_view(self):
        while True:
            user_input = input("======================================================\n"
                               "Yellow book is ready for use. Please choose and option."
                               "\n\t[1] Add new record"
                               "\n\t[2] Edit record by phone number"
                               "\n\t[3] Delete record"
                               "\n\t[4] View all stored records"
                               "\n\t[5] Search record (by name, phone, address)"
                               "\n\t[6] To exit]"
                               "\n======================================================\n")

            if self.__validate_menu_input(user_input):
                break
            else:
                print("Please choose valid option")
        if user_input == "1":
            self.add_record()
        elif user_input == "2":
            pass
        elif user_input == "3":
            pass
        elif user_input == "4":
            pass
        elif user_input == "5":
            pass
        elif user_input == "6":
            print("Exit process initiated")
            print("By by")
            sys.exit(0)


yb = YellowBook("data_base.txt")
yb.menu_view()
