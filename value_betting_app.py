
import streamlit as st
import pandas as pd

# Inizializzazione dello stato
if 'bankroll' not in st.session_state:
    st.session_state.bankroll = 1000.0
if 'bets' not in st.session_state:
    st.session_state.bets = []

# Funzione di Kelly Criterion
def kelly(prob, quota, bankroll):
    edge = (quota * prob) - 1
    kelly_fraction = edge / (quota - 1)
    stake = max(0, kelly_fraction * bankroll)
    return round(stake, 2)

# Interfaccia utente
st.title("📈 Value Betting App con Kelly Criterion")
st.write(f"💰 **Bankroll attuale**: €{round(st.session_state.bankroll, 2)}")

st.subheader("➕ Inserisci una nuova scommessa")

with st.form("scommessa"):
    evento = st.text_input("Evento", placeholder="Es: Milan - Inter")
    quota = st.number_input("Quota offerta", min_value=1.01, step=0.01)
    prob = st.number_input("Probabilità stimata (decimale)", min_value=0.0, max_value=1.0, step=0.01)
    risultato = st.selectbox("Esito", ["vinta", "persa"])
    submit = st.form_submit_button("Aggiungi scommessa")

    if submit and evento:
        stake = kelly(prob, quota, st.session_state.bankroll)
        if stake == 0:
            st.warning("⚠️ Nessun value bet. Quota troppo bassa rispetto alla probabilità stimata.")
        else:
            profitto = round((quota - 1) * stake if risultato == "vinta" else -stake, 2)
            st.session_state.bankroll += profitto

            st.session_state.bets.append({
                "Evento": evento,
                "Quota": quota,
                "Probabilità": prob,
                "Stake (€)": stake,
                "Esito": risultato,
                "Profitto (€)": profitto,
                "Bankroll (€)": round(st.session_state.bankroll, 2)
            })
            st.success(f"Scommessa aggiunta! Profitto: €{profitto}, Nuovo bankroll: €{round(st.session_state.bankroll, 2)}")

# Visualizzazione storico
if st.session_state.bets:
    st.subheader("📊 Storico scommesse")
    df = pd.DataFrame(st.session_state.bets)
    st.dataframe(df, use_container_width=True)

    totale_stake = df["Stake (€)"].sum()
    totale_profitto = df["Profitto (€)"].sum()
    roi = (totale_profitto / totale_stake * 100) if totale_stake > 0 else 0

    st.markdown(f"📌 **ROI totale**: `{roi:.2f}%`")
    st.markdown(f"🎯 **Profitto totale**: `€{totale_profitto:.2f}`")
