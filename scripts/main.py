import logging
import sys

# Importação dos módulos
from limpar_dados import processar_pipeline
from analise_cancelamento import analisar_performance_por_canal
from analise_temporal import analisar_evolucao_temporal
from analise_volume_por_status import analisar_status
from analise_maiores_produtos_vendidos import analisar_produtos_mais_vendidos
from analise_ticket_medio_por_segmento import analisar_ticket_medio_por_segmento

# ==============================================================================
# CONFIGURAÇÃO DE LOGGING
# ==============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==============================================================================
# INTERFACE DE USUÁRIO (TEXTOS E ESTÉTICA)
# ==============================================================================
def exibir_cabecalho():
    print("\n" + "="*60)
    print("       NOVASHOP DIGITAL CONSULTING - PEERS GROUP")
    print("="*60)
    print("Pipeline de Dados e Análises Estratégicas (2023-2024)")
    print("-"*60)

def exibir_menu():
    print("\n[ SELECIONE UMA ANÁLISE ]")
    print("1. Volume de Pedidos por Status (Questão 1)")
    print("2. Top 10 Produtos e Receita (Questão 2)")
    print("3. Ticket Médio por Segmento: B2C vs B2B (Questão 3)")
    print("4. Evolução Temporal e Sazonalidade (Questão 4)")
    print("5. Performance por Canal de Aquisição (Questão 5)")
    print("6. Sobre o tratamento dos dados (Questão 6)")
    print("0. Sair do Sistema")
    print("-"*60)

def confirmar_execucao() -> bool:
    """Solicita confirmação do usuário para continuar."""
    while True:
        resposta = input("Deseja continuar com o tratamento dos dados? (s/n): ").strip().lower()
        if resposta in ("s", "sim"):
            return True
        elif resposta in ("n", "nao", "não"):
            return False
        else:
            print("[!] Entrada inválida. Digite 's' para sim ou 'n' para não.")

# ==============================================================================
# ORQUESTRADOR PRINCIPAL
# ==============================================================================
def main():
    exibir_cabecalho()

    if not confirmar_execucao():
        print("\nOperação cancelada pelo usuário.")
        return
    
    logger.info("Iniciando processamento e tratamento de dados...")

    try:
        dfs = processar_pipeline()
        if not dfs:
            logger.error("Falha ao carregar DataFrames. Encerrando.")
            return
    except Exception as e:
        logger.error(f"Erro crítico no pipeline: {e}")
        sys.exit(1)

    while True:
        exibir_menu()
        opcao = input("Digite a opção desejada: ")
        try:
            match opcao:
                case "1":
                    print("\n>>> Processando Questão 1: Qual o volume de pedidos por status? Calcule a distribuição percentual e " \
                            "apresente os resultados em uma tabela. Inclua uma visualização gráfica (ex: gráfico de barras ou pizza).")
                    analisar_status(dfs['pedidos'])
                case "2":
                    print("\n>>> Processando Questão 2: Quais são os 10 produtos mais vendidos (por quantidade total de itens vendidos)? " \
                            "Apresente também a receita gerada por cada um deles.")
                    analisar_produtos_mais_vendidos(dfs['itens_pedido'], dfs['produtos'], dfs['pedidos'])
                case "3":
                    print("\n>>> Processando Questão 3: Qual o ticket médio de pedidos por segmento de cliente (B2C vs B2B)? Existe " \
                            "diferença estatisticamente relevante?")
                    analisar_ticket_medio_por_segmento(dfs['pedidos'], dfs['clientes'])
                case "4":
                    print("\n>>> Processando Questão 4: Analise a evolução mensal do volume de pedidos ao longo de 2023 e 2024. " \
                            "Há sazonalidade? Identifique picos e quedas e formule uma hipótese para cada padrão encontrado. ")
                    analisar_evolucao_temporal(dfs['pedidos'], dfs['tickets_suporte'])
                case "5":
                    print("\n>>> Processando Questão 5: Qual canal de aquisição de clientes apresenta a maior taxa de cancelamento " \
                                "de pedidos? E qual gera o maior valor médio de compra? Cruzar clientes → pedidos.")
                    analisar_performance_por_canal(dfs['pedidos'], dfs['clientes'])
                case "6":
                    print("\n>>> Para maiores detalhes sobre o tratamento dos dados, por favor leia o README do projeto.")                 
                case "0":
                    print("\nEncerrando sistema. Muito obrigado!")
                    break
                case _:
                    print("\n[!] Opção inválida. Tente novamente.")
        except Exception as e:
            logger.error(f"Erro ao executar a análise selecionada: {e}")

if __name__ == "__main__":
    main()
