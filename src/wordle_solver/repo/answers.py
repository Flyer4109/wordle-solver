import random
from abc import ABC, abstractmethod


class AnswersRepo(ABC):
    @abstractmethod
    def random_answer(self) -> str:
        pass


class TextFileAnswers(AnswersRepo):
    def __init__(self, file_path: str) -> None:
        self.answers = self.read_answers(file_path)

    @staticmethod
    def read_answers(file_path: str) -> list[str]:
        answers = []
        with open(file_path, "r") as f:
            for line in f:
                answers.append(line.strip())
        return answers

    def random_answer(self) -> str:
        random_index = random.randint(0, len(self.answers) - 1)
        return self.answers[random_index]


class NoopAnswers(AnswersRepo):
    def __init__(self, answer: str) -> None:
        self.answer = answer

    def random_answer(self) -> str:
        return self.answer
