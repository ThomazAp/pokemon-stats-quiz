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

            /* --- TITULOS PRINCIPAIS --- */
            h1, h2, h3 {{
                color: #ffcb05 !important;
                text-shadow: 2px 2px 0px #000 !important;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                letter-spacing: 1px;
                text-align: center !important;
                font-size: 32px !important;
            }}

            /* --- CENTRALIZAÇÃO E DESIGN DOS CARDS --- */
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

            /* Rótulos internos dos cards (HP, ATAQUE, DEFESA) */
            [data-testid="stMetricLabel"] p {{
                color: #ffcb05 !important;
                text-shadow: 1.5px 1.5px 0px #000 !important;
                font-family: 'Segoe UI', sans-serif;
                font-weight: bold !important;
                font-size: 18px !important;
                text-align: center !important;
                width: 100% !important;
                display: flex !important;
                justify-content: center !important;
            }}

            /* Números internos dos cards */
            [data-testid="stMetricValue"] {{
                color: #1a2a7a !important;
                font-size: 34px !important;
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
                border-radius: 8px !important;
                font-weight: 600 !important;
                transition: 0.2s;
            }}
            
            .stButton>button:hover {{
                background-color: #3b4cca !important;
                border-color: #ffffff !important;
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
        'dificuldade': 'Fácil'
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

# --- UI PRINCIPAL ---
st.markdown('<div class="main-ui">', unsafe_allow_html=True)
st.title("🕵️ QUEM É ESSE POKÉMON?")

# 1. SELETOR DE DIFICULDADE (Desativado se o jogo já começou)
dificuldade_selecionada = st.radio(
    "Dificuldade:", 
    ["Fácil", "Difícil"], 
    horizontal=True, 
    disabled=st.session_state.jogo_iniciado
)

# 2. TELA DE INÍCIO (Trava o jogo até clicar em Começar)
if not st.session_state.jogo_iniciado:
    st.write("---")
    if st.button("COMEÇAR JOGO ▶️", use_container_width=True):
        st.session_state.jogo_iniciado = True
        st.session_state.dificuldade = dificuldade_selecionada
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop() # Interrompe a leitura do código aqui até o jogo iniciar

# 3. GERADOR DE ROUND
if not st.session_state.game_over and 'pokemon' not in st.session_state:
    with st.spinner("Sorteando Pokémon..."):
        p = buscar_pokemon(random.randint(1, 151))
        if p:
            opcoes = {p['nome']}
            while len(opcoes) < 4:
                falso = buscar_pokemon(random.randint(1, 151))
                if falso:
                    opcoes.add(falso['nome'])
            lista = list(opcoes)
            random.shuffle(lista)
            st.session_state.update({'pokemon': p, 'alternativas': lista, 'respondido': False})

# 4. HUD (Vidas e Pontos)
c1, c2 = st.columns(2)
c1.markdown(f"### Vidas: {'🔴' * st.session_state.vidas}")
c2.markdown(f"### Pontos: **{st.session_state.pontos}**")

if st.session_state.game_over:
    st.error(f"Fim de Jogo! Pontuação: {st.session_state.pontos}")
    if st.button("Reiniciar 🔄", use_container_width=True):
        # Limpa tudo, inclusive o status de jogo iniciado para voltar à tela de seleção
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
        
        # REGRA DE EXIBIÇÃO DA IMAGEM
        mostrar_imagem = True if (st.session_state.dificuldade == "Fácil") or st.session_state.respondido else False

        if mostrar_imagem:
            _, mid, _ = st.columns([1, 1, 1])
            mid.image(p['sprite'], use_container_width=True)

        # LÓGICA DE RESPOSTA E BOTÕES
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
