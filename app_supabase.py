import streamlit as st
import pg8000.dbapi
import ssl
import tomllib
from pathlib import Path
from PIL import Image
from datetime import date, datetime, timedelta
import unicodedata

# Pasta onde está o app_supabase.py
PASTA_APP = Path(__file__).resolve().parent

# Arquivo com os dados do Supabase
CAMINHO_SECRETS = PASTA_APP / ".streamlit" / "secrets.toml"

# Lê o secrets.toml diretamente
with open(CAMINHO_SECRETS, "rb") as arquivo:
    dados_secrets = tomllib.load(arquivo)

postgres = dados_secrets["postgres"]
print("USUARIO LIDO:", postgres["user"])

# Conexão segura com o Supabase
CAMINHO_CERTIFICADO = PASTA_APP / "prod-ca-2021.crt"

ssl_context = ssl.create_default_context(
    cafile=str(CAMINHO_CERTIFICADO)
)

ssl_context.verify_flags &= ~ssl.VERIFY_X509_STRICT
def criar_conexao():
    return pg8000.dbapi.connect(
        host=postgres["host"],
        port=int(postgres["port"]),
        database=postgres["dbname"],
        user=postgres["user"],
        password=postgres["password"],
        ssl_context=ssl_context
    )

if "conexao_banco" not in st.session_state:
    st.session_state.conexao_banco = criar_conexao()
conn = st.session_state.conexao_banco

try:
    cursor_teste = conn.cursor()
    cursor_teste.execute("SELECT 1")
    cursor_teste.fetchone()
    cursor_teste.close()

except Exception:
    st.session_state.conexao_banco = criar_conexao()
conn = st.session_state.conexao_banco

class CursorCompat:

    def __init__(self, conexao):
        self.conexao = conexao
        self.cursor = None

    def execute(self, sql, params=None):
        global conn

        sql = sql.replace("?", "%s")

        try:
            # Cria um cursor novo para cada consulta
            self.cursor = self.conexao.cursor()

            if params is None:
                return self.cursor.execute(sql)

            return self.cursor.execute(
                sql,
                params
            )

        except pg8000.dbapi.InterfaceError:
            # Reconecta caso a conexão tenha fechado
            try:
                self.conexao.close()
            except Exception:
                pass

            nova_conexao = criar_conexao()

            st.session_state.conexao_banco = (
                nova_conexao
            )

            conn = nova_conexao
            self.conexao = nova_conexao

            self.cursor = (
                nova_conexao.cursor()
            )

            if params is None:
                return self.cursor.execute(sql)

            return self.cursor.execute(
                sql,
                params
            )

        except Exception:
            try:
                self.conexao.rollback()
            except Exception:
                try:
                    self.conexao.close()
                except Exception:
                    pass

                nova_conexao = criar_conexao()

                st.session_state.conexao_banco = (
                    nova_conexao
                )

                conn = nova_conexao
                self.conexao = nova_conexao

            raise

    def fetchone(self):
        if self.cursor is None:
            return None

        return self.cursor.fetchone()

    def fetchall(self):
        if self.cursor is None:
            return []

        return self.cursor.fetchall()


cursor = CursorCompat(conn)
st.set_page_config(
    page_title="Studio de Pilates",
    page_icon="🧘",
    layout="wide"
)
# =========================
# LOGIN
# =========================

if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.title("Acesso ao sistema")

    usuario_digitado = st.text_input("Usuário")
    senha_digitada = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if (
            usuario_digitado == st.secrets["auth"]["usuario"]
            and senha_digitada == st.secrets["auth"]["senha"]
        ):
            st.session_state.logado = True
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")

    st.stop()
st.markdown("""
<style>

/* =========================
   MENU LATERAL
   ========================= */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #163A5F 0%,
        #1C4A70 55%,
        #245B87 100%
    );
}
/* =========================
   MENU LATERAL
   ========================= */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #163A5F 0%,
        #1C4A70 55%,
        #245B87 100%
    );
}

/* Textos do menu */
[data-testid="stSidebar"] * {
    color: white;
}

/* Espaço interno */
[data-testid="stSidebar"] .block-container {
    padding-top: 22px;
    padding-left: 15px;
    padding-right: 15px;
}

/* Espaço entre opções */
[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 5px;
}

/* Cada opção do menu */
[data-testid="stSidebar"] [role="radiogroup"] label {
    min-height: 46px;
    display: flex;
    align-items: center;
    font-size: 16px !important;
    font-weight: 500 !important;
    padding: 10px 14px !important;
    margin-bottom: 3px !important;
    border-radius: 12px !important;
    transition: 0.2s ease;
}

/* Texto das opções */
[data-testid="stSidebar"] [role="radiogroup"] label p {
    color: rgba(255,255,255,0.88) !important;
    font-size: 16px !important;
}

/* Passar o mouse */
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.10);
}

/* Item selecionado */
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: rgba(255,255,255,0.18);
    border-left: 4px solid #56D6E0;
}

/* Texto selecionado */
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p {
    color: white !important;
    font-weight: 700 !important;
}

/* Tenta remover a bolinha do radio */
[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
    display: none !important;
}

/* Remove espaço da bolinha */
[data-testid="stSidebar"] div[role="radiogroup"] label {
    gap: 0 !important;
}
/* ESCONDE O INDICADOR VISUAL DO RADIO */
[data-testid="stSidebar"] [role="radiogroup"] label div[data-baseweb="radio"] {
    display: none !important;
}

/* REMOVE QUALQUER ESPAÇO RESERVADO PARA O RADIO */
[data-testid="stSidebar"] [role="radiogroup"] label > div {
    margin-left: 0 !important;
}

/* ALINHA O TEXTO À ESQUERDA */
[data-testid="stSidebar"] [role="radiogroup"] label {
    padding-left: 16px !important;
    gap: 0 !important;
}
/* BOTÕES DO MENU LATERAL */
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    min-height: 46px;
    background: transparent;
    color: white;
    border: none;
    border-radius: 12px;
    text-align: left;
    justify-content: flex-start;
    padding: 10px 16px;
    font-size: 16px;
    font-weight: 500;
    box-shadow: none;
}

/* Hover dos botões do menu */
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.12);
    color: white;
    border: none;
}

/* Remove borda ao clicar */
[data-testid="stSidebar"] .stButton > button:focus {
    color: white;
    border: none;
    box-shadow: none;
}

/* =========================
   TÍTULOS
   ========================= */

h1 {
    color: #163A5F;
    font-weight: 700;
}

h2, h3 {
    color: #245B87;
}

/* =========================
   BOTÕES GERAIS
   ========================= */

.stButton > button {
    background-color: #2E6F9E;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 9px 18px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #163A5F;
    color: white;
}

/* =========================
   BOTÕES DO MENU LATERAL
   ========================= */

[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    min-height: 46px;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    text-align: left !important;
    justify-content: flex-start !important;
    padding: 10px 16px !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    box-shadow: none !important;
    margin-bottom: 3px;
}

/* BOTÕES NORMAIS DO MENU */
[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
    background: transparent !important;
}

/* HOVER DOS BOTÕES NORMAIS */
[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
    background: rgba(255,255,255,0.10) !important;
}

/* PÁGINA ATUAL */
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: rgba(255,255,255,0.18) !important;
    border-left: 4px solid #56D6E0 !important;
    padding-left: 12px !important;
    font-weight: 700 !important;
}

/* HOVER DA PÁGINA ATUAL */
[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
    background: rgba(255,255,255,0.22) !important;
}

/* REMOVE BORDA AO CLICAR */
[data-testid="stSidebar"] .stButton > button:focus {
    color: white !important;
    box-shadow: none !important;
}

/* CAMPOS */
input {
    border-radius: 10px !important;
}

/* SELECTBOX */
div[data-baseweb="select"] > div {
    border-radius: 10px;
}

/* CARTÕES */
[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #D7E6F0;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.06);
}

/* DIVISORES */
hr {
    border-color: #D7E6F0;
}

/* ALERTAS - ESTILO POP-UP CENTRAL */
@keyframes popupEntrada {
    from {
        opacity: 0;
        transform: scale(0.96) translateY(-6px);
    }
    to {
        opacity: 1;
        transform: scale(1) translateY(0);
    }
}

[data-testid="stAlert"] {
    max-width: 720px;
    margin: 20px auto !important;
    padding: 18px 22px !important;
    border-radius: 16px !important;
    border-width: 2px !important;
    box-shadow: 0 10px 28px rgba(0,0,0,0.16);
    animation: popupEntrada 0.20s ease-out;
}

[data-testid="stAlert"] p {
    font-size: 18px !important;
    font-weight: 700 !important;
    text-align: center !important;
    line-height: 1.45 !important;
}

[data-testid="stAlert"] svg {
    width: 24px !important;
    height: 24px !important;
}

/* ESPAÇAMENTO DA PÁGINA */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

</style>
""", unsafe_allow_html=True)
logo = Image.open("logo_pilates.png")

col1, col2, col3 = st.sidebar.columns([1, 2, 1])

with col2:
    st.image(
        logo,
        width=150
    )

st.sidebar.markdown(
    """
    <div style="
        text-align: center;
        color: white;
        font-size: 21px;
        font-weight: 700;
        margin-top: -5px;
    ">
        Studio de Pilates
    </div>

    <div style="
        text-align: center;
        color: rgba(255,255,255,0.65);
        font-size: 12px;
        margin-bottom: 22px;
    ">
        Sistema de Gestão
    </div>
    """,
    unsafe_allow_html=True
)
def obter_dias_semana(texto_dias):
    if not texto_dias:
        return []

    texto = unicodedata.normalize(
        "NFKD", texto_dias
    ).encode(
        "ASCII", "ignore"
    ).decode().lower()

    mapa = {
        "segunda": 0,
        "seg": 0,
        "terca": 1,
        "ter": 1,
        "quarta": 2,
        "qua": 2,
        "quinta": 3,
        "qui": 3,
        "sexta": 4,
        "sex": 4,
        "sabado": 5,
        "sab": 5,
        "domingo": 6,
        "dom": 6
    }

    dias_encontrados = set()

    for nome, numero in mapa.items():
        if nome in texto:
            dias_encontrados.add(numero)

    return sorted(dias_encontrados)


def calcular_data_renovacao(
    data_inicio,
    texto_dias,
    quantidade_aulas,
    dias_sem_aula
):
    dias_turma = obter_dias_semana(texto_dias)

    if not dias_turma:
        return None

    data_atual = data_inicio
    aulas_contadas = 0

    while True:

        if (
            data_atual.weekday() in dias_turma
            and data_atual not in dias_sem_aula
        ):
            aulas_contadas += 1

            if aulas_contadas > quantidade_aulas:
                return data_atual

        data_atual += timedelta(days=1)

def calcular_fim_ciclo(
    data_inicio,
    texto_dias,
    quantidade_aulas,
    dias_sem_aula
):
    dias_turma = obter_dias_semana(texto_dias)

    if not dias_turma:
        return None

    data_atual = data_inicio
    aulas_contadas = 0

    while True:
        if (
            data_atual.weekday() in dias_turma
            and data_atual not in dias_sem_aula
        ):
            aulas_contadas += 1

            if aulas_contadas == quantidade_aulas:
                return data_atual

        data_atual += timedelta(days=1)
# =========================
# MENU LATERAL COM BOTÕES
# =========================

if "menu_ativo" not in st.session_state:
    st.session_state.menu_ativo = "🏠 Início"

opcoes_menu = [
    "🏠 Início",
    "👥 Alunos",
    "📅 Turmas",
    "✅ Presenças",
    "💰 Financeiro",
    "🩺 Fisioterapia",
    "💸 Despesas",
    "🔄 Reposições",
    "👨‍🏫 Instrutores",
    "📆 Dias sem aula",
    "📊 Relatórios"
]

def trocar_menu(opcao):
    st.session_state.menu_ativo = opcao


for opcao in opcoes_menu:

    if opcao == st.session_state.menu_ativo:
        tipo_botao = "primary"
    else:
        tipo_botao = "secondary"

    st.sidebar.button(
        opcao,
        key=f"menu_{opcao}",
        use_container_width=True,
        type=tipo_botao,
        on_click=trocar_menu,
        args=(opcao,)
    )        
st.sidebar.divider()

menu = st.session_state.menu_ativo
if menu == "🏠 Início":
    st.title("Início")

    from datetime import date
    import calendar

    hoje = date.today()
    ano_atual = hoje.year
    mes_atual = hoje.month

    ultimo_dia = calendar.monthrange(
        ano_atual,
        mes_atual
    )[1]

    data_inicio_mes = (
        f"{ano_atual}-"
        f"{mes_atual:02d}-01"
    )

    data_fim_mes = (
        f"{ano_atual}-"
        f"{mes_atual:02d}-"
        f"{ultimo_dia:02d}"
    )

    meses = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro"
    ]

    st.caption(
        f"Resumo de {meses[mes_atual - 1]} de {ano_atual}"
    )

    # =========================
    # ALUNOS E VAGAS
    # =========================

    cursor.execute("""
        SELECT COUNT(*)
        FROM alunos
    """)

    total_alunos = cursor.fetchone()[0] or 0

    cursor.execute("""
        SELECT SUM(limite_alunos)
        FROM turmas
    """)

    total_vagas = cursor.fetchone()[0] or 0

    vagas_disponiveis = (
        total_vagas - total_alunos
    )

    if vagas_disponiveis < 0:
        vagas_disponiveis = 0

    cursor.execute("""
        SELECT COUNT(*)
        FROM turmas
    """)

    total_turmas = cursor.fetchone()[0] or 0
    # =========================
    # ALERTAS DE RENOVAÇÃO
    # =========================

    cursor.execute("""
        SELECT DISTINCT ON (alunos.id)
            alunos.id,
            alunos.nome,
            turmas.dias,
            financeiro.data_pagamento,
            financeiro.plano
        FROM alunos
        INNER JOIN financeiro
            ON financeiro.aluno_id = alunos.id
        LEFT JOIN turmas
            ON alunos.turma_id = turmas.id
        WHERE financeiro.status = 'Pago'
          AND financeiro.data_pagamento IS NOT NULL
          AND financeiro.plano IN ('8 aulas', '24 aulas')
        ORDER BY
            alunos.id,
            financeiro.data_pagamento DESC,
            financeiro.id DESC
    """)

    dados_renovacoes = cursor.fetchall()

    # Dias em que o estúdio estará fechado
    cursor.execute("""
        SELECT data
        FROM dias_sem_aula
    """)

    dias_sem_aula_banco = cursor.fetchall()

    dias_sem_aula_inicio = set()

    for dia in dias_sem_aula_banco:
        dias_sem_aula_inicio.add(
            datetime.strptime(
                dia[0],
                "%Y-%m-%d"
            ).date()
        )

    renovacoes_atrasadas = []
    renovacoes_hoje = []
    renovacoes_proximas = []

    for registro in dados_renovacoes:
        aluno_nome = registro[1]
        dias_turma = registro[2]
        data_pagamento_aluno = registro[3]
        plano_aluno = registro[4]

        if not dias_turma:
            continue

        data_inicio_ciclo = datetime.strptime(
            data_pagamento_aluno,
            "%Y-%m-%d"
        ).date()

        if plano_aluno == "8 aulas":
            quantidade_aulas = 8
        else:
            quantidade_aulas = 24

        data_prevista = calcular_data_renovacao(
            data_inicio_ciclo,
            dias_turma,
            quantidade_aulas,
            dias_sem_aula_inicio
        )

        if data_prevista:
            diferenca = (data_prevista - hoje).days

            if diferenca < 0:
                renovacoes_atrasadas.append(
                    (
                        aluno_nome,
                        data_prevista,
                        abs(diferenca)
                    )
                )

            elif diferenca == 0:
                renovacoes_hoje.append(
                    (
                        aluno_nome,
                        data_prevista
                    )
                )

            elif diferenca <= 7:
                renovacoes_proximas.append(
                    (
                        aluno_nome,
                        data_prevista,
                        diferenca
                    )
                )

    st.divider()
    st.subheader("🔔 Renovações")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🔴 Atrasadas",
        len(renovacoes_atrasadas)
    )

    col2.metric(
        "📅 Hoje",
        len(renovacoes_hoje)
    )

    col3.metric(
        "⚠️ Próximos 7 dias",
        len(renovacoes_proximas)
    )

    total_alertas = (
        len(renovacoes_atrasadas)
        + len(renovacoes_hoje)
        + len(renovacoes_proximas)
    )

    if total_alertas == 0:
        st.success(
            "Nenhuma renovação prevista para os próximos 7 dias."
        )
    if total_alertas == 0:
        st.success(
            "Nenhuma renovação prevista para os próximos 7 dias."
        )

    for nome, data_renovacao, dias_atraso in renovacoes_atrasadas:
        st.error(
            f"🔴 {nome} — renovação prevista para "
            f"{data_renovacao.strftime('%d/%m/%Y')} "
            f"({dias_atraso} dia(s) em atraso)"
        )

    for nome, data_renovacao in renovacoes_hoje:
        st.error(
            f"🔴 {nome} — RENOVAÇÃO HOJE "
            f"({data_renovacao.strftime('%d/%m/%Y')})"
        )

    for nome, data_renovacao, dias_restantes in renovacoes_proximas:
        st.warning(
            f"⚠️ {nome} — renovação em "
            f"{dias_restantes} dia(s): "
            f"{data_renovacao.strftime('%d/%m/%Y')}"
        )
    # =========================
    # PILATES
    # =========================

    cursor.execute("""
        SELECT
            SUM(valor_liquido)
        FROM financeiro
        WHERE status = 'Pago'
        AND data_pagamento BETWEEN ? AND ?
    """, (
        data_inicio_mes,
        data_fim_mes
    ))

    receita_pilates = (
        cursor.fetchone()[0] or 0
    )

    cursor.execute("""
        SELECT
            SUM(valor)
        FROM financeiro
        WHERE status = 'Pendente'
        AND data_pagamento BETWEEN ? AND ?
    """, (
        data_inicio_mes,
        data_fim_mes
    ))

    pagamentos_pendentes = (
        cursor.fetchone()[0] or 0
    )

    # =========================
    # FISIOTERAPIA
    # =========================

    cursor.execute("""
        SELECT
            COUNT(*),
            SUM(valor_liquido)
        FROM fisioterapia
        WHERE data BETWEEN ? AND ?
    """, (
        data_inicio_mes,
        data_fim_mes
    ))

    resumo_fisio = cursor.fetchone()

    atendimentos_fisio = (
        resumo_fisio[0] or 0
    )

    receita_fisio = (
        resumo_fisio[1] or 0
    )

    # =========================
    # DESPESAS
    # =========================

    cursor.execute("""
        SELECT
            SUM(valor)
        FROM despesas
        WHERE data BETWEEN ? AND ?
    """, (
        data_inicio_mes,
        data_fim_mes
    ))

    despesas_mes = (
        cursor.fetchone()[0] or 0
    )

    # =========================
    # RESULTADO
    # =========================

    receita_total = (
        receita_pilates
        + receita_fisio
    )

    resultado_mes = (
        receita_total
        - despesas_mes
    )

    # =========================
    # PRIMEIRA LINHA
    # =========================

    st.subheader("Visão geral")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👥 Alunos",
        total_alunos
    )

    col2.metric(
        "📅 Turmas",
        total_turmas
    )

    col3.metric(
        "🪑 Vagas disponíveis",
        vagas_disponiveis
    )

    col4.metric(
        "🩺 Atendimentos Fisio",
        atendimentos_fisio
    )   
    # =========================
    # TURMAS COM VAGA
    # =========================
    st.subheader("🪑 Turmas com vaga")

    cursor.execute("""
        SELECT
            t.dias,
            t.horario,
            t.limite_alunos,
            COUNT(a.id) AS total_alunos
        FROM turmas t
        LEFT JOIN alunos a
            ON a.turma_id = t.id
        GROUP BY
            t.id,
            t.dias,
            t.horario,
            t.limite_alunos
        HAVING COUNT(a.id) < t.limite_alunos
        ORDER BY
            t.dias,
            t.horario
    """)

    turmas_com_vaga = cursor.fetchall()

    if len(turmas_com_vaga) == 0:
        st.info(
            "No momento não há turmas com vagas disponíveis."
        )

    else:
        for turma in turmas_com_vaga:
            dias = turma[0]
            horario = turma[1]
            limite = turma[2] or 0
            ocupadas = turma[3] or 0

            vagas = limite - ocupadas

            st.write(
                f"🟢 **{dias} - {horario}** "
                f"— {vagas} vaga(s)"
            )

    # =========================
    # RESUMO DAS TURMAS
    # =========================

    st.subheader("Ocupação das turmas")

    cursor.execute("""
        SELECT
            t.id,
            t.dias,
            t.horario,
            t.limite_alunos,
            COUNT(a.id) as total_alunos
        FROM turmas t
        LEFT JOIN alunos a
            ON a.turma_id = t.id
        GROUP BY
            t.id,
            t.dias,
            t.horario,
            t.limite_alunos
        ORDER BY
            t.dias,
            t.horario
    """)

    ocupacao_turmas = cursor.fetchall()

    if len(ocupacao_turmas) == 0:
        st.info(
            "Nenhuma turma cadastrada."
        )

    else:
        colunas = st.columns(3)

        for indice, turma in enumerate(ocupacao_turmas):
            turma_id = turma[0]
            dias = turma[1]
            horario = turma[2]
            limite = turma[3] or 0
            total_alunos = turma[4] or 0

            vagas = limite - total_alunos

            if vagas < 0:
                vagas = 0

            if limite > 0:
                percentual = total_alunos / limite

            if percentual > 1:
                percentual = 1

            if percentual < 0:
                percentual = 0

            else:
                percentual = 0            
            if vagas == 0:
                status = "🔴 Lotada"
            elif vagas == 1:
                status = "🟡 Última vaga"
            else:
                status = "🟢 Disponível"

            coluna = colunas[indice % 3]

            with coluna:
                with st.container(border=True):
                    st.markdown(
                        f"**{dias}**"
                    )

                    st.markdown(
                        f"🕐 {horario}"
                    )

                    st.progress(percentual)

                    st.caption(
                        f"{total_alunos} de {limite} alunos"
                    )

                    col_a, col_b = st.columns(2)

                    col_a.metric(
                        "Alunos",
                        total_alunos
                    )

                    col_b.metric(
                        "Vagas",
                        vagas
                    )

                    st.caption(status)

            if (indice + 1) % 3 == 0:
                colunas = st.columns(3)

elif menu == "👥 Alunos":
    st.title("Alunos")
    aba_cadastro, aba_lista, aba_edicao, aba_historico_aluno = st.tabs(
        [
            "➕ Cadastrar",
            "👥 Alunos cadastrados",
            "✏️ Editar / Excluir",
            "📚 Histórico do aluno"
        ]
    )

    # =========================
    # ABA 1 - CADASTRAR
    # =========================
    with aba_cadastro:
        st.subheader("Cadastrar aluno")

        cursor.execute("""
            SELECT
                turmas.id,
                turmas.dias,
                turmas.horario,
                turmas.limite_alunos,
                COUNT(alunos.id) AS ocupados
            FROM turmas
            LEFT JOIN alunos
                ON alunos.turma_id = turmas.id
            GROUP BY
                turmas.id,
                turmas.dias,
                turmas.horario,
                turmas.limite_alunos
            HAVING COUNT(alunos.id) < turmas.limite_alunos
            ORDER BY
                turmas.dias,
                turmas.horario
        """)

        turmas_cadastradas = cursor.fetchall()

        if len(turmas_cadastradas) == 0:
            st.warning(
                "Não há turmas com vagas disponíveis."
            )

        else:
            opcoes_turmas = {
                f"{t[1]} - {t[2]} | {t[3] - t[4]} vaga(s)": t[0]
                for t in turmas_cadastradas
            }

            with st.form(
                "form_cadastro_aluno",
                clear_on_submit=True
            ):
                nome = st.text_input(
                    "Nome do aluno"
                )

                telefone = st.text_input(
                    "Telefone"
                )

                cpf = st.text_input(
                    "CPF"
                )

                endereco = st.text_input(
                    "Endereço"
                )

                data_nascimento = st.text_input(
                    "Data de nascimento",
                    placeholder="DD/MM/AAAA"
                )

                tabela_preco = st.selectbox(
                    "Tabela de preço",
                    [
                        "Antigo",
                        "Novo"
                    ]
                )

                turma = st.selectbox(
                    "Turma",
                    list(opcoes_turmas.keys())
                )

                cadastrar = st.form_submit_button(
                    "Cadastrar aluno"
                )

                if cadastrar:
                    turma_id = opcoes_turmas[turma]

                    if nome.strip() == "":
                        st.warning(
                            "Digite o nome do aluno."
                        )

                    else:
                        cursor.execute("""
                            SELECT
                                t.limite_alunos,
                                COUNT(a.id)
                            FROM turmas t
                            LEFT JOIN alunos a
                                ON a.turma_id = t.id
                            WHERE t.id = ?
                            GROUP BY
                                t.id,
                                t.limite_alunos
                        """, (
                            turma_id,
                        ))

                        dados_vaga = cursor.fetchone()

                        limite_turma = (
                            dados_vaga[0] or 0
                        )

                        alunos_na_turma = (
                            dados_vaga[1] or 0
                        )

                        if alunos_na_turma >= limite_turma:
                            st.markdown(
                                """
                                <div style="
                                    position: fixed;
                                    top: 50%;
                                    left: 50%;
                                    transform: translate(-50%, -50%);
                                    z-index: 999999;
                                    width: 520px;
                                    max-width: 80%;
                                    background: white;
                                    border-radius: 18px;
                                    padding: 18px;
                                    box-shadow: 0 12px 40px rgba(0,0,0,0.28);
                                ">
                                    <div style="
                                        background-color: #fde8e8;
                                        color: #c62828;
                                        border-radius: 12px;
                                        padding: 22px;
                                        text-align: center;
                                        font-size: 20px;
                                        font-weight: 700;
                                    ">
                                        ❌ Esta turma está lotada.<br>
                                        Escolha outra turma.
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        else:
                            cursor.execute("""
                                INSERT INTO alunos
                                (
                                    nome,
                                    telefone,
                                    cpf,
                                    endereco,
                                    data_nascimento,
                                    turma,
                                    turma_id,
                                    tabela_preco
                                )
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                nome,
                                telefone,
                                cpf,
                                endereco,
                                data_nascimento,
                                turma,
                                turma_id,
                                tabela_preco
                            ))

                            conn.commit()

                            st.success(
                                f"Aluno {nome} cadastrado com sucesso!"
                            )
    # =========================
    # ABA 2 - LISTA DE ALUNOS
    # =========================
    with aba_lista:
        st.subheader("Alunos cadastrados")

        cursor.execute("""
            SELECT
                id,
                nome,
                telefone,
                cpf,
                endereco,
                data_nascimento,
                turma,
                tabela_preco
            FROM alunos
            ORDER BY nome
        """)

        alunos = cursor.fetchall()

        if len(alunos) == 0:
            st.info(
                "Nenhum aluno cadastrado ainda."
            )

        else:
            colunas = st.columns(
                [1, 2, 2, 2, 3, 2, 3, 2]
            )

            titulos = [
                "ID",
                "Nome",
                "Telefone",
                "CPF",
                "Endereço",
                "Nascimento",
                "Turma",
                "Tabela"
            ]

            for coluna, titulo in zip(
                colunas,
                titulos
            ):
                coluna.markdown(
                    f"**{titulo}**"
                )

            for aluno in alunos:
                colunas = st.columns(
                    [1, 2, 2, 2, 3, 2, 3, 2]
                )

                colunas[0].write(aluno[0])
                colunas[1].write(aluno[1])
                colunas[2].write(aluno[2])
                colunas[3].write(aluno[3])
                colunas[4].write(aluno[4])
                colunas[5].write(aluno[5])
                colunas[6].write(aluno[6])
                colunas[7].write(
                    aluno[7] or "Antigo"
                )

    # =========================
    # ABA 3 - EDITAR / EXCLUIR
    # =========================
    with aba_edicao:
        st.subheader(
            "Editar ou excluir aluno"
        )

        cursor.execute("""
            SELECT id, nome
            FROM alunos
            ORDER BY nome
        """)

        alunos_edicao = cursor.fetchall()

        if len(alunos_edicao) == 0:
            st.info(
                "Nenhum aluno disponível para edição."
            )

        else:
            opcoes_edicao = {
                f"{aluno[1]} - ID {aluno[0]}": aluno[0]
                for aluno in alunos_edicao
            }

            lista_alunos_edicao = (
                [""]
                + list(opcoes_edicao.keys())
            )

            aluno_selecionado = st.selectbox(
                "Selecione o aluno",
                lista_alunos_edicao,
                index=0,
                key="aluno_edicao"
            )

            if aluno_selecionado == "":
                st.info(
                    "Digite ou selecione um aluno para editar."
                )

            else:
                aluno_id_edicao = opcoes_edicao[
                    aluno_selecionado
                ]

                cursor.execute("""
                    SELECT
                        nome,
                        telefone,
                        cpf,
                        endereco,
                        data_nascimento,
                        turma,
                        turma_id,
                        tabela_preco
                    FROM alunos
                    WHERE id = ?
                """, (
                    aluno_id_edicao,
                ))

                dados_aluno = cursor.fetchone()

                novo_nome = st.text_input(
                    "Nome",
                    value=dados_aluno[0] or "",
                    key=f"editar_nome_{aluno_id_edicao}"
                )

                novo_telefone = st.text_input(
                    "Telefone",
                    value=dados_aluno[1] or "",
                    key=f"editar_telefone_{aluno_id_edicao}"
                )

                novo_cpf = st.text_input(
                    "CPF",
                    value=dados_aluno[2] or "",
                    key=f"editar_cpf_{aluno_id_edicao}"
                )

                novo_endereco = st.text_input(
                    "Endereço",
                    value=dados_aluno[3] or "",
                    key=f"editar_endereco_{aluno_id_edicao}"
                )

                nova_data_nascimento = st.text_input(
                    "Data de nascimento",
                    value=dados_aluno[4] or "",
                    placeholder="DD/MM/AAAA",
                    key=f"editar_nascimento_{aluno_id_edicao}"
                )

                opcoes_tabela = [
                    "Antigo",
                    "Novo"
                ]

                tabela_atual = dados_aluno[7]

                if tabela_atual in opcoes_tabela:
                    indice_tabela = (
                        opcoes_tabela.index(
                            tabela_atual
                        )
                    )
                else:
                    indice_tabela = 0

                nova_tabela_preco = st.selectbox(
                    "Tabela de preço",
                    opcoes_tabela,
                    index=indice_tabela,
                    key=(
                        f"editar_tabela_preco_"
                        f"{aluno_id_edicao}"
                    )
                )

                cursor.execute("""
                    SELECT id, dias, horario
                    FROM turmas
                    ORDER BY dias, horario
                """)

                turmas_edicao = cursor.fetchall()

                if len(turmas_edicao) == 0:
                    st.warning(
                        "Nenhuma turma cadastrada."
                    )

                else:
                    opcoes_turmas_edicao = {
                        f"{t[1]} - {t[2]}": t[0]
                        for t in turmas_edicao
                    }

                    nomes_turmas = list(
                        opcoes_turmas_edicao.keys()
                    )

                    turma_atual = dados_aluno[5]

                    if turma_atual in nomes_turmas:
                        indice_turma = (
                            nomes_turmas.index(
                                turma_atual
                            )
                        )
                    else:
                        indice_turma = 0

                    nova_turma = st.selectbox(
                        "Turma",
                        nomes_turmas,
                        index=indice_turma,
                        key=(
                            f"editar_turma_"
                            f"{aluno_id_edicao}"
                        )
                    )

                    nova_turma_id = (
                        opcoes_turmas_edicao[
                            nova_turma
                        ]
                    )

                    col_editar, col_excluir = (
                        st.columns(2)
                    )

                    if col_editar.button(
                        "Salvar alterações",
                        key=(
                            f"salvar_edicao_aluno_"
                            f"{aluno_id_edicao}"
                        )
                    ):

                        turma_id_atual = (
                            dados_aluno[6]
                        )

                        # =========================
                        # SE ESTIVER MUDANDO DE TURMA
                        # =========================
                        if (
                            nova_turma_id
                            != turma_id_atual
                        ):
                            cursor.execute("""
                                SELECT
                                    t.limite_alunos,
                                    COUNT(a.id)
                                FROM turmas t
                                LEFT JOIN alunos a
                                    ON a.turma_id = t.id
                                WHERE t.id = ?
                                GROUP BY
                                    t.id,
                                    t.limite_alunos
                            """, (
                                nova_turma_id,
                            ))

                            dados_vaga = (
                                cursor.fetchone()
                            )

                            if dados_vaga:
                                limite_turma = (
                                    dados_vaga[0]
                                    or 0
                                )

                                alunos_na_turma = (
                                    dados_vaga[1]
                                    or 0
                                )

                            else:
                                limite_turma = 0
                                alunos_na_turma = 0

                            if (
                                alunos_na_turma
                                >= limite_turma
                            ):
                                st.markdown(
                                    """
                                    <div style="
                                        position: fixed;
                                        top: 50%;
                                        left: 50%;
                                        transform: translate(-50%, -50%);
                                        z-index: 999999;
                                        width: 520px;
                                        max-width: 80%;
                                        background: white;
                                        border-radius: 18px;
                                        padding: 18px;
                                        box-shadow: 0 12px 40px rgba(0,0,0,0.28);
                                    ">
                                        <div style="
                                            background-color: #fde8e8;
                                            color: #c62828;
                                            border-radius: 12px;
                                            padding: 22px;
                                            text-align: center;
                                            font-size: 20px;
                                            font-weight: 700;
                                        ">
                                            ❌ Esta turma está lotada.<br>
                                            Escolha outra turma.
                                        </div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )

                            else:
                                cursor.execute("""
                                    UPDATE alunos
                                    SET
                                        nome = ?,
                                        telefone = ?,
                                        cpf = ?,
                                        endereco = ?,
                                        data_nascimento = ?,
                                        turma = ?,
                                        turma_id = ?,
                                        tabela_preco = ?
                                    WHERE id = ?
                                """, (
                                    novo_nome,
                                    novo_telefone,
                                    novo_cpf,
                                    novo_endereco,
                                    nova_data_nascimento,
                                    nova_turma,
                                    nova_turma_id,
                                    nova_tabela_preco,
                                    aluno_id_edicao
                                ))

                                conn.commit()

                                st.success(
                                    "Aluno atualizado com sucesso!"
                                )
                        # =========================
                        # CONTINUA NA MESMA TURMA
                        # =========================
                        else:
                            cursor.execute("""
                                UPDATE alunos
                                SET
                                    nome = ?,
                                    telefone = ?,
                                    cpf = ?,
                                    endereco = ?,
                                    data_nascimento = ?,
                                    turma = ?,
                                    turma_id = ?,
                                    tabela_preco = ?
                                WHERE id = ?
                            """, (
                                novo_nome,
                                novo_telefone,
                                novo_cpf,
                                novo_endereco,
                                nova_data_nascimento,
                                nova_turma,
                                nova_turma_id,
                                nova_tabela_preco,
                                aluno_id_edicao
                            ))

                            conn.commit()

                            st.success(
                                "Aluno atualizado com sucesso!"
                            )

                    if col_excluir.button(
                        "Excluir aluno",
                        key=(
                            f"excluir_aluno_"
                            f"{aluno_id_edicao}"
                        )
                    ):
                        cursor.execute("""
                            DELETE FROM alunos
                            WHERE id = ?
                        """, (
                            aluno_id_edicao,
                        ))

                        conn.commit()

                        st.success(
                            "Aluno excluído com sucesso!"
                        )

                        st.rerun()
    # =========================
    # ABA 4 - HISTÓRICO DO ALUNO
    # =========================
    with aba_historico_aluno:
        st.subheader("Histórico do aluno")

        cursor.execute("""
            SELECT id, nome
            FROM alunos
            ORDER BY nome
        """)

        alunos_historico = cursor.fetchall()

        if len(alunos_historico) == 0:
            st.info("Nenhum aluno cadastrado.")

        else:
            opcoes_historico = {
                f"{aluno[1]} - ID {aluno[0]}": aluno[0]
                for aluno in alunos_historico
            }

            lista_historico = (
                [""]
                + list(opcoes_historico.keys())
            )

            aluno_historico_selecionado = st.selectbox(
                "Selecione o aluno",
                lista_historico,
                index=0,
                key="aluno_historico_financeiro"
            )

            if aluno_historico_selecionado == "":
                st.info(
                    "Selecione um aluno para consultar o histórico."
                )

            else:
                aluno_id_historico = opcoes_historico[
                    aluno_historico_selecionado
                ]

                # =========================
                # DADOS DA TURMA ATUAL
                # =========================
                cursor.execute("""
                    SELECT
                        turmas.dias,
                        turmas.horario
                    FROM alunos
                    LEFT JOIN turmas
                        ON alunos.turma_id = turmas.id
                    WHERE alunos.id = ?
                """, (
                    aluno_id_historico,
                ))

                turma_historico = cursor.fetchone()

                if turma_historico:
                    dias_turma_historico = turma_historico[0]
                    horario_turma_historico = turma_historico[1]
                else:
                    dias_turma_historico = None
                    horario_turma_historico = None

                # =========================
                # DIAS SEM AULA
                # =========================
                cursor.execute("""
                    SELECT data
                    FROM dias_sem_aula
                """)

                dias_sem_aula_banco = cursor.fetchall()

                dias_sem_aula_historico = set()

                for dia in dias_sem_aula_banco:
                    dias_sem_aula_historico.add(
                        datetime.strptime(
                            dia[0],
                            "%Y-%m-%d"
                        ).date()
                    )

                # =========================
                # PAGAMENTOS / CICLOS
                # =========================
                cursor.execute("""
                    SELECT
                        id,
                        valor,
                        data_pagamento,
                        data_inicio_ciclo,
                        forma_pagamento,
                        status,
                        plano
                    FROM financeiro
                    WHERE aluno_id = ?
                    ORDER BY
                        COALESCE(
                            data_inicio_ciclo,
                            data_pagamento
                        ) DESC,
                        id DESC
                """, (
                    aluno_id_historico,
                ))

                pagamentos_aluno = cursor.fetchall()

                if len(pagamentos_aluno) == 0:
                    st.warning(
                        "Este aluno ainda não possui ciclos registrados."
                    )

                else:
                    # =========================
                    # CICLO ATUAL
                    # =========================
                    ultimo_pagamento = pagamentos_aluno[0]
                    
                    plano_atual = (
                        ultimo_pagamento[6]
                        or "8 aulas"
                    )

                    if "24" in str(plano_atual):
                        total_aulas_plano = 24
                    else:
                        total_aulas_plano = 8

                    data_inicio_ciclo_atual = (
                        ultimo_pagamento[3]
                        or ultimo_pagamento[2]
                    )     
                
                    cursor.execute("""
                        SELECT COUNT(*)
                        FROM presencas p
                        WHERE p.aluno_id = ?
                        AND p.data >= ?
                        AND (
                            p.status = 'Presente'

                            OR p.status = 'Reposição'

                            OR (
                                p.status = 'Falta'

                                AND NOT EXISTS (
                                    SELECT 1
                                    FROM reposicoes r
                                    WHERE r.aluno_id = p.aluno_id
                                    AND r.data_falta = p.data
                                    AND r.direito_reposicao = 'Sim'
                                    AND r.status IN (
                                        'Pendente',
                                        'Agendada',
                                        'Realizada'
                                    )
                                )
                            )
                        )
                    """, (
                        aluno_id_historico,
                        data_inicio_ciclo_atual
                    ))

                    aulas_utilizadas = (
                        cursor.fetchone()[0]
                        or 0
                    )

                    aulas_restantes = (
                        total_aulas_plano
                        - aulas_utilizadas
                    )

                    if aulas_restantes < 0:
                        aulas_restantes = 0

                    st.subheader("💳 Situação atual")

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Plano",
                        plano_atual
                    )

                    col2.metric(
                        "Aulas utilizadas",
                        aulas_utilizadas
                    )

                    col3.metric(
                        "Aulas restantes",
                        aulas_restantes
                    )                      
                    # =========================
                    # HISTÓRICO COMPLETO DE AULAS
                    # =========================
                    st.markdown(
                        "### 📚 Histórico completo de aulas"
                    )

                    cursor.execute("""
                        SELECT
                            data,
                            status
                        FROM presencas
                        WHERE aluno_id = ?
                        ORDER BY data DESC
                    """, (
                        aluno_id_historico,
                    ))

                    historico_completo = cursor.fetchall()

                    if len(historico_completo) == 0:
                        st.caption(
                            "Nenhuma aula registrada para este aluno."
                        )

                    else:
                        for registro in historico_completo:
                            data_registro = datetime.strptime(
                                str(registro[0]),
                                "%Y-%m-%d"
                            ).strftime("%d/%m/%Y")

                            status_registro = registro[1]

                            st.write(
                                f"**{data_registro}** — "
                                f"{status_registro}"
                            )                 
                    # =========================
                    # REPOSIÇÕES REALIZADAS
                    # =========================
                    cursor.execute("""
                        SELECT
                            r.data_falta,
                            r.data_reposicao,
                            t.dias,
                            t.horario
                        FROM reposicoes r
                        LEFT JOIN turmas t
                            ON r.turma_reposicao_id = t.id
                        WHERE r.aluno_id = ?
                        AND r.status = 'Realizada'
                        AND r.data_reposicao >= ?
                        ORDER BY r.data_reposicao DESC
                    """, (
                        aluno_id_historico,
                        data_inicio_ciclo_atual
                    ))

                    reposicoes_realizadas = cursor.fetchall()

                    if len(reposicoes_realizadas) > 0:
                        st.subheader(
                            "🔄 Reposições realizadas neste ciclo"
                        )

                        for reposicao in reposicoes_realizadas:

                            data_falta = reposicao[0]
                            data_reposicao = reposicao[1]
                            dias_reposicao = (
                                reposicao[2]
                                or "Turma não informada"
                            )
                            horario_reposicao = (
                                reposicao[3]
                                or ""
                            )

                            st.write(
                                f"**Falta:** {data_falta} | "
                                f"**Reposição:** {data_reposicao} | "
                                f"**Turma:** {dias_reposicao} "
                                f"{horario_reposicao}"
                            )

                    if dias_turma_historico:
                        st.write(
                            f"**Turma atual:** "
                            f"{dias_turma_historico} - "
                            f"{horario_turma_historico}"
                        )

                    st.divider()

                    # =========================
                    # TODOS OS CICLOS
                    # =========================
                    st.subheader("📚 Histórico de ciclos")

                    for numero, pagamento in enumerate(
                        pagamentos_aluno,
                        start=1
                    ):
                        valor_historico = pagamento[1]

                        data_pagamento_historico = (
                            pagamento[2]
                        )

                        inicio_ciclo_historico = (
                            pagamento[3]
                            or pagamento[2]
                        )

                        forma_historico = (
                            pagamento[4]
                            or "Não informado"
                        )

                        status_historico = (
                            pagamento[5]
                            or "Não informado"
                        )

                        plano_historico = (
                            pagamento[6]
                            or "8 aulas"
                        )

                        if "24" in str(plano_historico):
                            quantidade_aulas_historico = 24
                        else:
                            quantidade_aulas_historico = 8

                        fim_ciclo = None
                        proxima_renovacao = None

                        if (
                            inicio_ciclo_historico
                            and dias_turma_historico
                        ):
                            inicio_data = datetime.strptime(
                                inicio_ciclo_historico,
                                "%Y-%m-%d"
                            ).date()

                            fim_ciclo = calcular_fim_ciclo(
                                inicio_data,
                                dias_turma_historico,
                                quantidade_aulas_historico,
                                dias_sem_aula_historico
                            )

                            proxima_renovacao = (
                                calcular_data_renovacao(
                                    inicio_data,
                                    dias_turma_historico,
                                    quantidade_aulas_historico,
                                    dias_sem_aula_historico
                                )
                            )

                        data_pagamento_formatada = (
                            datetime.strptime(
                                data_pagamento_historico,
                                "%Y-%m-%d"
                            ).strftime("%d/%m/%Y")
                            if data_pagamento_historico
                            else "Não informada"
                        )

                        inicio_formatado = (
                            datetime.strptime(
                                inicio_ciclo_historico,
                                "%Y-%m-%d"
                            ).strftime("%d/%m/%Y")
                            if inicio_ciclo_historico
                            else "Não informado"
                        )

                        with st.container(border=True):
                            st.markdown(
                                f"### Ciclo {numero} — "
                                f"{plano_historico}"
                            )

                            st.write(
                                f"**Pagamento:** "
                                f"{data_pagamento_formatada}"
                            )

                            st.write(
                                f"**Início do ciclo:** "
                                f"{inicio_formatado}"
                            )

                            if fim_ciclo:
                                st.write(
                                    f"**Fim do ciclo:** "
                                    f"{fim_ciclo.strftime('%d/%m/%Y')}"
                                )

                            if proxima_renovacao:
                                st.write(
                                    f"**Próxima renovação:** "
                                    f"{proxima_renovacao.strftime('%d/%m/%Y')}"
                                )

                            st.write(
                                f"**Valor:** "
                                f"R$ {valor_historico:.2f}"
                            )

                            st.write(
                                f"**Forma de pagamento:** "
                                f"{forma_historico}"
                            )

                            st.write(
                                f"**Status:** "
                                f"{status_historico}"
                            )
elif menu == "📅 Turmas":
    st.title("Turmas")

    aba_cadastro, aba_lista, aba_edicao, aba_alunos_turma = st.tabs(
    [
        "➕ Cadastrar",
        "📋 Turmas cadastradas",
        "✏️ Editar / Excluir",
        "👥 Alunos da turma"
    ]
)

    # =========================
    # ABA 1 - CADASTRAR
    # =========================
    with aba_cadastro:
        st.subheader("Cadastrar turma")

        dias = st.selectbox(
            "Dias da turma",
            [
                "Segunda e Quinta",
                "Terça e Sexta",
                "Quarta e Sábado"
            ],
            key="cadastro_dias_turma"
        )

        horario = st.text_input(
            "Horário",
            placeholder="Exemplo: 06h",
            key="cadastro_horario_turma"
        )

        cursor.execute("""
            SELECT id, nome
            FROM instrutores
            ORDER BY nome
        """)

        instrutores_cadastrados = cursor.fetchall()

        if len(instrutores_cadastrados) == 0:
            st.warning(
                "Cadastre um instrutor antes de cadastrar a turma."
            )
            instrutor = None

        else:
            opcoes_instrutores = [
                instrutor[1]
                for instrutor in instrutores_cadastrados
            ]

            instrutor = st.selectbox(
                "Instrutor",
                opcoes_instrutores,
                key="cadastro_instrutor_turma"
            )

        limite_alunos = st.number_input(
            "Limite de alunos",
            min_value=1,
            max_value=10,
            value=4,
            key="cadastro_limite_turma"
        )

        if st.button(
            "Cadastrar turma",
            key="botao_cadastrar_turma"
        ):
            if instrutor is None:
                st.warning(
                    "Cadastre um instrutor primeiro."
                )

            elif horario.strip() == "":
                st.warning(
                    "Digite o horário da turma."
                )

            else:
                cursor.execute("""
                    INSERT INTO turmas
                    (
                        dias,
                        horario,
                        instrutor,
                        limite_alunos
                    )
                    VALUES (?, ?, ?, ?)
                """, (
                    dias,
                    horario,
                    instrutor,
                    limite_alunos
                ))

                conn.commit()

                st.success(
                    "Turma cadastrada com sucesso!"
                )

    # =========================
    # ABA 2 - TURMAS CADASTRADAS
    # =========================
    with aba_lista:
        st.subheader("Turmas cadastradas")

        cursor.execute("""
            SELECT
                t.id,
                t.dias,
                t.horario,
                t.instrutor,
                t.limite_alunos,
                COUNT(a.id) AS alunos_cadastrados
            FROM turmas t
            LEFT JOIN alunos a
                ON a.turma_id = t.id
            GROUP BY
                t.id,
                t.dias,
                t.horario,
                t.instrutor,
                t.limite_alunos
            ORDER BY
                t.dias,
                t.horario
        """)

        turmas = cursor.fetchall()

        if len(turmas) == 0:
            st.info(
                "Nenhuma turma cadastrada ainda."
            )

        else:
            colunas = st.columns(
                [1, 2, 1, 2, 1, 1, 1]
            )

            titulos = [
                "ID",
                "Dias",
                "Horário",
                "Instrutor",
                "Limite",
                "Alunos",
                "Vagas"
            ]

            for coluna, titulo in zip(
                colunas,
                titulos
            ):
                coluna.markdown(
                    f"**{titulo}**"
                )

            for turma in turmas:
                vagas = turma[4] - turma[5]

                colunas = st.columns(
                    [1, 2, 1, 2, 1, 1, 1]
                )

                colunas[0].write(turma[0])
                colunas[1].write(turma[1])
                colunas[2].write(turma[2])
                colunas[3].write(turma[3])
                colunas[4].write(turma[4])
                colunas[5].write(turma[5])
                colunas[6].write(vagas)

    # =========================
    # ABA 3 - EDITAR / EXCLUIR
    # =========================
    with aba_edicao:
        st.subheader("Editar ou excluir turma")

        cursor.execute("""
            SELECT
                id,
                dias,
                horario,
                instrutor,
                limite_alunos
            FROM turmas
            ORDER BY dias, horario
        """)

        turmas_edicao = cursor.fetchall()

        if len(turmas_edicao) == 0:
            st.info(
                "Nenhuma turma disponível para edição."
            )

        else:
            opcoes_turmas = {
                f"{t[1]} - {t[2]} - ID {t[0]}": t[0]
                for t in turmas_edicao
            }

            turma_selecionada = st.selectbox(
                "Selecione a turma",
                list(opcoes_turmas.keys()),
                key="turma_edicao"
            )

            turma_id_edicao = opcoes_turmas[
                turma_selecionada
            ]

            cursor.execute("""
                SELECT
                    dias,
                    horario,
                    instrutor,
                    limite_alunos
                FROM turmas
                WHERE id = ?
            """, (
                turma_id_edicao,
            ))

            dados_turma = cursor.fetchone()

            dias_opcoes = [
                "Segunda e Quinta",
                "Terça e Sexta",
                "Quarta e Sábado"
            ]

            if dados_turma[0] in dias_opcoes:
                indice_dias = dias_opcoes.index(
                    dados_turma[0]
                )
            else:
                indice_dias = 0

            novos_dias = st.selectbox(
    "Dias",
    dias_opcoes,
    index=indice_dias,
    key=f"editar_dias_turma_{turma_id_edicao}"
)

            novo_horario = st.text_input(
    "Horário",
    value=dados_turma[1] or "",
    key=f"editar_horario_turma_{turma_id_edicao}"
)

            cursor.execute("""
                SELECT nome
                FROM instrutores
                ORDER BY nome
            """)

            instrutores_edicao = cursor.fetchall()

            nomes_instrutores = [
                i[0]
                for i in instrutores_edicao
            ]

            instrutor_atual = dados_turma[2]

            if instrutor_atual in nomes_instrutores:
                indice_instrutor = nomes_instrutores.index(
                    instrutor_atual
                )
            else:
                indice_instrutor = 0

            if len(nomes_instrutores) > 0:
                novo_instrutor = st.selectbox(
    "Instrutor",
    nomes_instrutores,
    index=indice_instrutor,
    key=f"editar_instrutor_turma_{turma_id_edicao}"
)
            else:
                novo_instrutor = ""

            novo_limite = st.number_input(
    "Limite de alunos",
    min_value=1,
    max_value=10,
    value=int(
        dados_turma[3] or 4
    ),
    key=f"editar_limite_turma_{turma_id_edicao}"
)

            col_salvar, col_excluir = st.columns(2)

            if col_salvar.button(
                "Salvar alterações da turma",
                key="salvar_turma"
            ):
                cursor.execute("""
                    UPDATE turmas
                    SET
                        dias = ?,
                        horario = ?,
                        instrutor = ?,
                        limite_alunos = ?
                    WHERE id = ?
                """, (
                    novos_dias,
                    novo_horario,
                    novo_instrutor,
                    novo_limite,
                    turma_id_edicao
                ))

                novo_nome_turma = (
                    f"{novos_dias} - {novo_horario}"
                )

                cursor.execute("""
                    UPDATE alunos
                    SET turma = ?
                    WHERE turma_id = ?
                """, (
                    novo_nome_turma,
                    turma_id_edicao
                ))

                conn.commit()

                st.success(
                    "Turma atualizada com sucesso!"
                )

            if col_excluir.button(
                "Excluir turma",
                key="excluir_turma"
            ):
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM alunos
                    WHERE turma_id = ?
                """, (
                    turma_id_edicao,
                ))

                quantidade_alunos = cursor.fetchone()[0]

                if quantidade_alunos > 0:
                    st.error(
                        "Essa turma possui alunos cadastrados. "
                        "Troque os alunos de turma antes de excluir."
                    )

                else:
                    cursor.execute(
                        "DELETE FROM turmas WHERE id = ?",
                        (
                            turma_id_edicao,
                        )
                    )

                    conn.commit()

                    st.success(
                        "Turma excluída com sucesso!"
                    )
    # =========================
    # ABA 4 - ALUNOS DA TURMA
    # =========================
    with aba_alunos_turma:
        st.subheader("Alunos da turma")

        cursor.execute("""
            SELECT
                id,
                dias,
                horario,
                instrutor,
                limite_alunos
            FROM turmas
            ORDER BY dias, horario
        """)

        turmas_consulta = cursor.fetchall()

        if len(turmas_consulta) == 0:
            st.info(
                "Nenhuma turma cadastrada."
            )

        else:
            opcoes_consulta_turma = {
                f"{t[1]} - {t[2]}": t
                for t in turmas_consulta
            }

            lista_consulta_turmas = (
                [""]
                + list(opcoes_consulta_turma.keys())
            )

            turma_consulta = st.selectbox(
                "Selecione a turma",
                lista_consulta_turmas,
                index=0,
                key="consultar_alunos_turma"
            )

            if turma_consulta == "":
                st.info(
                    "Selecione uma turma para visualizar os alunos."
                )

            else:
                dados_turma_consulta = (
                    opcoes_consulta_turma[
                        turma_consulta
                    ]
                )

                turma_id_consulta = (
                    dados_turma_consulta[0]
                )

                instrutor_consulta = (
                    dados_turma_consulta[3]
                    or "Não informado"
                )

                limite_consulta = int(
                    dados_turma_consulta[4] or 4
                )

                cursor.execute("""
                    SELECT
                        id,
                        nome,
                        telefone,
                        tabela_preco
                    FROM alunos
                    WHERE turma_id = ?
                    ORDER BY nome
                """, (
                    turma_id_consulta,
                ))

                alunos_da_turma = cursor.fetchall()

                quantidade_alunos = len(
                    alunos_da_turma
                )

                vagas_disponiveis = (
                    limite_consulta
                    - quantidade_alunos
                )

                if vagas_disponiveis < 0:
                    vagas_disponiveis = 0

                st.write(
                    f"**Turma:** {turma_consulta}"
                )

                st.write(
                    f"**Instrutor:** "
                    f"{instrutor_consulta}"
                )

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Alunos",
                    quantidade_alunos
                )

                col2.metric(
                    "Limite",
                    limite_consulta
                )

                col3.metric(
                    "Vagas",
                    vagas_disponiveis
                )

                st.divider()

                if quantidade_alunos == 0:
                    st.info(
                        "Nenhum aluno cadastrado nesta turma."
                    )

                else:
                    st.subheader(
                        "👥 Alunos matriculados"
                    )

                    for numero, aluno in enumerate(
                        alunos_da_turma,
                        start=1
                    ):
                        nome_aluno = aluno[1]
                        telefone_aluno = (
                            aluno[2]
                            or "Não informado"
                        )
                        tabela_aluno = (
                            aluno[3]
                            or "Não informada"
                        )

                        st.write(
                            f"**{numero}. "
                            f"{nome_aluno}**"
                        )

                        st.caption(
                            f"Telefone: "
                            f"{telefone_aluno} | "
                            f"Tabela: {tabela_aluno}"
                        )

                        st.divider()
elif menu == "✅ Presenças":
    st.title("Presenças")

    aba_chamada, aba_historico = st.tabs(
        [
            "✅ Fazer chamada",
            "📋 Histórico de presenças"
        ]
    )
    # =========================
    # ABA 1 - FAZER CHAMADA
    # =========================
    with aba_chamada:
        st.subheader("Fazer chamada")
        if "mensagem_chamada" in st.session_state:
            st.success(
                st.session_state["mensagem_chamada"]
            )

            del st.session_state["mensagem_chamada"]

        # =========================
        # DATA DA AULA
        # =========================
        data_aula = st.date_input(
            "Data da aula",
            key="presenca_data"
        )

        dia_semana_numero = data_aula.weekday()

        mapa_dias = {
            0: "Segunda",
            1: "Terça",
            2: "Quarta",
            3: "Quinta",
            4: "Sexta",
            5: "Sábado",
            6: "Domingo"
        }

        dia_semana_nome = mapa_dias[
            dia_semana_numero
        ]

        # =========================
        # TURMAS DO DIA
        # =========================
        cursor.execute("""
            SELECT
                id,
                dias,
                horario,
                instrutor
            FROM turmas
            WHERE dias LIKE ?
            ORDER BY horario
        """, (
            f"%{dia_semana_nome}%",
        ))

        turmas_presenca = cursor.fetchall()

        if len(turmas_presenca) == 0:
            st.info(
                f"Nenhuma turma cadastrada para {dia_semana_nome}."
            )

        else:
            opcoes_turmas = {
                f"{t[1]} - {t[2]}": t[0]
                for t in turmas_presenca
            }

            lista_turmas_presenca = (
                [""]
                + list(opcoes_turmas.keys())
            )

            turma_escolhida = st.selectbox(
                "Escolha a turma",
                lista_turmas_presenca,
                index=0,
                key="presenca_turma"
            )

            if turma_escolhida == "":
                st.info(
                    "Selecione uma turma para fazer a chamada."
                )

            else:
                turma_id_presenca = opcoes_turmas[
                    turma_escolhida
                ]

                instrutor_padrao = None

                for turma in turmas_presenca:
                    if turma[0] == turma_id_presenca:
                        instrutor_padrao = turma[3]
                        break

                # =========================
                # INSTRUTOR DESTA AULA
                # =========================
                cursor.execute("""
                    SELECT nome
                    FROM instrutores
                    ORDER BY nome
                """)

                instrutores_cadastrados = (
                    cursor.fetchall()
                )

                nomes_instrutores = [
                    instrutor[0]
                    for instrutor in instrutores_cadastrados
                ]

                if len(nomes_instrutores) == 0:
                    st.warning(
                        "Nenhum instrutor cadastrado."
                    )

                    instrutor_aula = instrutor_padrao

                else:
                    if instrutor_padrao in nomes_instrutores:
                        indice_instrutor = nomes_instrutores.index(
                            instrutor_padrao
                        )
                    else:
                        indice_instrutor = 0

                    instrutor_aula = st.selectbox(
                        "👨‍🏫 Instrutor desta aula",
                        nomes_instrutores,
                        index=indice_instrutor,
                        key=(
                            f"instrutor_aula_"
                            f"{turma_id_presenca}_"
                            f"{data_aula}"
                        )
                    )

                # =========================
                # ALUNOS FIXOS
                # =========================
                cursor.execute("""
                    SELECT id, nome
                    FROM alunos
                    WHERE turma_id = ?
                    ORDER BY nome
                """, (
                    turma_id_presenca,
                ))

                alunos_turma = cursor.fetchall()

                # =========================
                # REPOSIÇÕES AGENDADAS
                # =========================
                cursor.execute("""
                    SELECT
                        a.id,
                        a.nome,
                        r.id
                    FROM reposicoes r
                    INNER JOIN alunos a
                        ON r.aluno_id = a.id
                    WHERE r.turma_reposicao_id = ?
                    AND r.data_reposicao = ?
                    AND r.status = 'Agendada'
                    ORDER BY a.nome
                """, (
                    turma_id_presenca,
                    str(data_aula)
                ))

                alunos_reposicao = (
                    cursor.fetchall()
                )

                if (
                    len(alunos_turma) == 0
                    and len(alunos_reposicao) == 0
                ):
                    st.warning(
                        "Não há alunos cadastrados "
                        "ou reposições agendadas "
                        "nessa turma."
                    )

                else:
                    st.subheader("Alunos")

                    presencas_marcadas = []

                    # =========================
                    # ALUNOS DA TURMA
                    # =========================
                    for aluno in alunos_turma:
                        aluno_id = aluno[0]
                        aluno_nome = aluno[1]

                        status = st.radio(
                            aluno_nome,
                            [
                                "Presente",
                                "Falta",
                                "Ausência justificada"
                            ],
                            horizontal=True,
                            key=(
                                f"presenca_"
                                f"{turma_id_presenca}_"
                                f"{aluno_id}_"
                                f"{data_aula}"
                            )
                        )

                        presencas_marcadas.append(
                            (
                                aluno_id,
                                turma_id_presenca,
                                str(data_aula),
                                status
                            )
                        )

                    # =========================
                    # ALUNOS DE REPOSIÇÃO
                    # =========================
                    if len(alunos_reposicao) > 0:
                        st.markdown(
                            "### 🔄 Reposições agendadas"
                        )

                        for reposicao in alunos_reposicao:
                            aluno_id = reposicao[0]
                            aluno_nome = reposicao[1]
                            reposicao_id = reposicao[2]

                            status = st.radio(
                                f"🔄 {aluno_nome}",
                                [
                                    "Reposição",
                                    "Não compareceu"
                                ],
                                horizontal=True,
                                key=(
                                    f"reposicao_chamada_"
                                    f"{reposicao_id}_"
                                    f"{data_aula}"
                                )
                            )

                            presencas_marcadas.append(
                                (
                                    aluno_id,
                                    turma_id_presenca,
                                    str(data_aula),
                                    status,
                                    reposicao_id
                                )
                            )

                    # =========================
                    # SALVAR CHAMADA
                    # =========================
                    if st.button(
                        "Salvar chamada",
                        key=(
                            f"salvar_chamada_"
                            f"{turma_id_presenca}_"
                            f"{data_aula}"
                        )
                    ):
                        for presenca in presencas_marcadas:
                            aluno_id = presenca[0]
                            turma_id = presenca[1]
                            data = presenca[2]
                            status = presenca[3]

                            if len(presenca) > 4:
                                reposicao_id = presenca[4]
                            else:
                                reposicao_id = None

                            cursor.execute("""
                                SELECT id
                                FROM presencas
                                WHERE aluno_id = ?
                                AND turma_id = ?
                                AND data = ?
                            """, (
                                aluno_id,
                                turma_id,
                                data
                            ))

                            presenca_existente = (
                                cursor.fetchone()
                            )

                            if presenca_existente:
                                cursor.execute("""
                                    UPDATE presencas
                                    SET
                                        status = ?,
                                        instrutor_aula = ?
                                    WHERE id = ?
                                """, (
                                    status,
                                    instrutor_aula,
                                    presenca_existente[0]
                                ))

                            else:
                                cursor.execute("""
                                    INSERT INTO presencas
                                    (
                                        aluno_id,
                                        turma_id,
                                        data,
                                        status,
                                        instrutor_aula
                                    )
                                    VALUES (?, ?, ?, ?, ?)
                                """, (
                                    aluno_id,
                                    turma_id,
                                    data,
                                    status,
                                    instrutor_aula
                                ))

                            if (
                                reposicao_id is not None
                                and status == "Reposição"
                            ):
                                cursor.execute("""
                                    UPDATE reposicoes
                                    SET status = 'Realizada'
                                    WHERE id = ?
                                """, (
                                    reposicao_id,
                                ))

                        conn.commit()

                        st.session_state["mensagem_chamada"] = (
                            "✅ Chamada salva com sucesso!"
                        )

                        st.rerun()
    # =========================
    # ABA 2 - HISTÓRICO
    # =========================
    with aba_historico:
        st.subheader("Histórico de presenças")

        # =========================
        # HORÁRIOS DISPONÍVEIS
        # =========================
        cursor.execute("""
            SELECT DISTINCT horario
            FROM turmas
            WHERE horario IS NOT NULL
            ORDER BY horario
        """)

        horarios_banco = cursor.fetchall()

        horarios = [
            horario[0]
            for horario in horarios_banco
            if horario[0]
        ]

        opcoes_horarios = (
            ["Todos os horários"]
            + horarios
        )

        horario_selecionado = st.selectbox(
            "Buscar por horário",
            opcoes_horarios,
            key="historico_presenca_horario"
        )

        # =========================
        # FILTRO POR DATA
        # =========================
        filtro_data = st.selectbox(
            "Buscar por data",
            [
                "Todas as datas",
                "Escolher uma data"
            ],
            key="historico_filtro_data"
        )

        if filtro_data == "Escolher uma data":
            data_selecionada = st.date_input(
                "Data",
                key="historico_presenca_data"
            )
        else:
            data_selecionada = None

        # =========================
        # CONSULTA DO HISTÓRICO
        # =========================
        if (
            horario_selecionado == "Todos os horários"
            and data_selecionada is None
        ):

            cursor.execute("""
                SELECT
                    p.id,
                    a.nome,
                    t.dias,
                    t.horario,
                    p.data,
                    p.status
                FROM presencas p
                INNER JOIN alunos a
                    ON p.aluno_id = a.id
                INNER JOIN turmas t
                    ON p.turma_id = t.id
                ORDER BY
                    p.data DESC,
                    t.horario,
                    a.nome
            """)

        elif (
            horario_selecionado != "Todos os horários"
            and data_selecionada is None
        ):

            cursor.execute("""
                SELECT
                    p.id,
                    a.nome,
                    t.dias,
                    t.horario,
                    p.data,
                    p.status
                FROM presencas p
                INNER JOIN alunos a
                    ON p.aluno_id = a.id
                INNER JOIN turmas t
                    ON p.turma_id = t.id
                WHERE t.horario = ?
                ORDER BY
                    p.data DESC,
                    a.nome
            """, (
                horario_selecionado,
            ))

        elif (
            horario_selecionado == "Todos os horários"
            and data_selecionada is not None
        ):

            cursor.execute("""
                SELECT
                    p.id,
                    a.nome,
                    t.dias,
                    t.horario,
                    p.data,
                    p.status
                FROM presencas p
                INNER JOIN alunos a
                    ON p.aluno_id = a.id
                INNER JOIN turmas t
                    ON p.turma_id = t.id
                WHERE p.data = ?
                ORDER BY
                    t.horario,
                    a.nome
            """, (
                str(data_selecionada),
            ))

        else:

            cursor.execute("""
                SELECT
                    p.id,
                    a.nome,
                    t.dias,
                    t.horario,
                    p.data,
                    p.status
                FROM presencas p
                INNER JOIN alunos a
                    ON p.aluno_id = a.id
                INNER JOIN turmas t
                    ON p.turma_id = t.id
                WHERE t.horario = ?
                AND p.data = ?
                ORDER BY
                    a.nome
            """, (
                horario_selecionado,
                str(data_selecionada)
            ))

        historico_presencas = cursor.fetchall()
elif menu == "💰 Financeiro":
    st.title("Financeiro")

    from datetime import date

    aba_pagamento, aba_historico, aba_edicao = st.tabs(
        [
            "➕ Novo pagamento",
            "📊 Resumo / Histórico",
            "✏️ Editar / Excluir"
        ]
    )

    # =========================
    # ABA 1 - NOVO PAGAMENTO
    # =========================
    with aba_pagamento:
        st.subheader("Novo pagamento")

        cursor.execute("""
            SELECT id, nome, tabela_preco
            FROM alunos
            ORDER BY nome
        """)

        alunos_financeiro = cursor.fetchall()

        if len(alunos_financeiro) == 0:
            st.info("Nenhum aluno cadastrado.")

        else:
            opcoes_alunos = {
                aluno[1]: {
                    "id": aluno[0],
                    "tabela_preco": aluno[2]
                }
                for aluno in alunos_financeiro
            }

            aluno_escolhido = st.selectbox(
                "Aluno",
                list(opcoes_alunos.keys()),
                key="financeiro_aluno"
            )

            aluno_id_financeiro = (
                opcoes_alunos[
                    aluno_escolhido
                ]["id"]
            )

            tabela_aluno = (
                opcoes_alunos[
                    aluno_escolhido
                ]["tabela_preco"]
            )

            if tabela_aluno not in [
                "Antigo",
                "Novo"
            ]:
                tabela_aluno = "Antigo"

            tabela_escolhida = st.selectbox(
                "Tabela de preço",
                [
                    "Antigo",
                    "Novo"
                ],
                index=(
                    0
                    if tabela_aluno == "Antigo"
                    else 1
                ),
                key=(
                    f"financeiro_tabela_preco_"
                    f"{aluno_id_financeiro}"
                )
            )
            plano = st.selectbox(
                "Plano",
                [
                    "8 aulas",
                    "24 aulas"
                ],
                key="financeiro_plano"
            )

            data_pagamento = st.date_input(
                "Data do pagamento",
                key="financeiro_data"
            )

            data_inicio_ciclo = st.date_input(
                "Início do ciclo",
                key="financeiro_inicio_ciclo"
            )
            # =========================
            # PREVISÃO DE RENOVAÇÃO
            # =========================
            cursor.execute("""
                SELECT turmas.dias
                FROM alunos
                LEFT JOIN turmas
                    ON alunos.turma_id = turmas.id
                WHERE alunos.id = ?
            """, (
                aluno_id_financeiro,
            ))

            resultado_turma = cursor.fetchone()

            if resultado_turma:
                dias_turma_aluno = resultado_turma[0]
            else:
                dias_turma_aluno = None

            cursor.execute("""
                SELECT data
                FROM dias_sem_aula
            """)

            dias_fechados_banco = cursor.fetchall()

            dias_fechados = set()

            for dia in dias_fechados_banco:
                dias_fechados.add(
                    datetime.strptime(
                        dia[0],
                        "%Y-%m-%d"
                    ).date()
                )

            if plano == "8 aulas":
                quantidade_aulas_plano = 8
            else:
                quantidade_aulas_plano = 24

            data_renovacao = calcular_data_renovacao(
                data_inicio_ciclo,
                dias_turma_aluno,
                quantidade_aulas_plano,
                dias_fechados
            )

            if data_renovacao:
                st.success(
                    f"📅 Renovação prevista: "
                    f"{data_renovacao.strftime('%d/%m/%Y')}"
                )
            else:
                st.warning(
                    "Não foi possível calcular a renovação. "
                    "Confira se o aluno está vinculado a uma turma."
                )
            # =========================
            # VALORES DO PLANO
            # =========================
            data_reajuste = date(2027, 1, 1)

            if data_pagamento >= data_reajuste:
                tabela_usada = "Novo"
            else:
                tabela_usada = tabela_escolhida

            if plano == "8 aulas":
                if tabela_usada == "Antigo":
                    valor = 150.00
                else:
                    valor = 180.00

            else:
                if tabela_usada == "Antigo":
                    valor = 410.00
                else:
                    valor = 500.00

            st.info(
                f"Tabela aplicada: {tabela_usada} | "
                f"Plano: {plano} | "
                f"Valor: R$ {valor:.2f}"
            )

            forma_pagamento = st.selectbox(
                "Forma de pagamento",
                [
                    "PIX",
                    "Dinheiro",
                    "Débito",
                    "Crédito"
                ],
                key="financeiro_forma"
            )

            if forma_pagamento in [
                "Débito",
                "Crédito"
            ]:
                taxa_percentual = st.number_input(
                    "Taxa do cartão (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=0.0,
                    step=0.1,
                    key="financeiro_taxa"
                )
            else:
                taxa_percentual = 0.0

            valor_taxa = (
                valor
                * taxa_percentual
                / 100
            )

            valor_liquido = (
                valor
                - valor_taxa
            )

            col1, col2 = st.columns(2)

            col1.metric(
                "Valor da taxa",
                f"R$ {valor_taxa:.2f}"
            )

            col2.metric(
                "Valor líquido",
                f"R$ {valor_liquido:.2f}"
            )

            status_pagamento = st.selectbox(
                "Status",
                [
                    "Pago",
                    "Pendente"
                ],
                key="financeiro_status"
            )

            if st.button(
                "Salvar pagamento",
                key="salvar_pagamento"
            ):
                cursor.execute("""
                    INSERT INTO financeiro
                    (
                        aluno_id,
                        valor,
                        data_pagamento,
                        data_inicio_ciclo,
                        forma_pagamento,
                        status,
                        taxa_percentual,
                        valor_taxa,
                        valor_liquido,
                        plano
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    aluno_id_financeiro,
                    valor,
                    str(data_pagamento),
                    str(data_inicio_ciclo),
                    forma_pagamento,
                    status_pagamento,
                    taxa_percentual,
                    valor_taxa,
                    valor_liquido,
                    plano
                ))

                conn.commit()

                st.success(
                    "Pagamento salvo com sucesso!"
                )

    # =========================
    # ABA 2 - RESUMO / HISTÓRICO
    # =========================
    with aba_historico:
        st.subheader("Resumo financeiro")

        cursor.execute("""
            SELECT
                financeiro.id,
                alunos.nome,
                financeiro.valor,
                financeiro.data_pagamento,
                financeiro.data_inicio_ciclo,
                financeiro.forma_pagamento,
                financeiro.status,
                financeiro.valor_taxa,
                financeiro.valor_liquido,
                financeiro.plano
            FROM financeiro
            INNER JOIN alunos
                ON financeiro.aluno_id = alunos.id
            ORDER BY financeiro.id DESC
        """)

        pagamentos = cursor.fetchall()

        total_recebido = 0
        total_pendente = 0
        total_taxas = 0
        total_liquido = 0

        for pagamento in pagamentos:
            if pagamento[6] == "Pago":
                total_recebido += pagamento[2]
                total_taxas += pagamento[7] or 0
                total_liquido += pagamento[8] or 0

            else:
                total_pendente += pagamento[2]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total bruto",
            f"R$ {total_recebido:.2f}"
        )

        col2.metric(
            "Taxas",
            f"R$ {total_taxas:.2f}"
        )

        col3.metric(
            "Total líquido",
            f"R$ {total_liquido:.2f}"
        )

        col4.metric(
            "Pendente",
            f"R$ {total_pendente:.2f}"
        )

        st.divider()
        st.subheader("Histórico")

        if len(pagamentos) == 0:
            st.info(
                "Nenhum pagamento registrado ainda."
            )

        else:
            for pagamento in pagamentos:
                plano_historico = (
                    pagamento[9]
                    or "Não informado"
                )

                inicio_ciclo_historico = (
                    pagamento[4]
                    or pagamento[3]
                )

                st.write(
                    f"**{pagamento[1]}** | "
                    f"Plano: {plano_historico} | "
                    f"Bruto: R$ {pagamento[2]:.2f} | "
                    f"Taxa: R$ {(pagamento[7] or 0):.2f} | "
                    f"Líquido: R$ {(pagamento[8] or 0):.2f} | "
                    f"Pagamento: {pagamento[3]} | "
                    f"Início do ciclo: {inicio_ciclo_historico} | "
                    f"{pagamento[5]} | "
                    f"{pagamento[6]}"
                )

    # =========================
    # ABA 3 - EDITAR / EXCLUIR
    # =========================
    with aba_edicao:
        st.subheader(
            "Editar ou excluir lançamento"
        )

        cursor.execute("""
            SELECT
                financeiro.id,
                alunos.nome,
                financeiro.valor,
                financeiro.data_pagamento,
                financeiro.data_inicio_ciclo,
                financeiro.forma_pagamento,
                financeiro.status,
                financeiro.taxa_percentual,
                financeiro.valor_taxa,
                financeiro.valor_liquido,
                financeiro.plano
            FROM financeiro
            INNER JOIN alunos
                ON financeiro.aluno_id = alunos.id
            ORDER BY financeiro.id DESC
        """)

        lancamentos = cursor.fetchall()

        if len(lancamentos) == 0:
            st.info(
                "Nenhum lançamento disponível para edição."
            )

        else:
            opcoes_lancamentos = {
                (
                    f"ID {l[0]} - "
                    f"{l[1]} - "
                    f"R$ {l[2]:.2f}"
                ): l[0]
                for l in lancamentos
            }

            lancamento_escolhido = st.selectbox(
                "Selecione o lançamento",
                list(opcoes_lancamentos.keys()),
                key="editar_financeiro"
            )

            lancamento_id = opcoes_lancamentos[
                lancamento_escolhido
            ]

            cursor.execute("""
                SELECT
                    valor,
                    data_pagamento,
                    data_inicio_ciclo,
                    forma_pagamento,
                    status,
                    taxa_percentual,
                    plano
                FROM financeiro
                WHERE id = ?
            """, (
                lancamento_id,
            ))

            dados_financeiro = cursor.fetchone()

            novo_valor = st.number_input(
                "Valor bruto",
                min_value=0.0,
                value=float(
                    dados_financeiro[0] or 0
                ),
                key=(
                    f"editar_valor_financeiro_"
                    f"{lancamento_id}"
                )
            )

            # =========================
            # DATAS
            # =========================
            if dados_financeiro[1]:
                data_pagamento_atual = (
                    datetime.strptime(
                        dados_financeiro[1],
                        "%Y-%m-%d"
                    ).date()
                )
            else:
                data_pagamento_atual = date.today()

            if dados_financeiro[2]:
                data_inicio_ciclo_atual = (
                    datetime.strptime(
                        dados_financeiro[2],
                        "%Y-%m-%d"
                    ).date()
                )
            else:
                data_inicio_ciclo_atual = (
                    data_pagamento_atual
                )

            nova_data_pagamento = st.date_input(
                "Data do pagamento",
                value=data_pagamento_atual,
                key=(
                    f"editar_data_pagamento_"
                    f"{lancamento_id}"
                )
            )

            nova_data_inicio_ciclo = st.date_input(
                "Início do ciclo",
                value=data_inicio_ciclo_atual,
                key=(
                    f"editar_inicio_ciclo_"
                    f"{lancamento_id}"
                )
            )

            planos_edicao = [
                "8 aulas",
                "24 aulas"
            ]

            plano_atual = dados_financeiro[6]

            if plano_atual in planos_edicao:
                indice_plano = planos_edicao.index(
                    plano_atual
                )
            else:
                indice_plano = 0

            novo_plano = st.selectbox(
                "Plano",
                planos_edicao,
                index=indice_plano,
                key=(
                    f"editar_plano_financeiro_"
                    f"{lancamento_id}"
                )
            )

            formas_pagamento = [
                "PIX",
                "Dinheiro",
                "Débito",
                "Crédito"
            ]

            forma_atual = dados_financeiro[3]

            if forma_atual in formas_pagamento:
                indice_forma = formas_pagamento.index(
                    forma_atual
                )
            else:
                indice_forma = 0

            nova_forma = st.selectbox(
                "Forma de pagamento",
                formas_pagamento,
                index=indice_forma,
                key=(
                    f"editar_forma_financeiro_"
                    f"{lancamento_id}"
                )
            )

            status_opcoes = [
                "Pago",
                "Pendente"
            ]

            status_atual = dados_financeiro[4]

            if status_atual in status_opcoes:
                indice_status = status_opcoes.index(
                    status_atual
                )
            else:
                indice_status = 0

            novo_status = st.selectbox(
                "Status",
                status_opcoes,
                index=indice_status,
                key=(
                    f"editar_status_financeiro_"
                    f"{lancamento_id}"
                )
            )

            if nova_forma in [
                "Débito",
                "Crédito"
            ]:
                nova_taxa = st.number_input(
                    "Taxa do cartão (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(
                        dados_financeiro[5] or 0
                    ),
                    key=(
                        f"editar_taxa_financeiro_"
                        f"{lancamento_id}"
                    )
                )

            else:
                nova_taxa = 0.0

            novo_valor_taxa = (
                novo_valor
                * nova_taxa
                / 100
            )

            novo_valor_liquido = (
                novo_valor
                - novo_valor_taxa
            )

            col1, col2 = st.columns(2)

            col1.metric(
                "Taxa",
                f"R$ {novo_valor_taxa:.2f}"
            )

            col2.metric(
                "Líquido",
                f"R$ {novo_valor_liquido:.2f}"
            )

            col_salvar, col_excluir = st.columns(2)

            if col_salvar.button(
                "Salvar alterações",
                key=(
                    f"salvar_financeiro_"
                    f"{lancamento_id}"
                )
            ):
                cursor.execute("""
                    UPDATE financeiro
                    SET
                        valor = ?,
                        data_pagamento = ?,
                        data_inicio_ciclo = ?,
                        forma_pagamento = ?,
                        status = ?,
                        taxa_percentual = ?,
                        valor_taxa = ?,
                        valor_liquido = ?,
                        plano = ?
                    WHERE id = ?
                """, (
                    novo_valor,
                    str(nova_data_pagamento),
                    str(nova_data_inicio_ciclo),
                    nova_forma,
                    novo_status,
                    nova_taxa,
                    novo_valor_taxa,
                    novo_valor_liquido,
                    novo_plano,
                    lancamento_id
                ))

                conn.commit()

                st.success(
                    "Lançamento atualizado com sucesso!"
                )

            if col_excluir.button(
                "Excluir lançamento",
                key=(
                    f"excluir_financeiro_"
                    f"{lancamento_id}"
                )
            ):
                cursor.execute(
                    """
                    DELETE FROM financeiro
                    WHERE id = ?
                    """,
                    (
                        lancamento_id,
                    )
                )

                conn.commit()

                st.success(
                    "Lançamento excluído com sucesso!"
                )

                st.rerun()
elif menu == "🩺 Fisioterapia":
    st.title("Fisioterapia")

    aba_atendimento, aba_resumo, aba_edicao = st.tabs(
        [
            "➕ Novo atendimento",
            "📊 Resumo",
            "✏️ Editar / Excluir"
        ]
    )

    # =========================
    # ABA 1 - NOVO ATENDIMENTO
    # =========================
    with aba_atendimento:
        st.subheader("Novo atendimento")

        if "fisio_form_version" not in st.session_state:
            st.session_state.fisio_form_version = 0

        versao_fisio = st.session_state.fisio_form_version

        if st.session_state.pop(
            "fisio_atendimento_salvo",
            False
        ):
            st.success(
                "Atendimento salvo com sucesso!"
            )

        paciente = st.text_input(
            "Nome do paciente",
            key=f"fisio_paciente_{versao_fisio}"
        )

        data_atendimento = st.date_input(
            "Data do atendimento",
            key=f"fisio_data_{versao_fisio}"
        )

        valor_fisio = st.number_input(
            "Valor do atendimento",
            min_value=0.0,
            value=80.0,
            step=10.0,
            key=f"fisio_valor_{versao_fisio}"
        )

        forma_pagamento_fisio = st.selectbox(
            "Forma de pagamento",
            [
                "PIX",
                "Dinheiro",
                "Débito",
                "Crédito"
            ],
            key=f"fisio_pagamento_{versao_fisio}"
        )

        if forma_pagamento_fisio in [
            "Débito",
            "Crédito"
        ]:
            taxa_fisio = st.number_input(
                "Taxa do cartão (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                key=f"fisio_taxa_{versao_fisio}"
            )

        else:
            taxa_fisio = 0.0

        valor_taxa_fisio = (
            valor_fisio
            * taxa_fisio
            / 100
        )

        valor_liquido_fisio = (
            valor_fisio
            - valor_taxa_fisio
        )

        col1, col2 = st.columns(2)

        col1.metric(
            "Valor da taxa",
            f"R$ {valor_taxa_fisio:.2f}"
        )

        col2.metric(
            "Valor líquido",
            f"R$ {valor_liquido_fisio:.2f}"
        )

        profissional = st.text_input(
            "Profissional",
            value="Igor",
            key=f"fisio_profissional_{versao_fisio}"
        )

        observacao_fisio = st.text_area(
            "Observação",
            key=f"fisio_observacao_{versao_fisio}"
        )

        if st.button(
            "Salvar atendimento",
            key=(
                f"salvar_atendimento_fisio_"
                f"{versao_fisio}"
            )
        ):
            if paciente.strip() == "":
                st.warning(
                    "Digite o nome do paciente."
                )

            else:
                cursor.execute("""
                    INSERT INTO fisioterapia
                    (
                        paciente,
                        data,
                        valor,
                        forma_pagamento,
                        taxa_percentual,
                        valor_taxa,
                        valor_liquido,
                        profissional,
                        observacao
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    paciente,
                    str(data_atendimento),
                    valor_fisio,
                    forma_pagamento_fisio,
                    taxa_fisio,
                    valor_taxa_fisio,
                    valor_liquido_fisio,
                    profissional,
                    observacao_fisio
                ))

                conn.commit()

                st.session_state[
                    "fisio_atendimento_salvo"
                ] = True

                st.session_state.fisio_form_version += 1

                st.rerun()  
    # =========================
    # ABA 3 - EDITAR / EXCLUIR
    # =========================
    with aba_edicao:
        st.subheader(
            "Editar ou excluir atendimento"
        )

        cursor.execute("""
            SELECT
                id,
                paciente,
                data,
                valor,
                forma_pagamento,
                taxa_percentual,
                valor_taxa,
                valor_liquido,
                profissional,
                observacao
            FROM fisioterapia
            ORDER BY id DESC
        """)

        atendimentos_edicao = cursor.fetchall()

        if len(atendimentos_edicao) == 0:
            st.info(
                "Nenhum atendimento disponível para edição."
            )

        else:
            opcoes_atendimentos = {
                f"ID {a[0]} - {a[1]} - R$ {a[3]:.2f}": a[0]
                for a in atendimentos_edicao
            }

            atendimento_selecionado = st.selectbox(
                "Selecione o atendimento",
                list(opcoes_atendimentos.keys()),
                key="editar_fisio"
            )

            atendimento_id = opcoes_atendimentos[
                atendimento_selecionado
            ]

            cursor.execute("""
                SELECT
                    paciente,
                    valor,
                    forma_pagamento,
                    taxa_percentual,
                    profissional,
                    observacao
                FROM fisioterapia
                WHERE id = ?
            """, (
                atendimento_id,
            ))

            dados_atendimento = cursor.fetchone()

            novo_paciente = st.text_input(
                "Paciente",
                value=dados_atendimento[0] or "",
                key=f"editar_paciente_fisio_{atendimento_id}"
            )

            novo_valor_fisio = st.number_input(
                "Valor do atendimento",
                min_value=0.0,
                value=float(
                    dados_atendimento[1] or 0
                ),
               key=f"editar_valor_fisio_{atendimento_id}"
            )

            formas_fisio = [
                "PIX",
                "Dinheiro",
                "Débito",
                "Crédito"
            ]

            forma_atual_fisio = dados_atendimento[2]

            if forma_atual_fisio in formas_fisio:
                indice_forma_fisio = formas_fisio.index(
                    forma_atual_fisio
                )
            else:
                indice_forma_fisio = 0

            nova_forma_fisio = st.selectbox(
                "Forma de pagamento",
                formas_fisio,
                index=indice_forma_fisio,
                key=f"editar_forma_fisio_{atendimento_id}"
            )

            if nova_forma_fisio in ["Débito", "Crédito"]:
                nova_taxa_fisio = st.number_input(
                    "Taxa do cartão (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(
                        dados_atendimento[3] or 0
                    ),
                    key=f"editar_taxa_fisio_{atendimento_id}"
                )
            else:
                nova_taxa_fisio = 0.0

            novo_valor_taxa_fisio = (
                novo_valor_fisio
                * nova_taxa_fisio
                / 100
            )

            novo_liquido_fisio = (
                novo_valor_fisio
                - novo_valor_taxa_fisio
            )

            novo_profissional = st.text_input(
                "Profissional",
                value=dados_atendimento[4] or "",
                key=f"editar_profissional_fisio_{atendimento_id}"
            )

            nova_observacao_fisio = st.text_area(
                "Observação",
                value=dados_atendimento[5] or "",
                key=f"editar_observacao_fisio_{atendimento_id}"
            )

            col1, col2 = st.columns(2)

            col1.metric(
                "Valor da taxa",
                f"R$ {novo_valor_taxa_fisio:.2f}"
            )

            col2.metric(
                "Valor líquido",
                f"R$ {novo_liquido_fisio:.2f}"
            )

            col_salvar, col_excluir = st.columns(2)

            if col_salvar.button(
                "Salvar alterações",
                key=f"salvar_edicao_fisio_{atendimento_id}"
            ):
                cursor.execute("""
                    UPDATE fisioterapia
                    SET
                        paciente = ?,
                        valor = ?,
                        forma_pagamento = ?,
                        taxa_percentual = ?,
                        valor_taxa = ?,
                        valor_liquido = ?,
                        profissional = ?,
                        observacao = ?
                    WHERE id = ?
                """, (
                    novo_paciente,
                    novo_valor_fisio,
                    nova_forma_fisio,
                    nova_taxa_fisio,
                    novo_valor_taxa_fisio,
                    novo_liquido_fisio,
                    novo_profissional,
                    nova_observacao_fisio,
                    atendimento_id
                ))

                conn.commit()

                st.success(
                    "Atendimento atualizado com sucesso!"
                )

            if col_excluir.button(
                "Excluir atendimento",
                key=f"excluir_fisio_{atendimento_id}"
            ):
                cursor.execute(
                    "DELETE FROM fisioterapia WHERE id = ?",
                    (
                        atendimento_id,
                    )
                )

                conn.commit()

                st.success(
                    "Atendimento excluído com sucesso!"
                )
elif menu == "💸 Despesas":
    st.title("Despesas")

    aba_nova, aba_historico, aba_edicao = st.tabs(
        [
            "➕ Nova despesa",
            "📋 Histórico / Resumo",
            "✏️ Editar / Excluir"
        ]
    )

    # =========================
    # ABA 1 - NOVA DESPESA
    # =========================
    with aba_nova:
        st.subheader("Nova despesa")

        descricao = st.text_input(
            "Descrição da despesa",
            key="despesa_descricao"
        )

        categoria = st.selectbox(
            "Categoria",
            [
                "Aluguel",
                "Energia",
                "Internet",
                "Água",
                "Material de limpeza",
                "Materiais",
                "Salários",
                "Manutenção",
                "Impostos",
                "Outros"
            ],
            key="despesa_categoria"
        )

        valor_despesa = st.number_input(
            "Valor da despesa",
            min_value=0.0,
            value=0.0,
            step=10.0,
            key="despesa_valor"
        )

        data_despesa = st.date_input(
            "Data da despesa",
            key="despesa_data"
        )

        forma_pagamento_despesa = st.selectbox(
            "Forma de pagamento",
            [
                "PIX",
                "Dinheiro",
                "Débito",
                "Crédito",
                "Boleto",
                "Transferência"
            ],
            key="despesa_pagamento"
        )

        observacao = st.text_area(
            "Observação",
            key="despesa_observacao"
        )

        if st.button(
            "Salvar despesa",
            key="salvar_despesa"
        ):
            if descricao.strip() == "":
                st.warning(
                    "Digite a descrição da despesa."
                )

            elif valor_despesa <= 0:
                st.warning(
                    "Informe um valor maior que zero."
                )

            else:
                cursor.execute("""
                    INSERT INTO despesas
                    (
                        descricao,
                        categoria,
                        valor,
                        data,
                        forma_pagamento,
                        observacao
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    descricao,
                    categoria,
                    valor_despesa,
                    str(data_despesa),
                    forma_pagamento_despesa,
                    observacao
                ))

                conn.commit()

                st.success(
                    "Despesa salva com sucesso!"
                )

    # =========================
    # ABA 2 - HISTÓRICO / RESUMO
    # =========================
    with aba_historico:
        st.subheader("Resumo das despesas")

        cursor.execute("""
            SELECT
                id,
                descricao,
                categoria,
                valor,
                data,
                forma_pagamento,
                observacao
            FROM despesas
            ORDER BY id DESC
        """)

        despesas = cursor.fetchall()

        total_despesas = 0

        for despesa in despesas:
            total_despesas += despesa[3]

        st.metric(
            "Total de despesas",
            f"R$ {total_despesas:.2f}"
        )

        st.divider()
        st.subheader("Histórico")

        if len(despesas) == 0:
            st.info(
                "Nenhuma despesa registrada ainda."
            )

        else:
            for despesa in despesas:
                st.write(
                    f"**{despesa[1]}** | "
                    f"{despesa[2]} | "
                    f"R$ {despesa[3]:.2f} | "
                    f"{despesa[4]} | "
                    f"{despesa[5]}"
                )

                if despesa[6]:
                    st.caption(
                        f"Observação: {despesa[6]}"
                    )

    # =========================
    # ABA 3 - EDITAR / EXCLUIR
    # =========================
    with aba_edicao:
        st.subheader(
            "Editar ou excluir despesa"
        )

        cursor.execute("""
            SELECT
                id,
                descricao,
                categoria,
                valor,
                data,
                forma_pagamento,
                observacao
            FROM despesas
            ORDER BY id DESC
        """)

        despesas_edicao = cursor.fetchall()

        if len(despesas_edicao) == 0:
            st.info(
                "Nenhuma despesa disponível para edição."
            )

        else:
            opcoes_despesas = {
                f"ID {d[0]} - {d[1]} - R$ {d[3]:.2f}": d[0]
                for d in despesas_edicao
            }

            despesa_selecionada = st.selectbox(
                "Selecione a despesa",
                list(opcoes_despesas.keys()),
                key="editar_despesa"
            )

            despesa_id = opcoes_despesas[
                despesa_selecionada
            ]

            cursor.execute("""
                SELECT
                    descricao,
                    categoria,
                    valor,
                    forma_pagamento,
                    observacao
                FROM despesas
                WHERE id = ?
            """, (
                despesa_id,
            ))

            dados_despesa = cursor.fetchone()

            nova_descricao = st.text_input(
                "Descrição",
                value=dados_despesa[0] or "",
                key="editar_descricao_despesa"
            )

            categorias = [
                "Aluguel",
                "Energia",
                "Internet",
                "Água",
                "Material de limpeza",
                "Materiais",
                "Salários",
                "Manutenção",
                "Impostos",
                "Outros"
            ]

            categoria_atual = dados_despesa[1]

            if categoria_atual in categorias:
                indice_categoria = categorias.index(
                    categoria_atual
                )
            else:
                indice_categoria = 0

            nova_categoria = st.selectbox(
                "Categoria",
                categorias,
                index=indice_categoria,
                key="editar_categoria_despesa"
            )

            novo_valor_despesa = st.number_input(
                "Valor",
                min_value=0.0,
                value=float(
                    dados_despesa[2] or 0
                ),
                key="editar_valor_despesa"
            )

            formas_despesa = [
                "PIX",
                "Dinheiro",
                "Débito",
                "Crédito",
                "Boleto",
                "Transferência"
            ]

            forma_atual_despesa = dados_despesa[3]

            if forma_atual_despesa in formas_despesa:
                indice_forma = formas_despesa.index(
                    forma_atual_despesa
                )
            else:
                indice_forma = 0

            nova_forma_despesa = st.selectbox(
                "Forma de pagamento",
                formas_despesa,
                index=indice_forma,
                key="editar_forma_despesa"
            )

            nova_observacao = st.text_area(
                "Observação",
                value=dados_despesa[4] or "",
                key="editar_observacao_despesa"
            )

            col_salvar, col_excluir = st.columns(2)

            if col_salvar.button(
                "Salvar alterações",
                key="salvar_edicao_despesa"
            ):
                cursor.execute("""
                    UPDATE despesas
                    SET
                        descricao = ?,
                        categoria = ?,
                        valor = ?,
                        forma_pagamento = ?,
                        observacao = ?
                    WHERE id = ?
                """, (
                    nova_descricao,
                    nova_categoria,
                    novo_valor_despesa,
                    nova_forma_despesa,
                    nova_observacao,
                    despesa_id
                ))

                conn.commit()

                st.success(
                    "Despesa atualizada com sucesso!"
                )

            if col_excluir.button(
                "Excluir despesa",
                key="excluir_despesa"
            ):
                cursor.execute(
                    "DELETE FROM despesas WHERE id = ?",
                    (
                        despesa_id,
                    )
                )

                conn.commit()

                st.success(
                    "Despesa excluída com sucesso!"
                )
elif menu == "🔄 Reposições":
    st.title("Reposições")

    aba_registro, aba_agendar, aba_lista = st.tabs(
        [
            "➕ Registrar falta",
            "📅 Agendar reposição",
            "📋 Reposições registradas"
        ]
    )

    # =========================
    # ABA 1 - REGISTRAR FALTA
    # =========================
    with aba_registro:
        st.subheader("Registrar falta / direito à reposição")

        cursor.execute("""
            SELECT id, nome
            FROM alunos
            ORDER BY nome
        """)

        alunos_reposicao = cursor.fetchall()

        if len(alunos_reposicao) == 0:
            st.info(
                "Nenhum aluno cadastrado."
            )

        else:
            opcoes_alunos = {
                f"{aluno[1]} - ID {aluno[0]}": aluno[0]
                for aluno in alunos_reposicao
            }

            aluno_reposicao = st.selectbox(
                "Aluno",
                list(opcoes_alunos.keys()),
                key="reposicao_aluno"
            )

            aluno_id_reposicao = opcoes_alunos[
                aluno_reposicao
            ]

            data_falta = st.date_input(
                "Data da falta",
                key="reposicao_data_falta"
            )

            motivo = st.text_input(
                "Motivo da falta",
                key="reposicao_motivo"
            )

            direito_reposicao = st.selectbox(
                "Tem direito à reposição?",
                [
                    "Sim",
                    "Não"
                ],
                key="reposicao_direito"
            )

            st.caption(
                "A data e a turma da reposição serão "
                "definidas depois, quando houver vaga."
            )

            if st.button(
                "Salvar falta",
                key="salvar_reposicao"
            ):
                if direito_reposicao == "Sim":
                    status_reposicao = "Pendente"
                else:
                    status_reposicao = "Sem direito"

                cursor.execute("""
                    INSERT INTO reposicoes
                    (
                        aluno_id,
                        data_falta,
                        motivo,
                        direito_reposicao,
                        data_reposicao,
                        status,
                        turma_reposicao_id
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    aluno_id_reposicao,
                    str(data_falta),
                    motivo,
                    direito_reposicao,
                    None,
                    status_reposicao,
                    None
                ))

                conn.commit()

                st.success(
                    "Falta registrada com sucesso!"
                )

    # =========================
    # ABA 2 - AGENDAR REPOSIÇÃO
    # =========================
    with aba_agendar:
        st.subheader("Agendar reposição")

        cursor.execute("""
            SELECT
                r.id,
                a.nome,
                r.data_falta
            FROM reposicoes r
            INNER JOIN alunos a
                ON r.aluno_id = a.id
            WHERE r.direito_reposicao = 'Sim'
            AND r.status = 'Pendente'
            ORDER BY r.data_falta, a.nome
        """)

        reposicoes_pendentes = cursor.fetchall()

        if len(reposicoes_pendentes) == 0:
            st.info(
                "Nenhuma reposição pendente."
            )

        else:
            opcoes_pendentes = {
                (
                    f"{r[1]} | "
                    f"Falta: {r[2]} | "
                    f"ID {r[0]}"
                ): r[0]
                for r in reposicoes_pendentes
            }

            reposicao_escolhida = st.selectbox(
                "Aluno / falta",
                list(opcoes_pendentes.keys()),
                key="agendar_reposicao_aluno"
            )

            reposicao_id = opcoes_pendentes[
                reposicao_escolhida
            ]            
            # =========================
            # VERIFICA REGRA DE REPOSIÇÕES
            # =========================
            cursor.execute("""
                SELECT
                    aluno_id,
                    data_falta
                FROM reposicoes
                WHERE id = ?
            """, (
                reposicao_id,
            ))

            dados_reposicao_atual = cursor.fetchone()

            inicio_ciclo_reposicao = None
            fim_ciclo_reposicao = None
            quantidade_outras_reposicoes = 0

            if dados_reposicao_atual:
                aluno_id_agendamento = dados_reposicao_atual[0]
                data_falta_agendamento = dados_reposicao_atual[1]

                cursor.execute("""
                    SELECT
                        COALESCE(
                            data_inicio_ciclo,
                            data_pagamento
                        ),
                        plano
                    FROM financeiro
                    WHERE aluno_id = ?
                    AND COALESCE(
                        data_inicio_ciclo,
                        data_pagamento
                    ) <= ?
                    ORDER BY
                        COALESCE(
                            data_inicio_ciclo,
                            data_pagamento
                        ) DESC,
                        id DESC
                    LIMIT 1
                """, (
                    aluno_id_agendamento,
                    data_falta_agendamento
                ))

                ciclo_reposicao = cursor.fetchone()

                if ciclo_reposicao:
                    inicio_ciclo_reposicao = datetime.strptime(
                        ciclo_reposicao[0],
                        "%Y-%m-%d"
                    ).date()

                    plano_reposicao = ciclo_reposicao[1] or "8 aulas"

                    if "24" in str(plano_reposicao):
                        aulas_ciclo_reposicao = 24
                    else:
                        aulas_ciclo_reposicao = 8

                    cursor.execute("""
                        SELECT turmas.dias
                        FROM alunos
                        LEFT JOIN turmas
                            ON alunos.turma_id = turmas.id
                        WHERE alunos.id = ?
                    """, (
                        aluno_id_agendamento,
                    ))

                    turma_ciclo = cursor.fetchone()

                    if turma_ciclo:
                        dias_ciclo_reposicao = turma_ciclo[0]

                        cursor.execute("""
                            SELECT data
                            FROM dias_sem_aula
                        """)

                        dias_fechados_reposicao = set()

                        for dia in cursor.fetchall():
                            dias_fechados_reposicao.add(
                                datetime.strptime(
                                    dia[0],
                                    "%Y-%m-%d"
                                ).date()
                            )

                        fim_ciclo_reposicao = calcular_fim_ciclo(
                            inicio_ciclo_reposicao,
                            dias_ciclo_reposicao,
                            aulas_ciclo_reposicao,
                            dias_fechados_reposicao
                        )

                        if fim_ciclo_reposicao:
                            cursor.execute("""
                                SELECT COUNT(*)
                                FROM reposicoes
                                WHERE aluno_id = ?
                                AND id <> ?
                                AND direito_reposicao = 'Sim'
                                AND data_falta BETWEEN ? AND ?
                            """, (
                                aluno_id_agendamento,
                                reposicao_id,
                                str(inicio_ciclo_reposicao),
                                str(fim_ciclo_reposicao)
                            ))

                            quantidade_outras_reposicoes = (
                                cursor.fetchone()[0] or 0
                            )

                            if quantidade_outras_reposicoes >= 2:
                                st.warning(
                                    "⚠️ Este aluno já possui 2 reposições "
                                    "neste ciclo. Este agendamento será "
                                    "considerado uma exceção."
                                )

            data_reposicao = st.date_input(
                "Data da reposição",
                key="agendar_data_reposicao"
            )
            if (
                fim_ciclo_reposicao
                and data_reposicao > fim_ciclo_reposicao
            ):
                st.warning(
                    "⚠️ A data escolhida está fora do ciclo do aluno. "
                    "Este agendamento será considerado uma exceção."
                )

            cursor.execute("""
                SELECT
                    id,
                    dias,
                    horario,
                    instrutor
                FROM turmas
                ORDER BY dias, horario
            """)

            turmas_reposicao = cursor.fetchall()

            if len(turmas_reposicao) == 0:
                st.warning(
                    "Nenhuma turma cadastrada."
                )

            else:
                opcoes_turmas_reposicao = {
                    (
                        f"{t[1]} - {t[2]} | "
                        f"Instrutor: {t[3]}"
                    ): t[0]
                    for t in turmas_reposicao
                }

                turma_reposicao = st.selectbox(
                    "Turma onde fará a reposição",
                    list(
                        opcoes_turmas_reposicao.keys()
                    ),
                    key="agendar_turma_reposicao"
                )

                turma_reposicao_id = (
                    opcoes_turmas_reposicao[
                        turma_reposicao
                    ]
                )

                if st.button(
                    "Agendar reposição",
                    key="botao_agendar_reposicao"
                ):
                    cursor.execute("""
                        UPDATE reposicoes
                        SET
                            data_reposicao = ?,
                            turma_reposicao_id = ?,
                            status = 'Agendada'
                        WHERE id = ?
                    """, (
                        str(data_reposicao),
                        turma_reposicao_id,
                        reposicao_id
                    ))

                    conn.commit()

                    st.success(
                        "Reposição agendada com sucesso!"
                    )

                    st.rerun()

    # =========================
    # ABA 3 - REPOSIÇÕES REGISTRADAS
    # =========================
    with aba_lista:
        st.subheader("Reposições registradas")

        cursor.execute("""
            SELECT
                r.id,
                a.nome,
                r.data_falta,
                r.motivo,
                r.direito_reposicao,
                r.data_reposicao,
                r.status,
                t.dias,
                t.horario
            FROM reposicoes r
            INNER JOIN alunos a
                ON r.aluno_id = a.id
            LEFT JOIN turmas t
                ON r.turma_reposicao_id = t.id
            ORDER BY r.id DESC
        """)

        reposicoes = cursor.fetchall()

        if len(reposicoes) == 0:
            st.info(
                "Nenhuma reposição registrada."
            )

        else:
            for reposicao in reposicoes:
                st.write(
                    f"**{reposicao[1]}**"
                )

                st.write(
                    f"Falta: {reposicao[2]} | "
                    f"Direito: {reposicao[4]} | "
                    f"Status: {reposicao[6]}"
                )

                if reposicao[5]:
                    st.write(
                        f"📅 Reposição: "
                        f"{reposicao[5]}"
                    )

                if reposicao[7]:
                    st.write(
                        f"🏫 Turma: "
                        f"{reposicao[7]} - "
                        f"{reposicao[8]}"
                    )

                if reposicao[3]:
                    st.caption(
                        f"Motivo: {reposicao[3]}"
                    )
                if st.button(
                    "🗑️ Excluir reposição",
                    key=f"excluir_reposicao_{reposicao[0]}"
                ):
                    cursor.execute("""
                        DELETE FROM reposicoes
                        WHERE id = ?
                    """, (
                        reposicao[0],
                    ))

                    conn.commit()

                    st.success(
                        "Reposição excluída com sucesso!"
                    )

                    st.rerun()
                st.divider()
elif menu == "👨‍🏫 Instrutores":
    st.title("Instrutores")

    aba_cadastro, aba_lista, aba_pagamentos = st.tabs(
        [
            "➕ Cadastrar",
            "👨‍🏫 Instrutores cadastrados",
            "💰 Pagamentos"
        ]
    )

    # =========================
    # ABA 1 - CADASTRAR
    # =========================
    with aba_cadastro:
        st.subheader("Cadastrar instrutor")

        nome_instrutor = st.text_input(
            "Nome do instrutor",
            key="instrutor_nome"
        )

        profissao_instrutor = st.text_input(
            "Profissão",
            key="instrutor_profissao"
        )

        percentual_instrutor = st.number_input(
            "Percentual de pagamento (%)",
            min_value=0.0,
            max_value=100.0,
            value=50.0,
            step=1.0,
            key="instrutor_percentual"
        )

        observacao_instrutor = st.text_area(
            "Observação",
            key="instrutor_observacao"
        )

        if st.button(
            "Cadastrar instrutor",
            key="salvar_instrutor"
        ):
            if nome_instrutor.strip() == "":
                st.warning(
                    "Digite o nome do instrutor."
                )

            else:
                cursor.execute("""
                    INSERT INTO instrutores
                    (
                        nome,
                        profissao,
                        percentual,
                        observacao
                    )
                    VALUES (?, ?, ?, ?)
                """, (
                    nome_instrutor,
                    profissao_instrutor,
                    percentual_instrutor,
                    observacao_instrutor
                ))

                conn.commit()

                st.success(
                    "Instrutor cadastrado com sucesso!"
                )

    # =========================
    # ABA 2 - INSTRUTORES CADASTRADOS
    # =========================
    with aba_lista:
        st.subheader("Instrutores cadastrados")

        cursor.execute("""
            SELECT
                id,
                nome,
                profissao,
                percentual,
                observacao
            FROM instrutores
            ORDER BY nome
        """)

        instrutores = cursor.fetchall()

        if len(instrutores) == 0:
            st.info(
                "Nenhum instrutor cadastrado."
            )

        else:
            for instrutor in instrutores:
                st.write(
                    f"**{instrutor[1]}** | "
                    f"{instrutor[2]} | "
                    f"Pagamento: {instrutor[3]:.0f}%"
                )

                if instrutor[4]:
                    st.caption(
                        f"Observação: {instrutor[4]}"
                    )

    # =========================
    # ABA 3 - PAGAMENTOS
    # =========================
    with aba_pagamentos:
        st.subheader("Pagamento dos Instrutores")

        data_inicio = st.date_input(
            "Data inicial",
            key="instrutor_data_inicio"
        )

        data_fim = st.date_input(
            "Data final",
            key="instrutor_data_fim"
        )

        valor_aula_aluno = st.number_input(
            "Valor da aula por aluno",
            min_value=0.0,
            value=18.75,
            step=0.50,
            key="instrutor_valor_aula"
        )

        cursor.execute("""
    SELECT
        i.nome,
        i.percentual,

        (
            SELECT COUNT(*)
            FROM presencas p
            WHERE p.instrutor_aula = i.nome

            AND p.data BETWEEN ? AND ?

            AND (
                p.status = 'Presente'

                OR (
                    p.status = 'Falta'

                    AND NOT EXISTS (
                        SELECT 1
                        FROM reposicoes r
                        WHERE r.aluno_id = p.aluno_id
                        AND r.data_falta = p.data
                        AND r.direito_reposicao = 'Sim'
                        AND r.status IN (
                            'Pendente',
                            'Agendada',
                            'Realizada'
                        )
                    )
                )

                OR p.status = 'Reposição'
            )
        ) AS presencas

    FROM instrutores i

    ORDER BY i.nome
""", (
    str(data_inicio),
    str(data_fim)
))
        pagamentos_instrutores = cursor.fetchall()

        if len(pagamentos_instrutores) == 0:
            st.info(
                "Nenhum instrutor cadastrado."
            )

        else:
            total_geral_instrutores = 0

            for pagamento in pagamentos_instrutores:
                nome = pagamento[0]
                percentual = pagamento[1] or 0
                presencas = pagamento[2] or 0

                valor_por_presenca = (
                    valor_aula_aluno
                    *float(percentual)
                    / 100
                )

                total_instrutor = (
                    presencas
                    * valor_por_presenca
                )

                total_geral_instrutores += total_instrutor

                st.markdown(
                    f"### {nome}"
                )

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Alunos presentes",
                    presencas
                )

                col2.metric(
                    "Valor por presença",
                    f"R$ {valor_por_presenca:.2f}"
                )

                col3.metric(
                    "Total a pagar",
                    f"R$ {total_instrutor:.2f}"
                )

            st.divider()

            st.metric(
                "Total geral dos instrutores",
                f"R$ {total_geral_instrutores:.2f}"
            )
elif menu == "📆 Dias sem aula":
    st.title("Dias sem aula")

    aba_cadastrar, aba_lista = st.tabs(
        ["➕ Cadastrar", "📋 Dias cadastrados"]
    )

    with aba_cadastrar:
        st.subheader("Cadastrar dia sem aula")

        data_sem_aula = st.date_input(
            "Data"
        )

        motivo = st.text_input(
            "Motivo",
            placeholder="Ex.: Feriado"
        )

        observacao = st.text_area(
            "Observação",
            placeholder="Ex.: Estúdio estará fechado."
        )

        if st.button("Salvar dia sem aula"):
            cursor.execute(
                """
                INSERT INTO dias_sem_aula
                (data, motivo, observacao)
                VALUES (?, ?, ?)
                """,
                (
                    str(data_sem_aula),
                    motivo,
                    observacao
                )
            )

            conn.commit()

            st.success("Dia sem aula cadastrado com sucesso!")
            st.rerun()

    with aba_lista:
        cursor.execute(
            """
            SELECT id, data, motivo, observacao
            FROM dias_sem_aula
            ORDER BY data
            """
        )

        dias = cursor.fetchall()

        if not dias:
            st.info("Nenhum dia sem aula cadastrado.")
        else:
            for dia in dias:
                st.write(
                    f"📅 {dia[1]} | "
                    f"{dia[2] or 'Sem motivo informado'}"
                )

                if dia[3]:
                    st.caption(dia[3])

                if st.button(
                    "🗑️ Excluir",
                    key=f"excluir_dia_{dia[0]}"
                ):
                    cursor.execute(
                        "DELETE FROM dias_sem_aula WHERE id = ?",
                        (dia[0],)
                    )
                    conn.commit()
                    st.rerun()

                st.divider()

elif menu == "📊 Relatórios":
    st.title("Relatórios")

    from datetime import date
    import calendar

    hoje = date.today()

    meses = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro"
    ]

    col_mes, col_ano = st.columns(2)

    mes_selecionado = col_mes.selectbox(
        "Mês",
        meses,
        index=hoje.month - 1,
        key="relatorio_mes"
    )

    ano_selecionado = col_ano.number_input(
        "Ano",
        min_value=2025,
        max_value=2100,
        value=hoje.year,
        step=1,
        key="relatorio_ano"
    )

    numero_mes = meses.index(
        mes_selecionado
    ) + 1

    ultimo_dia = calendar.monthrange(
        int(ano_selecionado),
        numero_mes
    )[1]

    data_inicio = (
        f"{int(ano_selecionado)}-"
        f"{numero_mes:02d}-01"
    )

    data_fim = (
        f"{int(ano_selecionado)}-"
        f"{numero_mes:02d}-"
        f"{ultimo_dia:02d}"
    )

    st.caption(
        f"Período: {mes_selecionado} de "
        f"{int(ano_selecionado)}"
    )

    aba_geral, aba_pilates, aba_fisio, aba_despesas = st.tabs(
        [
            "📊 Visão geral",
            "💰 Pilates",
            "🩺 Fisioterapia",
            "💸 Despesas"
        ]
    )

    # =========================
    # CONSULTAS DO MÊS
    # =========================

    cursor.execute("""
        SELECT
            COUNT(*),
            SUM(valor),
            SUM(valor_taxa),
            SUM(valor_liquido)
        FROM financeiro
        WHERE status = 'Pago'
        AND data_pagamento BETWEEN ? AND ?
    """, (
        data_inicio,
        data_fim
    ))

    resumo_pilates = cursor.fetchone()

    qtd_pagamentos = resumo_pilates[0] or 0
    bruto_pilates = resumo_pilates[1] or 0
    taxas_pilates = resumo_pilates[2] or 0
    liquido_pilates = resumo_pilates[3] or 0

    cursor.execute("""
        SELECT
            SUM(valor)
        FROM financeiro
        WHERE status = 'Pendente'
        AND data_pagamento BETWEEN ? AND ?
    """, (
        data_inicio,
        data_fim
    ))

    pendente_pilates = (
        cursor.fetchone()[0] or 0
    )

    cursor.execute("""
        SELECT
            COUNT(*),
            SUM(valor),
            SUM(valor_taxa),
            SUM(valor_liquido)
        FROM fisioterapia
        WHERE data BETWEEN ? AND ?
    """, (
        data_inicio,
        data_fim
    ))

    resumo_fisio = cursor.fetchone()

    qtd_fisio = resumo_fisio[0] or 0
    bruto_fisio = resumo_fisio[1] or 0
    taxas_fisio = resumo_fisio[2] or 0
    liquido_fisio = resumo_fisio[3] or 0

    cursor.execute("""
        SELECT
            COUNT(*),
            SUM(valor)
        FROM despesas
        WHERE data BETWEEN ? AND ?
    """, (
        data_inicio,
        data_fim
    ))

    resumo_despesas = cursor.fetchone()

    qtd_despesas = resumo_despesas[0] or 0
    total_despesas = resumo_despesas[1] or 0

    receita_total = (
        liquido_pilates
        + liquido_fisio
    )

    resultado_mes = (
        receita_total
        - total_despesas
    )

    # =========================
    # ABA 1 - VISÃO GERAL
    # =========================
    with aba_geral:
        st.subheader("Visão geral do mês")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Receita Pilates",
            f"R$ {liquido_pilates:.2f}"
        )

        col2.metric(
            "Receita Fisioterapia",
            f"R$ {liquido_fisio:.2f}"
        )

        col3.metric(
            "Receita total",
            f"R$ {receita_total:.2f}"
        )

        col4, col5, col6 = st.columns(3)

        col4.metric(
            "Despesas",
            f"R$ {total_despesas:.2f}"
        )

        col5.metric(
            "Resultado do mês",
            f"R$ {resultado_mes:.2f}"
        )

        col6.metric(
            "Pagamentos pendentes",
            f"R$ {pendente_pilates:.2f}"
        )

        st.divider()

        col7, col8, col9 = st.columns(3)

        col7.metric(
            "Pagamentos Pilates",
            qtd_pagamentos
        )

        col8.metric(
            "Atendimentos Fisio",
            qtd_fisio
        )

        col9.metric(
            "Despesas registradas",
            qtd_despesas
        )         
        st.divider()
        st.subheader("💳 Recebimentos por forma de pagamento")

        # =========================
        # PILATES POR FORMA
        # =========================
        st.markdown("### Pilates")

        cursor.execute("""
            SELECT
                forma_pagamento,
                COUNT(*),
                SUM(valor),
                SUM(valor_taxa),
                SUM(valor_liquido)
            FROM financeiro
            WHERE status = 'Pago'
            AND data_pagamento BETWEEN ? AND ?
            GROUP BY forma_pagamento
            ORDER BY forma_pagamento
        """, (
            data_inicio,
            data_fim
        ))

        formas_pilates = cursor.fetchall()

        if len(formas_pilates) == 0:
            st.info(
                "Nenhum pagamento de Pilates nesse período."
            )

        else:
            colunas = st.columns(4)

            for indice, item in enumerate(formas_pilates):
                forma = item[0] or "Não informado"
                quantidade = item[1] or 0
                bruto = item[2] or 0
                taxas = item[3] or 0
                liquido = item[4] or 0

                coluna = colunas[indice % 4]

                with coluna:
                    with st.container(border=True):
                        st.markdown(
                            f"### {forma}"
                        )

                        st.write(
                            f"**Pagamentos:** {quantidade}"
                        )

                        st.write(
                            f"**Bruto:** R$ {bruto:.2f}"
                        )

                        st.write(
                            f"**Taxas:** R$ {taxas:.2f}"
                        )

                        st.write(
                            f"**Líquido:** R$ {liquido:.2f}"
                        )

        st.divider()

        # =========================
        # FISIOTERAPIA POR FORMA
        # =========================
        st.markdown("### Fisioterapia")

        cursor.execute("""
            SELECT
                forma_pagamento,
                COUNT(*),
                SUM(valor),
                SUM(valor_taxa),
                SUM(valor_liquido)
            FROM fisioterapia
            WHERE data BETWEEN ? AND ?
            GROUP BY forma_pagamento
            ORDER BY forma_pagamento
        """, (
            data_inicio,
            data_fim
        ))

        formas_fisio = cursor.fetchall()

        if len(formas_fisio) == 0:
            st.info(
                "Nenhum pagamento de Fisioterapia nesse período."
            )

        else:
            colunas = st.columns(4)

            for indice, item in enumerate(formas_fisio):
                forma = item[0] or "Não informado"
                quantidade = item[1] or 0
                bruto = item[2] or 0
                taxas = item[3] or 0
                liquido = item[4] or 0

                coluna = colunas[indice % 4]

                with coluna:
                    with st.container(border=True):
                        st.markdown(
                            f"### {forma}"
                        )

                        st.write(
                            f"**Atendimentos:** {quantidade}"
                        )

                        st.write(
                            f"**Bruto:** R$ {bruto:.2f}"
                        )

                        st.write(
                            f"**Taxas:** R$ {taxas:.2f}"
                        )

                        st.write(
                            f"**Líquido:** R$ {liquido:.2f}"
                        )

    # =========================
    # ABA 2 - PILATES
    # =========================
    with aba_pilates:
        st.subheader("Financeiro do Pilates")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Bruto",
            f"R$ {bruto_pilates:.2f}"
        )

        col2.metric(
            "Taxas",
            f"R$ {taxas_pilates:.2f}"
        )

        col3.metric(
            "Líquido",
            f"R$ {liquido_pilates:.2f}"
        )

        col4.metric(
            "Pendente",
            f"R$ {pendente_pilates:.2f}"
        )

        st.divider()

        # =========================
        # RESUMO POR FORMA DE PAGAMENTO
        # =========================
        st.subheader(
            "💳 Recebimentos por forma de pagamento"
        )

        cursor.execute("""
            SELECT
                forma_pagamento,
                COUNT(*),
                SUM(valor),
                SUM(valor_taxa),
                SUM(valor_liquido)
            FROM financeiro
            WHERE status = 'Pago'
            AND data_pagamento BETWEEN ? AND ?
            GROUP BY forma_pagamento
            ORDER BY forma_pagamento
        """, (
            data_inicio,
            data_fim
        ))

        pagamentos_por_forma = cursor.fetchall()

        if len(pagamentos_por_forma) == 0:
            st.info(
                "Nenhum pagamento recebido nesse período."
            )

        else:
            colunas_formas = st.columns(4)

            for indice, forma in enumerate(
                pagamentos_por_forma
            ):
                forma_pagamento = (
                    forma[0]
                    or "Não informado"
                )

                quantidade = forma[1] or 0
                bruto = forma[2] or 0
                taxas = forma[3] or 0
                liquido = forma[4] or 0

                coluna = colunas_formas[
                    indice % 4
                ]

                with coluna:
                    with st.container(
                        border=True
                    ):
                        st.markdown(
                            f"### {forma_pagamento}"
                        )

                        st.metric(
                            "Pagamentos",
                            quantidade
                        )

                        st.write(
                            f"**Bruto:** "
                            f"R$ {bruto:.2f}"
                        )

                        st.write(
                            f"**Taxas:** "
                            f"R$ {taxas:.2f}"
                        )

                        st.write(
                            f"**Líquido:** "
                            f"R$ {liquido:.2f}"
                        )

        st.divider()
        st.subheader("Pagamentos do período")

        cursor.execute("""
            SELECT
                a.nome,
                f.valor,
                f.valor_taxa,
                f.valor_liquido,
                f.data_pagamento,
                f.forma_pagamento,
                f.status,
                f.plano
            FROM financeiro f
            INNER JOIN alunos a
                ON f.aluno_id = a.id
            WHERE f.data_pagamento
            BETWEEN ? AND ?
            ORDER BY f.data_pagamento DESC
        """, (
            data_inicio,
            data_fim
        ))

        pagamentos_mes = cursor.fetchall()

        if len(pagamentos_mes) == 0:
            st.info(
                "Nenhum pagamento nesse período."
            )

        else:
            for pagamento in pagamentos_mes:
                plano = (
                    pagamento[7]
                    or "Não informado"
                )

                st.write(
                    f"**{pagamento[0]}** | "
                    f"{plano} | "
                    f"R$ {pagamento[1]:.2f} | "
                    f"Líquido: R$ {(pagamento[3] or 0):.2f} | "
                    f"{pagamento[4]} | "
                    f"{pagamento[5]} | "
                    f"{pagamento[6]}"
                )

    # =========================
    # ABA 3 - FISIOTERAPIA
    # =========================
    with aba_fisio:
        st.subheader(
            "Relatório de Fisioterapia"
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Atendimentos",
            qtd_fisio
        )

        col2.metric(
            "Bruto",
            f"R$ {bruto_fisio:.2f}"
        )

        col3.metric(
            "Taxas",
            f"R$ {taxas_fisio:.2f}"
        )

        col4.metric(
            "Líquido",
            f"R$ {liquido_fisio:.2f}"
        )

        st.divider()
        st.subheader(
            "Atendimentos do período"
        )

        cursor.execute("""
            SELECT
                paciente,
                data,
                valor,
                valor_liquido,
                forma_pagamento,
                profissional
            FROM fisioterapia
            WHERE data BETWEEN ? AND ?
            ORDER BY data DESC
        """, (
            data_inicio,
            data_fim
        ))

        fisio_mes = cursor.fetchall()

        if len(fisio_mes) == 0:
            st.info(
                "Nenhum atendimento nesse período."
            )

        else:
            for atendimento in fisio_mes:
                st.write(
                    f"**{atendimento[0]}** | "
                    f"{atendimento[1]} | "
                    f"R$ {atendimento[2]:.2f} | "
                    f"Líquido: R$ {(atendimento[3] or 0):.2f} | "
                    f"{atendimento[4]} | "
                    f"{atendimento[5]}"
                )

    # =========================
    # ABA 4 - DESPESAS
    # =========================
    with aba_despesas:
        st.subheader(
            "Relatório de Despesas"
        )

        col1, col2 = st.columns(2)

        col1.metric(
            "Quantidade de despesas",
            qtd_despesas
        )

        col2.metric(
            "Total de despesas",
            f"R$ {total_despesas:.2f}"
        )

        st.divider()
        st.subheader(
            "Despesas do período"
        )

        cursor.execute("""
            SELECT
                descricao,
                categoria,
                valor,
                data,
                forma_pagamento
            FROM despesas
            WHERE data BETWEEN ? AND ?
            ORDER BY data DESC
        """, (
            data_inicio,
            data_fim
        ))

        despesas_mes = cursor.fetchall()

        if len(despesas_mes) == 0:
            st.info(
                "Nenhuma despesa nesse período."
            )

        else:
            for despesa in despesas_mes:
                st.write(
                    f"**{despesa[0]}** | "
                    f"{despesa[1]} | "
                    f"R$ {despesa[2]:.2f} | "
                    f"{despesa[3]} | "
                    f"{despesa[4]}"
                )