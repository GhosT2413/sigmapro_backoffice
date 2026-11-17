from core.models import Usuario, Vehiculo, Taller, FichaMantencion, AlertaMantencion, PrediccionIA, Servicio

def dashboard_callback(request, context):
    """
    Inyecta estadísticas y métricas del sistema en el dashboard principal de SIGMAPRO.
    """
    total_usuarios = Usuario.objects.count()
    usuarios_activos = Usuario.objects.filter(activo=True).count()
    total_talleres = Taller.objects.count()
    total_vehiculos = Vehiculo.objects.count()
    total_servicios = Servicio.objects.filter(activo=True).count()
    
    # Mantenciones y alertas
    fichas_en_proceso = FichaMantencion.objects.filter(estado__in=['EN_ESPERA', 'EN_MANTENIMIENTO']).count()
    fichas_finalizadas = FichaMantencion.objects.filter(estado='LISTO').count()
    alertas_pendientes = AlertaMantencion.objects.filter(estado='PENDIENTE').count()
    predicciones_pendientes = PrediccionIA.objects.filter(estado='PENDIENTE').count()
    
    # Actividad reciente
    ultimas_alertas = AlertaMantencion.objects.order_by('-id')[:5]
    ultimas_predicciones = PrediccionIA.objects.order_by('-id')[:5]
    ultimos_usuarios = Usuario.objects.select_related('role').order_by('-id')[:5]

    context.update({
        "stats": {
            "total_usuarios": total_usuarios,
            "usuarios_activos": usuarios_activos,
            "total_talleres": total_talleres,
            "total_vehiculos": total_vehiculos,
            "total_servicios": total_servicios,
            "fichas_en_proceso": fichas_en_proceso,
            "fichas_finalizadas": fichas_finalizadas,
            "alertas_pendientes": alertas_pendientes,
            "predicciones_pendientes": predicciones_pendientes,
        },
        "ultimas_alertas": ultimas_alertas,
        "ultimas_predicciones": ultimas_predicciones,
        "ultimos_usuarios": ultimos_usuarios,
    })
    return context

