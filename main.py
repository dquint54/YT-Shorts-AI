
from twisted.python.util import println

import Variables

from Logins import login
from Cooking_Facts_Generator import facts_generator


def main():

    login_success = login(Variables.username, Variables.password)

    if login_success:
        println("Youtube login was successful")
    else:
        println("Youtube login was not successful")




if __name__ == '__main__':
    main()
