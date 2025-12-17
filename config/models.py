"""
OpenRouter Model Configuration

Model configuration for the multi-agent Socionics analysis system.
Different agents use different model tiers for cost optimization.
"""

# =============================================================================
# MODEL TIERS
# =============================================================================

# Pro Model: Core analysis agents (Council, Discussion, Manager)
PRO_MODEL = "google/gemini-3-pro-preview"

# Mid Model: Scout agent (web summarization)
MID_MODEL = "google/gemini-3-flash-preview"

# Flash Model: Validator (fact-checking)
FLASH_MODEL = "google/gemini-3-flash-preview"

# OpenRouter base URL
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Model info for display purposes
MODEL_INFO = {
    PRO_MODEL: {
        "name": "Gemini 3 Pro",
        "provider": "Google",
        "context": 1000000,
        "role": "All Agents"
    }
}

