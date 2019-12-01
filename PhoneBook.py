import sys
import sqlite3
import string
import datetime


class PhoneBook:
    __cursor = None
    __conn = None
    __db_name = "PhoneBook"
    __command_line = {'1': "name", '2': "surname",
                      '3': "Age", '4': "[Birth date]", '5': "City",
                      '6': "Country", '7': "Phone"}

    def __init__(self):
        # Creating connection with stored data base
        self.__conn = sqlite3.connect("mydatabase.db")
        # Cursor is a special object stores the result of SELECT command.
        self.__cursor = self.__conn.cursor()
        self.__initate_db()

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

    def __initate_db(self):
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS {0}
        (name text, surname text, phone text, birth_date text, age text, city text, country text)"""
                              .format(self.__db_name))

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
                self.__conn.commit()  # Saves changes in data base

            except Exception as f:
                print("Sorry currently service is unavailable")
                print(f)

        else:
            print(
                " \nThe Yellowbook does not support 2 or more records with similar [First name] and {Second name] fields."
                " \nFill in another Surname.\n ")
            self.__exit_continue("Menu?")

        self.__exit_continue("Menu?")

    def view_all_records(self):
        commands = ["1", "2", "3", "4", "5", "6", "7"]
        while True:
            request = input(
                "\nPlease choose the needed category and enter the value."
                "\n________________________________ "
                "\n1 - Search by First name"
                "\n2 - Search by Last name"
                "\n3 - Search by Age"
                "\n4 - Search by Birth date "
                "\n5 - Search by City"
                "\n6 - Search by Country"
                "\n7 - Search by Phone number"
                "\n8 - Print all contacts"
                "\n9 - Search by Name and Surname"
                "\n0 - Step back\n")

            if request in commands:
                user_input = input("Enter {} in correct format. "
                                   "\nFor phone: start with '8' "
                                   "\nFor BIRTH DATE: you are to use the next data representation"
                                   " <yyyy-mm-dd>\n "
                                   .format(self.__command_line.get(request))).capitalize().strip()
                self.__cursor.execute("SELECT * FROM {0} WHERE {1} = \"{2}\" ".
                                      format(self.__db_name,
                                             self.__command_line.get(request),
                                             user_input.strip()))
                break

            elif request == '0':
                self.__exit_continue("Go to the menu?\n")
                break

            elif request == '8':
                self.__cursor.execute("SELECT * FROM {} ".format(self.__db_name))
                break

            elif request == '9':
                user_input_surname = input(
                    "Enter {} ".format(self.__command_line.get("1"))).strip().lower().capitalize()
                user_input_name = input("Enter {} ".format(self.__command_line.get("3"))).strip().lower().capitalize()
                print(user_input_surname, user_input_name)
                self.__cursor.execute("SELECT * FROM {0} WHERE {1} = \"{2}\" AND {3} = \"{4}\""
                                      .format(self.__db_name, "name", user_input_surname,
                                              "surname", user_input_name))
                break
            else:
                print("___________________________\nCommand is incorrect! Check if  the commands number is right.\n ")

        # Receives the result of the SQL request
        result = self.__cursor.fetchall()

        """
         >> VERIFIES IF RESULT EXISTS IN CURRENT TABLE.
        """

        if len(result) == 0:
            user_input = input("This record does not exist yet.\n "
                               "Would you like to create a new record (1) or find another(2)."
                               "\nEnter 1 or 2 or any to exit.\r")
            if user_input == '1':
                self.add_record()
            elif user_input == '2':
                self.view_all_records()
            else:
                self.menu_view()

        for i in result:
            print(i)
        self.__exit_continue("Return to the main menu?")

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
            self.view_all_records()

        elif user_input == "6":
            print("Exit process initiated")
            print("By by")
            sys.exit(0)

    def delete_record(self):
        commands = ["1", "2", "3"]
        request = input(
            "\nPlease choose the needed category and enter the value."
            "\n________________________________ "
            "\n1 - Delete by Phone number"
            "\n2 - Delete all contacts"
            "\n3 - Delete by First name and Last name"
            "\n0 - Step back")

        if request in commands:
            user_input = input("Enter {} ".format(self.__command_line.get(request))).strip().capitalize()
            print(user_input)

            self.__cursor.execute("Select *"
                                  " FROM Yellowbook "
                                  "WHERE {0} = \"{1}\"".
                                  format(self.__command_line.get(request), user_input))
            if len(self.__cursor.fetchall()) > 0:

                self.__cursor.execute("DELETE FROM Yellowbook WHERE {0} = \"{1}\" ".
                                      format(self.__command_line.get(request), user_input))
                print("Successfully deleted")
            else:
                print("Such record(s) does not exist.")
                self.delete_record()

        elif request == '0':
            self.__exit_continue("Go to the menu?")

        elif request == '9':
            self.__cursor.execute("DELETE "
                                  "FROM Yellowbook ")
            print("Successfully deleted")

        elif request == '10':
            user_input_surname = input("Enter {} ".format(self.__command_line.get("1"))).strip().capitalize()
            user_input_name = input("Enter {} ".format(self.__command_line.get("3"))).strip().capitalize()
            print(user_input_surname, user_input_name)
            self.__cursor.execute("DELETE "
                                  "FROM Yellowbook"
                                  " WHERE {0} = \"{1}\" AND {2} = \"{3}\""
                                  .format(self.__command_line.get("1"), user_input_surname,
                                          self.__command_line.get("3"), user_input_name))
        else:
            print("___________________________\nCommand is incorrect! Check if  the commands number is right. ")

        self.__conn.commit()

        self.menu_view()


yb = PhoneBook()
yb.menu_view()
