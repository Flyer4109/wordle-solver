from game_show_host import GameShowHost
from repo.answers import TestAnswers
from wordle import Game

if __name__ == "__main__":
    game = Game(TestAnswers("hello"))

    guess = GameShowHost.ask_question("What is your guess? ")
    has_won, guess_result, game_ended = game.input_guess(guess)
    print(guess_result)

    while not game_ended:
        guess = GameShowHost.ask_question("What is your next guess? ")
        has_won, guess_result, game_ended = game.input_guess(guess)
        print(guess_result)

    if has_won:
        print("You won!")
    else:
        print("You lost :(")

