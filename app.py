import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="KUROBA ZERO", page_icon="🔥", layout="wide")

st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #1a0033 0%, #0f001f 100%); color: #fff; }
    .big-title { font-size: 2.8rem; font-weight: 700; text-align: center; margin: 20px 0 10px; }
    .search-bar { background: rgba(255,255,255,0.08); border: 2px solid #9d4cff; border-radius: 50px; padding: 18px 25px; font-size: 1.4rem; }
    .result-card { background: rgba(255,255,255,0.06); border-radius: 16px; padding: 25px; margin: 20px 0; border: 1px solid #9d4cff; }
    .label { color: #ff4d94; font-size: 0.9rem; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">🔥 KUROBA ZERO</p>', unsafe_allow_html=True)
st.caption("Bouygues Mobile Dump • Test v2.6")

# AUTH rapide (on garde le privé)
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.warning("🔒 Accès privé")
    if st.button("Se connecter (mot de passe kuroba2026)"):
        st.session_state.authenticated = True
        st.rerun()
    st.stop()

# UPLOAD Bouygues
st.subheader("📤 Charge ton fichier Bouygues (JSON)")
uploaded = st.file_uploader("Dépose le fichier Bouygues ici", type=["json"])

if uploaded:
    # Lecture JSON Lines
    df = pd.read_json(uploaded, lines=True)
    st.success(f"✅ Bouygues chargé → {len(df)} enregistrements")

    # BARRE DE RECHERCHE
    query = st.text_input("", placeholder="Tape un prénom, nom, email ou téléphone (ex: MAGALIE ou 0627535983)", label_visibility="collapsed")

    if st.button("🔎 Search", type="primary", use_container_width=True) and query:
        with st.spinner("Recherche dans Bouygues..."):
            df_str = df.astype(str)
            mask = df_str.apply(lambda x: x.str.contains(query, case=False, na=False)).any(axis=1)
            results = df[mask]

            if not results.empty:
                st.markdown("### Résultats Bouygues")
                for _, row in results.iterrows():
                    st.markdown(f"""
                    <div class="result-card">
                        <span class="label">👤 PRENOM</span><br><h4>{row.get('Prenom', 'N/A')}</h4>
                        <span class="label">👤 NOM</span><br><h4>{row.get('Nom', 'N/A')}</h4>
                        <span class="label">📱 PHONE</span><br><h4>{row.get('Phone', 'N/A')}</h4>
                        <span class="label">✉️ EMAIL</span><br><h4>{row.get('Email', 'N/A')}</h4>
                        <span class="label">🏠 ADRESSE</span><br><h4>{row.get('Adresse', 'N/A')} {row.get('Codepostal', '')} {row.get('Ville', '')}</h4>
                        <span class="label">📅 DATE NAISSANCE</span><br><h4>{row.get('DateNaissance', 'N/A')}</h4>
                        <span class="label">🏦 IBAN</span><br><h4>{row.get('IBAN', 'N/A')}</h4>
                        <span class="label">🏦 BIC</span><br><h4>{row.get('BIC', 'N/A')}</h4>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Aucun résultat pour cette recherche.")

# Sidebar
with st.sidebar:
    st.success("Connecté")
    if st.button("Déconnexion"):
        st.session_state.authenticated = False
        st.rerun()

st.caption("v2.6 • Bouygues Mobile seulement • On ajoute les autres après test")
