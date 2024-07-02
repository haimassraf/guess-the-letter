import random


def try_update_letter_guessed(letter_guessed: str, old_letters_guessed: list) -> bool:
    """
    if the user guess true it append it to the old letter guess, if not it will print notification accordingly
    :param letter_guessed: str
    :param old_letters_guessed: list[str]
    :return: bool
    """
    if (len(letter_guessed) > 1 or not letter_guessed.isalpha() or not letter_guessed.isascii() or
            letter_guessed.lower() in old_letters_guessed):
        print('X')
        print(' -> '.join(sorted([*old_letters_guessed])))
        return False
    else:
        old_letters_guessed.append(letter_guessed.lower())
        return True


def show_hidden_word(secret_word: str, old_letters_guessed: list[str]) -> str:
    """
    show the hidden word with the letter that the user guess
    :param secret_word: str
    :param old_letters_guessed: list[str]
    :return: str
    """
    new_str = ""
    for char in secret_word:
        if char in old_letters_guessed:
            new_str += f" {char} "
        else:
            new_str += ' _ '
    return new_str


def check_win(secret_word: str, old_letters_guessed: list[str]) -> bool:
    """
    check if their no ' _ ' in the secret word and if the user won
    :param secret_word:
    :param old_letters_guessed:
    :return:
    """
    if '_' in show_hidden_word(secret_word, old_letters_guessed):
        return False
    return True


number_of_players = int(input("How many players do you wants to play? "))
# the number of the players

players = {}
for i in range(number_of_players):
    player_name = input(f"Enter name for player {i + 1}: ")
    players[player_name.upper()] = 0
# save all the players and there score

CATEGORY_LIST = ['fruits', 'cars', 'profession', 'countries']
user_choice = input(f"Enter a category ({', '.join(CATEGORY_LIST)}): ").lower()
# category to run on

while user_choice not in CATEGORY_LIST:
    user_choice = input(f"\nEnter a correct category ({', '.join(CATEGORY_LIST)}): ").lower()
#  not stop until the user enter a correct category

file = f"{user_choice}.txt"
# path of the correct category

with open(file, "r") as file:
    word_txt = file.read()
word_list = word_txt.split('\n')
# The list of the words from the selector category

big_flag = True
while word_list and big_flag:
    # run while there are words in the word list

    random_index = random.randint(0, len(word_list) - 1)
    secret_word = word_list.pop(random_index)
    # select a random secret word from the words list and remove it from the list

    print(' _ ' * len(secret_word))

    old_letter_guess = []
    # create a list that all the proper guessed letter will be there

    flag = True
    while flag:
        # nested loop that repeats on the player until the word guessed

        for player_name in players:
            # response the players turn

            letter_guess = input(f"\n{player_name} Enter a letter guess "
                                 f"(for stopping the game enter '.'): ").lower()

            if letter_guess == ".":
                flag = False
                big_flag = False
                break
            #     Brake condition if the player enter '.'

            while not try_update_letter_guessed(letter_guess, old_letter_guess):
                letter_guess = input(f"\n{player_name} Enter a correct letter guess "
                                     f"(for stopping the game enter '.'): ").lower()
                # not stop until the user enter a proper letter and if it`s not already guessed

                if letter_guess == ".":
                    flag = False
                    big_flag = False
                    break
                #     Brake condition if the player enter '.'

            if letter_guess in secret_word:
                # check if the letter guess is correct

                players[player_name] += 1
                # update the score of the player

                if check_win(secret_word, old_letter_guess):
                    # check if the users guessed all the letters

                    print(show_hidden_word(secret_word, old_letter_guess))
                    # find out the secret word

                    flag = False
                    break
                    # brake from two loops when the word guessed and continue to another word

                if flag:
                    print()
                    for player, score in players.items():
                        print(f"{player}: {score}")
                    # print the table score after every correct guessed
            else:
                print(':(\n')

            print(show_hidden_word(secret_word, old_letter_guess))
    #         Print the secret word with the guessed letters after every turn


player_name_width = max(len(player) for player in players) + 2
score_width = 6
print(f"\n{'Player'.ljust(player_name_width)}{'Score'.rjust(score_width)}")
print("=" * (player_name_width + score_width))
for player_name, score in players.items():
    print(f"{player_name.ljust(player_name_width)}{str(score).rjust(score_width)}")
# print a nice table score at the end of the game

high_score = 0
winner_player = ""
number_of_winners = 1
for player, score in players.items():
    if score > high_score:
        high_score = score
        number_of_winners = 1
        winner_player = player
    elif score == high_score:
        number_of_winners += 1
        winner_player += f", {player}"
# update the winner, amounts of winners and the max score

if number_of_winners == 1:
    print(f"\nThe winner is {winner_player} with {high_score} points!")
#     print unic message if there is one winner

elif 1 < number_of_winners < number_of_players:
    print(f"\nThere are some winners!\n{winner_player} with {high_score} points!")
#     print a message if there are some winners

else:
    print("It is a draw!")
#     in case that there a draw between all the players
