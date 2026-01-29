from django import forms
from .models import Task
from django import forms
from .models import DatosPersonales
from .models import ExperienciaLaboral

class DatosPersonalesForm(forms.ModelForm):
    class Meta:
        model = DatosPersonales
        fields = "__all__"
        widgets = {
            "fechanacimiento": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),
        }

    def clean_fechanacimiento(self):
        f = self.cleaned_data.get("fechanacimiento")
        if f and f > date.today():
            raise forms.ValidationError("La fecha no puede ser futura.")
        return f

from datetime import date
from django import forms

class ExperienciaLaboralForm(forms.ModelForm):
    class Meta:
        model = ExperienciaLaboral
        fields = "__all__"
        widgets = {
            "fechainiciogestion": forms.DateInput(attrs={"type": "date"}),
            "fechafingestion": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned = super().clean()
        ini = cleaned.get("fechainiciogestion")
        fin = cleaned.get("fechafingestion")

        if ini and ini > date.today():
            self.add_error("fechainiciogestion", "La fecha de inicio no puede ser futura.")

        if fin and fin > date.today():
            self.add_error("fechafingestion", "La fecha de fin no puede ser futura.")

        if ini and fin and fin < ini:
            self.add_error("fechafingestion", "La fecha fin no puede ser menor que la fecha inicio.")

        return cleaned


from .models import Reconocimiento

class ReconocimientoForm(forms.ModelForm):
    class Meta:
        model = Reconocimiento
        fields = "__all__"
        widgets = {
            "fechareconocimiento": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_fechareconocimiento(self):
        f = self.cleaned_data.get("fechareconocimiento")
        if f and f > date.today():
            raise forms.ValidationError("La fecha no puede ser futura.")
        return f


from .models import CursoRealizado

from django import forms
from datetime import date
from .models import CursoRealizado

class CursoRealizadoForm(forms.ModelForm):
    class Meta:
        model = CursoRealizado
        fields = "__all__"
        widgets = {
            "fechainicio": forms.DateInput(attrs={"type": "date"}),
            "fechafin": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned = super().clean()
        ini = cleaned.get("fechainicio")
        fin = cleaned.get("fechafin")

        if ini and ini > date.today():
            self.add_error("fechainicio", "La fecha de inicio no puede ser futura.")

        if fin and fin > date.today():
            self.add_error("fechafin", "La fecha de fin no puede ser futura.")

        if ini and fin and fin < ini:
            self.add_error("fechafin", "La fecha fin no puede ser menor que la fecha inicio.")

        return cleaned

        
from django import forms
from .models import ProductoAcademico

class ProductoAcademicoForm(forms.ModelForm):
    class Meta:
        model = ProductoAcademico
        fields = '__all__'

from .models import ProductoLaboral

class ProductoLaboralForm(forms.ModelForm):
    class Meta:
        model = ProductoLaboral
        fields = "__all__"
        widgets = {
            "fechaproducto": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_fechaproducto(self):
        f = self.cleaned_data.get("fechaproducto")
        if f and f > date.today():
            raise forms.ValidationError("La fecha no puede ser futura.")
        return f


from .models import VentaGarage

from django import forms
from .models import VentaGarage

class VentaGarageForm(forms.ModelForm):
    class Meta:
        model = VentaGarage
        fields = "__all__"
        widgets = {
            "fechapublicacion": forms.DateInput(attrs={"type": "date"}),
        }

from django import forms
from .models import ConfigSeccionesCV

class ConfigSeccionesCVForm(forms.ModelForm):
    class Meta:
        model = ConfigSeccionesCV
        fields = [
            "mostrar_datos_personales",
            "mostrar_experiencia",
            "mostrar_reconocimientos",
            "mostrar_cursos",
            "mostrar_productos_academicos",
            "mostrar_productos_laborales",
            "mostrar_venta_garage",
        ]
        widgets = {f: forms.CheckboxInput(attrs={"class": "form-check-input"}) for f in fields}
