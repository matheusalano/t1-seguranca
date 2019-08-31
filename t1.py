from math import gcd
from functools import reduce

def kasiski_test(text):

    tris = []
    distances = []

    #Salva os trigramas e a distancia entre eles
    for i in range(len(text) - 2):
        tri = text[i:i + 3]
        
        if tri in tris:
            last_idx = text.rfind(tri, 0, i)
            distances.append(i - last_idx)
        else:
            tris.append(tri)

    occur_count = {}

    #Conta o numero de ocorrencias de cada distancia encontrada e salva em um dicionario
    for d in distances:
        if d not in occur_count:
            occur_count[d] = 1
        else:
            occur_count[d] += 1
    
    #Ordena esse dicionario ao contrário pela numero de ocorrencias
    occur_count =  sorted(occur_count.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)   
    #Salva apenas as 20 distancias com maior ocorrencia
    occur_count = occur_count[:20]
    
    distances = list(map(lambda x: x[0], occur_count))
    
    #Retorna o MDC dessas distancias
    return reduce(lambda x,y:gcd(x,y),distances)
    
if __name__ == "__main__":
    
    f = open("DemCifrado.txt", "r")
    contents = f.read()
    print(kasiski_test(contents))
    

    