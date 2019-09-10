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

def find_total_difference(list1, list2):
    sum = 0
    for index in range(len(list1)) : 
      sum += abs(list1[index] - list2[index])
    
    return sum

def rotate_list(old_list):  #Code provided
     new_list = old_list[:]
     new_list.append(old_list[0])
     del new_list[0]
     return new_list

def key_generator(values, key_length):

    base_dict = dict({
        "a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0, "g": 0, "h": 0, "i": 0, "j": 0, "k": 0, "l": 0, "m": 0, "n": 0, "o": 0, "p": 0, "q": 0, "r": 0, "s": 0, "t": 0, "u": 0, "v": 0, "w": 0, "x": 0, "y": 0, "z": 0
    })

    pt_freq = [.1463, .0104, .0388, .0499, .1257, .0102, .0130, .0128, .0618, .0040, .0002, .0278, .0474, .0505, .1073, .0252, .0120, .0653, .0781, .0434, .0463, .0167, .0001, .0021, .0001, .0047]

    cosets = [None]*key_length

    for i in range(key_length):
        letter_feq = base_dict.copy()
        for word in values:
            frequency_count(letter_feq, word[i])
        cosets[i] = letter_feq

    key = ""
    for coset in cosets:
        cosetFreqList = list(coset.values())
        alphaList = list(coset)
    
        differenceList = []
        for index in range(len(alphaList)) :
            differenceList.append(find_total_difference(cosetFreqList, pt_freq))
            cosetFreqList = rotate_list(cosetFreqList)

        letter_index = differenceList.index(min(differenceList))
        letter = alphaList[letter_index]
        key += letter

    return key

def vigenere_decode(ciphertext, key, alphabet):
  cipherList = list(ciphertext)
  keyList = list(key)
  alphaList = list(alphabet)
  decodeText = ""
  
  for index in range(len(ciphertext)) : 
    cipherIndex = alphabet.index(cipherList[index])
    keyIndex = alphabet.index(((keyList[index % len(key)])))
    decodeTextIndex = (cipherIndex - keyIndex) % (26)
    decodeText += alphabet[decodeTextIndex]
    
  return decodeText

def main():
    filepath = sys.argv[1]
    f = open(filepath, "r")
    contents = f.read()
    keyword_length = kasiski_test(contents)
    values = prepare_data(keyword_length, contents)
    keyword = key_generator(values, keyword_length)
    print(vigenere_decode(contents, keyword, 'abcdefghijklmnopqrstuvwxyz'))

if __name__ == "__main__":
    main()
