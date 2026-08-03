import io
import re
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

def generate_clinical_pdf(report_text_name: str, language: str, report_text: str) -> bytes:
    """
    Generates a clean, professional, physician-grade PDF report for Health care AI patient guidance.
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
    primary_color = colors.HexColor("#0f1c18")  # Dark Slate Green Header
    accent_green = colors.HexColor("#059669")   # Medical Emerald Green
    text_dark = colors.HexColor("#1e293b")      # Slate Dark Text
    
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
        textColor=accent_green,
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

    # 1. Header Banner Table (Clean Health care AI Branding)
    header_p1 = Paragraph("Health care AI", title_style)
    header_p2 = Paragraph("Universal Multi-Lingual Medical Lab Report Interpreter & Educator", subtitle_style)
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

    # 2. Assessment Summary Table Box
    summary_title = Paragraph("<b>PATIENT LAB GUIDANCE SUMMARY</b>", ParagraphStyle('VTitle', fontName='Helvetica-Bold', fontSize=10, textColor=accent_green))
    
    summary_data = [
        [summary_title, ""],
        ["Report Assessment:", "Multi-Lingual Patient Educational Guidance"],
        ["Source Document:", f"{report_text_name}"],
        ["Guidance Language:", f"<b>{language}</b>"]
    ]

    summary_table = Table([[Paragraph(cell, body_style) if isinstance(cell, str) else cell for cell in row] for row in summary_data], colWidths=[180, 350])
    summary_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (1, 0)),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BORDER', (0, 0), (-1, -1), 1, colors.HexColor("#e2e8f0")),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 15))

    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceBefore=5, spaceAfter=10))

    # 3. Process Report Markdown Content into Clean Paragraphs
    lines = report_text.split('\n')
    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue
        
        # Skip raw separator lines like ===== or ------
        if re.match(r'^[=\-_]{3,}$', line_str):
            continue
            
        if line_str.startswith('### ') or line_str.startswith('## ') or line_str.startswith('# '):
            heading_text = line_str.lstrip('#').strip()
            story.append(Paragraph(heading_text, section_heading_style))
        elif line_str.startswith('- ') or line_str.startswith('* '):
            bullet_text = line_str[2:].strip()
            formatted_bullet = format_markdown_bold(bullet_text)
            story.append(Paragraph(f"• {formatted_bullet}", bullet_style))
        elif re.match(r'^\d+\.\s', line_str):
            parts = line_str.split('. ', 1)
            num_prefix = parts[0]
            item_text = parts[1] if len(parts) > 1 else ""
            formatted_item = format_markdown_bold(item_text)
            story.append(Paragraph(f"<b>{num_prefix}.</b> {formatted_item}", bullet_style))
        else:
            formatted_body = format_markdown_bold(line_str)
            story.append(Paragraph(formatted_body, body_style))

    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceBefore=10, spaceAfter=10))

    # 4. Official Footer Disclaimer
    disclaimer_text = (
        "<b>Medical Disclaimer:</b> This report is generated by Health care AI for patient educational and guidance purposes. "
        "It provides general reference range explanations and does NOT provide medical advice, diagnosis, or treatment. "
        "Please consult a licensed primary care physician regarding your medical lab results and clinical treatment planning."
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
