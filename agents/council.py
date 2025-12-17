"""
The Council - Three Specialist Agents with Discussion Phase + Validator

Three parallel Socionics analysts:
- Agent Reinin: Analyzes using Reinin Dichotomies
- Agent Quadra: Analyzes using Quadra Values
- Agent Functions: Analyzes using Model A Cognitive Functions

After initial analysis, agents participate in a discussion round where they
can see each other's conclusions and provide feedback before final synthesis.

The Validator agent fact-checks all theoretical claims for accuracy.

Model Tiers:
- Council agents use PRO_MODEL for high-quality typing analysis
- Validator uses FLASH_MODEL for efficient fact-checking
"""

import json
from typing import Dict, Tuple, List, Callable, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from config.prompts import (
    REININ_SYSTEM_PROMPT,
    QUADRA_SYSTEM_PROMPT,
    FUNCTIONS_SYSTEM_PROMPT,
    VALIDATOR_SYSTEM_PROMPT,
    COUNTER_ARGUMENT_PROMPT
)
from config.models import OPENROUTER_BASE_URL, PRO_MODEL, FLASH_MODEL, MID_MODEL


class CouncilAgent:
    """Base class for council specialist agents. Uses PRO_MODEL."""
    
    def __init__(self, api_key: str, system_prompt: str, name: str):
        self.name = name
        self.system_prompt = system_prompt
        self.llm = ChatOpenAI(
            model=PRO_MODEL,
            openai_api_key=api_key,
            openai_api_base=OPENROUTER_BASE_URL,
            default_headers={
                "HTTP-Referer": "https://socionics-research-lab.streamlit.app",
                "X-Title": "Socionics Research Lab"
            }
        )
    
    def analyze(self, dossier: dict) -> dict:
        """
        Analyze a character dossier.
        
        Args:
            dossier: Character dossier from Scout
            
        Returns:
            Analysis dictionary with type prediction
        """
        dossier_text = self._format_dossier(dossier)
        
        user_prompt = f"""Analyze the following character dossier and determine their Socionics type using your specialized framework.

CHARACTER DOSSIER:
{dossier_text}

Provide your analysis in the specified JSON format."""

        messages = [
            SystemMessage(content=self.system_prompt),
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
            
            analysis = json.loads(content.strip())
            analysis["agent_name"] = self.name
        except json.JSONDecodeError:
            analysis = {
                "agent_name": self.name,
                "predicted_type": "Unknown",
                "confidence": 0,
                "reasoning": "Failed to parse response",
                "raw_response": response.content
            }
        
        return analysis
    
    def respond_to_discussion(self, dossier: dict, all_analyses: dict) -> str:
        """
        Respond to other agents' analyses in discussion phase with counter-arguments.
        Uses the COUNTER_ARGUMENT_PROMPT to keep agents in their lanes.
        
        Args:
            dossier: Original character dossier
            all_analyses: Dict of agent_name -> analysis from all agents
            
        Returns:
            Discussion response string
        """
        own_analysis = all_analyses.get(self.name, {})
        other_analyses = {k: v for k, v in all_analyses.items() if k != self.name}
        
        # Build other predictions text
        other_predictions_text = ""
        for agent_name, analysis in other_analyses.items():
            pred_type = analysis.get('predicted_type', 'Unknown')
            confidence = analysis.get('confidence', 0)
            reasoning = analysis.get('reasoning', 'No reasoning provided')
            other_predictions_text += f"""
{agent_name} predicted: {pred_type} (confidence: {confidence}%)
Their reasoning: {reasoning}
"""
        
        # Use the counter-argument prompt
        formatted_prompt = COUNTER_ARGUMENT_PROMPT.format(
            agent_name=self.name,
            own_prediction=own_analysis.get('predicted_type', 'Unknown'),
            own_reasoning=own_analysis.get('reasoning', 'No reasoning provided'),
            other_predictions=other_predictions_text
        )
        
        messages = [
            SystemMessage(content=f"You are {self.name}. STAY IN YOUR LANE - only argue using your specialty framework."),
            HumanMessage(content=formatted_prompt)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def _format_dossier(self, dossier: dict) -> str:
        """Format dossier for prompt."""
        lines = [
            f"Character: {dossier.get('character_name', 'Unknown')}",
            f"Source: {dossier.get('media_source', 'Unknown')}",
            "",
            "BIOGRAPHICAL FACTS:"
        ]
        
        # Handle both old (behavioral_facts) and new (biographical_facts) format
        facts = dossier.get("biographical_facts", dossier.get("behavioral_facts", []))
        for i, fact in enumerate(facts, 1):
            lines.append(f"{i}. {fact}")
        
        lines.append("\nKEY QUOTES:")
        for quote_obj in dossier.get("key_quotes", []):
            if isinstance(quote_obj, dict):
                lines.append(f'- "{quote_obj.get("quote", "")}" ({quote_obj.get("context", "")})')
            else:
                lines.append(f'- "{quote_obj}"')
        
        # Handle relationships if present
        if "relationships" in dossier:
            lines.append("\nKEY RELATIONSHIPS:")
            for rel in dossier.get("relationships", []):
                if isinstance(rel, dict):
                    lines.append(f'- {rel.get("person", "Unknown")}: {rel.get("dynamic", "")}')
        
        lines.append(f"\nSUMMARY: {dossier.get('summary', 'No summary available')}")
        
        return "\n".join(lines)


class ReininAgent(CouncilAgent):
    """Agent specializing in Reinin Dichotomies analysis."""
    
    def __init__(self, api_key: str):
        super().__init__(api_key, REININ_SYSTEM_PROMPT, "Agent Reinin")


class QuadraAgent(CouncilAgent):
    """Agent specializing in Quadra Values analysis."""
    
    def __init__(self, api_key: str):
        super().__init__(api_key, QUADRA_SYSTEM_PROMPT, "Agent Quadra")


class FunctionsAgent(CouncilAgent):
    """Agent specializing in Model A Cognitive Functions analysis."""
    
    def __init__(self, api_key: str):
        super().__init__(api_key, FUNCTIONS_SYSTEM_PROMPT, "Agent Functions")


class ValidatorAgent:
    """Agent that fact-checks theoretical claims from other agents. Uses FLASH_MODEL."""
    
    def __init__(self, api_key: str):
        self.name = "The Validator"
        self.llm = ChatOpenAI(
            model=FLASH_MODEL,
            openai_api_key=api_key,
            openai_api_base=OPENROUTER_BASE_URL,
            default_headers={
                "HTTP-Referer": "https://socionics-research-lab.streamlit.app",
                "X-Title": "Socionics Research Lab"
            }
        )
    
    def validate(self, all_analyses: dict) -> dict:
        """
        Validate theoretical claims from all agents.
        
        Args:
            all_analyses: Dict of agent_name -> analysis from all agents
            
        Returns:
            Validation report dict
        """
        # Build summary of all claims
        claims_text = ""
        for agent_name, analysis in all_analyses.items():
            pred_type = analysis.get('predicted_type', 'Unknown')
            reasoning = analysis.get('reasoning', 'No reasoning')
            function_analysis = analysis.get('function_analysis', {})
            quadra_analysis = analysis.get('quadra_analysis', {})
            
            claims_text += f"""
═══════════════════════════════════════════════════════════════════════════════
{agent_name} - Predicted: {pred_type}
═══════════════════════════════════════════════════════════════════════════════
Reasoning: {reasoning}
"""
            if function_analysis:
                claims_text += f"\nFunction Analysis: {json.dumps(function_analysis, indent=2)}"
            if quadra_analysis:
                claims_text += f"\nQuadra Analysis: {json.dumps(quadra_analysis, indent=2)}"
        
        validation_prompt = f"""Review the following analyses for FACTUAL ACCURACY.

{claims_text}

Check for errors in:
1. Function position claims (e.g., if they say "LIE has Fe Role" - that's WRONG, LIE has Fe PoLR)
2. Quadra assignments (e.g., if they say "LIE is Beta" - that's WRONG, LIE is Gamma)
3. Dichotomy assignments
4. Logical consistency between claims

Respond in the specified JSON format."""

        messages = [
            SystemMessage(content=VALIDATOR_SYSTEM_PROMPT),
            HumanMessage(content=validation_prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        # Parse JSON response
        try:
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            validation = json.loads(content.strip())
        except json.JSONDecodeError:
            validation = {
                "errors_found": [],
                "verified_correct": [],
                "summary": f"Failed to parse validation response: {response.content[:200]}..."
            }
        
        return validation


class TheCouncil:
    """Orchestrates the three specialist agents with discussion and validation phases."""
    
    def __init__(self, api_key: str):
        self.agents = [
            ReininAgent(api_key),
            QuadraAgent(api_key),
            FunctionsAgent(api_key)
        ]
        self.agent_map = {agent.name: agent for agent in self.agents}
        self.validator = ValidatorAgent(api_key)
    
    def deliberate(self, dossier: dict, progress_callback: Callable = None) -> Tuple[Dict, Dict, Dict]:
        """
        Run all three agents in parallel.
        
        Args:
            dossier: Character dossier from Scout
            progress_callback: Optional callback for progress updates
            
        Returns:
            Tuple of (reinin_analysis, quadra_analysis, functions_analysis)
        """
        results = {}
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_agent = {
                executor.submit(agent.analyze, dossier): agent.name
                for agent in self.agents
            }
            
            for future in as_completed(future_to_agent):
                agent_name = future_to_agent[future]
                try:
                    results[agent_name] = future.result()
                    if progress_callback:
                        progress_callback(agent_name, results[agent_name])
                except Exception as e:
                    results[agent_name] = {
                        "agent_name": agent_name,
                        "predicted_type": "Error",
                        "confidence": 0,
                        "reasoning": f"Error during analysis: {str(e)}"
                    }
        
        return (
            results.get("Agent Reinin", {}),
            results.get("Agent Quadra", {}),
            results.get("Agent Functions", {})
        )
    
    def run_validation(self, all_analyses: dict) -> dict:
        """
        Run the validation phase to fact-check agent claims.
        
        Args:
            all_analyses: Dict of agent_name -> analysis
            
        Returns:
            Validation report dict
        """
        return self.validator.validate(all_analyses)
    
    def run_discussion(self, dossier: dict, all_analyses: dict, 
                       progress_callback: Callable = None) -> Dict[str, str]:
        """
        Run the discussion phase where agents respond to each other.
        
        Args:
            dossier: Original character dossier
            all_analyses: Dict of agent_name -> analysis
            progress_callback: Optional callback for streaming updates
            
        Returns:
            Dict of agent_name -> discussion response
        """
        discussion_responses = {}
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_agent = {
                executor.submit(agent.respond_to_discussion, dossier, all_analyses): agent.name
                for agent in self.agents
            }
            
            for future in as_completed(future_to_agent):
                agent_name = future_to_agent[future]
                try:
                    response = future.result()
                    discussion_responses[agent_name] = response
                    if progress_callback:
                        progress_callback(agent_name, response)
                except Exception as e:
                    discussion_responses[agent_name] = f"Error during discussion: {str(e)}"
        
        return discussion_responses
    
    def full_deliberation(self, dossier: dict, 
                          analysis_callback: Callable = None,
                          discussion_callback: Callable = None,
                          validation_callback: Callable = None) -> Tuple[Dict, Dict, Dict, Dict, Dict]:
        """
        Run full deliberation: analysis + discussion + validation phases.
        
        Args:
            dossier: Character dossier from Scout
            analysis_callback: Callback for analysis phase updates
            discussion_callback: Callback for discussion phase updates
            validation_callback: Callback for validation phase updates
            
        Returns:
            Tuple of (reinin_analysis, quadra_analysis, functions_analysis, discussion_responses, validation_report)
        """
        # Phase 1: Initial analyses
        reinin, quadra, functions = self.deliberate(dossier, analysis_callback)
        
        all_analyses = {
            "Agent Reinin": reinin,
            "Agent Quadra": quadra,
            "Agent Functions": functions
        }
        
        # Phase 2: Discussion
        discussion = self.run_discussion(dossier, all_analyses, discussion_callback)
        
        # Phase 3: Validation
        validation = self.run_validation(all_analyses)
        if validation_callback:
            validation_callback(validation)
        
        return reinin, quadra, functions, discussion, validation


