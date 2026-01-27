from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    Task,
    DatosPersonales,
    ExperienciaLaboral,
    Reconocimiento,
    CursoRealizado,
    ProductoAcademico,
    ProductoLaboral,
    VentaGarage,
)

admin.site.register(Task)
admin.site.register(DatosPersonales)
admin.site.register(ExperienciaLaboral)
admin.site.register(Reconocimiento)
admin.site.register(CursoRealizado)
admin.site.register(ProductoAcademico)
admin.site.register(ProductoLaboral)
admin.site.register(VentaGarage)


from django.contrib import admin
from .models import ConfigSeccionesCV

@admin.register(ConfigSeccionesCV)
class ConfigSeccionesCVAdmin(admin.ModelAdmin):
    list_display = (
        "mostrar_datos_personales",
        "mostrar_experiencia",
        "mostrar_reconocimientos",
        "mostrar_cursos",
        "mostrar_productos_academicos",
        "mostrar_productos_laborales",
        "mostrar_venta_garage",
        "actualizado",
    )

    # para evitar crear varias configuraciones (solo 1 fila)
    def has_add_permission(self, request):
        if ConfigSeccionesCV.objects.exists():
            return False
        return True
