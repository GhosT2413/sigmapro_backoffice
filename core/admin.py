from django.contrib import admin
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .forms import UsuarioForm
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


class PasswordEstadoFilter(admin.SimpleListFilter):
    """Filtro «Sin contraseña / Con contraseña» para localizar cuentas que no pueden ingresar."""

    title = "estado de contraseña"
    parameter_name = "password_estado"

    def lookups(self, request, model_admin):
        return [
            ("sin", "Sin contraseña (no pueden ingresar)"),
            ("con", "Con contraseña"),
        ]

    def queryset(self, request, queryset):
        sin = Q(password_hash__isnull=True) | Q(password_hash="")
        if self.value() == "sin":
            return queryset.filter(sin)
        if self.value() == "con":
            return queryset.exclude(sin)
        return queryset


@admin.register(Usuario)
class UsuarioAdmin(ModelAdmin):
    form = UsuarioForm

    list_display = [
        'id',
        'nombre_completo',
        'email',
        'role_badge',
        'telefono',
        'rut',
        'taller',
        'password_estado',
        'status_badge',
        'created_at',
    ]
    list_filter = [PasswordEstadoFilter, 'role', 'activo', 'hasAcceptedTerms', 'created_at']
    search_fields = ['nombre_completo', 'email', 'rut', 'telefono', 'rut_empresa']
    list_select_related = ['role', 'taller']
    list_filter_sheet = True
    list_per_page = 20
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
        ("Información Principal", {
            "fields": (
                "nombre_completo",
                "email",
                "role",
                "taller",
                ("activo", "hasAcceptedTerms"),
            )
        }),
        ("Acceso a la Cuenta (Contraseña)", {
            "description": (
                "Contraseña de ingreso al portal SIGMAPRO. Dejar vacío para no modificarla. "
                "Los usuarios sin contraseña no pueden iniciar sesión."
            ),
            "fields": ("nueva_password",),
        }),
        ("Identificación y Contacto", {
            "fields": (
                ("rut", "telefono"),
                "google_id",
                "foto_perfil_url",
            )
        }),
        ("Documentación: Mecánico Independiente", {
            "classes": ["collapse"],
            "fields": (
                "cedula_frente_url",
                "cedula_reverso_url",
                "certificado_antecedentes_url",
            )
        }),
        ("Documentación Legal: Taller Mecánico", {
            "classes": ["collapse"],
            "fields": (
                ("rut_empresa", "patente_comercial"),
                "representante_legal",
                "comprobante_domicilio_url",
            )
        }),
        ("Auditoría y Registro", {
            "classes": ["collapse"],
            "fields": (("created_at", "updated_at"),),
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

    @display(description="Contraseña")
    def password_estado(self, obj):
        """Estado del acceso y acceso directo para crear/cambiar la contraseña."""
        url = reverse("admin:core_usuario_change", args=[obj.id])
        if not obj.password_hash:
            return format_html(
                '<a href="{}" title="Este usuario no puede iniciar sesión. Haz click para crear su contraseña" '
                'style="color:#f87171;font-weight:600;">⚠ Sin contraseña — crear</a>',
                url,
            )
        return format_html(
            '<a href="{}" title="Haz click para cambiar la contraseña" style="color:#6ee7b7;">● Configurada</a>',
            url,
        )

    def save_model(self, request, obj, form, change):
        """
        Hashea la contraseña ingresada en `nueva_password` con bcrypt (cost 12)
        y la guarda en password_hash, tal cual la espera bcrypt.compare del backend.
        """
        password = form.cleaned_data.get("nueva_password")

        if password:
            obj.password_hash = form.hashear(password)

        super().save_model(request, obj, form, change)

        if password:
            self.message_user(
                request,
                f"Contraseña actualizada para {obj.email}. Ya puede iniciar sesión en el portal.",
                messages.SUCCESS,
            )
        elif not obj.password_hash:
            self.message_user(
                request,
                f"{obj.email} NO tiene contraseña: no podrá iniciar sesión hasta que le definas una "
                "(sección «Acceso a la Cuenta (Contraseña)»).",
                messages.WARNING,
            )

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
        'usuarios_link',
        'status_badge',
        'created_at',
    ]
    list_filter = ['activo', 'created_at']
    search_fields = ['nombre', 'rut_empresa', 'email_contacto', 'telefono', 'representante_legal']
    list_filter_sheet = True

    fieldsets = (
        ("Datos Comerciales", {
            "fields": (
                "nombre",
                ("rut_empresa", "patente_comercial"),
                "representante_legal",
                "activo",
            )
        }),
        ("Ubicación y Contacto", {
            "fields": (
                ("email_contacto", "telefono"),
                "direccion",
                "comprobante_domicilio_url",
            )
        }),
        ("Registro", {
            "classes": ["collapse"],
            "fields": (("created_at", "updated_at"),),
        }),
    )
    readonly_fields = ['created_at', 'updated_at']

    @display(description="Usuarios")
    def usuarios_link(self, obj):
        """
        Atajo a los usuarios de este taller (para allí crear/editar la contraseña).
        Un taller creado sin usuario o sin contraseña no puede iniciar sesión.
        """
        usuarios = obj.usuarios.all()
        total = usuarios.count()
        url_lista = reverse("admin:core_usuario_changelist") + f"?taller__id__exact={obj.id}"

        if total == 0:
            return format_html(
                '<a href="{}" title="Este taller no tiene usuarios: crea uno con rol TALLER para poder ingresar" '
                'style="color:#f87171;font-weight:600;">⚠ Sin usuarios — crear</a>',
                reverse("admin:core_usuario_add"),
            )
        sin_password = sum(1 for u in usuarios if not u.password_hash)
        if sin_password:
            return format_html(
                '<a href="{}" style="color:#f87171;font-weight:600;">{} usuario(s), {} sin contraseña →</a>',
                url_lista,
                total,
                sin_password,
            )
        return format_html('<a href="{}" style="color:#6ee7b7;">{} usuario(s) →</a>', url_lista, total)

    @display(description="Estado", label=True)
    def status_badge(self, obj):
        return ("Activo", "success") if obj.activo else ("Inactivo", "danger")


@admin.register(Cliente)
class ClienteAdmin(ModelAdmin):
    list_display = ['id', 'nombre_completo', 'rut', 'email', 'telefono', 'created_at']
    search_fields = ['nombre_completo', 'rut', 'email', 'telefono']
    list_filter = ['created_at']
    list_filter_sheet = True


@admin.register(Vehiculo)
class VehiculoAdmin(ModelAdmin):
    list_display = [
        'id',
        'patente_badge',
        'marca_modelo',
        'anio',
        'kilometraje_formatted',
        'tipo_uso',
        'status_badge',
        'cliente',
    ]
    list_filter = ['estado', 'tipo_uso', 'marca', 'anio']
    search_fields = ['patente', 'marca', 'modelo', 'vin']
    list_select_related = ['cliente']
    list_filter_sheet = True

    fieldsets = (
        ("Información del Vehículo", {
            "fields": (
                ("patente", "vin"),
                ("marca", "modelo", "anio"),
                "cliente",
            )
        }),
        ("Operatividad y Estado", {
            "fields": (
                ("kilometraje_actual", "tipo_uso"),
                "estado",
            )
        }),
        ("Vencimientos Legales", {
            "fields": (
                "vencimiento_revision_tecnica",
                "vencimiento_soap",
                "vencimiento_permiso_circulacion",
            )
        }),
    )

    @display(description="Patente")
    def patente_badge(self, obj):
        return obj.patente.upper() if obj.patente else "-"

    @display(description="Marca y Modelo")
    def marca_modelo(self, obj):
        return f"{obj.marca} {obj.modelo}"

    @display(description="Kilometraje")
    def kilometraje_formatted(self, obj):
        return f"{obj.kilometraje_actual:,} km".replace(',', '.')

    @display(description="Estado", label={
        "ACTIVO": "success",
        "EN_MANTENIMIENTO": "warning",
        "INACTIVO": "danger",
    })
    def status_badge(self, obj):
        return obj.estado


@admin.register(Servicio)
class ServicioAdmin(ModelAdmin):
    list_display = ['id', 'nombre', 'precio_formatted', 'tiempo_estimado_horas', 'status_badge']
    list_filter = ['activo']
    search_fields = ['nombre', 'descripcion']
    list_filter_sheet = True

    @display(description="Precio Base")
    def precio_formatted(self, obj):
        return f"${obj.precio_base:,.0f} CLP".replace(',', '.')

    @display(description="Estado", label=True)
    def status_badge(self, obj):
        return ("Activo", "success") if obj.activo else ("Inactivo", "danger")


@admin.register(FichaMantencion)
class FichaMantencionAdmin(ModelAdmin):
    list_display = [
        'id',
        'vehiculo_id',
        'taller_id',
        'kilometraje_ingreso',
        'costo_total_formatted',
        'status_badge',
        'fecha_ingreso',
    ]
    list_filter = ['estado', 'fecha_ingreso']
    search_fields = ['descripcion', 'diagnostico', 'trabajo_realizado']
    list_filter_sheet = True

    fieldsets = (
        ("Datos Principales", {
            "fields": (
                ("vehiculo_id", "taller_id", "mecanico_id"),
                "estado",
            )
        }),
        ("Kilometraje y Tiempos", {
            "fields": (
                ("kilometraje_ingreso", "kilometraje_salida"),
                ("fecha_inicio", "fecha_finalizacion"),
            )
        }),
        ("Costos Económicos", {
            "fields": (
                ("valor_arreglo", "costo_repuestos"),
                "costo_total",
            )
        }),
        ("Detalles Técnicos", {
            "fields": (
                "descripcion",
                "diagnostico",
                "trabajo_realizado",
            )
        }),
    )

    @display(description="Costo Total")
    def costo_total_formatted(self, obj):
        return f"${obj.costo_total:,.0f} CLP".replace(',', '.')

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
    list_filter_sheet = True

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
    list_filter_sheet = True

    fieldsets = (
        ("Predicción y Vehículo", {
            "fields": (
                "vehiculo_id",
                "componente",
                "estado",
            )
        }),
        ("Diagnóstico Predictivo de IA", {
            "fields": (
                ("probabilidad", "kilometraje_actual", "kilometraje_recomendado"),
                "diagnostico",
            )
        }),
    )

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
