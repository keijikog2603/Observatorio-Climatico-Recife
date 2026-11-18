import duckdb
import pandas as pd
from pathlib import Path

pasta_dados = Path("dados")
arquivo_csv = pasta_dados/"recife_dados_tratados.csv"
arquivo_banco = pasta_dados/"observatorio_climatico.duckb"

df = pd.read_csv(arquivo_csv)

print("Dados carregados:")
print(df.head())
print("Total de registros:", len(df))

conexao = duckdb.connect(str(arquivo_banco))
conexao.execute("""
    CREATE TABLE IF NOT EXISTS dados_climaticos (
        data DATE PRIMARY KEY,
        temperatura_maxima DOUBLE,
        temperatura_minima DOUBLE,
        precipitacao DOUBLE
    )
""")

conexao.register("dados_temporarios", df)
conexao.execute("""
    INSERT INTO dados_climaticos
    SELECT *
    FROM dados_temporarios
    ON CONFLICT (data) DO NOTHING
""")
conexao.unregister("dados_temporarios")

resultado = conexao.execute("""
    SELECT * FROM dados_climaticos
    ORDER BY data
""").fetchdf()

print("Dados armazenados no DuckDB:")
print(resultado)
print("Total de registros no banco:", len(resultado))

total = conexao.execute("""
    SELECT COUNT(*)
    FROM dados_climaticos
""").fetchone()[0]

print("Total de registros no banco:", total)

conexao.close()

print("Banco de dados fechado com sucesso!")