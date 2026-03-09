"""
Expense Tracker - A clean and modern expense tracking application
Built with Streamlit
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

DATA_DIR = "user_data"
os.makedirs(DATA_DIR, exist_ok=True)

def get_expenses_file(username: str) -> str:
    """Return the CSV path for a given username (sanitized)."""
    safe = "".join(c for c in username.strip().lower() if c.isalnum() or c in ("_", "-"))
    return os.path.join(DATA_DIR, f"{safe}.csv")

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------- CSS ----------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    font-family: 'DM Sans', sans-serif;
    background: #0d1117;
    color: #e6edf3;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #161b22;
    border-right: 1px solid #21262d;
}
section[data-testid="stSidebar"] * { color: #e6edf3 !important; }
section[data-testid="stSidebar"] .stMarkdown hr {
    border-color: #21262d;
}

/* ── Headings ── */
h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    letter-spacing: -0.5px;
}
h1 {
    font-size: 2.4rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #58a6ff 0%, #bc8cff 60%, #ff7b72 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    margin-bottom: 4px !important;
}
h3 { color: #c9d1d9 !important; font-weight: 700 !important; }

/* ── Subtitle ── */
.subtitle {
    text-align: center;
    color: #8b949e;
    font-size: 0.95rem;
    margin-bottom: 28px;
    letter-spacing: 0.3px;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: #161b22;
    padding: 6px 8px;
    border-radius: 12px;
    border: 1px solid #21262d;
    margin-bottom: 20px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: #8b949e !important;
    font-weight: 500;
    font-family: 'DM Sans', sans-serif;
    padding: 8px 18px;
    transition: all 0.2s ease;
}
.stTabs [aria-selected="true"] {
    background: #21262d !important;
    color: #e6edf3 !important;
    border-bottom: 2px solid #58a6ff !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 18px 20px !important;
    transition: border-color 0.2s;
}
[data-testid="stMetric"]:hover { border-color: #58a6ff; }
[data-testid="stMetricLabel"] { color: #8b949e !important; font-size: 0.82rem !important; text-transform: uppercase; letter-spacing: 0.8px; }
[data-testid="stMetricValue"] { color: #e6edf3 !important; font-family: 'Syne', sans-serif !important; font-size: 1.7rem !important; font-weight: 700 !important; }

/* ── Inputs ── */
.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stSelectbox div[data-baseweb="select"] > div {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 10px !important;
    color: #e6edf3 !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border-color 0.2s;
}
.stTextInput input:focus,
.stNumberInput input:focus,
.stDateInput input:focus {
    border-color: #58a6ff !important;
    box-shadow: 0 0 0 3px rgba(88,166,255,0.12) !important;
}
label { color: #8b949e !important; font-size: 0.85rem !important; font-weight: 500 !important; letter-spacing: 0.4px; }

/* ── Buttons ── */
.stButton > button {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px;
    transition: all 0.2s ease !important;
    border: none !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #1f6feb 0%, #388bfd 100%) !important;
    color: white !important;
    box-shadow: 0 4px 14px rgba(31,111,235,0.35) !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(31,111,235,0.45) !important;
}
.stButton > button:not([kind="primary"]) {
    background: #21262d !important;
    color: #e6edf3 !important;
    border: 1px solid #30363d !important;
}
.stButton > button:not([kind="primary"]):hover {
    background: #30363d !important;
    transform: translateY(-1px) !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #21262d;
}

/* ── Success / Info ── */
.stSuccess, .stInfo {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Divider ── */
hr { border-color: #21262d !important; margin: 16px 0 !important; }

/* ── Footer ── */
.footer {
    text-align: center;
    color: #484f58;
    font-size: 0.82rem;
    padding: 24px 0 8px;
    letter-spacing: 0.3px;
}

/* ── Stat badge (sidebar) ── */
.stat-badge {
    background: #21262d;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 10px 14px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.stat-label { color: #8b949e; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.6px; }
.stat-value { color: #58a6ff; font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1.05rem; }

/* ── Category pill ── */
.cat-pill {
    display: inline-block;
    background: #21262d;
    border: 1px solid #30363d;
    color: #c9d1d9;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.8rem;
    margin: 3px 2px;
}

/* ── Invisible select-row overlay button ── */
button[data-testid="baseButton-secondary"][kind="secondary"] {
    opacity: 0 !important;
    position: absolute;
    width: 100%;
    height: 100%;
    cursor: pointer;
}

/* ── Delete row card ── */
.del-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 8px;
    transition: border-color 0.18s, background 0.18s;
    cursor: pointer;
}
.del-card:hover { border-color: #30363d; background: #1c2128; }
.del-card.selected {
    border-color: #da3633 !important;
    background: rgba(218,54,51,0.06) !important;
    box-shadow: 0 0 0 1px #da3633;
}
.del-row-left { display: flex; align-items: center; gap: 14px; }
.del-icon {
    width: 38px; height: 38px;
    background: #21262d;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
}
.del-title { font-family: 'DM Sans', sans-serif; font-weight: 500; color: #e6edf3; font-size: 0.92rem; }
.del-sub   { color: #8b949e; font-size: 0.78rem; margin-top: 1px; }
.del-amount { font-family: 'Syne', sans-serif; font-weight: 700; color: #ff7b72; font-size: 1.05rem; }
.del-radio { width: 18px; height: 18px; border-radius: 50%; border: 2px solid #30363d; background: transparent; flex-shrink: 0; }
.del-radio.checked { border-color: #da3633; background: #da3633; box-shadow: 0 0 0 3px rgba(218,54,51,0.2); }

/* ── Confirm banner ── */
.confirm-banner {
    background: rgba(218,54,51,0.08);
    border: 1px solid #da3633;
    border-radius: 12px;
    padding: 16px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 12px;
}
.confirm-text { color: #ffa198; font-size: 0.9rem; font-weight: 500; }
.confirm-detail { color: #8b949e; font-size: 0.8rem; margin-top: 2px; }

/* ── Delete button override ── */
.del-btn > button {
    background: linear-gradient(135deg,#b91c1c,#da3633) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 14px rgba(218,54,51,0.35) !important;
}
.del-btn > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(218,54,51,0.5) !important;
}

</style>
""", unsafe_allow_html=True)


# ---------------------- PLOTLY THEME ----------------------
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#8b949e", size=12),
    margin=dict(l=10, r=10, t=30, b=10),
)
COLOR_SEQ = ["#58a6ff", "#bc8cff", "#ff7b72", "#3fb950", "#ffa657",
             "#79c0ff", "#d2a8ff", "#ffa198", "#56d364", "#ffb77a"]


# ---------------------- DATA FUNCTIONS ----------------------

def load_expenses(username: str):
    path = get_expenses_file(username)
    if os.path.exists(path):
        df = pd.read_csv(path)
        if not df.empty:
            df["Date"] = pd.to_datetime(df["Date"])
        return df
    return pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])


def save_expenses(df, username: str):
    path = get_expenses_file(username)
    if not df.empty:
        df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
    df.to_csv(path, index=False)


def add_expense(date, category, amount, description, username: str):
    df = load_expenses(username)
    new = pd.DataFrame({
        "Date": [date],
        "Category": [category],
        "Amount": [amount],
        "Description": [description],
    })
    df = pd.concat([df, new], ignore_index=True)
    save_expenses(df, username)
    return df


def delete_expense(index, username: str):
    df = load_expenses(username)
    df = df.drop(index).reset_index(drop=True)
    save_expenses(df, username)
    return df


def get_categories():
    return [
        "🍔 Food & Dining",
        "🚗 Transportation",
        "🛒 Shopping",
        "🏠 Housing",
        "💡 Utilities",
        "🎬 Entertainment",
        "🏥 Healthcare",
        "📚 Education",
        "✈️ Travel",
        "💰 Other",
    ]


# ---------------------- MAIN APP ----------------------

def main():

    # ── USER LOGIN ────────────────────────────────────────
    if "username" not in st.session_state:
        st.session_state.username = None

    if not st.session_state.username:
        st.markdown("<h1>💰 Expense Tracker</h1>", unsafe_allow_html=True)
        st.markdown(
            "<p class='subtitle'>Track, analyze, and master your spending</p>",
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)

        col_center, _, _ = st.columns([2, 1, 1])
        with col_center:
            st.markdown(
                "<div style='background:#161b22;border:1px solid #21262d;border-radius:16px;"
                "padding:32px 28px;max-width:420px;'>"
                "<h3 style='text-align:center;margin-bottom:4px;'>👋 Welcome!</h3>"
                "<p style='text-align:center;color:#8b949e;font-size:0.9rem;"
                "margin-bottom:20px;'>Enter your name to view or create your expense profile.</p>",
                unsafe_allow_html=True,
            )
            name_input = st.text_input("Your Name", placeholder="e.g. Alice", label_visibility="collapsed")
            if st.button("Continue →", type="primary", use_container_width=True):
                if name_input.strip():
                    st.session_state.username = name_input.strip()
                    st.rerun()
                else:
                    st.warning("Please enter your name to continue.")
            st.markdown("</div>", unsafe_allow_html=True)
        return  # Stop rendering until logged in

    username = st.session_state.username

    if "expense_date" not in st.session_state:
        st.session_state.expense_date = datetime.now().date()
    if "expense_category" not in st.session_state:
        st.session_state.expense_category = get_categories()[0]
    if "expense_amount" not in st.session_state:
        st.session_state.expense_amount = 10.0
    if "expense_description" not in st.session_state:
        st.session_state.expense_description = ""

    df = load_expenses(username)

    # ── SIDEBAR ──────────────────────────────────────────
    with st.sidebar:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<h2 style='font-family:Syne,sans-serif;font-weight:800;"
            "color:#e6edf3;text-align:center;margin-bottom:4px;'>💰 Expense<br>Tracker</h2>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<p style='text-align:center;color:#58a6ff;font-size:0.9rem;"
            f"margin-bottom:4px;font-weight:600;'>👤 {username}</p>"
            "<p style='text-align:center;color:#484f58;font-size:0.8rem;"
            "margin-bottom:12px;'>Your spending, at a glance</p>",
            unsafe_allow_html=True,
        )
        if st.button("🔄 Switch User", use_container_width=True):
            for key in ["username", "expense_date", "expense_category",
                        "expense_amount", "expense_description",
                        "delete_idx", "delete_confirm"]:
                st.session_state.pop(key, None)
            st.rerun()
        st.markdown("---")

        if not df.empty:
            total = df["Amount"].sum()
            avg = df["Amount"].mean()
            count = len(df)
            st.markdown(
                f"""
                <div class='stat-badge'>
                  <span class='stat-label'>Total Spent</span>
                  <span class='stat-value'>${total:,.2f}</span>
                </div>
                <div class='stat-badge'>
                  <span class='stat-label'>Transactions</span>
                  <span class='stat-value'>{count}</span>
                </div>
                <div class='stat-badge'>
                  <span class='stat-label'>Avg per Entry</span>
                  <span class='stat-value'>${avg:,.2f}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<p style='color:#484f58;font-size:0.85rem;text-align:center;"
                "padding:12px;'>No expenses yet.<br>Add your first one →</p>",
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown(
            "<p style='color:#8b949e;font-size:0.78rem;text-transform:uppercase;"
            "letter-spacing:0.8px;margin-bottom:10px;'>Categories</p>",
            unsafe_allow_html=True,
        )
        pills_html = "".join(
            f"<span class='cat-pill'>{cat}</span>" for cat in get_categories()
        )
        st.markdown(pills_html, unsafe_allow_html=True)

    # ── HEADER ───────────────────────────────────────────
    st.markdown("<h1>💰 Expense Tracker</h1>", unsafe_allow_html=True)
    st.markdown(
        f"<p class='subtitle'>Welcome back, <strong style='color:#58a6ff'>{username}</strong> — Track, analyze, and master your spending</p>",
        unsafe_allow_html=True,
    )

    # ── TABS ─────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["➕ Add Expense", "📋 All Expenses", "📊 Analytics"])

    # ── ADD EXPENSE ──────────────────────────────────────
    with tab1:
        st.markdown("### Add New Expense")
        col1, col2 = st.columns(2, gap="large")

        with col1:
            date = st.date_input("📅  Date", st.session_state.expense_date)
            category = st.selectbox("🏷️  Category", get_categories())

        with col2:
            amount = st.number_input("💵  Amount ($)", min_value=0.01, value=10.0, step=0.01)
            description = st.text_input("📝  Description", placeholder="What did you spend on?")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("＋  Add Expense", type="primary", use_container_width=True):
            if amount > 0:
                add_expense(date, category, amount, description, username)
                st.success("✅ Expense added successfully!")
                st.rerun()

    # ── ALL EXPENSES ─────────────────────────────────────
    with tab2:
        if df.empty:
            st.info("📭 No expenses recorded yet. Start by adding one!")
        else:
            total = df["Amount"].sum()
            avg = df["Amount"].mean()
            count = len(df)
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Spent", f"${total:,.2f}")
            c2.metric("Average", f"${avg:,.2f}")
            c3.metric("Transactions", count)

            st.markdown("<br>", unsafe_allow_html=True)

            display_df = df.copy()
            display_df["Date"] = display_df["Date"].dt.strftime("%b %d, %Y")
            display_df["Amount"] = display_df["Amount"].apply(lambda x: f"${x:,.2f}")
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Date": st.column_config.TextColumn("📅 Date", width=120),
                    "Category": st.column_config.TextColumn("🏷️ Category", width=180),
                    "Amount": st.column_config.TextColumn("💵 Amount", width=110),
                    "Description": st.column_config.TextColumn("📝 Description"),
                },
            )

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 🗑️ Delete an Expense")
            st.markdown(
                "<p style='color:#8b949e;font-size:0.85rem;margin-bottom:16px;'>"
                "Select a record below, then confirm deletion.</p>",
                unsafe_allow_html=True,
            )

            # Session state for selected delete index & confirm step
            if "delete_idx" not in st.session_state:
                st.session_state.delete_idx = None
            if "delete_confirm" not in st.session_state:
                st.session_state.delete_confirm = False

            CAT_ICONS = {
                "Food": "🍔", "Transportation": "🚗", "Shopping": "🛒",
                "Housing": "🏠", "Utilities": "💡", "Entertainment": "🎬",
                "Healthcare": "🏥", "Education": "📚", "Travel": "✈️", "Other": "💰",
            }

            def get_icon(cat):
                for k, v in CAT_ICONS.items():
                    if k.lower() in cat.lower():
                        return v
                return "💰"

            # Render one clickable card per row
            for i in range(len(df)):
                row = df.iloc[i]
                is_sel = st.session_state.delete_idx == i
                card_cls = "del-card selected" if is_sel else "del-card"
                radio_cls = "del-radio checked" if is_sel else "del-radio"
                icon = get_icon(row["Category"])
                date_str = row["Date"].strftime("%b %d, %Y")
                desc = row["Description"] if pd.notna(row["Description"]) and str(row["Description"]).strip() else "No description"

                col_card, col_btn = st.columns([11, 1])
                with col_card:
                    st.markdown(
                        f"""<div class='{card_cls}'>
                          <div class='del-row-left'>
                            <div class='del-icon'>{icon}</div>
                            <div>
                              <div class='del-title'>{row['Category']}</div>
                              <div class='del-sub'>{date_str} &nbsp;·&nbsp; {desc}</div>
                            </div>
                          </div>
                          <div style='display:flex;align-items:center;gap:16px;'>
                            <span class='del-amount'>${row['Amount']:,.2f}</span>
                            <div class='{radio_cls}'></div>
                          </div>
                        </div>""",
                        unsafe_allow_html=True,
                    )
                with col_btn:
                    # Invisible select button overlapping the card
                    if st.button("select", key=f"sel_{i}", help="Select this record",
                                 use_container_width=True):
                        st.session_state.delete_idx = i
                        st.session_state.delete_confirm = False
                        st.rerun()

            # Confirmation banner
            if st.session_state.delete_idx is not None:
                sel = df.iloc[st.session_state.delete_idx]
                sel_date = sel["Date"].strftime("%b %d, %Y")
                sel_desc = sel["Description"] if pd.notna(sel["Description"]) and str(sel["Description"]).strip() else "No description"

                st.markdown(
                    f"""<div class='confirm-banner'>
                      <div>
                        <div class='confirm-text'>⚠️ Delete this entry?</div>
                        <div class='confirm-detail'>{sel_date} &nbsp;·&nbsp; {sel['Category']} &nbsp;·&nbsp; {sel_desc}</div>
                      </div>
                      <div style='font-family:Syne,sans-serif;font-weight:700;color:#ff7b72;font-size:1.1rem;'>
                        ${sel['Amount']:,.2f}
                      </div>
                    </div>""",
                    unsafe_allow_html=True,
                )
                st.markdown("<br>", unsafe_allow_html=True)

                c_confirm, c_cancel, _ = st.columns([2, 2, 6])
                with c_confirm:
                    st.markdown("<div class='del-btn'>", unsafe_allow_html=True)
                    if st.button("🗑️  Yes, Delete", use_container_width=True, type="primary"):
                        delete_expense(st.session_state.delete_idx, username)
                        st.session_state.delete_idx = None
                        st.session_state.delete_confirm = False
                        st.success("✅ Record deleted successfully.")
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                with c_cancel:
                    if st.button("✕  Cancel", use_container_width=True):
                        st.session_state.delete_idx = None
                        st.session_state.delete_confirm = False
                        st.rerun()

    # ── ANALYTICS ────────────────────────────────────────
    with tab3:
        if df.empty:
            st.info("📊 No data yet — add some expenses to see your analytics!")
        else:
            total = df["Amount"].sum()
            avg = df["Amount"].mean()
            max_exp = df["Amount"].max()
            min_exp = df["Amount"].min()

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Spent", f"${total:,.2f}")
            c2.metric("Average", f"${avg:,.2f}")
            c3.metric("Highest", f"${max_exp:,.2f}")
            c4.metric("Lowest", f"${min_exp:,.2f}")

            st.markdown("<br>", unsafe_allow_html=True)

            chart1, chart2 = st.columns(2, gap="large")

            with chart1:
                st.markdown("#### Spending by Category")
                category_sum = df.groupby("Category")["Amount"].sum().reset_index()
                fig1 = px.pie(
                    category_sum,
                    values="Amount",
                    names="Category",
                    hole=0.55,
                    color_discrete_sequence=COLOR_SEQ,
                )
                fig1.update_traces(
                    textfont_color="#e6edf3",
                    marker=dict(line=dict(color="#0d1117", width=2)),
                )
                fig1.update_layout(
                    **PLOTLY_LAYOUT,
                    legend=dict(font=dict(color="#8b949e", size=11), bgcolor="rgba(0,0,0,0)"),
                    annotations=[dict(
                        text=f"<b>${total:,.0f}</b>",
                        x=0.5, y=0.5,
                        font=dict(size=18, color="#e6edf3", family="Syne"),
                        showarrow=False,
                    )],
                )
                st.plotly_chart(fig1, use_container_width=True)

            with chart2:
                st.markdown("#### Monthly Spending")
                df_copy = df.copy()
                df_copy["Month"] = pd.to_datetime(df_copy["Date"]).dt.to_period("M").astype(str)
                monthly = df_copy.groupby("Month")["Amount"].sum().reset_index()
                fig2 = px.bar(
                    monthly,
                    x="Month",
                    y="Amount",
                    color_discrete_sequence=["#1f6feb"],
                )
                fig2.update_traces(
                    marker_line_width=0,
                    marker_color="#1f6feb",
                    marker_opacity=0.85,
                )
                fig2.update_layout(
                    **PLOTLY_LAYOUT,
                    xaxis=dict(showgrid=False, tickfont=dict(color="#8b949e")),
                    yaxis=dict(
                        gridcolor="#21262d",
                        tickprefix="$",
                        tickfont=dict(color="#8b949e"),
                    ),
                    bargap=0.3,
                )
                st.plotly_chart(fig2, use_container_width=True)

            # Top category highlight
            if len(category_sum) > 0:
                top_cat = category_sum.loc[category_sum["Amount"].idxmax()]
                top_pct = (top_cat["Amount"] / total) * 100
                st.markdown(
                    f"<p style='color:#8b949e;font-size:0.9rem;text-align:center;"
                    f"margin-top:-10px;'>Top spending category: "
                    f"<span style='color:#58a6ff;font-weight:600;'>{top_cat['Category']}</span>"
                    f" — <span style='color:#e6edf3;'>${top_cat['Amount']:,.2f}</span>"
                    f" ({top_pct:.1f}% of total)</p>",
                    unsafe_allow_html=True,
                )

    # ── FOOTER ───────────────────────────────────────────
    st.markdown("---")
    st.markdown(
        "<div class='footer'>Built with Streamlit &nbsp;·&nbsp; Expense Tracker</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
