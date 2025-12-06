from reportlab.pdfgen import canvas

def export_pdf(users, path="data/report.pdf"):
    c=canvas.Canvas(path)
    y=800
    c.drawString(50,y,"Users Report")
    y-=40
    for u in users:
        c.drawString(50,y,f"{u}")
        y-=20
    c.save()
