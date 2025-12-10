"""
OpenRouter Model Configuration

Model configuration for the multi-agent Socionics analysis system.
Different agents use different model tiers for cost optimization.
"""

# =============================================================================
# MODEL TIERS
# =============================================================================

# Pro Model: Used for Manager (final synthesis) - highest quality reasoning
PRO_MODEL = "google/gemini-3-pro-preview"

# Mid Model: Used for Scout and Council agents - good balance of quality/cost
MID_MODEL = "google/gemini-2.5-pro"

# Flash Model: Used for Validator (fact-checking) - fast and cheap
FLASH_MODEL = "google/gemini-2.5-flash-preview-09-2025"

# OpenRouter base URL
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Model info for display purposes
MODEL_INFO = {
    PRO_MODEL: {
        "name": "Gemini 3 Pro Preview",
        "provider": "Google",
        "context": 1000000,
        "role": "Manager (Final Synthesis)"
    },
    MID_MODEL: {
        "name": "Gemini 2.5 Pro",
        "provider": "Google",
        "context": 1000000,
        "role": "Scout + Council (Research & Analysis)"
    },
    FLASH_MODEL: {
        "name": "Gemini 2.5 Flash Preview",
        "provider": "Google", 
        "context": 1000000,
        "role": "Validator (Fact-Check)"
    }
}

