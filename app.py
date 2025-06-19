import streamlit as st
import json
import urllib.parse
#from langchain.chat_models import ChatOpenAI
#from langchain.schema import SystemMessage, HumanMessage, AIMessage
import os

st.set_page_config(page_title="Credit Card Recommender", layout="centered")
st.markdown("""
    <style>
    html, body, .main {background-color: #181A20 !important; color: #F5F6FA !important;}
    .stButton>button {
        background-color: #00B8D9 !important;
        color: #fff !important;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1.1em;
        border: none;
        padding: 0.6em 1.5em;
        margin: 0.5em 0;
        box-shadow: 0 2px 8px #0002;
        transition: background 0.2s;
    }
    .stButton>button:hover {
        background-color: #36D399 !important;
        color: #181A20 !important;
    }
    /* Special style for Compare button */
    .compare-btn button {
        background-color: #fff !important;
        color: #181A20 !important;
        font-weight: 800 !important;
        border-radius: 10px !important;
        border: none !important;
        font-size: 1.1em !important;
        box-shadow: 0 2px 8px #0003;
        margin: 0.5em 0;
    }
    .compare-btn button:hover {
        background-color: #00B8D9 !important;
        color: #fff !important;
    }
    /* WhatsApp Button */
    .whatsapp-btn {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background-color: #25D366;
        padding: 12px;
        border-radius: 50%;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        width: 60px;
        height: 60px;
    }
    .whatsapp-btn:hover {
        background-color: #128C7E;
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
    }
    .whatsapp-btn svg {
        width: 32px;
        height: 32px;
    }
    .stChatMessage {
        background-color: #23272F !important;
        color: #F5F6FA !important;
        border-radius: 10px;
        margin-bottom: 10px;
        font-size: 1.1em;
        padding: 0.7em 1em;
        box-shadow: 0 2px 8px #0003;
    }
    .card-container {
        background: #23272F;
        border-radius: 16px;
        box-shadow: 0 4px 16px #0004;
        padding: 1.5em 1.2em;
        margin-bottom: 1.5em;
        color: #F5F6FA;
    }
    .card-container.selected {
        border: 2px solid #00B8D9;
        box-shadow: 0 0 0 4px #00b8d933;
    }
    .summary-container {
        background: #23272F;
        border-radius: 16px;
        box-shadow: 0 2px 12px #0003;
        padding: 1.2em 1em;
        margin-bottom: 2em;
        color: #F5F6FA;
        font-size: 1.13em;
    }
    .stMarkdown, .stText, .stSubheader, .stTable, .stImage, .stDivider {
        color: #F5F6FA !important;
        font-size: 1.08em;
    }
    .stTable {background-color: #23272F !important; color: #fff !important;}
    th {background-color: #23272F !important; color: #fff !important; font-weight: 800 !important;}
    td {color: #fff !important;}
    /* Headings */
    h1, .stApp h1, .stApp .stMarkdown h1, .stApp .stTitle {
        color: #fff !important;
        font-weight: 900 !important;
        letter-spacing: 0.5px;
    }
    h2, .stApp h2, .stApp .stMarkdown h2, .stApp .stSubheader {
        color: #fff !important;
        font-weight: 800 !important;
        letter-spacing: 0.2px;
    }
    h3, .stApp h3, .stApp .stMarkdown h3 {
        color: #fff !important;
        font-weight: 700 !important;
    }
    </style>
    
    <script>
    function openWhatsApp() {
        const number = "YOUR_PHONE_NUMBER";
        const message = "Hi! I'm interested in getting a credit card recommendation.";
        const url = `https://wa.me/${number}?text=${encodeURIComponent(message)}`;
        window.open(url, '_blank');
    }
    </script>
    """, unsafe_allow_html=True)

# Simple WhatsApp icon SVG
whatsapp_icon = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white">
    <path d="M12 0C5.373 0 0 5.373 0 12c0 2.625.846 5.059 2.284 7.034L.153 23.486l4.6-1.477A11.925 11.925 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zM8.441 6.356c.194-.338.446-.338.446-.338.338 0 1.085.048 1.674.048.59 0 1.179-.048 1.516-.048 0 0 .253 0 .446.338.194.337.641 1.157.641 2.314 0 1.157-.447 2.314-.447 2.314 0 0-.59.917-1.179.917-.59 0-1.179-.338-1.516-.338-.337 0-.926.338-1.516.338-.59 0-1.179-.917-1.179-.917s-.446-1.157-.446-2.314c0-1.157.447-1.977.641-2.314zm7.516 7.516c-.59 1.516-2.952 2.794-4.857 2.952-1.905.159-3.81-.579-3.81-.579l-2.313.772.772-2.313s-.738-1.905-.579-3.81c.159-1.905 1.436-4.268 2.952-4.857 1.516-.59 4.857-.252 6.373 1.264 1.515 1.516 1.853 4.857 1.264 6.373z"/>
</svg>
"""

st.markdown(f"""
    <div class="whatsapp-btn" onclick="openWhatsApp()">
        {whatsapp_icon}
    </div>
""", unsafe_allow_html=True)

st.title("🧑‍💼 Credit Card Recommendation Agent")

# Load card data
with open("card_data.json", "r") as f:
    cards = json.load(f)

# Session state for chat and user profile
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "profile" not in st.session_state:
    st.session_state["profile"] = {}
if "step" not in st.session_state:
    st.session_state["step"] = 0
if "show_compare" not in st.session_state:
    st.session_state["show_compare"] = False

# Define the Q&A flow
questions = [
    ("monthly_income", "What is your approximate monthly income (in Rs.)?"),
    ("spending_habits", "What are your main spending categories? (fuel, travel, groceries, dining, shopping, etc.)"),
    ("preferred_benefits", "What benefits do you prefer? (cashback, travel points, lounge access, etc.)"),
    ("existing_cards", "Do you already have any credit cards? (optional, you can skip)"),
    ("credit_score", "What is your approximate credit score? (or type 'unknown')")
]

# Display chat history (only user answers)
for i, msg in enumerate(st.session_state["messages"]):
    st.chat_message(msg["role"]).write(msg["content"])

# Q&A logic
if st.session_state["step"] < len(questions):
    key, q = questions[st.session_state["step"]]
    user_input = st.chat_input(q)
    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        st.session_state["profile"][key] = user_input
        st.session_state["step"] += 1
        st.experimental_rerun()
else:
    profile = st.session_state["profile"]
    income = int(''.join(filter(str.isdigit, profile.get("monthly_income", "0"))))
    benefits = profile.get("preferred_benefits", "").lower()
    spending = profile.get("spending_habits", "").lower()
    # Filter cards by eligibility and benefits
    def eligible(card):
        try:
            min_income = int(''.join(filter(str.isdigit, card["eligibility"])))
            return income >= min_income
        except:
            return True
    def matches_benefit(card):
        return any(b.strip() in card["perks"] or b.strip() in card["reward_type"].lower() for b in benefits.split(","))
    filtered = [c for c in cards if eligible(c) and matches_benefit(c)]
    if not filtered:
        filtered = [c for c in cards if eligible(c)]
    top_cards = filtered[:3]

    # --- Summary Section ---
    st.markdown('<div class="summary-container">', unsafe_allow_html=True)
    st.subheader("Your Profile Summary")
    st.markdown(f"**Monthly Income:** Rs. {profile.get('monthly_income','-')}")
    st.markdown(f"**Spending Habits:** {profile.get('spending_habits','-')}")
    st.markdown(f"**Preferred Benefits:** {profile.get('preferred_benefits','-')}")
    st.markdown(f"**Existing Cards:** {profile.get('existing_cards','-')}")
    st.markdown(f"**Credit Score:** {profile.get('credit_score','-')}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("Top Credit Card Recommendations")
    compare_selection = []
    for idx, card in enumerate(top_cards):
        selected = False
        if st.session_state.get("show_compare") and st.session_state.get("compare_cards"):
            selected = card in st.session_state["compare_cards"]
        card_container_class = "card-container selected" if selected else "card-container"
        st.markdown(f'<div class="{card_container_class}">', unsafe_allow_html=True)
        col1, col2 = st.columns([1,3])
        with col1:
            st.image(card["image_url"], width=100)
        with col2:
            st.markdown(f"### {card['name']} ({card['issuer']})")
            st.markdown(f"- **Joining Fee:** Rs. {card['joining_fee']}")
            st.markdown(f"- **Annual Fee:** Rs. {card['annual_fee']}")
            st.markdown(f"- **Perks:** {', '.join(card['perks'])}")
            st.markdown(f"- **Reward Type:** {card['reward_type']} ({card['reward_rate']})")
            st.markdown(f"- [Apply Now]({card['affiliate_link']})")
            # Why recommended
            reasons = []
            if matches_benefit(card):
                reasons.append("Matches your preferred benefits")
            if eligible(card):
                reasons.append("Eligible based on your income")
            if any(s in card["perks"] or s in card["reward_type"].lower() for s in spending.split(",")):
                reasons.append("Good for your spending habits")
            st.markdown(f"**Why recommended:** {'; '.join(reasons) if reasons else 'Best match from our database.'}")
            # Reward simulation (simple)
            est_reward = 0
            if "cashback" in card["reward_type"].lower() or "cashback" in card["perks"]:
                est_reward = income * 0.03 * 12  # Assume 3% cashback on monthly income spent
            elif "points" in card["reward_type"].lower():
                est_reward = income * 0.01 * 12  # Assume 1% value for points
            st.markdown(f"**Estimated Annual Reward:** Rs. {int(est_reward):,}")
            # Compare checkbox
            if st.checkbox(f"Compare this card", key=f"compare_{idx}"):
                compare_selection.append(card)
        st.markdown('</div>', unsafe_allow_html=True)

    # Compare Cards Button
    if compare_selection:
        with st.container():
            compare_btn = st.button("Compare Selected Cards", key="compare_btn", help="Compare the selected cards", use_container_width=True)
        if compare_btn:
            st.session_state["show_compare"] = True
            st.session_state["compare_cards"] = compare_selection
            st.experimental_rerun()

    # Comparison Table
    if st.session_state.get("show_compare") and st.session_state.get("compare_cards"):
        st.subheader("Card Comparison Table")
        compare_cards = st.session_state["compare_cards"]
        headers = ["Name", "Issuer", "Joining Fee", "Annual Fee", "Perks", "Reward Type", "Eligibility"]
        rows = []
        for c in compare_cards:
            rows.append([
                c["name"], c["issuer"], f"Rs. {c['joining_fee']}", f"Rs. {c['annual_fee']}", ', '.join(c['perks']), f"{c['reward_type']} ({c['reward_rate']})", c['eligibility']
            ])
        st.table([headers] + rows)
        if st.button("Back to Recommendations"):
            st.session_state["show_compare"] = False
            st.session_state["compare_cards"] = []
            st.experimental_rerun()

    # Option to restart
    if st.button("Restart Recommendation Journey"):
        st.session_state["messages"] = []
        st.session_state["profile"] = {}
        st.session_state["step"] = 0
        st.session_state["show_compare"] = False
        st.session_state["compare_cards"] = []
        st.experimental_rerun() 