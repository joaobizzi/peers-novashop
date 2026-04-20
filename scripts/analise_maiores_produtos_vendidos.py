import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
# ESTILIZAÇÃO VISUAL
# ==============================================================================
def configurar_estilo_grafico() -> None:
    """Define o padrão visual para os relatórios."""
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        'figure.figsize': (14, 8),
        'axes.titlesize': 16,
        'axes.titleweight': 'bold',
        'axes.labelweight': 'bold'
    })

# ==============================================================================
# LÓGICA DE NEGÓCIO: CALCULO DO RANKING DE PRODUTOS E RENTABILIDADE
# ==============================================================================
def calcular_metricas_produtos(df_itens: pd.DataFrame, df_produtos: pd.DataFrame, df_pedidos: pd.DataFrame) -> pd.DataFrame:
    """Calcula volume, receita bruta e receita líquida (margem) por produto, ignorando cancelados/devolvidos."""
    logger.info("Iniciando cálculo de rentabilidade por produto (apenas pedidos válidos)...")
    
    pedidos_validos_ids = df_pedidos[~df_pedidos['status'].isin(['cancelado', 'devolvido'])]['id']
    df_itens_filtrado = df_itens[df_itens['pedido_id'].isin(pedidos_validos_ids)].copy()

    df_detalhado = df_itens_filtrado.merge(
        df_produtos[['id', 'nome', 'custo_unitario']], 
        left_on='produto_id', 
        right_on='id',
        how='left'
    )
    
    df_detalhado['receita_bruta_item'] = df_detalhado['quantidade'] * df_detalhado['preco_praticado']
    df_detalhado['receita_liquida_item'] = df_detalhado['quantidade'] * (df_detalhado['preco_praticado'] - df_detalhado['custo_unitario'])
    
    ranking = df_detalhado.groupby(['produto_id', 'nome']).agg(
        quantidade_total=('quantidade', 'sum'),
        receita_bruta=('receita_bruta_item', 'sum'),
        receita_liquida=('receita_liquida_item', 'sum')
    ).reset_index()
    
    return ranking.sort_values(by='quantidade_total', ascending=False)

# ==============================================================================
# VISUALIZAÇÃO DOS RESULTADOS
# ==============================================================================
def plotar_ranking_dual(df_top: pd.DataFrame) -> None:
    """Compara o volume vendido com a Receita."""
    configurar_estilo_grafico()
    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_xlabel('Produtos')
    ax1.set_ylabel('Quantidade Vendida', color=color)
    sns.barplot(x='nome', y='quantidade_total', data=df_top, ax=ax1, color=color, alpha=0.6)
    ax1.tick_params(axis='y', labelcolor=color)
    plt.xticks(rotation=45, ha='right')

    ax2 = ax1.twinx()
    color = 'tab:green'
    ax2.set_ylabel('Receita Líquida Total (R$)', color=color)
    sns.lineplot(x='nome', y='receita_liquida', data=df_top, ax=ax2, color=color, marker='o', linewidth=3)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Top 10 Produtos: Volume de Vendas vs. Rentabilidade Líquida')
    fig.tight_layout()
    logger.info("Visualização de rentabilidade gerada.")
    plt.show()

def exibir_relatorio_console(df_top: pd.DataFrame, top_n: int) -> None:
    """Formata e imprime o ranking de produtos no console."""
    print("\n" + "="*85)
    print(f"ANÁLISE DE PRODUTOS: TOP {top_n} POR VOLUME E PERFORMANCE FINANCEIRA")
    print("="*85)
    
    exibicao = df_top[['nome', 'quantidade_total', 'receita_bruta', 'receita_liquida']].copy()
    exibicao.columns = ['Produto', 'Qtd Vendida', 'Rec. Bruta (R$)', 'Rec. Líquida (R$)']
    
    pd.options.display.float_format = '{:,.2f}'.format
    print(exibicao.to_string(index=False))
    print("-" * 85)

# ==============================================================================
# ORQUESTRADOR PRINCIPAL
# ==============================================================================
def analisar_produtos_mais_vendidos(
    df_itens: pd.DataFrame, 
    df_produtos: pd.DataFrame, 
    df_pedidos: pd.DataFrame,
    top_n: int = 10
) -> None:
    """Orquestra a análise de produtos: Cálculo -> Relatório -> Gráfico."""
    try:
        logger.info(f"Iniciando pipeline de análise para os top {top_n} itens...")
        df_ranking = calcular_metricas_produtos(df_itens, df_produtos, df_pedidos)
        df_top_n = df_ranking.head(top_n).copy()
        exibir_relatorio_console(df_top_n, top_n)
        plotar_ranking_dual(df_top_n)
    except Exception as e:
        logger.error(f"Falha na execução do pipeline de produtos: {e}")

# ==============================================================================
# EXECUÇÃO DIRETA (PROIBIDA)
# ==============================================================================
if __name__ == "__main__":
    print("\n" + "!"*85)
    print("AVISO: Este módulo faz parte da biblioteca de análise da NovaShop.")
    print("Ele não deve ser executado individualmente.")
    print("Por favor, execute o sistema através do arquivo: main.py")
    print("!"*85 + "\n")
