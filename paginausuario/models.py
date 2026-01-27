from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title=models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created=models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True,blank=True)
    important=models.BooleanField(default=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title +'- by'+ self.user.username
    

class DatosPersonales(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
    idperfil = models.AutoField(primary_key=True)
    descripcionperfil = models.CharField(max_length=50)
    perfilactivo = models.IntegerField()

    apellidos = models.CharField(max_length=60)
    nombres = models.CharField(max_length=60)
    nacionalidad = models.CharField(max_length=20)
    lugarnacimiento = models.CharField(max_length=60)
    fechanacimiento = models.CharField(max_length=60)


    numerocedula = models.CharField(max_length=10, unique=True)

    SEXO_CHOICES = [
        ('H', 'Hombre'),
        ('M', 'Mujer'),
    ]
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)

    estadocivil = models.CharField(max_length=50)
    licenciaconducir = models.CharField(max_length=6)

    telefonoconvencional = models.CharField(max_length=15)
    telefonofijo = models.CharField(max_length=15)

    direcciontrabajo = models.CharField(max_length=200)
    direcciondomiciliaria = models.CharField(max_length=200)

    sitioweb = models.CharField(max_length=60)

    foto = models.ImageField(
        upload_to="fotos_perfil/",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
    
			
class ExperienciaLaboral(models.Model):
    idexperiencialaboral = models.AutoField(primary_key=True)

    perfil = models.ForeignKey(
        DatosPersonales,
        on_delete=models.CASCADE,
        db_column="idperfilconqueestaactivo"
    )

    cargodesempenado = models.CharField(max_length=200)
    nombrempresa = models.CharField(max_length=50)
    lugarempresa = models.CharField(max_length=200)
    emailempresa = models.CharField(max_length=100)
    sitiowebempresa = models.CharField(max_length=100)

    nombrecontactoempresarial = models.CharField(max_length=100)
    telefonocontactoempresarial = models.CharField(max_length=60)

    fechainiciogestion = models.DateField()
    fechafingestion = models.DateField(null=True, blank=True)

    descripcionfunciones = models.CharField(max_length=100)

    activarparaqueseveaenfront = models.BooleanField(default=True)

    rutacertificado = models.FileField(
    upload_to="certificados_laborales/",
    null=True,
    blank=True
    )

    class Meta:
        db_table = "EXPERIENCIALABORAL"

			
			
class Reconocimiento(models.Model):
    idreconocimiento = models.AutoField(primary_key=True)

    perfil = models.ForeignKey(
        DatosPersonales,
        on_delete=models.CASCADE,
        db_column="idperfilconqueestaactivo"
    )

    TIPO_CHOICES = [
        ('Académico', 'Académico'),
        ('Público', 'Público'),
        ('Privado', 'Privado'),
    ]
    tiporeconocimiento = models.CharField(max_length=100, choices=TIPO_CHOICES)

    fechareconocimiento = models.DateField()
    descripcionreconocimiento = models.CharField(max_length=200)

    entidadpatrocinadora = models.CharField(max_length=100)
    nombrecontactoauspicia = models.CharField(max_length=100)
    telefonocontactoauspicia = models.CharField(max_length=60)

    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.FileField(
    upload_to="certificados_reconocimientos/",
    null=True,
    blank=True
    )

    class Meta:
        db_table = "RECONOCIMIENTOS"

			
class CursoRealizado(models.Model):
    idcursorealizado = models.AutoField(primary_key=True)

    perfil = models.ForeignKey(
        DatosPersonales,
        on_delete=models.CASCADE,
        db_column="idperfilconqueestaactivo"
    )

    nombrecurso = models.CharField(max_length=100)
    fechainicio = models.DateField()
    fechafin = models.DateField()

    totalhoras = models.CharField(max_length=100)
    descripcioncurso = models.CharField(max_length=200)

    entidadpatrocinadora = models.CharField(max_length=100)
    nombrecontactoauspicia = models.CharField(max_length=100)
    telefonocontactoauspicia = models.CharField(max_length=60)
    emailempresapatrocinadora = models.CharField(max_length=60)

    activarparaqueseveaenfront = models.BooleanField(default=True)
    rutacertificado = models.FileField(
    upload_to="certificados_cursos/",
    null=True,
    blank=True
    ) 

    class Meta:
        db_table = "CURSOSREALIZADOS"

			
class ProductoAcademico(models.Model):
    idproductoacademico = models.AutoField(primary_key=True)

    perfil = models.ForeignKey(
        DatosPersonales,
        on_delete=models.CASCADE,
        db_column="idperfilconqueestaactivo"
    )

    nombrerecurso = models.CharField(max_length=100)
    clasificador = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)

    activarparaqueseveaenfront = models.BooleanField(default=True)

    class Meta:
        db_table = "PRODUCTOSACADEMICOS"

			
class ProductoLaboral(models.Model):
    idproductoslaborales = models.AutoField(primary_key=True)

    perfil = models.ForeignKey(
        DatosPersonales,
        on_delete=models.CASCADE,
        db_column="idperfilconqueestaactivo"
    )

    nombreproducto = models.CharField(max_length=100)
    fechaproducto = models.DateField()
    descripcion = models.CharField(max_length=200)

    activarparaqueseveaenfront = models.BooleanField(default=True)

    class Meta:
        db_table = "PRODUCTOSLABORALES"
	
			
from django.utils import timezone

class VentaGarage(models.Model):
    idventagarage = models.AutoField(primary_key=True)

    perfil = models.ForeignKey(
        DatosPersonales,
        on_delete=models.CASCADE,
        db_column="idperfilconqueestaactivo"
    )

    nombreproducto = models.CharField(max_length=100)

    ESTADO_CHOICES = [
        ('Excelente', 'Excelente'),
        ('Bueno', 'Bueno'),
        ('Regular', 'Regular'),
    ]
    estadoproducto = models.CharField(max_length=40, choices=ESTADO_CHOICES)

    descripcion = models.CharField(max_length=200)
    valordelbien = models.DecimalField(max_digits=7, decimal_places=2)  # opcional subir a 7 por si hay valores mayores

    # ✅ NUEVO: fecha de publicación
    fechapublicacion = models.DateField(default=timezone.now)

    activarparaqueseveaenfront = models.BooleanField(default=True)

    # ✅ Imagen del producto (mejor que FileField)
    articulo = models.ImageField(
        upload_to="articulo_ventagarage/",
        null=True,
        blank=True
    )

    class Meta:
        db_table = "VENTAGARAGE"

from django.db import models

class ConfigSeccionesCV(models.Model):
    mostrar_datos_personales = models.BooleanField(default=True)
    mostrar_experiencia = models.BooleanField(default=True)
    mostrar_reconocimientos = models.BooleanField(default=True)
    mostrar_cursos = models.BooleanField(default=True)
    mostrar_productos_academicos = models.BooleanField(default=True)
    mostrar_productos_laborales = models.BooleanField(default=True)
    mostrar_venta_garage = models.BooleanField(default=True)

    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuración CV"
        verbose_name_plural = "Configuración CV"

    def __str__(self):
        return "Configuración de Secciones CV"
