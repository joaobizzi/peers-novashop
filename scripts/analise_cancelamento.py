import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import logging

# ==============================================================================
# CONFIGURAÇÃO DE LOGGING
# ==============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(funcName)s] - %(message)s'
)
logger = logging.getLogger(__name__)

# ==============================================================================
# LÓGICA DE NEGÓCIO: PROCESSAMENTO DE DADOS E ANALISE ESTATISTICA
# ==============================================================================
def processar_metricas_canais(df_pedidos: pd.DataFrame, df_clientes: pd.DataFrame) -> pd.DataFrame:
    """Consolida as métricas de negócio cruzando pedidos e clientes."""
    df_merge = df_pedidos.merge(
        df_clientes[['id', 'canal_aquisicao']], 
        left_on='cliente_id', right_on='id', how='inner'
    )
    
    df_merge['foi_cancelado'] = (df_merge['status'] == 'cancelado').astype(int)
    
    analise = df_merge.groupby('canal_aquisicao').agg(
        total_pedidos=('id_x', 'count'),
        qtd_cancelados=('foi_cancelado', 'sum'),
        ticket_medio=('valor_total', 'mean')
    ).reset_index()

    analise['taxa_cancelamento_%'] = (analise['qtd_cancelados'] / analise['total_pedidos']) * 100
    return analise.sort_values('taxa_cancelamento_%', ascending=False)

# ==============================================================================
# VISUALIZAÇÃO DOS RESULTADOS (TEXTO E GRAFÍCOS)
# ==============================================================================
def imprimir_conclusao_executiva(df_analise: pd.DataFrame) -> None:
    """Gera o relatório textual para o console."""
    c_cancel = df_analise.loc[df_analise['taxa_cancelamento_%'].idxmax()]
    c_ticket = df_analise.loc[df_analise['ticket_medio'].idxmax()]

    print("\n" + "="*80)
    print("RESUMO EXECUTIVO: PERFORMANCE DE CANAIS")
    print("="*80)
    print(f"1. MAIOR TAXA DE CANCELAMENTO: O canal '{c_cancel['canal_aquisicao']}'")
    print(f"   com {c_cancel['taxa_cancelamento_%']:.1f}% de desistência.")
    
    print(f"\n2. MAIOR VALOR MÉDIO DE COMPRA: O canal '{c_ticket['canal_aquisicao']}'")
    print(f"   com ticket médio de R$ {c_ticket['ticket_medio']:.2f}.")
    print("-" * 80)
    print("="*80 + "\n")

def adicionar_labels_barras(ax: plt.Axes, sufixo: str = "", prefixo: str = "") -> None:
    """Função independente para rotular as barras dos gráficos."""
    for p in ax.patches:
        h = p.get_height()
        if h > 0:
            ax.annotate(f'{prefixo}{h:,.1f}{sufixo}'.replace('.', ','),
                        (p.get_x() + p.get_width() / 2., h),
                        ha='center', va='center', xytext=(0, 10),
                        textcoords='offset points', weight='bold')

def plotar_dash_performance(df_analise: pd.DataFrame) -> None:
    """Gera o dashboard visual de performance de canais."""
    sns.set_theme(style="white")
    plt.rcParams.update({'figure.figsize': (16, 7), 'axes.spines.top': False, 'axes.spines.right': False})
    
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle('NovaShop: Performance por Canal de Aquisição', fontsize=18, weight='black', y=1.05)

    # Grafico 1: Cancelamento
    sns.barplot(
        x='canal_aquisicao', 
        y='taxa_cancelamento_%', 
        data=df_analise, 
        ax=ax1, 
        palette='flare',
        hue='canal_aquisicao',
        legend=False
    )
    ax1.set_title('Taxa de Cancelamento (%)')
    adicionar_labels_barras(ax1, sufixo="%")

    # Grafico 2: Ticket Médio
    sns.barplot(
        x='canal_aquisicao', 
        y='ticket_medio', 
        data=df_analise, 
        ax=ax2, 
        palette='viridis',
        hue='canal_aquisicao',
        legend=False
    )
    ax2.set_title('Valor Médio de Compra (R$)')
    adicionar_labels_barras(ax2, prefixo="R$ ")

    plt.tight_layout()
    plt.show()

# ==============================================================================
# ORQUESTRADOR PRINCIPAL
# ==============================================================================
def analisar_performance_por_canal(df_pedidos: pd.DataFrame, df_clientes: pd.DataFrame) -> None:
    """Função principal que coordena a análise de canais."""
    try:
        analise = processar_metricas_canais(df_pedidos, df_clientes)
        imprimir_conclusao_executiva(analise)
        plotar_dash_performance(analise)
    except Exception as e:
        logger.error(f"Erro na análise de canais: {e}")

# ==============================================================================
# EXECUÇÃO DIRETA (PROIBIDA)
# ==============================================================================
if __name__ == "__main__":
    print("\n" + "!"*85)
    print("AVISO: Este módulo faz parte da biblioteca de análise da NovaShop.")
    print("Ele não deve ser executado individualmente.")
    print("Por favor, execute o sistema através do arquivo: main.py")
    print("!"*85 + "\n")