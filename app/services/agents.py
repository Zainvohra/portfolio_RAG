from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
import os


GROQ_API_KEY = os.getenv("GROQ_API_KEY", None)
MODEL = "llama-3.3-70b-versatile"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"


async def query_pulse_ai(query: str):
    groq_model = OpenAIChatCompletionsModel(
        model=MODEL,
        openai_client=AsyncOpenAI(
            base_url=GROQ_BASE_URL,
            api_key=GROQ_API_KEY,
        ),
    )

    agent = Agent(
        name="PulseAI",
        instructions="You are a helpful assistant",
        model=groq_model,
    )

    result = await Runner.run(agent, input=query)

    return result.final_output
