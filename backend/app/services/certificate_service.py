from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from datetime import datetime
import io
from pathlib import Path

class CertificateGenerator:
    @staticmethod
    def generate_certificate(student_name: str, course_name: str, certificate_number: str, instructor_name: str) -> bytes:
        """Generate PDF certificate"""
        # Create a BytesIO object to store the PDF in memory
        pdf_buffer = io.BytesIO()
        
        # Create PDF
        doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, rightMargin=0.5*inch, leftMargin=0.5*inch)
        
        # Container for PDF elements
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=48,
            textColor=colors.HexColor('#1a5490'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=16,
            textColor=colors.HexColor('#333333'),
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#555555'),
            spaceAfter=15,
            alignment=TA_CENTER
        )
        
        # Add certificate title
        elements.append(Paragraph("CERTIFICATE OF COMPLETION", title_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Add decorative line
        elements.append(Paragraph("_" * 50, subtitle_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Certificate body
        elements.append(Paragraph("This is to certify that", body_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Student name
        name_style = ParagraphStyle(
            'StudentName',
            parent=styles['Normal'],
            fontSize=24,
            textColor=colors.HexColor('#1a5490'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        elements.append(Paragraph(student_name, name_style))
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Course completion text
        completion_text = f"has successfully completed the course<br/><b>{course_name}</b>"
        elements.append(Paragraph(completion_text, body_style))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Certificate details
        date_str = datetime.now().strftime("%B %d, %Y")
        details_text = f"Certificate Number: {certificate_number}<br/>Date: {date_str}"
        elements.append(Paragraph(details_text, body_style))
        
        elements.append(Spacer(1, 0.5*inch))
        
        # Signature section
        signature_style = ParagraphStyle(
            'Signature',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#555555'),
            alignment=TA_CENTER
        )
        
        elements.append(Paragraph("_" * 30, body_style))
        elements.append(Paragraph(f"{instructor_name}", signature_style))
        elements.append(Paragraph("Instructor", signature_style))
        
        # Build PDF
        doc.build(elements)
        
        # Get PDF bytes
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()
