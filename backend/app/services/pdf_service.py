import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

def generate_pdf_report(patient_data: dict, prediction_data: dict, doctor_name: str) -> BytesIO:
    """
    Generates a highly styled, professional PDF report for a patient's heart disease prediction.
    Saves it to the reports/ directory and returns the PDF bytes in a BytesIO buffer.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    
    # Custom Styles for Premium medical report look
    primary_color = colors.HexColor("#0d9488")    # Clinical Teal
    secondary_color = colors.HexColor("#0f172a")  # Slate-900
    text_color = colors.HexColor("#334155")       # Slate-700
    
    # Custom style definitions
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=primary_color,
        spaceAfter=15
    )
    
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=secondary_color,
        spaceBefore=12,
        spaceAfter=6,
        borderColor=primary_color,
        borderWidth=1
    )
    
    body_text = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        textColor=text_color,
        leading=14
    )

    bold_text = ParagraphStyle(
        'BoldTextCustom',
        parent=body_text,
        fontName='Helvetica-Bold'
    )
    
    recommendation_style = ParagraphStyle(
        'RecText',
        parent=body_text,
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#1e293b")
    )

    story = []

    # 1. Header Table (Branding)
    header_data = [
        [
            Paragraph("<b>HEARTCARE AI</b><br/><font size=8 color='#64748b'>Heart Disease Prediction System</font>", ParagraphStyle('HeaderL', parent=body_text, fontSize=16, leading=18, textColor=primary_color)),
            Paragraph("<b>CLINICAL DIAGNOSTIC REPORT</b><br/><font size=9 color='#64748b'>Date: " + prediction_data['date'][:10] + "</font>", ParagraphStyle('HeaderR', parent=body_text, alignment=2, leading=14))
        ]
    ]
    header_table = Table(header_data, colWidths=[3 * inch, 4.2 * inch])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LINEBELOW', (0,0), (-1,-1), 1.5, primary_color)
    ]))
    story.append(header_table)
    story.append(Spacer(1, 15))

    # 2. Patient Information Section
    story.append(Paragraph("Patient Information", section_heading))
    patient_info = [
        [
            Paragraph("<b>Patient ID:</b>", body_text), Paragraph(str(patient_data['patient_id']), body_text),
            Paragraph("<b>Name:</b>", body_text), Paragraph(str(patient_data['name']), body_text)
        ],
        [
            Paragraph("<b>Age / Gender:</b>", body_text), Paragraph(f"{patient_data['age']} yrs / {patient_data['gender']}", body_text),
            Paragraph("<b>Contact:</b>", body_text), Paragraph(str(patient_data['phone'] or 'N/A'), body_text)
        ],
        [
            Paragraph("<b>Height:</b>", body_text), Paragraph(f"{patient_data['height']} cm" if patient_data['height'] else "N/A", body_text),
            Paragraph("<b>Weight:</b>", body_text), Paragraph(f"{patient_data['weight']} kg" if patient_data['weight'] else "N/A", body_text)
        ],
        [
            Paragraph("<b>Assigned Physician:</b>", body_text), Paragraph(str(doctor_name), body_text),
            Paragraph("<b>Email:</b>", body_text), Paragraph(str(patient_data['email'] or 'N/A'), body_text)
        ]
    ]
    
    patient_table = Table(patient_info, colWidths=[1.5 * inch, 2.1 * inch, 1.5 * inch, 2.1 * inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(patient_table)
    story.append(Spacer(1, 15))

    # 3. Clinical Parameters Section
    story.append(Paragraph("Clinical Health Parameters", section_heading))
    
    # Map CP
    cp_map = {1: "Typical Angina", 2: "Atypical Angina", 3: "Non-anginal Pain", 4: "Asymptomatic"}
    thal_map = {3: "Normal", 6: "Fixed Defect", 7: "Reversible Defect"}
    slope_map = {1: "Upsloping", 2: "Flat", 3: "Downsloping"}
    ecg_map = {0: "Normal", 1: "ST-T Wave Abnormality", 2: "LV Hypertrophy"}
    
    clinical_info = [
        [
            Paragraph("<b>Resting Blood Pressure:</b>", body_text), Paragraph(f"{prediction_data['trestbps']} mmHg", body_text),
            Paragraph("<b>Serum Cholesterol:</b>", body_text), Paragraph(f"{prediction_data['chol']} mg/dL", body_text)
        ],
        [
            Paragraph("<b>Chest Pain Type:</b>", body_text), Paragraph(cp_map.get(prediction_data['cp'], "Unknown"), body_text),
            Paragraph("<b>Fasting Blood Sugar:</b>", body_text), Paragraph("Yes (>120 mg/dL)" if prediction_data['fbs'] == 1 else "No", body_text)
        ],
        [
            Paragraph("<b>Resting ECG:</b>", body_text), Paragraph(ecg_map.get(prediction_data['restecg'], "Normal"), body_text),
            Paragraph("<b>Max Heart Rate Achieved:</b>", body_text), Paragraph(f"{prediction_data['thalach']} bpm", body_text)
        ],
        [
            Paragraph("<b>Exercise Induced Angina:</b>", body_text), Paragraph("Yes" if prediction_data['exang'] == 1 else "No", body_text),
            Paragraph("<b>ST Depression (Oldpeak):</b>", body_text), Paragraph(f"{prediction_data['oldpeak']}", body_text)
        ],
        [
            Paragraph("<b>Slope of ST Segment:</b>", body_text), Paragraph(slope_map.get(prediction_data['slope'], "Flat"), body_text),
            Paragraph("<b>Vessels Colored (CA):</b>", body_text), Paragraph(str(prediction_data['ca']), body_text)
        ],
        [
            Paragraph("<b>Thalassemia:</b>", body_text), Paragraph(thal_map.get(prediction_data['thal'], "Normal"), body_text),
            Paragraph("", body_text), Paragraph("", body_text)
        ]
    ]
    clinical_table = Table(clinical_info, colWidths=[1.8 * inch, 1.8 * inch, 1.8 * inch, 1.8 * inch])
    clinical_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(clinical_table)
    story.append(Spacer(1, 15))

    # 4. AI Prediction Section
    story.append(Paragraph("AI Cardiovascular Risk Assessment", section_heading))
    
    # Determine color for risk
    risk_status = prediction_data['prediction_status']
    if risk_status == "HIGH RISK":
        risk_color = colors.HexColor("#ef4444")  # Red
        bg_color = colors.HexColor("#fef2f2")
    elif risk_status == "MEDIUM RISK":
        risk_color = colors.HexColor("#f59e0b")  # Amber
        bg_color = colors.HexColor("#fffbeb")
    else:
        risk_color = colors.HexColor("#10b981")  # Emerald Green
        bg_color = colors.HexColor("#f0fdf4")
        
    prediction_info = [
        [
            Paragraph("<b>Heart Disease Risk Status:</b>", body_text),
            Paragraph(f"<font color='{risk_color.hexval()}'><b>{risk_status}</b></font>", ParagraphStyle('RiskText', parent=bold_text, fontSize=12)),
            Paragraph("<b>Model Confidence:</b>", body_text),
            Paragraph(f"{prediction_data['prediction_confidence']}%", bold_text)
        ],
        [
            Paragraph("<b>Risk Probability Index:</b>", body_text),
            Paragraph(f"<b>{prediction_data['risk_percentage']}%</b>", ParagraphStyle('ProbText', parent=bold_text, fontSize=12, textColor=primary_color)),
            Paragraph("<b>Model Selected:</b>", body_text),
            Paragraph("Random Forest Classifier (Balanced)", body_text)
        ]
    ]
    prediction_table = Table(prediction_info, colWidths=[1.8 * inch, 1.8 * inch, 1.8 * inch, 1.8 * inch])
    prediction_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_color),
        ('GRID', (0,0), (-1,-1), 1, risk_color),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(prediction_table)
    story.append(Spacer(1, 15))

    # 5. Doctor Recommendations Section
    story.append(Paragraph("Clinical Recommendations & Lifestyle Interventions", section_heading))
    
    rec_text = prediction_data.get('doctor_recommendation') or prediction_data.get('recommendation') or "No specific recommendations provided."
    # Format line breaks in recommendation text for PDF flow
    rec_paragraphs = [Paragraph(p.strip(), recommendation_style) for p in rec_text.split('\n') if p.strip()]
    
    rec_cell = []
    for p in rec_paragraphs:
        rec_cell.append(p)
        rec_cell.append(Spacer(1, 3))
        
    rec_table_data = [[rec_cell]]
    rec_table = Table(rec_table_data, colWidths=[7.2 * inch])
    rec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#f8fafc")),
        ('BORDER', (0,0), (0,0), 1, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (0,0), 10),
        ('VALIGN', (0,0), (0,0), 'TOP')
    ]))
    story.append(rec_table)
    story.append(Spacer(1, 40))

    # 6. Signature Block
    sig_data = [
        [
            Paragraph("<b>Physician Signature:</b> ___________________________", body_text),
            Paragraph("<b>HeartCare AI Clinical Verification</b>", ParagraphStyle('SigR', parent=body_text, alignment=2))
        ]
    ]
    sig_table = Table(sig_data, colWidths=[4 * inch, 3.2 * inch])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM')
    ]))
    story.append(sig_table)

    # Build PDF
    doc.build(story)
    
    # Save a copy to the reports/ directory
    os.makedirs("reports", exist_ok=True)
    report_filename = f"reports/report_{patient_data['patient_id']}_{prediction_data.get('id', 'new')}.pdf"
    try:
        with open(report_filename, "wb") as f:
            f.write(buffer.getvalue())
        print(f"Report PDF archived at {report_filename}")
    except Exception as e:
        print(f"Failed to archive PDF report: {e}")

    buffer.seek(0)
    return buffer
