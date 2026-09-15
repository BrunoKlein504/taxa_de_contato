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

import base64
import unicodedata
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Operação Segura | Taxa de Contato",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PALETA - IDENTIDADE VISUAL
# ============================================================

AZUL_PRINCIPAL = "#2161DD"
AZUL_EQTL = "#005BCD"
AZUL_ESCURO = "#002060"
AZUL_MEDIO = "#4472C4"
AZUL_CLARO = "#7CB9E8"

AMARELO = "#FFC000"
LARANJA = "#FD8C03"
VERDE = "#00B050"

CINZA_FUNDO = "#F5F7FB"
CINZA_BORDA = "#E2E8F0"
CINZA_TEXTO = "#5F6B7A"

BRANCO = "#FFFFFF"
PRETO = "#242424"


# ============================================================
# CAMINHOS
# ============================================================

try:
    BASE_DIR = Path(__file__).resolve().parent
except NameError:
    BASE_DIR = Path.cwd()


LOGO_JORNADA = BASE_DIR / "jornada_seguranca.png"
LOGO_EQTL = BASE_DIR / "marca_equatorial.png"


# ============================================================
# FUNÇÃO PARA CONVERTER IMAGEM EM BASE64
# ============================================================

def imagem_base64(caminho):

    if not caminho.exists():
        return None

    with open(caminho, "rb") as arquivo:
        return base64.b64encode(
            arquivo.read()
        ).decode()


logo_jornada_b64 = imagem_base64(
    LOGO_JORNADA
)

logo_eqtl_b64 = imagem_base64(
    LOGO_EQTL
)


# ============================================================
# CSS GLOBAL
# ============================================================

st.html(
    f"""
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap'
    );

    html,
    body,
    [class*="css"] {{
        font-family:
            'Montserrat',
            'Segoe UI',
            sans-serif;
    }}

    .stApp {{
        background: {CINZA_FUNDO};
    }}

    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }}


    /* =======================================================
       SIDEBAR
    ======================================================= */

    [data-testid="stSidebar"] {{
        background:
            linear-gradient(
                180deg,
                {AZUL_ESCURO} 0%,
                {AZUL_EQTL} 100%
            );
    }}

    [data-testid="stSidebar"] * {{
        color: white;
    }}

    [data-testid="stSidebar"] label {{
        font-weight: 600;
    }}


    /* =======================================================
       HERO / CABEÇALHO
    ======================================================= */

    .hero {{
        background:
            linear-gradient(
                120deg,
                {AZUL_ESCURO} 0%,
                {AZUL_EQTL} 65%,
                {AZUL_PRINCIPAL} 100%
            );

        border-radius: 26px;

        padding:
            42px 44px;

        margin-bottom:
            32px;

        box-shadow:
            0 14px 32px
            rgba(
                0,
                32,
                96,
                .14
            );

        position: relative;
        overflow: hidden;
    }}

    .hero::after {{
        content: "";

        position: absolute;

        width: 340px;
        height: 340px;

        border-radius: 50%;

        background:
            rgba(
                255,
                192,
                0,
                .10
            );

        right: -90px;
        top: -165px;
    }}

    .hero-grid {{
        display: flex;

        align-items: center;

        justify-content:
            space-between;

        gap: 40px;

        position: relative;

        z-index: 2;
    }}

    .hero-text {{
        flex: 1;
    }}

    .hero-tag {{
        display: inline-block;

        background:
            {AMARELO};

        color:
            {AZUL_ESCURO};

        padding:
            7px 16px;

        border-radius:
            999px;

        font-size:
            12px;

        font-weight:
            800;

        letter-spacing:
            .4px;

        margin-bottom:
            16px;
    }}

    .hero-title {{
        color:
            white;

        font-size:
            42px;

        font-weight:
            900;

        line-height:
            1.08;

        margin:
            0;
    }}

    .hero-title-highlight {{
        color:
            {AMARELO};
    }}

    .hero-subtitle {{
        color:
            rgba(
                255,
                255,
                255,
                .88
            );

        font-size:
            15px;

        font-weight:
            500;

        margin-top:
            14px;

        margin-bottom:
            0;

        line-height:
            1.5;
    }}


    /* =======================================================
       LOGO DA JORNADA
    ======================================================= */

    .hero-logo-container {{
        min-width:
            300px;

        display:
            flex;

        align-items:
            center;

        justify-content:
            center;
    }}

    .hero-logo-box {{
        background:
            rgba(
                255,
                255,
                255,
                .12
            );

        border:
            1px solid
            rgba(
                255,
                255,
                255,
                .20
            );

        border-radius:
            22px;

        padding:
            12px;

        box-shadow:
            0 10px 28px
            rgba(
                0,
                0,
                0,
                .08
            );

        backdrop-filter:
            blur(4px);

        -webkit-backdrop-filter:
            blur(4px);
    }}

    .hero-logo-inner {{
        background:
            rgba(
                255,
                255,
                255,
                .88
            );

        border-radius:
            16px;

        padding:
            14px 18px;

        display:
            flex;

        align-items:
            center;

        justify-content:
            center;
    }}

    .hero-logo {{
        width:
            265px;

        max-height:
            105px;

        object-fit:
            contain;
    }}


    /* =======================================================
       RESPONSIVIDADE
    ======================================================= */

    @media (max-width: 900px) {{

        .hero {{
            padding:
                32px 28px;
        }}

        .hero-grid {{
            flex-direction:
                column;

            align-items:
                flex-start;
        }}

        .hero-title {{
            font-size:
                34px;
        }}

        .hero-logo-container {{
            min-width:
                0;

            width:
                100%;
        }}

        .hero-logo {{
            width:
                220px;
        }}

    }}


    /* =======================================================
       TÍTULOS DE SEÇÃO
    ======================================================= */

    .section-title {{
        border-left:
            6px solid
            {AMARELO};

        padding-left:
            14px;

        margin-top:
            30px;

        margin-bottom:
            18px;
    }}

    .section-title h2 {{
        color:
            {AZUL_ESCURO};

        font-size:
            22px;

        font-weight:
            900;

        margin:
            0;
    }}

    .section-title p {{
        color:
            {CINZA_TEXTO};

        font-size:
            12px;

        margin:
            5px 0 0 0;
    }}


    /* =======================================================
       CARDS
    ======================================================= */

    .kpi-card {{
        background:
            {BRANCO};

        border:
            1px solid
            {CINZA_BORDA};

        border-radius:
            17px;

        min-height:
            125px;

        padding:
            19px 20px;

        box-shadow:
            0 5px 15px
            rgba(
                0,
                32,
                96,
                .05
            );

        position:
            relative;

        overflow:
            hidden;
    }}

    .kpi-card::before {{
        content: "";

        position:
            absolute;

        top:
            0;

        bottom:
            0;

        left:
            0;

        width:
            5px;

        background:
            var(--accent);
    }}

    .kpi-label {{
        color:
            {CINZA_TEXTO};

        font-size:
            11px;

        font-weight:
            800;

        letter-spacing:
            .2px;

        text-transform:
            uppercase;

        margin-bottom:
            8px;
    }}

    .kpi-value {{
        color:
            {AZUL_ESCURO};

        font-size:
            29px;

        font-weight:
            900;

        line-height:
            1;

        margin-bottom:
            9px;
    }}

    .kpi-subtitle {{
        color:
            {CINZA_TEXTO};

        font-size:
            11px;

        font-weight:
            500;

        line-height:
            1.4;
    }}


    /* =======================================================
       BOX DE INFORMAÇÃO
    ======================================================= */

    .info-box {{
        background:
            {BRANCO};

        border:
            1px solid
            {CINZA_BORDA};

        border-left:
            5px solid
            {AZUL_PRINCIPAL};

        padding:
            16px 18px;

        border-radius:
            12px;

        color:
            {PRETO};

        font-size:
            13px;

        margin:
            12px 0;
    }}


    .warning-box {{
        background:
            #FFF8E5;

        border:
            1px solid
            #FFE093;

        border-left:
            5px solid
            {AMARELO};

        padding:
            17px 20px;

        border-radius:
            12px;

        color:
            {AZUL_ESCURO};

        font-size:
            13px;

        line-height:
            1.6;

        margin:
            15px 0;
    }}


    /* =======================================================
       DATAFRAME
    ======================================================= */

    [data-testid="stDataFrame"] {{
        background:
            white;

        border:
            1px solid
            {CINZA_BORDA};

        border-radius:
            14px;

        overflow:
            hidden;
    }}


    /* =======================================================
       FILE UPLOADER
    ======================================================= */

    [data-testid="stFileUploader"] {{
        background:
            white;

        border:
            1px solid
            {CINZA_BORDA};

        border-radius:
            14px;

        padding:
            5px 10px;
    }}


    /* =======================================================
       EXPANDER
    ======================================================= */

    [data-testid="stExpander"] {{
        background:
            white;

        border:
            1px solid
            {CINZA_BORDA};

        border-radius:
            12px;
    }}


    /* =======================================================
       RADIO
    ======================================================= */

    div[role="radiogroup"] {{
        background:
            white;

        padding:
            8px 12px;

        border-radius:
            12px;

        border:
            1px solid
            {CINZA_BORDA};
    }}

    </style>
    """
)


# ============================================================
# COMPONENTES
# ============================================================

def titulo_secao(
    titulo,
    subtitulo=""
):

    st.html(
        f"""
        <div class="section-title">

            <h2>
                {titulo}
            </h2>

            <p>
                {subtitulo}
            </p>

        </div>
        """
    )


def card_kpi(
    titulo,
    valor,
    subtitulo="",
    cor=AZUL_PRINCIPAL
):

    st.html(
        f"""
        <div
            class="kpi-card"
            style="--accent:{cor};"
        >

            <div class="kpi-label">
                {titulo}
            </div>

            <div class="kpi-value">
                {valor}
            </div>

            <div class="kpi-subtitle">
                {subtitulo}
            </div>

        </div>
        """
    )


def aplicar_layout_plotly(
    fig,
    titulo=None
):

    fig.update_layout(

        font=dict(
            family="Montserrat",
            color=PRETO
        ),

        paper_bgcolor=
            "rgba(0,0,0,0)",

        plot_bgcolor=
            BRANCO,

        margin=dict(
            l=35,
            r=25,
            t=70,
            b=35
        ),

        title=dict(
            text=titulo,

            font=dict(
                size=17,
                color=AZUL_ESCURO,
                family="Montserrat"
            )
        ),

        legend=dict(
            title="",

            orientation="h",

            yanchor="bottom",
            y=1.02,

            xanchor="right",
            x=1
        ),

        hoverlabel=dict(
            font_family="Montserrat"
        )
    )


    fig.update_xaxes(
        showgrid=False,
        linecolor=CINZA_BORDA
    )


    fig.update_yaxes(
        gridcolor="#EDF1F7",
        zeroline=False
    )


    return fig


# ============================================================
# HERO
# ============================================================

if logo_jornada_b64:

    logo_html = (
        f"""
        <div class="hero-logo-container">

            <div class="hero-logo-box">

                <div class="hero-logo-inner">

                    <img
                        class="hero-logo"
                        src="data:image/png;base64,{logo_jornada_b64}"
                    >

                </div>

            </div>

        </div>
        """
    )

else:

    logo_html = ""


st.html(
    f"""
    <div class="hero">

        <div class="hero-grid">

            <div class="hero-text">

                <div class="hero-tag">
                    Pilar Liderança
                </div>

                <h1 class="hero-title">

                    Operação Segura

                    <span class="hero-title-highlight">
                        | Taxa de Contato
                    </span>

                </h1>

                <p class="hero-subtitle">

                    Jornada de Segurança 2026 •

                    Cobertura, presença da liderança e
                    conformidade das inspeções

                </p>

            </div>

            {logo_html}

        </div>

    </div>
    """
)


# ============================================================
# SIDEBAR
# ============================================================

if logo_eqtl_b64:

    st.sidebar.html(
        f"""
        <div
            style="
                background:white;
                padding:14px;
                border-radius:16px;
                margin-bottom:22px;
                text-align:center;
            "
        >

            <img
                src="data:image/png;base64,{logo_eqtl_b64}"

                style="
                    width:100%;
                    max-width:220px;
                    object-fit:contain;
                "
            >

        </div>
        """
    )


st.sidebar.markdown(
    "### Configuração"
)


# ============================================================
# FUNÇÕES DE DADOS
# ============================================================

def normalizar_texto(
    valor
):

    if pd.isna(valor):
        return ""

    valor = (
        str(valor)
        .strip()
        .upper()
    )

    return "".join(

        c

        for c in unicodedata.normalize(
            "NFKD",
            valor
        )

        if not unicodedata.combining(c)
    )


def normalizar_id(
    serie
):

    return (

        serie

        .astype(str)

        .str.strip()

        .str.replace(
            r"\.0$",
            "",
            regex=True
        )
    )


@st.cache_data
def carregar_dados(
    arquivo
):

    return pd.read_excel(
        arquivo,
        sheet_name="Checklists Realizados"
    )


# ============================================================
# UPLOAD
# ============================================================

arquivo = st.file_uploader(
    "Selecione a base ESS",
    type=["xlsx"]
)


if arquivo is None:

    st.html(
        """
        <div class="info-box">

            <strong>
                Carregue a planilha do ESS
            </strong>

            para iniciar a análise da
            Taxa de Contato.

        </div>
        """
    )

    st.stop()


# ============================================================
# CARREGAMENTO
# ============================================================

df = carregar_dados(
    arquivo
)


df.columns = (
    df.columns
    .str.strip()
)


# ============================================================
# DATA
# ============================================================

df[
    "Data de Execução"
] = pd.to_datetime(

    df[
        "Data de Execução"
    ],

    errors="coerce"
)


df = df.dropna(

    subset=[

        "ID da Equipe",

        "Data de Execução"
    ]
)


df[
    "ID da Equipe"
] = normalizar_id(

    df[
        "ID da Equipe"
    ]
)


# ============================================================
# NORMALIZAÇÃO
# ============================================================

df[
    "Cargo Normalizado"
] = (

    df[
        "Cargo"
    ]

    .fillna("")

    .apply(
        normalizar_texto
    )
)


df[
    "Conformidade Normalizada"
] = (

    df[
        "Conformidade"
    ]

    .fillna("")

    .apply(
        normalizar_texto
    )
)


# ============================================================
# ANO
# ============================================================

anos = sorted(

    df[
        "Data de Execução"
    ]

    .dt.year

    .dropna()

    .unique()
)


ano = st.sidebar.selectbox(

    "Ano de análise",

    anos,

    index=
        len(anos) - 1
)


# ============================================================
# PRIMEIRO SEMESTRE
# ============================================================

df = df[

    (
        df[
            "Data de Execução"
        ]
        .dt.year
        == ano
    )

    &

    (
        df[
            "Data de Execução"
        ]
        .dt.month
        .between(
            1,
            6
        )
    )

].copy()


# ============================================================
# MÊS
# ============================================================

meses = {

    1: "Janeiro",

    2: "Fevereiro",

    3: "Março",

    4: "Abril",

    5: "Maio",

    6: "Junho"
}


ordem_meses = list(
    meses.values()
)


df[
    "Mês Número"
] = (

    df[
        "Data de Execução"
    ]
    .dt.month
)


df[
    "Mês"
] = (

    df[
        "Mês Número"
    ]
    .map(
        meses
    )
)


# ============================================================
# UNIVERSO DE EQUIPES
# ============================================================

todas_equipes = sorted(

    df[
        "ID da Equipe"
    ]

    .dropna()

    .unique()
)


total_equipes = len(
    todas_equipes
)


if total_equipes == 0:

    st.warning(
        "Nenhuma equipe encontrada."
    )

    st.stop()


# ============================================================
# INSPETORES
# ============================================================

total_inspetores = (

    df[
        "Inspetor"
    ]

    .dropna()

    .astype(str)

    .str.strip()

    .replace(
        "",
        pd.NA
    )

    .dropna()

    .nunique()
)


# ============================================================
# FILTRO DE LIDERANÇA
# ============================================================

padrao_lideranca = (

    r"\bLIDER\b|"

    r"\bGERENTE\b|"

    r"\bGTE\b"
)


mascara_lideranca = (

    df[
        "Cargo Normalizado"
    ]

    .str.contains(

        padrao_lideranca,

        regex=True,

        na=False
    )
)


df_lideranca = (

    df[
        mascara_lideranca
    ]

    .copy()
)


df_outros_cargos = (

    df[
        ~mascara_lideranca
    ]

    .copy()
)


# ============================================================
# LÍDERES
# ============================================================

total_lideres = (

    df_lideranca[
        "Inspetor"
    ]

    .dropna()

    .astype(str)

    .str.strip()

    .replace(
        "",
        pd.NA
    )

    .dropna()

    .nunique()
)


# ============================================================
# INSPEÇÕES DISTINTAS POR EQUIPE / MÊS
# ============================================================

inspecoes_equipe_mes = (

    df_lideranca

    .groupby(
        [
            "ID da Equipe",
            "Mês Número"
        ]
    )[
        "Inspeção"
    ]

    .nunique()

    .unstack(
        fill_value=0
    )
)


inspecoes_equipe_mes = (

    inspecoes_equipe_mes

    .reindex(

        index=
            todas_equipes,

        fill_value=0
    )
)


inspecoes_equipe_mes = (

    inspecoes_equipe_mes

    .reindex(

        columns=[
            1,
            2,
            3,
            4,
            5,
            6
        ],

        fill_value=0
    )
)


inspecoes_equipe_mes.columns = (
    ordem_meses
)


# ============================================================
# CONTATO
# ============================================================

teve_contato = (
    inspecoes_equipe_mes
    > 0
)


contato_t1_equipe = (

    teve_contato[
        [
            "Janeiro",
            "Fevereiro",
            "Março"
        ]
    ]

    .any(
        axis=1
    )
)


contato_t2_equipe = (

    teve_contato[
        [
            "Abril",
            "Maio",
            "Junho"
        ]
    ]

    .any(
        axis=1
    )
)


contato_semestre_equipe = (

    teve_contato

    .any(
        axis=1
    )
)


# ============================================================
# QUANTIDADES / TAXAS
# ============================================================

equipes_contato_t1 = int(
    contato_t1_equipe.sum()
)

equipes_contato_t2 = int(
    contato_t2_equipe.sum()
)


equipes_sem_contato_t1 = (
    total_equipes
    -
    equipes_contato_t1
)


equipes_sem_contato_t2 = (
    total_equipes
    -
    equipes_contato_t2
)


equipes_com_contato_semestre = int(
    contato_semestre_equipe.sum()
)


equipes_sem_contato_semestre = (
    total_equipes
    -
    equipes_com_contato_semestre
)


taxa_t1 = (
    equipes_contato_t1
    /
    total_equipes
)


taxa_t2 = (
    equipes_contato_t2
    /
    total_equipes
)


taxa_sem_contato_semestre = (
    equipes_sem_contato_semestre
    /
    total_equipes
)


# ============================================================
# EQUIPES SEM CONTATO DA LIDERANÇA
# ============================================================

ids_sem_contato = (

    contato_semestre_equipe[
        ~contato_semestre_equipe
    ]

    .index

    .tolist()
)


# ============================================================
# OUTROS CARGOS
# ============================================================

outros_sem_contato = (

    df_outros_cargos[

        df_outros_cargos[
            "ID da Equipe"
        ]

        .isin(
            ids_sem_contato
        )
    ]

    .copy()
)


equipes_inspecionadas_outros = (

    outros_sem_contato[
        "ID da Equipe"
    ]

    .nunique()
)


inspecoes_outros_sem_contato = (

    outros_sem_contato[
        "Inspeção"
    ]

    .nunique()
)


if equipes_inspecionadas_outros > 0:

    media_outros_por_equipe = (

        inspecoes_outros_sem_contato
        /
        equipes_inspecionadas_outros
    )

else:

    media_outros_por_equipe = 0


# ============================================================
# CARGOS DAS EQUIPES SEM CONTATO
# ============================================================

cargos_sem_contato = (

    outros_sem_contato

    .groupby(
        "Cargo Normalizado"
    )

    .agg(

        Equipes=(
            "ID da Equipe",
            "nunique"
        ),

        Inspeções=(
            "Inspeção",
            "nunique"
        ),

        Inspetores=(
            "Inspetor",
            "nunique"
        )
    )

    .reset_index()
)


cargos_sem_contato = (

    cargos_sem_contato[

        cargos_sem_contato[
            "Cargo Normalizado"
        ]
        != ""
    ]

    .sort_values(
        "Equipes",
        ascending=False
    )
)


# ============================================================
# RESUMO MENSAL
# ============================================================

resumo_mensal = []


for numero_mes, nome_mes in meses.items():

    com_contato = int(

        teve_contato[
            nome_mes
        ]

        .sum()
    )


    sem_contato = (
        total_equipes
        -
        com_contato
    )


    taxa = (
        com_contato
        /
        total_equipes
    )


    inspecoes_distintas = (

        df_lideranca[

            df_lideranca[
                "Mês Número"
            ]
            == numero_mes

        ][
            "Inspeção"
        ]

        .nunique()
    )


    lideres_ativos = (

        df_lideranca[

            df_lideranca[
                "Mês Número"
            ]
            == numero_mes

        ][
            "Inspetor"
        ]

        .dropna()

        .astype(str)

        .str.strip()

        .replace(
            "",
            pd.NA
        )

        .dropna()

        .nunique()
    )


    if total_lideres > 0:

        presenca = (
            lideres_ativos
            /
            total_lideres
        )

    else:

        presenca = 0


    resumo_mensal.append({

        "Trimestre":
            "T1"
            if numero_mes <= 3
            else "T2",

        "Mês":
            nome_mes,

        "Com contato":
            com_contato,

        "Sem contato":
            sem_contato,

        "Taxa de contato":
            taxa,

        "Inspeções distintas":
            inspecoes_distintas,

        "Líderes ativos":
            lideres_ativos,

        "Presença de líderes":
            presenca

    })


resumo_mensal = pd.DataFrame(
    resumo_mensal
)


media_equipes_mes = (

    resumo_mensal[
        "Com contato"
    ]

    .mean()
)


media_presenca_lideres = (

    resumo_mensal[
        "Presença de líderes"
    ]

    .mean()
)


# ============================================================
# INDICADORES DE COBERTURA
# ============================================================

titulo_secao(
    "Indicadores de cobertura",
    "Cobertura das equipes pela liderança no primeiro semestre."
)


c1, c2, c3 = st.columns(3)


with c1:

    card_kpi(
        "Taxa de Contato T1",
        f"{taxa_t1:.1%}",
        f"{equipes_contato_t1} equipes cobertas",
        AZUL_CLARO
    )


with c2:

    card_kpi(
        "Taxa de Contato T2",
        f"{taxa_t2:.1%}",
        f"{equipes_contato_t2} equipes cobertas",
        AZUL_PRINCIPAL
    )


with c3:

    card_kpi(
        "Sem contato no semestre",
        equipes_sem_contato_semestre,
        f"{taxa_sem_contato_semestre:.1%} do universo",
        AMARELO
    )


# ============================================================
# VISÃO GERAL
# ============================================================

titulo_secao(
    "Visão geral",
    "Indicadores de contexto da Operação Segura."
)


c1, c2, c3, c4, c5 = (
    st.columns(5)
)


with c1:

    card_kpi(
        "Total de equipes",
        total_equipes,
        "universo analisado",
        AZUL_EQTL
    )


with c2:

    card_kpi(
        "Média equipes / mês",
        f"{media_equipes_mes:.0f}",
        "equipes com contato",
        AZUL_MEDIO
    )


with c3:

    card_kpi(
        "Líderes / Gerentes",
        total_lideres,
        "distintos no semestre",
        AMARELO
    )


with c4:

    card_kpi(
        "Presença média",
        f"{media_presenca_lideres:.1%}",
        "liderança ativa / mês",
        LARANJA
    )


with c5:

    card_kpi(
        "Total de inspetores",
        total_inspetores,
        "todos os cargos",
        AZUL_PRINCIPAL
    )


# ============================================================
# COBERTURA MENSAL
# ============================================================

titulo_secao(
    "Cobertura mensal",
    "Quantidade de equipes com e sem contato da liderança em cada mês."
)


cores_com = [

    AZUL_CLARO,
    AZUL_CLARO,
    AZUL_CLARO,

    AZUL_PRINCIPAL,
    AZUL_PRINCIPAL,
    AZUL_PRINCIPAL
]


cores_sem = [

    "#D9E7F5",
    "#D9E7F5",
    "#D9E7F5",

    "#A8B8D0",
    "#A8B8D0",
    "#A8B8D0"
]


fig_mensal = go.Figure()


fig_mensal.add_trace(

    go.Bar(

        name=
            "Com contato",

        x=
            resumo_mensal[
                "Mês"
            ],

        y=
            resumo_mensal[
                "Com contato"
            ],

        text=
            resumo_mensal[
                "Com contato"
            ],

        textposition=
            "inside",

        marker_color=
            cores_com
    )
)


fig_mensal.add_trace(

    go.Bar(

        name=
            "Sem contato",

        x=
            resumo_mensal[
                "Mês"
            ],

        y=
            resumo_mensal[
                "Sem contato"
            ],

        text=
            resumo_mensal[
                "Sem contato"
            ],

        textposition=
            "inside",

        marker_color=
            cores_sem
    )
)


fig_mensal.update_layout(
    barmode=
        "stack"
)


aplicar_layout_plotly(
    fig_mensal,
    "Equipes com contato vs. sem contato"
)


fig_mensal.update_yaxes(
    title=
        "Quantidade de equipes"
)


st.plotly_chart(
    fig_mensal,
    use_container_width=True
)


# ============================================================
# DIAGNÓSTICO DA BAIXA COBERTURA
# ============================================================

titulo_secao(
    "Diagnóstico da baixa cobertura",
    "Entendimento das equipes que não receberam contato da liderança."
)


c1, c2, c3, c4 = (
    st.columns(4)
)


with c1:

    card_kpi(
        "Sem contato liderança",
        equipes_sem_contato_semestre,
        "jan. a jun.",
        AMARELO
    )


with c2:

    card_kpi(
        "Com outros cargos",
        equipes_inspecionadas_outros,
        "equipes inspecionadas",
        AZUL_MEDIO
    )


with c3:

    card_kpi(
        "Inspeções outros cargos",
        inspecoes_outros_sem_contato,
        "inspeções distintas",
        AZUL_PRINCIPAL
    )


with c4:

    card_kpi(
        "Média por equipe",
        f"{media_outros_por_equipe:.1f}",
        "inspeções de outros cargos",
        LARANJA
    )


if (
    equipes_inspecionadas_outros
    ==
    equipes_sem_contato_semestre
):

    st.html(
        f"""
        <div class="warning-box">

            <strong>
                Leitura importante:
            </strong>

            as
            <strong>
                {equipes_sem_contato_semestre}
            </strong>
            equipes classificadas como sem contato
            da liderança receberam inspeções de outros cargos.

            <br><br>

            Portanto, o indicador representa
            <strong>
                ausência de contato de Líder/Gerente/GTE
            </strong>
            e não ausência total de atividade de inspeção.

        </div>
        """
    )


# ============================================================
# QUEM INSPECIONOU ESSAS EQUIPES
# ============================================================

top_cargos = (

    cargos_sem_contato

    .head(10)

    .sort_values(
        "Equipes",
        ascending=True
    )
)


if not top_cargos.empty:

    fig_cargos = px.bar(

        top_cargos,

        x=
            "Equipes",

        y=
            "Cargo Normalizado",

        orientation=
            "h",

        text=
            "Equipes"
    )


    fig_cargos.update_traces(

        marker_color=
            AZUL_PRINCIPAL,

        textposition=
            "outside"
    )


    aplicar_layout_plotly(

        fig_cargos,

        "Quem inspecionou as equipes sem contato da liderança?"
    )


    fig_cargos.update_xaxes(
        title=
            "Equipes distintas"
    )


    fig_cargos.update_yaxes(
        title=""
    )


    st.plotly_chart(
        fig_cargos,
        use_container_width=True
    )


# ============================================================
# CONFORMIDADES E NÃO CONFORMIDADES
# ============================================================

titulo_secao(
    "Conformidades e não conformidades",
    "Qualidade das inspeções realizadas pela liderança."
)


# ============================================================
# STATUS POR INSPEÇÃO
# ============================================================

status_inspecoes = (

    df_lideranca

    .groupby(
        [
            "Inspeção",
            "ID da Equipe"
        ],
        as_index=False
    )

    .agg(

        Data=(
            "Data de Execução",
            "min"
        ),

        Possui_NC=(

            "Conformidade Normalizada",

            lambda valores:

                (
                    valores
                    ==
                    "NAO CONFORME"
                )

                .any()
        )
    )
)


status_inspecoes[
    "Status"
] = (

    status_inspecoes[
        "Possui_NC"
    ]

    .map({

        True:
            "Não Conforme",

        False:
            "Conforme"
    })
)


status_inspecoes[
    "Mês Número"
] = (

    status_inspecoes[
        "Data"
    ]

    .dt.month
)


status_inspecoes[
    "Mês"
] = (

    status_inspecoes[
        "Mês Número"
    ]

    .map(
        meses
    )
)


# ============================================================
# MÉTRICAS DE CONFORMIDADE
# ============================================================

total_inspecoes_lideranca = len(
    status_inspecoes
)


total_conformes = int(

    status_inspecoes[
        "Status"
    ]

    .eq(
        "Conforme"
    )

    .sum()
)


total_nao_conformes = int(

    status_inspecoes[
        "Status"
    ]

    .eq(
        "Não Conforme"
    )

    .sum()
)


if total_inspecoes_lideranca > 0:

    taxa_conformidade = (

        total_conformes

        /
        total_inspecoes_lideranca
    )

else:

    taxa_conformidade = 0


c1, c2, c3, c4 = (
    st.columns(4)
)


with c1:

    card_kpi(
        "Inspeções analisadas",
        total_inspecoes_lideranca,
        "inspeções distintas",
        AZUL_PRINCIPAL
    )


with c2:

    card_kpi(
        "Conformes",
        total_conformes,
        "sem NC identificada",
        VERDE
    )


with c3:

    card_kpi(
        "Com não conformidade",
        total_nao_conformes,
        "inspeções com ≥ 1 NC",
        LARANJA
    )


with c4:

    card_kpi(
        "Taxa de conformidade",
        f"{taxa_conformidade:.1%}",
        "das inspeções",
        VERDE
    )


# ============================================================
# CONFORMIDADE POR MÊS
# ============================================================

conformidade_mensal = (

    status_inspecoes

    .groupby(
        [
            "Mês Número",
            "Mês",
            "Status"
        ]
    )

    .size()

    .reset_index(
        name=
            "Inspeções"
    )
)


conformidade_mensal[
    "Mês"
] = pd.Categorical(

    conformidade_mensal[
        "Mês"
    ],

    categories=
        ordem_meses,

    ordered=
        True
)


conformidade_mensal = (

    conformidade_mensal

    .sort_values(
        "Mês"
    )
)


fig_conformidade = px.bar(

    conformidade_mensal,

    x=
        "Mês",

    y=
        "Inspeções",

    color=
        "Status",

    barmode=
        "group",

    text=
        "Inspeções",

    color_discrete_map={

        "Conforme":
            VERDE,

        "Não Conforme":
            LARANJA
    }
)


fig_conformidade.update_traces(
    textposition=
        "outside"
)


aplicar_layout_plotly(

    fig_conformidade,

    "Conformidade das inspeções por mês"
)


fig_conformidade.update_yaxes(
    title=
        "Quantidade de inspeções"
)


st.plotly_chart(
    fig_conformidade,
    use_container_width=True
)


# ============================================================
# DETALHAMENTO DAS NÃO CONFORMIDADES
# ============================================================

nc_detalhe = (

    df_lideranca[

        df_lideranca[
            "Conformidade Normalizada"
        ]

        ==
        "NAO CONFORME"
    ]

    .copy()
)


if (
    "Não Conformidade"
    in nc_detalhe.columns
):

    nc_detalhe[
        "Não Conformidade"
    ] = (

        nc_detalhe[
            "Não Conformidade"
        ]

        .fillna(
            "Sem descrição informada"
        )

        .astype(str)

        .str.strip()
    )


    nc_detalhe.loc[

        nc_detalhe[
            "Não Conformidade"
        ]
        == "",

        "Não Conformidade"

    ] = "Sem descrição informada"


    colunas_chave_nc = [

        coluna

        for coluna in [

            "Inspeção",
            "ID da Equipe",
            "Membro",
            "Não Conformidade"
        ]

        if coluna
        in nc_detalhe.columns
    ]


    if colunas_chave_nc:

        nc_detalhe = (

            nc_detalhe

            .drop_duplicates(
                subset=
                    colunas_chave_nc
            )
        )


# ============================================================
# PRINCIPAIS NÃO CONFORMIDADES
# ============================================================

if (
    not nc_detalhe.empty
    and
    "Não Conformidade"
    in nc_detalhe.columns
):

    ranking_nc = (

        nc_detalhe[
            "Não Conformidade"
        ]

        .value_counts()

        .reset_index()
    )


    ranking_nc.columns = [

        "Descrição",

        "Ocorrências"
    ]


    top_nc = (

        ranking_nc

        .head(15)

        .sort_values(
            "Ocorrências",
            ascending=True
        )
    )


    fig_nc = px.bar(

        top_nc,

        x=
            "Ocorrências",

        y=
            "Descrição",

        orientation=
            "h",

        text=
            "Ocorrências"
    )


    fig_nc.update_traces(

        marker_color=
            LARANJA,

        textposition=
            "outside"
    )


    aplicar_layout_plotly(

        fig_nc,

        "Principais não conformidades identificadas"
    )


    fig_nc.update_layout(
        height=620
    )


    fig_nc.update_yaxes(
        title=""
    )


    st.plotly_chart(
        fig_nc,
        use_container_width=True
    )


# ============================================================
# CATEGORIAS DE NC
# ============================================================

if (
    not nc_detalhe.empty
    and
    "Categoria"
    in nc_detalhe.columns
):

    categorias_nc = (

        nc_detalhe[
            "Categoria"
        ]

        .fillna(
            "Sem categoria"
        )

        .astype(str)

        .str.strip()

        .replace(
            "",
            "Sem categoria"
        )

        .value_counts()

        .reset_index()
    )


    categorias_nc.columns = [

        "Categoria",

        "Ocorrências"
    ]


    top_categorias = (

        categorias_nc

        .head(10)

        .sort_values(
            "Ocorrências",
            ascending=True
        )
    )


    fig_categoria = px.bar(

        top_categorias,

        x=
            "Ocorrências",

        y=
            "Categoria",

        orientation=
            "h",

        text=
            "Ocorrências"
    )


    fig_categoria.update_traces(

        marker_color=
            AMARELO,

        textposition=
            "outside"
    )


    aplicar_layout_plotly(

        fig_categoria,

        "Não conformidades por categoria"
    )


    fig_categoria.update_yaxes(
        title=""
    )


    st.plotly_chart(
        fig_categoria,
        use_container_width=True
    )


# ============================================================
# TABELA DE NÃO CONFORMIDADES
# ============================================================

titulo_secao(
    "Detalhamento das não conformidades",
    "Consulta das ocorrências registradas nas inspeções."
)


if not nc_detalhe.empty:

    colunas_nc = [

        "Data de Execução",

        "Inspeção",

        "ID da Equipe",

        "Inspetor",

        "Cargo",

        "Membro",

        "Categoria",

        "Não Conformidade",

        "Gravidade Não Conformidade",

        "Regional",

        "Local",

        "Tipo de Serviço"
    ]


    colunas_nc = [

        coluna

        for coluna in colunas_nc

        if coluna
        in nc_detalhe.columns
    ]


    tabela_nc = (

        nc_detalhe[
            colunas_nc
        ]

        .sort_values(
            "Data de Execução",
            ascending=False
        )
    )


    if (
        "Não Conformidade"
        in tabela_nc.columns
    ):

        descricoes = sorted(

            tabela_nc[
                "Não Conformidade"
            ]

            .dropna()

            .unique()
        )


        filtro_descricao = (
            st.multiselect(

                "Filtrar por descrição de NC",

                descricoes
            )
        )


        if filtro_descricao:

            tabela_nc = (

                tabela_nc[

                    tabela_nc[
                        "Não Conformidade"
                    ]

                    .isin(
                        filtro_descricao
                    )
                ]
            )


    st.dataframe(

        tabela_nc,

        use_container_width=True,

        hide_index=True
    )


else:

    st.success(
        "Nenhuma não conformidade encontrada."
    )


# ============================================================
# RESUMO MENSAL
# ============================================================

titulo_secao(
    "Resumo mensal",
    "Cobertura, volume de inspeções e presença da liderança."
)


resumo_visual = (
    resumo_mensal
    .copy()
)


resumo_visual[
    "Taxa de contato"
] = (

    resumo_visual[
        "Taxa de contato"
    ]

    .map(
        lambda x:
            f"{x:.1%}"
    )
)


resumo_visual[
    "Presença de líderes"
] = (

    resumo_visual[
        "Presença de líderes"
    ]

    .map(
        lambda x:
            f"{x:.1%}"
    )
)


st.dataframe(

    resumo_visual,

    use_container_width=True,

    hide_index=True
)


# ============================================================
# INSPEÇÕES POR EQUIPE
# ============================================================

titulo_secao(
    "Inspeções por equipe",
    "Quantidade de inspeções distintas por equipe em cada mês."
)


tabela_equipes = (
    inspecoes_equipe_mes
    .copy()
)


tabela_equipes[
    "Total"
] = (

    tabela_equipes[
        ordem_meses
    ]

    .sum(
        axis=1
    )
)


tabela_equipes = (

    tabela_equipes

    .reset_index()
)


opcao = st.radio(

    "Visualização",

    [

        "Todas as equipes",

        "Somente equipes sem contato",

        "Somente equipes com contato"

    ],

    horizontal=True
)


if (
    opcao
    ==
    "Somente equipes sem contato"
):

    tabela_exibicao = (

        tabela_equipes[

            tabela_equipes[
                "Total"
            ]

            == 0
        ]
    )


elif (
    opcao
    ==
    "Somente equipes com contato"
):

    tabela_exibicao = (

        tabela_equipes[

            tabela_equipes[
                "Total"
            ]

            > 0
        ]
    )


else:

    tabela_exibicao = (
        tabela_equipes
        .copy()
    )


st.dataframe(

    tabela_exibicao,

    use_container_width=True,

    hide_index=True
)


# ============================================================
# MEMÓRIA DE CÁLCULO
# ============================================================

with st.expander(
    "Memória de cálculo / validação"
):

    st.write(
        f"Total de equipes: **{total_equipes}**"
    )

    st.write(
        f"Equipes com contato no T1: "
        f"**{equipes_contato_t1}**"
    )

    st.write(
        f"Equipes sem contato no T1: "
        f"**{equipes_sem_contato_t1}**"
    )

    st.write(
        f"Equipes com contato no T2: "
        f"**{equipes_contato_t2}**"
    )

    st.write(
        f"Equipes sem contato no T2: "
        f"**{equipes_sem_contato_t2}**"
    )

    st.write(
        f"Equipes sem contato no semestre: "
        f"**{equipes_sem_contato_semestre}**"
    )

    st.write(
        f"Líderes/Gerentes distintos: "
        f"**{total_lideres}**"
    )

    st.write(
        f"Inspetores distintos: "
        f"**{total_inspetores}**"
    )

    st.write(
        f"Inspeções distintas da liderança: "
        f"**{total_inspecoes_lideranca}**"
    )

    st.write(
        f"Inspeções conformes: "
        f"**{total_conformes}**"
    )

    st.write(
        f"Inspeções com não conformidade: "
        f"**{total_nao_conformes}**"
    )

    st.write(
        f"Taxa de conformidade: "
        f"**{taxa_conformidade:.1%}**"
    )


# ============================================================
# FOOTER
# ============================================================

st.html(
    f"""
    <div
        style="
            margin-top:40px;

            border-top:
                1px solid
                {CINZA_BORDA};

            padding-top:
                18px;

            padding-bottom:
                15px;

            display:
                flex;

            justify-content:
                space-between;

            color:
                {CINZA_TEXTO};

            font-size:
                11px;
        "
    >

        <span>
            Jornada de Segurança 2026 • Operação Segura
        </span>

        <span>
            Pilar Liderança
        </span>

    </div>
    """
)