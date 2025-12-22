first_player, second_player = input("Введите имя первого игрока: "), input("Введите имя второго игрока: ")

print(f"Поприветствуем игроков! Первый игрок: {first_player}, Второй игрок: {second_player}")

question = "Чем на Руси выводили веснушки?"
game_word = "яйцо"

# TODO: исключить ввод цифр, пустых значений, спецсимволов
# TODO: определитиь игрока который начинает первым броском монетки
# TODO: очищать поле введеных букв (вопрос, слово, последняя введенная буква)
# TODO: показывать список использованных НЕВЕРНЫХ букв

print(question)
hidden_word = ["*"] * len(game_word)
print(f"Загаданное слово {len(game_word)} букв: {' '.join(hidden_word)}")

current_player = first_player
player_won = False

while "*" in hidden_word and not player_won:
    guess = input(f"{current_player} введите слово полностью или предполагаемую букву: ").lower()
    if guess == game_word:
        print(f"Победитель {current_player}")
        player_won = True
        break

    if guess in game_word:
        for i, char in enumerate(game_word):
            if char == guess:
                hidden_word[i] = guess
        print(f"Есть такая буква! Загаданное слово: {' '.join(hidden_word)}")

        if "*" not in hidden_word:
            print(f"Победитель {current_player}")
            break

        print(f"{current_player} угадал букву! Ходите еще раз.")
        continue
    else:
        print("Такой буквы нет. Ход переходит к следующему игроку")
        current_player = second_player if current_player == first_player else first_player



