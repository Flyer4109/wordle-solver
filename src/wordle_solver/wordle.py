from enum import Enum

from wordle_solver.repo.answers import AnswersRepo


class LetterResult(Enum):
    BLACK = 1
    YELLOW = 2
    GREEN = 3


class GameFinishedError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Game:
    MAX_GUESSES: int = 5

    def __init__(self, answer_supplier: AnswersRepo):
        self.__answerSupplier = answer_supplier
        self.__answer = self.__answerSupplier.random_answer()
        self.guess_history = []
        self.has_won = False

    def input_guess(self, guess: str) -> tuple[bool, list[LetterResult], bool]:
        if self._has_game_ended():
            return self.has_won, [], True

        self.guess_history.append(guess)

        guess_result = self._guess_result(guess)
        self.has_won = all(letter_result == LetterResult.GREEN for letter_result in guess_result)

        return self.has_won, guess_result, self._has_game_ended()

    def _has_game_ended(self) -> bool:
        return len(self.guess_history) >= Game.MAX_GUESSES or self.has_won

    def _guess_result(self, guess: str) -> list[LetterResult]:
        basic_result = self._basic_result(guess)
        return self._remove_duplicate_yellows(guess, basic_result)

    def _basic_result(self, guess: str) -> list[LetterResult]:
        guess_result = []

        for i, guess_letter in enumerate(guess):
            if guess_letter == self.__answer[i]:
                guess_result.append(LetterResult.GREEN)
            elif guess_letter in self.__answer:
                guess_result.append(LetterResult.YELLOW)
            else:
                guess_result.append(LetterResult.BLACK)

        return guess_result

    def _remove_duplicate_yellows(self, guess, position_result) -> list[LetterResult]:
        # Get a list of letters the player still has to guess.
        letters_left_to_guess = [letter for i, letter in enumerate(self.__answer) if
                                 position_result[i] != LetterResult.GREEN]

        # Detect duplicate yellows and turn them into black results.
        for i, result in enumerate(position_result):
            if result == LetterResult.YELLOW:
                if guess[i] in letters_left_to_guess:
                    letters_left_to_guess.remove(guess[i])
                else:
                    position_result[i] = LetterResult.BLACK
        return position_result

    def __str__(self):
        return (f"Wordle(answer={self.__answer}, guesses={self.guess_history}, guess_count={len(self.guess_history)}"
                f", has_won={self.has_won})")

    def __repr__(self):
        return str(self)
