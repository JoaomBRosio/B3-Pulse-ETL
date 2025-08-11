# B3 Pulse Etl

## Descrição do Projeto
Este projeto é uma aplicação ETL (Extração, Transformação e Carga) que processa dados da B3 (Bolsa de Valores do Brasil). Ele permite a extração de dados de arquivos ZIP, transformação desses dados em um formato utilizável, análise de retornos de ações e gerenciamento de uma carteira de ações favoritas.

## Estrutura do Projeto
```
b3pulse-etl
├── src
│   ├── main.py               # Ponto de entrada da aplicação com menu interativo
│   ├── etl
│   │   ├── extract.py        # Função para extrair arquivos de um ZIP
│   │   ├── transform.py      # Função para transformar arquivos de texto em DataFrame do pandas
│   │   ├── load.py           # Função para salvar DataFrame em formato Parquet
│   │   └── spark_transform.py # Funções para transformação de dados usando PySpark
│   ├── analysis
│   │   └── analytics.py      # Função para calcular os maiores retornos de ações
│   ├── portfolio
│   │   ├── manager.py        # Gerenciamento da carteira de ações do usuário
│   │   └── user_data.json    # Armazenamento dos dados da carteira em formato JSON
│   └── types
│       └── index.py          # Definições de tipos e interfaces
├── data
│   ├── raw                   # Diretório para arquivos brutos extraídos
│   ├── extracted             # Diretório para arquivos extraídos do ZIP
│   └── processed             # Diretório para arquivos processados (como Parquet)
├── requirements.txt          # Lista de dependências do projeto
├── README.md                 # Documentação do projeto
└── .gitignore                # Arquivos e diretórios a serem ignorados pelo Git
```

---

### O que se usa no projeto?

No projeto foram utilizadas as seguintes bibliotecas e tecnologias:

- **PySpark** (pyspark.sql, SparkSession, funções SQL)
- **Pandas** (manipulação de DataFrames)
- **JSON** (armazenamento de dados do usuário)
- **Parquet** (formato de arquivo para dados processados)
- **Python padrão** (`os`, `zipfile`, etc. para manipulação de arquivos e diretórios)

---

# Como o projeto funciona?

### Funcionamento Geral

1. **Extração**  
   - O usuário escolhe extrair arquivos ZIP da B3.
   - Função: `extract_zip`  
   - Chamada em `main.py` quando o usuário seleciona a opção de extração.
   - Resultado: Os arquivos `.ZIP` de raw são extraídos para extracted.

2. **Transformação**  
   - O usuário escolhe transformar os arquivos TXT extraídos em DataFrames.
   - Função: `parse_b3_file`  
   - Chamada em `main.py` na opção de transformação.
   - Resultado: Os arquivos TXT de extracted são convertidos em DataFrames.

3. **Carga**  
   - O usuário salva os DataFrames em formato Parquet.
   - Função: `save_to_parquet`  
   - Chamada em `main.py` após a transformação.
   - Resultado: Os DataFrames são salvos em processed.

4. **Análise**  
   - O usuário acessa o menu de análise para visualizar retornos.
   - Funções:  
     - `show_top_returns_spark`  
     - `show_bottom_returns_spark`  
     - `join_and_analyze_spark`  
   - Chamada em `main.py` dentro do menu de análise.
   - Resultado: Exibe os maiores/menores retornos das ações usando PySpark.

5. **Gerenciamento de Carteira**  
   - O usuário pode gerenciar sua carteira de ações favoritas.
   - Funções: `add_to_portfolio`, `remove_from_portfolio`, etc.  
   - Chamada em `main.py` quando o usuário acessa o menu de carteira.
   - Resultado: Dados salvos em `user_data.json`.

### Comunicação

- O arquivo principal `main.py` faz a orquestração, exibindo menus e chamando funções dos módulos de ETL, análise e carteira.
- Cada módulo tem funções específicas:
  - `extract.py`: extração de ZIP.
  - `transform.py`: transformação de TXT para DataFrame.
  - `load.py`: salva DataFrame em Parquet.
  - `spark_transform.py`: análise com PySpark.
  - `analytics.py`: cálculos de retornos.
  - `manager.py`: operações de carteira.

### Fluxo de Chamadas

- Usuário interage com o menu em `main.py`.
- Dependendo da opção, funções dos módulos são chamadas.
- Dados fluem entre os diretórios raw, extracted, processed.
- Resultados e dados de usuário são salvos em Parquet ou JSON.

### Resumo

- **Entrada:** Menu interativo em `main.py`.
- **Processamento:** Funções distribuídas nos módulos de ETL, análise e carteira.
- **Saída:** Dados processados em Parquet, análises exibidas, carteira salva em JSON.

---

## Explicando as suas funções

### 1. **extract_zip**  
- **Local:** extract.py  
- **Função:**  
  Extrai arquivos `.ZIP` da pasta raw para a pasta extracted.
- **Como é chamada:**  
  Pelo menu de extração em `main.py`.
- **Exemplo de uso:**  
  ```python
  extract_zip('data/raw/COTAHIST_A2024.ZIP', 'data/extracted/')
  ```

---

### 2. **parse_b3_file**  
- **Local:** transform.py  
- **Função:**  
  Lê o arquivo `.TXT` extraído e transforma em DataFrame (pandas ou spark).
- **Como é chamada:**  
  Pelo menu de transformação em `main.py`.
- **Exemplo de uso:**  
  ```python
  df = parse_b3_file('data/extracted/COTAHIST_A2024.TXT')
  ```

---

### 3. **save_to_parquet**  
- **Local:** load.py  
- **Função:**  
  Salva o DataFrame processado em formato `.parquet` na pasta processed.
- **Como é chamada:**  
  Após a transformação, em `main.py`.
- **Exemplo de uso:**  
  ```python
  save_to_parquet(df, 'data/processed/b3_2024.parquet')
  ```

---

### 4. **show_top_returns_spark**  
- **Local:** spark_transform.py  
- **Função:**  
  Analisa os dados processados e mostra as ações com maiores retornos usando PySpark.
- **Como é chamada:**  
  Pelo menu de análise em `main.py`.
- **Exemplo de uso:**  
  ```python
  show_top_returns_spark('data/processed/b3_2024.parquet')
  ```

---

### 5. **add_to_portfolio**  
- **Local:** manager.py  
- **Função:**  
  Adiciona uma ação à carteira do usuário, salva em `user_data.json`.
- **Como é chamada:**  
  Pelo menu de carteira em `main.py`.
- **Exemplo de uso:**  
  ```python
  add_to_portfolio('PETR4')
  ```

---

## Funções

### 1. **show_top_returns_spark**

- **O que faz:**  
  Mostra as ações com maiores retornos percentuais em um período.
- **Como funciona:**  
  1. Cria uma sessão Spark.
  2. Lê o arquivo Parquet com os dados das ações.
  3. Converte a coluna data para o tipo data.
  4. Cria uma tabela temporária chamada `b3` para usar SparkSQL.
  5. Executa uma query SQL que:
     - Agrupa por `ticker` (código da ação).
     - Calcula o preço de fechamento inicial (`first(preco_fechamento)`) e final (`last(preco_fechamento)`).
     - Calcula o rendimento percentual:  
       `((preco_fim - preco_inicio) / preco_inicio) * 100`
     - Ordena do maior para o menor rendimento.
     - Limita ao número `n` de resultados.
  6. Exibe o resultado.

---

### 2. **show_bottom_returns_spark**

- **O que faz:**  
  Mostra as ações com menores retornos percentuais (piores desempenhos).
- **Como funciona:**  
  Igual à função anterior, mas ordena do menor para o maior rendimento.

---

### 3. **join_and_analyze_spark**

- **O que faz:**  
  Compara o rendimento das ações entre dois anos (2024 e 2025).
- **Como funciona:**  
  1. Cria uma sessão Spark.
  2. Lê dois arquivos Parquet: um para 2024 e outro para 2025.
  3. Converte a coluna data para tipo data em ambos.
  4. Para cada ação (`ticker`):
     - Obtém a última data e preço de fechamento de 2024 (`spark_max`).
     - Obtém a primeira data e preço de fechamento de 2025 (`spark_min`).
  5. Faz um **join** entre os dois DataFrames pelo `ticker`:
     - Assim, para cada ação, junta o último preço de 2024 com o primeiro de 2025.
  6. Calcula o rendimento percentual entre esses dois preços.
  7. Ordena conforme o parâmetro `ordem` (`desc` para maiores, `asc` para menores).
  8. Exibe os `n` resultados.

### Join

- **O que é:**  
  Combina dados de dois DataFrames pelo campo `ticker`.
- **Como é feito:**  
  - Usa `join` do Spark:  
    ```python
    joined = last_2024.join(first_2025, on="ticker", how="inner")
    ```
  - Assim, para cada ação, junta o último preço de 2024 com o primeiro de 2025.

### Funções de agregação

- **first / last:**  
  Pega o primeiro e último valor de uma coluna para cada grupo.
- **max / min:**  
  Pega o maior ou menor valor (usado para datas e preços).
