from wordle_solver.repo.answers import NoopAnswers
from wordle_solver.wordle import Game, LetterResult

all_correct = [LetterResult.GREEN, LetterResult.GREEN, LetterResult.GREEN, LetterResult.GREEN, LetterResult.GREEN]
all_incorrect = [LetterResult.BLACK, LetterResult.BLACK, LetterResult.BLACK, LetterResult.BLACK, LetterResult.BLACK]
all_wrong_position = [LetterResult.YELLOW, LetterResult.YELLOW, LetterResult.YELLOW, LetterResult.YELLOW,
                      LetterResult.YELLOW]


def test_input_guess_game_ends_on_correct_word():
    game = Game(NoopAnswers("hello"))
    has_won, _, game_over = game.input_guess("hello")
    assert has_won is True
    assert game_over is True


def test_input_guess_no_letters_correct():
    game = Game(NoopAnswers("hello"))
    _, result, _ = game.input_guess("aaaaa")
    assert result == all_incorrect


def test_input_guess_all_letters_in_wrong_position():
    game = Game(NoopAnswers("hello"))
    _, result, _ = game.input_guess("lleoh")
    assert result == all_wrong_position


def test_input_guess_does_not_show_extra_duplicate_letters_as_yellow():
    game = Game(NoopAnswers("hello"))
    _, result, _ = game.input_guess("lllll")
    assert result == [LetterResult.BLACK, LetterResult.BLACK, LetterResult.GREEN, LetterResult.GREEN,
                      LetterResult.BLACK]


def test_input_guess_does_not_show_extra_duplicate_letters_as_yellow_when_in_wrong_locations():
    game = Game(NoopAnswers("hello"))
    _, result, _ = game.input_guess("llaal")
    # The first two 'l's should be yellow and the third 'l' should be black. As 'hello' only contains 2 'l's.
    assert result == [LetterResult.YELLOW, LetterResult.YELLOW, LetterResult.BLACK, LetterResult.BLACK,
                      LetterResult.BLACK]


def test_input_guess_game_ends_after_max_incorrect_guesses():
    game = Game(NoopAnswers("hello"))

    for _ in range(Game.MAX_GUESSES - 1):
        _, _, game_over = game.input_guess("aaaaa")
        assert game_over is False

    has_won, _, game_over = game.input_guess("aaaaa")
    assert game_over is True
    assert has_won is False


def test_input_guess_history_of_guesses():
    game = Game(NoopAnswers("hello"))

    game.input_guess("aaaaa")
    game.input_guess("lleoh")
    game.input_guess("lllll")

    assert game.guess_history == ["aaaaa", "lleoh", "lllll"]


def test_input_guess_after_game_ends_does_not_change_game_state():
    game = Game(NoopAnswers("hello"))

    has_won, _, game_over = game.input_guess("hello")

    assert has_won is True
    assert game_over is True

    has_won, result, game_over = game.input_guess("aaaaa")

    assert has_won is True
    assert result == []
    assert game_over is True
