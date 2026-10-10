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
conn = pg8000.dbapi.connect(
    host=postgres["host"],
    port=int(postgres["port"]),
    database=postgres["dbname"],
    user=postgres["user"],
    password=postgres["password"],
    ssl_context=ssl_context
)

class CursorCompat:
    def __init__(self, cursor):
        self.cursor = cursor

    def execute(self, sql, params=None):
        sql = sql.replace("?", "%s")

        if params is None:
            return self.cursor.execute(sql)

        return self.cursor.execute(sql, params)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()


cursor = CursorCompat(conn.cursor())

st.set_page_config(
    page_title="Studio de Pilates",
    page_icon="🧘",
    layout="wide"
)
# =========================
# LOGIN COM GOOGLE
# =========================

if not st.user.is_logged_in:
    st.title("Acesso ao sistema")
    st.write("Entre com sua conta Google para acessar.")

    if st.button("🔐 Entrar com Google"):
        st.login()

    st.stop()

st.markdown("""
<style>
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

/* ALERTAS */
[data-testid="stAlert"] {
    border-radius: 12px;
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

        data_atual += timedelta(days=1)# =========================
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

for opcao in opcoes_menu:

    if opcao == st.session_state.menu_ativo:
        tipo_botao = "primary"
    else:
        tipo_botao = "secondary"

    if st.sidebar.button(
        opcao,
        key=f"menu_{opcao}",
        use_container_width=True,
        type=tipo_botao
    ):
        st.session_state.menu_ativo = opcao
        st.rerun()
st.sidebar.divider()

if st.sidebar.button("🚪 Sair", use_container_width=True):
    st.logout()

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
    # FINANCEIRO
    # =========================

    st.subheader("Financeiro do mês")

    col5, col6, col7 = st.columns(3)

    col5.metric(
        "💰 Receita Pilates",
        f"R$ {receita_pilates:.2f}"
    )

    col6.metric(
        "🩺 Receita Fisioterapia",
        f"R$ {receita_fisio:.2f}"
    )

    col7.metric(
        "💵 Receita total",
        f"R$ {receita_total:.2f}"
    )

    col8, col9, col10 = st.columns(3)

    col8.metric(
        "💸 Despesas",
        f"R$ {despesas_mes:.2f}"
    )

    col9.metric(
        "📈 Resultado",
        f"R$ {resultado_mes:.2f}"
    )

    col10.metric(
        "⏳ Pendentes",
        f"R$ {pagamentos_pendentes:.2f}"
    )

    st.divider()

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
            COUNT(a.id)
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
        for turma in ocupacao_turmas:
            dias = turma[1]
            horario = turma[2]
            limite = turma[3] or 0
            ocupados = turma[4] or 0

            vagas = limite - ocupados

            if vagas < 0:
                vagas = 0

            percentual = 0

            if limite > 0:
                percentual = ocupados / limite

            col_turma, col_vagas = st.columns(
                [4, 1]
            )

            with col_turma:
                st.markdown(
                    f"**{dias} - {horario}**"
                )

                st.progress(
                    min(percentual, 1.0)
                )

            with col_vagas:
                st.metric(
                    "Vagas",
                    vagas
                )

            st.caption(
                f"{ocupados} de {limite} alunos cadastrados"
            )

            st.divider()

elif menu == "👥 Alunos":
    st.title("Alunos")

    aba_cadastro, aba_lista, aba_edicao = st.tabs(
        [
            "➕ Cadastrar",
            "👥 Alunos cadastrados",
            "✏️ Editar / Excluir"
        ]
    )

    # =========================
    # ABA 1 - CADASTRAR
    # =========================
    with aba_cadastro:
        st.subheader("Cadastrar aluno")

        nome = st.text_input(
            "Nome do aluno",
            key="cadastro_nome"
        )

        telefone = st.text_input(
            "Telefone",
            key="cadastro_telefone"
        )

        cpf = st.text_input(
            "CPF",
            key="cadastro_cpf"
        )

        endereco = st.text_input(
            "Endereço",
            key="cadastro_endereco"
        )

        data_nascimento = st.text_input(
            "Data de nascimento",
            placeholder="DD/MM/AAAA",
            key="cadastro_nascimento"
        )

        tabela_preco = st.selectbox(
            "Tabela de preço",
            [
                "Antigo",
                "Novo"
            ],
            key="cadastro_tabela"
        )

        cursor.execute("""
            SELECT id, dias, horario
            FROM turmas
            ORDER BY dias, horario
        """)

        turmas_cadastradas = cursor.fetchall()

        if len(turmas_cadastradas) == 0:
            st.warning(
                "Cadastre uma turma antes de cadastrar alunos."
            )

            turma = None
            turma_id = None

        else:
            opcoes_turmas = {
                f"{t[1]} - {t[2]}": t[0]
                for t in turmas_cadastradas
            }

            turma = st.selectbox(
                "Turma",
                list(opcoes_turmas.keys()),
                key="cadastro_turma"
            )

            turma_id = opcoes_turmas[turma]

        if st.button(
            "Cadastrar aluno",
            key="botao_cadastrar_aluno"
        ):
            if nome.strip() == "":
                st.warning(
                    "Digite o nome do aluno."
                )

            elif turma_id is None:
                st.warning(
                    "Selecione uma turma."
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

            aluno_selecionado = st.selectbox(
                "Selecione o aluno",
                list(opcoes_edicao.keys()),
                key="aluno_edicao"
            )

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
                key="editar_nome"
            )

            novo_telefone = st.text_input(
                "Telefone",
                value=dados_aluno[1] or "",
                key="editar_telefone"
            )

            novo_cpf = st.text_input(
                "CPF",
                value=dados_aluno[2] or "",
                key="editar_cpf"
            )

            novo_endereco = st.text_input(
                "Endereço",
                value=dados_aluno[3] or "",
                key="editar_endereco"
            )

            nova_data_nascimento = st.text_input(
                "Data de nascimento",
                value=dados_aluno[4] or "",
                placeholder="DD/MM/AAAA",
                key="editar_nascimento"
            )

            opcoes_tabela = [
                "Antigo",
                "Novo"
            ]

            tabela_atual = dados_aluno[7]

            if tabela_atual in opcoes_tabela:
                indice_tabela = opcoes_tabela.index(
                    tabela_atual
                )
            else:
                indice_tabela = 0

            nova_tabela_preco = st.selectbox(
                "Tabela de preço",
                opcoes_tabela,
                index=indice_tabela,
                key="editar_tabela_preco"
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
                    indice_turma = nomes_turmas.index(
                        turma_atual
                    )
                else:
                    indice_turma = 0

                nova_turma = st.selectbox(
                    "Turma",
                    nomes_turmas,
                    index=indice_turma,
                    key="editar_turma"
                )

                nova_turma_id = opcoes_turmas_edicao[
                    nova_turma
                ]

                col_editar, col_excluir = st.columns(2)

                if col_editar.button(
                    "Salvar alterações",
                    key="salvar_edicao_aluno"
                ):
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
                    key="excluir_aluno"
                ):
                    cursor.execute(
                        "DELETE FROM alunos WHERE id = ?",
                        (
                            aluno_id_edicao,
                        )
                    )

                    conn.commit()

                    st.success(
                        "Aluno excluído com sucesso!"
                    )
elif menu == "📅 Turmas":
    st.title("Turmas")

    aba_cadastro, aba_lista, aba_edicao = st.tabs(
        [
            "➕ Cadastrar",
            "📋 Turmas cadastradas",
            "✏️ Editar / Excluir"
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
                key="editar_dias_turma"
            )

            novo_horario = st.text_input(
                "Horário",
                value=dados_turma[1] or "",
                key="editar_horario_turma"
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
                    key="editar_instrutor_turma"
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
                key="editar_limite_turma"
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

        cursor.execute("""
            SELECT id, dias, horario
            FROM turmas
            ORDER BY dias, horario
        """)

        turmas_presenca = cursor.fetchall()

        if len(turmas_presenca) == 0:
            st.info(
                "Nenhuma turma cadastrada."
            )

        else:
            opcoes_turmas = {
                f"{t[1]} - {t[2]}": t[0]
                for t in turmas_presenca
            }

            turma_escolhida = st.selectbox(
                "Escolha a turma",
                list(opcoes_turmas.keys()),
                key="presenca_turma"
            )

            turma_id_presenca = opcoes_turmas[
                turma_escolhida
            ]

            data_aula = st.date_input(
                "Data da aula",
                key="presenca_data"
            )

            cursor.execute("""
                SELECT id, nome
                FROM alunos
                WHERE turma_id = ?
                ORDER BY nome
            """, (
                turma_id_presenca,
            ))

            alunos_turma = cursor.fetchall()

            if len(alunos_turma) == 0:
                st.warning(
                    "Não há alunos cadastrados nessa turma."
                )

            else:
                st.subheader("Alunos")

                presencas_marcadas = []

                for aluno in alunos_turma:
                    aluno_id = aluno[0]
                    aluno_nome = aluno[1]

                    status = st.radio(
                        aluno_nome,
                        [
                            "Presente",
                            "Falta"
                        ],
                        horizontal=True,
                        key=f"presenca_{aluno_id}"
                    )

                    presencas_marcadas.append(
                        (
                            aluno_id,
                            turma_id_presenca,
                            str(data_aula),
                            status
                        )
                    )

                if st.button(
                    "Salvar chamada",
                    key="salvar_chamada"
                ):
                    for presenca in presencas_marcadas:
                        aluno_id = presenca[0]
                        turma_id = presenca[1]
                        data = presenca[2]
                        status = presenca[3]

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
                                SET status = ?
                                WHERE id = ?
                            """, (
                                status,
                                presenca_existente[0]
                            ))

                        else:
                            cursor.execute("""
                                INSERT INTO presencas
                                (
                                    aluno_id,
                                    turma_id,
                                    data,
                                    status
                                )
                                VALUES (?, ?, ?, ?)
                            """, (
                                aluno_id,
                                turma_id,
                                data,
                                status
                            ))

                    conn.commit()

                    st.success(
                        "Chamada salva com sucesso!"
                    )

    # =========================
    # ABA 2 - HISTÓRICO
    # =========================
    with aba_historico:
        st.subheader("Histórico de presenças")

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

        historico_presencas = cursor.fetchall()

        if len(historico_presencas) == 0:
            st.info(
                "Nenhuma presença registrada."
            )

        else:
            for registro in historico_presencas:
                st.write(
                    f"**{registro[1]}** | "
                    f"{registro[2]} - {registro[3]} | "
                    f"{registro[4]} | "
                    f"{registro[5]}"
                )
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
                opcoes_alunos[aluno_escolhido]["id"]
            )

            tabela_aluno = (
                opcoes_alunos[aluno_escolhido]["tabela_preco"]
            )

            if tabela_aluno not in ["Antigo", "Novo"]:
                tabela_aluno = "Antigo"

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
                data_pagamento,
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
                tabela_usada = tabela_aluno

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

            if forma_pagamento in ["Débito", "Crédito"]:
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

            valor_taxa = valor * (
                taxa_percentual / 100
            )

            valor_liquido = (
                valor - valor_taxa
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
                        forma_pagamento,
                        status,
                        taxa_percentual,
                        valor_taxa,
                        valor_liquido,
                        plano
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    aluno_id_financeiro,
                    valor,
                    str(data_pagamento),
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
            if pagamento[5] == "Pago":
                total_recebido += pagamento[2]
                total_taxas += pagamento[6] or 0
                total_liquido += pagamento[7] or 0

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
                    pagamento[8]
                    or "Não informado"
                )

                st.write(
                    f"**{pagamento[1]}** | "
                    f"Plano: {plano_historico} | "
                    f"Bruto: R$ {pagamento[2]:.2f} | "
                    f"Taxa: R$ {(pagamento[6] or 0):.2f} | "
                    f"Líquido: R$ {(pagamento[7] or 0):.2f} | "
                    f"{pagamento[3]} | "
                    f"{pagamento[4]} | "
                    f"{pagamento[5]}"
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
                f"ID {l[0]} - {l[1]} - R$ {l[2]:.2f}": l[0]
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
                key="editar_valor_financeiro"
            )

            planos_edicao = [
                "8 aulas",
                "24 aulas"
            ]

            plano_atual = dados_financeiro[4]

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
                key="editar_plano_financeiro"
            )

            formas_pagamento = [
                "PIX",
                "Dinheiro",
                "Débito",
                "Crédito"
            ]

            forma_atual = dados_financeiro[1]

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
                key="editar_forma_financeiro"
            )

            status_opcoes = [
                "Pago",
                "Pendente"
            ]

            status_atual = dados_financeiro[2]

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
                key="editar_status_financeiro"
            )

            if nova_forma in ["Débito", "Crédito"]:
                nova_taxa = st.number_input(
                    "Taxa do cartão (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(
                        dados_financeiro[3] or 0
                    ),
                    key="editar_taxa_financeiro"
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
                key="salvar_financeiro"
            ):
                cursor.execute("""
                    UPDATE financeiro
                    SET
                        valor = ?,
                        forma_pagamento = ?,
                        status = ?,
                        taxa_percentual = ?,
                        valor_taxa = ?,
                        valor_liquido = ?,
                        plano = ?
                    WHERE id = ?
                """, (
                    novo_valor,
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
                key="excluir_financeiro"
            ):
                cursor.execute(
                    "DELETE FROM financeiro WHERE id = ?",
                    (
                        lancamento_id,
                    )
                )

                conn.commit()

                st.success(
                    "Lançamento excluído com sucesso!"
                )
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

        paciente = st.text_input(
            "Nome do paciente",
            key="fisio_paciente"
        )

        data_atendimento = st.date_input(
            "Data do atendimento",
            key="fisio_data"
        )

        valor_fisio = st.number_input(
            "Valor do atendimento",
            min_value=0.0,
            value=70.0,
            step=10.0,
            key="fisio_valor"
        )

        forma_pagamento_fisio = st.selectbox(
            "Forma de pagamento",
            [
                "PIX",
                "Dinheiro",
                "Débito",
                "Crédito"
            ],
            key="fisio_pagamento"
        )

        if forma_pagamento_fisio in ["Débito", "Crédito"]:
            taxa_fisio = st.number_input(
                "Taxa do cartão (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                key="fisio_taxa"
            )
        else:
            taxa_fisio = 0.0

        valor_taxa_fisio = (
            valor_fisio * taxa_fisio / 100
        )

        valor_liquido_fisio = (
            valor_fisio - valor_taxa_fisio
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
            key="fisio_profissional"
        )

        observacao_fisio = st.text_area(
            "Observação",
            key="fisio_observacao"
        )

        if st.button(
            "Salvar atendimento",
            key="salvar_atendimento_fisio"
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

                st.success(
                    "Atendimento salvo com sucesso!"
                )

    # =========================
    # ABA 2 - RESUMO
    # =========================
    with aba_resumo:
        st.subheader(
            "Resumo financeiro da Fisioterapia"
        )

        cursor.execute("""
            SELECT
                COUNT(*),
                SUM(valor),
                SUM(valor_taxa),
                SUM(valor_liquido)
            FROM fisioterapia
        """)

        resumo_fisio = cursor.fetchone()

        quantidade_atendimentos = (
            resumo_fisio[0] or 0
        )

        total_bruto_fisio = (
            resumo_fisio[1] or 0
        )

        total_taxas_fisio = (
            resumo_fisio[2] or 0
        )

        total_liquido_fisio = (
            resumo_fisio[3] or 0
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Atendimentos",
            quantidade_atendimentos
        )

        col2.metric(
            "Total bruto",
            f"R$ {total_bruto_fisio:.2f}"
        )

        col3.metric(
            "Taxas",
            f"R$ {total_taxas_fisio:.2f}"
        )

        col4.metric(
            "Total líquido",
            f"R$ {total_liquido_fisio:.2f}"
        )

        st.divider()
        st.subheader("Atendimentos registrados")

        cursor.execute("""
            SELECT
                paciente,
                data,
                valor,
                forma_pagamento,
                valor_taxa,
                valor_liquido,
                profissional,
                observacao
            FROM fisioterapia
            ORDER BY id DESC
        """)

        atendimentos = cursor.fetchall()

        if len(atendimentos) == 0:
            st.info(
                "Nenhum atendimento registrado."
            )

        else:
            for atendimento in atendimentos:
                st.write(
                    f"**{atendimento[0]}** | "
                    f"{atendimento[1]} | "
                    f"Bruto: R$ {atendimento[2]:.2f} | "
                    f"Taxa: R$ {(atendimento[4] or 0):.2f} | "
                    f"Líquido: R$ {(atendimento[5] or 0):.2f} | "
                    f"{atendimento[3]} | "
                    f"Profissional: {atendimento[6]}"
                )

                if atendimento[7]:
                    st.caption(
                        f"Observação: {atendimento[7]}"
                    )

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
                key="editar_paciente_fisio"
            )

            novo_valor_fisio = st.number_input(
                "Valor do atendimento",
                min_value=0.0,
                value=float(
                    dados_atendimento[1] or 0
                ),
                key="editar_valor_fisio"
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
                key="editar_forma_fisio"
            )

            if nova_forma_fisio in ["Débito", "Crédito"]:
                nova_taxa_fisio = st.number_input(
                    "Taxa do cartão (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(
                        dados_atendimento[3] or 0
                    ),
                    key="editar_taxa_fisio"
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
                key="editar_profissional_fisio"
            )

            nova_observacao_fisio = st.text_area(
                "Observação",
                value=dados_atendimento[5] or "",
                key="editar_observacao_fisio"
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
                key="salvar_edicao_fisio"
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
                key="excluir_fisio"
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

    aba_registro, aba_lista = st.tabs(
        [
            "➕ Registrar reposição",
            "📋 Reposições registradas"
        ]
    )

    # =========================
    # ABA 1 - REGISTRAR
    # =========================
    with aba_registro:
        st.subheader("Registrar reposição")

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
                aluno[1]: aluno[0]
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

            data_reposicao = st.date_input(
                "Data da reposição",
                key="reposicao_data"
            )

            status_reposicao = st.selectbox(
                "Status",
                [
                    "Pendente",
                    "Realizada"
                ],
                key="reposicao_status"
            )

            if st.button(
                "Salvar reposição",
                key="salvar_reposicao"
            ):
                cursor.execute("""
                    INSERT INTO reposicoes
                    (
                        aluno_id,
                        data_falta,
                        motivo,
                        direito_reposicao,
                        data_reposicao,
                        status
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    aluno_id_reposicao,
                    str(data_falta),
                    motivo,
                    direito_reposicao,
                    str(data_reposicao),
                    status_reposicao
                ))

                conn.commit()

                st.success(
                    "Reposição salva com sucesso!"
                )

    # =========================
    # ABA 2 - REPOSIÇÕES REGISTRADAS
    # =========================
    with aba_lista:
        st.subheader("Reposições registradas")

        cursor.execute("""
            SELECT
                reposicoes.id,
                alunos.nome,
                reposicoes.data_falta,
                reposicoes.motivo,
                reposicoes.direito_reposicao,
                reposicoes.data_reposicao,
                reposicoes.status
            FROM reposicoes
            INNER JOIN alunos
                ON reposicoes.aluno_id = alunos.id
            ORDER BY reposicoes.id DESC
        """)

        reposicoes = cursor.fetchall()

        if len(reposicoes) == 0:
            st.info(
                "Nenhuma reposição registrada."
            )

        else:
            for reposicao in reposicoes:
                st.write(
                    f"**{reposicao[1]}** | "
                    f"Falta: {reposicao[2]} | "
                    f"Direito: {reposicao[4]} | "
                    f"Reposição: {reposicao[5]} | "
                    f"Status: {reposicao[6]}"
                )

                if reposicao[3]:
                    st.caption(
                        f"Motivo: {reposicao[3]}"
                    )
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
                COUNT(p.id) AS presencas
            FROM instrutores i
            LEFT JOIN turmas t
                ON t.instrutor = i.nome
            LEFT JOIN presencas p
                ON p.turma_id = t.id
                AND p.status = 'Presente'
                AND p.data BETWEEN ? AND ?
            GROUP BY
                i.id,
                i.nome,
                i.percentual
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
                    * percentual
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