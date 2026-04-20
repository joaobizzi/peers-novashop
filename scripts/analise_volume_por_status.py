import logging
from typing import Optional
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================================================================
# CONFIGURAÇÃO DE LOGGING
# ==============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==============================================================================
# CONFIGURAÇÃO VISUAL
# ==============================================================================
def configurar_estilo(figsize: tuple[int, int] = (10, 6)) -> None:
    """Define a padronização visual global dos gráficos."""
    sns.set_theme(style="whitegrid")
    plt.rcParams["figure.figsize"] = figsize


# ==============================================================================
# LÓGICA DE NEGÓCIO: TRANSFORMAÇÃO DE DADOS
# ==============================================================================
def extrair_distribuicao_status(df_pedidos: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula o volume absoluto e a distribuição percentual por status.
    """
    if "status" not in df_pedidos.columns:
        raise ValueError("A coluna 'status' não foi encontrada no DataFrame.")
    df = df_pedidos.copy()
    contagem = (
        df["status"]
        .value_counts(dropna=False)
        .rename_axis("Status")
        .reset_index(name="Volume Absoluto")
    )
    total = contagem["Volume Absoluto"].sum()
    contagem["Distribuição (%)"] = (
        contagem["Volume Absoluto"] / total * 100
    )
    logger.info(
        "Distribuição de status calculada: %s registros analisados",
        total
    )
    return contagem

# ==============================================================================
# VISUALIZAÇÃO DOS RESULTADOS
# ==============================================================================
def plotar_status(df_status: pd.DataFrame, titulo: Optional[str] = None) -> None:
    """
    Gera um gráfico de barras com anotação percentual.
    """
    configurar_estilo()
    fig, ax = plt.subplots()

    sns.barplot(
        data=df_status,
        x="Status",
        y="Volume Absoluto",
        hue="Status",
        palette="viridis",
        legend=False,
        ax=ax
    )
    for i, patch in enumerate(ax.patches):
        valor = patch.get_height()
        percentual = df_status.iloc[i]["Distribuição (%)"]
        ax.annotate(
            f"{percentual:.1f}%",
            (patch.get_x() + patch.get_width() / 2, valor),
            ha="center",
            va="bottom",
            xytext=(0, 6),
            textcoords="offset points",
            fontsize=10,
            fontweight="bold"
        )
    ax.set_title(
        titulo or "Volume de Pedidos por Status",
        fontsize=14,
        fontweight="bold"
    )
    ax.set_xlabel("Status")
    ax.set_ylabel("Quantidade de Pedidos")
    plt.tight_layout()
    plt.show()

def exibir_tabela_distribuicao(df_status: pd.DataFrame) -> None:
    print("\n--- Tabela de Distribuição por Status ---")
    print(df_status.to_string(index=False))

    total = df_status["Volume Absoluto"].sum()
    print(f"\nTotal de Pedidos Analisados: {total}")

# ==============================================================================
# ORQUESTRADOR PRINCIPAL
# ==============================================================================
def analisar_status(df: pd.DataFrame) -> None:
    """
    Orquestra a análise de volume por status do pedido.
    """
    df_status = extrair_distribuicao_status(df)
    exibir_tabela_distribuicao(df_status)
    plotar_status(df_status)

# ==============================================================================
# EXECUÇÃO DIRETA (PROIBIDA)
# ==============================================================================
if __name__ == "__main__":
    print("\n" + "!"*85)
    print("AVISO: Este módulo faz parte da biblioteca de análise da NovaShop.")
    print("Ele não deve ser executado individualmente.")
    print("Por favor, execute o sistema através do arquivo: main.py")
    print("!"*85 + "\n")