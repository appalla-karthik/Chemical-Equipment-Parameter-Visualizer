import pandas as pd
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from django.core.files.base import ContentFile

NUMERIC_COLS = ['Flowrate','Pressure','Temperature']

def parse_csv_and_summary(file_path):
    df = pd.read_csv(file_path)
    df.columns = [c.strip() for c in df.columns]
    total_count = len(df)
    averages = {}
    for col in NUMERIC_COLS:
        if col in df.columns:
            averages[col] = float(df[col].dropna().mean())
        else:
            averages[col] = None
    type_dist = {}
    if 'Type' in df.columns:
        type_dist = df['Type'].value_counts().to_dict()
    summary = {
        'total_count': total_count,
        'averages': averages,
        'type_distribution': type_dist,
        'columns': list(df.columns),
    }
    return summary, df

def generate_pdf_report(summary, df, title="Equipment Report"):
    """Generate a professionally formatted PDF report"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2d5aa8'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    story = []
    
    # Title
    story.append(Paragraph(title, title_style))
    story.append(Paragraph(f"<font size=10 color='#666666'>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</font>", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Summary Statistics Section
    story.append(Paragraph("📊 Summary Statistics", heading_style))
    
    summary_data = [
        ['Metric', 'Value'],
        ['Total Equipment Records', str(summary.get('total_count', 0))],
    ]
    
    for k, v in summary.get('averages', {}).items():
        value_str = f"{v:.3f}" if v is not None else "N/A"
        summary_data.append([f'Average {k}', value_str])
    
    summary_table = Table(summary_data, colWidths=[3*inch, 2.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d5aa8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Type Distribution Section
    if summary.get('type_distribution'):
        story.append(Paragraph("🏷️  Equipment Type Distribution", heading_style))
        
        type_data = [['Type', 'Count', 'Percentage']]
        total = sum(summary.get('type_distribution', {}).values())
        for t, cnt in sorted(summary.get('type_distribution', {}).items()):
            percentage = (cnt / total * 100) if total > 0 else 0
            type_data.append([str(t), str(cnt), f'{percentage:.1f}%'])
        
        type_table = Table(type_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        type_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
        ]))
        story.append(type_table)
        story.append(Spacer(1, 0.3*inch))
    
    # Sample Data Section
    story.append(Paragraph("📋 Sample Data (First 10 Records)", heading_style))
    
    cols = list(df.columns)
    # Limit columns to first 6 for readability
    display_cols = cols[:6]
    sample_data = [display_cols]
    
    for idx, row in df.head(10).iterrows():
        row_values = [str(row.get(c, ""))[:30] for c in display_cols]
        sample_data.append(row_values)
    
    col_widths = [letter[0] / len(display_cols) - 0.1*inch for _ in display_cols]
    sample_table = Table(sample_data, colWidths=col_widths)
    sample_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d5aa8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
    ]))
    story.append(sample_table)
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return ContentFile(buffer.read(), name="report.pdf")
