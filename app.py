"""
Autonomous Socionics Research Lab

A multi-agent AI system that researches fictional characters and determines 
their Socionics personality type through web search and parallel analysis.
"""

import streamlit as st
import time
from pathlib import Path

# Import agents
from agents.scout import ScoutAgent
from agents.council import TheCouncil
from agents.manager import ManagerAgent

# Import PDF generator
from utils.pdf_generator import generate_pdf_report

# Import config
from config.models import PRO_MODEL, FLASH_MODEL, MID_MODEL, MODEL_INFO


# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="Socionics Research Lab",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
css_path = Path(__file__).parent / "styles" / "main.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# =============================================================================
# CONFIG PERSISTENCE (for API key)
# =============================================================================
import json

CONFIG_FILE = Path(__file__).parent / ".user_config.json"

def load_user_config():
    """Load user config from file."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_user_config(config):
    """Save user config to file."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
    except:
        pass

# Load saved config
_saved_config = load_user_config()


# =============================================================================
# ANALYSIS HISTORY PERSISTENCE
# =============================================================================
from datetime import datetime
import uuid

HISTORY_DIR = Path(__file__).parent / ".analysis_history"
HISTORY_DIR.mkdir(exist_ok=True)

def save_analysis_to_history(dossier, council_results, discussion_results, validation_results, final_result):
    """Save a completed analysis to history."""
    try:
        analysis_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().isoformat()
        character_name = dossier.get('character_name', 'Unknown')
        final_type = final_result.get('final_type', 'UNK')
        
        history_entry = {
            "id": analysis_id,
            "timestamp": timestamp,
            "character_name": character_name,
            "media_source": dossier.get('media_source', 'Unknown'),
            "final_type": final_type,
            "dossier": dossier,
            "council_results": council_results,
            "discussion_results": discussion_results,
            "validation_results": validation_results,
            "final_result": final_result
        }
        
        # Create safe filename
        safe_name = "".join(c if c.isalnum() else "_" for c in character_name)
        filename = f"{analysis_id}_{safe_name}.json"
        filepath = HISTORY_DIR / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(history_entry, f, indent=2, ensure_ascii=False)
        
        return analysis_id
    except Exception as e:
        print(f"Failed to save history: {e}")
        return None

def load_analysis_history():
    """Load list of all past analyses (summary only)."""
    history = []
    try:
        for filepath in HISTORY_DIR.glob("*.json"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    history.append({
                        "id": data.get("id"),
                        "timestamp": data.get("timestamp"),
                        "character_name": data.get("character_name"),
                        "media_source": data.get("media_source"),
                        "final_type": data.get("final_type"),
                        "filepath": str(filepath)
                    })
            except:
                continue
        # Sort by timestamp, newest first
        history.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    except:
        pass
    return history

def load_full_analysis(filepath):
    """Load complete analysis data from file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

def delete_analysis_from_history(filepath):
    """Delete an analysis from history."""
    try:
        file_path = Path(filepath)
        if file_path.exists():
            file_path.unlink()
            return True
    except Exception as e:
        print(f"Failed to delete history entry: {e}")
    return False


# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================
# Initialize API key: check Streamlit secrets first (for cloud), then saved config (for local)
if "api_key" not in st.session_state:
    try:
        if hasattr(st, 'secrets') and 'OPENROUTER_API_KEY' in st.secrets:
            st.session_state.api_key = st.secrets['OPENROUTER_API_KEY']
        else:
            st.session_state.api_key = _saved_config.get("api_key", "")
    except Exception:
        # No secrets file exists, fall back to saved config
        st.session_state.api_key = _saved_config.get("api_key", "")
if "phase" not in st.session_state:
    st.session_state.phase = "input"  # input, researching, analyzing, discussing, complete
if "dossier" not in st.session_state:
    st.session_state.dossier = None
if "council_results" not in st.session_state:
    st.session_state.council_results = None
if "discussion_results" not in st.session_state:
    st.session_state.discussion_results = None
if "validation_results" not in st.session_state:
    st.session_state.validation_results = None
if "final_result" not in st.session_state:
    st.session_state.final_result = None
if "auto_proceed" not in st.session_state:
    st.session_state.auto_proceed = _saved_config.get("auto_proceed", False)
if "viewing_history" not in st.session_state:
    st.session_state.viewing_history = None  # Stores filepath of history entry being viewed
if "analysis_saved" not in st.session_state:
    st.session_state.analysis_saved = False  # Track if current analysis was saved


# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    st.markdown("---")
    
    # API Key input - only show if not using Streamlit secrets
    try:
        _using_secrets = hasattr(st, 'secrets') and 'OPENROUTER_API_KEY' in st.secrets
    except Exception:
        _using_secrets = False
    
    if _using_secrets:
        st.success("✓ API Key configured via secrets")
    else:
        api_key = st.text_input(
            "OpenRouter API Key",
            type="password",
            value=st.session_state.api_key,
            help="Get your API key from openrouter.ai - it will be saved for future sessions"
        )
        if api_key:
            st.session_state.api_key = api_key
            # Save to config file for persistence across refreshes
            save_user_config({"api_key": api_key})
    
    st.markdown("---")
    
    # Model configuration info (read-only display)
    st.markdown("### 🤖 Model")
    
    pro_info = MODEL_INFO[PRO_MODEL]
    
    st.markdown(f"""
    <div style="padding: 12px; background: #333; border-radius: 4px;">
        <div style="color: #4CAF50; font-size: 0.75rem; text-transform: uppercase; font-weight: 600;">All Agents</div>
        <div style="color: #fff; font-weight: 600; font-size: 0.9rem;">{pro_info['name']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Auto-proceed toggle
    st.markdown("### ⚡ Automation")
    auto_proceed = st.checkbox(
        "Auto-proceed through all phases",
        value=st.session_state.auto_proceed,
        help="Automatically continue through all analysis phases without manual clicks (saved)"
    )
    st.session_state.auto_proceed = auto_proceed
    
    # Save auto-proceed preference
    current_config = load_user_config()
    if current_config.get("auto_proceed") != auto_proceed:
        current_config["auto_proceed"] = auto_proceed
        save_user_config(current_config)
    
    st.markdown("---")
    
    # Reset button
    if st.button("🔄 Reset Analysis", use_container_width=True):
        st.session_state.phase = "input"
        st.session_state.dossier = None
        st.session_state.council_results = None
        st.session_state.discussion_results = None
        st.session_state.validation_results = None
        st.session_state.final_result = None
        st.session_state.viewing_history = None
        st.session_state.analysis_saved = False
        st.rerun()
    
    st.markdown("---")
    
    # History Section (collapsible)
    st.markdown("### 📜 History")
    history = load_analysis_history()
    
    if history:
        with st.expander(f"View Past Analyses ({len(history)})", expanded=False):
            for entry in history:  # Show all entries
                # Parse timestamp for display
                try:
                    ts = datetime.fromisoformat(entry['timestamp'])
                    date_str = ts.strftime("%m/%d %H:%M")
                except:
                    date_str = "Unknown"
                
                # Create row with view button and delete button
                btn_label = f"{entry['character_name']} ({entry['final_type']})"
                btn_help = f"{entry['media_source']} • {date_str}"
                
                col_view, col_del = st.columns([5, 1])
                with col_view:
                    if st.button(btn_label, key=f"hist_{entry['id']}", help=btn_help, use_container_width=True):
                        # Load the full analysis
                        st.session_state.viewing_history = entry['filepath']
                        st.session_state.phase = "history_view"
                        st.rerun()
                with col_del:
                    if st.button("🗑️", key=f"del_{entry['id']}", help="Delete this analysis"):
                        if delete_analysis_from_history(entry['filepath']):
                            st.rerun()
    else:
        st.caption("No past analyses yet.")
    
    st.markdown("---")
    st.markdown("""
    <div style="color: #666; font-size: 0.75rem;">
        <strong>Socionics Research Lab v1.1</strong><br>
        A multi-agent AI system for<br>
        character personality analysis.
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# MAIN CONTENT
# =============================================================================

# Header
st.markdown("""
# 🔬 Autonomous Socionics Research Lab
### Multi-Agent Character Analysis System
""")

# Phase indicators (skip for history view)
if st.session_state.phase != "history_view":
    col1, col2, col3, col4 = st.columns(4)
    phases = [
        ("Phase 1: Research", "researching"),
        ("Phase 2: Analysis", "analyzing"),
        ("Phase 3: Discussion", "discussing"),
        ("Phase 4: Synthesis", "complete")
    ]
    
    phase_keys = [p[1] for p in phases]
    current_phase = st.session_state.phase
    current_index = phase_keys.index(current_phase) if current_phase in phase_keys else -1
    
    for col, (label, phase_key) in zip([col1, col2, col3, col4], phases):
        with col:
            phase_index = phase_keys.index(phase_key)
            if current_phase == phase_key:
                st.markdown(f'<div class="phase-indicator active">● {label}</div>', unsafe_allow_html=True)
            elif current_index > phase_index:
                st.markdown(f'<div class="phase-indicator complete">✓ {label}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="phase-indicator">○ {label}</div>', unsafe_allow_html=True)

st.markdown("---")

# Check for API key
if not st.session_state.api_key:
    st.warning("⚠️ Please enter your OpenRouter API key in the sidebar to begin.")
    st.stop()


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def display_dossier(dossier, expanded=True, use_expander=True):
    """Display the character dossier with new format support.
    
    Args:
        dossier: The character dossier data
        expanded: Whether the expander starts expanded (only applies if use_expander=True)
        use_expander: If True, wrap content in an expander. If False, render directly.
    """
    def render_dossier_content():
        st.markdown(f"### {dossier.get('character_name', 'Unknown')} — *{dossier.get('media_source', 'Unknown')}*")
        
        if dossier.get("summary"):
            st.markdown(f"**Summary:** {dossier['summary']}")
        
        # Handle both old (behavioral_facts) and new (biographical_facts) format
        facts = dossier.get("biographical_facts", dossier.get("behavioral_facts", []))
        if facts:
            st.markdown("#### Biographical Facts")
            for i, fact in enumerate(facts, 1):
                st.markdown(f"""
                <div class="fact-item">
                    <span class="fact-number">{i:02d}</span>
                    <span class="fact-text">{fact}</span>
                </div>
                """, unsafe_allow_html=True)
        
        if dossier.get("key_quotes"):
            st.markdown("#### Key Quotes")
            for quote_obj in dossier["key_quotes"]:
                if isinstance(quote_obj, dict):
                    st.markdown(f'> "{quote_obj.get("quote", "")}"')
                    st.caption(quote_obj.get("context", ""))
                else:
                    st.markdown(f'> "{quote_obj}"')
        
        if dossier.get("relationships"):
            st.markdown("#### Key Relationships")
            for rel in dossier["relationships"]:
                if isinstance(rel, dict):
                    st.markdown(f"- **{rel.get('person', 'Unknown')}**: {rel.get('dynamic', '')}")
    
    # Either wrap in expander or render directly
    if use_expander:
        with st.expander("View Complete Dossier", expanded=expanded):
            render_dossier_content()
    else:
        render_dossier_content()


# =============================================================================
# HISTORY VIEW MODE
# =============================================================================
if st.session_state.phase == "history_view" and st.session_state.viewing_history:
    # Load the historical analysis
    history_data = load_full_analysis(st.session_state.viewing_history)
    
    if history_data:
        st.markdown("## 📜 Historical Analysis")
        
        # Back button
        if st.button("← Back to New Analysis", type="secondary"):
            st.session_state.viewing_history = None
            st.session_state.phase = "input"
            st.rerun()
        
        st.markdown("---")
        
        # Parse timestamp
        try:
            ts = datetime.fromisoformat(history_data.get('timestamp', ''))
            date_str = ts.strftime("%B %d, %Y at %I:%M %p")
        except:
            date_str = "Unknown date"
        
        st.caption(f"Analyzed on {date_str}")
        
        # Display final result
        result = history_data.get('final_result', {})
        dossier = history_data.get('dossier', {})
        council = history_data.get('council_results', {})
        discussion = history_data.get('discussion_results', {})
        validation = history_data.get('validation_results', {})
        
        # Main result card
        st.markdown(f"""
        <div class="type-result" style="text-align: center; padding: 40px; border: 4px solid currentColor; margin-bottom: 24px;">
            <div class="type-code" style="font-size: 5rem; font-weight: 800; letter-spacing: -0.05em; color: #FF3B30;">{result.get('final_type', 'UNK')}</div>
            <div class="type-name" style="font-size: 1.5rem; color: #e0e0e0; margin-top: 8px;">{result.get('type_name', 'Unknown Type')}</div>
            <div class="type-nickname" style="font-size: 1.25rem; color: #FF3B30; font-style: italic; margin-top: 4px;">"{result.get('type_nickname', 'Unknown')}"</div>
            <div style="font-size: 1rem; color: #aaa; margin-top: 12px; text-transform: uppercase; letter-spacing: 0.1em;">{result.get('quadra', 'Unknown')} Quadra</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Confidence
        confidence = result.get("confidence_score", 0)
        st.markdown(f"### Confidence Score: {confidence}%")
        st.progress(confidence / 100)
        
        st.markdown("---")
        
        # Summary
        st.markdown("### Character Summary")
        st.markdown(result.get("summary", "No summary available."))
        
        # Agent predictions
        st.markdown("---")
        st.markdown("### Agent Predictions")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Agent Reinin", council.get('reinin', {}).get('predicted_type', 'N/A'))
        with col2:
            st.metric("Agent Quadra", council.get('quadra', {}).get('predicted_type', 'N/A'))
        with col3:
            st.metric("Agent Functions", council.get('functions', {}).get('predicted_type', 'N/A'))
        
        # Expandable sections
        with st.expander("View Dossier"):
            display_dossier(dossier, use_expander=False)
        
        with st.expander("View Agent Reasoning"):
            for agent_name, key in [("Agent Reinin", "reinin"), ("Agent Quadra", "quadra"), ("Agent Functions", "functions")]:
                st.markdown(f"**{agent_name}:** {council.get(key, {}).get('predicted_type', 'N/A')} ({council.get(key, {}).get('confidence', 0)}%)")
                st.markdown(council.get(key, {}).get("reasoning", "No reasoning provided"))
                st.markdown("---")
        
        if discussion:
            with st.expander("View Agent Discussion"):
                for name, response in discussion.items():
                    st.markdown(f"#### {name}")
                    st.markdown(response)
                    st.markdown("---")
        
        if validation:
            with st.expander("View Validation Results"):
                errors = validation.get("errors_found", [])
                if errors:
                    st.warning(f"Found {len(errors)} theoretical concern(s)")
                    for error in errors:
                        if isinstance(error, dict):
                            st.markdown(f"- **{error.get('agent', 'Agent')}**: {error.get('claim', '')} → {error.get('correction', '')}")
                else:
                    st.success("No theoretical errors found")
        
        # Synthesis details (Manager's final summary)
        if result.get("synthesis"):
            with st.expander("View Synthesis Details"):
                synthesis = result["synthesis"]
                st.markdown("**Agreements:**")
                st.markdown(synthesis.get("agreements", "N/A"))
                st.markdown("**Disagreements:**")
                st.markdown(synthesis.get("disagreements", "N/A"))
                if synthesis.get("majority_type"):
                    st.markdown("**Majority Type:**")
                    st.markdown(synthesis.get("majority_type", "N/A"))
                st.markdown("**Resolution:**")
                st.markdown(synthesis.get("resolution", "N/A"))
        
        # PDF Download for history entry
        st.markdown("---")
        st.markdown("### 📄 Download Report")
        try:
            pdf_bytes = generate_pdf_report(
                dossier=dossier,
                council_results=council,
                discussion_results=discussion or {},
                validation_results=validation or {},
                final_result=result
            )
            
            character_name = dossier.get('character_name', 'Character').replace(' ', '_')
            filename = f"socionics_report_{character_name}_{result.get('final_type', 'UNK')}.pdf"
            
            # Create a unique key for the download button
            history_id = history_data.get('id', 'unknown')
            download_key = f"pdf_history_{history_id}"
            
            st.download_button(
                label="⬇️ Download PDF Report",
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf",
                use_container_width=True,
                type="primary",
                key=download_key
            )
            st.caption("Download a beautifully formatted PDF of this historical analysis.")
        except Exception as e:
            st.error(f"PDF generation failed: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
    else:
        st.error("Could not load historical analysis.")
        if st.button("Return to Home"):
            st.session_state.viewing_history = None
            st.session_state.phase = "input"
            st.rerun()


# =============================================================================
# INPUT PHASE
# =============================================================================
elif st.session_state.phase == "input":
    st.markdown("## Enter Character Details")
    st.markdown("Provide the name of a fictional character and their source media.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        character_name = st.text_input(
            "Character Name",
            placeholder="e.g., Walter White",
            help="Enter the full name of the fictional character"
        )
    
    with col2:
        media_source = st.text_input(
            "Media Source",
            placeholder="e.g., Breaking Bad",
            help="TV show, movie, book, video game, etc."
        )
    
    st.markdown("")
    
    if st.button("🚀 Begin Analysis", type="primary", use_container_width=True):
        if not character_name or not media_source:
            st.error("Please enter both a character name and media source.")
        else:
            st.session_state.character_name = character_name
            st.session_state.media_source = media_source
            st.session_state.phase = "researching"
            st.rerun()


# =============================================================================
# RESEARCH PHASE (The Scout)
# =============================================================================
elif st.session_state.phase == "researching":
    st.markdown(f"## 🔍 Phase 1: The Scout")
    st.markdown(f"Researching **{st.session_state.character_name}** from *{st.session_state.media_source}*...")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        status_text.text("Initializing The Scout agent...")
        progress_bar.progress(10)
        
        scout = ScoutAgent(
            api_key=st.session_state.api_key
        )
        
        status_text.text("Searching the web for character information...")
        progress_bar.progress(30)
        
        dossier = scout.research(
            st.session_state.character_name,
            st.session_state.media_source
        )
        
        progress_bar.progress(100)
        status_text.text("Research complete!")
        
        st.session_state.dossier = dossier
        st.session_state.phase = "analyzing"
        time.sleep(1)
        st.rerun()
        
    except Exception as e:
        st.error(f"Error during research: {str(e)}")
        if st.button("Retry"):
            st.rerun()



# =============================================================================
# ANALYSIS PHASE (The Council)
# =============================================================================
elif st.session_state.phase == "analyzing":
    dossier = st.session_state.dossier
    
    # Show the dossier in its own expander (no separate header needed)
    display_dossier(dossier, expanded=True)
    
    st.markdown("---")
    st.markdown("## 🎭 Phase 2: The Council")
    st.markdown("Three specialist agents are analyzing the dossier in parallel...")
    
    # Run council analysis
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Agent Reinin")
        st.markdown("*Analyzing Reinin Dichotomies...*")
        reinin_placeholder = st.empty()
    
    with col2:
        st.markdown("### Agent Quadra")
        st.markdown("*Analyzing Quadra Values...*")
        quadra_placeholder = st.empty()
    
    with col3:
        st.markdown("### Agent Functions")
        st.markdown("*Analyzing Model A Functions...*")
        functions_placeholder = st.empty()
    
    try:
        council = TheCouncil(
            api_key=st.session_state.api_key
        )
        
        with st.spinner("The Council is deliberating..."):
            reinin, quadra, functions = council.deliberate(dossier)
        
        st.session_state.council_results = {
            "reinin": reinin,
            "quadra": quadra,
            "functions": functions
        }
        
        # Display results
        with col1:
            reinin_placeholder.empty()
            st.markdown(f"**Prediction:** `{reinin.get('predicted_type', 'Unknown')}`")
            st.markdown(f"**Confidence:** {reinin.get('confidence', 0)}%")
            with st.expander("View Reasoning"):
                st.markdown(reinin.get("reasoning", "No reasoning provided"))
        
        with col2:
            quadra_placeholder.empty()
            st.markdown(f"**Prediction:** `{quadra.get('predicted_type', 'Unknown')}`")
            st.markdown(f"**Quadra:** {quadra.get('predicted_quadra', 'Unknown')}")
            st.markdown(f"**Confidence:** {quadra.get('confidence', 0)}%")
            with st.expander("View Reasoning"):
                st.markdown(quadra.get("reasoning", "No reasoning provided"))
        
        with col3:
            functions_placeholder.empty()
            st.markdown(f"**Prediction:** `{functions.get('predicted_type', 'Unknown')}`")
            st.markdown(f"**Confidence:** {functions.get('confidence', 0)}%")
            with st.expander("View Reasoning"):
                st.markdown(functions.get("reasoning", "No reasoning provided"))
        
        st.markdown("---")
        
        # Auto-proceed or manual button
        if st.session_state.auto_proceed:
            st.session_state.phase = "discussing"
            st.rerun()
        elif st.button("💬 Proceed to Agent Discussion", type="primary", use_container_width=True):
            st.session_state.phase = "discussing"
            st.rerun()
    
    except Exception as e:
        st.error(f"Error during council analysis: {str(e)}")
        if st.button("Retry"):
            st.rerun()


# =============================================================================
# DISCUSSION PHASE (Agents Debate)
# =============================================================================
elif st.session_state.phase == "discussing":
    dossier = st.session_state.dossier
    council = st.session_state.council_results
    
    st.markdown("## 💬 Phase 3: Agent Discussion")
    st.markdown("The agents are reviewing each other's analyses and sharing their thoughts...")
    
    # Show initial predictions
    st.markdown("### Initial Predictions")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Agent Reinin:** `{council['reinin'].get('predicted_type', 'Unknown')}`")
    with col2:
        st.markdown(f"**Agent Quadra:** `{council['quadra'].get('predicted_type', 'Unknown')}`")
    with col3:
        st.markdown(f"**Agent Functions:** `{council['functions'].get('predicted_type', 'Unknown')}`")
    
    st.markdown("---")
    st.markdown("### Live Discussion")
    
    if st.session_state.discussion_results is None:
        try:
            the_council = TheCouncil(
                api_key=st.session_state.api_key
            )
            
            all_analyses = {
                "Agent Reinin": council["reinin"],
                "Agent Quadra": council["quadra"],
                "Agent Functions": council["functions"]
            }
            
            # Create placeholders for live updates
            discussion_containers = {}
            agent_names = ["Agent Reinin", "Agent Quadra", "Agent Functions"]
            
            for name in agent_names:
                with st.container():
                    st.markdown(f"#### {name}")
                    discussion_containers[name] = st.empty()
                    discussion_containers[name].markdown("*Thinking...*")
            
            # Run discussion
            with st.spinner("Agents are discussing..."):
                discussion = the_council.run_discussion(dossier, all_analyses)
            
            # Update displays
            for name, response in discussion.items():
                discussion_containers[name].markdown(response)
            
            st.session_state.discussion_results = discussion
            
            # Run validation
            st.markdown("---")
            st.markdown("### 🔍 The Validator - Fact-Checking Claims")
            
            with st.spinner("Validating theoretical accuracy..."):
                validation = the_council.run_validation(all_analyses)
            
            st.session_state.validation_results = validation
            
        except Exception as e:
            st.error(f"Error during discussion: {str(e)}")
            if st.button("Retry Discussion"):
                st.rerun()
    else:
        # Show saved discussion
        for name, response in st.session_state.discussion_results.items():
            st.markdown(f"#### {name}")
            st.markdown(response)
            st.markdown("---")
    
    # Show validation results
    if st.session_state.get("validation_results"):
        st.markdown("### 🔍 The Validator - Fact-Check Report")
        validation = st.session_state.validation_results
        
        # Show errors if any
        errors = validation.get("errors_found", [])
        if errors and len(errors) > 0:
            st.warning(f"⚠️ Found {len(errors)} theoretical error(s)")
            for error in errors:
                if isinstance(error, dict):
                    st.markdown(f"""
                    <div style="background: rgba(255, 193, 7, 0.2); padding: 12px; border-left: 4px solid #ffc107; margin-bottom: 8px;">
                        <strong>{error.get('agent', 'Unknown Agent')}</strong> claimed: "{error.get('claim', 'N/A')}"<br>
                        <span style="color: #ff6b6b;">✗ Correction: {error.get('correction', 'N/A')}</span>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.success("✓ No theoretical errors found")
        
        # Show recommendation
        if validation.get("recommended_type"):
            st.markdown(f"**Validator's Recommendation:** `{validation['recommended_type']}`")
        
        # Show summary
        if validation.get("summary"):
            with st.expander("View Validation Details"):
                st.markdown(validation["summary"])
    
    if st.session_state.discussion_results:
        st.markdown("")
        # Auto-proceed or manual button
        if st.session_state.auto_proceed:
            st.session_state.phase = "complete"
            st.rerun()
        elif st.button("⚡ Proceed to Final Synthesis", type="primary", use_container_width=True):
            st.session_state.phase = "complete"
            st.rerun()


# =============================================================================
# SYNTHESIS PHASE (The Manager)
# =============================================================================
elif st.session_state.phase == "complete":
    dossier = st.session_state.dossier
    council = st.session_state.council_results
    discussion = st.session_state.discussion_results
    
    # Check if we need to run the manager
    if st.session_state.final_result is None:
        st.markdown("## 🎯 Phase 4: The Manager")
        st.markdown("Synthesizing specialist opinions into final determination...")
        
        try:
            manager = ManagerAgent(
                api_key=st.session_state.api_key
            )
            
            with st.spinner("The Manager is reviewing all analyses, discussion, and validation..."):
                result = manager.synthesize(
                    dossier,
                    council["reinin"],
                    council["quadra"],
                    council["functions"],
                    discussion_results=discussion,
                    validation_results=st.session_state.get('validation_results')
                )
            
            st.session_state.final_result = result
            st.rerun()
            
        except Exception as e:
            st.error(f"Error during synthesis: {str(e)}")
            if st.button("Retry"):
                st.session_state.final_result = None
                st.rerun()
    
    else:
        result = st.session_state.final_result
        
        # Save to history (only once per analysis)
        if not st.session_state.analysis_saved:
            save_analysis_to_history(
                dossier=st.session_state.dossier,
                council_results=st.session_state.council_results,
                discussion_results=st.session_state.discussion_results or {},
                validation_results=st.session_state.get('validation_results', {}),
                final_result=result
            )
            st.session_state.analysis_saved = True
        
        # FINAL RESULT DISPLAY
        st.markdown("## 🎯 Final Determination")
        
        # Main result card
        st.markdown(f"""
        <div class="type-result" style="text-align: center; padding: 40px; border: 4px solid currentColor; margin-bottom: 24px;">
            <div class="type-code" style="font-size: 5rem; font-weight: 800; letter-spacing: -0.05em; color: #FF3B30;">{result.get('final_type', 'UNK')}</div>
            <div class="type-name" style="font-size: 1.5rem; color: #e0e0e0; margin-top: 8px;">{result.get('type_name', 'Unknown Type')}</div>
            <div class="type-nickname" style="font-size: 1.25rem; color: #FF3B30; font-style: italic; margin-top: 4px;">"{result.get('type_nickname', 'Unknown')}"</div>
            <div style="font-size: 1rem; color: #aaa; margin-top: 12px; text-transform: uppercase; letter-spacing: 0.1em;">{result.get('quadra', 'Unknown')} Quadra</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Confidence meter
        confidence = result.get("confidence_score", 0)
        st.markdown(f"### Confidence Score: {confidence}%")
        st.progress(confidence / 100)
        st.caption(result.get("confidence_explanation", ""))
        
        st.markdown("---")
        
        # Function stack if available
        if result.get("function_stack"):
            st.markdown("### Function Stack")
            st.code(result["function_stack"], language=None)
        
        # Key traits
        if result.get("key_traits"):
            st.markdown("### Key Traits")
            trait_cols = st.columns(len(result["key_traits"]))
            for col, trait in zip(trait_cols, result["key_traits"]):
                with col:
                    st.markdown(f"""
                    <div style="background: rgba(128, 128, 128, 0.1); padding: 16px; text-align: center; border: 2px solid currentColor;">
                        <span style="font-weight: 600;">{trait}</span>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Summary
        st.markdown("### Character Summary")
        st.markdown(result.get("summary", "No summary available."))
        
        st.markdown("---")
        
        # Agent predictions comparison
        if result.get("agent_predictions"):
            st.markdown("### Agent Predictions Comparison")
            pred = result["agent_predictions"]
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Agent Reinin", pred.get("reinin_predicted", "N/A"))
            with col2:
                st.metric("Agent Quadra", pred.get("quadra_predicted", "N/A"))
            with col3:
                st.metric("Agent Functions", pred.get("functions_predicted", "N/A"))
        
        # Synthesis details
        if result.get("synthesis"):
            with st.expander("View Synthesis Details"):
                synthesis = result["synthesis"]
                st.markdown("**Agreements:**")
                st.markdown(synthesis.get("agreements", "N/A"))
                st.markdown("**Disagreements:**")
                st.markdown(synthesis.get("disagreements", "N/A"))
                if synthesis.get("majority_type"):
                    st.markdown("**Majority Type:**")
                    st.markdown(synthesis.get("majority_type", "N/A"))
                st.markdown("**Resolution:**")
                st.markdown(synthesis.get("resolution", "N/A"))
        
        # Discussion phase results
        if discussion:
            with st.expander("View Agent Discussion"):
                for name, response in discussion.items():
                    st.markdown(f"#### {name}")
                    st.markdown(response)
                    st.markdown("---")
        
        # Council results
        with st.expander("View Individual Agent Analyses"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### Agent Reinin")
                st.markdown(f"**Prediction:** {council['reinin'].get('predicted_type', 'Unknown')}")
                st.markdown(f"**Confidence:** {council['reinin'].get('confidence', 0)}%")
                st.markdown(council['reinin'].get("reasoning", ""))
            
            with col2:
                st.markdown("#### Agent Quadra")
                st.markdown(f"**Prediction:** {council['quadra'].get('predicted_type', 'Unknown')}")
                st.markdown(f"**Confidence:** {council['quadra'].get('confidence', 0)}%")
                st.markdown(council['quadra'].get("reasoning", ""))
            
            with col3:
                st.markdown("#### Agent Functions")
                st.markdown(f"**Prediction:** {council['functions'].get('predicted_type', 'Unknown')}")
                st.markdown(f"**Confidence:** {council['functions'].get('confidence', 0)}%")
                st.markdown(council['functions'].get("reasoning", ""))
        
        # Dossier
        with st.expander("View Character Dossier"):
            display_dossier(dossier, use_expander=False)
        
        st.markdown("---")
        
        # PDF Download
        st.markdown("### 📄 Download Report")
        try:
            validation = st.session_state.get('validation_results', {})
            pdf_bytes = generate_pdf_report(
                dossier=dossier,
                council_results=council,
                discussion_results=discussion or {},
                validation_results=validation,
                final_result=result
            )
            
            character_name = dossier.get('character_name', 'Character').replace(' ', '_')
            filename = f"socionics_report_{character_name}_{result.get('final_type', 'UNK')}.pdf"
            
            # Create a unique key for the download button to prevent caching issues
            download_key = f"pdf_download_{character_name}_{result.get('final_type', 'UNK')}"
            
            st.download_button(
                label="⬇️ Download PDF Report",
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf",
                use_container_width=True,
                type="primary",
                key=download_key
            )
            st.caption("Download a beautifully formatted PDF of this analysis.")
        except Exception as e:
            st.error(f"PDF generation failed: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
            st.caption("PDF export requires reportlab. Run: pip install reportlab")


# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; font-size: 0.875rem;">
    <strong>Socionics Research Lab</strong> • Powered by OpenRouter • Swiss Design
</div>
""", unsafe_allow_html=True)

