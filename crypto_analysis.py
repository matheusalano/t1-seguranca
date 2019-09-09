import sys
from math import gcd
from functools import reduce


def kasiski_test(text):

    tris = []
    distances = []

    # Salva os trigramas e a distancia entre eles
    for i in range(len(text) - 2):
        tri = text[i:i + 3]

        if tri in tris:
            last_idx = text.rfind(tri, 0, i)
            distances.append(i - last_idx)
        else:
            tris.append(tri)

    occur_count = {}

    # Conta o numero de ocorrencias de cada distancia encontrada
    # e salva em um dicionário
    for d in distances:
        if d not in occur_count:
            occur_count[d] = 1
        else:
            occur_count[d] += 1

    # Ordena esse dicionario ao contrário pela numero de ocorrencias
    occur_count = sorted(occur_count.items(),
                         key=lambda kv: (kv[1], kv[0]), reverse=True)
    # Salva apenas as 20 distancias com maior ocorrencia
    occur_count = occur_count[:20]

    distances = list(map(lambda x: x[0], occur_count))

    # Retorna o MDC dessas distancias
    return reduce(lambda x, y: gcd(x, y), distances)


# Separa o texto cifrado em pedaços pelo tamanho da chave
def split_chunk_data(i, arr, size):
    chunk = arr[i:min(len(arr), i+size)]
    return chunk


# Prepara o texto cifrado para ser analizado
def prepare_data(keyword_lenght, contents):
    matrix_values = []
    for i in range(0, (len(contents)-keyword_lenght), keyword_lenght):
        word = split_chunk_data(i, contents, keyword_lenght)
        matrix_values.append(list(word))

    return matrix_values


# Contagem de frequencia das letras por posição na chave
# TODO: levar em consideração frequencia das letras em português
def frequency_count(_dict_, letter):
    if _dict_.__contains__(letter):
        _dict_.update({letter: _dict_[letter]+1})


def vigenere_test(values):
    # TODO: criar dict dinamicamente pelo tamanho da chave

    base_dict = dict({
        "a": 0,
        "b": 0,
        "c": 0,
        "d": 0,
        "e": 0,
        "f": 0,
        "g": 0,
        "h": 0,
        "i": 0,
        "j": 0,
        "k": 0,
        "l": 0,
        "m": 0,
        "n": 0,
        "o": 0,
        "p": 0,
        "q": 0,
        "r": 0,
        "s": 0,
        "t": 0,
        "u": 0,
        "v": 0,
        "w": 0,
        "x": 0,
        "y": 0,
        "z": 0
    })

    first_letter = base_dict.copy()
    second_letter = base_dict.copy()
    third_letter = base_dict.copy()
    fourth_letter = base_dict.copy()
    fifth_letter = base_dict.copy()
    sixth_letter = base_dict.copy()
    seventh_letter = base_dict.copy()
    for words in values:
        frequency_count(first_letter, words[0])
        frequency_count(second_letter, words[1])
        frequency_count(third_letter, words[2])
        frequency_count(fourth_letter, words[3])
        frequency_count(fifth_letter, words[4])
        frequency_count(sixth_letter, words[5])
        frequency_count(seventh_letter, words[6])

    for (key, value) in sorted(first_letter.items()):
        print(f"First Letter = {key} Count = {value}")


def main():
    filepath = sys.argv[1]
    f = open(filepath, "r")
    contents = f.read()
    keyword_lenght = kasiski_test(contents)
    values = prepare_data(keyword_lenght, contents)
    vigenere_test(values)


if __name__ == "__main__":
    main()
