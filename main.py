# This is a sample Python script.
# from imdbmoviedata
# import imdbseriesepdata
import os
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
# import imdbmoviedata

ch = input("Enter 1. for Movies \n 2.for Series")

if ch == "1":
    os.system('python imdbmoviedata.py')

elif ch == "2":
    os.system('python imdbseriesepdata.py')

else:
    print("invalid")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
