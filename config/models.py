"""
OpenRouter Model Configuration

Model configuration for the multi-agent Socionics analysis system.
Different agents use different model tiers for cost optimization.
"""

# =============================================================================
# MODEL TIERS
# =============================================================================

# All agents use Gemini 3 Pro for best results
PRO_MODEL = "google/gemini-3-pro-preview"

# Mid Model: Used for Scout and Council agents
MID_MODEL = "google/gemini-3-pro-preview"

# Flash Model: Used for Validator (fact-checking)
FLASH_MODEL = "google/gemini-3-pro-preview"

# OpenRouter base URL
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Model info for display purposes
MODEL_INFO = {
    PRO_MODEL: {
        "name": "Gemini 3 Pro Preview",
        "provider": "Google",
        "context": 1000000,
        "role": "All Agents"
    }
}

