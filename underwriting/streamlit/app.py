"""
Main Streamlit application for automobile insurance underwriting.

This is the entry point for the Streamlit web interface, providing
a modern, interactive dashboard for underwriting evaluation and A/B testing.
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
from underwriting.utils.env_loader import load_environment_variables

def configure_page():
    """Configure the Streamlit page settings."""
    st.set_page_config(
        page_title="Automobile Insurance Underwriting",
        page_icon="🚗",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/your-repo/underwriting-system',
            'Report a bug': 'https://github.com/your-repo/underwriting-system/issues',
            'About': """
            # Automobile Insurance Underwriting System
            
            An AI-powered underwriting system with comprehensive A/B testing capabilities.
            <p>Work-in-Progress Portfolio Project managed by <a href="https://jeremiahconnelly.dev" target="_blank">Jeremiah Connelly</a></p>   
            
            **Features:**
            - AI-powered decision making with OpenAI GPT-4
            - Interactive evaluation forms
            - Real-time A/B testing
            - Statistical analysis and reporting
            - Modern, responsive interface
            """
        }
    )

def load_custom_css():
    """Load custom CSS for enhanced styling."""
    st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary-color: #1f77b4;
        --secondary-color: #ff7f0e;
        --success-color: #2ca02c;
        --warning-color: #d62728;
        --info-color: #17a2b8;
        --light-bg: #f8f9fa;
        --dark-bg: #343a40;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Card styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid var(--primary-color);
        margin-bottom: 1rem;
    }
    
    .metric-card h3 {
        margin: 0 0 0.5rem 0;
        color: var(--primary-color);
        font-size: 1.1rem;
    }
    
    .metric-card .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    /* Status badges */
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.875rem;
        display: inline-block;
        margin: 0.25rem;
    }
    
    .status-accept {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .status-deny {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    
    .status-adjudicate {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    
    /* Progress bars */
    .progress-container {
        background-color: #e9ecef;
        border-radius: 10px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .progress-bar {
        height: 20px;
        border-radius: 10px;
        transition: width 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 0.875rem;
    }
    
    .progress-excellent { background-color: var(--success-color); }
    .progress-good { background-color: var(--info-color); }
    .progress-fair { background-color: var(--secondary-color); }
    .progress-poor { background-color: var(--warning-color); }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: var(--light-bg);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Alert styling */
    .alert {
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        border-left: 4px solid;
    }
    
    .alert-success {
        background-color: #d4edda;
        border-color: var(--success-color);
        color: #155724;
    }
    
    .alert-warning {
        background-color: #fff3cd;
        border-color: var(--secondary-color);
        color: #856404;
    }
    
    .alert-danger {
        background-color: #f8d7da;
        border-color: var(--warning-color);
        color: #721c24;
    }
    
    .alert-info {
        background-color: #d1ecf1;
        border-color: var(--info-color);
        color: #0c5460;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

def show_sidebar():
    """Display the sidebar with navigation and system info."""
    with st.sidebar:
        #st.markdown("## 🚗 Navigation")
        
        # System status
        st.markdown("### 📊 System Status")
        
        # Check OpenAI API key
        openai_key = os.environ.get('OPENAI_API_KEY')
        if openai_key and openai_key.strip():
            st.success("✅ OpenAI API Connected")
        else:
            st.error("❌ OpenAI API Key Missing")
            st.info("Set OPENAI_API_KEY environment variable")
        
        # System metrics
        st.markdown("### 📈 Quick Stats")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Rules Loaded", "3", help="Conservative, Standard, Liberal")
        
        with col2:
            st.metric("Sample Apps", "6", help="Test applicants available")
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
        
        if st.button("📋 Sample Test", use_container_width=True):
            st.switch_page("pages/02_📋_Evaluate.py")
        
        if st.button("🧪 A/B Testing", use_container_width=True):
            st.switch_page("pages/03_🧪_AB_Testing.py")
        
        # Help section
        st.markdown("### 💡 Help")
        with st.expander("Getting Started"):
            st.markdown("""
            1. **Evaluate**: Test applicant using the evaluation form. 
            2. **A/B Test**: Compare different rule configurations
            3. **Configure**: Adjust system settings as needed
            """)
        
        with st.expander("Decision Result Types"):
            st.markdown("""
            - **✅ ACCEPTED**: The Applicant is Approved for Coverage
            - **❌ DENY**: The Application is Denied Coverage  
            - **⚖️ ADJUDICATE**: Manual review required for Applicant
            """)

def show_main_dashboard():
    """Display the main dashboard content."""
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚗 Automobile Insurance Underwriting</h1>
        <p>AI-Powered Underwriting with A/B Testing, Configurable Decisioning Rules and Applicants</p>
        <p>(WIP) Portfolio Project managed by <a href="https://jeremiahconnelly.dev" target="_blank">Jeremiah Connelly</a></p>                     
    </div>
    """, unsafe_allow_html=True)
    
    # Key features overview
    st.markdown("## 🎯 Key Features")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🤖 Agentic AI System</h3>
            <p>OpenAI GPT-4 integration for intelligent risk assessment and decisioning </p> 
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🧪 A/B Testing</h3>
            <p>Statistical comparison of different underwriting rules and strategies testing</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Real-time</h3>
            <p>Interactive evaluation with feedback and visual indicators for reviewing</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>⚙️ Configurable</h3>
            <p>Flexible rule engine designs with conservative, baseline, and liberal policies</p> 
        </div>
        """, unsafe_allow_html=True)
    
    # Quick start section
    st.markdown("## 🚀 Quick Start")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Get started in 3 easy steps:
        
        1. **📋 Evaluate Applicant**: Use the interactive form to assess insurance applications
        2. **🧪 Run A/B Tests**: Compare different underwriting strategies with statistical analysis
        3. **📊 Review Results**: Get detailed insights with visual charts and recommendations
        
        The system uses AI to analyze applicant data including credit scores, 
        driving history, vehicle information, and coverage requirements to make intelligent 
        underwriting decisions.
        """)
    
    with col2:
        st.markdown("### 🎯 Quick Actions")
        
        if st.button("📋 Start Evaluation", use_container_width=True, type="primary"):
            st.switch_page("pages/02_📋_Evaluate.py")
        
        if st.button("🧪 A/B Testing", use_container_width=True):
            st.switch_page("pages/03_🧪_AB_Testing.py")
        
        if st.button("⚙️ Configuration", use_container_width=True):
            st.switch_page("pages/04_⚙️_Configuration.py")
        
        if st.button("📚 Documentation", use_container_width=True):
            st.switch_page("pages/05_📚_Documentation.py")
    
    # System overview
    st.markdown("## 📈 System Overview")
    
    tab1, tab2, tab3 = st.tabs(["🎯 Decision Engine", "📊 Analytics", "🔧 Configuration"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 🤖 AI Decision Making
            - **OpenAI GPT-4** integration for intelligent analysis
            - **LangChain** framework for prompt engineering
            - **Pydantic** models for data validation
            - **Real-time** evaluation with instant feedback
            """)
        
        with col2:
            st.markdown("""
            #### 📋 Evaluation Criteria
            - **Credit Score** analysis (300-850 range)
            - **Driving History** violations and claims
            - **Coverage History** lapse detection
            - **Vehicle Assessment** type and value
            """)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 🧪 A/B Testing
            - **Statistical Analysis** with confidence intervals
            - **Business Impact** loss ratio calculations
            - **Rule Comparison** conservative vs liberal
            - **Prompt Testing** different AI approaches
            """)
        
        with col2:
            st.markdown("""
            #### 📊 Reporting
            - **Visual Charts** with interactive plots
            - **Export Options** JSON and CSV formats
            - **Performance Metrics** acceptance rates
            - **Risk Assessment** detailed breakdowns
            """)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### ⚙️ Rule Engine
            - **Conservative** strict acceptance criteria
            - **Standard** balanced risk approach
            - **Liberal** growth-oriented policies
            - **Custom** configurable parameters
            """)
        
        with col2:
            st.markdown("""
            #### 🔧 System Settings
            - **Environment** variables configuration
            - **API Keys** secure management
            - **Logging** comprehensive tracking
            - **Performance** optimization settings
            """)

def main():
    """Main Streamlit application entry point."""
    # Load environment variables
    load_environment_variables()
    
    # Configure page
    configure_page()
    
    # Load custom CSS
    load_custom_css()
    
    # Show sidebar
    show_sidebar()
    
    # Show main content
    show_main_dashboard()

if __name__ == "__main__":
    main()

