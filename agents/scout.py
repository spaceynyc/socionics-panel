"""
The Scout Agent - Web Researcher

Searches the web for character information and compiles a dossier.
Uses PRO_MODEL for high-quality research and detailed fact gathering.
"""

import json
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from config.prompts import SCOUT_SYSTEM_PROMPT
from config.models import OPENROUTER_BASE_URL, PRO_MODEL
from utils.search import search_character, format_search_results


class ScoutAgent:
    """The Scout - Researches characters from the web."""
    
    def __init__(self, api_key: str):
        """
        Initialize the Scout agent.
        
        Args:
            api_key: OpenRouter API key
        """
        self.llm = ChatOpenAI(
            model=PRO_MODEL,
            openai_api_key=api_key,
            openai_api_base=OPENROUTER_BASE_URL,
            default_headers={
                "HTTP-Referer": "https://socionics-research-lab.streamlit.app",
                "X-Title": "Socionics Research Lab"
            }
        )
    
    def research(self, character_name: str, media_source: str) -> dict:
        """
        Research a character and compile a dossier.
        
        Args:
            character_name: Name of the character
            media_source: Source media (show, book, etc.)
            
        Returns:
            Dossier dictionary with behavioral facts and quotes
        """
        # Step 1: Search the web
        search_results = search_character(character_name, media_source)
        formatted_results = format_search_results(search_results, character_name, media_source)
        
        # Step 2: Have LLM analyze and compile dossier
        user_prompt = f"""Research subject: {character_name} from {media_source}

Here are web search results about this character:

{formatted_results}

Analyze these results and compile a structured dossier with 10 key behavioral facts and notable quotes that reveal their personality. Focus on personality-relevant information."""

        messages = [
            SystemMessage(content=SCOUT_SYSTEM_PROMPT),
            HumanMessage(content=user_prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        # Parse JSON response
        try:
            # Try to extract JSON from response
            content = response.content
            # Handle markdown code blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            dossier = json.loads(content.strip())
        except json.JSONDecodeError:
            # Fallback structure if parsing fails
            dossier = {
                "character_name": character_name,
                "media_source": media_source,
                "behavioral_facts": [response.content[:500]],
                "key_quotes": [],
                "summary": "Failed to parse structured response",
                "raw_response": response.content
            }
        
        return dossier
