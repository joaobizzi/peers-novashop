# Case Técnico: NovaShop - Digital Consulting 

Este repositório contém a solução do desafio técnico para a **NovaShop**, um e-commerce em expansão que busca entender as causas raízes de cancelamentos e o crescimento dos tickets de suporte.

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3.12.3
- **Biblioteca Principal:** `Pandas` para manipulação de dados.
- **Estrutura de Arquivos:** `Pathlib` para garantir compatibilidade entre sistemas operacionais (Windows/Linux).
- **Monitoramento:** Biblioteca `Logging` para rastreabilidade de erros e alertas de processo.
- **Visualização de Dados:** Biblioteca `Matplotlib` e `Seaborn` para geração e visualização de grafícos.
- **Estatistica:** Biblioteca `Scipy` para analise estatistica dos dados.

## 📊 Documentação de Tratamento de Inconsistências (Item 6)
Conforme exigido pelo item 6 do case, foram identificadas e tratadas as seguintes anomalias nas bases fornecidas:

| Dataset | Possiveis Inconsistências Tratadas | Tratamento Aplicado | Justificativa de Negócio |
| :--- | :--- | :--- | :--- |
| **Geral** | Datas em formato de texto/inconsistentes. | Conversão para `datetime`. | Necessário para analisar a evolução mensal de 2023/2024 e picos de demanda. |
| **Produtos** | Preços ou custos negativos. | Filtragem para manter apenas valores $\geq 0$. | Valores negativos invalidariam os cálculos de receita e ranking de produtos vendidos. |
| **Produtos** | Nomes de produtos ausentes (Nulos). | Remoção dos registros via `dropna`. | Garante a correta identificação dos 10 produtos mais vendidos. |
| **Pedidos** | Status 'entregue' com valor total $\leq 0$. | Exclusão dos registros inconsistentes. | Evita distorções no cálculo do ticket médio por segmento (B2C vs B2B). |
| **Avaliações**| Comentários nulos. | Preenchimento com "Sem comentário". | Preserva a linha da avaliação para métricas de satisfação, tratando apenas o texto. |
| **Itens Pedido**| Descontos nulos. | Imputação do valor `0.0`. | Essencial para operações matemáticas de faturamento e descontos por canal. |
| **Suporte** | Datas de resolução não preenchidas. | Mantidas como nulas (`NaT`). | Permite identificar tickets em aberto, ajudando a investigar a causa raiz do aumento do suporte. |

## 🚀 Como Executar o Script
1. Clone este repositório ou baixe os arquivos.
2. Certifique-se de que a estrutura de pastas segue o padrão:
   - `data/bruto/` (Contendo os CSVs originais).
   - `data/processado/` (Onde os arquivos limpos serão salvos).
3. Execute o comando no terminal:
   ```bash
   python main.py