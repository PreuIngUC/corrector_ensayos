import pandas as pd
import numpy as np
##B
archivo = "m1.csv"
df = pd.read_csv(archivo)

respuestas_correctas = [
    "C","C","D","A","B","C","D","A","D","D","A","B","A","B","D","A",
    "C","D","B","C","B",None,"A","D","D",None,"B","D","B","D","C","D"
]

preguntas_anuladas = [22, 26]

# Escala DEMRE original 0 a 60
escala_demre = {
    0:100, 1:190, 2:214, 3:235, 4:256, 5:275, 6:293, 7:308,
    8:323, 9:337, 10:353, 11:369, 12:383, 13:396, 14:406,
    15:415, 16:425, 17:437, 18:451, 19:465, 20:479, 21:489,
    22:497, 23:504, 24:511, 25:519, 26:530, 27:544, 28:558,
    29:571, 30:582, 31:590, 32:596, 33:603, 34:611, 35:621,
    36:634, 37:648, 38:662, 39:674, 40:683, 41:691, 42:700,
    43:710, 44:723, 45:738, 46:753, 47:767, 48:780, 49:792,
    50:806, 51:822, 52:839, 53:858, 54:877, 55:896, 56:918,
    57:942, 58:968, 59:997, 60:1000
}

def convertir_puntaje(correctas, max_validas=30):
    """
    Ajusta las correctas válidas a la escala DEMRE de 60 preguntas.
    Como aquí hay 30 preguntas válidas, 30 correctas equivale a 60 DEMRE.
    """
    correctas_equivalentes = round((correctas / max_validas) * 60)
    return escala_demre.get(correctas_equivalentes, 100)

resultados = []

for i, fila in df.iterrows():
    correctas = 0
    malas = 0
    omitidas_validas = 0
    anuladas_respondidas = 0
    total_respondidas = 0

    for n in range(1, 33):
        col = f"p{n}"
        respuesta = fila[col] if col in df.columns else np.nan

        if pd.notna(respuesta) and str(respuesta).strip() != "":
            total_respondidas += 1
            respuesta = str(respuesta).strip().upper()
        else:
            respuesta = ""

        if n in preguntas_anuladas:
            if respuesta != "":
                anuladas_respondidas += 1
            continue

        correcta = respuestas_correctas[n - 1]

        if respuesta == "":
            omitidas_validas += 1
        elif respuesta == correcta:
            correctas += 1
        else:
            malas += 1

    if total_respondidas > 32:
        puntaje = 100
        observacion = "CONTESTA AL AZAR, SE NOTAN INCONCORDANCIAS"
    else:
        puntaje = convertir_puntaje(correctas)
        observacion = ""

    resultados.append({
        "ID": i + 1,
        "CANTIDAD DE CORRECTAS": correctas,
        "CANTIDAD DE MALAS": malas,
        "OMITIDAS VALIDAS": omitidas_validas,
        "ANULADAS RESPONDIDAS": anuladas_respondidas,
        "PUNTAJE TOTAL": puntaje,
        "OBSERVACION": observacion
    })

df_resultado = pd.DataFrame(resultados)

df_resultado.to_csv("m1_corregido.csv", index=False)
df_resultado.to_excel("m1_corregido.xlsx", index=False)