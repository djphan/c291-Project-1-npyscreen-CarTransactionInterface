from base_application import BaseApplication

class ViolationRecord(BaseApplication):

    def __init__(self, cursor):
        super().__init__(cursor)

        self.welcome_msg = "VIOLATION_RECORD INIT"
        self.prompt_msg = "Enter Violation:\n> "

    # def validate(self, user_input):
    #     pass

    # def process_input(self, user_input):
    #     pass
