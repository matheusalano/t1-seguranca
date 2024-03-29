import sys
from math import gcd
from functools import reduce
from constants import ALPHABET, PORTUGUESE_FREQUENCY, ENGLISH_FREQUENCY


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
def prepare_data(keyword_length, contents):
    matrix_values = []
    for i in range(0, len(contents), keyword_length):
        word = split_chunk_data(i, contents, keyword_length)
        matrix_values.append(list(word))

    return matrix_values


# Contagem de frequencia das letras por posição na chave
# TODO: levar em consideração frequencia das letras em português
def frequency_count(_dict_, letter):
    if _dict_.__contains__(letter):
        _dict_.update({letter: _dict_[letter]+1})


def find_differences(freqList, lang_frequency):
    sum = 0
    totalLetters = reduce(lambda x, y: x + y, freqList)
    for index in range(len(freqList)):
        freq = (freqList[index] / totalLetters)
        sum += abs(freq - lang_frequency[index])

    return sum


def switch_head_tail(list):  # Code provided
    new_list = list[:]
    new_list.append(list[0])
    del new_list[0]
    return new_list


def key_generator(values, key_length, lang_frequency):

    base_dict = dict({
        "a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0, "g": 0, "h": 0, "i": 0,
        "j": 0, "k": 0, "l": 0, "m": 0, "n": 0, "o": 0, "p": 0, "q": 0, "r": 0,
        "s": 0, "t": 0, "u": 0, "v": 0, "w": 0, "x": 0, "y": 0, "z": 0
    })

    frequencies = [None]*key_length

    for i in range(key_length):
        letter_feq = base_dict.copy()
        for word in values:
            if i < len(word):
                frequency_count(letter_feq, word[i])
        frequencies[i] = letter_feq

    key = ""
    for freq in frequencies:
        freqList = list(freq.values())

        differenceList = []
        for index in range(len(ALPHABET)):
            differenceList.append(find_differences(freqList, lang_frequency))
            freqList = switch_head_tail(freqList)

        letter_index = differenceList.index(min(differenceList))
        letter = ALPHABET[letter_index]
        key += letter

    return key


def decoder(ciphertext, key):
    cipherList = list(ciphertext)
    keyList = list(key)
    decodeText = ""

    for index in range(len(ciphertext)):
        cipherIndex = ALPHABET.index(cipherList[index])
        keyIndex = ALPHABET.index(((keyList[index % len(key)])))
        decodeTextIndex = (cipherIndex - keyIndex) % (26)
        decodeText += ALPHABET[decodeTextIndex]

    return decodeText


def main():
    filepath = ''
    output_filepath = './output/'
    output_filename = 'decrypted.out'
    lang_frequency = None

    if len(sys.argv) == 4 and sys.argv[1] == '-l':
        filepath = sys.argv[3]
        lang_frequency = ENGLISH_FREQUENCY if sys.argv[2] == 'en_us' else PORTUGUESE_FREQUENCY

    elif len(sys.argv) == 2:
        filepath = sys.argv[1]
        lang_frequency = PORTUGUESE_FREQUENCY
    else:
        raise Exception(
            'Parameters: -l <en_us or pt_br> <file_name>\nLanguage is optional.')

    f = open(filepath, "r")
    contents = f.read()
    keyword_length = kasiski_test(contents)
    print('Keyword length: ', keyword_length)

    chunked_text = prepare_data(keyword_length, contents)
    keyword = key_generator(chunked_text, keyword_length, lang_frequency)

    print('\n\nKeyword: ', keyword)

    decoded_text = decoder(contents, keyword)

    ff = open(output_filepath + output_filename, "w+")
    ff.truncate(0)
    ff.write(decoded_text)
    ff.close()
    print('\n\nOpen ', output_filepath + output_filename)


if __name__ == "__main__":
    main()
