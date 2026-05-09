import os
from datetime import datetime
from flask import Flask, render_template, Response

# Create Flask application using the project root as the template folder
app = Flask(__name__, template_folder=".")
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

@app.route('/')
def index():
    return render_template('index.html')

def _pdf_escape(text: str) -> str:
    return text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')

def _build_cv_pdf_bytes() -> bytes:
    lines = [
        "Ankita Gupta",
        "AI & Data Scientist",
        "",
        "Email: guptaankita0143@gmail.com",
        "Phone: 8218282173",
        "",
        "Professional Summary",
        "Experienced Data Scientist & AI Consultant with 4 years of experience building AI/ML solutions in NLP, Computer Vision, and Generative AI.",
        "Strong expertise in GenAI, RAG architectures, prompt engineering, and Azure AI deployments.",
        "",
        "Skills",
        "Python, Flask, FastAPI, Machine Learning, LLMs, RAG, Azure, Data Engineering, Computer Vision, NLP.",
        "",
        "Experience",
        "Data Scientist at MaxRidge.AI Tech Pvt. Ltd.",
        "Developed LLM-powered systems, RAG pipelines, and AI-driven analytics solutions.",
    ]

    content_lines = [
        "BT",
        "/F1 14 Tf",
        "50 780 Td",
    ]

    for index, line in enumerate(lines):
        escaped = _pdf_escape(line)
        content_lines.append(f"({escaped}) Tj")
        if index < len(lines) - 1:
            content_lines.append("0 -20 Td")
    content_lines.append("ET")
    content = "\n".join(content_lines).encode("latin-1")

    objects = [
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n",
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n",
        b"4 0 obj\n<< /Length %d >>\nstream\n" % len(content) + content + b"\nendstream\nendobj\n",
        b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n",
    ]

    pdf = b"%PDF-1.4\n"
    offsets = []
    for obj in objects:
        offsets.append(len(pdf))
        pdf += obj

    xref_start = len(pdf)
    pdf += f"xref\n0 {len(objects) + 1}\n".encode("ascii")
    pdf += b"0000000000 65535 f \n"
    for offset in offsets:
        pdf += f"{offset:010d} 00000 n \n".encode("ascii")
    pdf += f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF".encode("ascii")

    return pdf

@app.route('/download-cv')
def download_cv():
    pdf_data = _build_cv_pdf_bytes()
    date_stamp = datetime.now().strftime('%d_%B_%Y')
    filename = f"Ankita_Gupta_CV_{date_stamp}.pdf"
    return Response(
        pdf_data,
        mimetype='application/pdf',
        headers={
            'Content-Disposition': f'attachment; filename="{filename}"'
        }
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
