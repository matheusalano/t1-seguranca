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
def frequency_count(_dict_, letter):
    if _dict_.__contains__(letter):
        _dict_.update({letter: _dict_[letter]+1})
    else:
        _dict_[letter] = 0


def vigenere_test(values):
    first_letter = dict()
    second_letter = dict()
    third_letter = dict()
    fourth_letter = dict()
    fifth_letter = dict()
    sixth_letter = dict()
    seventh_letter = dict()
    for words in values:
        frequency_count(first_letter, words[0])
        frequency_count(second_letter, words[1])
        frequency_count(third_letter, words[2])
        frequency_count(fourth_letter, words[3])
        frequency_count(fifth_letter, words[4])
        frequency_count(sixth_letter, words[5])
        frequency_count(seventh_letter, words[6])

    # TODO refatorar essa contagem
    for (key, value) in sorted(first_letter.items(), key=lambda x: x[1], reverse=True):
        if(value > 200):
            print(f"First Letter = {key} Count = {value}")

    for (key, value) in sorted(second_letter.items(), key=lambda x: x[1], reverse=True):
        if(value > 200):
            print(f"Second Letter = {key} Count = {value}")

    for (key, value) in sorted(third_letter.items(), key=lambda x: x[1], reverse=True):
        if(value > 200):
            print(f"Third Letter = {key} Count = {value}")

    for (key, value) in sorted(fourth_letter.items(), key=lambda x: x[1], reverse=True):
        if(value > 200):
            print(f"Fourth Letter = {key} Count = {value}")

    for (key, value) in sorted(fifth_letter.items(), key=lambda x: x[1], reverse=True):
        if(value > 200):
            print(f"Fifth Letter = {key} Count = {value}")

    for (key, value) in sorted(sixth_letter.items(), key=lambda x: x[1], reverse=True):
        if(value > 200):
            print(f"Sixth Letter = {key} Count = {value}")

    for (key, value) in sorted(seventh_letter.items(), key=lambda x: x[1], reverse=True):
        if(value > 200):
            print(f"Seventh Letter = {key} Count = {value}")


def main():
    filepath = sys.argv[1]
    f = open(filepath, "r")
    contents = f.read()
    keyword_lenght = kasiski_test(contents)
    values = prepare_data(keyword_lenght, contents)
    vigenere_test(values)


if __name__ == "__main__":
    main()
