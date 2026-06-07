import streamlit as st
import requests
import random
import base64

# Configuração da Página
st.set_page_config(page_title="Quem é esse Pokémon?", page_icon="🎮", layout="centered")

# --- DESIGN E CENTRALIZAÇÃO ---
def aplicar_layout_centrado(image_file):
    try:
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read())
        
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{encoded_string.decode()}");
                background-attachment: fixed;
                background-size: cover;
            }}
            
            .main-ui {{
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
            }}

            /* --- TITULOS PRINCIPAIS COM ALTO CONTRASTE --- */
            h1 {{
                color: #ffcb05 !important;
                font-size: 52px !important;
                text-shadow: 
                    -2.5px -2.5px 0 #000,  
                     2.5px -2.5px 0 #000,
                    -2.5px  2.5px 0 #000,
                     2.5px  2.5px 0 #000,
                     5px  5px 0px #000 !important; 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                letter-spacing: 2px;
                text-align: center !important;
                margin-bottom: 35px !important;
            }}

            h2, h3 {{
                color: #ffcb05 !important;
                text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000, 2px 2px 0 #000 !important;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                text-align: center !important;
            }}

            /* --- TITULOS DOS RADIOS (DIFICULDADE E GERAÇÃO) --- */
            .stRadio > label {{
                color: #ffcb05 !important;
                font-size: 24px !important; 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
                font-weight: 900 !important;
                text-shadow: 2px 2px 0px #000 !important;
                letter-spacing: 1px !important;
                margin-bottom: 10px !important;
            }}
            
            /* Cards das Opções */
            div[role="radiogroup"] p {{
                color: #1a2a7a !important;
                font-weight: bold !important;
                font-size: 18px !important;
                background-color: rgba(255, 255, 255, 0.9) !important;
                padding: 8px 18px;
                border-radius: 8px;
                border: 2px solid #ffcb05;
            }}

            /* --- CARDS DE STATUS --- */
            [data-testid="stMetric"] {{
                background-color: rgba(255, 255, 255, 0.95) !important;
                border-radius: 12px !important;
                padding: 15px 5px !important;
                border: 2px solid #3b4cca !important;
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
                justify-content: center !important;
                text-align: center !important;
                box-shadow: 4px 4px 10px rgba(0,0,0,0.1);
            }}

            [data-testid="stMetricLabel"] p {{
                color: #ffcb05 !important;
                text-shadow: 1.5px 1.5px 0px #000 !important;
                font-family: 'Segoe UI', sans-serif;
                font-weight: bold !important;
                font-size: 20px !important;
                text-align: center !important;
                width: 100% !important;
                display: flex !important;
                justify-content: center !important;
            }}

            [data-testid="stMetricValue"] {{
                color: #1a2a7a !important;
                font-size: 36px !important;
                font-weight: bold !important;
                width: 100% !important;
                display: flex !important;
                justify-content: center !important;
                text-align: center !important;
            }}

            /* --- BOTÕES --- */
            .stButton>button {{
                background-color: #1a2a7a !important; 
                color: white !important;
                border: 2px solid #ffcb05 !important;
                border-radius: 10px !important;
                font-weight: 700 !important;
                font-size: 18px !important;
                transition: 0.2s;
            }}
            
            .stButton>button:hover {{
                background-color: #3b4cca !important;
                border-color: #ffffff !important;
                transform: scale(1.02);
            }}
            </style>
            """, unsafe_allow_html=True)
    except: pass

# --- INICIALIZAÇÃO DO ESTADO ---
if 'pontos' not in st.session_state:
    st.session_state.update({
        'pontos': 0, 
        'vidas': 3, 
        'game_over': False, 
        'jogo_iniciado': False, 
        'dificuldade': 'Fácil',
        'geracao': '1ª Gen'
    })

aplicar_layout_centrado('background.png')

@st.cache_data(show_spinner=False)
def buscar_pokemon(id_p):
    try:
        res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{id_p}", timeout=5).json()
        return {"nome": res['name'].capitalize(), "sprite": res['sprites']['front_default'],
                "hp": res['stats'][0]['base_stat'], "atk": res['stats'][1]['base_stat'], "def": res['stats'][2]['base_stat']}
    except:
        return None

def obter_limites_geracao(geracao_escolhida):
    if "1ª" in geracao_escolhida: return 1, 151
    elif "2ª" in geracao_escolhida: return 152, 251
    elif "3ª" in geracao_escolhida: return 252, 386
    else: return 1, 386

# --- UI PRINCIPAL ---
st.markdown('<div class="main-ui">', unsafe_allow_html=True)
st.markdown("<h1>🕵️ QUEM É ESSE POKÉMON?</h1>", unsafe_allow_html=True)

# 1. SELETORES DE MENU
col_menu1, col_menu2 = st.columns(2)

with col_menu1:
    dificuldade_selecionada = st.radio(
        "Defina a Dificuldade:", 
        ["Fácil", "Difícil"], 
        horizontal=True, 
        disabled=st.session_state.jogo_iniciado
    )

with col_menu2:
    geracao_selecionada = st.radio(
        "Escolha a Geração:", 
        ["1ª Gen", "2ª Gen", "3ª Gen", "Todas"], 
        horizontal=True, 
        disabled=st.session_state.jogo_iniciado
    )

# 2. TELA DE INÍCIO
if not st.session_state.jogo_iniciado:
    st.write("---")
    if st.button("COMEÇAR JOGO ▶️", use_container_width=True):
        st.session_state.jogo_iniciado = True
        st.session_state.dificuldade = dificuldade_selecionada
        st.session_state.geracao = geracao_selecionada
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 3. GERADOR DE ROUND
if not st.session_state.game_over and 'pokemon' not in st.session_state:
    with st.spinner("Sorteando Pokémon..."):
        min_id, max_id = obter_limites_geracao(st.session_state.geracao)
        p = buscar_pokemon(random.randint(min_id, max_id))
        if p:
            opcoes = {p['nome']}
            while len(opcoes) < 4:
                falso = buscar_pokemon(random.randint(min_id, max_id))
                if falso: opcoes.add(falso['nome'])
            lista = list(opcoes)
            random.shuffle(lista)
            st.session_state.update({'pokemon': p, 'alternativas': lista, 'respondido': False})

# 4. HUD COM BOTÃO DE MENU
c1, c2, c3 = st.columns([2, 2, 1.5])
c1.markdown(f"### Vidas: {'🔴' * st.session_state.vidas}")
c2.markdown(f"### Pontos: **{st.session_state.pontos}**")
with c3:
    if st.button("🏠 Menu", use_container_width=True):
        for k in ['pontos', 'vidas', 'game_over', 'pokemon', 'jogo_iniciado']: 
            st.session_state.pop(k, None)
        st.rerun()

if st.session_state.game_over:
    st.error(f"Fim de Jogo! Pontuação: {st.session_state.pontos}")
    if st.button("Jogar Novamente 🔄", use_container_width=True):
        for k in ['pontos', 'vidas', 'game_over', 'pokemon', 'jogo_iniciado']: 
            st.session_state.pop(k, None)
        st.rerun()
else:
    if 'pokemon' in st.session_state:
        p = st.session_state.pokemon
        st.write("---")
        s1, s2, s3 = st.columns(3)
        s1.metric("HP", p['hp'])
        s2.metric("ATAQUE", p['atk'])
        s3.metric("DEFESA", p['def'])

        st.write("") 
        mostrar_imagem = True if (st.session_state.dificuldade == "Fácil") or st.session_state.respondido else False

        if mostrar_imagem:
            _, mid, _ = st.columns([1, 1, 1])
            mid.image(p['sprite'], use_container_width=True)

        if st.session_state.respondido:
            st.subheader(f"É o {p['nome']}!")
            if st.button("PRÓXIMO ➡️", use_container_width=True):
                st.session_state.pop('pokemon')
                st.rerun()
        else:
            st.write("### QUAL É O POKÉMON?")
            col_a, col_b = st.columns(2)
            for i, nome in enumerate(st.session_state.alternativas):
                btn_col = col_a if i % 2 == 0 else col_b
                if btn_col.button(nome, use_container_width=True):
                    st.session_state.respondido = True
                    if nome == p['nome']:
                        st.session_state.pontos += 1
                        st.success("Acertou!")
                        st.balloons()
                    else:
                        st.session_state.vidas -= 1
                        st.error(f"Errou! Era o {p['nome']}")
                        if st.session_state.vidas <= 0: st.session_state.game_over = True
                    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
