from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MoodBot",
    page_icon="🤖",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Space+Mono:wght@400;700&display=swap');

/* ── Root variables ── */
:root {
    --bg:       #0d0f14;
    --surface:  #161921;
    --border:   #252a38;
    --accent:   #7b61ff;
    --accent2:  #00e5c3;
    --text:     #e2e8f0;
    --muted:    #64748b;
    --sad:      #60a5fa;
    --angry:    #f87171;
    --funny:    #facc15;
    --radius:   14px;
}

/* ── Global ── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
}

[data-testid="stHeader"] { background: transparent !important; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, [data-testid="stToolbar"] { display: none !important; }

/* ── App wrapper ── */
.block-container {
    max-width: 760px !important;
    padding: 2rem 1.5rem 6rem !important;
}

/* ── Header ── */
.hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}
.hero h1 {
    font-family: 'Space Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    letter-spacing: -1px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 .35rem;
}
.hero p {
    color: var(--muted);
    font-size: .82rem;
    margin: 0;
    letter-spacing: .05em;
}

/* ── Mode cards ── */
.mode-row {
    display: flex;
    gap: .75rem;
    margin: 1.5rem 0;
    justify-content: center;
}
.mode-card {
    flex: 1;
    max-width: 160px;
    border: 2px solid var(--border);
    border-radius: var(--radius);
    padding: .9rem .5rem;
    text-align: center;
    cursor: pointer;
    transition: all .2s ease;
    background: var(--surface);
    user-select: none;
}
.mode-card:hover { transform: translateY(-3px); }
.mode-card.active-sad    { border-color: var(--sad);   background: rgba(96,165,250,.1); }
.mode-card.active-angry  { border-color: var(--angry); background: rgba(248,113,113,.1); }
.mode-card.active-funny  { border-color: var(--funny); background: rgba(250,204,21,.1); }
.mode-icon  { font-size: 1.8rem; }
.mode-label { font-size: .7rem; letter-spacing: .1em; text-transform: uppercase; margin-top: .3rem; color: var(--muted); }

/* ── Divider ── */
.divider { border: none; border-top: 1px solid var(--border); margin: 1.25rem 0; }

/* ── Chat window ── */
.chat-window {
    display: flex;
    flex-direction: column;
    gap: .85rem;
    min-height: 60px;
    margin-bottom: 1rem;
}

/* ── Bubbles ── */
.bubble-wrap {
    display: flex;
    align-items: flex-end;
    gap: .6rem;
    animation: fadeUp .25s ease both;
}
.bubble-wrap.user  { flex-direction: row-reverse; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}

.avatar {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
    background: var(--surface);
    border: 1px solid var(--border);
}

.bubble {
    max-width: 75%;
    padding: .7rem 1rem;
    border-radius: 16px;
    font-size: .875rem;
    line-height: 1.6;
    white-space: pre-wrap;
    word-break: break-word;
}
.bubble.user {
    background: var(--accent);
    color: #fff;
    border-bottom-right-radius: 4px;
}
.bubble.bot {
    background: var(--surface);
    border: 1px solid var(--border);
    border-bottom-left-radius: 4px;
}

/* Thinking indicator */
.thinking {
    display: flex; gap: 4px; align-items: center;
    padding: .7rem 1rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    border-bottom-left-radius: 4px;
    width: fit-content;
}
.dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--muted);
    animation: bounce 1.2s infinite ease-in-out;
}
.dot:nth-child(2) { animation-delay: .2s; }
.dot:nth-child(3) { animation-delay: .4s; }
@keyframes bounce {
    0%,80%,100% { transform: translateY(0); }
    40%          { transform: translateY(-6px); background: var(--accent2); }
}

/* ── Status bar ── */
.status-bar {
    display: flex;
    align-items: center;
    gap: .5rem;
    font-size: .72rem;
    color: var(--muted);
    margin-bottom: .5rem;
    letter-spacing: .05em;
}
.status-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--accent2);
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%,100% { opacity: 1; } 50% { opacity: .3; }
}

/* ── Input area ── */
[data-testid="stChatInput"] > div {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: .25rem .5rem !important;
    font-family: 'JetBrains Mono', monospace !important;
}
[data-testid="stChatInput"] textarea {
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: .875rem !important;
}
[data-testid="stChatInput"]:focus-within > div {
    border-color: var(--accent) !important;
}

/* ── Streamlit radio (hidden, we use custom cards) ── */
[data-testid="stRadio"] { display: none !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar       { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────────────────────────
MODES = {
    "😢 Sad":   ("sad",   "You are a sad, emotional AI assistant. You respond with melancholy and empathy, often sighing."),
    "😡 Angry": ("angry", "You are an angry AI assistant. You respond with frustration and bluntness, though still helpfully."),
    "😄 Funny": ("funny", "You are a hilarious AI assistant. You crack jokes, use puns, and keep things light-hearted."),
}

def get_avatar(role: str, mode: str) -> str:
    if role == "user":
        return "👤"
    icons = {"sad": "😢", "angry": "😡", "funny": "😄"}
    return icons.get(mode, "🤖")

def render_bubble(role: str, content: str, mode: str):
    avatar = get_avatar(role, mode)
    bubble_class = "user" if role == "user" else "bot"
    wrap_class   = "user" if role == "user" else "bot"
    st.markdown(f"""
    <div class="bubble-wrap {wrap_class}">
        <div class="avatar">{avatar}</div>
        <div class="bubble {bubble_class}">{content}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
if "messages"      not in st.session_state: st.session_state.messages      = []
if "lc_messages"   not in st.session_state: st.session_state.lc_messages   = []
if "mode"          not in st.session_state: st.session_state.mode          = "funny"
if "mode_label"    not in st.session_state: st.session_state.mode_label    = "😄 Funny"
if "model"         not in st.session_state: st.session_state.model         = None
if "system_set"    not in st.session_state: st.session_state.system_set    = False


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🤖 MoodBot</h1>
    <p>PICK A MOOD · START CHATTING · TYPE "exit" TO RESET</p>
</div>
""", unsafe_allow_html=True)


# ── Mode selector ─────────────────────────────────────────────────────────────
st.markdown('<div class="mode-row">', unsafe_allow_html=True)
cols = st.columns(3)
for i, (label, (key, _)) in enumerate(MODES.items()):
    active_class = f"active-{key}" if st.session_state.mode == key else ""
    with cols[i]:
        # Invisible radio hidden by CSS; real click via button
        if st.button(label, key=f"mode_btn_{key}", use_container_width=True):
            if st.session_state.mode != key:
                st.session_state.mode        = key
                st.session_state.mode_label  = label
                st.session_state.messages    = []
                st.session_state.lc_messages = []
                st.session_state.system_set  = False
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Highlight active mode visually
mode_colors = {"sad": "#60a5fa", "angry": "#f87171", "funny": "#facc15"}
active_color = mode_colors[st.session_state.mode]
st.markdown(f"""
<div style="text-align:center; margin: -.5rem 0 1rem;">
    <span style="display:inline-block; padding:.3rem .9rem; border-radius:99px;
                 background:{active_color}22; border:1px solid {active_color};
                 color:{active_color}; font-size:.72rem; letter-spacing:.1em;">
        ● ACTIVE MODE: {st.session_state.mode_label.upper()}
    </span>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ── Lazy-init model ───────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    return init_chat_model("open-mistral-7b", model_provider="mistralai", max_tokens=200)

try:
    model = load_model()
except Exception as e:
    st.error(f"⚠️ Could not load model: {e}")
    st.stop()


# ── Status bar ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="status-bar">
    <div class="status-dot"></div>
    open-mistral-7b &nbsp;·&nbsp; {len(st.session_state.messages)} messages
</div>
""", unsafe_allow_html=True)


# ── Chat history ──────────────────────────────────────────────────────────────
st.markdown('<div class="chat-window">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    render_bubble(msg["role"], msg["content"], st.session_state.mode)
st.markdown('</div>', unsafe_allow_html=True)


# ── Input ─────────────────────────────────────────────────────────────────────
prompt = st.chat_input("Type a message…")

if prompt:
    # Handle exit
    if prompt.strip().lower() in ("exit", "stop", "quit"):
        st.session_state.messages    = []
        st.session_state.lc_messages = []
        st.session_state.system_set  = False
        st.rerun()

    # Add user bubble immediately
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Build LC message list
    if not st.session_state.system_set:
        _, system_prompt = MODES[st.session_state.mode_label]
        st.session_state.lc_messages = [SystemMessage(system_prompt)]
        st.session_state.system_set = True

    st.session_state.lc_messages.append(HumanMessage(prompt))

    # Stream / call model
    with st.spinner(""):
        try:
            response = model.invoke(st.session_state.lc_messages)
            reply = response.content.strip()
        except Exception as e:
            reply = f"⚠️ Error: {e}"

    st.session_state.lc_messages.append(AIMessage(reply))
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()