import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
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
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, title)
    y -= 30
    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"Total equipment rows: {summary.get('total_count')}")
    y -= 20
    for k,v in summary.get('averages', {}).items():
        c.drawString(40, y, f"Average {k}: {v:.3f}" if v is not None else f"Average {k}: N/A")
        y -= 15
    y -= 10
    c.drawString(40, y, "Type distribution:")
    y -= 15
    for t, cnt in summary.get('type_distribution', {}).items():
        c.drawString(60, y, f"{t}: {cnt}")
        y -= 12
    y -= 20
    c.drawString(40, y, "Sample data (first 10 rows):")
    y -= 15
    cols = list(df.columns)
    header = " | ".join(cols)
    c.drawString(40, y, header)
    y -= 12
    for idx, row in df.head(10).iterrows():
        row_txt = " | ".join(str(row.get(c, "")) for c in cols)
        c.drawString(40, y, row_txt[:120])
        y -= 12
        if y < 40:
            c.showPage()
            y = height - 40
    c.save()
    buffer.seek(0)
    return ContentFile(buffer.read(), name="report.pdf")
