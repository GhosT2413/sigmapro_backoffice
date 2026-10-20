from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import (
    Role,
    Usuario,
    Taller,
    Cliente,
    Vehiculo,
    Servicio,
    FichaMantencion,
    AlertaMantencion,
    PrediccionIA,
)

@admin.register(Role)
class RoleAdmin(ModelAdmin):
    list_display = ['id', 'nombre', 'descripcion', 'status_badge']
    list_filter = ['activo']
    search_fields = ['nombre', 'descripcion']
    ordering = ['id']

    @display(description="Estado", label=True)
    def status_badge(self, obj):
        return ("Activo", "success") if obj.activo else ("Inactivo", "danger")


@admin.register(Usuario)
class UsuarioAdmin(ModelAdmin):
    list_display = [
        'id',
        'nombre_completo',
        'email',
        'role',
        'telefono',
        'rut',
        'taller',
        'activo',
        'created_at',
    ]
    list_filter = ['role', 'activo', 'hasAcceptedTerms', 'created_at']
    search_fields = ['nombre_completo', 'email', 'rut', 'telefono', 'rut_empresa']
    list_select_related = ['role', 'taller']
    list_editable = ['role', 'activo']
    readonly_fields = ['created_at', 'updated_at']
    actions = [
        'asignar_rol_cliente',
        'asignar_rol_taller',
        'asignar_rol_mecanico_independiente',
        'asignar_rol_mecanico',
        'asignar_rol_recepcionista',
        'asignar_rol_administrador',
    ]

    fieldsets = (
        ("Datos Principales", {
            "fields": (
                "nombre_completo",
                "email",
                "role",
                "taller",
                "activo",
                "hasAcceptedTerms",
            )
        }),
        ("Identificación y Contacto", {
            "fields": (
                "rut",
                "telefono",
                "fecha_nacimiento",
                "google_id",
                "foto_perfil_url",
            )
        }),
        ("Mecánico Independiente (Documentación)", {
            "classes": ["collapse"],
            "fields": (
                "cedula_frente_url",
                "cedula_reverso_url",
                "certificado_antecedentes_url",
            )
        }),
        ("Taller Mecánico (Documentación Legal)", {
            "classes": ["collapse"],
            "fields": (
                "rut_empresa",
                "patente_comercial",
                "representante_legal",
                "comprobante_domicilio_url",
            )
        }),
        ("Auditoría", {
            "fields": ("created_at", "updated_at"),
        }),
    )

    @display(description="Rol", label={
        "ADMINISTRADOR": "danger",
        "TALLER": "warning",
        "MECANICO_INDEPENDIENTE": "info",
        "MECANICO": "primary",
        "RECEPCIONISTA": "secondary",
        "CLIENTE": "success",
    })
    def role_badge(self, obj):
        if obj.role:
            return obj.role.nombre
        return "Sin Rol"

    @display(description="Estado", label=True)
    def status_badge(self, obj):
        return ("Activo", "success") if obj.activo else ("Inactivo", "danger")

    @admin.action(description="Asignar rol: CLIENTE (ID 1)")
    def asignar_rol_cliente(self, request, queryset):
        rol = Role.objects.filter(id=1).first()
        updated = queryset.update(role=rol)
        self.message_user(request, f"Se actualizó a rol CLIENTE en {updated} usuario(s).")

    @admin.action(description="Asignar rol: MECÁNICO INDEPENDIENTE (ID 2)")
    def asignar_rol_mecanico_independiente(self, request, queryset):
        rol = Role.objects.filter(id=2).first()
        updated = queryset.update(role=rol)
        self.message_user(request, f"Se actualizó a rol MECÁNICO INDEPENDIENTE en {updated} usuario(s).")

    @admin.action(description="Asignar rol: TALLER (ID 3)")
    def asignar_rol_taller(self, request, queryset):
        rol = Role.objects.filter(id=3).first()
        updated = queryset.update(role=rol)
        self.message_user(request, f"Se actualizó a rol TALLER en {updated} usuario(s).")

    @admin.action(description="Asignar rol: ADMINISTRADOR (ID 4)")
    def asignar_rol_administrador(self, request, queryset):
        rol = Role.objects.filter(id=4).first()
        updated = queryset.update(role=rol)
        self.message_user(request, f"Se actualizó a rol ADMINISTRADOR en {updated} usuario(s).")

    @admin.action(description="Asignar rol: MECÁNICO (ID 5)")
    def asignar_rol_mecanico(self, request, queryset):
        rol = Role.objects.filter(id=5).first()
        updated = queryset.update(role=rol)
        self.message_user(request, f"Se actualizó a rol MECÁNICO en {updated} usuario(s).")

    @admin.action(description="Asignar rol: RECEPCIONISTA (ID 6)")
    def asignar_rol_recepcionista(self, request, queryset):
        rol = Role.objects.filter(id=6).first()
        updated = queryset.update(role=rol)
        self.message_user(request, f"Se actualizó a rol RECEPCIONISTA en {updated} usuario(s).")


@admin.register(Taller)
class TallerAdmin(ModelAdmin):
    list_display = [
        'id',
        'nombre',
        'rut_empresa',
        'email_contacto',
        'telefono',
        'status_badge',
        'created_at',
    ]
    list_filter = ['activo', 'created_at']
    search_fields = ['nombre', 'rut_empresa', 'email_contacto', 'telefono', 'representante_legal']

    @display(description="Estado", label=True)
    def status_badge(self, obj):
        return ("Activo", "success") if obj.activo else ("Inactivo", "danger")


@admin.register(Cliente)
class ClienteAdmin(ModelAdmin):
    list_display = ['id', 'nombre_completo', 'rut', 'email', 'telefono', 'created_at']
    search_fields = ['nombre_completo', 'rut', 'email', 'telefono']
    list_filter = ['created_at']


@admin.register(Vehiculo)
class VehiculoAdmin(ModelAdmin):
    list_display = [
        'id',
        'patente',
        'marca',
        'modelo',
        'anio',
        'kilometraje_actual',
        'tipo_uso',
        'status_badge',
        'cliente',
    ]
    list_filter = ['estado', 'tipo_uso', 'marca', 'anio']
    search_fields = ['patente', 'marca', 'modelo', 'vin']
    list_select_related = ['cliente']

    @display(description="Estado", label={
        "ACTIVO": "success",
        "EN_MANTENIMIENTO": "warning",
        "INACTIVO": "danger",
    })
    def status_badge(self, obj):
        return obj.estado


@admin.register(Servicio)
class ServicioAdmin(ModelAdmin):
    list_display = ['id', 'nombre', 'precio_base', 'tiempo_estimado_horas', 'status_badge']
    list_filter = ['activo']
    search_fields = ['nombre', 'descripcion']

    @display(description="Estado", label=True)
    def status_badge(self, obj):
        return ("Activo", "success") if obj.activo else ("Inactivo", "danger")


@admin.register(FichaMantencion)
class FichaMantencionAdmin(ModelAdmin):
    list_display = [
        'id',
        'vehiculo_id',
        'taller_id',
        'mecanico_id',
        'kilometraje_ingreso',
        'costo_total',
        'status_badge',
        'fecha_ingreso',
    ]
    list_filter = ['estado', 'fecha_ingreso']
    search_fields = ['descripcion', 'diagnostico', 'trabajo_realizado']

    @display(description="Estado", label={
        "EN_ESPERA": "info",
        "EN_MANTENIMIENTO": "warning",
        "LISTO": "success",
        "CANCELADO": "danger",
    })
    def status_badge(self, obj):
        return obj.estado


@admin.register(AlertaMantencion)
class AlertaMantencionAdmin(ModelAdmin):
    list_display = [
        'id',
        'vehiculo_id',
        'tipo',
        'descripcion',
        'kilometraje_objetivo',
        'fecha_objetivo',
        'status_badge',
    ]
    list_filter = ['estado', 'tipo', 'fecha_objetivo']
    search_fields = ['tipo', 'descripcion']

    @display(description="Estado", label={
        "PENDIENTE": "warning",
        "ATENDIDA": "success",
        "CANCELADA": "danger",
    })
    def status_badge(self, obj):
        return obj.estado


@admin.register(PrediccionIA)
class PrediccionIAAdmin(ModelAdmin):
    list_display = [
        'id',
        'vehiculo_id',
        'componente',
        'probabilidad_pct',
        'kilometraje_recomendado',
        'status_badge',
        'fecha_prediccion',
    ]
    list_filter = ['estado', 'componente']
    search_fields = ['componente', 'diagnostico']

    @display(description="Probabilidad")
    def probabilidad_pct(self, obj):
        if obj.probabilidad is not None:
            return f"{obj.probabilidad}%"
        return "-"

    @display(description="Estado", label={
        "PENDIENTE": "warning",
        "REVISADA": "info",
        "ATENDIDA": "success",
    })
    def status_badge(self, obj):
        return obj.estado
