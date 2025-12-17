"""
Socionics Knowledge Base

Comprehensive reference data scraped from Wikisocion for accurate Socionics typing.
This knowledge base is injected into agent prompts to ensure theoretically sound analysis.
"""

# =============================================================================
# MODEL A - FUNCTION POSITIONS
# =============================================================================

MODEL_A_POSITIONS = """
MODEL A - THE 8 FUNCTION POSITIONS

The 8 functions of Model A are arranged in a 2x4 matrix. Each position has specific properties 
that determine how a person relates to the information element placed there.

┌─────────────────────────────────────────────────────────────────────────────┐
│  POSITION    │  BLOCK     │  STRENGTH  │  VALUED  │  DIMENSIONALITY         │
├─────────────────────────────────────────────────────────────────────────────┤
│  1. Leading  │  Ego       │  Strong    │  Yes     │  4D (Global)            │
│  2. Creative │  Ego       │  Strong    │  Yes     │  3D (Situational)       │
│  3. Role     │  Super-Ego │  Weak      │  No      │  2D (Norms)             │
│  4. PoLR     │  Super-Ego │  Weak      │  No      │  1D (Experience only)   │
│  5. Suggest. │  Super-Id  │  Weak      │  Yes     │  1D (Experience only)   │
│  6. Activ.   │  Super-Id  │  Weak      │  Yes     │  2D (Norms)             │
│  7. Ignoring │  Id        │  Strong    │  No      │  3D (Situational)       │
│  8. Demonst. │  Id        │  Strong    │  No      │  4D (Global)            │
└─────────────────────────────────────────────────────────────────────────────┘

THE FOUR BLOCKS:

EGO BLOCK (Functions 1-2): Strong, Valued, Conscious, Mental
- The core of one's personality and conscious competence
- Source of confidence and active engagement with the world
- What a person naturally does well and enjoys
- Rarely causes feelings of doubt or shame

SUPER-EGO BLOCK (Functions 3-4): Weak, Subdued, Conscious, Mental  
- Area of perceived weakness that one tries to "work on"
- Source of stress when challenged
- Role function (3): Can be activated situationally but exhausting
- Vulnerable/PoLR (4): Most painful area, causes insecurity and distress

SUPER-ID BLOCK (Functions 5-6): Weak, Valued, Unconscious, Vital
- What a person seeks from others and appreciates receiving
- Suggestive (5): Perfectly complements leading function, never "too much"
- Activating (6): Appreciated in moderation, "hidden agenda"

ID BLOCK (Functions 7-8): Strong, Subdued, Unconscious, Vital
- Capable but undervalued, used privately or as "backup"
- Ignoring (7): Antithetical to base function, deliberately avoided
- Demonstrative (8): Used playfully or to defend, often taken for granted
"""

FUNCTION_DESCRIPTIONS = """
DETAILED FUNCTION POSITION DESCRIPTIONS:

1. LEADING/BASE FUNCTION (Ego Block)
- Most dominant psychic function, describes core perspective on life
- Creates constant, inadvertent judgments and assessments
- Produces robust confidence when speaking from this function
- Use is effortless and produces internal satisfaction
- People project these values onto others (source of both conflict and dualization)
- 4-dimensional: Can process experience, norms, situations, AND time/development

2. CREATIVE FUNCTION (Ego Block)
- Primary mode of APPLICATION of the base function
- "How do I make contact with the world?" vs base function's "What do I want?"
- Turns on and off - inconsistent attention that may jar others who value it more
- Used to help others with problems in this area (through the lens of base function)
- Criticism here is more sensitive than criticism of base function
- 3-dimensional: Can process experience, norms, and situations

3. ROLE FUNCTION (Super-Ego Block)
- Opposition to base function - both cannot be "on" simultaneously
- Perceived as personal weakness needing development
- Attempts to develop are sporadic, forgotten when crisis passes
- The focus of "self-improvement" efforts that often fail
- Easier to accept criticism here than at PoLR (has theoretical value)
- 2-dimensional: Can only process experience and social norms

4. VULNERABLE/PoLR FUNCTION (Super-Ego Block)  
- Point of Least Resistance - creates frustration and inadequacy
- Does not understand the importance of this element
- Trying to engage it creates insecurity and distress
- Often ignored even when most relevant
- People develop minimalist or unconventional approaches here
- 1-dimensional: Can only process personal experience

5. SUGGESTIVE FUNCTION (Super-Id Block)
- Dual-seeking function - perfectly complements leading function
- CANNOT be overwhelmed by this - the more present, the better
- Sustained presence creates soothing psychological effect
- Easily entertained by this kind of information
- Deficiency leads to exhaustion if trying to supply it oneself
- 1-dimensional: Accepts readily but processes only through experience

6. ACTIVATING FUNCTION (Super-Id Block)
- "Hidden Agenda" - appreciated but past a point seems excessive
- Can use sporadically but lacks natural balance
- May indulge recklessly or sorely neglect
- Best used in support of the suggestive function
- 2-dimensional: Can process experience and norms

7. IGNORING FUNCTION (Id Block)
- Rival image of base function - antithetical approach to same domain
- Subconscious annoyance, deliberately limited in public
- When lectured about it, sees information as superfluous
- Used extensively in private, called upon when necessary
- Does not cause psychological stress like weak functions, just boredom
- 3-dimensional: Sophisticated understanding but deliberately avoided

8. DEMONSTRATIVE FUNCTION (Id Block)
- Used as a game or to ridicule those who take it too seriously
- Often used against conventional usage to prove a point
- Just as sophisticated understanding as leading function
- Protects dual's vulnerable function
- Information here is taken as obvious and irrelevant to focus on
- 4-dimensional: Full capability but undervalued
"""

# =============================================================================
# INFORMATION ELEMENTS
# =============================================================================

INFORMATION_ELEMENTS = """
THE 8 INFORMATION ELEMENTS (IM Elements):

Each element represents a type of information the psyche can perceive and process.

INTUITION (Perceiving potential and time):
┌─────────────────────────────────────────────────────────────────────────────┐
│ Ne (Extraverted Intuition) - Potential & Essence                            │
│ - Potential, permutation, isomorphism, semblance, essence                   │
│ - Uncertainty, the unknown, opening up new "windows"                        │
│ - Seeing opportunities, chance, being the first                             │
│ - Refreshing informational suddenness, diversity of interests               │
│ - "What if?" thinking, brainstorming, bringing up new possibilities         │
├─────────────────────────────────────────────────────────────────────────────┤
│ Ni (Introverted Intuition) - Time & Development                             │
│ - Development over time, historicity, cause and effect                      │
│ - Consequences, repetition, archetypal themes and examples                  │
│ - Looking for causes in history or the past                                 │
│ - Past-future forecasting of event dynamics, rhythm                         │
│ - Delay or act-now timing, past-turned imagination                          │
└─────────────────────────────────────────────────────────────────────────────┘

SENSING (Perceiving concrete reality):
┌─────────────────────────────────────────────────────────────────────────────┐
│ Se (Extraverted Sensing) - Force & Reality                                  │
│ - Sensing of immediate static qualities of objects                          │
│ - Sensing of immediate reality, external appearance, texture, form          │
│ - Static objects, impact, direct physical effect, power                     │
│ - Span, extent, scope of influence, territory, ownership                    │
│ - Presence, assertiveness, mobilizing resources                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ Si (Introverted Sensing) - Homeostasis & Flow                               │
│ - Homeostasis, continuity, smoothness, flow                                 │
│ - Satisfaction, aesthetics, quality of life, pleasure                       │
│ - Relaxation, convenience, quality                                          │
│ - How environment affects physical/psychological state                      │
│ - Internal physical sensations and harmony                                  │
└─────────────────────────────────────────────────────────────────────────────┘

LOGIC (Judging by impersonal criteria):
┌─────────────────────────────────────────────────────────────────────────────┐
│ Te (Extraverted Logic) - Efficiency & Action                                │
│ - Efficiency, method, mechanism, knowledge, work                            │
│ - Reason in motion, direction of activity into its most logical course      │
│ - "Logic of actions", utilitarianism, expediency, benefit                   │
│ - Practical results, facts and data                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ Ti (Introverted Logic) - Structure & Analysis                               │
│ - Structure, analysis, coherence, consistency                               │
│ - Cogency, accordance, match, commensurability                              │
│ - Understanding, order, classification (or lack thereof)                    │
│ - Logical frameworks, structural relationships between components           │
└─────────────────────────────────────────────────────────────────────────────┘

ETHICS (Judging by personal criteria):
┌─────────────────────────────────────────────────────────────────────────────┐
│ Fe (Extraverted Ethics) - Emotional Atmosphere                              │
│ - Emotional atmosphere, romanticism, cooperation, treatment                 │
│ - Qualitative judgment of behavior, sympathy                                │
│ - Ethical estimations of observable actions, "ethics of actions"            │
│ - Enthusiasm, emotional expression, group mood                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ Fi (Introverted Ethics) - Internal Sentiments                               │
│ - Internal harmony, resonance or dissonance of personal sentiments          │
│ - Sympathy, pity, compassion, support, condemnation, judgment               │
│ - Positive and negative emotional space between people                      │
│ - "Ethics of relations", loyalty, personal trust                            │
└─────────────────────────────────────────────────────────────────────────────┘

CRITICAL DISTINCTIONS:
- Ne vs Ni: External potential/essence vs internal development/history
- Se vs Si: External static reality/impact vs internal homeostasis/flow
- Te vs Ti: External logic of actions vs internal logic of structure
- Fe vs Fi: External ethics of actions vs internal resonance of sentiments

STRUCTURAL PROPERTIES:

STATIC VS DYNAMIC (Discrete vs Continuous):
Static (Discrete, abruptly changing):
- Ne: Discrete temporal phases, sets of discrete alternatives
- Ti: Discrete logical/structural dependencies between states
- Se: Discrete spatial boundaries, territory, control
- Fi: Discrete types of interpersonal relationships (friend/enemy)

Dynamic (Continuous, constant fluctuation):
- Si: Continuous physical exchanges with environment
- Fe: Continuous excitations in psychological states
- Ni: Continuous evolution of things over time
- Te: Continuous incoming stream of objective facts

EXTROVERTED VS INTROVERTED (Object vs Relation):
Extroverted (Information about objects as they are):
- Ne: Something has potential or does not
- Fe: One is happy or sad (observable state)
- Se: Awareness of external properties/reality
- Te: Something is useful or not (objective property)

Introverted (Information about relations between objects):
- Si: Relation between person and environment (comfort)
- Ti: Logical relation between statements (if X then Y)
- Ni: Temporal relation between events (X leads to Y)
- Fi: Relation between people (X relates well to Y)
"""

# =============================================================================
# TYPE FUNCTION STACKS
# =============================================================================

TYPE_FUNCTION_STACKS = """
ALL 16 TYPE FUNCTION STACKS (Model A):

ALPHA QUADRA (Values: Si, Ne, Fe, Ti):
┌─────────────────────────────────────────────────────────────────────────────┐
│ ILE (ENTp) "Don Quixote"                                                    │
│ 1-Ne  2-Ti  3-Fi  4-Se  5-Si  6-Fe  7-Ni  8-Te                             │
│ Lead: Possibilities | Creative: Systems | PoLR: Force | Suggestive: Comfort│
├─────────────────────────────────────────────────────────────────────────────┤
│ SEI (ISFp) "Dumas"                                                          │
│ 1-Si  2-Fe  3-Te  4-Ni  5-Ne  6-Ti  7-Se  8-Fi                             │
│ Lead: Comfort | Creative: Emotions | PoLR: Time | Suggestive: Possibilities│
├─────────────────────────────────────────────────────────────────────────────┤
│ ESE (ESFj) "Hugo"                                                           │
│ 1-Fe  2-Si  3-Ni  4-Te  5-Ti  6-Ne  7-Fi  8-Se                             │
│ Lead: Emotions | Creative: Comfort | PoLR: Efficiency | Suggestive: Systems│
├─────────────────────────────────────────────────────────────────────────────┤
│ LII (INTj) "Robespierre"                                                    │
│ 1-Ti  2-Ne  3-Se  4-Fi  5-Fe  6-Si  7-Te  8-Ni                             │
│ Lead: Systems | Creative: Possibilities | PoLR: Relations | Suggestive: Emotions│
└─────────────────────────────────────────────────────────────────────────────┘

BETA QUADRA (Values: Se, Ni, Fe, Ti):
┌─────────────────────────────────────────────────────────────────────────────┐
│ EIE (ENFj) "Hamlet"                                                         │
│ 1-Fe  2-Ni  3-Si  4-Te  5-Ti  6-Se  7-Fi  8-Ne                             │
│ Lead: Emotions | Creative: Time | PoLR: Efficiency | Suggestive: Systems   │
├─────────────────────────────────────────────────────────────────────────────┤
│ LSI (ISTj) "Maxim Gorky"                                                    │
│ 1-Ti  2-Se  3-Ne  4-Fi  5-Fe  6-Ni  7-Te  8-Si                             │
│ Lead: Systems | Creative: Force | PoLR: Relations | Suggestive: Emotions   │
├─────────────────────────────────────────────────────────────────────────────┤
│ SLE (ESTp) "Zhukov"                                                         │
│ 1-Se  2-Ti  3-Fi  4-Ne  5-Ni  6-Fe  7-Si  8-Te                             │
│ Lead: Force | Creative: Systems | PoLR: Possibilities | Suggestive: Time   │
├─────────────────────────────────────────────────────────────────────────────┤
│ IEI (INFp) "Yesenin"                                                        │
│ 1-Ni  2-Fe  3-Te  4-Se  5-Si  6-Ti  7-Ne  8-Fi                             │
│ Lead: Time | Creative: Emotions | PoLR: Force | Suggestive: Comfort        │
└─────────────────────────────────────────────────────────────────────────────┘

GAMMA QUADRA (Values: Se, Ni, Te, Fi):
┌─────────────────────────────────────────────────────────────────────────────┐
│ SEE (ESFp) "Napoleon"                                                       │
│ 1-Se  2-Fi  3-Ne  4-Ti  5-Ni  6-Te  7-Si  8-Fe                             │
│ Lead: Force | Creative: Relations | PoLR: Systems | Suggestive: Time       │
├─────────────────────────────────────────────────────────────────────────────┤
│ ILI (INTp) "Balzac"                                                         │
│ 1-Ni  2-Te  3-Fe  4-Si  5-Se  6-Fi  7-Ne  8-Ti                             │
│ Lead: Time | Creative: Efficiency | PoLR: Comfort | Suggestive: Force      │
├─────────────────────────────────────────────────────────────────────────────┤
│ LIE (ENTj) "Jack London"                                                    │
│ 1-Te  2-Ni  3-Si  4-Fe  5-Fi  6-Se  7-Ti  8-Ne                             │
│ Lead: Efficiency | Creative: Time | PoLR: Emotions | Suggestive: Relations │
├─────────────────────────────────────────────────────────────────────────────┤
│ ESI (ISFj) "Dreiser"                                                        │
│ 1-Fi  2-Se  3-Te  4-Ne  5-Ni  6-Ti  7-Fe  8-Si                             │
│ Lead: Relations | Creative: Force | PoLR: Possibilities | Suggestive: Time │
└─────────────────────────────────────────────────────────────────────────────┘

DELTA QUADRA (Values: Si, Ne, Te, Fi):
┌─────────────────────────────────────────────────────────────────────────────┐
│ IEE (ENFp) "Huxley"                                                         │
│ 1-Ne  2-Fi  3-Ti  4-Se  5-Si  6-Te  7-Ni  8-Fe                             │
│ Lead: Possibilities | Creative: Relations | PoLR: Force | Suggestive: Comfort│
├─────────────────────────────────────────────────────────────────────────────┤
│ SLI (ISTp) "Gabin"                                                          │
│ 1-Si  2-Te  3-Fe  4-Ni  5-Ne  6-Fi  7-Se  8-Ti                             │
│ Lead: Comfort | Creative: Efficiency | PoLR: Time | Suggestive: Possibilities│
├─────────────────────────────────────────────────────────────────────────────┤
│ LSE (ESTj) "Stirlitz"                                                       │
│ 1-Te  2-Si  3-Ni  4-Fe  5-Fi  6-Ne  7-Ti  8-Se                             │
│ Lead: Efficiency | Creative: Comfort | PoLR: Emotions | Suggestive: Relations│
├─────────────────────────────────────────────────────────────────────────────┤
│ EII (INFj) "Dostoevsky"                                                     │
│ 1-Fi  2-Ne  3-Se  4-Ti  5-Te  6-Si  7-Fe  8-Ni                             │
│ Lead: Relations | Creative: Possibilities | PoLR: Systems | Suggestive: Efficiency│
└─────────────────────────────────────────────────────────────────────────────┘
"""

# =============================================================================
# EXPLICIT FUNCTION POSITION LOOKUP - USE THIS TO FACT-CHECK CLAIMS
# =============================================================================

FUNCTION_POSITION_LOOKUP = """
FUNCTION POSITION LOOKUP TABLE - CANONICAL REFERENCE (from SCS Types):

Positions: 1=Leading, 2=Creative, 3=Role, 4=Vulnerable(PoLR), 5=Suggestive, 6=Mobilizing, 7=Ignoring, 8=Demonstrative

USE THIS TO VERIFY ANY CLAIMS ABOUT FUNCTION POSITIONS.

┌───────┬─────────┬──────────┬─────────┬─────────┬─────────┬────────┬───────┬───────┐
│ TYPE  │   1st   │   2nd    │   3rd   │   4th   │   5th   │  6th   │  7th  │  8th  │
│       │  LEAD   │ CREATIVE │  ROLE   │  POLR   │ SUGGEST │ MOBIL  │ IGNOR │ DEMO  │
├───────┼─────────┼──────────┼─────────┼─────────┼─────────┼────────┼───────┼───────┤
│ ILE   │ Ne      │ Ti       │ Se      │ Fi      │ Si      │ Fe     │ Ni    │ Te    │
│ SEI   │ Si      │ Fe       │ Ni      │ Te      │ Ne      │ Ti     │ Se    │ Fi    │
│ ESE   │ Fe      │ Si       │ Te      │ Ni      │ Ti      │ Ne     │ Fi    │ Se    │
│ LII   │ Ti      │ Ne       │ Fi      │ Se      │ Fe      │ Si     │ Te    │ Ni    │
├───────┼─────────┼──────────┼─────────┼─────────┼─────────┼────────┼───────┼───────┤
│ EIE   │ Fe      │ Ni       │ Te      │ Si      │ Ti      │ Se     │ Fi    │ Ne    │
│ LSI   │ Ti      │ Se       │ Fi      │ Ne      │ Fe      │ Ni     │ Te    │ Si    │
│ SLE   │ Se      │ Ti       │ Ne      │ Fi      │ Ni      │ Fe     │ Si    │ Te    │
│ IEI   │ Ni      │ Fe       │ Si      │ Te      │ Se      │ Ti     │ Ne    │ Fi    │
├───────┼─────────┼──────────┼─────────┼─────────┼─────────┼────────┼───────┼───────┤
│ SEE   │ Se      │ Fi       │ Ne      │ Ti      │ Ni      │ Te     │ Si    │ Fe    │
│ ILI   │ Ni      │ Te       │ Si      │ Fe      │ Se      │ Fi     │ Ne    │ Ti    │
│ LIE   │ Te      │ Ni       │ Fe      │ Si      │ Fi      │ Se     │ Ti    │ Ne    │
│ ESI   │ Fi      │ Se       │ Ti      │ Ne      │ Te      │ Ni     │ Fe    │ Si    │
├───────┼─────────┼──────────┼─────────┼─────────┼─────────┼────────┼───────┼───────┤
│ IEE   │ Ne      │ Fi       │ Se      │ Ti      │ Si      │ Te     │ Ni    │ Fe    │
│ SLI   │ Si      │ Te       │ Ni      │ Fe      │ Ne      │ Fi     │ Se    │ Ti    │
│ LSE   │ Te      │ Si       │ Fe      │ Ni      │ Fi      │ Ne     │ Ti    │ Se    │
│ EII   │ Fi      │ Ne       │ Ti      │ Se      │ Te      │ Si     │ Fe    │ Ni    │
└───────┴─────────┴──────────┴─────────┴─────────┴─────────┴────────┴───────┴───────┘

QUICK REFERENCE - VERIFIED STACKS FROM SCS:

SEE (ESFp) "Napoleon":
  1-Se = LEADING - Dominant force/willpower
  2-Fi = CREATIVE - Ethics in service of Se
  3-Ne = ROLE - Can do possibilities but it's effortful
  4-Ti = POLR - Logical systems cause distress ← Pain point!
  5-Ni = SUGGESTIVE - Seeks vision/foresight
  6-Te = MOBILIZING - Motivated by efficiency
  7-Si = IGNORING - Ignores comfort
  8-Fe = DEMONSTRATIVE - Strong but prefers Fi

ILI (INTp) "Balzac":
  1-Ni = LEADING - Dominant vision/foresight
  2-Te = CREATIVE - Efficiency in service of Ni
  3-Si = ROLE - Can do comfort but it's effortful
  4-Fe = POLR - Group emotions cause distress ← Pain point!
  5-Se = SUGGESTIVE - Seeks force/action
  6-Fi = MOBILIZING - Motivated by relationships
  7-Ne = IGNORING - Ignores brainstorming
  8-Ti = DEMONSTRATIVE - Strong logic but prefers Te

ESI (ISFj) "Dreiser":
  1-Fi = LEADING - Dominant ethics/relationships
  2-Se = CREATIVE - Force in service of Fi
  3-Ti = ROLE - Can do logic but it's effortful
  4-Ne = POLR - Possibilities cause distress ← Pain point!
  5-Te = SUGGESTIVE - Seeks efficiency
  6-Ni = MOBILIZING - Motivated by vision
  7-Fe = IGNORING - Ignores group emotions
  8-Si = DEMONSTRATIVE - Strong comfort awareness

SLE (ESTp) "Zhukov":
  1-Se = LEADING - Dominant force/willpower
  2-Ti = CREATIVE - Logic in service of Se ← STRONG Ti!
  3-Ne = ROLE - Can brainstorm but prefers action
  4-Fi = POLR - Personal relationships cause distress
  5-Ni = SUGGESTIVE - Seeks vision
  6-Fe = MOBILIZING - Motivated by group harmony
  7-Si = IGNORING - Ignores comfort
  8-Te = DEMONSTRATIVE - Strong efficiency but prefers Ti

KEY FACTS:
- SEE has Ti PoLR, Ne Role (struggles with logical analysis)
- ESI has Ne PoLR, Ti Role (struggles with uncertainty)
- SLE has Fi PoLR but STRONG Ti (Creative) - can be very logical
- ILI has Fe PoLR (struggles with group emotional harmony)
"""


# =============================================================================
# REININ DICHOTOMIES
# =============================================================================

REININ_DICHOTOMIES = """
THE 15 REININ DICHOTOMIES:

These are mathematically derived trait pairs that divide the 16 types evenly.

BASE JUNGIAN DICHOTOMIES (4):
1. Extroversion/Introversion (E/I)
2. Intuition/Sensing (N/S)  
3. Logic/Ethics (T/F)
4. Irrational/Rational (P/J)

DERIVED DICHOTOMIES (11):

STATIC vs DYNAMIC (E*P):
- Static (IJ + EP): Perceive reality as discrete states, snapshots
- Dynamic (IP + EJ): Perceive reality as continuous processes, flows
Static types: ILE, LII, ESE, SEI, SLE, LSI, EIE, IEI, ILI, LIE, ESI, SEE, SLI, LSE, EII, IEE

POSITIVIST vs NEGATIVIST (E*N*T):
- Positivist: Focus on presence of qualities, what IS there
- Negativist: Focus on absence of qualities, what is NOT there
Positivists: SEI, ESE, LSI, IEI, SEE, LIE, EII, SLI
Negativists: ILE, LII, SLE, EIE, ILI, ESI, LSE, IEE

ASKING vs DECLARING (E*N*T*P = ENTP):
- Asking/Questioners: Communicate through questions, dialogue-oriented
- Declaring: Communicate through statements, monologue-oriented
Asking: ILE, LII, EIE, IEI, SEE, ESI, LSE, SLI
Declaring: SEI, ESE, SLE, LSI, ILI, LIE, EII, IEE

TACTICAL vs STRATEGIC (N*P):
- Tactical: Focus on methods, HOW to do something
- Strategic: Focus on goals, WHAT to achieve
Tactical: ILE, ESE, LSI, IEI, ILI, SEE, EII, LSE
Strategic: SEI, LII, SLE, EIE, LIE, ESI, SLI, IEE

CONSTRUCTIVIST vs EMOTIVIST (T*P):
- Constructivist: Build emotional states through logical analysis
- Emotivist: Build logical conclusions through emotional experience
Constructivists: ILE, ESE, SLE, EIE, ILI, SEE, SLI, EII
Emotivists: SEI, LII, LSI, IEI, LIE, ESI, LSE, IEE

PROCESS vs RESULT (N*T*P):
- Process: Value the journey, procedure, step-by-step
- Result: Value the outcome, end justifies means
Process: ILE, SEI, EIE, LSI, SEE, ILI, LSE, EII
Result: LII, ESE, SLE, IEI, LIE, ESI, SLI, IEE

COMPLIANT vs OBSTINATE (E*T):
- Compliant: Yield on objects/territory, hold firm on relationships
- Obstinate: Hold firm on objects/territory, yield on relationships
Compliant: ILE, LII, SEI, ESE, LIE, ESI, SLI, IEE
Obstinate: SLE, LSI, EIE, IEI, SEE, ILI, LSE, EII

CAREFREE vs FARSIGHTED (E*N):
- Carefree: Deal with problems as they arise, present-focused
- Farsighted: Anticipate and prepare for problems, future-focused
Carefree: ILE, SEI, SLE, LSI, ESI, LIE, SLI, IEE
Farsighted: LII, ESE, EIE, IEI, SEE, ILI, LSE, EII

MERRY vs SERIOUS:
- Merry: Prefer group interaction, collaborative atmosphere
- Serious: Prefer one-on-one, intensive interaction
(This dichotomy relates to valuing Fe+Ti vs Te+Fi)

JUDICIOUS vs DECISIVE (E*N*P):
- Judicious: Consider multiple perspectives before acting, deliberate
- Decisive: Act quickly based on initial assessment, resolute
Judicious: ILE, SEI, LII, ESE, LSE, EII, SLI, IEE
Decisive: SLE, LSI, EIE, IEI, SEE, ILI, LIE, ESI

ARISTOCRATIC vs DEMOCRATIC (N*T):
- Aristocratic: Think in terms of groups, categories, collective identity
- Democratic: Think in terms of individuals, personal qualities
Aristocratic: EIE, LSI, IEI, SLE, LSE, EII, SLI, IEE
Democratic: ILE, SEI, LII, ESE, SEE, ILI, LIE, ESI

YIELDING vs STUBBORN:
- Yielding: Flexible on opinions, firm on actions
- Stubborn: Firm on opinions, flexible on actions

SUBJECTIVIST vs OBJECTIVIST (E*T*P):
- Subjectivist: Trust personal/internal criteria
- Objectivist: Trust external/universal criteria
Subjectivists: ILE, SEI, LII, ESE, SLE, LSI, EIE, IEI
Objectivists: SEE, ILI, LIE, ESI, LSE, EII, SLI, IEE
"""

# =============================================================================
# REININ TRAITS BY TYPE
# =============================================================================

REININ_BY_TYPE = """
REININ DICHOTOMY ASSIGNMENTS FOR ALL 16 TYPES:

ILE (ENTp): judicious, subjectivist, democratic, process, carefree, yielding, static, tactical, constructivist, positivist, asking
SEI (ISFp): judicious, subjectivist, democratic, process, carefree, yielding, dynamic, strategic, emotivist, negativist, declaring
LII (INTj): judicious, subjectivist, democratic, result, farsighted, obstinate, static, strategic, emotivist, negativist, asking
ESE (ESFj): judicious, subjectivist, democratic, result, farsighted, obstinate, dynamic, tactical, constructivist, positivist, declaring

EIE (ENFj): decisive, subjectivist, aristocratic, process, carefree, obstinate, dynamic, strategic, constructivist, negativist, asking
LSI (ISTj): decisive, subjectivist, aristocratic, process, carefree, obstinate, static, tactical, emotivist, positivist, declaring
IEI (INFp): decisive, subjectivist, aristocratic, result, farsighted, yielding, dynamic, tactical, emotivist, positivist, asking
SLE (ESTp): decisive, subjectivist, aristocratic, result, farsighted, yielding, static, strategic, constructivist, negativist, declaring

SEE (ESFp): decisive, objectivist, democratic, process, farsighted, obstinate, static, strategic, emotivist, positivist, asking
ILI (INTp): decisive, objectivist, democratic, process, farsighted, obstinate, dynamic, tactical, constructivist, negativist, declaring
ESI (ISFj): decisive, objectivist, democratic, result, carefree, yielding, static, tactical, constructivist, negativist, asking
LIE (ENTj): decisive, objectivist, democratic, result, carefree, yielding, dynamic, strategic, emotivist, positivist, declaring

LSE (ESTj): judicious, objectivist, aristocratic, process, farsighted, yielding, dynamic, tactical, emotivist, negativist, asking
EII (INFj): judicious, objectivist, aristocratic, process, farsighted, yielding, static, strategic, constructivist, positivist, declaring
SLI (ISTp): judicious, objectivist, aristocratic, result, carefree, obstinate, dynamic, strategic, constructivist, positivist, asking
IEE (ENFp): judicious, objectivist, aristocratic, result, carefree, obstinate, static, tactical, emotivist, negativist, declaring
"""

# =============================================================================
# QUADRA VALUES
# =============================================================================

QUADRA_VALUES = """
QUADRA VALUES - What Each Quadra Prioritizes:

Quadra values are the information elements that appear in Ego (strong, conscious) 
or Super-Id (weak but valued) positions for all types in that quadra.

ALPHA QUADRA (ILE, SEI, ESE, LII):
Valued: Si + Ne + Fe + Ti
- Prioritize comfort, harmony, and intellectual exploration
- Value playful discussions, brainstorming, warmth
- Prefer democratic, egalitarian group dynamics
- Enjoy novelty, possibilities, and theoretical debate
- Seek comfortable environments that allow free thinking
- AVOID: Power games, harshness, forced action, pessimism

BETA QUADRA (EIE, LSI, SLE, IEI):
Valued: Se + Ni + Fe + Ti  
- Prioritize passion, drama, decisive action, and vision
- Value emotional intensity and collective causes
- Prefer hierarchical structures with clear leadership
- Enjoy willpower challenges and dramatic narratives
- Seek meaningful struggles and grand purposes
- AVOID: Boredom, weakness, lack of conviction, triviality

GAMMA QUADRA (SEE, ILI, LIE, ESI):
Valued: Se + Ni + Te + Fi
- Prioritize achievement, profit, and personal integrity
- Value competition, results, and personal responsibility
- Prefer pragmatic individualism, each person carries their weight
- Enjoy business dealings, strategic action, loyalty
- Seek effectiveness and authentic relationships
- AVOID: Inefficiency, emotional manipulation, dependency, group-think

DELTA QUADRA (IEE, SLI, LSE, EII):
Valued: Si + Ne + Te + Fi
- Prioritize helpfulness, sincerity, and practical solutions
- Value quiet competence, mentoring, authenticity
- Prefer democratic approach focused on personal growth
- Enjoy useful work, genuine care, alternative perspectives
- Seek comfortable productivity and real human connection
- AVOID: Force, manipulation, superficiality, hierarchy for its own sake
"""

# =============================================================================
# COMMON TYPING MISTAKES
# =============================================================================

TYPING_MISTAKES = """
COMMON SOCIONICS TYPING MISTAKES TO AVOID:

1. CONFUSING FUNCTION POSITION WITH STRENGTH
   - A strong function (1,2,7,8) isn't necessarily used often - 7 and 8 are subdued
   - A weak function (3,4,5,6) can still be prominently displayed when stressed or when compensating

2. CONFUSING QUADRA VALUES WITH TYPE
   - All types in a quadra share values but express them very differently
   - An LII and an ESE both value Fe, but LII seeks it (suggestive) while ESE leads with it

3. MISTAKING ROLE FUNCTION FOR BASE
   - The role function (3rd) can look like confident use when someone is "performing"
   - But it's exhausting and inconsistent, unlike true base function use

4. IGNORING POLR (4th Function)
   - The PoLR is often the clearest typing marker
   - What does the person AVOID, dismiss, or become distressed about?
   - Fe PoLR: Avoids emotional displays, keeps conversations "to the point"
   - Ne PoLR: Fears uncertainty, struggles with "what-ifs"
   - Si PoLR: Ignores physical needs, can't relax
   - Te PoLR: Rejects external facts, defensive about efficiency

5. CONFUSING INTROVERSION/EXTRAVERSION
   - Socionics E/I is about the LEADING function, not social behavior
   - An introverted type can be very social (SEI is often warm and engaging)
   - An extraverted type can be reserved (ILE can seem detached when theorizing)

6. MISTAKING SUGGESTIVE FOR WEAKNESS
   - The suggestive function (5th) is weak but highly valued
   - People WANT information here and respond positively to it
   - Contrast with PoLR (4th) which is weak and causes distress

7. APPLYING MBTI LOGIC TO SOCIONICS
   - MBTI J/P is about external behavior
   - Socionics j/p is about the leading function being rational or irrational
   - MBTI INTP = Socionics INTj (LII) NOT INTp (ILI)
"""

# =============================================================================
# BEHAVIORAL MARKERS BY FUNCTION POSITION
# =============================================================================

BEHAVIORAL_MARKERS = """
BEHAVIORAL MARKERS BY FUNCTION AND POSITION:

When an element is in the LEADING (1st) position, the person:
- Constantly references this aspect in conversation
- Makes categorical, confident statements about it
- Projects that everyone values this
- Pursues it actively and effortlessly
- Gets deeply engaged when discussing it

When an element is in the CREATIVE (2nd) position, the person:
- Uses it to support and implement their leading function goals
- Turns it on and off - inconsistent focus
- Offers help to others using this function
- May correct others' overemphasis on it

When an element is in the ROLE (3rd) position, the person:
- Attempts to develop it periodically then gives up
- Performs it when socially expected
- Feels awkward or exhausted using it
- Sees it as self-improvement area

When an element is in the POLR (4th) position, the person:
- Ignores or dismisses its importance
- Becomes distressed when forced to engage with it
- Develops minimalist or unconventional approaches
- May overcompensate or completely avoid

When an element is in the SUGGESTIVE (5th) position, the person:
- Lights up when receiving information about it
- Never feels it's "too much"
- Seeks it from others
- Feels soothed by its presence

When an element is in the ACTIVATING (6th) position, the person:
- Appreciates it but in moderation
- Has a "hidden agenda" related to it
- May indulge recklessly or neglect entirely
- Uses it sporadically

When an element is in the IGNORING (7th) position, the person:
- Finds extensive discussion of it boring
- Can use it well but prefers not to
- Uses it privately or as backup
- Sees focus on it as missing the point

When an element is in the DEMONSTRATIVE (8th) position, the person:
- Uses it playfully or to ridicule overemphasis
- Takes it for granted
- Protects others' weak points in this area
- Considers information about it obvious
"""

# =============================================================================
# ASSEMBLED FULL REFERENCE
# =============================================================================

FULL_SOCIONICS_REFERENCE = f"""
{MODEL_A_POSITIONS}

{FUNCTION_DESCRIPTIONS}

{INFORMATION_ELEMENTS}

{TYPE_FUNCTION_STACKS}

{FUNCTION_POSITION_LOOKUP}

{REININ_DICHOTOMIES}

{REININ_BY_TYPE}

{QUADRA_VALUES}

{TYPING_MISTAKES}

{BEHAVIORAL_MARKERS}
"""

