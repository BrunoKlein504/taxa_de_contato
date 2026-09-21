import base64
import re
import unicodedata
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Operação Segura | Taxa de Contato",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# REGRAS DE NEGÓCIO
# ============================================================

DISTRIBUIDORAS = {
    "AL": "Alagoas",
    "AP": "Amapá",
    "GO": "Goiás",
    "MA": "Maranhão",
    "PI": "Piauí",
    "RS": "Rio Grande do Sul",
    "PA": "Pará",
<<<<<<< HEAD
}


# ============================================================
# META DE LIDERANÇAS
# ============================================================

META_LIDERES = {
    "AL": 44,
}


# ============================================================
# META DA TAXA DE CONTATO
# ============================================================

META_TAXA_CONTATO = 1.00


# ============================================================
# TIPOS CONSIDERADOS COMO LIDERANÇA
# ============================================================

TIPOS_LIDERANCA = [
    "Líder",
    "Gerente",
    "Executivo",
    "Superintendente",
    "Técnico de Distribuição",
]


# ============================================================
# ORIGEM PRINCIPAL
# ============================================================

ORIGEM_PRINCIPAL = "PMS"


# ============================================================
# ORIGENS FORA DO CONTEXTO PRINCIPAL
# ============================================================

ORIGENS_EXCLUIDAS = {
    "PPCR",
    "CIPA",
    "Não informado",
=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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
VERMELHO = "#D64545"

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


PASTA_BASE = BASE_DIR / "base"

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
        caractere
        for caractere
        in unicodedata.normalize(
            "NFKD",
            valor
        )
        if not unicodedata.combining(
            caractere
        )
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
<<<<<<< HEAD
# IDENTIFICAÇÃO DA DISTRIBUIDORA
# ============================================================

def identificar_distribuidora(
    nome_arquivo
):
=======
# IDENTIFICA DISTRIBUIDORA PELO NOME DO ARQUIVO
# ============================================================

def identificar_distribuidora(nome_arquivo):
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b

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
<<<<<<< HEAD
# PADRONIZAÇÃO DA ORIGEM
=======
# PADRONIZAÇÃO DE ORIGEM
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
# ============================================================

def padronizar_origem(valor):

    texto = normalizar_texto(
        valor
    )

    if not texto:
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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


<<<<<<< HEAD
    return "Outras"
=======
    return (
        str(valor)
        .strip()
        .title()
    )
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b


# ============================================================
# CLASSIFICAÇÃO DA LIDERANÇA
# ============================================================

def classificar_tipo_lideranca(cargo):

    texto = normalizar_texto(
        cargo
    )

<<<<<<< HEAD
=======

>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    if not texto:

        return None


    # --------------------------------------------------------
<<<<<<< HEAD
    # TÉCNICO DE DISTRIBUIÇÃO
    # --------------------------------------------------------

    if (
        "DISTRIBUICAO" in texto
        and
        (
            "TECNICO" in texto
            or
            re.search(
                r"\bTEC\b",
                texto
            )
        )
    ):

        return "Técnico de Distribuição"


    if re.search(
        r"\bTEC.*DIST",
        texto
    ):

        return "Técnico de Distribuição"


    # --------------------------------------------------------
=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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
<<<<<<< HEAD
# CLASSIFICAÇÃO DOS NÃO LÍDERES
=======
# PADRONIZAÇÃO DOS NÃO LÍDERES
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
# ============================================================

def classificar_nao_lider(cargo):

    texto = normalizar_texto(
        cargo
    )

<<<<<<< HEAD
=======

>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    if not texto:

        return None


<<<<<<< HEAD
    # Se for liderança, não entra nesta visão.

    if (
        classificar_tipo_lideranca(
            cargo
        )
=======
    # Se já foi classificado como liderança,
    # não pode entrar em não líderes.

    if (
        classificar_tipo_lideranca(cargo)
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        is not None
    ):

        return None


    # --------------------------------------------------------
<<<<<<< HEAD
    # TÉCNICO DE SEGURANÇA
=======
    # TÉCNICO SEGURANÇA
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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
<<<<<<< HEAD
    # TÉCNICO DE OPERAÇÃO
    # --------------------------------------------------------

    if (
        "OPERACAO" in texto
        and
        (
            "TECNICO" in texto
            or
            re.search(
                r"\bTEC\b",
                texto
            )
        )
    ):

        return "Técnico de Operação"


    # --------------------------------------------------------
    # TÉCNICO DE PROJETOS / OBRAS
    # --------------------------------------------------------

    if (
        (
            "PROJET" in texto
            or
            "OBRA" in texto
        )
        and
        (
            "TECNICO" in texto
            or
            re.search(
                r"\bTEC\b",
                texto
            )
        )
    ):

        return (
            "Técnico de Projetos "
            "e Obras"
        )
=======
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
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b


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
<<<<<<< HEAD
    # COORDENADOR
    # --------------------------------------------------------

    if "COORDEN" in texto:

        return "Coordenador"


    # --------------------------------------------------------
    # SUPERVISOR
    # --------------------------------------------------------

    if "SUPERVIS" in texto:

        return "Supervisor"


    # --------------------------------------------------------
=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    # ASSISTENTE
    # --------------------------------------------------------

    if "ASSIST" in texto:

        return "Assistente"


    # --------------------------------------------------------
    # TRAINEE
    # --------------------------------------------------------

    if "TRAINEE" in texto:

        return "Trainee"


<<<<<<< HEAD
=======
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


>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    return "Outros"


# ============================================================
<<<<<<< HEAD
# CARREGAMENTO DAS BASES ESS
=======
# CARREGAMENTO DAS BASES
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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
<<<<<<< HEAD
    )


# ============================================================
# RESUMO DE INSPEÇÕES
# ============================================================

def resumo_inspecoes(base):

    if base.empty:

        return {
            "total": 0,
            "equipes": 0,
            "repetidas": 0,
        }


    # Uma inspeção pode aparecer em várias linhas no ESS
    # por causa de membro, item, conformidade etc.
    #
    # Por isso consideramos uma ocorrência por:
    #
    # Inspeção + Equipe

    base_unica = (
        base[
            [
                "Inspeção",
                "Chave Equipe"
            ]
        ]
        .dropna(
            subset=[
                "Inspeção",
                "Chave Equipe"
            ]
        )
        .drop_duplicates()
    )


    total = len(
        base_unica
    )


    equipes = (
        base_unica[
            "Chave Equipe"
        ]
        .nunique()
    )


    repetidas = max(
        total
        -
        equipes,
        0
    )


    return {
        "total":
            int(total),

        "equipes":
            int(equipes),

        "repetidas":
            int(repetidas),
    }


=======
    )


>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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

<<<<<<< HEAD
logo_jornada_b64 = imagem_base64(
    LOGO_JORNADA
)

logo_eqtl_b64 = imagem_base64(
    LOGO_EQTL
=======
logo_jornada_b64 = (
    imagem_base64(
        LOGO_JORNADA
    )
)

logo_eqtl_b64 = (
    imagem_base64(
        LOGO_EQTL
    )
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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

<<<<<<< HEAD

    html,
    body,
    [class*="css"] {{

=======
    html,
    body,
    [class*="css"] {{
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        font-family:
            'Montserrat',
            'Segoe UI',
            sans-serif;
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    .stApp {{
<<<<<<< HEAD

        background:
            {CINZA_FUNDO};

=======
        background:
            {CINZA_FUNDO};
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    .block-container {{
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        padding-top:
            1.5rem;

        padding-bottom:
            3rem;

        max-width:
            1500px;
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    /* =======================================================
       SIDEBAR
    ======================================================= */

    [data-testid="stSidebar"] {{
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        background:
            linear-gradient(
                180deg,
                {AZUL_ESCURO} 0%,
                {AZUL_EQTL} 100%
            );
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    [data-testid="stSidebar"] * {{
<<<<<<< HEAD

        color:
            white;

=======
        color:
            white;
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    [data-testid="stSidebar"] label {{
<<<<<<< HEAD

        font-weight:
            600;

=======
        font-weight:
            600;
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    [data-testid="stSidebar"]
    [data-baseweb="select"] > div {{
<<<<<<< HEAD

        background:
            white;

=======
        background:
            white;
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    [data-testid="stSidebar"]
    [data-baseweb="select"] span {{
<<<<<<< HEAD

        color:
            {AZUL_ESCURO};

=======
        color:
            {AZUL_ESCURO};
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    /* =======================================================
       HERO
    ======================================================= */

    .hero {{
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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
<<<<<<< HEAD
            18px;
=======
            32px;
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b

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
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    .hero::after {{
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    .hero-grid {{
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    .hero-text {{
<<<<<<< HEAD

        flex:
            1;

=======
        flex:
            1;
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    .hero-tag {{
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    .hero-title {{
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    .hero-title-highlight {{
<<<<<<< HEAD

        color:
            {AMARELO};

=======
        color:
            {AMARELO};
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    .hero-subtitle {{
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        color:
            rgba(
                255,
                255,
                255,
<<<<<<< HEAD
                .90
=======
                .88
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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
<<<<<<< HEAD

    }}


    /* =======================================================
       FONTE ESS
    ======================================================= */

    .source-banner {{

        background:
            white;

        border:
            1px solid
            {CINZA_BORDA};

        border-left:
            6px solid
            {AZUL_PRINCIPAL};

        border-radius:
            12px;

        padding:
            14px 18px;

        margin-bottom:
            25px;

        display:
            flex;

        align-items:
            center;

        gap:
            15px;

        box-shadow:
            0 4px 12px
            rgba(
                0,
                32,
                96,
                .04
            );

    }}


    .source-badge {{

        background:
            {AZUL_ESCURO};

        color:
            white;

        font-size:
            12px;

        font-weight:
            800;

        padding:
            7px 12px;

        border-radius:
            8px;

        white-space:
            nowrap;

    }}


    .source-text {{

        color:
            {AZUL_ESCURO};

        font-size:
            13px;

        font-weight:
            600;

    }}


    .source-text span {{

        color:
            {CINZA_TEXTO};

        font-weight:
            500;

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    /* =======================================================
       LOGO
    ======================================================= */

    .hero-logo-container {{
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        min-width:
            300px;

        display:
            flex;

        align-items:
            center;

        justify-content:
            center;
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    .hero-logo-box {{
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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

<<<<<<< HEAD
=======
        box-shadow:
            0 10px 28px
            rgba(
                0,
                0,
                0,
                .08
            );
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    .hero-logo-inner {{
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    .hero-logo {{
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        width:
            265px;

        max-height:
            105px;

        object-fit:
            contain;
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    /* =======================================================
<<<<<<< HEAD
       SEÇÕES
    ======================================================= */

    .section-title {{

=======
       SECTION
    ======================================================= */

    .section-title {{
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        border-left:
            6px solid
            {AMARELO};

        padding-left:
            14px;

        margin-top:
<<<<<<< HEAD
            32px;

        margin-bottom:
            18px;

=======
            30px;

        margin-bottom:
            18px;
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    .section-title h2 {{
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        color:
            {AZUL_ESCURO};

        font-size:
            22px;

        font-weight:
            900;

        margin:
            0;
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    .section-title p {{
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        color:
            {CINZA_TEXTO};

        font-size:
            12px;

        margin:
            5px 0 0 0;
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    /* =======================================================
       KPI
    ======================================================= */

    .kpi-card {{
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    .kpi-card::before {{
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    .kpi-label {{
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    .kpi-value {{
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        color:
            {AZUL_ESCURO};

        font-size:
            29px;

        font-weight:
            900;

        margin-bottom:
            9px;
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    .kpi-subtitle {{
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        color:
            {CINZA_TEXTO};

        font-size:
            11px;

        font-weight:
            500;

        line-height:
            1.4;
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    /* =======================================================
<<<<<<< HEAD
       BOXES
    ======================================================= */

    .warning-box {{

=======
       ALERTA
    ======================================================= */

    .warning-box {{
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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
<<<<<<< HEAD

    }}


    .blue-box {{

        background:
            #EEF4FF;

        border:
            1px solid
            #D8E5FF;

        border-left:
            5px solid
            {AZUL_PRINCIPAL};

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

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    /* =======================================================
       TABELAS
    ======================================================= */

    [data-testid="stDataFrame"] {{
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        background:
            white;

        border:
            1px solid
            {CINZA_BORDA};

        border-radius:
            14px;

        overflow:
            hidden;
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    }}


    /* =======================================================
       RESPONSIVO
    ======================================================= */

    @media (max-width: 900px) {{

        .hero-grid {{
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
            flex-direction:
                column;

            align-items:
                flex-start;
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        }}


        .hero-title {{
<<<<<<< HEAD

            font-size:
                34px;

=======
            font-size:
                34px;
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        }}


        .hero-logo-container {{
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
            min-width:
                0;

            width:
                100%;
<<<<<<< HEAD

        }}


        .source-banner {{

            align-items:
                flex-start;

            flex-direction:
                column;

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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

<<<<<<< HEAD
                    PMS • Meta de 100% das equipes
                    com contato da liderança
                    em cada ciclo de 3 meses.
=======
                    Meta: 100% das equipes com contato
                    da liderança dentro de cada ciclo de 3 meses.
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b

                </p>

            </div>

            {logo_html}

        </div>

    </div>
    """
)


# ============================================================
<<<<<<< HEAD
# DESTAQUE DA FONTE ESS
# ============================================================

st.html(
    """
    <div class="source-banner">

        <div class="source-badge">
            FONTE: ESS
        </div>

        <div class="source-text">

            Dados extraídos do
            <strong>ESS</strong>

            <span>
                • Recorte principal do dashboard:
                Operação Segura via PMS
            </span>

        </div>

    </div>
    """
)


# ============================================================
# LOCALIZA OS ARQUIVOS ESS
=======
# LOCALIZA ARQUIVOS
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
# ============================================================

if not PASTA_BASE.exists():

    st.error(
        "A pasta `base` não foi encontrada "
<<<<<<< HEAD
        "ao lado do app.py."
=======
        "ao lado do arquivo app.py."
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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
<<<<<<< HEAD
        "Nenhum arquivo ESS `.xlsx` foi encontrado "
=======
        "Nenhum arquivo `.xlsx` foi encontrado "
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        "na pasta `base`."
    )

    st.stop()


# ============================================================
<<<<<<< HEAD
# CARREGAMENTO DAS BASES ESS
# ============================================================

df, erros_carregamento = (
    carregar_bases(
        [
            str(arquivo)
            for arquivo
            in arquivos_excel
        ]
=======
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
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    )
)


if df.empty:

    st.error(
<<<<<<< HEAD
        "Nenhuma base ESS pôde ser carregada."
    )

    st.stop()


# ============================================================
# VALIDAÇÃO DAS COLUNAS
# ============================================================

COLUNAS_OBRIGATORIAS = [
    "ID da Equipe",
    "Data de Execução",
    "Inspeção",
    "Inspetor",
    "Cargo",
    "Origem",
    "Conformidade",
]


colunas_faltantes = [
    coluna
    for coluna
    in COLUNAS_OBRIGATORIAS
    if coluna
    not in df.columns
]


if colunas_faltantes:

    st.error(
        "A base ESS não possui as seguintes "
        "colunas obrigatórias: "
        +
        ", ".join(
            colunas_faltantes
        )
=======
        "Nenhuma base pôde ser carregada."
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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
<<<<<<< HEAD
=======
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
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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


<<<<<<< HEAD
=======
# ============================================================
# CLASSIFICA NÃO LÍDER
# ============================================================

>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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


<<<<<<< HEAD
=======
# ============================================================
# CONFORMIDADE
# ============================================================

>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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


<<<<<<< HEAD
=======
# ============================================================
# ORIGEM
# ============================================================

>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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


<<<<<<< HEAD
=======
# ============================================================
# CHAVE ÚNICA DA EQUIPE
# ============================================================

>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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


st.sidebar.caption(
    "Fonte de dados: ESS"
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
<<<<<<< HEAD
    for _, nome
=======
    for sigla, nome
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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
        "Nenhuma data válida encontrada na base ESS."
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
<<<<<<< HEAD
        )
    ]
    .copy()
)


if df_periodo.empty:

    st.warning(
        "Não há registros ESS no período selecionado."
=======
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
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    )

    st.stop()


# ============================================================
<<<<<<< HEAD
# UNIVERSO DE EQUIPES
# ============================================================
#
# O universo é criado antes de filtrar PMS.
#
# Dessa forma, uma equipe sem PMS continua
# aparecendo no denominador da taxa de contato.
=======
# UNIVERSO DAS EQUIPES
# ============================================================
#
# IMPORTANTE:
#
# Criado ANTES do filtro de origem.
#
# Assim não diminuímos artificialmente
# o denominador da Taxa de Contato.
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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
        "Nenhuma equipe encontrada na base ESS."
    )

    st.stop()


# ============================================================
<<<<<<< HEAD
# BASE DE CONTEXTO
# ============================================================

df_contexto = (
    df_periodo[
        ~df_periodo[
            "Origem Padronizada"
        ]
        .isin(
            ORIGENS_EXCLUIDAS
        )
=======
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
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    ]
    .copy()
)


# ============================================================
<<<<<<< HEAD
# BASE PRINCIPAL - PMS
# ============================================================

df_pms = (
    df_contexto[
        df_contexto[
            "Origem Padronizada"
        ]
        ==
        ORIGEM_PRINCIPAL
    ]
    .copy()
)
=======
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
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b


# ============================================================
# PMS - LIDERANÇA
# ============================================================

df_pms_lideranca = (
    df_pms[
        df_pms[
            "É Liderança"
        ]
    ]
    .copy()
)


# ============================================================
# TODAS AS ORIGENS - LIDERANÇA
# ============================================================

df_contexto_lideranca = (
    df_contexto[
        df_contexto[
            "É Liderança"
        ]
    ]
    .copy()
)


# ============================================================
# PMS - NÃO LÍDERES
# ============================================================

df_pms_nao_lider = (
    df_pms[
        ~df_pms[
            "É Liderança"
        ]
    ]
    .copy()
)


df_pms_nao_lider = (
    df_pms_nao_lider[
        df_pms_nao_lider[
            "Inspetor"
        ]
        .notna()
        &
        df_pms_nao_lider[
            "Perfil Não Líder"
        ]
        .notna()
    ]
    .copy()
)


df_pms_nao_lider_limpo = (
    df_pms_nao_lider[
        df_pms_nao_lider[
            "Perfil Não Líder"
        ]
        !=
        "Outros"
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


bases_com_mes = [
    df_pms_lideranca,
    df_contexto_lideranca,
    df_pms_nao_lider,
    df_pms_nao_lider_limpo,
]


for base in bases_com_mes:

    base[
        "Mês Número"
    ] = (
        base[
            "Data de Execução"
        ]
        .dt.month
    )


    base[
        "Mês"
    ] = (
        base[
            "Mês Número"
        ]
        .map(
            meses
        )
    )


# ============================================================
# META DE LIDERANÇA
# ============================================================

siglas_no_recorte = sorted(
    df_periodo[
        "Sigla Distribuidora"
    ]
    .dropna()
    .unique()
)


<<<<<<< HEAD
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
# INSPEÇÕES PMS POR EQUIPE / MÊS
# ============================================================

if df_pms_lideranca.empty:

    inspecoes_equipe_mes = (
        pd.DataFrame(
            0,
            index=
                todas_equipes,
            columns=[
                1,
                2,
                3,
                4,
                5,
                6
            ]
        )
    )

else:

    inspecoes_equipe_mes = (
        df_pms_lideranca
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
=======
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
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    )


inspecoes_equipe_mes.columns = (
    ordem_meses
)


# ============================================================
<<<<<<< HEAD
# COBERTURA
=======
# HOUVE CONTATO?
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
# ============================================================

teve_contato = (
    inspecoes_equipe_mes
    >
    0
)


<<<<<<< HEAD
contato_t1 = (
=======
# ============================================================
# T1
# ============================================================

contato_t1_equipe = (
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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


<<<<<<< HEAD
contato_t2 = (
=======
# ============================================================
# T2
# ============================================================

contato_t2_equipe = (
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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


<<<<<<< HEAD
contato_semestre = (
=======
# ============================================================
# SEMESTRE
# ============================================================

contato_semestre_equipe = (
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    teve_contato
    .any(
        axis=1
    )
)


# ============================================================
<<<<<<< HEAD
# TAXA DE CONTATO
=======
# CÁLCULOS
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
# ============================================================

equipes_contato_t1 = int(
    contato_t1.sum()
)


equipes_contato_t2 = int(
    contato_t2.sum()
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


<<<<<<< HEAD
gap_t1 = (
=======
gap_t1_pp = (
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    META_TAXA_CONTATO
    -
    taxa_t1
) * 100


<<<<<<< HEAD
gap_t2 = (
=======
gap_t2_pp = (
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    META_TAXA_CONTATO
    -
    taxa_t2
) * 100
<<<<<<< HEAD


# ============================================================
# INSPEÇÕES PMS - T1 / T2 / SEMESTRE
# ============================================================

base_t1 = (
    df_pms_lideranca[
        df_pms_lideranca[
            "Mês Número"
        ]
        .between(
            1,
            3
        )
    ]
)


base_t2 = (
    df_pms_lideranca[
        df_pms_lideranca[
            "Mês Número"
        ]
        .between(
            4,
            6
        )
    ]
)


resumo_t1 = resumo_inspecoes(
    base_t1
)


resumo_t2 = resumo_inspecoes(
    base_t2
)


resumo_semestre = resumo_inspecoes(
    df_pms_lideranca
)


# ============================================================
# TABELA RESUMO DAS INSPEÇÕES
# ============================================================

tabela_resumo_inspecoes = (
    pd.DataFrame(
        [
            {
                "Período":
                    "T1",

                "Total de inspeções realizadas":
                    resumo_t1[
                        "total"
                    ],

                "Equipes únicas com contato":
                    resumo_t1[
                        "equipes"
                    ],

                "Inspeções em equipes já contatadas":
                    resumo_t1[
                        "repetidas"
                    ],
            },

            {
                "Período":
                    "T2",

                "Total de inspeções realizadas":
                    resumo_t2[
                        "total"
                    ],

                "Equipes únicas com contato":
                    resumo_t2[
                        "equipes"
                    ],

                "Inspeções em equipes já contatadas":
                    resumo_t2[
                        "repetidas"
                    ],
            },

            {
                "Período":
                    "Semestre",

                "Total de inspeções realizadas":
                    resumo_semestre[
                        "total"
                    ],

                "Equipes únicas com contato":
                    resumo_semestre[
                        "equipes"
                    ],

                "Inspeções em equipes já contatadas":
                    resumo_semestre[
                        "repetidas"
                    ],
            },
        ]
    )
)


# ============================================================
# LIDERANÇAS ATIVAS
# ============================================================

lideres_ativos = (
    df_pms_lideranca[
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
# LIDERANÇA POR TIPO
# ============================================================

lideres_por_tipo = (
    df_pms_lideranca
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
    "Pessoas com inspeção PMS",
]


# ============================================================
# LIDERANÇAS ATIVAS POR MÊS
# ============================================================

lideres_mensais = []


for numero_mes, nome_mes in meses.items():

    base_mes = (
        df_pms_lideranca[
            df_pms_lideranca[
                "Mês Número"
            ]
            ==
            numero_mes
        ]
    )


    quantidade = (
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


    lideres_mensais.append(
        {
            "Mês":
                nome_mes,

            "Lideranças com inspeção PMS":
                int(
                    quantidade
                ),
        }
    )


lideres_mensais = (
    pd.DataFrame(
        lideres_mensais
    )
)
=======


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
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b


# ============================================================
# PARTICIPAÇÃO DA LIDERANÇA
# ============================================================

if (
    meta_lideres is not None
    and
    meta_lideres > 0
):

    aderencia_lideres = (
        lideres_ativos
        /
        meta_lideres
    )

else:

    aderencia_lideres = None


# ============================================================
# COBERTURA MENSAL
# ============================================================

resumo_cobertura_mensal = []


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


    resumo_cobertura_mensal.append(
        {
            "Mês":
                nome_mes,

            "Equipes únicas com contato":
                com_contato,

            "Equipes sem contato":
                sem_contato,
        }
    )


<<<<<<< HEAD
resumo_cobertura_mensal = (
    pd.DataFrame(
        resumo_cobertura_mensal
    )
)


# ============================================================
# INSPEÇÕES POR ORIGEM
# ============================================================

inspecoes_origem = (
    df_contexto_lideranca[
        [
            "Origem Padronizada",
            "Inspeção",
            "Chave Equipe"
        ]
    ]
    .dropna(
        subset=[
            "Inspeção",
            "Chave Equipe"
=======
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
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        ]
    )
<<<<<<< HEAD
    .drop_duplicates()
)


inspecoes_por_origem = (
    inspecoes_origem
    .groupby(
        "Origem Padronizada"
    )
    .size()
    .reset_index(
        name=
            "Total de inspeções"
    )
)


ordem_origens = [
    "PMS",
    "Rotina",
    "Mutirão",
    "Altas Horas",
    "Outras",
]


inspecoes_por_origem[
    "Ordem"
] = (
    inspecoes_por_origem[
        "Origem Padronizada"
    ]
    .map(
        {
            origem:
                indice
            for indice, origem
            in enumerate(
                ordem_origens
            )
        }
    )
    .fillna(
        999
    )
)


inspecoes_por_origem = (
    inspecoes_por_origem
    .sort_values(
        "Ordem"
=======


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
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    )
)


<<<<<<< HEAD
total_inspecoes_contexto = len(
    inspecoes_origem
)


total_inspecoes_pms = (
    resumo_semestre[
        "total"
    ]
)


total_inspecoes_outras_origens = max(
    total_inspecoes_contexto
    -
    total_inspecoes_pms,
    0
)


# ============================================================
# NÃO LÍDERES
# ============================================================

total_inspetores_nao_lideres = (
    df_pms_nao_lider_limpo[
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


nao_lideres_resumo = (
    df_pms_nao_lider_limpo
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


=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
# ============================================================
# CONFORMIDADE POR INSPEÇÃO
# ============================================================

<<<<<<< HEAD
if df_pms_lideranca.empty:

    status_inspecoes = (
        pd.DataFrame(
            columns=[
                "Inspeção",
                "Chave Equipe",
                "Data",
                "Possui_NC",
                "Status",
                "Mês Número",
                "Mês",
            ]
=======
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
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        )
    )

else:

    status_inspecoes = (
        df_pms_lideranca
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
                    "Conforme",
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


<<<<<<< HEAD
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

=======
# ============================================================
# MÉTRICAS DE CONFORMIDADE
# ============================================================
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b

total_inspecoes_analisadas = len(
    status_inspecoes
)


total_conformes = int(
    (
        status_inspecoes[
            "Status"
        ]
        ==
        "Conforme"
    )
    .sum()
)


total_nao_conformes = int(
    (
        status_inspecoes[
            "Status"
        ]
        ==
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
    df_pms_lideranca[
        df_pms_lideranca[
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
        ==
        "",
        "Não Conformidade"
    ] = (
        "Sem descrição informada"
    )


<<<<<<< HEAD
    chaves_nc = [
        coluna
        for coluna
        in [
            "Inspeção",
            "Chave Equipe",
            "Membro",
            "Não Conformidade",
=======
    colunas_chave_nc = [
        coluna
        for coluna in [
            "Inspeção",
            "Chave Equipe",
            "Membro",
            "Não Conformidade"
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        ]
        if coluna
        in nc_detalhe.columns
    ]


<<<<<<< HEAD
    if chaves_nc:
=======
    if colunas_chave_nc:
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b

        nc_detalhe = (
            nc_detalhe
            .drop_duplicates(
                subset=
<<<<<<< HEAD
                    chaves_nc
=======
                    colunas_chave_nc
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
            )
        )


# ============================================================
<<<<<<< HEAD
# 1. OPERAÇÃO SEGURA - PMS
# ============================================================

titulo_secao(
    "Operação Segura — PMS",
    (
        "Indicadores calculados a partir dos registros "
        "do ESS com origem PMS."
=======
# OBJETIVO CENTRAL
# ============================================================

titulo_secao(
    "Objetivo central",
    (
        "Verificar se 100% das equipes receberam pelo menos "
        "um contato da liderança em cada ciclo de 3 meses."
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    )
)


st.html(
<<<<<<< HEAD
    """
=======
    f"""
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    <div class="warning-box">

        <strong>
            Regra da Taxa de Contato:
        </strong>

<<<<<<< HEAD
        100% das equipes devem receber pelo menos um contato
        da liderança dentro de cada ciclo de três meses.

        <br><br>

        Uma equipe que recebeu várias inspeções continua
        representando somente uma equipe coberta.
=======
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
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b

    </div>
    """
)


# ============================================================
<<<<<<< HEAD
# TAXA DE CONTATO
# ============================================================

c1, c2, c3, c4 = st.columns(
    4
)
=======
# CARDS PRINCIPAIS
# ============================================================

c1, c2, c3, c4 = st.columns(4)
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b


with c1:

    card_kpi(
        "Meta trimestral",
        "100%",
<<<<<<< HEAD
        "equipes com contato em até 3 meses",
=======
        "das equipes em até 3 meses",
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        AMARELO
    )


with c2:

    card_kpi(
        "Taxa de Contato T1",
        f"{taxa_t1:.1%}",
        (
<<<<<<< HEAD
            f"{equipes_sem_contato_t1} "
            f"equipes ainda sem contato"
=======
            f"{equipes_sem_contato_t1} equipes pendentes"
            f" • gap {gap_t1_pp:.1f} p.p."
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        ),
        LARANJA
    )


with c3:

    card_kpi(
        "Taxa de Contato T2",
        f"{taxa_t2:.1%}",
        (
<<<<<<< HEAD
            f"{equipes_sem_contato_t2} "
            f"equipes ainda sem contato"
=======
            f"{equipes_sem_contato_t2} equipes pendentes"
            f" • gap {gap_t2_pp:.1f} p.p."
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        ),
        LARANJA
    )


with c4:

    card_kpi(
<<<<<<< HEAD
        "Equipes no universo",
        total_equipes,
        "equipes identificadas na base ESS",
=======
        "Total de equipes",
        total_equipes,
        "universo do indicador",
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        AZUL_PRINCIPAL
    )


# ============================================================
# TAXA X META
# ============================================================

<<<<<<< HEAD
=======
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


>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
fig_meta = go.Figure()


fig_meta.add_trace(
    go.Bar(

<<<<<<< HEAD
        x=[
            "T1",
            "T2"
        ],

        y=[
            taxa_t1 * 100,
            taxa_t2 * 100
        ],
=======
        x=
            comparativo_meta[
                "Trimestre"
            ],

        y=
            comparativo_meta[
                "Taxa"
            ],
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b

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
<<<<<<< HEAD
            "Taxa realizada",
=======
            "Taxa realizada"
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    )
)


fig_meta.add_hline(
<<<<<<< HEAD

    y=
        100,
=======
    y=100,
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b

    line_dash=
        "dash",

    line_color=
        AMARELO,

<<<<<<< HEAD
    line_width=
        3,

    annotation_text=
        "Meta = 100%",

    annotation_position=
        "top right",
=======
    line_width=3,

    annotation_text=
        "Meta 100%",

    annotation_position=
        "top right"
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
)


fig_meta.update_yaxes(
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    range=[
        0,
        110
    ],

    title=
<<<<<<< HEAD
        "% das equipes com contato",
=======
        "Taxa de contato (%)"
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
)


aplicar_layout_plotly(
    fig_meta,
    (
<<<<<<< HEAD
        "Cobertura das equipes no PMS "
        "em cada ciclo de 3 meses"
=======
        "Taxa de Contato realizada x "
        "meta de 100% em 3 meses"
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    )
)


st.plotly_chart(
    fig_meta,
    use_container_width=True
)


# ============================================================
<<<<<<< HEAD
# 2. VOLUME X COBERTURA
# ============================================================

titulo_secao(
    "Volume de inspeções x cobertura das equipes",
    (
        "Diferencia o total de inspeções registradas no ESS "
        "da quantidade de equipes efetivamente alcançadas."
=======
# PRESENÇA DA LIDERANÇA
# ============================================================

titulo_secao(
    "Presença da liderança",
    (
        "Líderes, Gerentes, Executivos e Superintendentes "
        "que realizaram pelo menos uma inspeção."
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    )
)


<<<<<<< HEAD
c1, c2, c3, c4 = st.columns(
    4
=======
c1, c2, c3, c4 = (
    st.columns(4)
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
)


with c1:

    card_kpi(
<<<<<<< HEAD
        "Total de inspeções PMS",
        resumo_semestre[
            "total"
        ],
        "inspeções realizadas pela liderança",
=======
        "Lideranças ativas",
        lideres_ativos_semestre,
        "inspetores distintos no semestre",
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        AZUL_PRINCIPAL
    )


with c2:

    card_kpi(
<<<<<<< HEAD
        "Equipes únicas com contato",
        resumo_semestre[
            "equipes"
        ],
        "cada equipe é contada apenas uma vez",
        VERDE
    )


with c3:

    card_kpi(
        "Inspeções repetidas",
        resumo_semestre[
            "repetidas"
        ],
        "inspeções em equipes já contatadas",
        LARANJA
    )


with c4:

    card_kpi(
        "Lideranças que fizeram PMS",
        lideres_ativos,
        "pessoas com pelo menos uma inspeção",
        AZUL_MEDIO
    )


st.html(
    """
    <div class="blue-box">

        <strong>
            Como interpretar:
        </strong>

        se o ESS registrar 162 inspeções e essas inspeções
        alcançarem 130 equipes diferentes, então 32 inspeções
        ocorreram em equipes que já haviam recebido contato.

        <br><br>

        Essas inspeções representam esforço da liderança,
        mas não aumentam a quantidade de equipes cobertas
        pela Taxa de Contato.

    </div>
    """
)


st.dataframe(
    tabela_resumo_inspecoes,
    use_container_width=True,
    hide_index=True,
)


# ============================================================
# 3. LIDERANÇA
# ============================================================

titulo_secao(
    "Participação da liderança na Operação Segura",
    (
        "Pessoas identificadas no ESS que realizaram "
        "pelo menos uma inspeção PMS."
    )
)


c1, c2, c3 = st.columns(
    3
)


with c1:

    card_kpi(
        "Lideranças ativas no PMS",
        lideres_ativos,
        "pessoas com pelo menos uma inspeção PMS",
        AZUL_PRINCIPAL
    )


with c2:

    card_kpi(
        "Meta de lideranças",
=======
        "Meta de líderes",
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        (
            meta_lideres
            if meta_lideres
            is not None
<<<<<<< HEAD
            else
            "N/D"
        ),
        (
            "meta cadastrada para a distribuidora"
=======
            else "N/D"
        ),
        (
            "Meta da distribuidora"
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
            if meta_lideres
            is not None
            else
            "meta ainda não cadastrada"
        ),
        AMARELO
    )


with c3:

    card_kpi(
<<<<<<< HEAD
        "Participação da liderança",
=======
        "Presença acumulada",
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        (
            f"{aderencia_lideres:.1%}"
            if aderencia_lideres
            is not None
            else
            "N/D"
        ),
        (
<<<<<<< HEAD
            "lideranças com PMS ÷ meta cadastrada"
            if aderencia_lideres
            is not None
            else
            "aguardando meta da distribuidora"
        ),
=======
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
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        AZUL_MEDIO
    )


# ============================================================
<<<<<<< HEAD
# GRÁFICOS DA LIDERANÇA
# ============================================================

col1, col2 = st.columns(
    2
=======
# GRÁFICOS DE LIDERANÇA
# ============================================================

col1, col2 = (
    st.columns(2)
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
)


with col1:

<<<<<<< HEAD
    fig_tipo = px.bar(

=======
    fig_tipo_lider = px.bar(
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        lideres_por_tipo,

        x=
            "Tipo de liderança",

        y=
<<<<<<< HEAD
            "Pessoas com inspeção PMS",

        text=
            "Pessoas com inspeção PMS",
=======
            "Quantidade de líderes",

        text=
            "Quantidade de líderes",
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b

        color=
            "Tipo de liderança",

        color_discrete_map={
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
            "Líder":
                AZUL_CLARO,

            "Gerente":
                AZUL_MEDIO,

            "Executivo":
                AZUL_PRINCIPAL,

            "Superintendente":
                AZUL_ESCURO,
<<<<<<< HEAD

            "Técnico de Distribuição":
                AMARELO,
=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        }
    )


<<<<<<< HEAD
    fig_tipo.update_traces(
=======
    fig_tipo_lider.update_traces(
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        textposition=
            "outside"
    )


<<<<<<< HEAD
    fig_tipo.update_layout(
=======
    fig_tipo_lider.update_layout(
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        showlegend=
            False
    )


    aplicar_layout_plotly(
<<<<<<< HEAD
        fig_tipo,
        (
            "Pessoas com inspeção PMS "
            "por tipo de liderança"
        )
    )


    fig_tipo.update_yaxes(
        title=
            "Quantidade de pessoas"
    )


    fig_tipo.update_xaxes(
        title=""
=======
        fig_tipo_lider,
        "Quantidade de lideranças ativas por tipo"
    )


    fig_tipo_lider.update_yaxes(
        title=
            "Inspetores distintos"
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    )


    st.plotly_chart(
<<<<<<< HEAD
        fig_tipo,
=======
        fig_tipo_lider,
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        use_container_width=True
    )


with col2:

<<<<<<< HEAD
    fig_lideres_mes = go.Figure()


    fig_lideres_mes.add_trace(
        go.Bar(

            x=
                lideres_mensais[
=======
    fig_presenca = go.Figure()


    fig_presenca.add_trace(
        go.Bar(

            x=
                resumo_mensal[
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
                    "Mês"
                ],

            y=
<<<<<<< HEAD
                lideres_mensais[
                    "Lideranças com inspeção PMS"
                ],

            text=
                lideres_mensais[
                    "Lideranças com inspeção PMS"
=======
                resumo_mensal[
                    "Líderes ativos"
                ],

            text=
                resumo_mensal[
                    "Líderes ativos"
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
                ],

            textposition=
                "outside",

            marker_color=[
                AZUL_CLARO,
                AZUL_CLARO,
                AZUL_CLARO,
                AZUL_PRINCIPAL,
                AZUL_PRINCIPAL,
<<<<<<< HEAD
                AZUL_PRINCIPAL,
            ],

            name=
                "Pessoas com PMS",
=======
                AZUL_PRINCIPAL
            ],

            name=
                "Lideranças ativas"
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        )
    )


<<<<<<< HEAD
    if (
        meta_lideres
        is not None
    ):

        fig_lideres_mes.add_hline(

=======
    if meta_lideres is not None:

        fig_presenca.add_hline(
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
            y=
                meta_lideres,

            line_dash=
                "dash",

            line_color=
                AMARELO,

<<<<<<< HEAD
            line_width=
                3,

            annotation_text=
                f"Meta = {meta_lideres}",

            annotation_position=
                "top right",
=======
            line_width=3,

            annotation_text=
                f"Meta: {meta_lideres}",

            annotation_position=
                "top right"
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        )


    aplicar_layout_plotly(
<<<<<<< HEAD
        fig_lideres_mes,
        (
            "Pessoas da liderança que realizaram "
            "PMS em cada mês"
=======
        fig_presenca,
        (
            "Quantidade de lideranças distintas "
            "com inspeção por mês"
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        )
    )


<<<<<<< HEAD
    fig_lideres_mes.update_yaxes(
        title=
            "Quantidade de pessoas"
    )


    fig_lideres_mes.update_xaxes(
        title=""
=======
    fig_presenca.update_yaxes(
        title=
            "Lideranças ativas"
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    )


    st.plotly_chart(
<<<<<<< HEAD
        fig_lideres_mes,
=======
        fig_presenca,
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        use_container_width=True
    )


<<<<<<< HEAD
=======
# ============================================================
# TABELA LIDERANÇA
# ============================================================

>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
st.dataframe(
    lideres_por_tipo,
    use_container_width=True,
    hide_index=True
)


# ============================================================
<<<<<<< HEAD
# 4. COBERTURA MENSAL
# ============================================================

titulo_secao(
    "Cobertura mensal das equipes no PMS",
    (
        "Quantidade de equipes diferentes que receberam "
        "pelo menos uma inspeção PMS no mês."
=======
# COBERTURA MENSAL
# ============================================================

titulo_secao(
    "Cobertura mensal das equipes",
    (
        "Mostra quantas equipes tiveram pelo menos uma "
        "inspeção da liderança em cada mês."
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    )
)


<<<<<<< HEAD
fig_cobertura = go.Figure()


fig_cobertura.add_trace(
    go.Bar(

        name=
            "Equipes únicas com contato",

        x=
            resumo_cobertura_mensal[
=======
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
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
                "Mês"
            ],

        y=
<<<<<<< HEAD
            resumo_cobertura_mensal[
                "Equipes únicas com contato"
            ],

        text=
            resumo_cobertura_mensal[
                "Equipes únicas com contato"
            ],

        textposition=
            "inside",

        marker_color=[
            AZUL_CLARO,
            AZUL_CLARO,
            AZUL_CLARO,
            AZUL_PRINCIPAL,
            AZUL_PRINCIPAL,
            AZUL_PRINCIPAL,
        ],
    )
)


fig_cobertura.add_trace(
    go.Bar(

        name=
            "Equipes sem contato",

        x=
            resumo_cobertura_mensal[
                "Mês"
            ],

        y=
            resumo_cobertura_mensal[
                "Equipes sem contato"
            ],

        text=
            resumo_cobertura_mensal[
                "Equipes sem contato"
=======
            resumo_mensal[
                "Com contato"
            ],

        text=
            resumo_mensal[
                "Com contato"
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
            ],

        textposition=
            "inside",

        marker_color=
<<<<<<< HEAD
            "#CDD7E5",
=======
            cores_com
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    )
)


<<<<<<< HEAD
fig_cobertura.update_layout(
=======
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
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    barmode=
        "stack"
)


aplicar_layout_plotly(
<<<<<<< HEAD
    fig_cobertura,
    (
        "Equipes alcançadas pela liderança "
        "em cada mês"
=======
    fig_mensal,
    (
        "Equipes com contato x "
        "sem contato em cada mês"
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    )
)


<<<<<<< HEAD
fig_cobertura.update_yaxes(
=======
fig_mensal.update_yaxes(
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    title=
        "Quantidade de equipes"
)


<<<<<<< HEAD
fig_cobertura.update_xaxes(
    title=""
)


st.plotly_chart(
    fig_cobertura,
=======
st.plotly_chart(
    fig_mensal,
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    use_container_width=True
)


# ============================================================
<<<<<<< HEAD
# 5. OUTRAS ORIGENS
# ============================================================

titulo_secao(
    "Esforço da liderança além do PMS",
    (
        "O PMS é o foco da Operação Segura. "
        "As demais origens do ESS aparecem como contexto."
=======
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
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    )
)


<<<<<<< HEAD
c1, c2, c3 = st.columns(
    3
=======
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
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
)


with c1:

    card_kpi(
<<<<<<< HEAD
        "Inspeções PMS",
        total_inspecoes_pms,
        "foco principal da Operação Segura",
        AZUL_PRINCIPAL
=======
        "Total de inspetores",
        total_inspetores_nao_lideres,
        "não líderes distintos",
        AZUL_MEDIO
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    )


with c2:

    card_kpi(
<<<<<<< HEAD
        "Inspeções em outras origens",
        total_inspecoes_outras_origens,
        "Rotina, Mutirão, Altas Horas e outras",
        AZUL_MEDIO
=======
        "Inspeções de não líderes",
        total_inspecoes_nao_lideres,
        "inspeções distintas",
        AZUL_PRINCIPAL
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    )


with c3:

    card_kpi(
<<<<<<< HEAD
        "Total de inspeções da liderança",
        total_inspecoes_contexto,
        "PMS + demais origens do recorte ESS",
        AMARELO
    )


if not inspecoes_por_origem.empty:

    cores_origem = [
        (
            AZUL_PRINCIPAL
            if origem
            ==
            "PMS"
            else
            AZUL_CLARO
        )
        for origem
        in inspecoes_por_origem[
            "Origem Padronizada"
        ]
    ]


    fig_origem = go.Figure()


    fig_origem.add_trace(
        go.Bar(

            x=
                inspecoes_por_origem[
                    "Origem Padronizada"
                ],

            y=
                inspecoes_por_origem[
                    "Total de inspeções"
                ],

            text=
                inspecoes_por_origem[
                    "Total de inspeções"
                ],

            textposition=
                "outside",

            marker_color=
                cores_origem,
        )
    )


    aplicar_layout_plotly(
        fig_origem,
        (
            "Quantidade de inspeções da liderança "
            "por origem no ESS"
        )
    )


    fig_origem.update_xaxes(
        title=""
    )


    fig_origem.update_yaxes(
        title=
            "Quantidade de inspeções"
    )


    fig_origem.update_layout(
        showlegend=False
    )


    st.plotly_chart(
        fig_origem,
        use_container_width=True
    )


# ============================================================
# 6. NÃO LÍDERES
# ============================================================

titulo_secao(
    "Participação de não líderes no PMS",
    (
        "Executivos e Técnicos de Distribuição não aparecem "
        "nesta seção, pois são considerados liderança."
    )
)


c1, c2 = st.columns(
    2
)


with c1:

    card_kpi(
        "Total de inspetores não líderes",
        total_inspetores_nao_lideres,
        "pessoas identificadas no ESS",
        AZUL_MEDIO
    )


with c2:

    card_kpi(
        "Perfis de não líderes",
=======
        "Perfis identificados",
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        nao_lideres_resumo[
            "Perfil Não Líder"
        ]
        .nunique(),
<<<<<<< HEAD
        "categorias após padronização dos cargos",
=======
        "categorias padronizadas",
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        AMARELO
    )


<<<<<<< HEAD
=======
# ============================================================
# GRÁFICO NÃO LÍDERES
# ============================================================

>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
if not nao_lideres_resumo.empty:

    grafico_nao_lideres = (
        nao_lideres_resumo
<<<<<<< HEAD
        .head(
            12
        )
=======
        .head(12)
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        .sort_values(
            "Inspetores",
            ascending=True
        )
    )


    fig_nao_lideres = px.bar(
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        grafico_nao_lideres,

        x=
            "Inspetores",

        y=
            "Perfil Não Líder",

        orientation=
            "h",

        text=
<<<<<<< HEAD
            "Inspetores",
=======
            "Inspetores"
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    )


    fig_nao_lideres.update_traces(
<<<<<<< HEAD

=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        marker_color=
            AZUL_MEDIO,

        textposition=
<<<<<<< HEAD
            "outside",
=======
            "outside"
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    )


    aplicar_layout_plotly(
        fig_nao_lideres,
        (
<<<<<<< HEAD
            "Pessoas não classificadas como liderança "
            "que realizaram PMS"
=======
            "Quantidade de inspetores "
            "não líderes por perfil"
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        )
    )


<<<<<<< HEAD
    fig_nao_lideres.update_yaxes(
        title=""
    )


    fig_nao_lideres.update_xaxes(
        title=
            "Quantidade de pessoas"
=======
    fig_nao_lideres.update_xaxes(
        title=
            "Inspetores distintos"
    )


    fig_nao_lideres.update_yaxes(
        title=""
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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
<<<<<<< HEAD
# 7. CONFORMIDADES
# ============================================================

titulo_secao(
    "Conformidades e não conformidades no PMS",
    (
        "Avaliação das inspeções de liderança "
        "registradas no ESS."
=======
# CONFORMIDADE
# ============================================================

titulo_secao(
    "Conformidades e não conformidades",
    (
        "Uma inspeção é considerada não conforme "
        "quando possui pelo menos um registro "
        "de não conformidade."
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    )
)


<<<<<<< HEAD
c1, c2, c3, c4 = st.columns(
    4
=======
c1, c2, c3, c4 = (
    st.columns(4)
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
)


with c1:

    card_kpi(
        "Inspeções analisadas",
        total_inspecoes_analisadas,
<<<<<<< HEAD
        "inspeções PMS avaliadas",
=======
        "inspeções distintas da liderança",
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        AZUL_PRINCIPAL
    )


with c2:

    card_kpi(
<<<<<<< HEAD
        "Sem não conformidade",
        total_conformes,
        "inspeções sem NC registrada",
=======
        "Conformes",
        total_conformes,
        "sem NC identificada",
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        VERDE
    )


with c3:

    card_kpi(
        "Com não conformidade",
        total_nao_conformes,
<<<<<<< HEAD
        "inspeções com pelo menos uma NC",
=======
        "com pelo menos 1 NC",
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        LARANJA
    )


with c4:

    card_kpi(
<<<<<<< HEAD
        "Percentual sem NC",
        f"{taxa_conformidade:.1%}",
        "inspeções sem NC ÷ inspeções analisadas",
=======
        "Taxa de conformidade",
        f"{taxa_conformidade:.1%}",
        "conformes ÷ analisadas",
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        VERDE
    )


<<<<<<< HEAD
if not status_inspecoes.empty:

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
            "Inspeções PMS sem NC x "
            "inspeções PMS com NC"
        )
    )


    fig_conformidade.update_yaxes(
        title=
            "Quantidade de inspeções"
    )


    fig_conformidade.update_xaxes(
        title=""
    )


    st.plotly_chart(
        fig_conformidade,
        use_container_width=True
    )
=======
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
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b


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
        "Ocorrências",
    ]


    top_nc = (
        ranking_nc
        .head(
            15
        )
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
<<<<<<< HEAD
            "Ocorrências",
=======
            "Ocorrências"
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    )


    fig_nc.update_traces(

        marker_color=
            LARANJA,

        textposition=
            "outside",
    )


    fig_nc.update_layout(
        height=
            620
    )


    aplicar_layout_plotly(
        fig_nc,
<<<<<<< HEAD
        (
            "Principais descrições "
            "de não conformidade"
        )
=======
        "Principais descrições de não conformidade"
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    )


    fig_nc.update_yaxes(
        title=""
    )


    st.plotly_chart(
        fig_nc,
        use_container_width=True
    )


# ============================================================
<<<<<<< HEAD
# DETALHAMENTO DAS NÃO CONFORMIDADES
=======
# DETALHAMENTO DAS NCS
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
# ============================================================

titulo_secao(
    "Detalhamento das não conformidades",
    (
<<<<<<< HEAD
        "Registros da base ESS relacionados "
        "às inspeções PMS da liderança."
=======
        "Ocorrências registradas nas inspeções "
        "realizadas pela liderança."
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
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
        hide_index=True,
    )


else:

    st.success(
        "Nenhuma não conformidade encontrada "
        "nas inspeções PMS do recorte selecionado."
    )


<<<<<<< HEAD
# ============================================================
# 8. INSPEÇÕES POR EQUIPE
# ============================================================

titulo_secao(
    "Inspeções PMS por equipe",
    (
        "Cada célula mostra quantas inspeções PMS "
        "da liderança estão registradas no ESS "
        "para aquela equipe no mês."
    )
=======
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
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
)


tabela_equipes = (
    inspecoes_equipe_mes
    .copy()
)


tabela_equipes[
    "Total no semestre"
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
<<<<<<< HEAD
        on=
            "Chave Equipe",
=======

        on=
            "Chave Equipe",

>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
        how=
            "left"
    )
)


colunas_tabela_equipes = [
    "Distribuidora",
    "ID da Equipe",
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
<<<<<<< HEAD
    "Total no semestre",
=======
    "Total",
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
]


tabela_equipes = (
    tabela_equipes[
        [
            coluna
            for coluna
<<<<<<< HEAD
            in colunas_tabela_equipes
=======
            in colunas_ordem
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
            if coluna
            in tabela_equipes.columns
        ]
    ]
)


opcao_equipes = st.radio(

    "Mostrar",

    [
        "Todas as equipes",
<<<<<<< HEAD
        "Somente equipes sem contato PMS",
        "Somente equipes com contato PMS",
=======
        "Somente equipes sem contato",
        "Somente equipes com contato",
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    ],

    horizontal=True,
)


if (
    opcao_equipes
    ==
    "Somente equipes sem contato PMS"
):

    tabela_exibicao = (
        tabela_equipes[
            tabela_equipes[
                "Total no semestre"
            ]
            ==
            0
        ]
    )


elif (
    opcao_equipes
    ==
    "Somente equipes com contato PMS"
):

    tabela_exibicao = (
        tabela_equipes[
            tabela_equipes[
                "Total no semestre"
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
    hide_index=True,
)


# ============================================================
<<<<<<< HEAD
# 9. VALIDAÇÃO COM A BASE ESS
=======
# ERROS DE CARREGAMENTO
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
# ============================================================

titulo_secao(
    "Validação com a base ESS",
    (
        "Memória de cálculo para conferência dos indicadores "
        "com os registros oficiais extraídos do ESS."
    )
)


st.html(
    """
    <div class="warning-box">

        <strong>
            Validação dos dados:
        </strong>

        o dashboard aplica regras de limpeza, padronização
        de cargos, identificação da liderança e classificação
        das origens sobre os registros extraídos do
        <strong>ESS</strong>.

        <br><br>

        A conferência final do recorte e das regras de negócio
        deve ser realizada junto ao cliente utilizando a
        própria fonte ESS como referência.

    </div>
    """
)


# ============================================================
# MEMÓRIA DE CÁLCULO
# ============================================================

with st.expander(
    "Memória de cálculo / validação ESS"
):

    st.write(
        "Fonte de dados: **ESS**"
    )


    st.write(
        f"Distribuidora: "
        f"**{distribuidora_selecionada}**"
    )


    st.write(
        f"Ano: "
        f"**{ano}**"
    )


    st.write(
<<<<<<< HEAD
        f"Equipes identificadas na base ESS: "
        f"**{total_equipes}**"
    )


    st.write(
        f"Total de inspeções PMS da liderança: "
        f"**{resumo_semestre['total']}**"
    )
=======
        f"Origens consideradas: "
        f"**{', '.join(origens_selecionadas)}**"
    )


    st.write(
        f"Total de equipes no universo: "
        f"**{total_equipes}**"
    )

>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b


    st.write(
        f"Equipes únicas com contato PMS: "
        f"**{resumo_semestre['equipes']}**"
    )


    st.write(
        f"Inspeções realizadas em equipes "
        f"já contatadas: "
        f"**{resumo_semestre['repetidas']}**"
    )


    st.write(
        f"Taxa de Contato T1: "
        f"**{taxa_t1:.1%}**"
    )


    st.write(
        f"Gap T1 para 100%: "
        f"**{gap_t1:.1f} p.p.**"
    )


    st.write(
        f"Taxa de Contato T1: "
        f"**{taxa_t1:.1%}**"
    )


    st.write(
        f"Equipes pendentes no T1: "
        f"**{equipes_sem_contato_t1}**"
    )

<<<<<<< HEAD

    st.write(
        f"Taxa de Contato T2: "
        f"**{taxa_t2:.1%}**"
    )
=======
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b


    st.write(
        f"Gap T2 para 100%: "
        f"**{gap_t2:.1f} p.p.**"
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
<<<<<<< HEAD
        f"Lideranças que realizaram PMS: "
        f"**{lideres_ativos}**"
    )

=======
        f"Lideranças ativas: "
        f"**{lideres_ativos_semestre}**"
    )


    st.write(
        f"Meta de lideranças: "
        f"**{meta_lideres if meta_lideres is not None else 'N/D'}**"
    )
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b


    st.write(
        f"Inspetores não líderes: "
        f"**{total_inspetores_nao_lideres}**"
    )


    st.write(
        f"Meta de lideranças: "
        f"**{meta_lideres if meta_lideres is not None else 'N/D'}**"
    )


    st.write(
        f"Inspetores não líderes classificados: "
        f"**{total_inspetores_nao_lideres}**"
    )


    st.write(
        f"Inspeções PMS sem NC: "
        f"**{total_conformes}**"
    )


    st.write(
        f"Inspeções PMS com NC: "
        f"**{total_nao_conformes}**"
    )


<<<<<<< HEAD
    # ========================================================
    # CARGOS AINDA NÃO CLASSIFICADOS
    # ========================================================

    cargos_outros = (
        df_pms_nao_lider[
            df_pms_nao_lider[
                "Perfil Não Líder"
            ]
            ==
            "Outros"
        ][
            "Cargo"
        ]
        .dropna()
        .astype(str)
        .str.strip()
        .value_counts()
        .reset_index()
=======
    st.write(
        f"Taxa de conformidade: "
        f"**{taxa_conformidade:.1%}**"
>>>>>>> 53b421b8e0724afa32b57e022fac068dad5eea2b
    )


    if not cargos_outros.empty:

        cargos_outros.columns = [
            "Cargo original no ESS",
            "Quantidade de registros",
        ]


        st.write(
            "#### Cargos do ESS ainda classificados como Outros"
        )


        st.caption(
            "Essa tabela ajuda a identificar novos cargos "
            "que precisam ser incluídos na padronização."
        )


        st.dataframe(
            cargos_outros,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# ERROS DE CARREGAMENTO
# ============================================================

if not erros_carregamento.empty:

    with st.expander(
        "Arquivos ESS com erro de carregamento"
    ):

        st.dataframe(
            erros_carregamento,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# FOOTER
# ============================================================

st.html(
    f"""
    <div
        style="
            margin-top:40px;
            border-top:1px solid {CINZA_BORDA};
            padding-top:18px;
            padding-bottom:15px;
            display:flex;
            justify-content:space-between;
            color:{CINZA_TEXTO};
            font-size:11px;
        "
    >

        <span>
            Jornada de Segurança 2026 • Operação Segura
        </span>

        <span>
            Fonte: ESS • Pilar Liderança • PMS
        </span>

    </div>
    """
)