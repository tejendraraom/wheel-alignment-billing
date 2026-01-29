from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

env = Environment(
    loader=FileSystemLoader(os.path.join(BASE_DIR, "templates"))
)

def generate_invoice_pdf(bill):
    template = env.get_template("invoice.html")
    html_content = template.render(bill=bill)
    return HTML(string=html_content).write_pdf()
