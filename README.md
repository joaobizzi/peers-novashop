# Case Técnico: NovaShop — Digital Consulting

> Análise estratégica de dados de e-commerce para o processo seletivo de estágio CDPeers - 2026.

<div align="center">


**[🌐 Acessar Dashboard Interativo](https://joaobizzi.github.io/peers-novashop/)**

</div>

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Tecnologias Utilizadas](#️-tecnologias-utilizadas)
- [Pipeline de Dados](#-pipeline-de-dados)
- [Documentação de Tratamento de Dados](#-documentação-de-tratamento-de-dados-item-6)
- [Análises Realizadas](#-análises-realizadas)
- [Principais Descobertas](#-principais-descobertas)
- [Como Executar](#-como-executar)

---

## 🔍 Visão Geral

Este repositório contém a solução completa do desafio técnico para a **NovaShop**, um e-commerce em expansão que busca entender as causas-raiz de cancelamentos e o crescimento dos tickets de suporte.

O projeto é composto por dois entregáveis principais:

| Entregável | Descrição |
|:---|:---|
| **Pipeline Python** | Scripts de limpeza, validação e análise estatística dos dados |
| **Dashboard Web** | Interface visual interativa publicada via GitHub Pages |

**Base de dados analisada:** 15.000 pedidos · 3.000 clientes · 200 produtos · Período 2023–2024

---

## 📁 Estrutura do Repositório

```
peers-novashop/
│
├── data/
│   ├── bruto/                  # CSVs originais fornecidos (input)
│   │   ├── clientes.csv
│   │   ├── produtos.csv
│   │   ├── pedidos.csv
│   │   ├── itens_pedido.csv
│   │   ├── avaliacoes.csv
│   │   └── tickets_suporte.csv
│   │
│   └── processado/             # CSVs após limpeza (output do pipeline)
│       ├── clientes_limpo.csv
│       ├── produtos_limpo.csv
│       ├── pedidos_limpo.csv
│       ├── itens_pedido_limpo.csv
│       ├── avaliacoes_limpo.csv
│       └── tickets_suporte_limpo.csv
│
├── scripts/                    # Módulos Python de análise
│   ├── main.py                 # Ponto de entrada — orquestra todo o sistema
│   ├── limpar_dados.py         # Pipeline de limpeza e validação
│   ├── analise_volume_por_status.py
│   ├── analise_cancelamento.py
│   ├── analise_maiores_produtos_vendidos.py
│   ├── analise_ticket_medio_por_segmento.py
│   ├── analise_temporal.py
│   └── analise_cancelamento.py
│
├── docs/                       # Dashboard web (GitHub Pages)
│   └── index.html              # Interface interativa
│   ├── script.js
│   └── style.css
│
├── README.md
└── requirements.txt
```

---

## 🛠️ Tecnologias Utilizadas

| Biblioteca | Versão | Uso |
|:---|:---|:---|
| `Python` | 3.12.3 | Linguagem principal |
| `Pandas` | 2.1.4 | Manipulação e transformação de dados |
| `Matplotlib` | 3.6.3 | Geração de gráficos |
| `Seaborn` | 0.13.2 | Visualizações estatísticas |
| `SciPy` | 1.11.4 | Testes de hipótese (Welch's T-Test) |
| `Pathlib` | stdlib | Compatibilidade de caminhos Windows/Linux |
| `Logging` | stdlib | Rastreabilidade de erros e alertas de processo |
| `Chart.js` | 4.4.1 | Gráficos interativos no dashboard web |

---

## 🔄 Pipeline de Dados

O módulo `limpar_dados.py` orquestra um pipeline determinístico em 4 etapas:

```
[data/bruto/*.csv]
       │
       ▼
  1. Ler ──── Leitura dos CSVs originais via Pandas
       │
       ▼
  2. Limpar ───── Limpeza específica por entidade (Strategy Pattern)
       │          limpar_clientes() / limpar_produtos() / limpar_pedidos()
       │          limpar_avaliacoes() / limpar_itens_pedido() / limpar_suporte()
       ▼
  3. Tratar ─ Sincronização financeira bottom-up
       │          valor_total recalculado a partir de itens_pedido
       │          Pedidos com valor inválido em status financeiro → removidos
       ▼
  4. Salvar ─── Salva resultados em data/processado/*_limpo.csv
       │
       ▼
[scripts/analise_*.py] ── Módulos de análise consomem os dados limpos
```

> **Determinismo garantido:** dado o mesmo CSV de entrada, a saída é sempre idêntica — facilitando auditoria e versionamento.

---

## 📊 Documentação de Tratamento de Dados (Item 6)

### Visão Geral das Bases

| Base | Linhas Processadas | Módulo Responsável |
|:---|:---:|:---|
| `clientes` | 3.000 | `limpar_clientes()` |
| `produtos` | 200 | `limpar_produtos()` |
| `pedidos` | 15.000 | `limpar_pedidos()` + `sincronizar_integridade_financeira()` |
| `itens_pedido` | 36.740 | `limpar_itens_pedido()` |
| `avaliacoes` | 8.000 | `limpar_avaliacoes()` |
| `tickets_suporte` | 4.000 | `limpar_suporte()` |
| **Total** | **~66.940** | |

### Regras de Limpeza por Entidade

| Dataset | Inconsistência Identificada | Tratamento Aplicado | Justificativa de Negócio |
|:---|:---|:---|:---|
| **Geral** | Datas em formato texto ou inconsistentes | Conversão para `datetime` com `errors='coerce'` | Necessário para análise temporal mensal (2023/2024) e identificação de picos sazonais |
| **Clientes** | Coluna `segmento` com variações de capitalização (ex: `b2b`, `B2B`, `b2B`) | Normalização via `.str.strip().str.upper()` | Garante integridade no cruzamento com pedidos para análise B2B vs B2C |
| **Produtos** | Preços ou custos com valores negativos | Filtragem: mantidos apenas registros com `preco_unitario >= 0` e `custo_unitario >= 0` | Valores negativos invalidariam cálculos de receita bruta, líquida e ranking de produtos |
| **Produtos** | Nomes de produtos ausentes (nulos) | Remoção via `dropna(subset=['nome'])` | Garante identificação correta dos 10 produtos mais vendidos por volume |
| **Avaliações** | Comentários nulos | Imputação com `"Sem comentário"` | Preserva a linha para métricas de satisfação sem distorcer análises de texto |
| **Avaliações** | Registros sem `pedido_id`, `produto_id` ou `id` | Remoção via `dropna(subset=[...])` | Avaliações sem chave de relacionamento são inúteis para cruzamento com pedidos |
| **Pedidos** | Pedidos com status financeiro (`entregue`, `em_transito`, `cancelado`, `devolvido`) e `valor_total` nulo ou ≤ 0 | Exclusão dos registros inconsistentes | Evita distorções no ticket médio e nas análises de receita por segmento e canal |
| **Pedidos** | `valor_total` inconsistente com os itens do pedido | Recálculo bottom-up: `valor_total = SUM(quantidade × preco_praticado)` por `pedido_id` | `itens_pedido` é a fonte de verdade — garante integridade financeira das análises |
| **Itens Pedido** | Coluna `desconto_aplicado` com valores nulos | Imputação com `0.0` | Essencial para operações aritméticas de faturamento; ausência de registro = sem desconto |
| **Itens Pedido** | Registros sem `preco_praticado` ou `quantidade` | Remoção via `dropna(subset=[...])` | Itens sem preço ou quantidade não permitem cálculo de receita |
| **Tickets Suporte** | `data_resolucao` não preenchida | Mantida como `NaT` (nula) | Representa tickets em aberto — informação relevante para medir backlog de suporte |
| **Tickets Suporte** | Cálculo de `tempo_resolucao_dias` ausente | Computado como `(data_resolucao - data_abertura).dt.days` | Permite análise de SLA e eficiência do time de suporte ao cliente |
| **Geral** | Registros duplicados em todas as bases | Remoção via `drop_duplicates()` ao final de cada limpeza | Evita dupla contagem em todas as métricas de volume e financeiras |

### Integridade Financeira — Sincronização Bottom-Up

A função `sincronizar_integridade_financeira()` garante consistência entre as tabelas `pedidos` e `itens_pedido`:

```python
# 1. Recalcula o valor real de cada pedido a partir dos itens
df_itens['total_item'] = df_itens['quantidade'] * df_itens['preco_praticado']
soma_itens = df_itens.groupby('pedido_id')['total_item'].sum().round(2)

# 2. Substitui o valor_total original pelo recalculado
df_pedidos = df_pedidos.merge(soma_itens, on='id', how='left')
df_pedidos['valor_total'] = df_pedidos['valor_calculado'].fillna(df_pedidos['valor_total'])

# 3. Remove pedidos financeiros com valor inválido
status_financeiros = ['entregue', 'em_transito', 'cancelado', 'devolvido']
filtro_invalido = (df['status'].isin(status_financeiros)) & (
    df['valor_total'].isna() | (df['valor_total'] <= 0)
)
df_final = df[~filtro_invalido]
```

> ⚠️ **Limitação conhecida:** pedidos sem itens associados mantêm o `valor_total` original silenciosamente.

---

## 📈 Análises Realizadas

| # | Questão | Módulo | Método |
|:---:|:---|:---|:---|
| Q1 | Volume e distribuição percentual por status de pedido | `analise_volume_por_status.py` | Contagem + normalização |
| Q2 | Top 10 produtos por volume vendido e receita líquida | `analise_maiores_produtos_vendidos.py` | Groupby + join com custo unitário |
| Q3 | Ticket médio B2B vs B2C com teste de significância | `analise_ticket_medio_por_segmento.py` | Welch's T-Test (`scipy.stats`) |
| Q4 | Evolução temporal mensal e sazonalidade (2023–2024) | `analise_temporal.py` | Série temporal + correlação com tickets |
| Q5 | Taxa de cancelamento e ticket médio por canal de aquisição | `analise_cancelamento.py` | Merge clientes → pedidos + groupby |

---

## 🚀 Como Executar

### Pré-requisitos

```bash
python --version  # 3.12.3 ou superior
```

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/joaobizzi/peers-novashop
cd peers-novashop

# 2. (Opcional) Crie um ambiente virtual
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt
```

### Execução

```bash
# A partir da raiz do projeto
python scripts/main.py
```

### Dashboard Web

Acesse a interface interativa diretamente pelo navegador, sem necessidade de instalação:

**[🌐 https://joaobizzi.github.io/peers-novashop/](https://joaobizzi.github.io/peers-novashop/)**


<div align="center">
  <sub>Desenvolvido por <strong>João Pedro Bizzi Oliveira</strong> · Peers Group · Digital Consulting</sub>
</div>
