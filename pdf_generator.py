import io
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

def generate_clinical_pdf(chol: float, thalach: float, diag_prediction: str, report_text: str) -> bytes:
    """
    Generates a professional, physician-grade PDF report for the patient clinical assessment.
    Returns the PDF file bytes in memory.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette & Styles
    primary_color = colors.HexColor("#1e1035")  # Deep Purple Header
    accent_green = colors.HexColor("#059669")   # Medical Emerald Green
    accent_red = colors.HexColor("#dc2626")     # Alert Red
    text_dark = colors.HexColor("#1e293b")      # Slate Dark Text
    
    is_high_risk = "HIGH" in str(diag_prediction).upper()
    risk_color = accent_red if is_high_risk else accent_green
    risk_badge_text = "HIGH RISK ASSESSMENT" if is_high_risk else "LOW RISK ASSESSMENT"

    # Title & Subtitle Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=colors.white,
        alignment=TA_LEFT,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor("#cbd5e1"),
        alignment=TA_LEFT
    )

    section_heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        textColor=text_dark,
        leading=14,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'ReportBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        textColor=text_dark,
        leading=14,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    story = []

    # 1. Header Banner Table
    header_p1 = Paragraph("❤️ CardioCare AI", title_style)
    header_p2 = Paragraph("Clinical Decision Support System | Human-Centered Health Intelligence", subtitle_style)
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    date_p = Paragraph(f"<font color='#cbd5e1' size=8>Date: {now_str}</font>", ParagraphStyle('DateRight', alignment=TA_RIGHT))

    header_table_data = [
        [[header_p1, header_p2], date_p]
    ]

    header_table = Table(header_table_data, colWidths=[380, 150])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), primary_color),
        ('PADDING', (0, 0), (-1, -1), 14),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 15))

    # 2. Patient Clinical Vitals Table Box
    vitals_title = Paragraph("<b>PATIENT CLINICAL METRICS SUMMARY</b>", ParagraphStyle('VTitle', fontName='Helvetica-Bold', fontSize=10, textColor=primary_color))
    
    vitals_data = [
        [vitals_title, ""],
        ["Total Cholesterol Level:", f"{int(chol)} mg/dL"],
        ["Max Heart Rate (Exercise):", f"{int(thalach)} bpm"],
        ["Diagnostic Risk Level:", f"<font color='{risk_color.hexval()}'><b>{diag_prediction}</b> ({risk_badge_text})</font>"]
    ]

    vitals_table = Table([[Paragraph(cell, body_style) if isinstance(cell, str) else cell for cell in row] for row in vitals_data], colWidths=[200, 330])
    vitals_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (1, 0)),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BORDER', (0, 0), (-1, -1), 1, colors.HexColor("#e2e8f0")),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(vitals_table)
    story.append(Spacer(1, 15))

    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceBefore=5, spaceAfter=10))

    # 3. Process Report Markdown Content into Paragraphs
    lines = report_text.split('\n')
    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue
        
        if line_str.startswith('### ') or line_str.startswith('## '):
            heading_text = line_str.lstrip('#').strip()
            # Clean emojis if any
            story.append(Paragraph(heading_text, section_heading_style))
        elif line_str.startswith('- ') or line_str.startswith('* '):
            bullet_text = line_str[2:].strip()
            # Replace markdown bold ** text ** with HTML <b> text </b>
            formatted_bullet = format_markdown_bold(bullet_text)
            story.append(Paragraph(f"• {formatted_bullet}", bullet_style))
        elif line_str.startswith('1. ') or line_str.startswith('2. ') or line_str.startswith('3. ') or line_str.startswith('4. '):
            item_text = line_str[3:].strip()
            formatted_item = format_markdown_bold(item_text)
            story.append(Paragraph(f"{line_str[:3]} {formatted_item}", bullet_style))
        else:
            formatted_body = format_markdown_bold(line_str)
            story.append(Paragraph(formatted_body, body_style))

    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceBefore=10, spaceAfter=10))

    # 4. Official Footer Disclaimer
    disclaimer_text = (
        "<b>Medical Disclaimer:</b> This report is generated by CardioCare AI Clinical Decision Support System for informational and clinical guidance purposes. "
        "It is designed to assist, not replace, the relationship that exists between a patient and their physician. "
        "Please consult a certified cardiologist or primary care physician for medical diagnosis and treatment planning."
    )
    story.append(Paragraph(disclaimer_text, ParagraphStyle('Disclaimer', fontName='Helvetica-Oblique', fontSize=7.5, textColor=colors.HexColor("#64748b"), leading=10)))

    # Build Document
    doc.build(story)
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data

def format_markdown_bold(text: str) -> str:
    """Converts markdown **bold** syntax to ReportLab <b>bold</b> HTML tags."""
    parts = text.split('**')
    if len(parts) == 1:
        return text
    
    result = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            result.append(f"<b>{part}</b>")
        else:
            result.append(part)
    return "".join(result)
