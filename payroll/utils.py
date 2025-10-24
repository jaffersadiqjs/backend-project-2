from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from django.http import HttpResponse
from openpyxl import Workbook

def generate_salary_slip_pdf(payroll):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elems = []

    elems.append(Paragraph("Company XYZ Pvt Ltd", styles['Title']))
    elems.append(Paragraph(f"Salary Slip - {payroll.month}/{payroll.year}", styles['Heading2']))
    elems.append(Spacer(1, 12))
    elems.append(Paragraph(f"Employee: {payroll.employee.name} ({payroll.employee.emp_id})", styles['Normal']))
    elems.append(Paragraph(f"Department: {payroll.employee.department} - Designation: {payroll.employee.designation}", styles['Normal']))
    elems.append(Spacer(1, 12))

    data = [
        ['Total Days', payroll.total_days],
        ['Present Days', payroll.present_days],
        ['Daily Salary (INR)', f"{payroll.employee.salary_per_day:.2f}"],
        ['Net Salary (INR)', f"{payroll.net_salary:.2f}"],
    ]
    table = Table(data, colWidths=[200, 200])
    table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    ]))
    elems.append(table)
    elems.append(Spacer(1, 24))
    elems.append(Paragraph("This is a computer generated slip.", styles['Normal']))

    doc.build(elems)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=salary_slip_{payroll.employee.emp_id}_{payroll.month}_{payroll.year}.pdf'
    return response

def export_payrolls_to_excel(payroll_qs):
    wb = Workbook()
    ws = wb.active
    ws.title = "Payroll"
    headers = ['Emp ID', 'Name', 'Month', 'Year', 'Present Days', 'Net Salary']
    ws.append(headers)
    for p in payroll_qs:
        ws.append([p.employee.emp_id, p.employee.name, p.month, p.year, p.present_days, float(p.net_salary)])
    stream = BytesIO()
    wb.save(stream)
    stream.seek(0)
    response = HttpResponse(stream.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=payroll_report.xlsx'
    return response
