# Observatorio-Climatico-Recife

## Sobre o projeto

O Observatório Climático Local é um projeto acadêmico que realiza a coleta, o tratamento, o armazenamento e a análise de dados meteorológicos históricos do município do Recife, Pernambuco.

O objetivo é identificar padrões de precipitação e variações de temperatura, transformando dados meteorológicos em informações organizadas que possam contribuir para a compreensão dos períodos de chuvas intensas na região.

**Público-alvo:**
- Moradores do Recife, especialmente de regiões afetadas por chuvas intensas.
- Estudantes e pesquisadores.
- Pessoas interessadas em informações meteorológicas.

## Fonte dos dados

Os dados são obtidos por meio da API histórica Open-Meteo.

Fonte: https://open-meteo.com/

**Localidade:** Recife — Pernambuco, Brasil.

**Coordenadas:**
- Latitude: -8.0476
- Longitude: -34.8770

**Período analisado:** 25/05/2022 a 23/06/2022.

**Quantidade:** 30 dias consecutivos.

**Fuso horário:** America/Recife.

### Variáveis utilizadas

| Variável | Descrição | Unidade |
|---|---|---|
| temperature_2m_max | Temperatura máxima diária | °C |
| temperature_2m_min | Temperatura mínima diária | °C |
| precipitation_sum | Precipitação diária acumulada | mm |

## Tecnologias utilizadas

- Python: coleta e processamento dos dados.
- Requests: comunicação com a API.
- Pandas: tratamento e organização dos registros.
- DuckDB: armazenamento dos dados.
- SQL: consultas e análises.

## Preparação do ambiente

É necessário ter o Python instalado.

Instale as dependências com:

```bash
pip install -r requirements.txt
```

As principais bibliotecas utilizadas são:

- requests
- pandas
- duckdb

## Ordem de execução

Execute os arquivos na seguinte ordem:

**1. Coleta dos dados**

```bash
python coleta.py
```

Esse programa acessa a API Open-Meteo, coleta os dados meteorológicos e gera os arquivos JSON e CSV na pasta `dados/`.

**2. Tratamento e armazenamento**

```bash
python banco.py
```

Esse programa realiza o tratamento e a validação dos dados e os armazena no banco DuckDB.

**3. Execução das consultas SQL**

```bash
python -c "import duckdb; c=duckdb.connect('dados/observatorio_climatico.duckdb'); c.execute(open('consultas.sql', encoding='utf-8').read()); c.close(); print('Consultas executadas!')"
```

As consultas geram arquivos com os resultados das análises.

## Banco de dados

O projeto utiliza o DuckDB para armazenar os registros meteorológicos.

A tabela principal é chamada `dados_climaticos` e possui os seguintes campos:

| Campo | Descrição |
|---|---|
| data | Data do registro |
| temperatura_maxima | Temperatura máxima diária |
| temperatura_minima | Temperatura mínima diária |
| precipitacao | Precipitação diária acumulada |

A coluna `data` funciona como chave primária para evitar registros duplicados durante novas execuções.

## Resultados principais

Durante os 30 dias analisados, foram encontrados:

- Precipitação total: 521,5 mm.
- Dias com chuva: 28.
- Dias sem chuva: 2.
- Média diária de precipitação: 17,38 mm.
- Maior precipitação diária: 120,3 mm, em 28/05/2022.
- Temperatura máxima média: 26,64 °C.
- Temperatura mínima média: 22,35 °C.

## Limitações

A análise considera somente 30 dias consecutivos e três variáveis meteorológicas.

Os dados históricos da Open-Meteo podem ser provenientes de modelos meteorológicos e reanálises, não representando necessariamente medições diretas de uma estação meteorológica local.

Os resultados possuem finalidade histórica e informativa. Não constituem previsão meteorológica nem sistema de alerta de enchentes.

## Relatório

O relatório técnico e analítico da AE2 apresenta o processo de coleta, tratamento, armazenamento, consultas SQL, indicadores e interpretação dos resultados.

O documento está disponível neste repositório.
