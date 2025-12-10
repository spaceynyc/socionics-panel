"""
PDF Report Generator for Socionics Analysis

Generates visually stunning Dark Mode Swiss-style PDF reports with
an engineering blueprint aesthetic and Swiss Grid layout.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics import renderPDF
from io import BytesIO
from datetime import datetime


class LabTheme:
    """Dark Mode Swiss color palette for the Autonomous Socionics Research Lab."""
    # Core backgrounds
    BACKGROUND = HexColor('#0E1117')      # Streamlit dark background
    SURFACE = HexColor('#262730')          # Lighter grey for cards/boxes
    
    # Text colors
    TEXT_MAIN = HexColor('#FFFFFF')        # White - primary text
    TEXT_DIM = HexColor('#FAFAFA')         # Off-white - body text
    TEXT_LIGHT_GREY = HexColor('#B0B0B0')  # Lighter grey for secondary text
    
    # Accent colors
    ACCENT_CYAN = HexColor('#00E5FF')      # Headers, lines, highlights
    ACCENT_GREEN = HexColor('#00FF00')     # High confidence, success
    ACCENT_RED = HexColor('#FF4B4B')       # Alerts, low confidence
    
    # Grid overlay color (very low opacity grey)
    GRID_COLOR = Color(0.3, 0.3, 0.35, alpha=0.3)
    
    # Quadra colors for type badges
    QUADRA_ALPHA = HexColor('#9C27B0')     # Purple for Alpha
    QUADRA_BETA = HexColor('#FF4B4B')      # Red for Beta
    QUADRA_GAMMA = HexColor('#2196F3')     # Blue for Gamma
    QUADRA_DELTA = HexColor('#4CAF50')     # Green for Delta
    
    @classmethod
    def get_quadra_color(cls, quadra: str):
        """Get the color for a given quadra."""
        quadra_map = {
            'alpha': cls.QUADRA_ALPHA,
            'beta': cls.QUADRA_BETA,
            'gamma': cls.QUADRA_GAMMA,
            'delta': cls.QUADRA_DELTA,
        }
        return quadra_map.get(quadra.lower(), cls.ACCENT_CYAN)


def draw_dark_background(canvas, doc):
    """
    Draw the dark background.
    Called on every page build.
    """
    width, height = A4
    
    # Draw the main dark background (solid, no grid)
    canvas.setFillColor(LabTheme.BACKGROUND)
    canvas.rect(0, 0, width, height, fill=1, stroke=0)


def create_custom_styles():
    """Create custom paragraph styles for the Dark Mode Swiss PDF with Swiss Grid typography."""
    styles = getSampleStyleSheet()
    
    # Lab Title - Massive bold header
    styles.add(ParagraphStyle(
        name='LabTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=LabTheme.TEXT_MAIN,
        alignment=TA_LEFT,
        spaceAfter=0
    ))
    
    # Timestamp style - Cyan accent
    styles.add(ParagraphStyle(
        name='Timestamp',
        fontName='Helvetica',
        fontSize=10,
        textColor=LabTheme.ACCENT_CYAN,
        alignment=TA_RIGHT,
        spaceAfter=0
    ))
    
    # Hero Name - Massive white text for character name (30pt)
    styles.add(ParagraphStyle(
        name='HeroName',
        fontName='Helvetica-Bold',
        fontSize=30,
        textColor=LabTheme.TEXT_MAIN,
        alignment=TA_LEFT,
        spaceAfter=8,
        leading=36
    ))
    
    # Hero Type - Large type display (reduced to prevent overlap)
    styles.add(ParagraphStyle(
        name='HeroType',
        fontName='Helvetica-Bold',
        fontSize=28,
        textColor=LabTheme.TEXT_MAIN,
        alignment=TA_LEFT,
        spaceAfter=18
    ))
    
    # Tracked Label - Uppercase, tracked-out letters for labels
    # Swiss design uses uppercase with letter-spacing for labels
    styles.add(ParagraphStyle(
        name='TrackedLabel',
        fontName='Helvetica-Bold',
        fontSize=9,
        textColor=LabTheme.ACCENT_CYAN,
        alignment=TA_LEFT,
        spaceAfter=4,
        spaceBefore=10
    ))
    
    # Data Value - Large numbers/values for data blocks
    styles.add(ParagraphStyle(
        name='DataValue',
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=LabTheme.TEXT_MAIN,
        alignment=TA_LEFT,
        spaceAfter=0
    ))
    
    # Report Title
    styles.add(ParagraphStyle(
        name='ReportTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=LabTheme.ACCENT_CYAN,
        alignment=TA_LEFT,  # Swiss: Flush left
        spaceAfter=20
    ))
    
    # Report Subtitle
    styles.add(ParagraphStyle(
        name='ReportSubtitle',
        fontName='Helvetica',
        fontSize=11,
        textColor=LabTheme.TEXT_DIM,
        alignment=TA_LEFT,  # Swiss: Flush left
        spaceAfter=25
    ))
    
    # Section Heading - Uppercase for Swiss style
    styles.add(ParagraphStyle(
        name='SectionHeading',
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=LabTheme.ACCENT_CYAN,
        alignment=TA_LEFT,
        spaceBefore=25,
        spaceAfter=15
    ))
    
    # Sub Heading
    styles.add(ParagraphStyle(
        name='SubHeading',
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=LabTheme.ACCENT_CYAN,
        alignment=TA_LEFT,
        spaceBefore=10,
        spaceAfter=4
    ))
    
    # Card Title - For agent card headers
    styles.add(ParagraphStyle(
        name='CardTitle',
        fontName='Helvetica-Bold',
        fontSize=11,
        textColor=LabTheme.TEXT_MAIN,
        alignment=TA_LEFT,
        spaceAfter=4
    ))
    
    # Card Body - Body text inside cards (generous line spacing for readability)
    styles.add(ParagraphStyle(
        name='CardBody',
        fontName='Helvetica',
        fontSize=10,
        textColor=LabTheme.TEXT_DIM,
        alignment=TA_LEFT,  # Swiss: Flush left, ragged right
        spaceAfter=8,
        leading=18  # Generous line spacing for readability
    ))
    
    # Report Body - Main text (flush left)
    styles.add(ParagraphStyle(
        name='ReportBody',
        fontName='Helvetica',
        fontSize=10,
        textColor=LabTheme.TEXT_DIM,
        alignment=TA_LEFT,  # Swiss: Flush left
        spaceAfter=8,
        leading=16
    ))
    
    # Small Text - Secondary info
    styles.add(ParagraphStyle(
        name='SmallText',
        fontName='Helvetica',
        fontSize=9,
        textColor=LabTheme.TEXT_DIM,
        alignment=TA_LEFT,
        spaceAfter=8,
        leading=15
    ))
    
    # Type Code - Large type display (centered for hero banner fallback)
    styles.add(ParagraphStyle(
        name='TypeCode',
        fontName='Helvetica-Bold',
        fontSize=42,
        textColor=LabTheme.ACCENT_CYAN,
        alignment=TA_CENTER,
        spaceAfter=5
    ))
    
    # Type Name
    styles.add(ParagraphStyle(
        name='TypeName',
        fontName='Helvetica',
        fontSize=13,
        textColor=LabTheme.TEXT_DIM,
        alignment=TA_LEFT,
        spaceAfter=20
    ))
    
    # Success text
    styles.add(ParagraphStyle(
        name='SuccessText',
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=LabTheme.ACCENT_GREEN,
        alignment=TA_LEFT,
        spaceAfter=6
    ))
    
    # Alert text
    styles.add(ParagraphStyle(
        name='AlertText',
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=LabTheme.ACCENT_RED,
        alignment=TA_LEFT,
        spaceAfter=6
    ))
    
    # Disclaimer text - Monospaced for technical report vibe
    styles.add(ParagraphStyle(
        name='Disclaimer',
        fontName='Courier',
        fontSize=7,
        textColor=LabTheme.TEXT_LIGHT_GREY,
        alignment=TA_LEFT,
        spaceAfter=0,
        leading=9
    ))
    
    return styles



def _tracked_text(text: str) -> str:
    """
    Format text as a stylized label with Title Case.
    Previously had letter-spacing, now just returns clean Title Case.
    """
    return text.title()


def _format_markdown_for_pdf(text: str) -> str:
    """
    Convert markdown-style formatting to ReportLab-compatible HTML.
    Handles: **bold**, headers, bullet points, numbered lists, paragraphs.
    """
    import re
    
    if not text:
        return ""
    
    # Convert **text** to <b>text</b>
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    
    # Convert *text* to <i>text</i>
    text = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', text)
    
    # Split into paragraphs (double newline or numbered/bulleted sections)
    paragraphs = []
    current = []
    
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            if current:
                paragraphs.append(' '.join(current))
                current = []
        elif line.startswith(('- ', '• ', '* ')):
            # Bullet point
            if current:
                paragraphs.append(' '.join(current))
                current = []
            paragraphs.append('• ' + line[2:].strip())
        elif re.match(r'^\d+\.', line):
            # Numbered list
            if current:
                paragraphs.append(' '.join(current))
                current = []
            paragraphs.append(line)
        else:
            current.append(line)
    
    if current:
        paragraphs.append(' '.join(current))
    
    # Join with proper spacing
    return '<br/><br/>'.join(paragraphs)


def _create_hero_module(dossier: dict, final_result: dict, styles) -> list:
    """
    Create the Hero Module as a list of flowable elements.
    Returns a list that can be extended into the story.
    """
    character_name = dossier.get('character_name', 'Unknown')
    media_source = dossier.get('media_source', 'Unknown Source')
    final_type = final_result.get('final_type', '???')
    quadra = final_result.get('quadra', 'Unknown')
    confidence = final_result.get('confidence_score', 0)
    type_name = final_result.get('type_name', '')
    
    # Determine confidence color
    if confidence >= 80:
        conf_color = LabTheme.ACCENT_GREEN.hexval()
    elif confidence >= 50:
        conf_color = LabTheme.ACCENT_CYAN.hexval()
    else:
        conf_color = LabTheme.ACCENT_RED.hexval()
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # Truncate very long media sources
    if len(media_source) > 60:
        media_source = media_source[:57] + "..."
    
    # Build flowables list (no fixed heights, auto-sizes)
    elements = [
        # Character name
        Paragraph(character_name, styles['HeroName']),
        Paragraph(f'<font color="{LabTheme.TEXT_LIGHT_GREY.hexval()}">{media_source}</font>', styles['SmallText']),
        Spacer(1, 15),
        
        # Type code
        Paragraph(final_type, styles['HeroType']),
        Paragraph(f'{type_name} — {quadra} Quadra', styles['CardBody']),
        Spacer(1, 10),
        
        # Stats line
        Paragraph(
            f'<font color="{conf_color}"><b>Confidence: {confidence}%</b></font> &nbsp;&nbsp;|&nbsp;&nbsp; '
            f'<font color="{LabTheme.ACCENT_CYAN.hexval()}">Analyzed: {timestamp}</font>',
            styles['ReportBody']
        ),
    ]
    
    return elements


def _create_agent_card(agent_name: str, predicted_type: str, confidence: int, 
                       reasoning: str, styles) -> Table:
    """
    Create an Agent Card with surface background and left tab border.
    Swiss Grid card style with 10px padding and white left border tab.
    """
    # Card content
    card_content = [
        [Paragraph(agent_name.upper(), styles['CardTitle'])],
        [Paragraph(f'<b>Type:</b> {predicted_type} &nbsp;|&nbsp; <b>Confidence:</b> {confidence}%', styles['CardBody'])],
    ]
    
    if reasoning:
        # Show full reasoning (no truncation for agent cards)
        card_content.append([Paragraph(reasoning, styles['CardBody'])])
    
    card_table = Table(card_content, colWidths=[6.5*inch])
    card_table.setStyle(TableStyle([
        # Surface background
        ('BACKGROUND', (0, 0), (-1, -1), LabTheme.SURFACE),
        # White left border "tab" effect (1pt)
        ('LINEBEFORE', (0, 0), (0, -1), 2, LabTheme.TEXT_MAIN),
        # Padding (10px ≈ 7pt)
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        # Alignment
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    return card_table


def _create_confidence_bar(confidence: int, width_inches: float = 6.5) -> Drawing:
    """
    Create a geometric confidence bar using reportlab.graphics.
    
    Args:
        confidence: Confidence percentage (0-100)
        width_inches: Total width of the bar in inches
        
    Returns:
        Drawing object containing the confidence bar
    """
    bar_width = width_inches * inch
    bar_height = 4 * mm  # 4mm tall as specified
    
    # Create the drawing canvas
    d = Drawing(bar_width, bar_height + 2*mm)  # Extra space for visual breathing
    
    # Background bar (dark grey)
    bg_bar = Rect(0, 0, bar_width, bar_height)
    bg_bar.fillColor = LabTheme.SURFACE
    bg_bar.strokeColor = None
    d.add(bg_bar)
    
    # Fill bar (color based on confidence)
    if confidence > 0:
        fill_width = (confidence / 100.0) * bar_width
        
        # Color: Green if >80%, Cyan otherwise
        if confidence >= 80:
            fill_color = LabTheme.ACCENT_GREEN
        elif confidence >= 50:
            fill_color = LabTheme.ACCENT_CYAN
        else:
            fill_color = LabTheme.ACCENT_RED
        
        fill_bar = Rect(0, 0, fill_width, bar_height)
        fill_bar.fillColor = fill_color
        fill_bar.strokeColor = None
        d.add(fill_bar)
    
    return d


def _create_dichotomy_matrix(dichotomies: list, styles) -> Table:
    """
    Create a visual matrix of Reinin dichotomies using 10x10mm squares.
    
    Filled square = the trait the type HAS
    Empty square = the opposite trait
    
    Args:
        dichotomies: List of dicts with 'trait' and 'has' keys
                     e.g., [{'trait': 'Static', 'opposite': 'Dynamic', 'has': True}, ...]
        styles: PDF styles dict
        
    Returns:
        Table containing the dichotomy matrix
    """
    if not dichotomies:
        return None
    
    # Each dichotomy gets a 10x10mm square
    square_size = 10 * mm
    squares_per_row = 8  # 8 squares per row for good layout
    
    rows = []
    current_row_squares = []
    current_row_labels = []
    
    for dich in dichotomies:
        trait = dich.get('trait', '?')
        opposite = dich.get('opposite', '?')
        has_trait = dich.get('has', True)
        
        # Create the square drawing
        d = Drawing(square_size, square_size)
        
        if has_trait:
            # Filled square for the trait the type HAS
            square = Rect(1*mm, 1*mm, square_size - 2*mm, square_size - 2*mm)
            square.fillColor = LabTheme.ACCENT_CYAN
            square.strokeColor = LabTheme.ACCENT_CYAN
            square.strokeWidth = 0.5
        else:
            # Empty/outline square for the opposite
            square = Rect(1*mm, 1*mm, square_size - 2*mm, square_size - 2*mm)
            square.fillColor = None
            square.strokeColor = LabTheme.SURFACE
            square.strokeWidth = 1
        
        d.add(square)
        current_row_squares.append(d)
        
        # Label (show the trait name, uppercase, size 6)
        label = trait.upper() if has_trait else opposite.upper()
        current_row_labels.append(Paragraph(
            f'<font size="6">{label[:6]}</font>',  # Truncate to 6 chars
            styles['SmallText']
        ))
        
        # Start new row if needed
        if len(current_row_squares) >= squares_per_row:
            rows.append(current_row_squares)
            rows.append(current_row_labels)
            current_row_squares = []
            current_row_labels = []
    
    # Add remaining items
    if current_row_squares:
        # Pad with empty cells if needed
        while len(current_row_squares) < squares_per_row:
            current_row_squares.append('')
            current_row_labels.append('')
        rows.append(current_row_squares)
        rows.append(current_row_labels)
    
    if not rows:
        return None
    
    # Create the table
    col_widths = [square_size + 2*mm] * squares_per_row
    matrix_table = Table(rows, colWidths=col_widths)
    matrix_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 1),
        ('RIGHTPADDING', (0, 0), (-1, -1), 1),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
    ]))
    
    return matrix_table


# Reinin dichotomy pairs for reference
REININ_PAIRS = [
    ('Static', 'Dynamic'),
    ('Positivist', 'Negativist'),
    ('Asking', 'Declaring'),
    ('Tactical', 'Strategic'),
    ('Constructivist', 'Emotivist'),
    ('Process', 'Result'),
    ('Compliant', 'Obstinate'),
    ('Careless', 'Farsighted'),
    ('Merry', 'Serious'),
    ('Judicious', 'Decisive'),
    ('Aristocratic', 'Democratic'),
]


def generate_pdf_report(dossier: dict, council_results: dict, 
                        discussion_results: dict, validation_results: dict, 
                        final_result: dict) -> bytes:
    """
    Generate a Dark Mode Swiss-style PDF report with Swiss Grid layout.
    
    Features:
    - Hero Module with 30%/70% column split
    - Agent Cards with surface background and left tab borders
    - Flush left, ragged right typography
    - Tracked uppercase labels
    
    Args:
        dossier: Character dossier from Scout
        council_results: Results from the three Council agents
        discussion_results: Discussion phase results
        validation_results: Validation phase results  
        final_result: Final synthesized result from Manager
        
    Returns:
        PDF as bytes
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4,
        leftMargin=0.6*inch,
        rightMargin=0.6*inch,
        topMargin=1.2*inch,  # Extra top margin for header
        bottomMargin=0.8*inch  # Extra bottom margin for footer disclaimer
    )
    
    styles = create_custom_styles()
    story = []
    
    # === HERO MODULE (Top of Page 1) ===
    # Simple stacked layout with auto-sizing
    hero_elements = _create_hero_module(dossier, final_result, styles)
    story.extend(hero_elements)
    story.append(Spacer(1, 15))
    
    # === CONFIDENCE BAR (Geometric visualization) ===
    confidence = final_result.get('confidence_score', 0)
    confidence_bar = _create_confidence_bar(confidence)
    story.append(confidence_bar)
    story.append(Spacer(1, 15))
    
    # Key traits and function stack below hero
    traits = final_result.get('key_traits', [])
    if traits:
        story.append(Paragraph(_tracked_text('Key Traits'), styles['TrackedLabel']))
        traits_text = " • ".join(traits)
        story.append(Paragraph(traits_text, styles['ReportBody']))
    
    function_stack = final_result.get('function_stack', '')
    if function_stack:
        story.append(Paragraph(_tracked_text('Function Stack'), styles['TrackedLabel']))
        story.append(Paragraph(function_stack, styles['ReportBody']))
    
    # Summary
    summary = final_result.get('summary', '')
    if summary:
        story.append(Spacer(1, 10))
        story.append(Paragraph(summary, styles['ReportBody']))
    
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=LabTheme.SURFACE))
    
    # === AGENT CARDS (Page 2) ===
    story.append(PageBreak())  # Start new page for Agent Analysis
    story.append(Paragraph(_tracked_text('Agent Analysis'), styles['SectionHeading']))
    story.append(Spacer(1, 8))
    
    # Create cards for each agent
    for agent_name, key in [("Agent Reinin", "reinin"), ("Agent Quadra", "quadra"), ("Agent Functions", "functions")]:
        agent_data = council_results.get(key, {})
        predicted_type = agent_data.get('predicted_type', 'N/A')
        confidence = agent_data.get('confidence', 0)
        reasoning = agent_data.get('reasoning', '')
        
        card = _create_agent_card(agent_name, predicted_type, confidence, reasoning, styles)
        story.append(card)
        story.append(Spacer(1, 8))  # Space between cards
    
    # === VALIDATION RESULTS ===
    if validation_results:
        story.append(Spacer(1, 12))
        story.append(Paragraph(_tracked_text('Theoretical Validation'), styles['SectionHeading']))
        
        errors = validation_results.get('errors_found', [])
        if errors and len(errors) > 0:
            story.append(Paragraph(f"⚠️ Found {len(errors)} theoretical concern(s)", styles['AlertText']))
            for error in errors:
                if isinstance(error, dict):
                    error_text = f"• <b>{error.get('agent', 'Agent')}</b>: {error.get('claim', '')} → {error.get('correction', '')}"
                    story.append(Paragraph(error_text, styles['SmallText']))
        else:
            story.append(Paragraph("✓ No theoretical errors identified", styles['SuccessText']))
        
        if validation_results.get('summary'):
            story.append(Spacer(1, 5))
            story.append(Paragraph(validation_results['summary'], styles['SmallText']))
    
    # === DISCUSSION HIGHLIGHTS (New Page) ===
    if discussion_results:
        story.append(PageBreak())  # Start new page for Discussion
        story.append(Paragraph(_tracked_text('Agent Discussion'), styles['SectionHeading']))
        
        for agent_name, response in discussion_results.items():
            if response:
                # Format response with proper markdown conversion
                formatted_response = _format_markdown_for_pdf(response)
                story.append(Paragraph(f"<b>{agent_name}</b>", styles['SubHeading']))
                story.append(Paragraph(formatted_response, styles['CardBody']))
                story.append(Spacer(1, 15))
    
    # === CHARACTER DOSSIER SUMMARY (New Page) ===
    story.append(PageBreak())  # Start new page for Character Dossier
    story.append(Paragraph(_tracked_text('Character Dossier'), styles['SectionHeading']))
    
    # Key quotes
    quotes = dossier.get('key_quotes', [])
    if quotes and len(quotes) > 0:
        story.append(Paragraph(_tracked_text('Selected Quotes'), styles['TrackedLabel']))
        for i, quote_obj in enumerate(quotes[:5]):  # Limit to 5 quotes
            if isinstance(quote_obj, dict):
                quote_text = f'"{quote_obj.get("quote", "")}" — {quote_obj.get("context", "")}'
            else:
                quote_text = f'"{quote_obj}"'
            story.append(Paragraph(f"• {quote_text}", styles['SmallText']))
    
    # Biographical facts from Scout
    facts = dossier.get('biographical_facts', dossier.get('behavioral_facts', []))
    if facts and len(facts) > 0:
        story.append(Spacer(1, 15))
        story.append(Paragraph(_tracked_text('Biographical Facts'), styles['TrackedLabel']))
        for fact in facts:
            if fact:
                story.append(Paragraph(f"• {fact}", styles['SmallText']))
    
    # === FOOTER (in story - for last page content) ===
    story.append(Spacer(1, 30))
    story.append(HRFlowable(width="100%", thickness=1, color=LabTheme.SURFACE))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        _tracked_text('Autonomous Socionics Research Lab') + " • Multi-Agent Analysis System",
        styles['SmallText']
    ))
    
    def draw_header_footer(canvas, doc):
        """Draw the header and footer on each page."""
        width, height = A4
        
        # First draw the dark background with grid
        draw_dark_background(canvas, doc)
        
        # Draw header
        canvas.saveState()
        
        # Lab title - Top (smaller font to fit with timestamp)
        canvas.setFont('Helvetica-Bold', 16)
        canvas.setFillColor(LabTheme.TEXT_MAIN)
        canvas.drawString(0.6*inch, height - 0.45*inch, "AUTONOMOUS SOCIONICS RESEARCH LAB")
        
        # Timestamp - Same line, right aligned
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(LabTheme.ACCENT_CYAN)
        canvas.drawRightString(width - 0.6*inch, height - 0.45*inch, timestamp)
        
        # Separator line - Full width cyan line under header
        canvas.setStrokeColor(LabTheme.ACCENT_CYAN)
        canvas.setLineWidth(2)
        canvas.line(0.6*inch, height - 0.6*inch, width - 0.6*inch, height - 0.6*inch)
        
        # === FOOTER (on every page) ===
        # Page number on top line
        page_num = doc.page
        canvas.setFont('Courier', 8)
        canvas.setFillColor(LabTheme.TEXT_LIGHT_GREY)
        canvas.drawRightString(width - 0.6*inch, 0.45*inch, f"PAGE {page_num}")
        
        # Disclaimer on bottom line (smaller, separate from page number)
        canvas.setFont('Courier', 6)
        disclaimer_text = "EXPERIMENTAL: AI-generated analysis may contain errors."
        canvas.drawString(0.6*inch, 0.25*inch, disclaimer_text)
        
        canvas.restoreState()
    
    # Build PDF with custom background and header
    doc.build(story, onFirstPage=draw_header_footer, onLaterPages=draw_header_footer)
    buffer.seek(0)
    return buffer.getvalue()

