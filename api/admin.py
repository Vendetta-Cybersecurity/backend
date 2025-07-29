from django.contrib import admin
from .models import (
    Departamento, Rol, Empleado, Usuario, Sesion, 
    PerfilEmpleado, Notificacion, ActividadUsuario, LogSistema
)

# =============================================
# ADMIN PARA DEPARTAMENTOS
# =============================================
@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['id_departamento', 'nombre', 'estado', 'fecha_creacion']
    list_filter = ['estado', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    ordering = ['nombre']

# =============================================
# ADMIN PARA ROLES
# =============================================
@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ['id_rol', 'nombre', 'id_departamento', 'nivel_acceso', 'estado']
    list_filter = ['nivel_acceso', 'estado', 'id_departamento']
    search_fields = ['nombre', 'descripcion']
    ordering = ['id_departamento', 'nombre']

# =============================================
# ADMIN PARA EMPLEADOS
# =============================================
@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['id_empleado', 'numero_documento', 'nombre_completo', 'email', 'id_departamento', 'estado']
    list_filter = ['estado', 'id_departamento', 'id_rol', 'fecha_ingreso']
    search_fields = ['nombres', 'apellidos', 'email', 'numero_documento']
    ordering = ['apellidos', 'nombres']
    date_hierarchy = 'fecha_ingreso'
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('numero_documento', 'tipo_documento', 'nombres', 'apellidos', 'email', 'telefono', 'fecha_nacimiento')
        }),
        ('Información Laboral', {
            'fields': ('id_departamento', 'id_rol', 'fecha_ingreso', 'fecha_salida', 'salario', 'estado')
        }),
        ('Ubicación', {
            'fields': ('direccion', 'ciudad')
        }),
        ('Otros', {
            'fields': ('foto_perfil',)
        })
    )

# =============================================
# ADMIN PARA USUARIOS
# =============================================
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['id_usuario', 'username', 'id_empleado', 'estado', 'ultimo_acceso', 'bloqueado']
    list_filter = ['estado', 'bloqueado', 'fecha_creacion']
    search_fields = ['username', 'id_empleado__nombres', 'id_empleado__apellidos']
    ordering = ['username']
    
    fieldsets = (
        ('Información de Acceso', {
            'fields': ('id_empleado', 'username', 'password_hash', 'estado')
        }),
        ('Seguridad', {
            'fields': ('bloqueado', 'intentos_fallidos', 'fecha_bloqueo', 'token_2fa')
        }),
        ('Recuperación', {
            'fields': ('token_recuperacion', 'fecha_expiracion_token')
        }),
        ('Configuración', {
            'fields': ('configuracion_usuario',)
        })
    )

# =============================================
# ADMIN PARA SESIONES
# =============================================
@admin.register(Sesion)
class SesionAdmin(admin.ModelAdmin):
    list_display = ['id_sesion', 'id_usuario', 'activa', 'fecha_inicio', 'fecha_expiracion', 'ip_origen']
    list_filter = ['activa', 'fecha_inicio', 'fecha_expiracion']
    search_fields = ['id_usuario__username', 'ip_origen', 'ubicacion']
    ordering = ['-fecha_inicio']
    date_hierarchy = 'fecha_inicio'

# =============================================
# ADMIN PARA PERFILES DE EMPLEADOS
# =============================================
@admin.register(PerfilEmpleado)
class PerfilEmpleadoAdmin(admin.ModelAdmin):
    list_display = ['id_perfil', 'id_empleado', 'fecha_actualizacion']
    search_fields = ['id_empleado__nombres', 'id_empleado__apellidos', 'biografia']
    ordering = ['-fecha_actualizacion']

# =============================================
# ADMIN PARA NOTIFICACIONES
# =============================================
@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ['id_notificacion', 'titulo', 'id_usuario', 'tipo', 'categoria', 'leida', 'fecha_creacion']
    list_filter = ['tipo', 'categoria', 'leida', 'fecha_creacion']
    search_fields = ['titulo', 'mensaje', 'id_usuario__username']
    ordering = ['-fecha_creacion']
    date_hierarchy = 'fecha_creacion'

# =============================================
# ADMIN PARA ACTIVIDADES DE USUARIO
# =============================================
@admin.register(ActividadUsuario)
class ActividadUsuarioAdmin(admin.ModelAdmin):
    list_display = ['id_actividad', 'id_usuario', 'accion', 'modulo', 'fecha_actividad', 'ip_origen']
    list_filter = ['accion', 'modulo', 'fecha_actividad']
    search_fields = ['id_usuario__username', 'accion', 'descripcion']
    ordering = ['-fecha_actividad']
    date_hierarchy = 'fecha_actividad'

# =============================================
# ADMIN PARA LOG DEL SISTEMA
# =============================================
@admin.register(LogSistema)
class LogSistemaAdmin(admin.ModelAdmin):
    list_display = ['id_log', 'nivel', 'mensaje_corto', 'modulo', 'id_usuario', 'fecha_log']
    list_filter = ['nivel', 'modulo', 'fecha_log']
    search_fields = ['mensaje', 'modulo', 'id_usuario__username']
    ordering = ['-fecha_log']
    date_hierarchy = 'fecha_log'
    
    def mensaje_corto(self, obj):
        return obj.mensaje[:50] + '...' if len(obj.mensaje) > 50 else obj.mensaje
    mensaje_corto.short_description = 'Mensaje'
