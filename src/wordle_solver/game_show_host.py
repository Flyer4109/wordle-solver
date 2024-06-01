import re


class GameShowHost:
    @staticmethod
    def ask_question(question: str) -> str:
        guess = input(question)
        while not GameShowHost.validate_guess(guess):
            print("Invalid guess. Must be 5 letters.")
            guess = input(question)
        return guess

    @staticmethod
    def validate_guess(guess: str) -> bool:
        regex = r"^[a-zA-Z]{5}$"
        return re.match(regex, guess) is not None
