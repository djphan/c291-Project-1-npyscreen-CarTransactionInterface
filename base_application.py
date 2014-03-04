

class BaseApplication:
    """
    Provide basic (but incomplete) application functionality. Specific
    applications will inherit from this class. Not to be instantiated; only
    instances of subclasses should be called.

    Defines:
      get_input
      run
      
    Override:
      __init__
      process_input
      validate
    """
    
    def __init__(self, cursor):

        self.curs = cursor
        self.quit = False

        #--- Override the variables below ---#

        # Prompt message
        self.prompt_msg = "Enter input, or \"q\" to quit:\n> "

        # Welcome message
        self.welcome_msg = "BASE_APPLICATION"

    def get_input(self):
        while 1:
            user_input = input(self.prompt_msg)

            if user_input in {'q', 'Q', 'quit', 'Quit', 'QUIT'}:
                self.quit = True
                return None

            elif self.validate(user_input):
                return user_input

            else:
                print("Unrecognized command. Please try again.")
                # and loop back to get new input

    def validate(self, user_input):
        """
        Given user input from the terminal, return True if the input is valid to
        pass to process_input.

        Subclasses of BaseApplication should override this.
        """
        return user_input in {'foo', 'bar', '1', '2', '3', '10'}

    def run(self):
        print(self.welcome_msg)
        while not self.quit:
            user_input = self.get_input()
            if user_input:
                self.process_input(user_input)

    def process_input(self, user_input):
        """
        Contains only test code in BaseApplication.
        Subclasses of BaseApplication should override this.
        """
        print("NCHARS: %d" % len(user_input))
        print(user_input)


