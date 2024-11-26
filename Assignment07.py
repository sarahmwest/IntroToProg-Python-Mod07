# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   S.West,24Nov24,Added classes and inheritance
# ------------------------------------------------------------------------------------------ #
import json

# ---------------------------------------DATA---------------------------------------#
# Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Global Variables
students: list = []  # A table of student data.
menu_choice: str  # Hold the choice made by the user.


class Person:  # This class is a generic blueprint for instances of objects created using the Person class.
    """
      A class representing a person's data.

      Properties:
      - first_name: str = the student's first name
      - last_name: str = the student's last name
      ChangeLog:
      S.West, 24Nov24, Created the class.
      """

    def __init__(self, first_name: str = '',
                 last_name: str = ''):  # Initializes the starting values of the properties.
        self.first_name = first_name  # Property
        self.last_name = last_name  # Property

    # "Value" will be set to the argument of the parameter when an object from this class is created.
    # The "self" keyword tells Python to use this first instance of the parameter in the initializer.

    @property  # Getter
    def first_name(self):
        """
        Returns the first name as a title.
        :return : first name with proper formatting (string).
        """
        return self.__first_name.title()  # Returns the inputted name in title case.

    # The double underscore above means that the attribute is private and cannot be changed by outside code.

    @first_name.setter
    def first_name(self, value: str):
        """
        Sets the first name with validation.
        :param value: (string)
        :return : None
        """
        # The value parameter is what will be entered later on by the user.
        if value.isalpha() or value == '':  # Validation code for if the entered value is not a string/alphanumeric.
            self.__first_name = value
        else:
            raise ValueError("The name should only contain letters.")

    @property  # Getter
    def last_name(self):
        """
        Returns the last name as a title.
        :return : last name with proper formatting (string).
        """
        return self.__last_name.title()

    @last_name.setter
    def last_name(self, value: str):
        """
        Sets the last name with validation.
        :param value: (string)
        :return : None
        """
        if value.isalpha() or value == '':
            self.__last_name = value
        else:
            raise ValueError("The name should only contain letters.")

    def __str__(self):  # Overrides the default string method that prints the memory address to add a custom comment!
        """
        The string function for Person.
        :return : The string as a csv value.
        """
        return f'{self.__first_name}, {self.__last_name}'


class Student(Person):
    """
       A collection data specific to students - inherited from the Person class.

       Student Class specific Properties:
      - course_name: str = the student's course they are registered for.

       ChangeLog: (Who, When, What)
       S.West, 24Nov24, Created Class
    """

    # Call to the Person constructor and pass it the first_name and last_name data.
    def __init__(self, first_name: str = '', last_name: str = '', course_name: str = ''):  # Adding course_name.
        super().__init__(first_name=first_name, last_name=last_name)  # Calls the parent class initiator.
        self.course_name = course_name  # Adds the course name property to the initiator.

    @property  # Getter
    def course_name(self):
        """
        Sets the course name in title case.
        :return : course name (string).
        """
        return self.__course_name.title()

    @course_name.setter
    def course_name(self, value: str = ''):
        """
        Sets the course name.
        :param value: (string)
        :return : None
        """
        self.__course_name = value

    def __str__(self):  # Override the default string that prints the memory address to add a custom comment!
        """
        The string function for Student.
        :return : The string as a csv value.
        """
        return f'{self.__first_name}, {self.__last_name}, {self.__course_name}'


# ---------------------------------------Processing --------------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions that work with Json files.

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    S.West, 25Nov24, Updated code in a few of the methods to work with student objects.
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """ This function reads data from a json file and loads it into a list of student objects.

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        S.West, 24Nov24, Converted the list of dictionaries to list of student objects.

        :param file_name: string data with name of file to read from
        :param student_data: list of student objects to be filled with file data

        :return: list
        """
        list_of_dictionary_data: list = []  # Stores the JSON file data as a list of dictionaries.
        student_object: object  # The new object variable that loads data into student_data.
        try:
            file = open(file_name, "r")
            list_of_dictionary_data = json.load(file)  # The load function returns a list of dictionary rows.
            for student in list_of_dictionary_data:
                student_object: Student = Student(first_name=student["FirstName"],
                                                  last_name=student["LastName"],
                                                  course_name=student[
                                                      "CourseName"])  # Converts dictionaries to objects.
                student_data.append(student_object)  # Adds the converted data from the JSON file into the parameter.
                file.close()
        except FileNotFoundError as e:  # I added more custom error handling.
            IO.output_error_messages("Text file must exist before running this script!", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error reading the file!", e)
        finally:
            if file.closed == False:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes data to a json file with data from a list of student objects.

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        S.West, 24Nov24, Updated code to use convert student objects to dictionaries to work with JSON files.

        :param file_name: string data with name of file to write to
        :param student_data: list of student objects to be writen to the file.

        :return: None
        """

        try:
            list_of_dictionary_data: list = []
            for student in student_data:  # Convert list of student objects to list of dictionary rows.
                # Formats the student's data into dictionary rows for each student in student_data.
                student_json: dict \
                    = {"FirstName": student.first_name, "LastName": student.last_name,
                       "CourseName": student.course_name}
                list_of_dictionary_data.append(student_json)  # Appends data  in the newly created
                # dictionary row for each student to the list_of_dictionary_data variable.
            file = open(file_name, "w")
            json.dump(list_of_dictionary_data, file)  # Writing the data stored as a dictionary to file.
            file.close()
            IO.output_student_and_course_names(
                student_data=student_data)  # Shows the user all the data that has been saved.
        except Exception as e:
            message = "Error: There was a problem with writing to the file.\n"
            message += "Please check that the file is not open by another program."
            IO.output_error_messages(message=message, error=e)
        finally:
            if file.closed == False:
                file.close()


# ---------------------------------------Presentation --------------------------------------- #
class IO:
    """
    A collection of presentation layer functions that manage user input and output.

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    RRoot,1.2.2030,Added menu output and input functions
    RRoot,1.3.2030,Added a function to display the data
    RRoot,1.4.2030,Added a function to display custom error messages
    S.West, 25Nov24, Updated code in a few of the functions to work with student objects.
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays the custom error messages to the user

        ChangeLog: (Who, When, What)
        RRoot,1.3.2030,Created function

        :param message: string with message data to display
        :param error: Exception object with technical message to display

        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu of choices to the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function


        :return: None
        """
        print()  # Adding extra space to make it look nicer.
        print(menu)
        print()  # Adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice():
        """ This function gets a menu choice from the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function

        :return: string with the users choice
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):  # Note these are strings
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing e to avoid the technical message

        return choice

    @staticmethod
    def output_student_and_course_names(student_data: list):
        """ This function displays the student and course names to the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        S.West, 24Nov24, Updated the formatting to use student objects.

        :param student_data: list of student objects to be displayed to the user.

        :return: None
        """

        print("-" * 50)
        for student in student_data:  # Updated the print statement to call the student objects.
            print(f'Student {student.first_name} '
                  f'{student.last_name} is enrolled in {student.course_name}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """ This function gets the student's first name and last name, with a course name from the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function.
        S.West, 24Nov24, Updated the try block to use student objects instead of dictionaries.

        :param student_data: list of student objects to be filled with input data.

        :return: list
        """

        try:
            student = Student()  # The variable student creates objects from the class Student.
            # Sets the names of the object instance from class student equal to the user input.
            student.first_name = input("What is the student's first name? ")
            student.last_name = input("What is the student's last name? ")
            student.course_name = input("Please enter the course name: ")
            student_data.append(student)  # Adds the student object to the list of objects stored in student_data.
        except ValueError as e:
            IO.output_error_messages(message="One of the values was the correct type of data!", error=e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with your entered data.", error=e)
        return student_data  # The newly entered data is stored in the student_data variable as a list of objects.


# -----Start of main body-----#

# When the program starts, read the file data into a list of lists (table).
# Extract the data from the file.
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present and Process the data
while True:

    # Present the menu of choices
    IO.output_menu(menu=MENU)

    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":  # I added the method call to show student data to the user after registering.
        students = IO.input_student_data(student_data=students)
        IO.output_student_and_course_names(students)
        continue

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_and_course_names(students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # Out of the loop.
    # Removed the else block because error handling is already in place for the input_menu_choice method.

print("Program Ended")
