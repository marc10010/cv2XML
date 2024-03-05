from django.db import models
class Referencia (models.Model):
    descripcion = models.TextField()

    def __str__(self):
        return self.descripcion
class Idioma(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Titulacion(models.Model):
    descripcion = models.TextField()

    def __str__(self):
        return self.descripcion

class Experiencia(models.Model):
    descripcion = models.TextField()

    def __str__(self):
        return self.descripcion

class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=100)
    nombre_completo = models.CharField(max_length=150)
    subcategoria = models.CharField(max_length=50)
    descripcion = models.TextField()
    ciudad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    referencias = models.ManyToManyField(Referencia)
    idiomas = models.ManyToManyField(Idioma)
    titulaciones = models.ManyToManyField(Titulacion)
    experiencias = models.ManyToManyField(Experiencia)

    def __str__(self):
        return self.nombre_completo