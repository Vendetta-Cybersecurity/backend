from rest_framework import serializers
from .models import (
    Departamento, Rol, Empleado, Usuario, Sesion, 
    PerfilEmpleado, Notificacion, ActividadUsuario, LogSistema
)

# =============================================
# SERIALIZERS BÁSICOS
# =============================================

class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'

class RolSerializer(serializers.ModelSerializer):
    departamento_nombre = serializers.CharField(source='id_departamento.nombre', read_only=True)
    
    class Meta:
        model = Rol
        fields = '__all__'

class EmpleadoSerializer(serializers.ModelSerializer):
    departamento_nombre = serializers.CharField(source='id_departamento.nombre', read_only=True)
    rol_nombre = serializers.CharField(source='id_rol.nombre', read_only=True)
    nombre_completo = serializers.CharField(read_only=True)
    
    class Meta:
        model = Empleado
        fields = '__all__'

class EmpleadoCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating employees without readonly fields"""
    class Meta:
        model = Empleado
        exclude = ['fecha_creacion', 'fecha_modificacion']

class UsuarioSerializer(serializers.ModelSerializer):
    empleado_nombre = serializers.CharField(source='id_empleado.nombre_completo', read_only=True)
    empleado_email = serializers.EmailField(source='id_empleado.email', read_only=True)
    
    class Meta:
        model = Usuario
        fields = '__all__'
        extra_kwargs = {
            'password_hash': {'write_only': True}
        }

class SesionSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='id_usuario.username', read_only=True)
    
    class Meta:
        model = Sesion
        fields = '__all__'

class PerfilEmpleadoSerializer(serializers.ModelSerializer):
    empleado_nombre = serializers.CharField(source='id_empleado.nombre_completo', read_only=True)
    
    class Meta:
        model = PerfilEmpleado
        fields = '__all__'

class NotificacionSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='id_usuario.username', read_only=True)
    
    class Meta:
        model = Notificacion
        fields = '__all__'

class ActividadUsuarioSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='id_usuario.username', read_only=True)
    
    class Meta:
        model = ActividadUsuario
        fields = '__all__'

class LogSistemaSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='id_usuario.username', read_only=True)
    
    class Meta:
        model = LogSistema
        fields = '__all__'

# =============================================
# SERIALIZERS ESPECÍFICOS PARA CASOS DE USO
# =============================================

class EmpleadoResumenSerializer(serializers.ModelSerializer):
    """Serializer con información resumida del empleado"""
    departamento_nombre = serializers.CharField(source='id_departamento.nombre', read_only=True)
    rol_nombre = serializers.CharField(source='id_rol.nombre', read_only=True)
    nombre_completo = serializers.CharField(read_only=True)
    
    class Meta:
        model = Empleado
        fields = [
            'id_empleado', 'numero_documento', 'nombre_completo', 
            'email', 'telefono', 'departamento_nombre', 'rol_nombre', 
            'fecha_ingreso', 'estado'
        ]

class DepartamentoConEmpleadosSerializer(serializers.ModelSerializer):
    """Serializer que incluye empleados del departamento"""
    empleados = EmpleadoResumenSerializer(source='empleado_set', many=True, read_only=True)
    total_empleados = serializers.SerializerMethodField()
    
    class Meta:
        model = Departamento
        fields = '__all__'
    
    def get_total_empleados(self, obj):
        return obj.empleado_set.filter(estado='activo').count()

class UsuarioConPerfilSerializer(serializers.ModelSerializer):
    """Serializer que incluye información del empleado y perfil"""
    empleado = EmpleadoSerializer(source='id_empleado', read_only=True)
    
    class Meta:
        model = Usuario
        fields = ['id_usuario', 'username', 'ultimo_acceso', 'estado', 'empleado']

class NotificacionesUsuarioSerializer(serializers.ModelSerializer):
    """Serializer para notificaciones de un usuario específico"""
    class Meta:
        model = Notificacion
        fields = [
            'id_notificacion', 'titulo', 'mensaje', 'tipo', 
            'categoria', 'leida', 'fecha_creacion', 'url_accion'
        ]

# =============================================
# SERIALIZERS PARA ESTADÍSTICAS Y REPORTES
# =============================================

class EstadisticasDepartamentoSerializer(serializers.Serializer):
    """Serializer para estadísticas por departamento"""
    id_departamento = serializers.IntegerField()
    nombre = serializers.CharField()
    total_empleados = serializers.IntegerField()
    empleados_activos = serializers.IntegerField()
    empleados_inactivos = serializers.IntegerField()
    empleados_suspendidos = serializers.IntegerField()

class EstadisticasGeneralesSerializer(serializers.Serializer):
    """Serializer para estadísticas generales del sistema"""
    total_empleados = serializers.IntegerField()
    empleados_activos = serializers.IntegerField()
    total_departamentos = serializers.IntegerField()
    total_roles = serializers.IntegerField()
    usuarios_activos = serializers.IntegerField()
    sesiones_activas = serializers.IntegerField()
    notificaciones_no_leidas = serializers.IntegerField()
