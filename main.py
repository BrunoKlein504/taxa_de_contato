# import streamlit as st
# import pandas as pd
# import unicodedata

# # ============================================================
# # CONFIGURAÇÃO
# # ============================================================

# st.set_page_config(
#     page_title="Taxa de Contato - Operação Segura",
#     layout="wide"
# )

# st.title("Taxa de Contato — Operação Segura")

# st.caption(
#     "100% das equipes devem receber pelo menos uma inspeção "
#     "de Líder/Gerente a cada trimestre."
# )


# # ============================================================
# # FUNÇÕES
# # ============================================================

# def normalizar_texto(valor):
#     """Remove acentos e coloca texto em maiúsculo."""
#     if pd.isna(valor):
#         return ""

#     valor = str(valor).strip().upper()

#     return "".join(
#         c
#         for c in unicodedata.normalize("NFKD", valor)
#         if not unicodedata.combining(c)
#     )


# def normalizar_id(serie):
#     """
#     Evita IDs do Excel ficando como 123.0.
#     """
#     return (
#         serie
#         .astype(str)
#         .str.strip()
#         .str.replace(r"\.0$", "", regex=True)
#     )


# @st.cache_data
# def carregar_dados(arquivo):
#     return pd.read_excel(
#         arquivo,
#         sheet_name="Checklists Realizados"
#     )


# # ============================================================
# # UPLOAD
# # ============================================================

# arquivo = st.file_uploader(
#     "Selecione a planilha",
#     type=["xlsx"]
# )

# if arquivo is None:
#     st.info("Carregue a planilha para iniciar.")
#     st.stop()


# # ============================================================
# # TRATAMENTO
# # ============================================================

# df = carregar_dados(arquivo)

# df.columns = df.columns.str.strip()

# df["Data de Execução"] = pd.to_datetime(
#     df["Data de Execução"],
#     errors="coerce"
# )

# df["ID da Equipe"] = normalizar_id(
#     df["ID da Equipe"]
# )

# if "Codigo da Equipe/Instalação" in df.columns:
#     df["Codigo da Equipe/Instalação"] = normalizar_id(
#         df["Codigo da Equipe/Instalação"]
#     )

# df["Cargo Normalizado"] = (
#     df["Cargo"]
#     .fillna("")
#     .apply(normalizar_texto)
# )

# df = df.dropna(
#     subset=["Data de Execução"]
# )


# # ============================================================
# # PRIMEIRO SEMESTRE
# # ============================================================

# anos = sorted(
#     df["Data de Execução"]
#     .dt.year
#     .unique()
# )

# ano = st.sidebar.selectbox(
#     "Ano",
#     anos,
#     index=len(anos) - 1
# )

# df = df[
#     (df["Data de Execução"].dt.year == ano)
#     & (df["Data de Execução"].dt.month.between(1, 6))
# ].copy()


# # ============================================================
# # FILTROS
# # ============================================================

# st.sidebar.header("Filtros")

# for coluna in [
#     "Unidade de Negócio (Distribuidora)",
#     "Superintendência",
#     "Regional"
# ]:

#     if coluna not in df.columns:
#         continue

#     opcoes = sorted(
#         df[coluna]
#         .dropna()
#         .astype(str)
#         .unique()
#     )

#     selecionados = st.sidebar.multiselect(
#         coluna,
#         opcoes
#     )

#     if selecionados:
#         df = df[
#             df[coluna]
#             .astype(str)
#             .isin(selecionados)
#         ]


# # ============================================================
# # UNIVERSO TOTAL DE EQUIPES
# # ============================================================

# equipes_base = sorted(
#     df["ID da Equipe"]
#     .dropna()
#     .unique()
# )

# total_equipes = len(equipes_base)

# if total_equipes == 0:
#     st.warning("Nenhuma equipe encontrada.")
#     st.stop()


# # ============================================================
# # FILTRO: LÍDER / GERENTE
# # ============================================================

# # GTE foi incluído porque existem cargos com essa abreviação
# # na sua planilha.
# padrao_lideranca = r"\bLIDER\b|\bGERENTE\b|\bGTE\b"

# lideranca = df[
#     df["Cargo Normalizado"].str.contains(
#         padrao_lideranca,
#         regex=True,
#         na=False
#     )
# ].copy()


# # ============================================================
# # REMOVER DUPLICIDADE
# # ============================================================

# # Sua planilha possui diversas linhas referentes à mesma inspeção,
# # por exemplo por membro ou não conformidade.
# #
# # Então:
# # 1 inspeção + 1 equipe = 1 contato.

# inspecoes = (
#     lideranca
#     .sort_values("Data de Execução")
#     .drop_duplicates(
#         subset=[
#             "Inspeção",
#             "ID da Equipe"
#         ]
#     )
#     .copy()
# )

# inspecoes["Mês"] = (
#     inspecoes["Data de Execução"].dt.month
# )


# # ============================================================
# # CONTAGEM POR TRIMESTRE
# # ============================================================

# t1 = (
#     inspecoes[
#         inspecoes["Mês"].between(1, 3)
#     ]
#     .groupby("ID da Equipe")
#     .agg(
#         Inspeções_T1=("Inspeção", "nunique"),
#         Primeiro_Contato_T1=("Data de Execução", "min"),
#         Ultimo_Contato_T1=("Data de Execução", "max")
#     )
# )


# t2 = (
#     inspecoes[
#         inspecoes["Mês"].between(4, 6)
#     ]
#     .groupby("ID da Equipe")
#     .agg(
#         Inspeções_T2=("Inspeção", "nunique"),
#         Primeiro_Contato_T2=("Data de Execução", "min"),
#         Ultimo_Contato_T2=("Data de Execução", "max")
#     )
# )


# # ============================================================
# # TABELA DE TODAS AS EQUIPES
# # ============================================================

# status = pd.DataFrame({
#     "ID da Equipe": equipes_base
# })

# status = status.merge(
#     t1,
#     left_on="ID da Equipe",
#     right_index=True,
#     how="left"
# )

# status = status.merge(
#     t2,
#     left_on="ID da Equipe",
#     right_index=True,
#     how="left"
# )

# status["Inspeções_T1"] = (
#     status["Inspeções_T1"]
#     .fillna(0)
#     .astype(int)
# )

# status["Inspeções_T2"] = (
#     status["Inspeções_T2"]
#     .fillna(0)
#     .astype(int)
# )

# status["Coberto T1"] = (
#     status["Inspeções_T1"] >= 1
# )

# status["Coberto T2"] = (
#     status["Inspeções_T2"] >= 1
# )

# status["Cumpriu semestre"] = (
#     status["Coberto T1"]
#     & status["Coberto T2"]
# )


# # ============================================================
# # STATUS
# # ============================================================

# def classificar(row):

#     if row["Coberto T1"] and row["Coberto T2"]:
#         return "OK"

#     if row["Coberto T1"] and not row["Coberto T2"]:
#         return "Pendente T2"

#     if not row["Coberto T1"] and row["Coberto T2"]:
#         return "Pendente T1"

#     return "Sem contato"


# status["Status"] = status.apply(
#     classificar,
#     axis=1
# )


# # ============================================================
# # MÉTRICAS
# # ============================================================

# cobertas_t1 = status["Coberto T1"].sum()
# cobertas_t2 = status["Coberto T2"].sum()

# cumpriram = (
#     status["Cumpriu semestre"].sum()
# )

# sem_contato = (
#     (
#         (status["Inspeções_T1"] == 0)
#         & (status["Inspeções_T2"] == 0)
#     )
#     .sum()
# )


# taxa_t1 = cobertas_t1 / total_equipes
# taxa_t2 = cobertas_t2 / total_equipes
# taxa_semestre = cumpriram / total_equipes


# # ============================================================
# # KPIs
# # ============================================================

# st.subheader("Visão geral")

# c1, c2, c3, c4, c5 = st.columns(5)

# c1.metric(
#     "Total de equipes",
#     total_equipes
# )

# c2.metric(
#     "Cobertura T1",
#     f"{taxa_t1:.1%}",
#     f"{cobertas_t1}/{total_equipes}"
# )

# c3.metric(
#     "Cobertura T2",
#     f"{taxa_t2:.1%}",
#     f"{cobertas_t2}/{total_equipes}"
# )

# c4.metric(
#     "Cumpriram ambos",
#     f"{taxa_semestre:.1%}",
#     f"{cumpriram}/{total_equipes}"
# )

# c5.metric(
#     "Sem contato",
#     sem_contato
# )


# # ============================================================
# # EVOLUÇÃO MENSAL
# # ============================================================

# st.divider()

# st.subheader("Evolução mensal da taxa de contato")

# st.caption(
#     "Cada equipe é contabilizada apenas no mês do primeiro "
#     "contato dentro daquele trimestre."
# )

# nomes_meses = {
#     1: "Janeiro",
#     2: "Fevereiro",
#     3: "Março",
#     4: "Abril",
#     5: "Maio",
#     6: "Junho"
# }

# # Meta solicitada:
# # 1º mês = 33%
# # 2º mês = +33%
# # 3º mês = restante até 100%.
# #
# # Embora 33 + 33 + 36 = 102%, a meta acumulada final
# # é limitada a 100%.

# metas_incrementais = [
#     0.33,
#     0.33,
#     0.36
# ]

# resultado_mensal = []


# for trimestre, meses in {
#     "T1": [1, 2, 3],
#     "T2": [4, 5, 6]
# }.items():

#     dados_tri = inspecoes[
#         inspecoes["Mês"].isin(meses)
#     ]

#     # Primeiro contato de cada equipe no trimestre
#     primeiro_contato = (
#         dados_tri
#         .groupby("ID da Equipe")[
#             "Data de Execução"
#         ]
#         .min()
#     )

#     mes_primeiro_contato = (
#         primeiro_contato.dt.month
#     )

#     acumulado = 0
#     meta_acumulada = 0

#     for posicao, mes in enumerate(meses):

#         novas_equipes = (
#             mes_primeiro_contato
#             .eq(mes)
#             .sum()
#         )

#         acumulado += novas_equipes

#         meta_mes = metas_incrementais[posicao]

#         meta_acumulada = min(
#             meta_acumulada + meta_mes,
#             1
#         )

#         resultado_mensal.append({
#             "Trimestre": trimestre,
#             "Mês": nomes_meses[mes],
#             "Novas equipes": novas_equipes,
#             "Equipes acumuladas": acumulado,
#             "Taxa": acumulado / total_equipes,
#             "Meta": meta_acumulada
#         })


# evolucao = pd.DataFrame(
#     resultado_mensal
# )


# # ============================================================
# # GRÁFICO
# # ============================================================

# grafico = evolucao.copy()

# grafico["Período"] = (
#     grafico["Trimestre"]
#     + " - "
#     + grafico["Mês"]
# )

# grafico = (
#     grafico
#     .set_index("Período")[
#         ["Taxa", "Meta"]
#     ]
# )

# st.line_chart(
#     grafico
# )


# # ============================================================
# # TABELA DE EVOLUÇÃO
# # ============================================================

# tabela_evolucao = evolucao.copy()

# tabela_evolucao["Taxa"] = (
#     tabela_evolucao["Taxa"]
#     .map(lambda x: f"{x:.1%}")
# )

# tabela_evolucao["Meta"] = (
#     tabela_evolucao["Meta"]
#     .map(lambda x: f"{x:.0%}")
# )

# st.dataframe(
#     tabela_evolucao,
#     use_container_width=True,
#     hide_index=True
# )


# # ============================================================
# # EQUIPES NÃO INSPECIONADAS
# # ============================================================

# st.divider()

# st.subheader("Equipes pendentes")

# col1, col2 = st.columns(2)


# with col1:

#     st.markdown(
#         f"### Sem contato no T1 ({(~status['Coberto T1']).sum()})"
#     )

#     st.dataframe(
#         status[
#             ~status["Coberto T1"]
#         ][
#             [
#                 "ID da Equipe",
#                 "Inspeções_T1",
#                 "Inspeções_T2",
#                 "Status"
#             ]
#         ],
#         use_container_width=True,
#         hide_index=True
#     )


# with col2:

#     st.markdown(
#         f"### Sem contato no T2 ({(~status['Coberto T2']).sum()})"
#     )

#     st.dataframe(
#         status[
#             ~status["Coberto T2"]
#         ][
#             [
#                 "ID da Equipe",
#                 "Inspeções_T1",
#                 "Inspeções_T2",
#                 "Status"
#             ]
#         ],
#         use_container_width=True,
#         hide_index=True
#     )


# # ============================================================
# # CONCENTRAÇÃO DE INSPEÇÕES
# # ============================================================

# st.divider()

# st.subheader("Concentração de inspeções")

# st.caption(
#     "Aqui aparecem equipes que receberam várias inspeções, "
#     "enquanto outras podem ter ficado sem contato."
# )


# status["Excesso T1"] = (
#     status["Inspeções_T1"] - 1
# ).clip(lower=0)

# status["Excesso T2"] = (
#     status["Inspeções_T2"] - 1
# ).clip(lower=0)

# status["Inspeções excedentes"] = (
#     status["Excesso T1"]
#     + status["Excesso T2"]
# )


# repetidas = status[
#     status["Inspeções excedentes"] > 0
# ].sort_values(
#     "Inspeções excedentes",
#     ascending=False
# )


# c1, c2 = st.columns(2)

# c1.metric(
#     "Equipes com inspeção repetida",
#     len(repetidas)
# )

# c2.metric(
#     "Inspeções excedentes",
#     repetidas["Inspeções excedentes"].sum()
# )


# st.dataframe(
#     repetidas[
#         [
#             "ID da Equipe",
#             "Inspeções_T1",
#             "Inspeções_T2",
#             "Excesso T1",
#             "Excesso T2",
#             "Status"
#         ]
#     ],
#     use_container_width=True,
#     hide_index=True
# )


# # ============================================================
# # TODAS AS EQUIPES
# # ============================================================

# st.divider()

# st.subheader("Status por equipe")

# filtro_status = st.multiselect(
#     "Status",
#     sorted(status["Status"].unique())
# )

# status_filtrado = status.copy()

# if filtro_status:
#     status_filtrado = status_filtrado[
#         status_filtrado["Status"]
#         .isin(filtro_status)
#     ]


# st.dataframe(
#     status_filtrado[
#         [
#             "ID da Equipe",
#             "Inspeções_T1",
#             "Primeiro_Contato_T1",
#             "Inspeções_T2",
#             "Primeiro_Contato_T2",
#             "Status"
#         ]
#     ],
#     use_container_width=True,
#     hide_index=True
# )


# # ============================================================
# # HISTÓRICO INDIVIDUAL
# # ============================================================

# st.divider()

# st.subheader("Histórico da equipe")

# equipe = st.selectbox(
#     "Selecione uma equipe",
#     equipes_base
# )

# historico = inspecoes[
#     inspecoes["ID da Equipe"] == equipe
# ].sort_values(
#     "Data de Execução"
# )

# colunas = [
#     coluna
#     for coluna in [
#         "Data de Execução",
#         "Inspeção",
#         "ID da Equipe",
#         "Codigo da Equipe/Instalação",
#         "Inspetor",
#         "Cargo",
#         "Regional",
#         "Local"
#     ]
#     if coluna in historico.columns
# ]

# st.dataframe(
#     historico[colunas],
#     use_container_width=True,
#     hide_index=True
# )

# import pandas as pd
# import streamlit as st
# import plotly.express as px
# import unicodedata


# # ============================================================
# # CONFIGURAÇÃO
# # ============================================================

# st.set_page_config(
#     page_title="Taxa de Contato",
#     layout="wide"
# )

# st.title("Taxa de Contato por Equipe")

# st.caption(
#     "Cada equipe é contabilizada somente no primeiro contato "
#     "realizado dentro de cada trimestre."
# )


# # ============================================================
# # FUNÇÕES
# # ============================================================

# def normalizar_texto(valor):

#     if pd.isna(valor):
#         return ""

#     valor = str(valor).strip().upper()

#     return "".join(
#         c
#         for c in unicodedata.normalize("NFKD", valor)
#         if not unicodedata.combining(c)
#     )


# # ============================================================
# # UPLOAD
# # ============================================================

# arquivo = st.file_uploader(
#     "Selecione a planilha",
#     type=["xlsx"]
# )

# if arquivo is None:
#     st.stop()


# # ============================================================
# # CARREGAMENTO
# # ============================================================

# df = pd.read_excel(
#     arquivo,
#     sheet_name="Checklists Realizados"
# )

# df.columns = df.columns.str.strip()

# df["Data de Execução"] = pd.to_datetime(
#     df["Data de Execução"],
#     errors="coerce"
# )

# df = df.dropna(
#     subset=[
#         "ID da Equipe",
#         "Data de Execução"
#     ]
# )


# # ============================================================
# # PRIMEIRO SEMESTRE
# # ============================================================

# df = df[
#     df["Data de Execução"]
#     .dt.month
#     .between(1, 6)
# ].copy()


# # ============================================================
# # UNIVERSO DE EQUIPES
# # ============================================================

# # Guardamos as equipes antes do filtro de liderança.
# # Dessa forma, equipes sem contato de líder/gerente
# # continuam entrando no denominador.

# todas_equipes = (
#     df["ID da Equipe"]
#     .dropna()
#     .unique()
# )

# total_equipes = len(todas_equipes)


# # ============================================================
# # FILTRO DE LIDERANÇA
# # ============================================================

# df["Cargo Normalizado"] = (
#     df["Cargo"]
#     .fillna("")
#     .apply(normalizar_texto)
# )

# df_lideranca = df[
#     df["Cargo Normalizado"].str.contains(
#         r"\bLIDER\b|\bGERENTE\b|\bGTE\b",
#         regex=True,
#         na=False
#     )
# ].copy()


# # ============================================================
# # REMOVE REPETIÇÕES DA MESMA INSPEÇÃO
# # ============================================================

# if "Inspeção" in df_lideranca.columns:

#     df_lideranca = (
#         df_lideranca
#         .sort_values("Data de Execução")
#         .drop_duplicates(
#             subset=[
#                 "Inspeção",
#                 "ID da Equipe"
#             ]
#         )
#     )


# # ============================================================
# # IDENTIFICA MÊS E TRIMESTRE
# # ============================================================

# df_lideranca["Mês"] = (
#     df_lideranca["Data de Execução"]
#     .dt.month
# )

# df_lideranca["Trimestre"] = (
#     df_lideranca["Mês"]
#     .apply(
#         lambda x: "T1"
#         if x <= 3
#         else "T2"
#     )
# )


# # ============================================================
# # PRIMEIRO CONTATO DE CADA EQUIPE NO TRIMESTRE
# # ============================================================

# # Essa é a principal regra.
# #
# # Se uma equipe foi inspecionada:
# #
# # Janeiro
# # Fevereiro
# # Março
# #
# # apenas janeiro será considerado para a cobertura.
# #
# # A contagem reinicia no T2.

# primeiro_contato = (
#     df_lideranca
#     .groupby(
#         [
#             "ID da Equipe",
#             "Trimestre"
#         ],
#         as_index=False
#     )
#     ["Data de Execução"]
#     .min()
# )

# primeiro_contato["Mês"] = (
#     primeiro_contato["Data de Execução"]
#     .dt.month
# )


# # ============================================================
# # CRIA MATRIZ DE COBERTURA
# # ============================================================

# meses = {
#     1: "Janeiro",
#     2: "Fevereiro",
#     3: "Março",
#     4: "Abril",
#     5: "Maio",
#     6: "Junho"
# }

# equipes = pd.DataFrame(
#     False,
#     index=todas_equipes,
#     columns=list(meses.values())
# )

# equipes.index.name = "ID da Equipe"


# # ============================================================
# # MARCA APENAS O PRIMEIRO CONTATO
# # ============================================================

# for _, linha in primeiro_contato.iterrows():

#     equipe = linha["ID da Equipe"]

#     mes = linha["Mês"]

#     nome_mes = meses[mes]

#     equipes.loc[
#         equipe,
#         nome_mes
#     ] = True


# # ============================================================
# # CONTATO POR TRIMESTRE
# # ============================================================

# equipes["Contato T1"] = (
#     equipes[
#         [
#             "Janeiro",
#             "Fevereiro",
#             "Março"
#         ]
#     ]
#     .any(axis=1)
# )

# equipes["Contato T2"] = (
#     equipes[
#         [
#             "Abril",
#             "Maio",
#             "Junho"
#         ]
#     ]
#     .any(axis=1)
# )


# # ============================================================
# # CONTATO NO SEMESTRE
# # ============================================================

# equipes["Contato no período"] = (
#     equipes["Contato T1"]
#     |
#     equipes["Contato T2"]
# )


# # ============================================================
# # CÁLCULOS
# # ============================================================

# contato_t1 = (
#     equipes["Contato T1"]
#     .sum()
# )

# contato_t2 = (
#     equipes["Contato T2"]
#     .sum()
# )

# sem_contato_t1 = (
#     total_equipes
#     - contato_t1
# )

# sem_contato_t2 = (
#     total_equipes
#     - contato_t2
# )

# com_contato_semestre = (
#     equipes["Contato no período"]
#     .sum()
# )

# sem_contato_semestre = (
#     total_equipes
#     - com_contato_semestre
# )


# # ============================================================
# # TAXAS
# # ============================================================

# taxa_t1 = (
#     contato_t1
#     / total_equipes
# )

# taxa_t2 = (
#     contato_t2
#     / total_equipes
# )

# taxa_sem_contato = (
#     sem_contato_semestre
#     / total_equipes
# )


# # ============================================================
# # KPIs
# # ============================================================

# c1, c2, c3 = st.columns(3)

# c1.metric(
#     "Taxa de Contato T1",
#     f"{taxa_t1:.1%}",
#     f"{contato_t1} equipes"
# )

# c2.metric(
#     "Taxa de Contato T2",
#     f"{taxa_t2:.1%}",
#     f"{contato_t2} equipes"
# )

# c3.metric(
#     "Sem contato no semestre",
#     sem_contato_semestre,
#     f"{taxa_sem_contato:.1%} do total"
# )


# # ============================================================
# # COBERTURA MENSAL
# # ============================================================

# st.subheader(
#     "Entrada de novas equipes na cobertura"
# )

# resultado_mensal = []

# acumulado_t1 = 0
# acumulado_t2 = 0


# for numero_mes, nome_mes in meses.items():

#     novas_equipes = (
#         equipes[nome_mes]
#         .sum()
#     )

#     if numero_mes <= 3:

#         acumulado_t1 += novas_equipes

#         acumulado = acumulado_t1

#         trimestre = "T1"

#     else:

#         acumulado_t2 += novas_equipes

#         acumulado = acumulado_t2

#         trimestre = "T2"

#     taxa = (
#         acumulado
#         / total_equipes
#     )

#     resultado_mensal.append({

#         "Trimestre": trimestre,

#         "Mês": nome_mes,

#         "Novas equipes": novas_equipes,

#         "Equipes acumuladas": acumulado,

#         "Taxa": taxa
#     })


# resultado_mensal = pd.DataFrame(
#     resultado_mensal
# )


# # ============================================================
# # TABELA MENSAL
# # ============================================================

# st.dataframe(

#     resultado_mensal.style.format({
#         "Taxa": "{:.1%}"
#     }),

#     use_container_width=True,

#     hide_index=True
# )


# # ============================================================
# # GRÁFICO MENSAL
# # ============================================================

# fig_mensal = px.bar(

#     resultado_mensal,

#     x="Mês",

#     y="Novas equipes",

#     color="Trimestre",

#     text="Novas equipes",

#     title="Novas equipes cobertas por mês"
# )

# fig_mensal.update_traces(
#     textposition="outside"
# )

# fig_mensal.update_layout(

#     xaxis_title="",

#     yaxis_title="Quantidade de novas equipes"
# )

# st.plotly_chart(
#     fig_mensal,
#     use_container_width=True
# )


# # ============================================================
# # COBERTURA POR TRIMESTRE
# # ============================================================

# st.subheader(
#     "Cobertura das equipes por trimestre"
# )

# grafico = pd.DataFrame({

#     "Trimestre": [
#         "T1",
#         "T1",
#         "T2",
#         "T2"
#     ],

#     "Status": [
#         "Com contato",
#         "Sem contato",
#         "Com contato",
#         "Sem contato"
#     ],

#     "Equipes": [
#         contato_t1,
#         sem_contato_t1,
#         contato_t2,
#         sem_contato_t2
#     ]
# })


# fig = px.bar(

#     grafico,

#     x="Trimestre",

#     y="Equipes",

#     color="Status",

#     barmode="stack",

#     text="Equipes",

#     title="Equipes com e sem contato"
# )

# fig.update_traces(
#     textposition="inside"
# )

# fig.update_layout(

#     xaxis_title="",

#     yaxis_title="Quantidade de equipes"
# )

# st.plotly_chart(
#     fig,
#     use_container_width=True
# )


# # ============================================================
# # EQUIPES SEM CONTATO
# # ============================================================

# st.subheader(
#     "Equipes sem nenhum contato entre janeiro e junho"
# )

# equipes_sem_contato = (
#     equipes[
#         ~equipes["Contato no período"]
#     ]
#     .reset_index()
# )

# st.write(
#     f"**{len(equipes_sem_contato)} equipes** "
#     "não receberam nenhum contato no período."
# )

# st.dataframe(

#     equipes_sem_contato[
#         ["ID da Equipe"]
#     ],

#     use_container_width=True,

#     hide_index=True
# )


# # ============================================================
# # VISÃO POR EQUIPE
# # ============================================================

# st.subheader(
#     "Primeiro contato válido por equipe"
# )

# visual = (
#     equipes
#     .reset_index()
#     .copy()
# )

# for coluna in [
#     "Janeiro",
#     "Fevereiro",
#     "Março",
#     "Abril",
#     "Maio",
#     "Junho",
#     "Contato T1",
#     "Contato T2",
#     "Contato no período"
# ]:

#     visual[coluna] = (
#         visual[coluna]
#         .replace({
#             True: "Sim",
#             False: "Não"
#         })
#     )


# st.dataframe(
#     visual,
#     use_container_width=True,
#     hide_index=True
# )

import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import unicodedata


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Taxa de Contato",
    layout="wide"
)

st.title("Taxa de Contato por Equipe")

st.caption(
    "Análise de cobertura das equipes e volume de inspeções "
    "realizadas por Líderes e Gerentes."
)


# ============================================================
# FUNÇÕES
# ============================================================

def normalizar_texto(valor):

    if pd.isna(valor):
        return ""

    valor = str(valor).strip().upper()

    return "".join(
        c
        for c in unicodedata.normalize("NFKD", valor)
        if not unicodedata.combining(c)
    )


def normalizar_id(serie):

    return (
        serie
        .astype(str)
        .str.strip()
        .str.replace(r"\.0$", "", regex=True)
    )


@st.cache_data
def carregar_dados(arquivo):

    return pd.read_excel(
        arquivo,
        sheet_name="Checklists Realizados"
    )


# ============================================================
# UPLOAD
# ============================================================

arquivo = st.file_uploader(
    "Selecione a planilha",
    type=["xlsx"]
)

if arquivo is None:
    st.stop()


# ============================================================
# CARREGAMENTO
# ============================================================

df = carregar_dados(arquivo)

df.columns = df.columns.str.strip()


# ============================================================
# TRATAMENTO
# ============================================================

df["Data de Execução"] = pd.to_datetime(
    df["Data de Execução"],
    errors="coerce"
)

df = df.dropna(
    subset=[
        "ID da Equipe",
        "Data de Execução"
    ]
)

df["ID da Equipe"] = normalizar_id(
    df["ID da Equipe"]
)


# ============================================================
# ANO
# ============================================================

anos = sorted(
    df["Data de Execução"]
    .dt.year
    .dropna()
    .unique()
)

ano = st.sidebar.selectbox(
    "Ano",
    anos,
    index=len(anos) - 1
)


# ============================================================
# PRIMEIRO SEMESTRE
# ============================================================

df = df[
    (df["Data de Execução"].dt.year == ano)
    &
    (df["Data de Execução"].dt.month.between(1, 6))
].copy()


# ============================================================
# UNIVERSO TOTAL DE EQUIPES
# ============================================================

# O universo é definido ANTES do filtro de liderança.
#
# Dessa forma, equipes que aparecem na base mas nunca
# receberam inspeção de Líder/Gerente continuam sendo
# consideradas como "sem contato".

todas_equipes = sorted(
    df["ID da Equipe"]
    .dropna()
    .unique()
)

total_equipes = len(todas_equipes)


if total_equipes == 0:

    st.warning(
        "Nenhuma equipe encontrada no período."
    )

    st.stop()


# ============================================================
# TOTAL DE INSPETORES
# ============================================================

total_inspetores = (
    df["Inspetor"]
    .dropna()
    .astype(str)
    .str.strip()
    .replace("", pd.NA)
    .dropna()
    .nunique()
)


# ============================================================
# FILTRO LÍDER / GERENTE
# ============================================================

df["Cargo Normalizado"] = (
    df["Cargo"]
    .fillna("")
    .apply(normalizar_texto)
)

padrao_lideranca = (
    r"\bLIDER\b|"
    r"\bGERENTE\b|"
    r"\bGTE\b"
)

df_lideranca = df[
    df["Cargo Normalizado"].str.contains(
        padrao_lideranca,
        regex=True,
        na=False
    )
].copy()


# ============================================================
# MÊS
# ============================================================

df_lideranca["Mês Número"] = (
    df_lideranca["Data de Execução"]
    .dt.month
)


meses = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho"
}


df_lideranca["Mês"] = (
    df_lideranca["Mês Número"]
    .map(meses)
)


# ============================================================
# TOTAL DE LÍDERES / GERENTES
# ============================================================

total_lideres = (
    df_lideranca["Inspetor"]
    .dropna()
    .astype(str)
    .str.strip()
    .replace("", pd.NA)
    .dropna()
    .nunique()
)


# ============================================================
# QUANTIDADE DE INSPEÇÕES DISTINTAS POR EQUIPE / MÊS
# ============================================================

# Essa é uma das principais mudanças.
#
# Uma inspeção pode aparecer várias vezes na planilha
# devido aos membros / itens.
#
# Portanto:
#
# Equipe A + Janeiro + Inspeção 123
#
# vale apenas UMA inspeção.
#
# Porém, se a mesma equipe tiver:
#
# Inspeção 123
# Inspeção 456
# Inspeção 789
#
# então exibimos 3 inspeções para aquela equipe no mês.

inspecoes_equipe_mes = (
    df_lideranca
    .groupby(
        [
            "ID da Equipe",
            "Mês Número"
        ]
    )["Inspeção"]
    .nunique()
    .unstack(fill_value=0)
)


# ============================================================
# INCLUI EQUIPES SEM CONTATO
# ============================================================

inspecoes_equipe_mes = (
    inspecoes_equipe_mes
    .reindex(
        index=todas_equipes,
        fill_value=0
    )
)


# ============================================================
# GARANTE OS 6 MESES
# ============================================================

inspecoes_equipe_mes = (
    inspecoes_equipe_mes
    .reindex(
        columns=[1, 2, 3, 4, 5, 6],
        fill_value=0
    )
)


inspecoes_equipe_mes.columns = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho"
]


# ============================================================
# CONTATO SIM / NÃO
# ============================================================

# Aqui a quantidade vira apenas um indicador lógico
# para calcular a cobertura.
#
# 0 inspeções = sem contato
# 1 ou mais = com contato

teve_contato = (
    inspecoes_equipe_mes > 0
)


# ============================================================
# CONTATO T1
# ============================================================

contato_t1_equipe = (
    teve_contato[
        [
            "Janeiro",
            "Fevereiro",
            "Março"
        ]
    ]
    .any(axis=1)
)


# ============================================================
# CONTATO T2
# ============================================================

contato_t2_equipe = (
    teve_contato[
        [
            "Abril",
            "Maio",
            "Junho"
        ]
    ]
    .any(axis=1)
)


# ============================================================
# CONTATO NO SEMESTRE
# ============================================================

contato_semestre_equipe = (
    teve_contato.any(axis=1)
)


# ============================================================
# QUANTIDADES TRIMESTRAIS
# ============================================================

equipes_contato_t1 = (
    contato_t1_equipe.sum()
)

equipes_contato_t2 = (
    contato_t2_equipe.sum()
)


equipes_sem_contato_t1 = (
    total_equipes
    - equipes_contato_t1
)

equipes_sem_contato_t2 = (
    total_equipes
    - equipes_contato_t2
)


# ============================================================
# TAXAS
# ============================================================

taxa_t1 = (
    equipes_contato_t1
    / total_equipes
)

taxa_t2 = (
    equipes_contato_t2
    / total_equipes
)


# ============================================================
# SEM NENHUM CONTATO NO SEMESTRE
# ============================================================

equipes_com_contato_semestre = (
    contato_semestre_equipe.sum()
)

equipes_sem_contato_semestre = (
    total_equipes
    - equipes_com_contato_semestre
)

taxa_sem_contato_semestre = (
    equipes_sem_contato_semestre
    / total_equipes
)


# ============================================================
# RESUMO MENSAL
# ============================================================

resumo_mensal = []


for numero_mes, nome_mes in meses.items():

    # ----------------------------------------
    # Equipes com contato
    # ----------------------------------------

    com_contato = (
        teve_contato[nome_mes]
        .sum()
    )


    # ----------------------------------------
    # Equipes sem contato
    # ----------------------------------------

    sem_contato = (
        total_equipes
        - com_contato
    )


    # ----------------------------------------
    # Taxa mensal
    # ----------------------------------------

    taxa_contato = (
        com_contato
        / total_equipes
    )


    # ----------------------------------------
    # Inspeções distintas
    # ----------------------------------------

    inspecoes_distintas = (
        df_lideranca[
            df_lideranca["Mês Número"] == numero_mes
        ]["Inspeção"]
        .nunique()
    )


    # ----------------------------------------
    # Líderes ativos no mês
    # ----------------------------------------

    lideres_ativos = (
        df_lideranca[
            df_lideranca["Mês Número"] == numero_mes
        ]["Inspetor"]
        .dropna()
        .astype(str)
        .str.strip()
        .replace("", pd.NA)
        .dropna()
        .nunique()
    )


    # ----------------------------------------
    # Presença de líderes
    # ----------------------------------------

    if total_lideres > 0:

        presenca_lideres = (
            lideres_ativos
            / total_lideres
        )

    else:

        presenca_lideres = 0


    # ----------------------------------------
    # Trimestre
    # ----------------------------------------

    trimestre = (
        "T1"
        if numero_mes <= 3
        else "T2"
    )


    resumo_mensal.append({

        "Trimestre": trimestre,

        "Mês": nome_mes,

        "Com contato": com_contato,

        "Sem contato": sem_contato,

        "Taxa de contato": taxa_contato,

        "Inspeções distintas": inspecoes_distintas,

        "Líderes ativos": lideres_ativos,

        "Presença de líderes": presenca_lideres

    })


resumo_mensal = pd.DataFrame(
    resumo_mensal
)


# ============================================================
# MÉDIA DE EQUIPES COM CONTATO POR MÊS
# ============================================================

media_equipes_mes = (
    resumo_mensal["Com contato"]
    .mean()
)


# ============================================================
# MÉDIA DE PRESENÇA DOS LÍDERES
# ============================================================

media_presenca_lideres = (
    resumo_mensal["Presença de líderes"]
    .mean()
)


# ============================================================
# CARDS - TAXA DE CONTATO
# ============================================================

st.subheader(
    "Indicadores de cobertura"
)

c1, c2, c3 = st.columns(3)


c1.metric(
    "Taxa de Contato T1",
    f"{taxa_t1:.1%}",
    f"{equipes_contato_t1} equipes"
)


c2.metric(
    "Taxa de Contato T2",
    f"{taxa_t2:.1%}",
    f"{equipes_contato_t2} equipes"
)


c3.metric(
    "Sem contato no semestre",
    f"{equipes_sem_contato_semestre}",
    f"{taxa_sem_contato_semestre:.1%} do total"
)


# ============================================================
# CARDS - CONTEXTO
# ============================================================

st.subheader(
    "Visão geral"
)

c1, c2, c3, c4, c5 = st.columns(5)


c1.metric(
    "Total de equipes",
    f"{total_equipes:,}".replace(",", ".")
)


c2.metric(
    "Média de equipes / mês",
    f"{media_equipes_mes:.0f}",
    "com contato"
)


c3.metric(
    "Líderes / Gerentes",
    total_lideres
)


c4.metric(
    "Presença média da liderança",
    f"{media_presenca_lideres:.1%}"
)


c5.metric(
    "Total de inspetores",
    total_inspetores
)


# ============================================================
# CORES
# ============================================================

# T1 = tonalidade clara
# T2 = tonalidade escura

AZUL_T1 = "#7CB9E8"

AZUL_T2 = "#1F4E79"

CINZA_T1 = "#DCE6EF"

CINZA_T2 = "#697B8C"


# ============================================================
# GRÁFICO - COM CONTATO VS SEM CONTATO POR MÊS
# ============================================================

st.subheader(
    "Cobertura mensal das equipes"
)


cores_com_contato = [
    AZUL_T1,
    AZUL_T1,
    AZUL_T1,
    AZUL_T2,
    AZUL_T2,
    AZUL_T2
]


cores_sem_contato = [
    CINZA_T1,
    CINZA_T1,
    CINZA_T1,
    CINZA_T2,
    CINZA_T2,
    CINZA_T2
]


fig_mensal = go.Figure()


fig_mensal.add_trace(

    go.Bar(

        name="Com contato",

        x=resumo_mensal["Mês"],

        y=resumo_mensal["Com contato"],

        text=resumo_mensal["Com contato"],

        textposition="inside",

        marker_color=cores_com_contato,

        customdata=(
            resumo_mensal[
                [
                    "Taxa de contato",
                    "Inspeções distintas"
                ]
            ]
            .to_numpy()
        ),

        hovertemplate=(
            "<b>%{x}</b><br>"
            "Com contato: %{y}<br>"
            "Taxa: %{customdata[0]:.1%}<br>"
            "Inspeções distintas: %{customdata[1]}"
            "<extra></extra>"
        )
    )
)


fig_mensal.add_trace(

    go.Bar(

        name="Sem contato",

        x=resumo_mensal["Mês"],

        y=resumo_mensal["Sem contato"],

        text=resumo_mensal["Sem contato"],

        textposition="inside",

        marker_color=cores_sem_contato,

        hovertemplate=(
            "<b>%{x}</b><br>"
            "Sem contato: %{y}"
            "<extra></extra>"
        )
    )
)


fig_mensal.update_layout(

    barmode="stack",

    title=(
        "Equipes com contato vs. sem contato por mês"
    ),

    xaxis_title="",

    yaxis_title="Quantidade de equipes",

    legend_title="Status",

    hovermode="x unified"
)


st.plotly_chart(
    fig_mensal,
    use_container_width=True
)


st.caption(
    "Janeiro a março representam o 1º trimestre em tom claro. "
    "Abril a junho representam o 2º trimestre em tom mais escuro."
)


# ============================================================
# TAXA TRIMESTRAL
# ============================================================

st.subheader(
    "Taxa de contato por trimestre"
)


dados_trimestre = pd.DataFrame({

    "Trimestre": [
        "T1",
        "T2"
    ],

    "Taxa": [
        taxa_t1 * 100,
        taxa_t2 * 100
    ],

    "Equipes": [
        equipes_contato_t1,
        equipes_contato_t2
    ]
})


fig_trimestre = go.Figure()


fig_trimestre.add_trace(

    go.Bar(

        x=dados_trimestre["Trimestre"],

        y=dados_trimestre["Taxa"],

        marker_color=[
            AZUL_T1,
            AZUL_T2
        ],

        text=[
            f"{taxa_t1:.1%}",
            f"{taxa_t2:.1%}"
        ],

        textposition="outside",

        customdata=dados_trimestre[
            ["Equipes"]
        ],

        hovertemplate=(
            "<b>%{x}</b><br>"
            "Taxa: %{y:.1f}%<br>"
            "Equipes com contato: %{customdata[0]}"
            "<extra></extra>"
        )
    )
)


fig_trimestre.update_layout(

    title="Cobertura trimestral",

    xaxis_title="",

    yaxis_title="Taxa de contato (%)",

    yaxis_range=[
        0,
        100
    ],

    showlegend=False
)


st.plotly_chart(
    fig_trimestre,
    use_container_width=True
)


# ============================================================
# PRESENÇA DOS LÍDERES
# ============================================================

st.subheader(
    "Presença mensal da liderança"
)


cores_lideres = [
    AZUL_T1,
    AZUL_T1,
    AZUL_T1,
    AZUL_T2,
    AZUL_T2,
    AZUL_T2
]


fig_lideres = go.Figure()


fig_lideres.add_trace(

    go.Bar(

        x=resumo_mensal["Mês"],

        y=resumo_mensal["Líderes ativos"],

        marker_color=cores_lideres,

        text=[
            (
                f"{ativos} "
                f"({presenca:.0%})"
            )

            for ativos, presenca in zip(
                resumo_mensal["Líderes ativos"],
                resumo_mensal["Presença de líderes"]
            )
        ],

        textposition="outside",

        hovertemplate=(
            "<b>%{x}</b><br>"
            "Líderes ativos: %{y}"
            "<extra></extra>"
        )
    )
)


fig_lideres.update_layout(

    title=(
        "Quantidade de Líderes/Gerentes "
        "com pelo menos uma inspeção no mês"
    ),

    xaxis_title="",

    yaxis_title="Líderes ativos",

    showlegend=False
)


st.plotly_chart(
    fig_lideres,
    use_container_width=True
)


# ============================================================
# RESUMO MENSAL
# ============================================================

st.subheader(
    "Resumo mensal"
)


resumo_visual = resumo_mensal.copy()


resumo_visual["Taxa de contato"] = (
    resumo_visual["Taxa de contato"]
    .map(
        lambda x: f"{x:.1%}"
    )
)


resumo_visual["Presença de líderes"] = (
    resumo_visual["Presença de líderes"]
    .map(
        lambda x: f"{x:.1%}"
    )
)


st.dataframe(
    resumo_visual,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# INSPEÇÕES DISTINTAS POR EQUIPE / MÊS
# ============================================================

st.subheader(
    "Quantidade de inspeções por equipe"
)

st.caption(
    "Cada célula representa a quantidade de inspeções distintas "
    "realizadas naquela equipe durante o mês."
)


tabela_equipes = (
    inspecoes_equipe_mes
    .copy()
)


# ============================================================
# TOTAL DE INSPEÇÕES DISTINTAS POR EQUIPE
# ============================================================

total_inspecoes_por_equipe = (
    df_lideranca
    .groupby(
        "ID da Equipe"
    )["Inspeção"]
    .nunique()
)


tabela_equipes[
    "Total de inspeções distintas"
] = (

    tabela_equipes
    .index
    .map(
        total_inspecoes_por_equipe
    )
)


tabela_equipes[
    "Total de inspeções distintas"
] = (

    tabela_equipes[
        "Total de inspeções distintas"
    ]
    .fillna(0)
    .astype(int)
)


# ============================================================
# MESES COM CONTATO
# ============================================================

tabela_equipes[
    "Meses com contato"
] = (

    (
        tabela_equipes[
            [
                "Janeiro",
                "Fevereiro",
                "Março",
                "Abril",
                "Maio",
                "Junho"
            ]
        ] > 0
    )
    .sum(axis=1)
)


tabela_equipes = (
    tabela_equipes
    .reset_index()
)


# ============================================================
# FILTRO DA TABELA
# ============================================================

opcao = st.radio(

    "Mostrar",

    [
        "Todas as equipes",
        "Somente equipes sem contato",
        "Somente equipes com contato"
    ],

    horizontal=True
)


if opcao == "Somente equipes sem contato":

    tabela_exibicao = tabela_equipes[
        tabela_equipes[
            "Total de inspeções distintas"
        ] == 0
    ]


elif opcao == "Somente equipes com contato":

    tabela_exibicao = tabela_equipes[
        tabela_equipes[
            "Total de inspeções distintas"
        ] > 0
    ]


else:

    tabela_exibicao = (
        tabela_equipes.copy()
    )


st.dataframe(
    tabela_exibicao,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# VALIDAÇÃO
# ============================================================

with st.expander(
    "Validação dos cálculos"
):

    st.write(
        f"**Total de equipes:** {total_equipes}"
    )

    st.write(
        f"**Equipes com contato no T1:** "
        f"{equipes_contato_t1}"
    )

    st.write(
        f"**Equipes sem contato no T1:** "
        f"{equipes_sem_contato_t1}"
    )

    st.write(
        f"**Equipes com contato no T2:** "
        f"{equipes_contato_t2}"
    )

    st.write(
        f"**Equipes sem contato no T2:** "
        f"{equipes_sem_contato_t2}"
    )

    st.write(
        f"**Equipes sem nenhum contato no semestre:** "
        f"{equipes_sem_contato_semestre}"
    )

    st.write(
        f"**Líderes/Gerentes distintos:** "
        f"{total_lideres}"
    )

    st.write(
        f"**Inspetores distintos na base:** "
        f"{total_inspetores}"
    )