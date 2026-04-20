import pandas as pd
import logging
from pathlib import Path
from typing import Dict, List, Callable

# ==============================================================================
# CONFIGURAÇÕES E LOGGING
# ==============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(funcName)s] - %(message)s'
)
logger = logging.getLogger(__name__)

CAMINHO_BRUTO = Path("data/bruto/")
CAMINHO_PROCESSADO = Path("data/processado/")
BASES_CONFIG = [
    'clientes', 'produtos', 'avaliacoes', 
    'pedidos', 'itens_pedido', 'tickets_suporte'
]

# ==============================================================================
# FUNÇÕES AUXILIARES
# ==============================================================================
def converter_colunas_data(df: pd.DataFrame, colunas: List[str]) -> pd.DataFrame:
    """Converte colunas específicas para datetime com tratamento de erro."""
    for col in colunas:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        else:
            logger.warning(f"Coluna de data ausente para conversão: {col}")
    return df

# ==============================================================================
# LÓGICA DE LIMPEZA E INTEGRIDADE
# ==============================================================================
def limpar_clientes(df: pd.DataFrame) -> pd.DataFrame:
    df = converter_colunas_data(df, ['data_cadastro'])
    if 'segmento' in df.columns:
        df['segmento'] = df['segmento'].str.strip().str.upper()
    return df

def limpar_produtos(df: pd.DataFrame) -> pd.DataFrame:
    if all(col in df.columns for col in ['preco_unitario', 'custo_unitario']):
        df = df.query("preco_unitario >= 0 and custo_unitario >= 0").copy()
    return df.dropna(subset=['nome'])

def limpar_avaliacoes(df: pd.DataFrame) -> pd.DataFrame:
    df = converter_colunas_data(df, ['data_avaliacao'])
    df['comentario'] = df['comentario'].fillna("Sem comentário")
    return df.dropna(subset=['pedido_id', 'produto_id', 'id'])

def limpar_pedidos(df: pd.DataFrame) -> pd.DataFrame:
    df = converter_colunas_data(df, ['data_pedido'])
    return df

def limpar_itens_pedido(df: pd.DataFrame) -> pd.DataFrame:
    if 'desconto_aplicado' in df.columns:
        df['desconto_aplicado'] = df['desconto_aplicado'].fillna(0.0)
    return df.dropna(subset=['preco_praticado', 'quantidade'])

def limpar_suporte(df: pd.DataFrame) -> pd.DataFrame:
    df = converter_colunas_data(df, ['data_abertura', 'data_resolucao'])
    df['tempo_resolucao_dias'] = (df['data_resolucao'] - df['data_abertura']).dt.days
    return df

def sincronizar_integridade_financeira(df_pedidos: pd.DataFrame, df_itens: pd.DataFrame) -> pd.DataFrame:
    """Recalcula o valor_total de pedidos com base na granularidade de itens_pedido."""
    logger.info("Sincronizando valor_total dos pedidos com base nos itens (bottom-up)...")
    
    df_itens_calc = df_itens.copy()
    df_itens_calc['total_item'] = (
        df_itens_calc['quantidade'] * df_itens_calc['preco_praticado']
    )
    
    soma_itens = df_itens_calc.groupby('pedido_id')['total_item'].sum().round(2).reset_index()
    soma_itens.columns = ['id', 'valor_calculado']
    
    df_final = df_pedidos.merge(soma_itens, on='id', how='left')
    df_final['valor_total'] = df_final['valor_calculado'].fillna(df_final['valor_total'])
    
    status_financeiros = ['entregue', 'em_transito', 'cancelado', 'devolvido']
    filtro_invalido = (df_final['status'].isin(status_financeiros)) & (
        df_final['valor_total'].isna() | (df_final['valor_total'] <= 0)
    )
    
    return df_final[~filtro_invalido].drop(columns=['valor_calculado']).copy()

# ==============================================================================
# PROCESSAMENTO
# ==============================================================================
def aplicar_limpeza(df: pd.DataFrame, tipo_base: str) -> pd.DataFrame:
    """Mapeia e aplica a função de limpeza correspondente."""
    limpadores: Dict[str, Callable[[pd.DataFrame], pd.DataFrame]] = {
        'clientes': limpar_clientes,
        'produtos': limpar_produtos,
        'avaliacoes': limpar_avaliacoes,
        'pedidos': limpar_pedidos,
        'itens_pedido': limpar_itens_pedido,
        'tickets_suporte': limpar_suporte
    }
    
    funcao_limpeza = limpadores.get(tipo_base, lambda d: d)
    
    logger.info(f"Iniciando limpeza da base: {tipo_base}")
    df_limpo = funcao_limpeza(df)
    
    return df_limpo.drop_duplicates()

# ==============================================================================
# ORQUESTRADOR PRINCIPAL
# ==============================================================================
def processar_pipeline() -> Dict[str, pd.DataFrame]:
    """Executa o fluxo completo incluindo sincronização de integridade."""
    dfs_processados = {}
    CAMINHO_PROCESSADO.mkdir(parents=True, exist_ok=True)
    
    for nome_base in BASES_CONFIG:
        caminho_entrada = CAMINHO_BRUTO / f"{nome_base}.csv"
        if not caminho_entrada.exists():
            logger.error(f"Arquivo não encontrado: {caminho_entrada}")
            continue
            
        try:
            df = pd.read_csv(caminho_entrada)
            dfs_processados[nome_base] = aplicar_limpeza(df, nome_base)
        except Exception as e:
            logger.exception(f"Erro ao processar {nome_base}: {e}")

    if 'pedidos' in dfs_processados and 'itens_pedido' in dfs_processados:
        dfs_processados['pedidos'] = sincronizar_integridade_financeira(
            dfs_processados['pedidos'], 
            dfs_processados['itens_pedido']
        )

    for nome_base, df_final in dfs_processados.items():
        caminho_saida = CAMINHO_PROCESSADO / f"{nome_base}_limpo.csv"
        df_final.to_csv(caminho_saida, index=False)
        logger.info(f"Salvo: {caminho_saida.name} ({len(df_final)} linhas)")

    return dfs_processados

# ==============================================================================
# EXECUÇÃO DIRETA (PROIBIDA)
# ==============================================================================
if __name__ == "__main__":
    print("\n" + "!"*85)
    print("AVISO: Este módulo faz parte da biblioteca de análise da NovaShop.")
    print("Ele não deve ser executado individualmente.")
    print("Por favor, execute o sistema através do arquivo: main.py")
    print("!"*85 + "\n")
