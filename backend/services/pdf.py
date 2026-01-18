from weasyprint import HTML

def html_to_pdf(html: str, out: str):
    HTML(string=html).write_pdf(out)
