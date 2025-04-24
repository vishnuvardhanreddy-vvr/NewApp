import asyncio
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings

# Function to get LLM (similar to the sync version, but async-compatible)
async def get_llm() -> BaseChatModel:
    """
    Asynchronously initializes and returns the correct LLM model based on the configured provider.
    """
    LLM_PROVIDER = settings.LLM_PROVIDER
    LLM_TEMPERATURE = settings.LLM_TEMPERATURE
    if LLM_PROVIDER == "gemini":
        return ChatGoogleGenerativeAI(model="gemini-pro", temperature=LLM_TEMPERATURE)

    # elif LLM_PROVIDER == "openai":
    #     from langchain.chat_models import ChatOpenAI
    #     return ChatOpenAI(model="gpt-4", temperature=TEMPERATURE)

    # elif LLM_PROVIDER == "anthropic":
    #     from langchain_anthropic import ChatAnthropic
    #     return ChatAnthropic(model="claude-3", temperature=TEMPERATURE)

    else:
        raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")

# Asynchronous function to run LLM with a prompt and input data
async def get_data(prompt: str) -> dict:
    """
    Runs the LLM asynchronously with the provided prompt and input data, and returns a structured JSON response.
    """
    llm = await get_llm()  # Get LLM asynchronously

    # Asynchronously get the response from the LLM
    response = await llm.invoke([HumanMessage(content=prompt)])

    try:
        # Expect model to return valid JSON
        return eval(response.content) if isinstance(response.content, str) else response.content
    except Exception as e:
        raise ValueError(f"Invalid JSON response: {e}")