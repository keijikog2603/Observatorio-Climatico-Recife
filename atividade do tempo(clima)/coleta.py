import requests
import json
from pathlib import Path
from datetime import datetime
import pandas as pd

cidade = "Recife"
estado = "Pernambuco"
latitude = -8.0476
longitude = -34.8770
data_inicial = "2022-05-25"
data_final = "2022-06-23"

url = "https://archive-api.open-meteo.com/v1/archive"

parametros = {
    "latitude": latitude,
    "longitude": longitude,
    "start_date": data_inicial,
    "end_date": data_final,

    "daily": [
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum"
    ],

    "timezone": "America/Recife"
}

resposta = requests.get(
    url,
    params=parametros,
    timeout=60
)
resposta.raise_for_status()
print("Status:", resposta.status_code)

dados = resposta.json()
data_hora_coleta = datetime.now().astimezone()

print("Data e hora da coleta:", data_hora_coleta)

df = pd.DataFrame(dados["daily"])
df = df.rename(columns={
    "time": "data",
    "temperature_2m_max": "temperatura_maxima",
    "temperature_2m_min": "temperatura_minima",
    "precipitation_sum": "precipitacao"
})
df["data"] = pd.to_datetime(df["data"])
df["temperatura_maxima"] = pd.to_numeric(
    df["temperatura_maxima"]
)
df["temperatura_minima"] = pd.to_numeric(
    df["temperatura_minima"]
)
df["precipitacao"] = pd.to_numeric(
    df["precipitacao"]
)

pasta_dados = Path("dados")
pasta_dados.mkdir(exist_ok=True)

arquivo_json = pasta_dados / "recife_dados_originais.json"

metadados = {
    "cidade": cidade,
    "estado": estado,
    "latitude": latitude,
    "longitude": longitude,
    "data_inicial": data_inicial,
    "data_final": data_final,
    "fuso_horario": "America/Recife",
    "data_hora_coleta": str(data_hora_coleta),
    "variaveis": [
        "temperatura_maxima",
        "temperatura_minima",
        "precipitacao"
    ],
    "fonte": "Open-Meteo Historical Weather API"
}

arquivo_metadados = pasta_dados / "metadados_coleta.json"

with open(arquivo_metadados, "w", encoding="utf-8") as arquivo:
    json.dump(metadados, arquivo, ensure_ascii=False, indent=4)
with open(arquivo_json, "w", encoding="utf-8") as arquivo:
    json.dump(dados, arquivo, ensure_ascii=False, indent=4)

temperaturas_invalidas = df[
    df["temperatura_maxima"] < df["temperatura_minima"]
]

precipitacao_invalida = df[
    df["precipitacao"] < 0
]

print("Total de registros:", len(df))

print("Data inicial:", df["data"].min())
print("Data final:", df["data"].max())

datas_esperadas = pd.date_range(
    start=data_inicial,
    end=data_final,
    freq="D"
)
datas_faltantes = datas_esperadas.difference(df["data"])

print("Dias faltantes:", len(datas_faltantes))
print("Temperaturas inconsistentes:", len(temperaturas_invalidas))
print("Precipitações negativas:", len(precipitacao_invalida))
print(dados.keys())
print(dados["daily"])
print(df.head())
print(df.dtypes)
print(df.isnull().sum())
print("Registros duplicados:", df.duplicated().sum())
print("Datas duplicadas:", df["data"].duplicated().sum())
print("Arquivo JSON salvo com sucesso!")


arquivo_csv = pasta_dados / "recife_dados_tratados.csv"
df.to_csv(
    arquivo_csv,
    index=False,
    encoding="utf-8-sig"
)
print("Tabela tratada salva com sucesso!")