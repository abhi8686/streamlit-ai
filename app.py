import streamlit as st
from drive_manager import list_data_files
from workflow import generate_response
from datetime import datetime

# --- Streamlit Configuration ---
st.set_page_config(page_title="Health Tutor Console", layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom styling */
    .stApp {
        background-color: white;
    }
    
    [data-testid="stSidebar"] {
        background-color: #EFEFEF;
        width: 20vw;
        min-width: 20vw;
    }
    
    [data-testid="stSidebar"][aria-expanded="true"] {
        width: 20vw;
        min-width: 20vw;
    }

    .stMain {
        padding-right: 20vw;
    }
    
    .main-container {
        background-color: white;
        padding: 2rem 3rem;
        border-radius: 10px;
        margin: 1rem;
        margin-right: 20vw;
    }
    
    .greeting-header {
        font-size: 2.5rem;
        font-weight: 600;
        color: #1E1E1E;
        margin-bottom: 0.3rem;
    }
    
    .date-display {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    
    .action-button {
        background: white;
        border: 2px solid #E0E0E0;
        border-radius: 10px;
        padding: 1rem 1.5rem;
        font-size: 1.05rem;
        width: 100%;
        text-align: left;
        cursor: pointer;
        transition: all 0.2s;
        color: #1E1E1E;
    }
    
    .action-button:hover {
        border-color: #4A90E2;
        box-shadow: 0 2px 8px rgba(74, 144, 226, 0.2);
    }
    
    .stButton > button {
        background: white;
        border: 2px solid #E0E0E0;
        border-radius: 10px;
        padding: 1rem 1.5rem;
        font-size: 1.05rem;
        width: 100%;
        color: #1E1E1E;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        border-color: #4A90E2;
        box-shadow: 0 2px 8px rgba(74, 144, 226, 0.2);
        background: white;
    }
    
    .alert-box {
        background-color: #E3F2FD;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .alert-count {
        font-size: 2rem;
        color: #E74C3C;
        font-weight: 600;
    }
    
    .sidebar-section {
        margin-bottom: 2rem;
    }
    
    .chat-message {
        background-color: #F5F5F5;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .right-sidebar {
        background-color: #dceaf7;
        padding: 2rem 1.5rem;
        border-radius: 10px;
        min-height: 100vh;
    }

    .stAppHeader {
    display: none;
    }
    
    /* Apply background to the entire right column container */
    .element-container:has(.right-sidebar) {
        background-color: #dceaf7 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialize Session State ---
if "sessions" not in st.session_state:
    st.session_state.sessions = {"Session 1": []}
if "current_session" not in st.session_state:
    st.session_state.current_session = "Session 1"
if "preset_query" not in st.session_state:
    st.session_state.preset_query = None
if "show_chat" not in st.session_state:
    st.session_state.show_chat = False

# --- Sidebar: Saved Chats & Documents ---
with st.sidebar:
    st.markdown("### 💬 Saved Chats")
    
    
    # Session management
    # for session_name in st.session_state.sessions.keys():
    #     if st.button(session_name, key=f"session_{session_name}"):
    #         st.session_state.current_session = session_name
    #         st.session_state.show_chat = True
    #         st.rerun()
    
    # st.divider()
    
    # st.markdown("### 📂 Current Documents")
    # files = list_data_files()
    
    # if not files:
    #     st.info("No documents found")
    # else:
    #     for f in files:
    #         st.markdown(f"📄 {f['name']}")

# --- Main Content ---
active_messages = st.session_state.sessions[st.session_state.current_session]

# Get current date
now = datetime.now()
day_name = now.strftime("%A")
month_name = now.strftime("%B")
day = now.day
year = now.year
# Right panel CSS (shown on all screens)
st.markdown("""
<style>
.right-panel {
    position: fixed;
    top: 0px; 
    right: 0px;
    width: 20vw;
    background: #dceaf7;
    padding: 2rem 1.5rem;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.2);
    z-index: 999;
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}

.right-panel .alert-section {
    background-color: #dceaf7;
    padding: 2rem;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 3rem;
    width: 100%;
}

.right-panel .alert-icon {
    font-size: 3rem;
    margin-bottom: 0.5rem;
}

.right-panel .alert-count {
    font-size: 2rem;
    color: #E74C3C;
    font-weight: 600;
}

.right-panel .action-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 2rem;
    font-size: 1.1rem;
    color: #1E1E1E;
    font-weight: 500;
    width: 100%;
}

.right-panel .action-icon {
    font-size: 2rem;
    flex-shrink: 0;
}
</style>
""", unsafe_allow_html=True)

# Right panel HTML (shown on all screens)
st.markdown("""
<div class="right-panel">
    <div class="alert-section">
        <div class="alert-icon">📢</div>
        <div class="alert-count">2 Alerts</div>
    </div>
    <div class="action-item">
        <div class="action-icon">🔬</div>
        <span>Share with Carepod</span>
    </div>
    <div class="action-item">
        <div class="action-icon">📸</div>
        <span>Add Health Photos</span>
    </div>
    <div class="action-item">
        <div class="action-icon">📊</div>
        <span>View Dashboard</span>
    </div>
</div>
""", unsafe_allow_html=True)
# Check if we should show chat interface or home screen
if st.session_state.show_chat or len(active_messages) > 0:
    # Show chat interface
    st.markdown("# Health Tutor Console")
    
    # Display chat messages
    for message in active_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    chat_input = st.chat_input("Enter your medical question:")
    
    # Process query
    query = None
    if st.session_state.preset_query:
        query = st.session_state.preset_query
        st.session_state.preset_query = None
    elif chat_input:
        query = chat_input
    
    if query:
        st.session_state.show_chat = True
        active_messages.append({"role": "user", "content": query})
        
        with st.chat_message("user"):
            st.markdown(query)
        
        with st.chat_message("assistant"):
            with st.spinner("Claude is thinking..."):
                answer = generate_response(query)
            st.markdown(answer)
        
        active_messages.append({"role": "assistant", "content": answer})
        st.session_state.sessions[st.session_state.current_session] = active_messages
        st.rerun()
else:
    # Show home screen with action buttons
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f'<h1 class="greeting-header">Hello Alex!</h1>', unsafe_allow_html=True)
        st.markdown(f'<p class="date-display">☀️ {day_name}, {month_name} {day}, {year}</p>', unsafe_allow_html=True)
        
        st.markdown("### Quick Actions")
        
        # Action buttons
        if st.button("📅 Give me my 30-day health report"):
            st.session_state.preset_query = "Give me my 30-day health report"
            st.session_state.show_chat = True
            st.rerun()
        
        if st.button("🏥 Help me prepare for a Care Provider visit"):
            st.session_state.preset_query = "Help me prepare for a Care Provider visit"
            st.session_state.show_chat = True
            st.rerun()
        
        if st.button("❤️ Give me my heart health status"):
            st.session_state.preset_query = "Give me my heart health status"
            st.session_state.show_chat = True
            st.rerun()
        
        if st.button("📄 Explain my Alerts"):
            st.session_state.preset_query = "Explain my Alerts"
            st.session_state.show_chat = True
            st.rerun()


