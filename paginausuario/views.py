from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test


from .models import (
    DatosPersonales,
    ExperienciaLaboral,
    Reconocimiento,
    CursoRealizado,
    ProductoAcademico,
    ProductoLaboral,
    VentaGarage)

from .models import ConfigSeccionesCV

def get_cv_config():
    cfg, _ = ConfigSeccionesCV.objects.get_or_create(id=1)
    return cfg


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "GET":
        return render(request, "paginaregistro.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                return HttpResponse("User created successfully")
            except:
                return render(
                    request,
                    "paginaregistro.html",
                    {"form": UserCreationForm, "error": "Username already exists"},
                )
        return render(
            request,
            "paginaregistro.html",
            {"form": UserCreationForm, "error": "Password do not match"},
        )

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirección según rol
            if user.is_staff:
                return redirect("admin_dashboard")
            else:
                return redirect("user_dashboard")
        else:
            return render(request, "login.html", {
                "error": "Usuario o contraseña incorrectos"
            })

    return render(request, "login.html")

from django.contrib.auth.decorators import login_required


def user_dashboard(request):
    cfg = get_cv_config()
    return render(request, "usuario/dashboard.html", {"cfg": cfg})



from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_dashboard(request):
    return render(request, "admin/dashboard.html")

from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_dashboard(request):
    context = {
        "total_usuarios": User.objects.count(),
        "usuarios_activos": User.objects.filter(is_active=True).count(),
        "total_hojas": 0,
        "total_pdf": 0,
    }
    return render(request, "admin/dashboard.html", context)

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect("login")

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False  # usuario normal
            user.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "signup.html", {"form": form})

## DATOS PERSONALES

from django.shortcuts import render, redirect
from .models import DatosPersonales
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .forms import DatosPersonalesForm

def lista_personas(request):
    persona = DatosPersonales.objects.filter(perfilactivo=1).first()
    return render(request, "datospersonales.html", {
        "vista": "detalle",
        "persona": persona
    })

def detalle_persona(request, pk):
    persona = get_object_or_404(DatosPersonales, pk=pk)
    return render(request, "datospersonales.html", {
        "vista": "detalle",
        "persona": persona
    })

@staff_member_required
def formulario_persona(request, pk):
    persona = get_object_or_404(DatosPersonales, pk=pk)

    if request.method == "POST":
        form = DatosPersonalesForm(request.POST, request.FILES, instance=persona)
        if form.is_valid():
            datos = form.save(commit=False)
            datos.user = request.user
            datos.save()
            return redirect("detalle_persona", pk=persona.pk)
    else:
        form = DatosPersonalesForm(instance=persona)

    return render(request, "datospersonales.html", {
        "vista": "formulario",
        "form": form,
        "persona": persona,
    })
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render

@staff_member_required
def crear_persona(request):
    if request.method == "POST":
        form = FormularioDatos(request.POST, request.FILES)
        if form.is_valid():
            datos = form.save(commit=False)
            datos.user = request.user
            datos.save()
            return redirect("detalle_persona", pk=datos.pk)
    else:
        form = FormularioDatos()

    return render(request, "datospersonales.html", {
        "vista": "formulario",
        "form": form
    })


from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

import os
import os
from reportlab.platypus import Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

import os
from reportlab.platypus import Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.platypus import Image
import os

from reportlab.platypus import Image
import os
from django.conf import settings

import os
import hashlib
from django.conf import settings
from reportlab.platypus import Image as RLImage

from pdf2image import convert_from_path  # pip install pdf2image
from PIL import Image as PILImage  # pip install pillow


def _ruta_archivo(campo):
    """Resuelve path absoluto del FileField o string guardado en BD."""
    if not campo:
        return None
    if hasattr(campo, "path"):
        return campo.path
    return os.path.join(settings.MEDIA_ROOT, str(campo))


def pdf_a_preview_png(ruta_pdf, dpi=130):
    """
    Convierte la PRIMERA página del PDF a PNG y guarda en media/previews/
    Devuelve la ruta del PNG generado.
    (Usa cache: si ya existe, no vuelve a convertir)
    """
    os.makedirs(os.path.join(settings.MEDIA_ROOT, "previews"), exist_ok=True)

    # nombre estable por hash (cache)
    key = hashlib.md5(ruta_pdf.encode("utf-8")).hexdigest()
    out_png = os.path.join(settings.MEDIA_ROOT, "previews", f"{key}.png")

    if os.path.exists(out_png):
        return out_png

    poppler_path = getattr(settings, "POPPLER_PATH", None)  # en Linux puede ser None

    pages = convert_from_path(
        ruta_pdf,
        dpi=dpi,
        first_page=1,
        last_page=1,
        poppler_path=poppler_path
    )

    # pages[0] es un PIL Image
    img: PILImage = pages[0].convert("RGB")
    img.save(out_png, "PNG", optimize=True)

    return out_png


def cargar_imagen_o_preview(campo, ancho=160, alto=160):
    """
    - Si es imagen -> la inserta
    - Si es PDF -> genera preview PNG de la 1ra página y lo inserta
    """
    ruta = _ruta_archivo(campo)
    if not ruta or not os.path.exists(ruta):
        return None

    ext = os.path.splitext(ruta)[1].lower()

    # Si es PDF -> convertir a PNG
    if ext == ".pdf":
        try:
            ruta = pdf_a_preview_png(ruta, dpi=130)
        except Exception as e:
            print("Error convirtiendo PDF a imagen:", e)
            return None

    # Si no es imagen soportada, no intentar
    if os.path.splitext(ruta)[1].lower() not in [".png", ".jpg", ".jpeg", ".webp"]:
        return None

    img = RLImage(ruta)
    img.drawWidth = ancho
    img.drawHeight = alto
    return img


import io
import requests
from datetime import datetime

from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def cargar_imagen_o_preview(file_field, ancho=92, alto=92):
    """
    Devuelve un Flowable Image para imágenes (funciona con Cloudinary),
    y None para PDFs u otros tipos (para no romper ReportLab).
    """
    if not file_field:
        return None

    # Si el campo no tiene archivo asociado
    try:
        url = file_field.url
    except Exception:
        return None

    if not url:
        return None

    url_lower = url.lower()

    # Si es PDF, NO intentamos renderizar como imagen
    if url_lower.endswith(".pdf"):
        return None

    # Descargar imagen desde URL (Cloudinary u otro storage)
    try:
        r = requests.get(url, timeout=12)
        r.raise_for_status()
        img_bytes = io.BytesIO(r.content)
        img = Image(img_bytes, width=ancho, height=alto)
        img.hAlign = "RIGHT"
        return img
    except Exception:
        return None


def certificado_cell(file_field, styles, ancho=150, alto=105):
    """
    - Si es PDF: devuelve un link clickeable
    - Si es imagen: devuelve preview (Image)
    - Si no existe o falla: '—'
    """
    if not file_field:
        return "—"

    try:
        url = file_field.url
    except Exception:
        return "—"

    if not url:
        return "—"

    if url.lower().endswith(".pdf"):
        # Link clickeable dentro del PDF
        return Paragraph(f'<link href="{url}">Ver certificado (PDF)</link>', styles["SmallPro"])

    # Intentar como imagen
    img = cargar_imagen_o_preview(file_field, ancho=ancho, alto=alto)
    return img if img else Paragraph("Certificado no disponible", styles["SmallPro"])


import io
import requests
from datetime import datetime

from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def cargar_imagen_o_preview(file_field, ancho=92, alto=92):
    """
    Devuelve un Flowable Image para imágenes (funciona con Cloudinary),
    y None para PDFs u otros tipos (para no romper ReportLab).
    """
    if not file_field:
        return None

    # Si el campo no tiene archivo asociado
    try:
        url = file_field.url
    except Exception:
        return None

    if not url:
        return None

    url_lower = url.lower()

    # Si es PDF, NO intentamos renderizar como imagen
    if url_lower.endswith(".pdf"):
        return None

    # Descargar imagen desde URL (Cloudinary u otro storage)
    try:
        r = requests.get(url, timeout=12)
        r.raise_for_status()
        img_bytes = io.BytesIO(r.content)
        img = Image(img_bytes, width=ancho, height=alto)
        img.hAlign = "RIGHT"
        return img
    except Exception:
        return None


def certificado_cell(file_field, styles, ancho=150, alto=105):
    """
    - Si es PDF: devuelve un link clickeable
    - Si es imagen: devuelve preview (Image)
    - Si no existe o falla: '—'
    """
    if not file_field:
        return "—"

    try:
        url = file_field.url
    except Exception:
        return "—"

    if not url:
        return "—"

    if url.lower().endswith(".pdf"):
        # Link clickeable dentro del PDF
        return Paragraph(f'<link href="{url}">Ver certificado (PDF)</link>', styles["SmallPro"])

    # Intentar como imagen
    img = cargar_imagen_o_preview(file_field, ancho=ancho, alto=alto)
    return img if img else Paragraph("Certificado no disponible", styles["SmallPro"])


from datetime import datetime
from django.http import HttpResponse

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader


def datos_pdf(request):
    cfg = get_cv_config()

    # ✅ más robusto si perfilactivo es BooleanField
    datos = DatosPersonales.objects.filter(perfilactivo=True).first()
    if not datos:
        return HttpResponse("No hay datos para generar el PDF")

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="hoja_de_vida_premium.pdf"'

    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=55,
        bottomMargin=55
    )

    styles = getSampleStyleSheet()

    # =========================
    # ESTILOS PREMIUM
    # =========================
    if "NameTitle" not in styles:
        styles.add(ParagraphStyle(
            name="NameTitle",
            fontSize=22,
            leading=26,
            fontName="Helvetica-Bold",
            textColor=colors.HexColor("#111827"),
            spaceAfter=2,
        ))

    if "SubHeader" not in styles:
        styles.add(ParagraphStyle(
            name="SubHeader",
            fontSize=10.5,
            leading=14,
            fontName="Helvetica",
            textColor=colors.HexColor("#6B7280"),
            spaceAfter=8,
        ))

    if "NormalPro" not in styles:
        styles.add(ParagraphStyle(
            name="NormalPro",
            fontSize=10.3,
            leading=13.2,
            fontName="Helvetica",
            textColor=colors.HexColor("#1F2937"),
        ))

    if "SmallPro" not in styles:
        styles.add(ParagraphStyle(
            name="SmallPro",
            fontSize=9.2,
            leading=12.0,
            fontName="Helvetica",
            textColor=colors.HexColor("#374151"),
        ))

    table_style_premium = TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F3F4F6")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#111827")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.HexColor("#D1D5DB")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
    ])

    # =========================
    # FOOTER
    # =========================
    generated_at = datetime.now().strftime("%d/%m/%Y %H:%M")

    def draw_footer(canvas, doc_):
        canvas.saveState()
        canvas.setFont("Helvetica", 9)

        canvas.setStrokeColor(colors.HexColor("#D1D5DB"))
        canvas.setLineWidth(0.6)
        canvas.line(doc_.leftMargin, 45, A4[0] - doc_.rightMargin, 45)

        left_text = f"{datos.nombres} {datos.apellidos} · Hoja de vida"
        center_text = f"Generado: {generated_at}"
        right_text = f"Página {canvas.getPageNumber()}"

        canvas.setFillColor(colors.HexColor("#6B7280"))
        canvas.drawString(doc_.leftMargin, 30, left_text)
        canvas.drawCentredString(A4[0] / 2, 30, center_text)
        canvas.drawRightString(A4[0] - doc_.rightMargin, 30, right_text)

        canvas.restoreState()

    # =========================
    # HELPERS
    # =========================
    elements = []
    ANCHO_UTIL = A4[0] - doc.leftMargin - doc.rightMargin

    def section_bar(title):
        bar = Table([[title]], colWidths=[ANCHO_UTIL])
        bar.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EEF2FF")),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#1D4ED8")),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 11),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ]))
        elements.append(Spacer(1, 10))
        elements.append(bar)
        elements.append(Spacer(1, 8))

    def kv_table(rows):
        t = Table(rows, colWidths=[155, ANCHO_UTIL - 155])
        t.setStyle(table_style_premium)
        return t

    def two_col_blocks(items, render_block, gap=10):
        blocks = [render_block(x) for x in items]
        if len(blocks) % 2 == 1:
            blocks.append(Spacer(1, 1))

        rows = []
        for i in range(0, len(blocks), 2):
            rows.append([blocks[i], blocks[i + 1]])

        tbl = Table(
            rows,
            colWidths=[(ANCHO_UTIL - gap) / 2, (ANCHO_UTIL - gap) / 2],
            hAlign="LEFT"
        )
        tbl.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), gap),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ]))
        return tbl

    def imagen_con_limite(filefield, max_w, max_h):
        """
        - Mantiene tamaño original.
        - Reduce SOLO si no cabe.
        - Si no hay .path (cloud/URL), cae a cargar_imagen_o_preview.
        - Si es PDF, muestra etiqueta.
        """
        if not filefield:
            return None

        try:
            path = getattr(filefield, "path", None)

            if not path:
                return cargar_imagen_o_preview(filefield, ancho=max_w, alto=max_h)

            if str(path).lower().endswith(".pdf"):
                return Paragraph("📄 Certificado (PDF adjunto)", styles["SmallPro"])

            ir = ImageReader(path)
            iw, ih = ir.getSize()

            img = Image(path)
            # Mantener tamaño original y reducir solo si no cabe
            scale = min(max_w / float(iw), max_h / float(ih), 1.0)
            img.drawWidth = iw * scale
            img.drawHeight = ih * scale
            return img

        except Exception:
            return cargar_imagen_o_preview(filefield, ancho=max_w, alto=max_h)

    def certificado_fullwidth(filefield):
        """
        Certificado sin cuadro (sin borde).
        Muestra arriba 'CERTIFICADO' y luego la imagen al tamaño original
        (solo reduce si no cabe en la página).
        """
        if not filefield:
            return

        elements.append(Spacer(1, 10))

        # Título arriba (sin cuadro)
        elements.append(Paragraph("<b>CERTIFICADO</b>", styles["SubHeader"]))
        elements.append(Spacer(1, 6))

        img = imagen_con_limite(filefield, max_w=ANCHO_UTIL, max_h=700)
        if not img:
            elements.append(Paragraph("—", styles["NormalPro"]))
            elements.append(Spacer(1, 12))
            return

        # Centrar sin borde usando una tabla “invisible”
        wrapper = Table([[img]], colWidths=[ANCHO_UTIL], hAlign="LEFT")
        wrapper.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            # SIN BOX / SIN GRID / SIN BACKGROUND
        ]))
        elements.append(wrapper)
        elements.append(Spacer(1, 14))

    def color_estado(estado):
        e = (estado or "").strip().lower()
        if "excelente" in e:
            return colors.HexColor("#ECFDF5")
        if "bueno" in e:
            return colors.HexColor("#EFF6FF")
        if "regular" in e:
            return colors.HexColor("#FFFBEB")
        return colors.white

    # =========================
    # HEADER
    # =========================
    nombre = f"{datos.nombres} {datos.apellidos}"
    subtitulo = "Hoja de Vida Profesional"
    foto = cargar_imagen_o_preview(datos.foto, ancho=92, alto=92)  # ✅ perfil fijo

    contacto_line = " | ".join([
        f"Cédula: {datos.numerocedula}",
        f"Tel: {datos.telefonoconvencional}",
        f"Web: {datos.sitioweb}" if datos.sitioweb else "Web: —"
    ])

    left_header = [
        Paragraph(nombre, styles["NameTitle"]),
        Paragraph(subtitulo, styles["SubHeader"]),
        Paragraph(contacto_line, styles["SmallPro"]),
    ]

    header_tbl = Table([[left_header, foto if foto else ""]], colWidths=[360, 90])
    header_tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(header_tbl)

    div = Table([[""]], colWidths=[ANCHO_UTIL])
    div.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 1, colors.HexColor("#E5E7EB"))]))
    elements.append(div)

    # =========================
    # DATOS PERSONALES
    # =========================
    if getattr(cfg, "mostrar_datos_personales", True):
        section_bar("DATOS PERSONALES")
        tabla_datos = [
            ["Nombres", datos.nombres or "—"],
            ["Apellidos", datos.apellidos or "—"],
            ["Nacionalidad", datos.nacionalidad or "—"],
            ["Lugar de nacimiento", datos.lugarnacimiento or "—"],
            ["Fecha de nacimiento", str(datos.fechanacimiento) if datos.fechanacimiento else "—"],
            ["Cédula", datos.numerocedula or "—"],
            ["Sexo", datos.get_sexo_display() if hasattr(datos, "get_sexo_display") else "—"],
            ["Estado civil", datos.estadocivil or "—"],
            ["Licencia de conducir", datos.licenciaconducir or "—"],
            ["Teléfono", datos.telefonoconvencional or "—"],
            ["Teléfono fijo", getattr(datos, "telefonofijo", "—") or "—"],
            ["Dirección domiciliaria", datos.direcciondomiciliaria or "—"],
            ["Dirección trabajo", datos.direcciontrabajo or "—"],
            ["Sitio web", datos.sitioweb or "—"],
        ]
        elements.append(kv_table(tabla_datos))

    # =========================
    # EXPERIENCIA LABORAL (certificado sin cuadro)
    # =========================
    if getattr(cfg, "mostrar_experiencia", True):
        section_bar("EXPERIENCIA LABORAL")

        exps = ExperienciaLaboral.objects.filter(
            perfil=datos,
            activarparaqueseveaenfront=True
        )

        if exps.exists():
            for exp in exps:
                tabla = [
                    ["Cargo", exp.cargodesempenado or "—"],
                    ["Empresa", exp.nombrempresa or "—"],
                    ["Lugar", exp.lugarempresa or "—"],
                    ["Email", exp.emailempresa or "—"],
                    ["Sitio web", exp.sitiowebempresa or "—"],
                    ["Contacto", f"{exp.nombrecontactoempresarial} - {exp.telefonocontactoempresarial}"],
                    ["Periodo", f"{exp.fechainiciogestion} - {exp.fechafingestion if exp.fechafingestion else 'Actual'}"],
                    ["Funciones", Paragraph(exp.descripcionfunciones or "—", styles["NormalPro"])],
                ]
                elements.append(kv_table(tabla))
                certificado_fullwidth(getattr(exp, "rutacertificado", None))
        else:
            elements.append(Paragraph("No registra experiencia laboral.", styles["NormalPro"]))

    # =========================
    # RECONOCIMIENTOS (certificado sin cuadro)
    # =========================
    if getattr(cfg, "mostrar_reconocimientos", True):
        section_bar("RECONOCIMIENTOS")

        recs = Reconocimiento.objects.filter(perfil=datos, activarparaqueseveaenfront=True)
        if recs.exists():
            for r in recs:
                tabla = [
                    ["Tipo", r.tiporeconocimiento or "—"],
                    ["Fecha", str(r.fechareconocimiento) if r.fechareconocimiento else "—"],
                    ["Descripción", Paragraph(r.descripcionreconocimiento or "—", styles["NormalPro"])],
                    ["Entidad", r.entidadpatrocinadora or "—"],
                    ["Contacto", f"{r.nombrecontactoauspicia} - {r.telefonocontactoauspicia}"],
                ]
                elements.append(kv_table(tabla))
                certificado_fullwidth(getattr(r, "rutacertificado", None))
        else:
            elements.append(Paragraph("No registra reconocimientos.", styles["NormalPro"]))

    # =========================
    # CURSOS REALIZADOS (certificado sin cuadro)
    # =========================
    if getattr(cfg, "mostrar_cursos", True):
        section_bar("CURSOS REALIZADOS")

        cursos = CursoRealizado.objects.filter(perfil=datos, activarparaqueseveaenfront=True)
        if cursos.exists():
            for c in cursos:
                tabla = [
                    ["Curso", c.nombrecurso or "—"],
                    ["Inicio", str(c.fechainicio) if c.fechainicio else "—"],
                    ["Fin", str(c.fechafin) if c.fechafin else "—"],
                    ["Horas", str(c.totalhoras) if c.totalhoras is not None else "—"],
                    ["Descripción", Paragraph(c.descripcioncurso or "—", styles["NormalPro"])],
                    ["Entidad", c.entidadpatrocinadora or "—"],
                    ["Contacto", f"{c.nombrecontactoauspicia} - {c.telefonocontactoauspicia}"],
                    ["Email", c.emailempresapatrocinadora or "—"],
                ]
                elements.append(kv_table(tabla))
                certificado_fullwidth(getattr(c, "rutacertificado", None))
        else:
            elements.append(Paragraph("No registra cursos.", styles["NormalPro"]))

    # =========================
    # PRODUCTOS ACADÉMICOS
    # =========================
    if getattr(cfg, "mostrar_productos_academicos", True):
        section_bar("PRODUCTOS ACADÉMICOS")

        pacad = list(ProductoAcademico.objects.filter(perfil=datos, activarparaqueseveaenfront=True))
        if pacad:
            def render_pacad(p):
                t = Table(
                    [
                        [Paragraph(f"<b>Recurso:</b> {p.nombrerecurso}", styles["SmallPro"])],
                        [Paragraph(f"<b>Clasificador:</b> {p.clasificador}", styles["SmallPro"])],
                        [Paragraph(f"<b>Descripción:</b> {p.descripcion}", styles["SmallPro"])],
                    ],
                    colWidths=[(ANCHO_UTIL - 10) / 2]
                )
                t.setStyle(TableStyle([
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
                    ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ]))
                return t

            elements.append(two_col_blocks(pacad, render_pacad))
        else:
            elements.append(Paragraph("No registra productos académicos.", styles["NormalPro"]))

    # =========================
    # PRODUCTOS LABORALES
    # =========================
    if getattr(cfg, "mostrar_productos_laborales", True):
        section_bar("PRODUCTOS LABORALES")

        plab = list(ProductoLaboral.objects.filter(perfil=datos, activarparaqueseveaenfront=True))
        if plab:
            def render_plab(p):
                t = Table(
                    [
                        [Paragraph(f"<b>Producto:</b> {p.nombreproducto}", styles["SmallPro"])],
                        [Paragraph(f"<b>Fecha:</b> {p.fechaproducto}", styles["SmallPro"])],
                        [Paragraph(f"<b>Descripción:</b> {p.descripcion}", styles["SmallPro"])],
                    ],
                    colWidths=[(ANCHO_UTIL - 10) / 2]
                )
                t.setStyle(TableStyle([
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
                    ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ]))
                return t

            elements.append(two_col_blocks(plab, render_plab))
        else:
            elements.append(Paragraph("No registra productos laborales.", styles["NormalPro"]))

    # =========================
    # VENTA DE GARAGE (más visible)
    # =========================
    if getattr(cfg, "mostrar_venta_garage", True):
        section_bar("VENTA DE GARAGE")

        ventas = list(VentaGarage.objects.filter(perfil=datos, activarparaqueseveaenfront=True))
        if ventas:
            for v in ventas:
                foto_art = cargar_imagen_o_preview(v.articulo, ancho=230, alto=170)

                fecha_pub = getattr(v, "fechapublicacion", None)
                fecha_pub_txt = str(fecha_pub) if fecha_pub else "—"

                estado_txt = v.estadoproducto or "—"
                bg = color_estado(estado_txt)

                left = foto_art if foto_art else Paragraph("<b>Foto:</b> —", styles["SmallPro"])

                right = [
                    Paragraph(f"<b>Producto:</b> {v.nombreproducto}", styles["NormalPro"]),
                    Paragraph(f"<b>Estado:</b> {estado_txt}", styles["NormalPro"]),
                    Paragraph(f"<b>Fecha publicación:</b> {fecha_pub_txt}", styles["NormalPro"]),
                    Paragraph(f"<b>Valor:</b> ${v.valordelbien}", styles["NormalPro"]),
                    Paragraph(f"<b>Descripción:</b> {v.descripcion}", styles["NormalPro"]),
                ]

                card = Table([[left, right]], colWidths=[250, ANCHO_UTIL - 250])
                card.setStyle(TableStyle([
                    ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#D1D5DB")),
                    ("BACKGROUND", (0, 0), (-1, -1), bg),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ]))

                elements.append(card)
                elements.append(Spacer(1, 12))
        else:
            elements.append(Paragraph("No hay productos en venta.", styles["NormalPro"]))

    # =========================
    # BUILD
    # =========================
    doc.build(elements, onFirstPage=draw_footer, onLaterPages=draw_footer)
    return response




##EXPERIENCIA LABORAL

from .models import ExperienciaLaboral
from .forms import ExperienciaLaboralForm

def experiencia_list(request):
    cfg = get_cv_config()

    # Público: bloqueado si apagado
    if not cfg.mostrar_experiencia and not request.user.is_staff:
        return render(request, "bloqueado.html", {"mensaje": "Experiencia Laboral está deshabilitada por el administrador."})

    # Mostrar solo activos para público, pero admin ve todo
    if request.user.is_staff:
        experiencias = ExperienciaLaboral.objects.all()
    else:
        experiencias = ExperienciaLaboral.objects.filter(activarparaqueseveaenfront=True)

    return render(request, 'experiencia/list.html', {'experiencias': experiencias, "cfg": cfg})



@staff_member_required
def experiencia_create(request):
    form = ExperienciaLaboralForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('experiencia_list')
    return render(request, 'experiencia/form.html', {'form': form})


@staff_member_required
def experiencia_update(request, pk):
    experiencia = get_object_or_404(ExperienciaLaboral, pk=pk)

    if request.method == "POST":
        form = ExperienciaLaboralForm(
            request.POST,
            request.FILES,
            instance=experiencia
        )

        if form.is_valid():
            form.save()
            return redirect('experiencia_list')

    else:
        form = ExperienciaLaboralForm(instance=experiencia)

    return render(request, 'experiencia/form.html', {'form': form})


@staff_member_required
def experiencia_delete(request, pk):
    experiencia = get_object_or_404(ExperienciaLaboral, pk=pk)
    if request.method == 'POST':
        experiencia.delete()
        return redirect('experiencia_list')
    return render(request, 'experiencia/delete.html', {'experiencia': experiencia})

##RECONOCIMIENTOS

from django.shortcuts import render, redirect, get_object_or_404
from .models import Reconocimiento
from .forms import ReconocimientoForm

def reconocimiento_list(request):
    cfg = get_cv_config()

    if not cfg.mostrar_reconocimientos and not request.user.is_staff:
        return render(request, "bloqueado.html", {"mensaje": "Reconocimientos está deshabilitada por el administrador."})

    if request.user.is_staff:
        reconocimientos = Reconocimiento.objects.all()
    else:
        reconocimientos = Reconocimiento.objects.filter(activarparaqueseveaenfront=True)

    return render(request, 'reconocimiento/list.html', {'reconocimientos': reconocimientos, "cfg": cfg})



@staff_member_required
def reconocimiento_create(request):
    form = ReconocimientoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('reconocimiento_list')
    return render(request, 'reconocimiento/form.html', {'form': form, 'accion': 'Crear'})


@staff_member_required
def reconocimiento_update(request, pk):
    reconocimiento = get_object_or_404(Reconocimiento, pk=pk)
    form = ReconocimientoForm(request.POST or None, request.FILES or None, instance=reconocimiento)

    if form.is_valid():
        form.save()
        return redirect('reconocimiento_list')

    return render(request, 'reconocimiento/form.html', {
        'form': form,
        'accion': 'Editar'
    })


@staff_member_required
def reconocimiento_delete(request, pk):
    reconocimiento = get_object_or_404(Reconocimiento, pk=pk)
    if request.method == 'POST':
        reconocimiento.delete()
        return redirect('reconocimiento_list')
    return render(request, 'reconocimiento/delete.html', {'reconocimiento': reconocimiento})


##CURSOS REALIZADOS

from django.shortcuts import render, redirect, get_object_or_404
from .models import CursoRealizado
from .forms import CursoRealizadoForm

def curso_list(request):
    cfg = get_cv_config()

    if not cfg.mostrar_cursos and not request.user.is_staff:
        return render(request, "bloqueado.html", {"mensaje": "Cursos está deshabilitada por el administrador."})

    if request.user.is_staff:
        cursos = CursoRealizado.objects.all()
    else:
        cursos = CursoRealizado.objects.filter(activarparaqueseveaenfront=True)

    return render(request, 'curso/list.html', {'cursos': cursos, "cfg": cfg})



@staff_member_required
def curso_create(request):
    form = CursoRealizadoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('curso_list')
    return render(request, 'curso/form.html', {'form': form, 'accion': 'Crear'})


@staff_member_required
def curso_update(request, pk):
    curso = get_object_or_404(CursoRealizado, pk=pk)
    form = CursoRealizadoForm(
        request.POST or None,
        request.FILES or None,
        instance=curso
    )

    if form.is_valid():
        form.save()
        return redirect('curso_list')

    return render(request, 'curso/form.html', {
        'form': form,
        'accion': 'Editar'
    })


@staff_member_required
def curso_delete(request, pk):
    curso = get_object_or_404(CursoRealizado, pk=pk)
    if request.method == 'POST':
        curso.delete()
        return redirect('curso_list')
    return render(request, 'curso/delete.html', {'curso': curso})

##PRODUCTO ACADEMICO
from django.shortcuts import render, redirect, get_object_or_404
from .models import ProductoAcademico
from .forms import ProductoAcademicoForm


def productoacademico_list(request):
    cfg = get_cv_config()

    if not cfg.mostrar_productos_academicos and not request.user.is_staff:
        return render(request, "bloqueado.html", {"mensaje": "Productos Académicos está deshabilitada por el administrador."})

    if request.user.is_staff:
        productos = ProductoAcademico.objects.all()
    else:
        productos = ProductoAcademico.objects.filter(activarparaqueseveaenfront=True)

    return render(request, 'productoacademico/list.html', {'productos': productos, "cfg": cfg})



@staff_member_required
def productoacademico_create(request):
    form = ProductoAcademicoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('productoacademico_list')
    return render(request, 'productoacademico/form.html', {'form': form, 'accion': 'Crear'})


@staff_member_required
def productoacademico_update(request, pk):
    producto = get_object_or_404(ProductoAcademico, pk=pk)
    form = ProductoAcademicoForm(request.POST or None, instance=producto)
    if form.is_valid():
        form.save()
        return redirect('productoacademico_list')
    return render(request, 'productoacademico/form.html', {'form': form, 'accion': 'Editar'})


@staff_member_required
def productoacademico_delete(request, pk):
    producto = get_object_or_404(ProductoAcademico, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('productoacademico_list')
    return render(request, 'productoacademico/delete.html', {'producto': producto})


##PRODUCTO LABORAL
from django.shortcuts import render, redirect, get_object_or_404
from .models import ProductoLaboral
from .forms import ProductoLaboralForm


def producto_laboral_list(request):
    cfg = get_cv_config()

    if not cfg.mostrar_productos_laborales and not request.user.is_staff:
        return render(request, "bloqueado.html", {"mensaje": "Productos Laborales está deshabilitada por el administrador."})

    if request.user.is_staff:
        productos = ProductoLaboral.objects.all()
    else:
        productos = ProductoLaboral.objects.filter(activarparaqueseveaenfront=True)

    return render(request, 'productolaboral/list.html', {'productos': productos, "cfg": cfg})



@staff_member_required
def producto_laboral_create(request):
    form = ProductoLaboralForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('producto_laboral_list')
    return render(request, 'productolaboral/form.html', {
        'form': form,
        'accion': 'Crear'
    })


@staff_member_required
def producto_laboral_update(request, pk):
    producto = get_object_or_404(ProductoLaboral, pk=pk)
    form = ProductoLaboralForm(request.POST or None, instance=producto)
    if form.is_valid():
        form.save()
        return redirect('producto_laboral_list')
    return render(request, 'productolaboral/form.html', {
        'form': form,
        'accion': 'Editar'
    })


@staff_member_required
def producto_laboral_delete(request, pk):
    producto = get_object_or_404(ProductoLaboral, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('producto_laboral_list')
    return render(request, 'productolaboral/delete.html', {
        'producto': producto
    })

##VENTA DE GARAGE
from django.shortcuts import render, redirect, get_object_or_404
from .models import VentaGarage
from .forms import VentaGarageForm

def ventagarage_list(request):
    cfg = get_cv_config()

    if not cfg.mostrar_venta_garage and not request.user.is_staff:
        return render(request, "bloqueado.html", {"mensaje": "Venta de Garage está deshabilitada por el administrador."})

    if request.user.is_staff:
        ventas = VentaGarage.objects.all()
    else:
        ventas = VentaGarage.objects.filter(activarparaqueseveaenfront=True)

    return render(request, 'ventagarage/list.html', {'ventas': ventas, "cfg": cfg})



@staff_member_required
def ventagarage_create(request):
    form = VentaGarageForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('ventagarage_list')
    return render(request, 'ventagarage/form.html', {
        'form': form,
        'accion': 'Crear'
    })


@staff_member_required
def ventagarage_update(request, pk):
    venta = get_object_or_404(VentaGarage, pk=pk)
    form = VentaGarageForm(
        request.POST or None,
        request.FILES or None,
        instance=venta
    )

    if form.is_valid():
        form.save()
        return redirect('ventagarage_list')

    return render(request, 'ventagarage/form.html', {
        'form': form,
        'accion': 'Editar'
    })


@staff_member_required
def ventagarage_delete(request, pk):
    venta = get_object_or_404(VentaGarage, pk=pk)
    if request.method == 'POST':
        venta.delete()
        return redirect('ventagarage_list')
    return render(request, 'ventagarage/delete.html', {
        'venta': venta
    })


from .models import DatosPersonales
from django.contrib.auth.decorators import login_required


def dashboard_usuario(request):
    personas = DatosPersonales.objects.filter(usuario=request.user)

    return render(request, 'dashboard.html', {
        'personas': personas
    })


from .models import ConfigSeccionesCV

def get_cv_config():
    cfg = ConfigSeccionesCV.objects.first()
    if not cfg:
        cfg = ConfigSeccionesCV.objects.create()
    return cfg

from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ConfigSeccionesCVForm
from .models import ConfigSeccionesCV


def secciones_admin(request):
    cfg = get_cv_config()

    if request.method == "POST":
        form = ConfigSeccionesCVForm(request.POST, instance=cfg)
        if form.is_valid():
            form.save()
            return redirect("secciones_admin")
    else:
        form = ConfigSeccionesCVForm(instance=cfg)

    return render(request, "admin/secciones.html", {"form": form, "cfg": cfg})
