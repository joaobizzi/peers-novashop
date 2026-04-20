import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from scipy import stats
from typing import Tuple

# ==============================================================================
# CONFIGURAÇÃO DE LOGGING
# ==============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(funcName)s] - %(message)s'
)
logger = logging.getLogger(__name__)

# ==============================================================================
# LÓGICA DE NEGÓCIO: ESTATÍSTICA E PROCESSAMENTO
# ==============================================================================
def preparar_dados_segmentados(df_pedidos: pd.DataFrame, df_clientes: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Filtra pedidos faturados e cruza com segmentos de clientes."""
    logger.info("Filtrando pedidos válidos e cruzando com base de clientes...")
    
    status_faturados = ['entregue', 'em_transito']
    df_faturados = df_pedidos[df_pedidos['status'].isin(status_faturados)].copy()

    df_faturados = df_faturados.merge(
        df_clientes[['id', 'segmento']], 
        left_on='cliente_id', 
        right_on='id', 
        how='inner'
    )
    
    metricas = df_faturados.copy()
    metricas = metricas.groupby('segmento')['valor_total'].agg(
        ['mean', 'count', 'std']
    ).reset_index()
    metricas.columns = ['Segmento', 'Ticket Médio (R$)', 'Total de Pedidos', 'Desvio Padrão']

    return df_faturados, metricas

def realizar_teste_estatistico(df: pd.DataFrame) -> Tuple[float, float]:
    """Calcula o Teste T tratando possíveis erros de dados."""
    logger.info("Realizando teste de hipótese (T-Test)...")
    
    b2b = df[df['segmento'] == 'B2B']['valor_total']
    b2c = df[df['segmento'] == 'B2C']['valor_total']

    if len(b2b) < 2 or len(b2c) < 2:
        logger.warning("Amostra insuficiente para Teste T. Retornando p-value 1.0")
        return 0.0, 1.0 

    t_stat, p_value = stats.ttest_ind(b2b, b2c, equal_var=False)

    if pd.isna(p_value):
        return 0.0, 1.0
        
    return t_stat, p_value

# ==============================================================================
# VISUALIZAÇÃO DOS RESULTADOS
# ==============================================================================
def plotar_distribuicao_segmentos(df_metricas: pd.DataFrame) -> None:
    """Exibe a distribuição de volume de pedidos por segmento (Gráfico de Pizza)."""
    plt.figure(figsize=(10, 7))
    
    cores = sns.color_palette("Pastel1")
    explode = (0.05, 0)
    
    plt.pie(
        df_metricas['Total de Pedidos'], 
        labels=df_metricas['Segmento'], 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=cores, 
        explode=explode,
        shadow=True
    )
    
    plt.title("Distribuição do Volume de Pedidos por Segmento (Entregues/Em Transito)", fontsize=14, weight='bold')
    plt.tight_layout()
    logger.info("Gráfico de pizza gerado.")
    plt.show()

def exibir_conclusao_consultiva(df_metricas: pd.DataFrame, p_value: float) -> None:
    """Apresenta os resultados com foco em tomada de decisão estratégica."""
    print("\n" + "="*70)
    print("ANÁLISE ESTATÍSTICA: PERFORMANCE B2B VS B2C")
    print("="*70)

    print("\nTicket médio considera apenas pedidos entregues e em_transito")
    print("Cancelados são excluídos pois não representam vendas concluídas")
    print("Devolvidos são excluídos para não distorcer o comportamento de compra\n")
    
    pd.options.display.float_format = lambda x: f'{x:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    print(df_metricas.to_string(index=False))
    
    print("\n" + "-"*70)
    print(f"RESULTADO DO TESTE T (P-Value): {p_value:.4f}\n")
    
    if p_value < 0.05:
        print("CONCLUSÃO: Diferença ESTATISTICAMENTE RELEVANTE encontrada.")
        print("Insight: O segmento com maior Ticket Médio possui um comportamento de")
        print("compra distinto, sugerindo estratégias de marketing diferenciadas.")
    else:
        print("CONCLUSÃO: Diferença NÃO é estatisticamente relevante.")
        print("Insight: Apesar das médias numéricas diferentes, a variação interna")
        print("dos grupos indica que os segmentos se comportam de forma similar.")
    print("="*70 + "\n")

# ==============================================================================
# ORQUESTRADOR PRINCIPAL
# ==============================================================================
def analisar_ticket_medio_por_segmento(df_pedidos: pd.DataFrame, df_clientes: pd.DataFrame) -> None:
    """Orquestra a análise de ticket médio e relevância estatística."""
    try:
        df_consolidado, metricas = preparar_dados_segmentados(df_pedidos, df_clientes)
        _, p_value = realizar_teste_estatistico(df_consolidado)
        
        exibir_conclusao_consultiva(metricas, p_value)
        plotar_distribuicao_segmentos(metricas)
    except Exception as e:
        logger.error(f"Erro ao analisar ticket médio: {e}")

# ==============================================================================
# EXECUÇÃO DIRETA (PROIBIDA)
# ==============================================================================
if __name__ == "__main__":
    print("\n" + "!"*85)
    print("AVISO: Este módulo faz parte da biblioteca de análise da NovaShop.")
    print("Ele não deve ser executado individualmente.")
    print("Por favor, execute o sistema através do arquivo: main.py")
    print("!"*85 + "\n")
