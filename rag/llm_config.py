import os
import sys
from agents import set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel

# ============================================================================
# OPENAI TRACING CONFIGURATION (OpenAI key used ONLY for tracing)
# ============================================================================

def configure_openai_tracing(enabled=True):
    """
    Configure OpenAI tracing with manual API key setup.
    OpenAI key is used ONLY for tracing - Groq handles all LLM operations.
    """
    if enabled:
        api_key = os.getenv("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = api_key
        print(f"✅ OpenAI tracing key set manually")
        if api_key:
            print(f"   Tracing key: {api_key[:7]}...{api_key[-4:]}")
        set_tracing_disabled(False)
    else:
        set_tracing_disabled(True)


# ============================================================================
# GROQ MODEL CONFIGURATION (Used for actual LLM operations)
# ============================================================================

def configure_groq_model():
    """Configure Groq model for all LLM operations."""

    # Configure Groq API key - this handles all actual LLM requests
    groq_api_key = os.getenv("GROQ_API_KEY")
    # Validate Groq API key
    if not groq_api_key:
        print("❌ Error: GROQ_API_KEY not set.")
        print("   Please set it: export GROQ_API_KEY=gsk_your_groq_key")
        sys.exit(1)

    print(f"✅ Groq model configured (for LLM operations)")

    # Create the LiteLLM model configuration
    return LitellmModel(
        model="groq/llama-3.3-70b-versatile",
        api_key=groq_api_key,
    )


def configure_gemini_model():
    """Configure Gemini model for all LLM operations."""

    # Configure Gemini API key - this handles all actual LLM requests
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    # Validate Gemini API key
    if not gemini_api_key:
        print("❌ Error: GEMINI_API_KEY not set.")
        print("   Please set it: export GEMINI_API_KEY=your_gemini_key")
        sys.exit(1)

    print(f"✅ Gemini model configured (for LLM operations)")

    # Create the LiteLLM model configuration
    return LitellmModel(
        model="gemini/gemini-2.0-flash-exp",
        api_key=gemini_api_key,
    )


# ============================================================================
# TEST AGENT USING LLM_MODEL WITH OPENAI AGENTS SDK
# ============================================================================

async def test_agent_with_llm_model():
    """
    Test function to demonstrate how OpenAI Agents SDK uses the llm_model.
    This creates a simple test agent that uses the configured llm_model.
    """
    try:
        from agents import Agent, Runner
        
        print("🧪 Testing OpenAI Agents SDK with configured llm_model...")
        
        # Create a test agent using the configured llm_model
        test_agent = Agent(
            name="test_agent",
            instructions="You are a helpful test agent. Respond to user queries concisely.",
            model=llm_model,  # Use our configured llm_model here
            tools=[]  # No tools for this simple test
        )
        
        print(f"✅ Test agent created successfully")
        print(f"   Agent name: {test_agent.name}")
        print(f"   Using LLM model: {llm_model.model}")
        
        # Test the agent with a simple query
        test_query = "Hello! Can you tell me what 2+2 equals?"
        print(f"\n📝 Testing with query: '{test_query}'")
        
        # Use Runner.run to execute the agent
        response = await Runner.run(test_agent, test_query)
        print(f"🤖 Agent response: {response}")
        
        
    except Exception as e:
        print(f"❌ Error during test: {e}")



# Initialize Groq model
# llm_model = configure_groq_model() 

# Initialize Groq model
llm_model = configure_gemini_model() 
# llm_model.turn_on_debug()


# Initialize tracing
configure_openai_tracing(enabled=True)


# Example usage:
if __name__ == "__main__":
    import asyncio
    asyncio.run(test_agent_with_llm_model()) 


