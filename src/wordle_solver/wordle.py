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
        guess_result = []

        for i, guess_letter in enumerate(guess):
            if guess_letter == self.__answer[i]:
                guess_result.append(LetterResult.GREEN)
            elif guess_letter in self.__answer:
                # TODO Improve yellow logic so that it doesn't count the same letter twice.
                guess_result.append(LetterResult.YELLOW)
            else:
                guess_result.append(LetterResult.BLACK)

        return guess_result

    def __str__(self):
        return (f"Wordle(answer={self.__answer}, guesses={self.guess_history}, guess_count={len(self.guess_history)}"
                f", has_won={self.has_won})")

    def __repr__(self):
        return str(self)
