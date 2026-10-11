from typing import Union, Tuple

from search import search
from pathlib import Path


def print_instruction():
    """
    Выводит инструкцию по работе с программой
    """

    print("=" * 100)
    print("Программа поиска вхождений подстроки (подстрок) в строке (алгоритм Бойера–Мура–Хорспула)")
    print("=" * 100)
    print()
    print("Что нужно сделать:")
    print("1. Введите сам текст ИЛИ полный путь к файлу")
    print("   Если файл существует, программа прочитает его содержимое.")
    print("2. Укажите слово/фразу. Можно искать")
    print("   сразу несколько шаблонов: в этом случае вводите их по очереди, нажимая Enter после ввода шаблона.")
    print("3. Выберите настройки:")
    print("   • Учитывать регистр: если важно отличать «Тест» от «тест», введите True.")
    print("     Если не важно — введите False.")
    print("   • Направление поиска: 'first' — искать первые вхождения (с начала),")
    print("     'last' — последние вхождения (с конца).")
    print("   • Количество вхождений: сколько позиций нужно найти (целое число).")
    print("   • Количество подстрок для поиска: какое количество подстрок будет введено для поиска (целое число).")
    print()
    print("После ввода программа покажет позиции (номера символов), где найдены")
    print("совпадения. Если ничего не найдено — будет выведено None.")
    print("Для остановки программы напишите Exit.")
    print("-" * 100)
    print()


def start_app() -> int:
    """
    Функция, отвечающая за получение настроек от пользователя

    Возвращает
    ----------
    int
        Ответ программы на взаимодействие с ней
    """

    file_or_string = input('\nВведите строку по которой будет выполняться поиск, '
                           'либо введите путь до файла, в котором находится строка. \n'
                           'Формат ввода пути к файлу: C:\\...\\name_of_file.txt: ')

    if file_or_string == 'Exit':
        return 2

    path_obj = Path(file_or_string)

    search_in_file = False

    if path_obj.is_file():
        search_in_file = True
        file_path = file_or_string
    else:
        general_string = file_or_string

    count_of_sub_string = input('\nВведите количество подстрок, которые будут искаться (нужно ввести любое целое число от 1): ')
    if count_of_sub_string == 'Exit':
        return 2

    try:
        count_of_sub_string = int(count_of_sub_string)

        if count_of_sub_string < 1:
            print('\n!!! Количество подстрок обязательно должно быть больше либо равным единице. Повторите попытку сначала.')
            return -1

    except ValueError:
        print('\n!!! Количество подстрок может вводиться только числовым значением. Повторите попытку сначала')
        return -1

    if count_of_sub_string == 1:
        sub_string = input('\nВведите подстроку для поиска: ')
        if sub_string == 'Exit':
            return 2
    else:

        sub_string = []
        for i in range(count_of_sub_string):
            sub_string.append(input('Введите подстроку №' + str(i + 1) + " для поиска: "))
            if sub_string[i] == 'Exit':
                return 2

        sub_string = tuple(sub_string)

    max_input = input('\nВведите количество вхождений для поиска: ')
    if max_input == 'Exit':
        return 2

    try:
        max_input = int(max_input)

        if max_input < 1:
            print('\n!!! Количество вхождений обязательно должно быть больше либо равным единице. Повторите попытку сначала.')
            return -1

    except ValueError:
        print('\n!!! Количество вхождений может вводиться только числовым значением. Повторите попытку сначала')
        return -1

    method = input('\nУкажите метод поиска с конца (last) или с начала (first): ')
    if method == 'Exit':
        return 2

    if method != 'last' and method != 'first':
        print('\n!!! Есть только два метода поиска: first (с начала) и last (с конца). Повторите попытку сначала.')
        return -1

    case_sensitivity = input('\nУкажите чувствительность к регистру 0 или 1: 0 - отключить чувствительность, 1 - включить чувствительность: ')
    if case_sensitivity == 'Exit':
        return 2

    if case_sensitivity == '0':
        case_sensitivity = False
    elif case_sensitivity == '1':
        case_sensitivity = True
    else:
        print('\n!!! Чувствительность к регистру задается нулём или единицей. Повторите попытку сначала.')
        return -1

    if not search_in_file:
        start_search(general_string, sub_string, case_sensitivity, method, max_input)
    else:
        searcher_in_file(file_path, sub_string, case_sensitivity, method, max_input)

    return 0


def start_search(general_string: str, sub_string: Union[str, Tuple[str, ...]], case_sensitivity: bool, method: str, max_input: int) -> None:
    """
    Вспомогательная функция перед поиском,
    отвечает за вывод результата

    Параметры
    ---------
    general_string : str
        Строка для поиска.
    sub_string : str
        Подстрока.
    Case_sensitivity: bool
        Чувствительность к регистру.
    count : int
        Максимальное количество вхождений.
    is_last: bool
        Последняя или не последняя подстрока для поиска.
    """

    indexes = search(general_string, sub_string, case_sensitivity, method, max_input)
    print()

    if not indexes:

        print('Количество вхождений: 0')
        return

    if isinstance(indexes, tuple):

        print('Количество вхождений: ', len(indexes))
        print(return_count_of_sub_str(sub_string, indexes))

    else:

        answer_to_user = ''
        all_count = 0
        for key in indexes:
            all_count += len(indexes[key])
            answer_to_user += return_count_of_sub_str(key, indexes[key]) + '\n'

        print('Количество вхождений: ', all_count)
        print(answer_to_user)


def return_count_of_sub_str(sub_str: Union[str, Tuple[str, ...]], tuple_of_indexes: tuple) -> str:
    """
    Возвращает оформленный ответ Подстрока: *позиции на которых встретилась*

    Параметры
    ---------
    sub_str: Union[str, Tuple[str, ...]]
            Подстрока.
    tuple_of_indexes: tuple
            Кортеж индексов.

    Возвращает
    ----------
    str
        Подстрока с указанием позиций на которых она встречается
    """

    answer_to_user = f'Подстрока {sub_str} встречается на позициях: '

    counter = 0
    for index in tuple_of_indexes:
        counter += 1

        answer_to_user += str(index + 1)

        if counter != len(tuple_of_indexes):
            answer_to_user += ', '

    return answer_to_user


def return_count_of_sub_str_to_search_in_file(tuple_of_indexes: tuple, block_start_pos: int) -> str:
    """
    Возвращает позиции на которых встретилась подстрока (функция реализована для поиска в файле)

    Параметры
    ---------
    tuple_of_indexes: tuple
            Кортеж индексов.

    Возвращает
    ----------
    str
        Позиции, на которых встречается подстрока
    """

    answer_to_user = ''

    for index in tuple_of_indexes:

        answer_to_user += str(index + block_start_pos) + ', '

    return answer_to_user


def stream_file_blocks(file_path: str,
                       sub_str: str,
                       block_size: int = 5):
    """
    Читает файл блоками, обеспечивая перекрытие на стыке блоков.
    Возвращает (текст_блока, абсолютная_позиция_начала_в_файле).
    На данный момент корректно работает с кодировкой utf-8.

    Параметры
    ---------
    file_path: Path
            Путь к файлу.
    block_size: int
            Размер блока для чтения (в байтах).
    sub_str: str
            Подстрока.
    """

    overlap = len(sub_str) - 1
    prev_tail = ""
    curr_index = 0

    with open(file_path, 'r', encoding="utf-8") as file:
        while True:
            text_block = file.read(block_size)

            if not text_block:
                break

            text_block = prev_tail + text_block
            if prev_tail != "":
                block_start_pos = curr_index - len(prev_tail)
            else:
                block_start_pos = curr_index

            curr_index += len(text_block) - len(prev_tail)

            if overlap > 0:
                if len(text_block) >= overlap:
                    prev_tail = text_block[-overlap:]
                else:
                    prev_tail = text_block

            yield text_block, block_start_pos


def searcher_in_file(file_path: str, sub_string: Union[str, Tuple[str, ...]], case_sensitivity: bool, method: str, max_input: int) -> None:
    """
    Вспомогательная функция для поиска в файле, отвечает за вывод результата

    Параметры
    ---------
    sub_string : str
        Подстрока.
    case_sensitivity: bool
        Чувствительность к регистру.
    method: str
        Метод поиска с начала или с конца.
    max_input : int
        Максимальное количество вхождений.
    """

    user_answer = ''
    total_number = 0

    if isinstance(sub_string, tuple):

        curr_answer = ''

        for sub_str in sub_string:
            for block_text, block_start_pos in stream_file_blocks(file_path, sub_str):
                indexes = search(block_text, sub_str, case_sensitivity, method, max_input)

                if indexes is not None:

                    total_number += len(indexes)
                    user_answer += return_count_of_sub_str_to_search_in_file(indexes, block_start_pos)

            user_answer = f'Подстрока {sub_str} встречается на позициях {user_answer}'
            user_answer = user_answer[:-2] + '\n'

            curr_answer += user_answer
            user_answer = ''

        user_answer = curr_answer

    else:
        for block_text, block_start_pos in stream_file_blocks(file_path, sub_string):
            indexes = search(block_text, sub_string, case_sensitivity, method, max_input)

            if indexes is not None:

                total_number += len(indexes)
                user_answer += return_count_of_sub_str_to_search_in_file(indexes, block_start_pos)

        user_answer = f'Подстрока {sub_string} встречается на позициях {user_answer}'
        user_answer = user_answer[:-2] + '\n'

    print('\nКоличество вхождений: ', total_number)
    print(user_answer)


if __name__ == '__main__':

    print_instruction()

    answer = start_app()

    while answer != 2:
        answer = start_app()



