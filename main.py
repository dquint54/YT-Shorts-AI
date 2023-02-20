from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import Variables



from Login import login

def main():


    login(Variables.username, Variables.password)



if __name__ == '__main__':

    main()

