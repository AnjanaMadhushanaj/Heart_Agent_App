import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

os.makedirs("sample_lab_reports", exist_ok=True)

styles = getSampleStyleSheet()
title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=16, textColor=colors.HexColor("#0f172a"))
body_style = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=10, textColor=colors.HexColor("#334155"), leading=14)

def build_lab_pdf(filename: str, patient_name: str, chol: int, thalach: int, risk_label: str):
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    # Header
    story.append(Paragraph("<b>CENTRAL DIAGNOSTIC LABORATORY</b>", title_style))
    story.append(Paragraph("Cardiovascular & Lipid Panel Diagnostic Assessment Report", body_style))
    story.append(Spacer(1, 15))
    
    # Patient Info Table
    info_data = [
        ["Patient Name:", patient_name, "Date:", "2026-08-01"],
        ["Age / Gender:", "54 / Male", "Ref. Doctor:", "Dr. S. Perera (Cardiologist)"]
    ]
    info_table = Table(info_data, colWidths=[100, 160, 80, 160])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 15))
    
    # Test Results Table
    story.append(Paragraph("<b>LABORATORY TEST RESULTS SUMMARY</b>", ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor("#1e293b"))))
    story.append(Spacer(1, 8))
    
    results_data = [
        ["Test Parameter", "Measured Value", "Reference Range", "Flag Status"],
        ["Total Cholesterol", f"{chol} mg/dL", "< 200.0 mg/dL", "HIGH" if chol > 200 else "NORMAL"],
        ["Maximum Heart Rate (Exercise)", f"{thalach} bpm", "60.0 - 200.0 bpm", risk_label],
    ]
    
    res_table = Table(results_data, colWidths=[180, 110, 110, 100])
    res_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
    ]))
    story.append(res_table)
    story.append(Spacer(1, 20))
    
    # Doctor Note
    story.append(Paragraph(f"<b>Pathology Note:</b> Patient exhibits Total Cholesterol of {chol} mg/dL and Maximum Heart Rate of {thalach} bpm during cardiac stress testing.", body_style))
    
    doc.build(story)

# Generate 3 sample PDFs
build_lab_pdf("sample_lab_reports/high_risk_cholesterol_report.pdf", "Kamal Jayasinghe", 265, 130, "HIGH RISK")
build_lab_pdf("sample_lab_reports/normal_vitals_report.pdf", "Nimal Fernando", 175, 165, "NORMAL")
build_lab_pdf("sample_lab_reports/borderline_risk_report.pdf", "Saman Silva", 242, 145, "ELEVATED")

print("Generated 3 sample lab report PDFs inside sample_lab_reports/ folder!")
