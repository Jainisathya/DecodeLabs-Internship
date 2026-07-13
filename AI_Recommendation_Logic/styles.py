"""
styles.py – Theme definitions and CSS loader for AI Smart Recommendation Hub.
"""

THEMES = {
    "Dark": {
        "background":   "#0D1117",
        "surface":      "#161B22",
        "surface2":     "#21262D",
        "primary":      "#7C3AED",
        "secondary":    "#A78BFA",
        "accent":       "#06D6A0",
        "text":         "#E6EDF3",
        "muted":        "#8B949E",
        "border":       "#30363D",
        "shadow":       "rgba(0,0,0,0.6)",
        "gradient":     "linear-gradient(135deg,#7C3AED,#06D6A0)",
        "card_hover":   "#7C3AED"
    },
    "Light": {
        "background":   "#F0F4FF",
        "surface":      "#FFFFFF",
        "surface2":     "#F8FAFF",
        "primary":      "#4F46E5",
        "secondary":    "#7C3AED",
        "accent":       "#06D6A0",
        "text":         "#0F172A",
        "muted":        "#64748B",
        "border":       "#E2E8F0",
        "shadow":       "rgba(79,70,229,0.12)",
        "gradient":     "linear-gradient(135deg,#4F46E5,#7C3AED)",
        "card_hover":   "#4F46E5"
    },
    "Ocean": {
        "background":   "#0A192F",
        "surface":      "#112240",
        "surface2":     "#1D3461",
        "primary":      "#64FFDA",
        "secondary":    "#0EA5E9",
        "accent":       "#F72585",
        "text":         "#CCD6F6",
        "muted":        "#8892B0",
        "border":       "#233554",
        "shadow":       "rgba(100,255,218,0.08)",
        "gradient":     "linear-gradient(135deg,#0EA5E9,#64FFDA)",
        "card_hover":   "#64FFDA"
    },
    "Sunset": {
        "background":   "#1A0A00",
        "surface":      "#2A1200",
        "surface2":     "#3D1F00",
        "primary":      "#FF6B35",
        "secondary":    "#FFB347",
        "accent":       "#FFE66D",
        "text":         "#FFF3E0",
        "muted":        "#FFCC80",
        "border":       "#5D3A1A",
        "shadow":       "rgba(255,107,53,0.2)",
        "gradient":     "linear-gradient(135deg,#FF6B35,#FFB347)",
        "card_hover":   "#FF6B35"
    },
    "Emerald": {
        "background":   "#001A12",
        "surface":      "#00291C",
        "surface2":     "#003D2A",
        "primary":      "#00D68F",
        "secondary":    "#36D399",
        "accent":       "#3ABFF8",
        "text":         "#D1FAE5",
        "muted":        "#6EE7B7",
        "border":       "#065F46",
        "shadow":       "rgba(0,214,143,0.12)",
        "gradient":     "linear-gradient(135deg,#00D68F,#3ABFF8)",
        "card_hover":   "#00D68F"
    },
    "Cosmic": {
        "background":   "#04000F",
        "surface":      "#0D0021",
        "surface2":     "#190038",
        "primary":      "#BD00FF",
        "secondary":    "#FF007A",
        "accent":       "#00F5FF",
        "text":         "#E8DFFF",
        "muted":        "#A78BFA",
        "border":       "#3B0066",
        "shadow":       "rgba(189,0,255,0.2)",
        "gradient":     "linear-gradient(135deg,#BD00FF,#FF007A)",
        "card_hover":   "#BD00FF"
    }
}


def load_css(theme_name: str = "Dark") -> str:
    """Return the full CSS string for the chosen theme."""
    if theme_name not in THEMES:
        theme_name = "Dark"
    t = THEMES[theme_name]

    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── GLOBAL ─────────────────────────────────── */
html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif !important;
}}

.stApp {{
    background: {t["background"]};
    color: {t["text"]};
}}

/* ── SIDEBAR ─────────────────────────────────── */
section[data-testid="stSidebar"] {{
    background: {t["surface"]} !important;
    border-right: 1px solid {t["border"]};
}}

section[data-testid="stSidebar"] * {{
    color: {t["text"]} !important;
}}

/* ── MAIN CONTENT ────────────────────────────── */
.block-container {{
    padding: 1.5rem 2rem !important;
}}

/* ── HERO ────────────────────────────────────── */
.hero-wrap {{
    background: {t["gradient"]};
    border-radius: 24px;
    padding: 52px 40px;
    text-align: center;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px {t["shadow"]};
}}

.hero-wrap::before {{
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    background: rgba(255,255,255,0.06);
    border-radius: 50%;
}}

.hero-wrap h1 {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    color: #fff;
    margin: 0 0 12px;
    text-shadow: 0 2px 20px rgba(0,0,0,0.3);
}}

.hero-wrap p {{
    font-size: 1.15rem;
    color: rgba(255,255,255,0.88);
    margin: 0;
}}

/* ── STAT CARDS ─────────────────────────────── */
.stat-card {{
    background: {t["surface"]};
    border: 1px solid {t["border"]};
    border-radius: 18px;
    padding: 28px 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    box-shadow: 0 4px 20px {t["shadow"]};
}}

.stat-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: {t["gradient"]};
    border-radius: 18px 18px 0 0;
}}

.stat-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 16px 40px {t["shadow"]};
}}

.stat-value {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    background: {t["gradient"]};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    display: block;
    margin-bottom: 6px;
}}

.stat-label {{
    color: {t["muted"]};
    font-size: 0.9rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}}

/* ── CATEGORY CARDS ─────────────────────────── */
.cat-card {{
    background: {t["surface"]};
    border: 1px solid {t["border"]};
    border-radius: 20px;
    padding: 28px 20px;
    margin-top: 10px;
    text-align: center;
    transition: all 0.3s ease;
    box-shadow: 0 4px 20px {t["shadow"]};
    cursor: pointer;
}}

.cat-card:hover {{
    transform: translateY(-8px);
    border-color: {t["card_hover"]};
    box-shadow: 0 20px 50px {t["shadow"]};
}}

.cat-icon {{
    font-size: 3rem;
    display: block;
    margin-bottom: 12px;
}}

.cat-title {{
    color: {t["primary"]};
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 8px;
    font-family: 'Space Grotesk', sans-serif;
}}

.cat-desc {{
    color: {t["muted"]};
    font-size: 0.85rem;
    line-height: 1.5;
}}

/* ── RECOMMENDATION CARDS ─────────────────────── */
.rec-card {{
    background: {t["surface"]};
    border: 1px solid {t["border"]};
    border-radius: 18px;
    padding: 22px 24px;
    margin: 12px 0;
    transition: all 0.3s ease;
    box-shadow: 0 4px 20px {t["shadow"]};
    position: relative;
    overflow: hidden;
}}

.rec-card::before {{
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    background: {t["gradient"]};
    border-radius: 18px 0 0 18px;
}}

.rec-card:hover {{
    transform: translateX(6px);
    border-color: {t["card_hover"]};
    box-shadow: 0 12px 40px {t["shadow"]};
}}

.rec-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
    flex-wrap: wrap;
    gap: 8px;
}}

.rec-title {{
    font-size: 1.15rem;
    font-weight: 700;
    color: {t["text"]};
    font-family: 'Space Grotesk', sans-serif;
}}

.rec-badge {{
    background: {t["gradient"]};
    color: #fff;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}}

.rec-desc {{
    color: {t["muted"]};
    font-size: 0.92rem;
    line-height: 1.6;
    margin: 0 0 14px;
}}

.rec-meta {{
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}}

.rec-rating, .rec-score {{
    font-size: 0.88rem;
    font-weight: 600;
    color: {t["secondary"]};
}}

/* ── SECTION HEADERS ─────────────────────────── */
.section-header {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: {t["text"]};
    margin: 28px 0 16px;
    display: flex;
    align-items: center;
    gap: 10px;
}}

/* ── STREAMLIT OVERRIDES ─────────────────────── */
.stButton > button {{
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.55rem 1.1rem !important;
    background: {t["gradient"]} !important;
    color: #fff !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 15px {t["shadow"]} !important;
}}

.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px {t["shadow"]} !important;
    opacity: 0.92 !important;
}}

.stSelectbox > div, .stTextInput > div > div {{
    border-radius: 12px !important;
    background: {t["surface2"]} !important;
    border: 1px solid {t["border"]} !important;
    color: {t["text"]} !important;
}}

.stSelectbox label, .stTextInput label, .stSlider label {{
    color: {t["muted"]} !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
}}

.stMetric {{
    background: {t["surface"]};
    border: 1px solid {t["border"]};
    border-radius: 14px;
    padding: 16px;
    box-shadow: 0 2px 12px {t["shadow"]};
}}

.stMetric label {{
    color: {t["muted"]} !important;
    font-size: 0.82rem !important;
}}

.stMetric [data-testid="metric-container"] > div {{
    color: {t["primary"]} !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
}}

/* ── DATAFRAME ───────────────────────────────── */
.stDataFrame {{
    border-radius: 14px !important;
    overflow: hidden !important;
    border: 1px solid {t["border"]} !important;
}}

/* ── EXPANDER ────────────────────────────────── */
.streamlit-expanderHeader {{
    background: {t["surface"]} !important;
    border-radius: 12px !important;
    border: 1px solid {t["border"]} !important;
    color: {t["text"]} !important;
    font-weight: 600 !important;
}}

/* ── DIVIDER ─────────────────────────────────── */
hr {{
    border-color: {t["border"]} !important;
    margin: 20px 0 !important;
}}

/* ── ALERT BOXES ─────────────────────────────── */
.stSuccess, .stInfo, .stWarning, .stError {{
    border-radius: 12px !important;
}}

/* ── FOOTER ─────────────────────────────────── */
.footer-wrap {{
    text-align: center;
    color: {t["muted"]};
    padding: 24px 0 8px;
    font-size: 0.85rem;
    border-top: 1px solid {t["border"]};
    margin-top: 48px;
}}

/* ── TREND PILL ─────────────────────────────── */
.trend-pill {{
    display: inline-block;
    background: {t["surface2"]};
    border: 1px solid {t["border"]};
    border-radius: 30px;
    padding: 6px 16px;
    font-size: 0.85rem;
    font-weight: 500;
    color: {t["text"]};
    margin: 4px;
    cursor: pointer;
    transition: all 0.2s ease;
}}

.trend-pill:hover {{
    border-color: {t["primary"]};
    color: {t["primary"]};
    background: {t["surface"]};
}}

/* ── SCROLLBAR ───────────────────────────────── */
::-webkit-scrollbar {{ width: 6px; }}
::-webkit-scrollbar-track {{ background: {t["background"]}; }}
::-webkit-scrollbar-thumb {{
    background: {t["border"]};
    border-radius: 4px;
}}
::-webkit-scrollbar-thumb:hover {{ background: {t["primary"]}; }}

</style>
"""
