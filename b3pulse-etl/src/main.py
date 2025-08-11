from etl.extract import extract_zip
from etl.transform import parse_b3_file
from etl.load import save_to_parquet
from analysis.analytics import (
    show_top_returns_spark,
    show_bottom_returns_spark,
    join_and_analyze_spark
)
from portfolio.manager import add_stock, remove_stock, show_portfolio

def analysis_menu():
    print("\n--- ANÁLISE ---")
    print("1. Maiores rendimentos")
    print("2. Menores rendimentos")
    print("3. Ver rendimentos de uma base")
    print("4. Comparar bases (join)")
    print("0. Voltar")

if __name__ == "__main__":
    while True:
        print("\n--- MENU ---")
        print("1. Extrair arquivos B3")
        print("2. Transformar dados de 2024 e 2025 com Pandas")
        print("3. Análise de dados com SparkSQL")
        print("4. Adicionar ação à favoritos")
        print("5. Remover ação da favoritos")
        print("6. Ver favoritos")
        print("0. Sair")
        op = input("Escolha: ")

        if op == "1":
            extract_zip("data/raw/COTAHIST_A2024.ZIP", "data/extracted/")
            extract_zip("data/raw/COTAHIST_A2025.ZIP", "data/extracted/")
            print("Arquivos extraídos.")

        elif op == "2":
            df_2024 = parse_b3_file("data/extracted/COTAHIST_A2024.TXT")
            save_to_parquet(df_2024, "data/processed/b3_2024.parquet")
            df_2025 = parse_b3_file("data/extracted/COTAHIST_A2025.TXT")
            save_to_parquet(df_2025, "data/processed/b3_2025.parquet")
            print("Dados de 2024 e 2025 transformados e salvos.")

        elif op == "3":
            while True:
                analysis_menu()
                a_op = input("Escolha análise: ")
                if a_op == "1":
                    base = input("Qual base? (2024 ou 2025): ")
                    n = int(input("Quantos resultados? "))
                    parquet = f"data/processed/b3_{base}.parquet"
                    show_top_returns_spark(parquet, n)
                elif a_op == "2":
                    base = input("Qual base? (2024 ou 2025): ")
                    n = int(input("Quantos resultados? "))
                    parquet = f"data/processed/b3_{base}.parquet"
                    show_bottom_returns_spark(parquet, n)
                elif a_op == "3":
                    base = input("Qual base? (2024 ou 2025): ")
                    n = int(input("Quantos resultados? "))
                    parquet = f"data/processed/b3_{base}.parquet"
                    show_top_returns_spark(parquet, n)
                elif a_op == "4":
                    tipo = input("Comparar melhores ou piores? (m/p): ").lower()
                    n = int(input("Quantos resultados comparar? "))
                    ordem = "desc" if tipo == "m" else "asc"
                    join_and_analyze_spark("data/processed/b3_2024.parquet", "data/processed/b3_2025.parquet", n, ordem)

                elif a_op == "0":
                    break

        elif op == "4":
            ticker = input("Ticker: ").upper()
            add_stock(ticker)

        elif op == "5":
            ticker = input("Ticker: ").upper()
            remove_stock(ticker)

        elif op == "6":
            print("Sua carteira:", show_portfolio())

        elif op == "0":
            break