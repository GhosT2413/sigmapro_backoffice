from django.db import models

class Role(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        ordering = ['id']

    def __str__(self):
        return f"{self.nombre} ({self.id})"


class Taller(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    rut_empresa = models.CharField(max_length=30, unique=True)
    patente_comercial = models.CharField(max_length=20, blank=True, null=True)
    comprobante_domicilio_url = models.TextField(blank=True, null=True)
    representante_legal = models.CharField(max_length=200, blank=True, null=True)
    email_contacto = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'talleres'
        verbose_name = 'Taller'
        verbose_name_plural = 'Talleres'

    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_completo = models.CharField(max_length=200)
    email = models.CharField(max_length=150, unique=True)
    password_hash = models.CharField(max_length=255, blank=True, null=True)
    google_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    rut = models.CharField(max_length=20, blank=True, null=True)
    activo = models.BooleanField(default=True)
    hasAcceptedTerms = models.BooleanField(default=False, db_column='hasAcceptedTerms')
    fecha_nacimiento = models.DateField(blank=True, null=True)
    foto_perfil_url = models.TextField(blank=True, null=True)
    cedula_frente_url = models.TextField(blank=True, null=True)
    cedula_reverso_url = models.TextField(blank=True, null=True)
    certificado_antecedentes_url = models.TextField(blank=True, null=True)
    rut_empresa = models.CharField(max_length=30, blank=True, null=True)
    patente_comercial = models.CharField(max_length=20, blank=True, null=True)
    comprobante_domicilio_url = models.TextField(blank=True, null=True)
    representante_legal = models.CharField(max_length=200, blank=True, null=True)
    taller = models.ForeignKey(Taller, on_delete=models.SET_NULL, db_column='taller_id', blank=True, null=True, related_name='usuarios')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, db_column='role_id', blank=True, null=True, related_name='usuarios')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.nombre_completo} ({self.email})"


class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    usuario_id = models.PositiveIntegerField(blank=True, null=True)
    empresa_id = models.PositiveIntegerField(blank=True, null=True)
    nombre_completo = models.CharField(max_length=200)
    rut = models.CharField(max_length=20, blank=True, null=True, unique=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nombre_completo


class Vehiculo(models.Model):
    TIPO_USO_CHOICES = [
        ('DIARIO', 'Diario'),
        ('CARRERA', 'Carrera'),
        ('TUNING', 'Tuning'),
        ('EXHIBICION', 'Exhibición'),
    ]
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('EN_MANTENIMIENTO', 'En Mantenimiento'),
        ('INACTIVO', 'Inactivo'),
    ]

    id = models.AutoField(primary_key=True)
    empresa_id = models.PositiveIntegerField(blank=True, null=True)
    patente = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    anio = models.IntegerField(blank=True, null=True, db_column='anio')
    vin = models.CharField(max_length=50, blank=True, null=True)
    kilometraje_actual = models.PositiveIntegerField(default=0)
    tipo_uso = models.CharField(max_length=20, choices=TIPO_USO_CHOICES, default='DIARIO')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVO')
    vencimiento_revision_tecnica = models.DateField(blank=True, null=True)
    vencimiento_soap = models.DateField(blank=True, null=True)
    vencimiento_permiso_circulacion = models.DateField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, db_column='cliente_id', blank=True, null=True, related_name='vehiculos')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'vehiculos'
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'

    def __str__(self):
        return f"{self.patente} - {self.marca} {self.modelo}"


class Servicio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    tiempo_estimado_horas = models.DecimalField(max_digits=6, decimal_places=2, default=1.00)
    precio_base = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'servicios'
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    def __str__(self):
        return self.nombre


class FichaMantencion(models.Model):
    ESTADO_CHOICES = [
        ('EN_ESPERA', 'En Espera'),
        ('EN_MANTENIMIENTO', 'En Mantenimiento'),
        ('LISTO', 'Listo'),
        ('CANCELADO', 'Cancelado'),
    ]

    id = models.AutoField(primary_key=True)
    vehiculo_id = models.PositiveIntegerField()
    taller_id = models.PositiveIntegerField(blank=True, null=True)
    mecanico_id = models.PositiveIntegerField(blank=True, null=True)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_finalizacion = models.DateTimeField(blank=True, null=True)
    kilometraje_ingreso = models.PositiveIntegerField()
    kilometraje_salida = models.PositiveIntegerField(blank=True, null=True)
    valor_arreglo = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    costo_repuestos = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    costo_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    descripcion = models.TextField(blank=True, null=True)
    diagnostico = models.TextField(blank=True, null=True)
    trabajo_realizado = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='EN_ESPERA')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'fichas_mantencion'
        verbose_name = 'Ficha de Mantención'
        verbose_name_plural = 'Fichas de Mantención'

    def __str__(self):
        return f"Ficha #{self.id} (Vehículo: {self.vehiculo_id})"


class AlertaMantencion(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('ATENDIDA', 'Atendida'),
        ('CANCELADA', 'Cancelada'),
    ]

    id = models.AutoField(primary_key=True)
    vehiculo_id = models.PositiveIntegerField()
    tipo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255)
    kilometraje_objetivo = models.PositiveIntegerField(blank=True, null=True)
    fecha_objetivo = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'alertas_mantencion'
        verbose_name = 'Alerta de Mantención'
        verbose_name_plural = 'Alertas de Mantención'

    def __str__(self):
        return f"Alerta #{self.id} - {self.tipo}"


class PrediccionIA(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('REVISADA', 'Revisada'),
        ('ATENDIDA', 'Atendida'),
    ]

    id = models.AutoField(primary_key=True)
    vehiculo_id = models.PositiveIntegerField()
    fecha_prediccion = models.DateTimeField(auto_now_add=True)
    componente = models.CharField(max_length=150, blank=True, null=True)
    diagnostico = models.TextField(blank=True, null=True)
    kilometraje_actual = models.PositiveIntegerField(blank=True, null=True)
    kilometraje_recomendado = models.PositiveIntegerField(blank=True, null=True)
    probabilidad = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')

    class Meta:
        managed = False
        db_table = 'predicciones_ia'
        verbose_name = 'Predicción IA'
        verbose_name_plural = 'Predicciones IA'

    def __str__(self):
        return f"Predicción #{self.id} - {self.componente or 'General'}"
