# Streamlit CrewAI Chatbot with Sources and Contact Information
# Simple UI chatbot that shows sources and detailed contact info

import streamlit as st
import os
from datetime import datetime
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="AI Chatbot Assistant",
    page_icon="🤖",
    layout="wide"
)

# =============================================================================
# SETUP FUNCTIONS
# =============================================================================

@st.cache_resource
def setup_tools():
    """Setup web tools for the chatbot"""
    try:
        search_tool = SerperDevTool(
            description="Search the web for current information with sources"
        )
        scrape_tool = ScrapeWebsiteTool(
            description="Extract detailed content from websites"
        )
        return [search_tool, scrape_tool]
    except Exception as e:
        st.error(f"Error setting up tools: {str(e)}")
        return []

@st.cache_resource
def setup_llm():
    """Setup Groq LLM with proper configuration"""
    try:
        # Ensure API key is set
        if not os.getenv("GROQ_API_KEY"):
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        return LLM(
            model="groq/meta-llama/llama-4-scout-17b-16e-instruct",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.7,
            timeout=60
        )
    except Exception as e:
        st.error(f"Error setting up LLM: {str(e)}")
        return None

def create_research_agent(llm, tools):
    """Create agent that provides detailed info with sources"""
    if not llm or not tools:
        return None
        
    try:
        agent = Agent(
            role="Research Assistant with Source Citation",
            goal="Provide detailed, accurate information with proper source citations and contact details",
            backstory="""
            You are a professional research assistant who:
            - Check for the historical context of the query if only relevant with the query
            - Always provides accurate and detailed information
            - infomration is up-to-date and relevant
            - Uses web search tools to find current information
            - searches to up to date information in the current time if specified in the query
            - try to search for the most recent information available
            - Scrapes websites for detailed content when necessary
            - Always provides sources for your information
            - Includes contact details when available (names, phone numbers, addresses, emails)
            - Gives comprehensive answers with specific details
            - Cites websites, articles, and sources used
            - When searching for professionals (doctors, lawyers, etc.), includes their names and contact info
            - Formats responses clearly with sources at the end
            """,
            tools=tools,
            llm=llm,
            verbose=False,
            allow_delegation=False
        )
        return agent
    except Exception as e:
        st.error(f"Error creating agent: {str(e)}")
        return None

# =============================================================================
# CHAT HISTORY MANAGEMENT
# =============================================================================

def initialize_chat_history():
    """Initialize chat history in session state"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def add_to_history(user_msg, bot_msg):
    """Add conversation to history"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.chat_history.append({
        "timestamp": timestamp,
        "user": user_msg,
        "bot": bot_msg
    })

def get_context_from_history():
    """Get recent conversation context"""
    if not st.session_state.chat_history:
        return ""
    
    recent_chats = st.session_state.chat_history[-3:]  # Last 3 conversations
    context = "Previous conversation context:\n"
    for chat in recent_chats:
        context += f"User: {chat['user']}\n"
        context += f"Assistant: {chat['bot'][:200]}...\n\n"
    return context

# =============================================================================
# MAIN CHATBOT FUNCTION
# =============================================================================

def get_chatbot_response(user_message, agent):
    """Get response from chatbot with sources"""
    
    if not agent:
        return "Error: Agent not properly initialized. Please check your API keys."
    
    try:
        context = get_context_from_history()
        
        full_prompt = f"""
        {context}
        
        Current user question: {user_message}
        
        Instructions:
        - You are a professional research assistant
        - Use web search tools to find current information
        - Scrape websites for detailed content when necessary
        - Always provide sources for your information
        - If the query is about a specific location, include relevant local information
        - Try to find the most recent information available
        - Try to find information that is up-to-date and relevant according the timeframe of the query
        - Provide detailed, helpful information
        - Always include sources and citations
        - If searching for professionals (doctors, lawyers, restaurants, etc.), include:
          * Names of specific people/businesses
          * Contact information (phone, address, email if available)
          * Professional credentials or specialties
        - Format your response clearly Don't Include think in it.
        - End with a "Sources:" section listing all websites/sources used
        - Be specific and comprehensive in your answers
        - give output in a way that is easy to read and understand and good for the user
        """
        
        task = Task(
            description=full_prompt,
            agent=agent,
            expected_output="Detailed response with sources and contact information when applicable"
        )
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=False
        )
        
        result = crew.kickoff()
        return str(result)
        
    except Exception as e:
        error_msg = f"I encountered an error: {str(e)}"
        if "API key" in str(e).lower():
            error_msg += "\n\nPlease check that your API keys are correctly set in the .env file."
        elif "timeout" in str(e).lower():
            error_msg += "\n\nThe request timed out. Please try again."
        elif "rate limit" in str(e).lower():
            error_msg += "\n\nRate limit exceeded. Please wait a moment and try again."
        return error_msg

# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_api_keys():
    """Validate that required API keys are present"""
    groq_key = os.getenv("GROQ_API_KEY")
    serper_key = os.getenv("SERPER_API_KEY")
    
    missing_keys = []
    if not groq_key:
        missing_keys.append("GROQ_API_KEY")
    if not serper_key:
        missing_keys.append("SERPER_API_KEY")
    
    return len(missing_keys) == 0, missing_keys

# =============================================================================
# STREAMLIT UI
# =============================================================================

def main():
    """Main Streamlit application"""
    
    # Title and description
    st.title("🤖 AI Research Assistant")
    st.write("Ask me anything! I'll provide detailed information with sources and contact details.")
    
    # Sidebar for information and controls
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Check API keys
        keys_valid, missing_keys = validate_api_keys()
        
        if keys_valid:
            st.success("✅ API keys loaded from environment")
        else:
            st.error("❌ Missing API keys")
        
        st.write("---")
        st.header("💡 Example Queries")
        st.write("• Find doctors in New York")
        st.write("• Latest AI news")
        st.write("• Best restaurants in Paris")
        st.write("• Python programming tutorials")
        
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
            st.rerun()
    
    # Initialize components
    initialize_chat_history()
    
    # Check if API keys are set
    if not keys_valid:
        st.warning("⚠️ Please set the required API keys in your .env file!")
        st.stop()
    
    # Setup chatbot components
    with st.spinner("Initializing AI components..."):
        tools = setup_tools()
        llm = setup_llm()
        agent = create_research_agent(llm, tools)
    
    if not agent:
        st.error("Failed to initialize the AI agent. Please check your configuration and try again.")
        st.stop()
    
    # Chat interface
    st.write("---")
    
    # Display chat history
    if st.session_state.chat_history:
        st.subheader("💬 Conversation History")
        
        for i, chat in enumerate(st.session_state.chat_history):
            with st.container():
                col1, col2 = st.columns([1, 10])
                with col1:
                    st.write(f"**{chat['timestamp']}**")
                with col2:
                    st.write(f"**You:** {chat['user']}")
                    with st.expander("View Response", expanded=(i == len(st.session_state.chat_history)-1)):
                        st.write(chat['bot'])
                st.write("---")
    
    # Input section
    st.subheader("💭 Ask me anything!")
    
    # Create input form
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Your message:",
            height=100,
            placeholder="Type your question here... (e.g., 'Find cardiologists in Boston with their contact details')"
        )
        
        col1, col2, col3 = st.columns([1, 1, 8])
        with col1:
            submit_button = st.form_submit_button("Send 📤")
        with col2:
            example_button = st.form_submit_button("Example Query")
    
    # Handle example query
    if example_button:
        user_input = "Find top 3 dermatologists in Los Angeles with their names and contact information"
        submit_button = True
    
    # Process user input
    if submit_button and user_input.strip():
        with st.spinner("🔍 Researching and gathering information..."):
            
            # Get response
            response = get_chatbot_response(user_input.strip(), agent)
            
            # Add to history
            add_to_history(user_input.strip(), response)
            
            # Display new response
            st.subheader("🤖 Latest Response")
            st.write(f"**Your Question:** {user_input.strip()}")
            st.write("**Assistant's Answer:**")
            st.write(response)
            
            # Rerun to update chat history display
            st.rerun()
    
    elif submit_button:
        st.warning("Please enter a message!")
    
    # Footer
    st.write("---")
    st.caption("💡 This chatbot provides information with sources and contact details. Always verify important information independently.")


if __name__ == "__main__":
    main()