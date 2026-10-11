from typing import Dict


def return_table(substr: str) -> Dict[str, int]:
    """
    Строит таблицу смещений для алгоритма Бойера-Мура-Хорспула
    для прямого поиска подстроки (слева направо).

    Параметры
    ---------
    substr : str
        Подстрока, для которой строится таблица смещений.

    Возвращает
    ----------
    dict[str, int]
        Словарь вида {символ: смещение}.

    """

    unique_sym = set()
    len_substr = len(substr)

    dictionary_offset = {}

    for i in range(len_substr - 2, -1, -1):

        if substr[i] in unique_sym:
            continue
        else:
            dictionary_offset[substr[i]] = len_substr - i - 1
            unique_sym.add(substr[i])

    if substr[-1] not in unique_sym:
        dictionary_offset[substr[-1]] = len_substr

    dictionary_offset['*'] = len_substr

    return dictionary_offset


def return_reverse_table(substr: str) -> Dict[str, int]:
    """
    Строит таблицу смещений для алгоритма Бойера-Мура-Хорспула, для поиска подстроки с конца.

    Параметры
    ---------
    substr : str
        Подстрока, для которой строится таблица смещений.

    Возвращает
    ----------
    dict[str, int]
        Словарь вида {символ: смещение}.

    """

    unique_sym = set()
    len_substr = len(substr)

    dictionary_offset = {}

    for i in range(1, len_substr):
        if substr[i] in unique_sym:
            continue
        else:
            dictionary_offset[substr[i]] = i
            unique_sym.add(substr[i])

    if substr[0] not in unique_sym:
        dictionary_offset[substr[0]] = len_substr

    dictionary_offset['*'] = len_substr

    return dictionary_offset
