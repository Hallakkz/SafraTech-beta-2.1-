import streamlit as st
import pandas as pd
import requests


st.set_page_config(page_title="SafraTech IA", page_icon="🌱", layout="wide")

# -------------------------
# ESTILO VISUAL
# -------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Fundo geral */
.stApp {
    background: linear-gradient(135deg, #0a1a0f 0%, #0d2218 50%, #0a1a0f 100%);
    color: #e8f5e9;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071510 0%, #0d2218 100%) !important;
    border-right: 1px solid #1a4a2a;
}
[data-testid="stSidebar"] * {
    color: #c8e6c9 !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stNumberInput label {
    color: #81c784 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 500;
}

/* Título principal */
h1 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 2.4rem !important;
    background: linear-gradient(90deg, #69f0ae, #b9f6ca);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.02em;
    padding-bottom: 0.5rem;
}

/* Headers */
h2, h3 {
    font-family: 'Syne', sans-serif !important;
    color: #a5d6a7 !important;
    font-weight: 700 !important;
}

/* Cards de métrica */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #0d2a1a, #133d26);
    border: 1px solid #1e5c35;
    border-radius: 16px;
    padding: 1.2rem 1.4rem !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(105,240,174,0.08);
    transition: transform 0.2s, box-shadow 0.2s;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.5), inset 0 1px 0 rgba(105,240,174,0.12);
}
[data-testid="stMetricLabel"] {
    color: #81c784 !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-weight: 500 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    color: #69f0ae !important;
    font-size: 1.9rem !important;
    font-weight: 700 !important;
}

/* Botões */
.stButton > button {
    background: linear-gradient(135deg, #1b5e20, #2e7d32) !important;
    color: #b9f6ca !important;
    border: 1px solid #388e3c !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em;
    padding: 0.6rem 2rem !important;
    transition: all 0.2s !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.3) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2e7d32, #388e3c) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(56,142,60,0.4) !important;
}

/* Selectbox e inputs */
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background: #0d2218 !important;
    border: 1px solid #1e5c35 !important;
    border-radius: 10px !important;
    color: #c8e6c9 !important;
}

/* Alertas */
.stSuccess {
    background: rgba(27, 94, 32, 0.3) !important;
    border: 1px solid #2e7d32 !important;
    border-radius: 10px !important;
    color: #c8e6c9 !important;
}
.stError {
    background: rgba(183, 28, 28, 0.25) !important;
    border: 1px solid #c62828 !important;
    border-radius: 10px !important;
}
.stWarning {
    background: rgba(230, 81, 0, 0.2) !important;
    border: 1px solid #bf360c !important;
    border-radius: 10px !important;
}

/* Divider */
hr {
    border-color: #1a4a2a !important;
    margin: 1.5rem 0 !important;
}

/* Caption / footer */
.stCaption {
    color: #4caf50 !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.05em;
}

/* Radio buttons na sidebar */
[data-testid="stSidebar"] .stRadio > div {
    gap: 0.3rem;
}
[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,0.03);
    border: 1px solid #1a4a2a;
    border-radius: 8px;
    padding: 0.4rem 0.8rem !important;
    transition: all 0.15s;
    text-transform: none !important;
    letter-spacing: normal !important;
    font-size: 0.85rem !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    border-color: #388e3c;
    background: rgba(56,142,60,0.1);
}

/* Header badge */
.header-badge {
    display: inline-block;
    background: linear-gradient(135deg, #1b5e20, #2e7d32);
    color: #b9f6ca;
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    border: 1px solid #388e3c;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

texts = {
    "Português": {
        "title": "🌱 SafraTech IA - Gestão de Precisão",
        "nav": "Navegação:",
        "menu": ["Recomendação", "Diagnóstico Agrícola", "🐂 Pecuária", "💬 Assistente"],
        "sidebar_cfg": "Configurações",
        "crop_label": "Cultura Alvo:",
        "area_label": "Área (Acres):",
        "rec_header": "📌 Necessidade Nutricional Estimada",
        "diag_header": "🩺 Diagnóstico de Saúde do Solo",
        "soil_label": "Tipo de Solo:",
        "btn_diag": "Gerar Relatório",
        "missing": "Faltando",
        "excess": "Excesso de",
        "adequate": "Nível adequado",
        "ideal_unit": "Kg",
        "footer": "A SafraTech IA não é humana. Pode cometer erros.",
        "nutrients": ["Nitrogênio", "Fósforo", "Potássio"],
        "no_data": "Dados insuficientes para",
        "pec_header": "🐂 Análise de Saúde do Rebanho",
        "pec_race": "Raça:",
        "pec_sex": "Sexo:",
        "pec_age": "Idade (meses):",
        "pec_weight": "Peso atual (Kg):",
        "pec_system": "Sistema de criação:",
        "pec_systems": ["Pasto", "Semi-confinamento", "Confinamento"],
        "pec_btn": "Analisar Animal",
        "pec_expected": "Peso esperado para a idade",
        "pec_score": "Escore corporal",
        "pec_gain": "Ganho diário médio (Kg/dia)",
        "pec_status": "Situação",
        "pec_status_map": {
            "abaixo_peso": "⚠️ Abaixo do Peso",
            "saudavel": "✅ Saudável",
            "acima_peso": "📈 Acima da Média",
        },
        "pec_no_data": "Nenhum dado encontrado para essa raça/sexo/idade no banco de dados.",
        "pec_potential": "Potencial de ganho",
        "crops": {
            "Arroz": "Arroz", "Milho": "Milho", "Feijão": "Feijão",
            "Algodão": "Algodão", "Soja": "Soja",
        },
        "soils": {
            "Sandy": "Arenoso", "Loamy": "Franco", "Black": "Preto",
            "Red": "Vermelho", "Clayey": "Argiloso",
        },
    },
    "English": {
        "title": "🌱 SafraTech AI - Precision Management",
        "nav": "Navigation:",
        "menu": ["Recommendation", "Agricultural Diagnosis", "🐂 Livestock", "💬 Assistant"],
        "sidebar_cfg": "Settings",
        "crop_label": "Target Crop:",
        "area_label": "Area (Acres):",
        "rec_header": "📌 Estimated Nutritional Need",
        "diag_header": "🩺 Soil Health Diagnosis",
        "soil_label": "Soil Type:",
        "btn_diag": "Generate Report",
        "missing": "Missing",
        "excess": "Excess of",
        "adequate": "Adequate level",
        "ideal_unit": "Kg",
        "footer": "SafraTech AI is not human. It can make mistakes.",
        "nutrients": ["Nitrogen", "Phosphorus", "Potassium"],
        "no_data": "Insufficient data for",
        "pec_header": "🐂 Herd Health Analysis",
        "pec_race": "Breed:",
        "pec_sex": "Sex:",
        "pec_age": "Age (months):",
        "pec_weight": "Current Weight (Kg):",
        "pec_system": "Raising system:",
        "pec_systems": ["Pasture", "Semi-feedlot", "Feedlot"],
        "pec_btn": "Analyze Animal",
        "pec_expected": "Expected weight for age",
        "pec_score": "Body score",
        "pec_gain": "Average daily gain (Kg/day)",
        "pec_status": "Status",
        "pec_status_map": {
            "abaixo_peso": "⚠️ Underweight",
            "saudavel": "✅ Healthy",
            "acima_peso": "📈 Above Average",
        },
        "pec_no_data": "No data found for this breed/sex/age in the database.",
        "pec_potential": "Growth potential",
        "crops": {
            "Arroz": "Rice", "Milho": "Corn", "Feijão": "Kidney Beans",
            "Algodão": "Cotton", "Soja": "Soybean",
        },
        "soils": {
            "Sandy": "Sandy", "Loamy": "Loamy", "Black": "Black",
            "Red": "Red", "Clayey": "Clayey",
        },
    },
}

# -------------------------
# CARREGAMENTO SEGURO
# -------------------------
@st.cache_data
def load_data():
    map_intern = {
        "rice": "Arroz", "maize": "Milho",
        "kidneybeans": "Feijão", "cotton": "Algodão",
        "soybean": "Soja",
    }

    try:
        df = pd.read_csv("Safratech_crop_recommendation.csv")
        df.columns = [c.strip() for c in df.columns]
        df["label"] = df["label"].str.strip().str.lower().replace(map_intern)
    except Exception:
        df = pd.DataFrame({"label": ["Arroz"], "N": [80], "P": [40], "K": [40]})

    # Tipos de solo fixos — não depende do CSV para não quebrar a tradução
    SOILS = ["Sandy", "Loamy", "Black", "Red", "Clayey"]

    try:
        df2 = pd.read_csv("data_core.csv")
        df2.columns = [c.strip() for c in df2.columns]
        # Descobre coluna de solo (aceita "Solo", "Soil", primeira coluna)
        soil_col = next(
            (c for c in df2.columns if c.lower() in ("solo", "soil")),
            df2.columns[0],
        )
        df2 = df2.rename(columns={soil_col: "Solo"})
        # Garante que só apareçam valores mapeáveis
        valid = df2["Solo"].isin(SOILS)
        if valid.any():
            soils_available = sorted(df2.loc[valid, "Solo"].unique().tolist())
        else:
            soils_available = SOILS
    except Exception:
        soils_available = SOILS

    return df, soils_available


@st.cache_data
def load_pecuaria():
    try:
        df_pec = pd.read_csv("safratech ia pecuaria.csv")
        df_pec.columns = [c.strip().lower().replace(" ", "_") for c in df_pec.columns]
        df_pec["raca"] = df_pec["raca"].str.strip().str.lower()
        df_pec["sexo"] = df_pec["sexo"].str.strip().str.lower()
        df_pec["situacao"] = df_pec["situacao"].str.strip().str.lower()
    except Exception:
        df_pec = pd.DataFrame({
            "raca": ["nelore"], "sexo": ["macho"], "idade_meses": [24],
            "peso_kg": [420], "escore_corporal": [6.0],
            "ganho_diario_kg": [0.6], "situacao": ["saudavel"],
        })
    return df_pec


df, soils_available = load_data()
df_pec = load_pecuaria()

# -------------------------
# INTERFACE
# -------------------------
try:
    st.sidebar.image("safratech_ia.png", use_container_width=True)
except Exception:
    pass
lang = st.sidebar.selectbox("🌐 Language", list(texts.keys()))
t = texts[lang]

# Funções de tradução — retornam a própria chave se não encontrada
def translate_crop(key):
    return t["crops"].get(key, key)

def translate_soil(key):
    return t["soils"].get(key, key)

st.title(t["title"])
st.sidebar.header(t["sidebar_cfg"])
menu = st.sidebar.radio(t["nav"], t["menu"])

# Cultura e área
cultura = st.sidebar.selectbox(
    t["crop_label"],
    sorted(df["label"].unique()),
    format_func=translate_crop,
)
acres = st.sidebar.number_input(t["area_label"], min_value=1.0, max_value=5000.0, value=1.0)

# Médias nutricionais para a cultura selecionada
dados_filtro = df[df["label"] == cultura]
if not dados_filtro.empty:
    ideal_n = dados_filtro["N"].mean()
    ideal_p = dados_filtro["P"].mean()
    ideal_k = dados_filtro["K"].mean()
else:
    ideal_n = ideal_p = ideal_k = 0.0

# -------------------------
# ABA 1: RECOMENDAÇÃO
# -------------------------
if menu == t["menu"][0]:
    st.markdown('<div class="header-badge">📌 Nutrição</div>' if lang == "Português" else '<div class="header-badge">📌 Nutrition</div>', unsafe_allow_html=True)
    st.header(t["rec_header"])
    st.subheader(f"🌱 {translate_crop(cultura)}")

    c1, c2, c3 = st.columns(3)
    hectares_equiv = acres * 0.4047
    c1.metric(t["nutrients"][0], f"{ideal_n * hectares_equiv:.1f} {t['ideal_unit']}")
    c2.metric(t["nutrients"][1], f"{ideal_p * hectares_equiv:.1f} {t['ideal_unit']}")
    c3.metric(t["nutrients"][2], f"{ideal_k * hectares_equiv:.1f} {t['ideal_unit']}")

# -------------------------
# ABA 2: DIAGNÓSTICO
# -------------------------
elif menu == t["menu"][1]:
    st.markdown('<div class="header-badge">🩺 Solo</div>' if lang == "Português" else '<div class="header-badge">🩺 Soil</div>', unsafe_allow_html=True)
    st.header(t["diag_header"])

    solo = st.selectbox(
        t["soil_label"],
        soils_available,
        format_func=translate_soil,
    )

    st.write(f"### {t['nutrients'][0]}, {t['nutrients'][1]}, {t['nutrients'][2]} (Kg/ha)")
    col_n, col_p, col_k = st.columns(3)
    n_user = col_n.number_input(t["nutrients"][0], min_value=0.0, key="n_in")
    p_user = col_p.number_input(t["nutrients"][1], min_value=0.0, key="p_in")
    k_user = col_k.number_input(t["nutrients"][2], min_value=0.0, key="k_in")

    if st.button(t["btn_diag"]):
        st.divider()
        st.subheader(f"📊 {translate_crop(cultura)} — {translate_soil(solo)}")

        hectares_equiv = acres * 0.4047

        params = [
            (t["nutrients"][0], n_user, ideal_n * hectares_equiv),
            (t["nutrients"][1], p_user, ideal_p * hectares_equiv),
            (t["nutrients"][2], k_user, ideal_k * hectares_equiv),
        ]

        tips = {
            "Português": {
                "N": {
                    "low":  "🌿 Sua planta pode estar **amarelada**, com crescimento lento e folhas pequenas. Aplique mais Nitrogênio.",
                    "high": "🌿 Sua planta pode estar com **folhagem verde escura demais**, produzindo pouca fruta e mais suscetível a pragas. Reduza o Nitrogênio.",
                    "ok":   "🌿 Nitrogênio em nível ideal. Planta deve estar bem verde e crescendo forte.",
                },
                "P": {
                    "low":  "🌱 Sua planta pode ter **raiz fraca e crescimento travado**. Folhas podem ficar arroxeadas. Aplique mais Fósforo.",
                    "high": "🌱 Excesso de Fósforo pode **travar a absorção de zinco e ferro**, causando deficiências mesmo com adubo. Reduza o Fósforo.",
                    "ok":   "🌱 Fósforo em nível ideal. Raiz forte e boa floração esperadas.",
                },
                "K": {
                    "low":  "🍌 Sua planta pode ter **bordas das folhas amareladas ou queimadas**, frutos menores e menos resistência à seca. Aplique mais Potássio.",
                    "high": "🍌 Excesso de Potássio pode causar **falta de magnésio e cálcio**, gerando amarelamento mesmo com adubo. Reduza o Potássio.",
                    "ok":   "🍌 Potássio em nível ideal. Planta mais resistente e frutos de melhor qualidade.",
                },
            },
            "English": {
                "N": {
                    "low":  "🌿 Your plant may be **yellowing**, with slow growth and small leaves. Apply more Nitrogen.",
                    "high": "🌿 Your plant may have **very dark green foliage**, producing little fruit and more susceptible to pests. Reduce Nitrogen.",
                    "ok":   "🌿 Nitrogen at ideal level. Plant should be healthy green and growing strong.",
                },
                "P": {
                    "low":  "🌱 Your plant may have **weak roots and stunted growth**. Leaves may turn purple. Apply more Phosphorus.",
                    "high": "🌱 Excess Phosphorus can **block zinc and iron absorption**, causing deficiencies even with fertilizer. Reduce Phosphorus.",
                    "ok":   "🌱 Phosphorus at ideal level. Strong roots and good flowering expected.",
                },
                "K": {
                    "low":  "🍌 Your plant may have **yellowed or scorched leaf edges**, smaller fruits and less drought resistance. Apply more Potassium.",
                    "high": "🍌 Excess Potassium can cause **magnesium and calcium deficiency**, causing yellowing even with fertilizer. Reduce Potassium.",
                    "ok":   "🍌 Potassium at ideal level. More resistant plant and better quality fruits.",
                },
            },
        }

        nutrient_keys = ["N", "P", "K"]

        for i, (nome, atual, ideal) in enumerate(params):
            if ideal == 0:
                st.warning(f"⚠️ {t['no_data']} {nome}")
                continue

            diff = ideal - atual
            nk = nutrient_keys[i]
            tip = tips[lang][nk]

            if atual < (ideal * 0.9):
                st.error(f"❌ {nome}: {t['missing']} {abs(diff):.1f} Kg/ha (ideal: {ideal:.1f})")
                st.caption(tip["low"])
            elif atual > (ideal * 1.2):
                st.warning(f"⚠️ {nome}: {t['excess']} {atual - ideal:.1f} Kg/ha (ideal: {ideal:.1f})")
                st.caption(tip["high"])
            else:
                st.success(f"✅ {nome}: {t['adequate']} ({atual:.1f} Kg/ha)")
                st.caption(tip["ok"])

# -------------------------
# ABA 3: PECUÁRIA
# -------------------------
elif menu == t["menu"][2]:
    st.markdown('<div class="header-badge">🐂 Pecuária</div>' if lang == "Português" else '<div class="header-badge">🐂 Livestock</div>', unsafe_allow_html=True)
    st.header(t["pec_header"])

    racas = sorted(df_pec["raca"].str.capitalize().unique().tolist())
    raca = st.selectbox(t["pec_race"], racas)
    sexo_opts = {"Português": {"macho": "Macho", "femea": "Fêmea"}, "English": {"macho": "Male", "femea": "Female"}}
    sexo_display = list(sexo_opts[lang].values())
    sexo_keys = list(sexo_opts[lang].keys())
    sexo_sel = st.selectbox(t["pec_sex"], sexo_display)
    sexo = sexo_keys[sexo_display.index(sexo_sel)]

    idade = st.number_input(t["pec_age"], min_value=1, max_value=120, value=24)
    peso_atual = st.number_input(t["pec_weight"], min_value=10.0, max_value=1500.0, value=300.0)
    st.selectbox(t["pec_system"], t["pec_systems"])

    if st.button(t["pec_btn"]):
        st.divider()

        filtro = df_pec[
            (df_pec["raca"] == raca.lower()) &
            (df_pec["sexo"] == sexo)
        ]

        # Busca registros próximos à idade informada (±6 meses)
        filtro_idade = filtro[
            (filtro["idade_meses"] >= idade - 6) &
            (filtro["idade_meses"] <= idade + 6)
        ]

        if filtro_idade.empty:
            filtro_idade = filtro  # fallback sem filtro de idade

        if filtro_idade.empty:
            st.warning(t["pec_no_data"])
        else:
            peso_min = filtro_idade["peso_kg"].min()
            peso_max = filtro_idade["peso_kg"].max()
            peso_medio = filtro_idade["peso_kg"].mean()
            escore_medio = filtro_idade["escore_corporal"].mean()
            ganho_medio = filtro_idade["ganho_diario_kg"].mean()

            # Determina situação
            if peso_atual < peso_min * 0.95:
                situacao_key = "abaixo_peso"
            elif peso_atual > peso_max * 1.05:
                situacao_key = "acima_peso"
            else:
                situacao_key = "saudavel"

            situacao_label = t["pec_status_map"][situacao_key]

            # Potencial de ganho
            if ganho_medio >= 0.8:
                potencial = "🚀 Alto" if lang == "Português" else "🚀 High"
            elif ganho_medio >= 0.5:
                potencial = "➡️ Médio" if lang == "Português" else "➡️ Medium"
            else:
                potencial = "🐢 Baixo" if lang == "Português" else "🐢 Low"

            st.subheader(f"{raca} — {sexo_sel} — {idade} {'meses' if lang == 'Português' else 'months'}")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric(t["pec_expected"], f"{peso_min:.0f} – {peso_max:.0f} Kg")
            c2.metric(t["pec_score"], f"{escore_medio:.1f}/10")
            c3.metric(t["pec_gain"], f"{ganho_medio:.2f} Kg")
            c4.metric(t["pec_status"], situacao_label)

            st.markdown(f"**{t['pec_potential']}:** {potencial}")

            if situacao_key == "abaixo_peso":
                st.error(f"⚠️ Peso atual ({peso_atual:.1f} Kg) abaixo do esperado ({peso_min:.0f}–{peso_max:.0f} Kg). Revise a alimentação e sanidade do animal." if lang == "Português" else f"⚠️ Current weight ({peso_atual:.1f} Kg) below expected ({peso_min:.0f}–{peso_max:.0f} Kg). Review feeding and animal health.")
            elif situacao_key == "acima_peso":
                st.success(f"📈 Animal acima da média ({peso_atual:.1f} Kg). Excelente desempenho!" if lang == "Português" else f"📈 Animal above average ({peso_atual:.1f} Kg). Excellent performance!")
            else:
                st.success(f"✅ Animal dentro do peso esperado ({peso_atual:.1f} Kg). Continue o manejo atual." if lang == "Português" else f"✅ Animal within expected weight ({peso_atual:.1f} Kg). Continue current management.")


# -------------------------
# ABA 4: ASSISTENTE
# -------------------------
elif menu == t["menu"][3]:
    st.markdown('<div class="header-badge">💬 Assistente</div>' if lang == "Português" else '<div class="header-badge">💬 Assistant</div>', unsafe_allow_html=True)
    st.header("💬 Assistente SafraTech" if lang == "Português" else "💬 SafraTech Assistant")
    st.caption("Tire dúvidas sobre agricultura, solo, nutrição de plantas e pecuária." if lang == "Português" else "Ask questions about agriculture, soil, plant nutrition and livestock.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    pergunta = st.chat_input("Digite sua pergunta..." if lang == "Português" else "Type your question...")

    if pergunta:
        st.session_state.chat_history.append({"role": "user", "content": pergunta})
        with st.chat_message("user"):
            st.markdown(pergunta)

        with st.chat_message("assistant"):
            with st.spinner("Pensando..." if lang == "Português" else "Thinking..."):
                try:
                    api_key = st.secrets["gemini"]["api_key"]
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

                    system_prompt = (
                        "Você é o Assistente SafraTech, um especialista em agricultura de precisão e pecuária. "
                        "Responda sempre em português de forma clara, prática e objetiva. "
                        "Foque em: nutrição de plantas (NPK), tipos de solo, culturas (soja, milho, arroz, feijão, algodão), "
                        "pecuária (Nelore, Tabapuá e outras raças zebuínas), manejo de pastagem, adubação e sanidade animal. "
                        "Se a pergunta não for sobre agricultura ou pecuária, redirecione gentilmente para esses temas."
                    ) if lang == "Português" else (
                        "You are the SafraTech Assistant, an expert in precision agriculture and livestock. "
                        "Always respond in English in a clear, practical and objective way. "
                        "Focus on: plant nutrition (NPK), soil types, crops (soybean, corn, rice, beans, cotton), "
                        "livestock (Nellore, Tabapua and other zebu breeds), pasture management, fertilization and animal health. "
                        "If the question is not about agriculture or livestock, gently redirect to these topics."
                    )

                    contents = []
                    for msg in st.session_state.chat_history[:-1]:
                        contents.append({
                            "role": "user" if msg["role"] == "user" else "model",
                            "parts": [{"text": msg["content"]}]
                        })
                    contents.append({"role": "user", "parts": [{"text": system_prompt + "\n\n" + pergunta}]})

                    resp = requests.post(url, json={"contents": contents})
                    data = resp.json()
                    resposta = data["candidates"][0]["content"]["parts"][0]["text"]

                except Exception as e:
                    resposta = f"Erro ao conectar com o assistente: {e}"

                st.markdown(resposta)
                st.session_state.chat_history.append({"role": "assistant", "content": resposta})

    if st.session_state.chat_history:
        if st.button("🗑️ Limpar conversa" if lang == "Português" else "🗑️ Clear chat"):
            st.session_state.chat_history = []
            st.rerun()

st.caption(t["footer"])