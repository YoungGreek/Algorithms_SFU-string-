from typing import Union, Tuple, Optional

from table import return_table, return_reverse_table
from logging import log_execution_time


def search(string: str, sub_string: Union[str, Tuple[str, ...]],
           case_sensitivity: bool, method: str, count: int) -> Optional[Union[Tuple[int, ...], dict]]:
    """
    Поиск подстроки (или нескольких подстрок) в строке.

    Параметры
    ---------
    string : str
        Исходная строка для поиска.
    sub_string : str | tuple[str, ...]
        Подстрока для поиска либо кортеж подстрок для одновременного поиска.
    case_sensitivity : bool
        Если True - поиск чувствителен к регистру. Если False — регистр игнорируется.
    method : str
        Способ поиска: 'first' — искать первые вхождения, 'last' — последние.
    count : int
        Максимальное количество найденных позиций для каждой подстроки.

    Возвращаемое значение
    ---------------------
    tuple[int, ...] | dict | None
        - Если `sub_string` — строка: кортеж индексов начала найденных вхождений
          (в порядке обнаружения) или None, если ничего не найдено.
        - Если `sub_string` — кортеж: словарь вида {подстрока: tuple[int, ...] или None}.
        - None возвращается, если исходная строка пуста или длина подстроки больше длины строки.
    """

    if string == "":
        return None

    if isinstance(sub_string, tuple):
        return_dict = {}

        if not case_sensitivity:
            string = string.lower()

        counter = 0

        is_last = False
        for sub_str in sub_string:

            counter += 1
            if counter == len(sub_string) or count == 1:
                is_last = True

            if len(string) < len(sub_str):
                return_dict[sub_str] = None

            else:
                if not case_sensitivity:
                    return_dict[sub_str] = help_to_search(string, sub_str.lower(), count, method, is_last)
                else:
                    return_dict[sub_str] = help_to_search(string, sub_str, count, method, is_last)

            if return_dict[sub_str] is not None:
                count -= len(return_dict[sub_str])

        return return_dict

    else:

        if sub_string == "" or len(string) < len(sub_string):
            return None

        if not case_sensitivity:
            string = string.lower()
            sub_string = sub_string.lower()

        return help_to_search(string, sub_string, count, method, True)


def help_to_search(string: str, sub_string: str, count: int, method: str, is_last: bool) -> Optional[Tuple[int, ...]]:
    """
    Вспомогательная функция для разделения поиска с начала или с конца.

    Параметры
    ---------
    string : str
        Строка, в которой выполняется поиск.
    sub_string : str
        Подстрока для поиска.
    count : int
        Максимальное число найденных позиций.
    method : str
        'first' или 'last'.
    is_last: bool
        Последняя или не последняя подстрока для поиска

    Возвращает
    ----------
    tuple[int, ...] | None
        Кортеж индексов или None, если совпадений нет.
    """

    if count == 0:
        return None

    if method == 'first':
        return search_first(string, sub_string, count, is_last)
    elif method == 'last':
        return search_last(string, sub_string, count, is_last)
    else:
        return None


@log_execution_time
def search_first(string: str, sub_string: str, count: int, is_last: bool) -> Optional[Tuple[int, ...]]:
    """
    Поиск вхождений с начала (алгоритм Бойера-Мура-Хорспула).

    Параметры
    ---------
    string : str
        Строка для поиска.
    sub_string : str
        Подстрока.
    count : int
        Максимальное количество вхождений.
    is_last: bool
        Последняя или не последняя подстрока для поиска

    Возвращает
    ----------
    tuple[int, ...] | None
        Кортеж стартовых индексов найденных вхождений или None, если нет совпадений.
    """

    dictionary_offset = return_table(sub_string)

    len_substr = len(sub_string)

    index_arr = []

    i = len_substr - 1
    while i < len(string):
        k = 0
        for j in range(len_substr - 1, -1, -1):
            if string[i - k] != sub_string[j]:
                if j == len_substr - 1:
                    if string[i] in dictionary_offset:
                        off = dictionary_offset[string[i]]
                    else:
                        off = dictionary_offset['*']
                else:
                    off = dictionary_offset[sub_string[j]]
                i += off
                break
            else:
                k += 1

                if j == 0:
                    index_arr.append(i - k + 1)
                    i += dictionary_offset[sub_string[0]]

                    count -= 1
                    if (count == 1 and not is_last) or count == 0:
                        if len(index_arr) == 0:
                            return None
                        return tuple(index_arr)

    if len(index_arr) == 0:
        return None
    return tuple(index_arr)


@log_execution_time
def search_last(string: str, sub_string: str, count: int, is_last: bool) -> Optional[Tuple[int, ...]]:
    """
    Поиск вхождений с конца (алгоритм Бойера-Мура-Хорспула).

    Параметры
    ---------
    string : str
        Строка для поиска.
    sub_string : str
        Подстрока.
    count : int
        Максимальное количество вхождений.
    is_last: bool
        Последняя или не последняя подстрока для поиска

    Возвращает
    ----------
    tuple[int, ...] | None
        Кортеж стартовых индексов найденных вхождений или None, если нет совпадений.
    """

    dictionary_offset = return_reverse_table(sub_string)

    len_substr = len(sub_string)

    index_arr = []

    i = len(string) - len_substr
    while i >= 0:
        k = 0

        for j in range(0, len_substr):
            if string[i + k] != sub_string[j]:
                if j == 0:
                    if string[i] in dictionary_offset:
                        off = dictionary_offset[string[i]]
                    else:
                        off = dictionary_offset['*']
                else:
                    off = dictionary_offset[sub_string[j]]
                i -= off
                break
            else:
                k += 1

                if j == len_substr - 1:
                    index_arr.append(i)
                    i -= dictionary_offset[sub_string[0]]

                    count -= 1
                    if (count == 1 and not is_last) or count == 0:
                        if len(index_arr) == 0:
                            return None
                        return tuple(index_arr)

    if len(index_arr) == 0:
        return None
    return tuple(index_arr)
