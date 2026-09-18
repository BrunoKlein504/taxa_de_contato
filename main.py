import base64
import re
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
    initial_sidebar_state="expanded",
)


# ============================================================
# DISTRIBUIDORAS
# ============================================================

DISTRIBUIDORAS = {
    "AL": "Alagoas",
    "AP": "Amapá",
    "GO": "Goiás",
    "MA": "Maranhão",
    "PI": "Piauí",
    "RS": "Rio Grande do Sul",
    "PA": "Pará",
}


# ============================================================
# META DE LIDERANÇA
# ============================================================

# Por enquanto apenas AL possui meta informada.
#
# Quando tiver as demais:
#
# "AP": XX,
# "GO": XX,
# etc.

META_LIDERES = {
    "AL": 44,
}


# ============================================================
# META DA TAXA DE CONTATO
# ============================================================

META_TAXA_CONTATO = 1.00


# ============================================================
# TIPOS DE LIDERANÇA
# ============================================================

TIPOS_LIDERANCA = [
    "Líder",
    "Gerente",
    "Executivo",
    "Superintendente",
]


# ============================================================
# ORIGENS QUE NÃO DEVEM ENTRAR NO RECORTE
# ============================================================

ORIGENS_EXCLUIDAS = [
    "PPCR",
    "CIPA",
]


# ============================================================
# PALETA
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


PASTA_BASE = (
    BASE_DIR
    / "base"
)

LOGO_JORNADA = (
    BASE_DIR
    / "jornada_seguranca.png"
)

LOGO_EQTL = (
    BASE_DIR
    / "marca_equatorial.png"
)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def imagem_base64(caminho):

    if not caminho.exists():
        return None

    with open(caminho, "rb") as arquivo:

        return base64.b64encode(
            arquivo.read()
        ).decode()


def normalizar_texto(valor):

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


def normalizar_id(serie):

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


# ============================================================
# IDENTIFICA DISTRIBUIDORA PELO NOME DO ARQUIVO
# ============================================================

def identificar_distribuidora(nome_arquivo):

    nome = (
        Path(nome_arquivo)
        .stem
        .upper()
    )

    resultado = re.search(
        r"(?:^|[_\-\s])"
        r"(AL|AP|GO|MA|PI|RS|PA)"
        r"(?:[_\-\s]|$)",
        nome,
    )

    if resultado:

        sigla = resultado.group(1)

        return (
            sigla,
            DISTRIBUIDORAS[sigla]
        )

    return (
        "N/D",
        "Não identificada"
    )


# ============================================================
# PADRONIZAÇÃO DE ORIGEM
# ============================================================

def padronizar_origem(valor):

    texto = normalizar_texto(
        valor
    )

    if not texto:
        return "Não informado"


    if "PMS" in texto:

        return "PMS"


    if "ROTINA" in texto:

        return "Rotina"


    if "MUTIRAO" in texto:

        return "Mutirão"


    if (
        "ALTA" in texto
        and
        "HORA" in texto
    ):

        return "Altas Horas"


    if "PPCR" in texto:

        return "PPCR"


    if "CIPA" in texto:

        return "CIPA"


    return (
        str(valor)
        .strip()
        .title()
    )


# ============================================================
# CLASSIFICAÇÃO DA LIDERANÇA
# ============================================================

def classificar_tipo_lideranca(cargo):

    texto = normalizar_texto(
        cargo
    )


    if not texto:

        return None


    # --------------------------------------------------------
    # SUPERINTENDENTE
    # --------------------------------------------------------

    if (
        "SUPERINTEND" in texto
        or
        re.search(
            r"\bSUPT\b",
            texto
        )
    ):

        return "Superintendente"


    # --------------------------------------------------------
    # GERENTE
    # --------------------------------------------------------

    if (
        "GERENTE" in texto
        or
        re.search(
            r"\bGTE\b",
            texto
        )
    ):

        return "Gerente"


    # --------------------------------------------------------
    # EXECUTIVO
    # --------------------------------------------------------

    if (
        "EXECUTIVO" in texto
        or
        "EXECUTIVA" in texto
        or
        re.search(
            r"\bEXEC\b",
            texto
        )
    ):

        return "Executivo"


    # --------------------------------------------------------
    # LÍDER
    # --------------------------------------------------------

    if "LIDER" in texto:

        return "Líder"


    return None


# ============================================================
# PADRONIZAÇÃO DOS NÃO LÍDERES
# ============================================================

def classificar_nao_lider(cargo):

    texto = normalizar_texto(
        cargo
    )


    if not texto:

        return None


    # Se já foi classificado como liderança,
    # não pode entrar em não líderes.

    if (
        classificar_tipo_lideranca(cargo)
        is not None
    ):

        return None


    # --------------------------------------------------------
    # TÉCNICO SEGURANÇA
    # --------------------------------------------------------

    if (
        "SEGURANCA" in texto
        and
        "TRABALHO" in texto
    ):

        return (
            "Técnico de Segurança "
            "do Trabalho"
        )


    # --------------------------------------------------------
    # TÉCNICO DISTRIBUIÇÃO
    # --------------------------------------------------------

    if "DISTRIBUICAO" in texto:

        if (
            "TEC" in texto
            or
            "TECNICO" in texto
        ):

            return (
                "Técnico de Distribuição"
            )


    # --------------------------------------------------------
    # TÉCNICO OPERAÇÃO
    # --------------------------------------------------------

    if "OPERACAO" in texto:

        if (
            "TEC" in texto
            or
            "TECNICO" in texto
        ):

            return (
                "Técnico de Operação"
            )


    # --------------------------------------------------------
    # PROJETOS / OBRAS
    # --------------------------------------------------------

    if (
        "PROJET" in texto
        or
        "OBRA" in texto
    ):

        if (
            "TEC" in texto
            or
            "TECNICO" in texto
        ):

            return (
                "Técnico de Projetos "
                "e Obras"
            )


    # --------------------------------------------------------
    # ELETRICISTA
    # --------------------------------------------------------

    if "ELETRICISTA" in texto:

        return "Eletricista"


    # --------------------------------------------------------
    # ENGENHEIRO
    # --------------------------------------------------------

    if "ENGENHEIR" in texto:

        return "Engenheiro"


    # --------------------------------------------------------
    # FISCAL
    # --------------------------------------------------------

    if "FISCAL" in texto:

        return "Fiscal"


    # --------------------------------------------------------
    # ANALISTA
    # --------------------------------------------------------

    if (
        "ANALISTA" in texto
        or
        re.search(
            r"\bANL\b",
            texto
        )
    ):

        return "Analista"


    # --------------------------------------------------------
    # ASSISTENTE
    # --------------------------------------------------------

    if "ASSIST" in texto:

        return "Assistente"


    # --------------------------------------------------------
    # TRAINEE
    # --------------------------------------------------------

    if "TRAINEE" in texto:

        return "Trainee"


    # --------------------------------------------------------
    # CIPEIRO
    # --------------------------------------------------------

    if (
        "CIPEIR" in texto
        or
        "CIPA" in texto
    ):

        return "Cipeiro"


    # --------------------------------------------------------
    # COORDENADOR
    # --------------------------------------------------------

    if "COORDEN" in texto:

        return "Coordenador"


    # --------------------------------------------------------
    # SUPERVISOR
    # --------------------------------------------------------

    if "SUPERVIS" in texto:

        return "Supervisor"


    return "Outros"


# ============================================================
# CARREGAMENTO DAS BASES
# ============================================================

@st.cache_data
def carregar_bases(caminhos):

    bases = []
    erros = []


    for caminho_str in caminhos:

        caminho = Path(
            caminho_str
        )


        try:

            temp = pd.read_excel(
                caminho,
                sheet_name=
                    "Checklists Realizados"
            )


            temp.columns = (
                temp.columns
                .str.strip()
            )


            sigla, distribuidora = (
                identificar_distribuidora(
                    caminho.name
                )
            )


            temp[
                "Sigla Distribuidora"
            ] = sigla


            temp[
                "Distribuidora"
            ] = distribuidora


            temp[
                "Arquivo Origem"
            ] = caminho.name


            bases.append(
                temp
            )


        except Exception as erro:

            erros.append(
                {
                    "Arquivo":
                        caminho.name,

                    "Erro":
                        str(erro)
                }
            )


    if not bases:

        return (
            pd.DataFrame(),
            pd.DataFrame(
                erros
            )
        )


    df_final = pd.concat(
        bases,
        ignore_index=True,
        sort=False
    )


    return (
        df_final,
        pd.DataFrame(
            erros
        )
    )


# ============================================================
# COMPONENTES VISUAIS
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
        linecolor=
            CINZA_BORDA
    )


    fig.update_yaxes(
        gridcolor=
            "#EDF1F7",
        zeroline=False
    )


    return fig


# ============================================================
# IMAGENS
# ============================================================

logo_jornada_b64 = (
    imagem_base64(
        LOGO_JORNADA
    )
)

logo_eqtl_b64 = (
    imagem_base64(
        LOGO_EQTL
    )
)


# ============================================================
# CSS
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
        background:
            {CINZA_FUNDO};
    }}


    .block-container {{
        padding-top:
            1.5rem;

        padding-bottom:
            3rem;

        max-width:
            1500px;
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
        color:
            white;
    }}


    [data-testid="stSidebar"] label {{
        font-weight:
            600;
    }}


    [data-testid="stSidebar"]
    [data-baseweb="select"] > div {{
        background:
            white;
    }}


    [data-testid="stSidebar"]
    [data-baseweb="select"] span {{
        color:
            {AZUL_ESCURO};
    }}


    /* =======================================================
       HERO
    ======================================================= */

    .hero {{
        background:
            linear-gradient(
                120deg,
                {AZUL_ESCURO} 0%,
                {AZUL_EQTL} 65%,
                {AZUL_PRINCIPAL} 100%
            );

        border-radius:
            26px;

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

        position:
            relative;

        overflow:
            hidden;
    }}


    .hero::after {{
        content:
            "";

        position:
            absolute;

        width:
            340px;

        height:
            340px;

        border-radius:
            50%;

        background:
            rgba(
                255,
                192,
                0,
                .10
            );

        right:
            -90px;

        top:
            -165px;
    }}


    .hero-grid {{
        display:
            flex;

        align-items:
            center;

        justify-content:
            space-between;

        gap:
            40px;

        position:
            relative;

        z-index:
            2;
    }}


    .hero-text {{
        flex:
            1;
    }}


    .hero-tag {{
        display:
            inline-block;

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
       LOGO
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
       SECTION
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
       KPI
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
        content:
            "";

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
       ALERTA
    ======================================================= */

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
       TABELAS
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
       RESPONSIVO
    ======================================================= */

    @media (max-width: 900px) {{

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

    }}

    </style>
    """
)


# ============================================================
# HERO
# ============================================================

if logo_jornada_b64:

    logo_html = f"""
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

                    Meta: 100% das equipes com contato
                    da liderança dentro de cada ciclo de 3 meses.

                </p>

            </div>

            {logo_html}

        </div>

    </div>
    """
)


# ============================================================
# LOCALIZA ARQUIVOS
# ============================================================

if not PASTA_BASE.exists():

    st.error(
        "A pasta `base` não foi encontrada "
        "ao lado do arquivo app.py."
    )

    st.stop()


arquivos_excel = sorted(
    arquivo
    for arquivo
    in PASTA_BASE.glob(
        "*.xlsx"
    )
    if (
        arquivo.is_file()
        and
        not arquivo.name.startswith(
            "~$"
        )
    )
)


if not arquivos_excel:

    st.error(
        "Nenhum arquivo `.xlsx` foi encontrado "
        "na pasta `base`."
    )

    st.stop()


# ============================================================
# CARREGA BASES
# ============================================================

caminhos = [
    str(arquivo)
    for arquivo
    in arquivos_excel
]


df, erros_carregamento = (
    carregar_bases(
        caminhos
    )
)


if df.empty:

    st.error(
        "Nenhuma base pôde ser carregada."
    )

    st.stop()


# ============================================================
# TRATAMENTO GERAL
# ============================================================

df[
    "Data de Execução"
] = pd.to_datetime(
    df[
        "Data de Execução"
    ],
    errors="coerce"
)


df = (
    df
    .dropna(
        subset=[
            "ID da Equipe",
            "Data de Execução"
        ]
    )
    .copy()
)


df[
    "ID da Equipe"
] = normalizar_id(
    df[
        "ID da Equipe"
    ]
)


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


# ============================================================
# CLASSIFICA LIDERANÇA
# ============================================================

df[
    "Tipo de Liderança"
] = (
    df[
        "Cargo"
    ]
    .apply(
        classificar_tipo_lideranca
    )
)


df[
    "É Liderança"
] = (
    df[
        "Tipo de Liderança"
    ]
    .notna()
)


# ============================================================
# CLASSIFICA NÃO LÍDER
# ============================================================

df[
    "Perfil Não Líder"
] = (
    df[
        "Cargo"
    ]
    .apply(
        classificar_nao_lider
    )
)


# ============================================================
# CONFORMIDADE
# ============================================================

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
# ORIGEM
# ============================================================

df[
    "Origem Padronizada"
] = (
    df[
        "Origem"
    ]
    .apply(
        padronizar_origem
    )
)


# ============================================================
# CHAVE ÚNICA DA EQUIPE
# ============================================================

df[
    "Chave Equipe"
] = (
    df[
        "Sigla Distribuidora"
    ]
    .astype(str)
    .str.strip()
    +
    " | "
    +
    df[
        "ID da Equipe"
    ]
    .astype(str)
    .str.strip()
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
# DISTRIBUIDORA
# ============================================================

distribuidoras_presentes = set(
    df[
        "Distribuidora"
    ]
    .dropna()
    .unique()
)


distribuidoras_disponiveis = [
    nome
    for sigla, nome
    in DISTRIBUIDORAS.items()
    if nome
    in distribuidoras_presentes
]


opcoes_distribuidora = (
    [
        "Todas as distribuidoras"
    ]
    +
    distribuidoras_disponiveis
)


distribuidora_selecionada = (
    st.sidebar.selectbox(
        "Distribuidora",
        opcoes_distribuidora
    )
)


if (
    distribuidora_selecionada
    !=
    "Todas as distribuidoras"
):

    df_distribuidora = (
        df[
            df[
                "Distribuidora"
            ]
            ==
            distribuidora_selecionada
        ]
        .copy()
    )

else:

    df_distribuidora = (
        df.copy()
    )


# ============================================================
# ANO
# ============================================================

anos = sorted(
    df_distribuidora[
        "Data de Execução"
    ]
    .dt.year
    .dropna()
    .unique()
)


if not anos:

    st.warning(
        "Não foram encontradas datas válidas."
    )

    st.stop()


ano = st.sidebar.selectbox(
    "Ano de análise",
    anos,
    index=
        len(anos) - 1
)


# ============================================================
# PRIMEIRO SEMESTRE
# ============================================================

df_periodo = (
    df_distribuidora[
        (
            df_distribuidora[
                "Data de Execução"
            ]
            .dt.year
            ==
            ano
        )
        &
        (
            df_distribuidora[
                "Data de Execução"
            ]
            .dt.month
            .between(
                1,
                6
            )
        )
    ]
    .copy()
)


# ============================================================
# ORIGENS
# ============================================================

origens_encontradas = sorted(
    df_periodo[
        "Origem Padronizada"
    ]
    .dropna()
    .unique()
)


origens_excluidas_normalizadas = [
    normalizar_texto(
        origem
    )
    for origem
    in ORIGENS_EXCLUIDAS
]


origens_disponiveis = [
    origem
    for origem
    in origens_encontradas
    if (
        normalizar_texto(
            origem
        )
        not in
        origens_excluidas_normalizadas
        and
        origem
        !=
        "Não informado"
    )
]


origens_selecionadas = (
    st.sidebar.multiselect(
        "Origem",
        origens_disponiveis,
        default=
            origens_disponiveis,
        help=(
            "PPCR e CIPA são retirados "
            "do recorte principal."
        )
    )
)


if not origens_selecionadas:

    st.warning(
        "Selecione pelo menos uma origem."
    )

    st.stop()


# ============================================================
# UNIVERSO DAS EQUIPES
# ============================================================
#
# IMPORTANTE:
#
# Criado ANTES do filtro de origem.
#
# Assim não diminuímos artificialmente
# o denominador da Taxa de Contato.
# ============================================================

cadastro_equipes = (
    df_periodo[
        [
            "Chave Equipe",
            "Sigla Distribuidora",
            "Distribuidora",
            "ID da Equipe"
        ]
    ]
    .drop_duplicates(
        subset=[
            "Chave Equipe"
        ]
    )
)


todas_equipes = sorted(
    cadastro_equipes[
        "Chave Equipe"
    ]
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
# BASE OPERACIONAL
# ============================================================

df_operacional = (
    df_periodo[
        df_periodo[
            "Origem Padronizada"
        ]
        .isin(
            origens_selecionadas
        )
    ]
    .copy()
)


# ============================================================
# MÊS
# ============================================================

meses = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
}


ordem_meses = list(
    meses.values()
)


df_operacional[
    "Mês Número"
] = (
    df_operacional[
        "Data de Execução"
    ]
    .dt.month
)


df_operacional[
    "Mês"
] = (
    df_operacional[
        "Mês Número"
    ]
    .map(
        meses
    )
)


# ============================================================
# LIDERANÇA X NÃO LIDERANÇA
# ============================================================

df_lideranca = (
    df_operacional[
        df_operacional[
            "É Liderança"
        ]
    ]
    .copy()
)


df_nao_lider = (
    df_operacional[
        ~df_operacional[
            "É Liderança"
        ]
    ]
    .copy()
)


# ============================================================
# LIMPEZA DOS NÃO LÍDERES
# ============================================================

df_nao_lider = (
    df_nao_lider[
        df_nao_lider[
            "Perfil Não Líder"
        ]
        .notna()
        &
        df_nao_lider[
            "Inspetor"
        ]
        .notna()
    ]
    .copy()
)


# ============================================================
# META DE LIDERANÇA
# ============================================================
#
# CORREÇÃO DO ERRO DO PYLANCE.
#
# Antes:
#
# META_LIDERES.get(sigla)
#
# podia retornar None.
#
# Agora "metas_encontradas" contém SOMENTE int.
# ============================================================

siglas_no_recorte = sorted(
    df_periodo[
        "Sigla Distribuidora"
    ]
    .dropna()
    .unique()
)


metas_encontradas = [
    META_LIDERES[
        sigla
    ]
    for sigla
    in siglas_no_recorte
    if sigla
    in META_LIDERES
]


if (
    len(siglas_no_recorte)
    == 1
    and
    siglas_no_recorte[0]
    in META_LIDERES
):

    meta_lideres = (
        META_LIDERES[
            siglas_no_recorte[0]
        ]
    )


elif (
    len(siglas_no_recorte) > 0
    and
    len(metas_encontradas)
    ==
    len(siglas_no_recorte)
):

    meta_lideres = sum(
        metas_encontradas
    )


else:

    meta_lideres = None


# ============================================================
# INSPEÇÕES POR EQUIPE / MÊS
# ============================================================

inspecoes_equipe_mes = (
    df_lideranca
    .groupby(
        [
            "Chave Equipe",
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


# ============================================================
# INCLUI EQUIPES QUE NÃO RECEBERAM CONTATO
# ============================================================

inspecoes_equipe_mes = (
    inspecoes_equipe_mes
    .reindex(
        index=
            todas_equipes,
        fill_value=0
    )
)


# ============================================================
# GARANTE OS 6 MESES
# ============================================================

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
# HOUVE CONTATO?
# ============================================================

teve_contato = (
    inspecoes_equipe_mes
    >
    0
)


# ============================================================
# T1
# ============================================================

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


# ============================================================
# T2
# ============================================================

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


# ============================================================
# SEMESTRE
# ============================================================

contato_semestre_equipe = (
    teve_contato
    .any(
        axis=1
    )
)


# ============================================================
# CÁLCULOS
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


gap_t1_pp = (
    META_TAXA_CONTATO
    -
    taxa_t1
) * 100


gap_t2_pp = (
    META_TAXA_CONTATO
    -
    taxa_t2
) * 100


# ============================================================
# QUANTIDADE POR TIPO DE LIDERANÇA
# ============================================================

lideres_por_tipo = (
    df_lideranca
    .groupby(
        "Tipo de Liderança"
    )[
        "Inspetor"
    ]
    .nunique()
    .reindex(
        TIPOS_LIDERANCA,
        fill_value=0
    )
    .reset_index()
)


lideres_por_tipo.columns = [
    "Tipo de liderança",
    "Quantidade de líderes"
]


# ============================================================
# INSPEÇÕES POR TIPO DE LIDERANÇA
# ============================================================

inspecoes_por_tipo_lider = (
    df_lideranca
    .groupby(
        "Tipo de Liderança"
    )[
        "Inspeção"
    ]
    .nunique()
    .reindex(
        TIPOS_LIDERANCA,
        fill_value=0
    )
    .reset_index()
)


inspecoes_por_tipo_lider.columns = [
    "Tipo de liderança",
    "Inspeções distintas"
]


lideres_por_tipo = (
    lideres_por_tipo
    .merge(
        inspecoes_por_tipo_lider,
        on=
            "Tipo de liderança",
        how=
            "left"
    )
)


# ============================================================
# LIDERANÇAS ATIVAS
# ============================================================

lideres_ativos_semestre = (
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


total_inspecoes_lideranca = (
    df_lideranca[
        "Inspeção"
    ]
    .nunique()
)


if (
    meta_lideres is not None
    and
    meta_lideres > 0
):

    aderencia_lideres = (
        lideres_ativos_semestre
        /
        meta_lideres
    )

else:

    aderencia_lideres = None


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


    base_mes = (
        df_lideranca[
            df_lideranca[
                "Mês Número"
            ]
            ==
            numero_mes
        ]
    )


    inspecoes_distintas = (
        base_mes[
            "Inspeção"
        ]
        .nunique()
    )


    lideres_ativos = (
        base_mes[
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


    if (
        meta_lideres is not None
        and
        meta_lideres > 0
    ):

        presenca_lideres = (
            lideres_ativos
            /
            meta_lideres
        )

    else:

        presenca_lideres = None


    resumo_mensal.append(
        {
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
                presenca_lideres,
        }
    )


resumo_mensal = pd.DataFrame(
    resumo_mensal
)


# ============================================================
# NÃO LÍDERES
# ============================================================

total_inspetores_nao_lideres = (
    df_nao_lider[
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


total_inspecoes_nao_lideres = (
    df_nao_lider[
        "Inspeção"
    ]
    .nunique()
)


nao_lideres_resumo = (
    df_nao_lider
    .groupby(
        "Perfil Não Líder"
    )
    .agg(

        Inspetores=(
            "Inspetor",
            "nunique"
        ),

        Inspeções=(
            "Inspeção",
            "nunique"
        ),

        Equipes=(
            "Chave Equipe",
            "nunique"
        ),
    )
    .reset_index()
    .sort_values(
        "Inspetores",
        ascending=False
    )
)


# ============================================================
# CONFORMIDADE POR INSPEÇÃO
# ============================================================

status_inspecoes = (
    df_lideranca
    .groupby(
        [
            "Inspeção",
            "Chave Equipe"
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
    .map(
        {
            True:
                "Não Conforme",

            False:
                "Conforme"
        }
    )
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

total_inspecoes_analisadas = len(
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


if total_inspecoes_analisadas > 0:

    taxa_conformidade = (
        total_conformes
        /
        total_inspecoes_analisadas
    )

else:

    taxa_conformidade = 0


# ============================================================
# DETALHE DAS NÃO CONFORMIDADES
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
    ] = (
        "Sem descrição informada"
    )


    colunas_chave_nc = [
        coluna
        for coluna in [
            "Inspeção",
            "Chave Equipe",
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
# OBJETIVO CENTRAL
# ============================================================

titulo_secao(
    "Objetivo central",
    (
        "Verificar se 100% das equipes receberam pelo menos "
        "um contato da liderança em cada ciclo de 3 meses."
    )
)


st.html(
    f"""
    <div class="warning-box">

        <strong>
            Regra da Taxa de Contato:
        </strong>

        cada equipe precisa receber pelo menos um contato
        da liderança no T1 (janeiro a março) e novamente
        no T2 (abril a junho).

        <br><br>

        Uma equipe com várias inspeções continua representando
        apenas uma equipe coberta na Taxa de Contato.

        <br><br>

        <strong>
            Origens consideradas:
        </strong>

        {', '.join(origens_selecionadas)}

    </div>
    """
)


# ============================================================
# CARDS PRINCIPAIS
# ============================================================

c1, c2, c3, c4 = st.columns(4)


with c1:

    card_kpi(
        "Meta trimestral",
        "100%",
        "das equipes em até 3 meses",
        AMARELO
    )


with c2:

    card_kpi(
        "Taxa de Contato T1",
        f"{taxa_t1:.1%}",
        (
            f"{equipes_sem_contato_t1} equipes pendentes"
            f" • gap {gap_t1_pp:.1f} p.p."
        ),
        LARANJA
    )


with c3:

    card_kpi(
        "Taxa de Contato T2",
        f"{taxa_t2:.1%}",
        (
            f"{equipes_sem_contato_t2} equipes pendentes"
            f" • gap {gap_t2_pp:.1f} p.p."
        ),
        LARANJA
    )


with c4:

    card_kpi(
        "Total de equipes",
        total_equipes,
        "universo do indicador",
        AZUL_PRINCIPAL
    )


# ============================================================
# TAXA X META
# ============================================================

comparativo_meta = pd.DataFrame(
    {
        "Trimestre": [
            "T1",
            "T2"
        ],

        "Taxa": [
            taxa_t1 * 100,
            taxa_t2 * 100
        ],
    }
)


fig_meta = go.Figure()


fig_meta.add_trace(
    go.Bar(

        x=
            comparativo_meta[
                "Trimestre"
            ],

        y=
            comparativo_meta[
                "Taxa"
            ],

        text=[
            f"{taxa_t1:.1%}",
            f"{taxa_t2:.1%}"
        ],

        textposition=
            "outside",

        marker_color=[
            AZUL_CLARO,
            AZUL_PRINCIPAL
        ],

        name=
            "Taxa realizada"
    )
)


fig_meta.add_hline(
    y=100,

    line_dash=
        "dash",

    line_color=
        AMARELO,

    line_width=3,

    annotation_text=
        "Meta 100%",

    annotation_position=
        "top right"
)


fig_meta.update_yaxes(
    range=[
        0,
        110
    ],

    title=
        "Taxa de contato (%)"
)


aplicar_layout_plotly(
    fig_meta,
    (
        "Taxa de Contato realizada x "
        "meta de 100% em 3 meses"
    )
)


st.plotly_chart(
    fig_meta,
    use_container_width=True
)


# ============================================================
# PRESENÇA DA LIDERANÇA
# ============================================================

titulo_secao(
    "Presença da liderança",
    (
        "Líderes, Gerentes, Executivos e Superintendentes "
        "que realizaram pelo menos uma inspeção."
    )
)


c1, c2, c3, c4 = (
    st.columns(4)
)


with c1:

    card_kpi(
        "Lideranças ativas",
        lideres_ativos_semestre,
        "inspetores distintos no semestre",
        AZUL_PRINCIPAL
    )


with c2:

    card_kpi(
        "Meta de líderes",
        (
            meta_lideres
            if meta_lideres
            is not None
            else "N/D"
        ),
        (
            "Meta da distribuidora"
            if meta_lideres
            is not None
            else
            "meta ainda não cadastrada"
        ),
        AMARELO
    )


with c3:

    card_kpi(
        "Presença acumulada",
        (
            f"{aderencia_lideres:.1%}"
            if aderencia_lideres
            is not None
            else
            "N/D"
        ),
        (
            "lideranças ativas ÷ meta"
            if aderencia_lideres
            is not None
            else
            "necessário cadastrar a meta"
        ),
        (
            VERDE
            if (
                aderencia_lideres
                is not None
                and
                aderencia_lideres >= 1
            )
            else
            LARANJA
        )
    )


with c4:

    card_kpi(
        "Inspeções da liderança",
        total_inspecoes_lideranca,
        "inspeções distintas",
        AZUL_MEDIO
    )


# ============================================================
# GRÁFICOS DE LIDERANÇA
# ============================================================

col1, col2 = (
    st.columns(2)
)


with col1:

    fig_tipo_lider = px.bar(
        lideres_por_tipo,

        x=
            "Tipo de liderança",

        y=
            "Quantidade de líderes",

        text=
            "Quantidade de líderes",

        color=
            "Tipo de liderança",

        color_discrete_map={
            "Líder":
                AZUL_CLARO,

            "Gerente":
                AZUL_MEDIO,

            "Executivo":
                AZUL_PRINCIPAL,

            "Superintendente":
                AZUL_ESCURO,
        }
    )


    fig_tipo_lider.update_traces(
        textposition=
            "outside"
    )


    fig_tipo_lider.update_layout(
        showlegend=
            False
    )


    aplicar_layout_plotly(
        fig_tipo_lider,
        "Quantidade de lideranças ativas por tipo"
    )


    fig_tipo_lider.update_yaxes(
        title=
            "Inspetores distintos"
    )


    st.plotly_chart(
        fig_tipo_lider,
        use_container_width=True
    )


with col2:

    fig_presenca = go.Figure()


    fig_presenca.add_trace(
        go.Bar(

            x=
                resumo_mensal[
                    "Mês"
                ],

            y=
                resumo_mensal[
                    "Líderes ativos"
                ],

            text=
                resumo_mensal[
                    "Líderes ativos"
                ],

            textposition=
                "outside",

            marker_color=[
                AZUL_CLARO,
                AZUL_CLARO,
                AZUL_CLARO,
                AZUL_PRINCIPAL,
                AZUL_PRINCIPAL,
                AZUL_PRINCIPAL
            ],

            name=
                "Lideranças ativas"
        )
    )


    if meta_lideres is not None:

        fig_presenca.add_hline(
            y=
                meta_lideres,

            line_dash=
                "dash",

            line_color=
                AMARELO,

            line_width=3,

            annotation_text=
                f"Meta: {meta_lideres}",

            annotation_position=
                "top right"
        )


    aplicar_layout_plotly(
        fig_presenca,
        (
            "Quantidade de lideranças distintas "
            "com inspeção por mês"
        )
    )


    fig_presenca.update_yaxes(
        title=
            "Lideranças ativas"
    )


    st.plotly_chart(
        fig_presenca,
        use_container_width=True
    )


# ============================================================
# TABELA LIDERANÇA
# ============================================================

st.dataframe(
    lideres_por_tipo,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# COBERTURA MENSAL
# ============================================================

titulo_secao(
    "Cobertura mensal das equipes",
    (
        "Mostra quantas equipes tiveram pelo menos uma "
        "inspeção da liderança em cada mês."
    )
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
    (
        "Equipes com contato x "
        "sem contato em cada mês"
    )
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
# RESUMO MENSAL
# ============================================================

resumo_visual = (
    resumo_mensal.copy()
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
            (
                f"{x:.1%}"
                if pd.notna(x)
                else "N/D"
            )
    )
)


st.dataframe(
    resumo_visual,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# NÃO LÍDERES
# ============================================================

titulo_secao(
    "Inspeções realizadas por não líderes",
    (
        "Executivos não aparecem nesta seção. "
        "Os cargos restantes foram agrupados "
        "em perfis padronizados."
    )
)


c1, c2, c3 = (
    st.columns(3)
)


with c1:

    card_kpi(
        "Total de inspetores",
        total_inspetores_nao_lideres,
        "não líderes distintos",
        AZUL_MEDIO
    )


with c2:

    card_kpi(
        "Inspeções de não líderes",
        total_inspecoes_nao_lideres,
        "inspeções distintas",
        AZUL_PRINCIPAL
    )


with c3:

    card_kpi(
        "Perfis identificados",
        nao_lideres_resumo[
            "Perfil Não Líder"
        ]
        .nunique(),
        "categorias padronizadas",
        AMARELO
    )


# ============================================================
# GRÁFICO NÃO LÍDERES
# ============================================================

if not nao_lideres_resumo.empty:

    grafico_nao_lideres = (
        nao_lideres_resumo
        .head(12)
        .sort_values(
            "Inspetores",
            ascending=True
        )
    )


    fig_nao_lideres = px.bar(
        grafico_nao_lideres,

        x=
            "Inspetores",

        y=
            "Perfil Não Líder",

        orientation=
            "h",

        text=
            "Inspetores"
    )


    fig_nao_lideres.update_traces(
        marker_color=
            AZUL_MEDIO,

        textposition=
            "outside"
    )


    aplicar_layout_plotly(
        fig_nao_lideres,
        (
            "Quantidade de inspetores "
            "não líderes por perfil"
        )
    )


    fig_nao_lideres.update_xaxes(
        title=
            "Inspetores distintos"
    )


    fig_nao_lideres.update_yaxes(
        title=""
    )


    st.plotly_chart(
        fig_nao_lideres,
        use_container_width=True
    )


    st.dataframe(
        nao_lideres_resumo,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# CONFORMIDADE
# ============================================================

titulo_secao(
    "Conformidades e não conformidades",
    (
        "Uma inspeção é considerada não conforme "
        "quando possui pelo menos um registro "
        "de não conformidade."
    )
)


c1, c2, c3, c4 = (
    st.columns(4)
)


with c1:

    card_kpi(
        "Inspeções analisadas",
        total_inspecoes_analisadas,
        "inspeções distintas da liderança",
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
        "com pelo menos 1 NC",
        LARANJA
    )


with c4:

    card_kpi(
        "Taxa de conformidade",
        f"{taxa_conformidade:.1%}",
        "conformes ÷ analisadas",
        VERDE
    )


# ============================================================
# CONFORMIDADE MENSAL
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

    ordered=True
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
            LARANJA,
    }
)


fig_conformidade.update_traces(
    textposition=
        "outside"
)


aplicar_layout_plotly(
    fig_conformidade,
    (
        "Inspeções conformes x "
        "não conformes por mês"
    )
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


    fig_nc.update_layout(
        height=
            620
    )


    aplicar_layout_plotly(
        fig_nc,
        "Principais descrições de não conformidade"
    )


    fig_nc.update_yaxes(
        title=""
    )


    st.plotly_chart(
        fig_nc,
        use_container_width=True
    )


# ============================================================
# DETALHAMENTO DAS NCS
# ============================================================

titulo_secao(
    "Detalhamento das não conformidades",
    (
        "Ocorrências registradas nas inspeções "
        "realizadas pela liderança."
    )
)


if not nc_detalhe.empty:

    colunas_nc = [
        "Distribuidora",
        "Data de Execução",
        "Origem Padronizada",
        "Inspeção",
        "ID da Equipe",
        "Inspetor",
        "Tipo de Liderança",
        "Cargo",
        "Membro",
        "Categoria",
        "Não Conformidade",
        "Gravidade Não Conformidade",
        "Regional",
        "Local",
        "Tipo de Serviço",
    ]


    colunas_nc = [
        coluna
        for coluna
        in colunas_nc
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
        "Origem Padronizada"
        in tabela_nc.columns
    ):

        tabela_nc = (
            tabela_nc
            .rename(
                columns={
                    "Origem Padronizada":
                        "Origem"
                }
            )
        )


    st.dataframe(
        tabela_nc,
        use_container_width=True,
        hide_index=True
    )


else:

    st.success(
        "Nenhuma não conformidade encontrada "
        "no recorte selecionado."
    )


# ============================================================
# INSPEÇÕES POR EQUIPE
# ============================================================

titulo_secao(
    "Inspeções por equipe",
    (
        "Cada célula representa a quantidade de "
        "inspeções distintas realizadas pela liderança "
        "naquela equipe durante o mês."
    )
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


tabela_equipes = (
    tabela_equipes
    .merge(
        cadastro_equipes,

        on=
            "Chave Equipe",

        how=
            "left"
    )
)


colunas_ordem = [
    "Distribuidora",
    "ID da Equipe",
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Total",
]


tabela_equipes = (
    tabela_equipes[
        [
            coluna
            for coluna
            in colunas_ordem
            if coluna
            in tabela_equipes.columns
        ]
    ]
)


opcao = st.radio(
    "Visualização",

    [
        "Todas as equipes",
        "Somente equipes sem contato",
        "Somente equipes com contato",
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
            ==
            0
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
            >
            0
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
# ERROS DE CARREGAMENTO
# ============================================================

if not erros_carregamento.empty:

    with st.expander(
        "Erros de carregamento"
    ):

        st.dataframe(
            erros_carregamento,
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
        f"Distribuidora: "
        f"**{distribuidora_selecionada}**"
    )


    st.write(
        f"Ano: "
        f"**{ano}**"
    )


    st.write(
        f"Origens consideradas: "
        f"**{', '.join(origens_selecionadas)}**"
    )


    st.write(
        f"Total de equipes no universo: "
        f"**{total_equipes}**"
    )


    st.write(
        f"Taxa de Contato T1: "
        f"**{taxa_t1:.1%}**"
    )


    st.write(
        f"Equipes pendentes no T1: "
        f"**{equipes_sem_contato_t1}**"
    )


    st.write(
        f"Taxa de Contato T2: "
        f"**{taxa_t2:.1%}**"
    )


    st.write(
        f"Equipes pendentes no T2: "
        f"**{equipes_sem_contato_t2}**"
    )


    st.write(
        f"Lideranças ativas: "
        f"**{lideres_ativos_semestre}**"
    )


    st.write(
        f"Meta de lideranças: "
        f"**{meta_lideres if meta_lideres is not None else 'N/D'}**"
    )


    st.write(
        f"Inspetores não líderes: "
        f"**{total_inspetores_nao_lideres}**"
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
        f"Inspeções com NC: "
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