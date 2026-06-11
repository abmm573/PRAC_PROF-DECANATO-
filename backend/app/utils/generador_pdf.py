import io
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

W, H = A4

# ── Paleta institucional exacta ──────────────────────────────────────────────
AZUL_OSCURO = colors.HexColor("#1e3a5f")
AZUL_TABLA  = colors.HexColor("#2563eb")
GRIS_FONDOS = colors.HexColor("#f8fafc")
GRIS_BORDE  = colors.HexColor("#e2e8f0")
BLANCO      = colors.white

# Colores para el Badge de Estado
VERDE    = colors.HexColor("#16a34a")
ROJO     = colors.HexColor("#dc2626")
AMARILLO = colors.HexColor("#d97706")

MARGIN = 1.5 * cm
W_UTIL = W - 2 * MARGIN

def _estado_color(estado: str):
    e = (estado or "").upper()
    if e == "APROBADO": return VERDE
    if e == "RECHAZADO": return ROJO
    return AMARILLO

def generar_comprobante_pdf(datos_reporte: dict) -> io.BytesIO:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    
    y = H - MARGIN

    # 1. CABECERA INSTITUCIONAL (Azul Marino)
    cab_h = 2.2 * cm
    c.setFillColor(AZUL_OSCURO)
    c.rect(MARGIN, y - cab_h, W_UTIL, cab_h, fill=1, stroke=0)
    
    c.setFillColor(BLANCO)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN + 0.5*cm, y - 0.8*cm, "FACULTAD DE CIENCIAS SOCIALES · UMSA")
    c.setFont("Helvetica", 9)
    c.drawString(MARGIN + 0.5*cm, y - 1.4*cm, "Sistema de Control de Asistencia de Pasantes")
    
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(MARGIN + W_UTIL - 0.5*cm, y - 0.8*cm, "Reporte Diario de Asistencia")
    c.setFont("Helvetica", 8)
    c.drawRightString(MARGIN + W_UTIL - 0.5*cm, y - 1.4*cm, f"Fecha: {datos_reporte.get('fecha', '')}")

    y -= (cab_h + 0.5*cm)

    # 2. INFORMACIÓN DEL PASANTE (Banda Gris)
    info_h = 1.8 * cm
    c.setFillColor(GRIS_FONDOS)
    c.rect(MARGIN, y - info_h, W_UTIL, info_h, fill=1, stroke=1)
    c.setStrokeColor(GRIS_BORDE)
    
    c.setFillColor(AZUL_OSCURO)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGIN + 0.5*cm, y - 0.6*cm, f"Pasante: {datos_reporte.get('pasante_nombre', 'N/A')}")
    
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 9)
    c.drawString(MARGIN + 0.5*cm, y - 1.2*cm, f"Carrera: {datos_reporte.get('carrera_nombre', 'N/A')}")
    
    y -= (info_h + 0.8*cm)

    # 3. TABLA DE TIEMPOS (Cabecera Azul Vibrante)
    header_h = 0.8 * cm
    fila_h = 0.8 * cm
    c.setFillColor(AZUL_TABLA)
    c.rect(MARGIN, y - header_h, W_UTIL, header_h, fill=1, stroke=0)
    
    c.setFillColor(BLANCO)
    c.setFont("Helvetica-Bold", 9)
    col_ws = [W_UTIL * 0.25, W_UTIL * 0.25, W_UTIL * 0.20, W_UTIL * 0.30]
    
    headers = ["Hora Entrada", "Hora Salida", "Total Horas", "Estado Resolución"]
    curr_x = MARGIN
    for i, txt in enumerate(headers):
        c.drawString(curr_x + 0.3*cm, y - 0.5*cm, txt)
        curr_x += col_ws[i]
    
    y -= header_h
    
    # Fila de datos
    c.setFillColor(BLANCO)
    c.rect(MARGIN, y - fila_h, W_UTIL, fila_h, fill=1, stroke=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 9)
    
    c.drawString(MARGIN + 0.3*cm, y - 0.5*cm, str(datos_reporte.get('hora_entrada', '—')))
    c.drawString(MARGIN + col_ws[0] + 0.3*cm, y - 0.5*cm, str(datos_reporte.get('hora_salida', '—')))
    c.drawString(MARGIN + sum(col_ws[:2]) + 0.3*cm, y - 0.5*cm, f"{datos_reporte.get('horas_trabajadas', 0)} hrs")
    
    # Badge de estado en la tabla
    estado = (datos_reporte.get('estado') or 'APROBADO').upper()
    badge_w, badge_h = 2.4*cm, 0.5*cm
    bx = MARGIN + sum(col_ws[:3]) + (col_ws[3] - badge_w)/2
    by = y - 0.65*cm
    c.setFillColor(_estado_color(estado))
    c.roundRect(bx, by, badge_w, badge_h, 4, fill=1, stroke=0)
    c.setFillColor(BLANCO)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(bx + badge_w/2, by + 0.15*cm, estado)

    y -= (fila_h + 1.2*cm)

    # 4. ACTIVIDADES REALIZADAS
    c.setFillColor(AZUL_OSCURO)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGIN, y, "Actividades Realizadas:")
    
    y -= 0.6 * cm
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    
    # Ajuste de texto largo
    text_obj = c.beginText(MARGIN, y)
    text_obj.setLeading(14)
    actividades = datos_reporte.get('actividades', 'No se registraron actividades.')
    
    # Dividir texto en líneas para que no se salga de la hoja
    words = actividades.split()
    line = ""
    for word in words:
        if c.stringWidth(line + " " + word) < W_UTIL:
            line += " " + word
        else:
            text_obj.textLine(line.strip())
            line = word
    text_obj.textLine(line.strip())
    c.drawText(text_obj)

    # 5. FIRMAS (Pie de página profesional)
    f_y = 4 * cm
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.5)
    fw = 4.8 * cm
    
    # Líneas
    c.line(MARGIN + 0.5*cm, f_y, MARGIN + 0.5*cm + fw, f_y)
    c.line(MARGIN + W_UTIL - fw - 0.5*cm, f_y, MARGIN + W_UTIL - 0.5*cm, f_y)
    
    f_y2 = f_y - 2.2*cm
    c.line(MARGIN + 0.5*cm, f_y2, MARGIN + 0.5*cm + fw, f_y2)
    c.line(MARGIN + W_UTIL - fw - 0.5*cm, f_y2, MARGIN + W_UTIL - 0.5*cm, f_y2)

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(MARGIN + 0.5*cm + fw/2, f_y - 0.4*cm, "Pasante")
    c.drawCentredString(MARGIN + W_UTIL - fw/2 - 0.5*cm, f_y - 0.4*cm, "Tutor Institucional")
    c.drawCentredString(MARGIN + 0.5*cm + fw/2, f_y2 - 0.4*cm, "Coordinador")
    c.drawCentredString(MARGIN + W_UTIL - fw/2 - 0.5*cm, f_y2 - 0.4*cm, "Docente de la UMSA")

    c.save()
    buf.seek(0)
    return buf