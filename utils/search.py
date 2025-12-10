"""
DuckDuckGo Search Wrapper

Provides web search functionality for the Scout agent.
"""

from duckduckgo_search import DDGS
from typing import List, Dict
import time


def search_character(character_name: str, media_source: str, max_results: int = 15) -> List[Dict]:
    """
    Search for information about a fictional character.
    
    Args:
        character_name: Name of the character (e.g., "Walter White")
        media_source: Source media (e.g., "Breaking Bad")
        max_results: Maximum number of results to return
        
    Returns:
        List of search results with title, body, and href
    """
    # Multiple query strategies for better coverage
    search_queries = [
        # Primary queries with media source
        f'"{character_name}" "{media_source}" personality',
        f'"{character_name}" "{media_source}" character analysis',
        f'{character_name} {media_source} traits behavior',
        f'{character_name} {media_source} quotes',
        # Fallback queries without quotes (broader match)
        f'{character_name} {media_source} wiki',
        f'{character_name} {media_source} personality type',
        # Very broad fallback
        f'{character_name} character',
    ]
    
    all_results = []
    
    with DDGS() as ddgs:
        for query in search_queries:
            # Stop if we have enough results
            if len(all_results) >= max_results:
                break
                
            try:
                # Add small delay to avoid rate limiting
                time.sleep(0.3)
                results = list(ddgs.text(query, max_results=5))
                all_results.extend(results)
            except Exception as e:
                print(f"Search error for '{query}': {e}")
                continue
    
    # Remove duplicates by href
    seen_urls = set()
    unique_results = []
    for result in all_results:
        url = result.get("href", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(result)
    
    return unique_results[:max_results]


def format_search_results(results: List[Dict], character_name: str = "", media_source: str = "") -> str:
    """
    Format search results into a readable string for the LLM.
    
    Args:
        results: List of search results
        character_name: Name of character (for context if no results)
        media_source: Media source (for context if no results)
        
    Returns:
        Formatted string of search results
    """
    if not results:
        # Provide helpful context even when no results found
        return f"""No direct search results were found for "{character_name}" from "{media_source}".

However, you should still attempt to create a dossier based on your existing knowledge of this character. 
If this is a well-known character from popular media, use your training data to compile behavioral facts and quotes.
If this is an obscure or unknown character, indicate that in your response and provide what limited information you can."""
    
    formatted = []
    for i, result in enumerate(results, 1):
        title = result.get("title", "No title")
        body = result.get("body", "No description")
        href = result.get("href", "")
        
        formatted.append(f"""
--- Result {i} ---
Title: {title}
Source: {href}
Content: {body}
""")
    
    return "\n".join(formatted)

