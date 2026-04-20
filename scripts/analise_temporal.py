import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import logging
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
# ESTILIZAÇÃO VISUAL
# ==============================================================================
def configurar_estilo_temporal() -> None:
    """Configura o padrão visual"""
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        'figure.figsize': (16, 12),
        'axes.titlesize': 18,
        'axes.titleweight': 'bold',
        'axes.labelweight': 'bold',
        'legend.title_fontsize': 12
    })
    logger.info("Estilo temporal executivo configurado.")

# ==============================================================================
# LÓGICA DE NEGÓCIO: TRATAMENTO DE DADOS
# ==============================================================================
def preparar_dados_pedidos(df_pedidos: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Prepara a evolução por categoria e o consolidado total de pedidos."""
    df = df_pedidos.copy()
    df['mes_referencia'] = df['data_pedido'].dt.to_period('M').dt.to_timestamp()
    
    df['categoria_status'] = df['status'].apply(
        lambda x: 'Ativos (Entregue/Trânsito)' if x in ['entregue', 'em_transito'] else 'Cancelados/Devolvidos'
    )
    
    evolucao_status = df.groupby(['mes_referencia', 'categoria_status']).size().reset_index(name='volume')
    evolucao_total = df.groupby('mes_referencia').size().reset_index(name='volume')
    evolucao_total['categoria_status'] = 'Volume Total de Pedidos'
    
    return evolucao_status, evolucao_total

def preparar_dados_tickets(df_tickets: pd.DataFrame) -> pd.DataFrame:
    """Prepara a evolução mensal de tickets de suporte."""
    df_t = df_tickets.copy()
    df_t['mes_referencia'] = df_t['data_abertura'].dt.to_period('M').dt.to_timestamp()

    evolucao_tickets = df_t.groupby('mes_referencia').size().reset_index(name='volume_tickets')
    return evolucao_tickets

# ==============================================================================
# ESTILIZAÇÃO E VISUALIZAÇÃO
# ==============================================================================
def plotar_evolucao_temporal(df_evolucao: pd.DataFrame, df_total: pd.DataFrame, df_tickets: pd.DataFrame) -> None:
    """Gerar o grafico da evolução temporal (2023-2024)."""
    configurar_estilo_temporal()
    
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [2, 1]})

    # GRÁFICO 1: PEDIDOS
    sns.lineplot(
        data=df_evolucao, 
        x='mes_referencia', y='volume', hue='categoria_status', 
        marker='o', linewidth=2.5,
        palette={'Ativos (Entregue/Trânsito)': '#2E86C1', 'Cancelados/Devolvidos': '#E74C3C'},
        ax=ax1
    )

    sns.lineplot(
        data=df_total, 
        x='mes_referencia', y='volume', 
        marker='s', linewidth=4, color='#27AE60',
        label='Volume Total de Pedidos',
        ax=ax1
    )

    # GRÁFICO 2: TICKETS
    ax2.bar(df_tickets['mes_referencia'], df_tickets['volume_tickets'], 
            width=20, color='#F39C12', alpha=0.8, label='Tickets de Suporte Feitos')

    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    plt.xticks(rotation=45)

    for x, y in zip(df_total['mes_referencia'], df_total['volume']):
        ax1.annotate(f'{int(y):,}'.replace(',', '.'), (x, y), 
                    textcoords="offset points", xytext=(0,15), 
                    ha='center', fontsize=11, weight='black', color='#145A32')

    for x, y in zip(df_tickets['mes_referencia'], df_tickets['volume_tickets']):
        ax2.annotate(f'{int(y)}', (x, y), textcoords="offset points", 
                    xytext=(0,5), ha='center', fontsize=9, weight='bold')

    plt.suptitle('NovaShop: Evolução Temporal e Saúde da Operação (2023 - 2024)', fontsize=20, weight='bold', y=0.95)
    ax1.set_ylabel('Quantidade de Pedidos')
    ax2.set_ylabel('Tickets Abertos')
    ax1.legend(title='Indicadores', loc='upper left', frameon=True)
    ax2.legend(loc='upper left')
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    logger.info("Gráfico integrado gerado com sucesso.")
    plt.show()

# ==============================================================================
# INSIGHTS E HIPÓTESES
# ==============================================================================
def gerar_hipoteses_estrategicas(df_total: pd.DataFrame) -> None:
    """Analisa para formular conclusões de negócio."""
    print("\n" + "="*85)
    print("ANÁLISE DE SAZONALIDADE")
    print("="*85)
    
    pico = df_total.loc[df_total['volume'].idxmax()]
    
    print(f"PICO DE OPERAÇÃO: {pico['mes_referencia'].strftime('%m/%Y')} com {int(pico['volume']):,} pedidos.".replace(',', '.'))
    print("-" * 85)

    print("HIPÓTESES SUGERIDAS:")
    print("1. [PICO NOVEMBRO]: Sazonalidade agressiva de Black Friday. O aumento súbito")
    print("   de pedidos pode estar sobrecarregando a logística, explicando o aumento")
    print("   nos tickets de suporte e cancelamentos por atraso (meses de novembro e")
    print("   dezembro de 2023), o que nos mostra que a empresa não estava preparada")
    print("   para esse aumento e, provavelmente, houve uma perda de confiança por parte")
    print("   dos clientes.")
    
    print("\n2. [PICO DEZEMBRO]: Compras de Natal.")
    
    print("\n3. [QUEDA JANEIRO]: 'Ressaca' de consumo pós-festas e impacto de impostos")
    print("   de início de ano (IPVA/IPTU) no orçamento das famílias B2C.")

# ==============================================================================
# ORQUESTRADOR PRINCIPAL
# ==============================================================================
def analisar_evolucao_temporal(df_pedidos: pd.DataFrame, df_tickets: pd.DataFrame) -> None:
    """Orquestra a análise temporal integrada."""
    try:
        evol_status, evol_total = preparar_dados_pedidos(df_pedidos)
        evol_tickets = preparar_dados_tickets(df_tickets)
    
        gerar_hipoteses_estrategicas(evol_total)
        plotar_evolucao_temporal(evol_status, evol_total, evol_tickets)
    except Exception as e:
        logger.error(f"Erro na análise temporal: {e}")

# ==============================================================================
# EXECUÇÃO DIRETA (PROIBIDA)
# ==============================================================================
if __name__ == "__main__":
    print("\n" + "!"*85)
    print("AVISO: Este módulo faz parte da biblioteca de análise da NovaShop.")
    print("Ele não deve ser executado individualmente.")
    print("Por favor, execute o sistema através do arquivo: main.py")
    print("!"*85 + "\n")
