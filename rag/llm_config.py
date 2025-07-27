import os
import sys

from agents import set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel


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

    print(f"Gemini key: {gemini_api_key[:7]}...{gemini_api_key[-4:]}")

    # Create the LiteLLM model configuration
    return LitellmModel(
        model="gemini/gemini-2.0-flash-exp",
        api_key=gemini_api_key,
    )


# Initialize tracing
configure_openai_tracing(enabled=True)


llm_model = configure_gemini_model()



