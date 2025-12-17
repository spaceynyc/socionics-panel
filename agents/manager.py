"""
The Manager Agent - Final Synthesizer

Reviews all specialist opinions and outputs the final result.
Uses PRO_MODEL for high-quality synthesis and reasoning.
"""

import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from config.prompts import MANAGER_SYSTEM_PROMPT
from config.models import OPENROUTER_BASE_URL, PRO_MODEL


class ManagerAgent:
    """The Manager - Synthesizes specialist opinions into final verdict."""
    
    def __init__(self, api_key: str):
        """
        Initialize the Manager agent.
        
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
    
    def synthesize(
        self,
        dossier: dict,
        reinin_analysis: dict,
        quadra_analysis: dict,
        functions_analysis: dict,
        discussion_results: dict = None,
        validation_results: dict = None
    ) -> dict:
        """
        Synthesize specialist opinions into final verdict.
        
        Args:
            dossier: Original character dossier
            reinin_analysis: Analysis from Agent Reinin
            quadra_analysis: Analysis from Agent Quadra
            functions_analysis: Analysis from Agent Functions
            discussion_results: Optional discussion responses from agents
            validation_results: Optional validation report from the Validator
            
        Returns:
            Final verdict dictionary
        """
        # Build discussion section if available
        discussion_section = ""
        if discussion_results:
            discussion_section = "\n\n=== AGENT DISCUSSION (Counter-arguments and Refinements) ===\n"
            for agent_name, response in discussion_results.items():
                discussion_section += f"\n{agent_name}:\n{response}\n"
        
        # Build validation section if available
        validation_section = ""
        if validation_results:
            validation_section = "\n\n=== VALIDATOR REPORT (Fact-Check Results) ===\n"
            errors = validation_results.get("errors_found", [])
            if errors:
                validation_section += f"Errors Found: {len(errors)}\n"
                for error in errors:
                    if isinstance(error, dict):
                        validation_section += f"- {error.get('agent', 'Agent')}: {error.get('claim', '')} → {error.get('correction', '')}\n"
            else:
                validation_section += "No theoretical errors found.\n"
            
            if validation_results.get("summary"):
                validation_section += f"Summary: {validation_results['summary']}\n"
        
        # Get dossier summary for context
        dossier_summary = dossier.get('summary', 'No summary available.')
        
        user_prompt = f"""CHARACTER: {dossier.get('character_name', 'Unknown')} from {dossier.get('media_source', 'Unknown')}

SCOUT'S SUMMARY: {dossier_summary}

SPECIALIST ANALYSES:

=== AGENT REININ (Reinin Dichotomies) ===
Predicted Type: {reinin_analysis.get('predicted_type', 'Unknown')}
Confidence: {reinin_analysis.get('confidence', 0)}%
Reasoning: {reinin_analysis.get('reasoning', 'No reasoning provided')}

=== AGENT QUADRA (Quadra Values) ===
Predicted Type: {quadra_analysis.get('predicted_type', 'Unknown')}
Predicted Quadra: {quadra_analysis.get('predicted_quadra', 'Unknown')}
Confidence: {quadra_analysis.get('confidence', 0)}%
Reasoning: {quadra_analysis.get('reasoning', 'No reasoning provided')}

=== AGENT FUNCTIONS (Model A Functions) ===
Predicted Type: {functions_analysis.get('predicted_type', 'Unknown')}
Confidence: {functions_analysis.get('confidence', 0)}%
Reasoning: {functions_analysis.get('reasoning', 'No reasoning provided')}{discussion_section}{validation_section}

Based on these specialist analyses{', their discussion,' if discussion_results else ''}{' and the validation report,' if validation_results else ''} synthesize a final determination. Consider areas of agreement and disagreement, weigh the evidence quality, and account for any errors flagged by the Validator."""

        messages = [
            SystemMessage(content=MANAGER_SYSTEM_PROMPT),
            HumanMessage(content=user_prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        # Parse JSON response
        try:
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            verdict = json.loads(content.strip())
        except json.JSONDecodeError:
            # Fallback if parsing fails
            verdict = {
                "final_type": "Unknown",
                "type_name": "Could not determine",
                "type_nickname": "Unknown",
                "quadra": "Unknown",
                "confidence_score": 0,
                "confidence_explanation": "Failed to parse response",
                "key_traits": [],
                "summary": response.content[:500],
                "raw_response": response.content
            }
        
        return verdict
