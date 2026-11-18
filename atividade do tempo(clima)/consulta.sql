COPY (
    SELECT
        SUM(precipitacao) AS precipitacao_total
    FROM dados_climaticos
)
TO 'dados/precipitacao_total.csv'
(HEADER, DELIMITER ',', OVERWRITE_OR_IGNORE true);

COPY (
    SELECT
        data,
        precipitacao
    FROM dados_climaticos
    ORDER BY precipitacao DESC
    LIMIT 5
)
TO 'dados/cinco_maiores_chuvas.csv'
(HEADER, DELIMITER ',', OVERWRITE_OR_IGNORE true);

COPY (
    SELECT
        AVG(temperatura_maxima) AS media_temperatura_maxima,
        AVG(temperatura_minima) AS media_temperatura_minima,
        MAX(temperatura_maxima) AS maior_temperatura,
        MIN(temperatura_minima) AS menor_temperatura
    FROM dados_climaticos
)
TO 'dados/analise_temperaturas.csv'
(HEADER, DELIMITER ',', OVERWRITE_OR_IGNORE true);

COPY (
    SELECT
        SUM(precipitacao) AS precipitacao_total,
        AVG(precipitacao) AS media_diaria,
        MAX(precipitacao) AS maior_precipitacao,
        COUNT(CASE WHEN precipitacao > 0 THEN 1 END) AS dias_com_chuva,
        COUNT(CASE WHEN precipitacao = 0 THEN 1 END) AS dias_sem_chuva
    FROM dados_climaticos
)
TO 'dados/resumo_precipitacao.csv'
(HEADER, DELIMITER ',', OVERWRITE_OR_IGNORE true);

COPY (
    SELECT
        data,
        precipitacao,
        CASE
            WHEN precipitacao = 0 THEN 'Sem chuva'
            WHEN precipitacao <= 10 THEN 'Chuva fraca'
            WHEN precipitacao <= 30 THEN 'Chuva moderada'
            ELSE 'Chuva intensa'
        END AS classificacao
    FROM dados_climaticos
    ORDER BY precipitacao DESC
)
TO 'dados/classificacao_chuvas.csv'
(HEADER, DELIMITER ',', OVERWRITE_OR_IGNORE true);

COPY (
    WITH dias_chuvosos AS (
        SELECT
            data,
            data - CAST(
                ROW_NUMBER() OVER (ORDER BY data) AS INTEGER
            ) AS grupo
        FROM dados_climaticos
        WHERE precipitacao > 0
    )

    SELECT
        COALESCE(MAX(quantidade_dias), 0) AS maior_sequencia_chuvosa
    FROM (
        SELECT
            grupo,
            COUNT(*) AS quantidade_dias
        FROM dias_chuvosos
        GROUP BY grupo
    ) AS sequencias
)
TO 'dados/sequencia_chuvosa.csv'
(HEADER, DELIMITER ',', OVERWRITE_OR_IGNORE true);