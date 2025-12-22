import random


def get_players_names():
    while True:
        player_1 = input("Введите имя первого игрока: ").strip()
        player_2 = input("Введите имя второго игрока: ").strip()

        if validate_names(player_1, player_2):
            print("\nПоприветствуем игроков!")
            print(f"Первый игрок: {player_1}\nВторой игрок: {player_2}")
            return player_1, player_2


def validate_names(name_1, name_2):
    if not name_1 or not name_2:
        print("Имена не должны быть пустыми, введите имя еще раз.\n")
        return False
    if name_1 == name_2:
        print("Имена не должны быть одинаковыми, введите имя еще раз.\n")
        return False
    if any(char.isdigit() for char in name_1 + name_2):
        print("Имена не должны содержать цифры, введите имя еще раз.\n")
        return False
    return True


def load_questions():
    # return {
    # "Столица франции?" : "париж",
    # "Как звали собаку в сказке про репку?" : "жучка",
    # "Как называется результат умножения?" : "произведение",
    # "Как называется свадьба на 25 летнюю годовщину" : "серебряная",
    # "Кто был басистом в The Beatles?" : "пол маккартни",
    # "Самый большой океан?" : "тихий",
    # "Самая маленькая птица?" : "колибри",
    # "Самая милая кошка?" : "соня"
    # }
    return {
    # Простые односложные слова
    "Какой фрукт желтый и кислый?": "лимон",
    "Какое животное дает молоко?": "корова",
    "Что светит ночью на небе?": "луна",
    "Какой цвет получается при смешивании красного и синего?": "фиолетовый",
    "Что измеряет термометр?": "температура",
    "Кто автор сказки о золотой рыбке?": "пушкин",
    "Какой месяц идет после мая?": "июнь",
    "Что такое html?": "язык",
    "Как называется результат сложения?": "сумма",
    "Сколько ног у паука?": "восемь",

    # Двусложные слова
    "Столица россии?": "москва",
    "Самый жаркий материк?": "африка",
    "Какой напиток делают из винограда?": "вино",
    "Кто написал картину черный квадрат?": "малевич",
    "Какой прибор показывает время?": "часы",

    # Трехсложные слова
    "Самый большой материк?": "евразия",
    "Первый месяц весны?": "март",
    "Сладкий красный овощ?": "помидор",
    "Какой праздник отмечают 9 мая?": "победа",
    "Сколько планет в солнечной системе?": "восемь",
}



def choose_random_question(questions):
    return random.choice(list(questions.keys()))


def create_hidden_word(answer):
    return ["_"] * len(answer)


def display_game_state(question, hidden_word, current_player, wrong_guesses):
    print("\n" + "=" * 50)
    print(f"Вопрос: {question}")
    print(f"Слово из {len(hidden_word)} букв: {' '.join(hidden_word)}")
    print(f"Ходит: {current_player}")

    if wrong_guesses:
        print(f"Неверные буквы: {', '.join(sorted(wrong_guesses))}")

    print("=" * 50)


def get_player_guess(current_player):
    while True:
        guess = input(f"\n{current_player}, введите букву или слово целиком: ").lower().strip()

        if not guess:
            print("Ввод не может быть пустым!")
            continue

        if not validate_guess(guess):
            print("Можно вводить только буквы русского алфавита!")
            continue

        return guess


def validate_guess(guess):
    valid_chars = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя ")
    return all(char in valid_chars for char in guess)


def process_guess(guess, answer, hidden_word):
    if guess == answer:
        return True, hidden_word

    if len(guess) == 1:
        if guess in answer:
            new_hidden_word = hidden_word.copy()
            for i, char in enumerate(answer):
                if char == guess:
                    new_hidden_word[i] = guess
            return False, new_hidden_word
        else:
            return False, hidden_word

    return False, hidden_word


def determine_first_player(player1, player2):
    print(f"\nОпределяем, кто ходит первым...")
    result = random.choice([player1, player2])
    print(f"Первым ходит: {result}!")
    return result


def switch_player(current_player, player1, player2):
    return player2 if current_player == player1 else player1


def check_game_over(hidden_word):
    return "_" not in hidden_word


def display_final_results(winner, question, answer):
    print("\n" + "=" * 50)
    print("ИГРА ОКОНЧЕНА!")
    print(f"ПОБЕДИТЕЛЬ: {winner}")
    print(f"Вопрос: {question}")
    print(f"Загаданное слово: {answer}")
    print("=" * 50)


def game_start_notification():
    print(f"\n{'=' * 50}")
    print("НАЧИНАЕМ ИГРУ!")
    print(f"{'=' * 50}")


def game_loop(player1, player2, questions):
    question = choose_random_question(questions)
    answer = questions[question]

    hidden_word = create_hidden_word(answer)
    current_player = determine_first_player(player1, player2)
    wrong_guesses = set()
    game_over = False

    game_start_notification()

    while not game_over:
        display_game_state(question, hidden_word, current_player, wrong_guesses)

        guess = get_player_guess(current_player)

        guessed_word, new_hidden_word = process_guess(guess, answer, hidden_word)

        if guessed_word:
            print(f"\nПОБЕДА! {current_player} угадал слово целиком!")
            game_over = True
        elif new_hidden_word != hidden_word:
            hidden_word = new_hidden_word
            print(f"\nВерно! Буква '{guess}' есть в слове.")

            if check_game_over(hidden_word):
                print(f"\nПОБЕДА! {current_player} угадал все слово!")
                game_over = True
            else:
                print(f"{current_player} получает дополнительный ход!")
                continue
        else:
            if len(guess) != 1:
                print(f"\nНеверно! Загаданное слово не '{guess}'. Ход переходит к следующему игроку")
            else:
                print(f"\nНеверно! Буквы '{guess}' нет в слове. Ход переходит к следующему игроку")
                wrong_guesses.add(guess)
            current_player = switch_player(current_player, player1, player2)

    display_final_results(current_player, question, answer)


def play_game():
    player1, player2 = get_players_names()
    questions = load_questions()
    game_loop(player1, player2, questions)


def main():
    print("ДОБРО ПОЖАЛОВАТЬ В ИГРУ!")

    while True:
        play_game()

        play_again = input("\nХотите сыграть еще раз? (да/нет): ").lower()

        if play_again in ["да", "д", "yes", "y"]:
            game_start_notification()
        else:
            print("\nСпасибо за игру! До встречи!")
            break


if __name__ == "__main__":
    main()
