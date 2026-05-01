import openai
import json
import pandas as pd
import streamlit as st
import os
os.environ['STREAMLIT_PRY_ARROW_DISABLE'] = 'True'

st.set_page_config(
    page_title="PropScout AI | Elite Terminal",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS pro prémiový B2B vzhled
st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #FAFAFA; }
    .hero-title { font-size: 3rem; font-weight: 800; color: #E2B714; margin-bottom: 0px; }
    .hero-subtitle { font-size: 1.2rem; color: #A0AEC0; margin-bottom: 30px; }
    .card { background-color: #1A202C; padding: 20px; border-radius: 10px; border-left: 5px solid #E2B714; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .card-title { font-size: 1.5rem; font-weight: bold; color: #FFFFFF; }
    .badge-best { background-color: #2F855A; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold; }
    .badge-worst { background-color: #C53030; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold; }
    .metric-value { font-size: 1.8rem; font-weight: bold; color: #E2B714; }
    </style>
""", unsafe_allow_html=True)

mock_listings = """
1. [Dubaj, JVC] Cena: 180,000 EUR. 1BR apartmán, off-plan, hotovo 2026. Developer Emaar. Očekávaný nájem 15,000 EUR/rok. Žádné poplatky agentuře.
2. [Španělsko, Malaga] Cena: 65,000 EUR. 3+1, 10 min od moře. Platba možná jen v kryptu nebo hotovosti. Chybí fotky interiéru, dům potřebuje "menší opravy" (rekonstrukce střechy). Výnos prý 20%.
3. [Polsko, Varšava] Cena: 130,000 EUR. 2kk, centrum města. Pronajato spolehlivému nájemníkovi za 8,500 EUR/rok čistého. Právně čisté, plné vlastnictví.
4. [Egypt, Hurghada] Cena: 25,000 EUR. Studio na pláži. Garantovaný výnos 15% na 10 let. Právní status: usufruct (užívací právo na 99 let, ne osobní vlastnictví).
"""


def analyze_and_rank_properties(api_key, listings_text):
    openai.api_key = api_key
    
    system_prompt = """
    Jsi elitní investiční manažer a realitní analytik (spojení Warrena Buffetta a lokálního experta na reality).
    Tvým úkolem je přijmout surová data inzerátů, analyzovat je a SEŘADIT je od nejlepší investice po nejhorší.
    
    Kritéria hodnocení (A-F skóre):
    1. Reálnost ROI (Falešné sliby nad 10 % bez rizika automaticky penalizuj).
    2. Právní rizika (Chybějící vlastnictví, platby v hotovosti = obrovské red flags).
    3. Likvidita (Jak snadno to půjde prodat dál).
    
    TVŮJ VÝSTUP MUSÍ BÝT PŘESNĚ VE FORMÁTU JSON (nic jiného, žádný markdown okolo).
    Struktura JSON:
    {
      "analyza": [
        {
          "poradi": 1,
          "lokalita": "Město, Země",
          "cena": "Cena v EUR",
          "roi_odhad": "Reálný odhad v %",
          "hodnoceni": "A/B/C/D/F",
          "shrnuti": "Proč je to na této pozici (max 2 věty).",
          "red_flags": ["riziko 1", "riziko 2"],
          "doporuceni": "Koupit / Vyhnout se / Nutný audit"
        }
      ]
    }
    """
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o", # Možno změnit na gpt-3.5-turbo pro levnější testování
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": listings_text}
            ],
            response_format={ "type": "json_object" } # Vynutí striktní JSON výstup
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}


st.markdown('<p class="hero-title">PropScout AI 🎯</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Mezinárodní investiční terminál. Proměňte surová data v čistý zisk.</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2933/2933245.png", width=100)
    st.markdown("### 🔐 Autentizace")
    api_key_input = st.text_input("OpenAI API Klíč (Zabezpečeno)", type="password")
    
    st.markdown("---")
    st.markdown("### ⚙️ Investiční strategie")
    strategy = st.selectbox("Typ hledání", ["Konzervativní (Cashflow)", "Agresivní (Flipping)", "Ochrana kapitálu"])
    
    st.markdown("---")
    st.caption("PropScout AI v1.0. Core Engine aktivní.")

# Main Content
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📥 Vstup surových dat (Batch Processing)")
    st.info("Vložte text ze zahraničních portálů, e-mailů od makléřů nebo použijte naše testovací data.")
    user_input = st.text_area("Surové inzeráty:", value=mock_listings, height=300)
    
    analyze_btn = st.button("🚀 Spustit hlubokou AI Analýzu", use_container_width=True, type="primary")

with col2:
    st.markdown("### 🧠 AI Kognitivní proces")
    st.markdown("""
    Náš model provádí:
    * **Cross-reference cen** na lokálním trhu.
    * **Analýzu sentimentu** (detekce zoufalých prodejců nebo lživých frází).
    * **Právní screening** (identifikace podezřelých platebních metod).
    """)
    st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80", use_container_width=True)

st.markdown("---")


if analyze_btn:
    if not api_key_input:
        st.error("⚠️ Pro spuštění enginu je nutný API klíč.")
    else:
        with st.spinner("AI engine skenuje trhy, analyzuje ROI a hledá skrytá rizika..."):
            result = analyze_and_rank_properties(api_key_input, user_input)
            
            if "error" in result:
                st.error(f"Chyba enginu: {result['error']}")
            else:
                st.markdown("## 📊 Výsledky analýzy: Od nejlepšího po nejhorší")
                
                for item in result.get("analyza", []):
                    # Nastavení barvy podle pořadí
                    badge_class = "badge-best" if item['poradi'] == 1 else "badge-worst" if item['poradi'] > 2 else "badge-best"
                    
                    # Vykreslení karty
                    st.markdown(f"""
                    <div class="card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span class="card-title">#{item['poradi']} {item['lokalita']}</span>
                            <span class="{badge_class}">Skóre: {item['hodnoceni']}</span>
                        </div>
                        <hr style="border-color: #4A5568;">
                        <p><strong>Cena:</strong> <span class="metric-value">{item['cena']}</span> | <strong>Reálné ROI:</strong> <span style="color: #4FD1C5; font-weight: bold;">{item['roi_odhad']}</span></p>
                        <p><strong>Doporučení makléře:</strong> {item['doporuceni']}</p>
                        <p><em>{item['shrnuti']}</em></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Zobrazení Red Flags
                    if item.get('red_flags') and len(item['red_flags']) > 0 and item['red_flags'][0] != "Žádné výrazné":
                        with st.expander("🚨 Zobrazit detekovaná rizika (Red Flags)"):
                            for rf in item['red_flags']:
                                st.error(rf)