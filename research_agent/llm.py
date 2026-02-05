from langchain_groq import ChatGroq

from config.settings import settings


def get_llm():
    """
    Returns a ChatModel with automatic fallback.
    Primary: Groq (Llama 3.3 70B) — fast, free.
    Fallback: Google Gemini Flash — free tier (optional).
    """
    primary = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=settings.groq_api_key,
        temperature=0.2,
        max_retries=2,
        request_timeout=30,
    )

    if settings.gemini_api_key:
        from langchain_google_genai import ChatGoogleGenerativeAI

        fallback = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=settings.gemini_api_key,
            temperature=0.2,
        )
        return primary.with_fallbacks([fallback])

    return primary
