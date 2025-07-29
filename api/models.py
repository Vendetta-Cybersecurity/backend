from django.db import models
from django.contrib.auth.models import AbstractUser
import json

# =============================================
# 1. DEPARTAMENTOS
# =============================================
class Departamento(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    
    id_departamento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'departamentos'
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
    
    def __str__(self):
        return self.nombre

# =============================================
# 2. ROLES
# =============================================
class Rol(models.Model):
    NIVEL_ACCESO_CHOICES = [
        ('basico', 'Básico'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
        ('admin', 'Administrador'),
    ]
    
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    
    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    id_departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, db_column='id_departamento')
    descripcion = models.TextField(blank=True, null=True)
    nivel_acceso = models.CharField(max_length=12, choices=NIVEL_ACCESO_CHOICES, default='basico')
    permisos_sistema = models.JSONField(default=dict)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
    
    def __str__(self):
        return f"{self.nombre} - {self.id_departamento.nombre}"

# =============================================
# 3. EMPLEADOS
# =============================================
class Empleado(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('PP', 'Pasaporte'),
    ]
    
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('suspendido', 'Suspendido'),
    ]
    
    id_empleado = models.AutoField(primary_key=True)
    numero_documento = models.CharField(max_length=20, unique=True)
    tipo_documento = models.CharField(max_length=2, choices=TIPO_DOCUMENTO_CHOICES, default='CC')
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    id_departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, db_column='id_departamento')
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE, db_column='id_rol')
    fecha_ingreso = models.DateField()
    fecha_salida = models.DateField(blank=True, null=True)
    salario = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    foto_perfil = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=12, choices=ESTADO_CHOICES, default='activo')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'empleados'
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"
    
    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

# =============================================
# 4. USUARIOS
# =============================================
class Usuario(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('bloqueado', 'Bloqueado'),
    ]
    
    id_usuario = models.AutoField(primary_key=True)
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, db_column='id_empleado')
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=255)
    ultimo_acceso = models.DateTimeField(blank=True, null=True)
    intentos_fallidos = models.IntegerField(default=0)
    bloqueado = models.BooleanField(default=False)
    fecha_bloqueo = models.DateTimeField(blank=True, null=True)
    token_2fa = models.CharField(max_length=100, blank=True, null=True)
    token_recuperacion = models.CharField(max_length=100, blank=True, null=True)
    fecha_expiracion_token = models.DateTimeField(blank=True, null=True)
    configuracion_usuario = models.JSONField(default=dict)
    estado = models.CharField(max_length=12, choices=ESTADO_CHOICES, default='activo')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.username} - {self.id_empleado.nombre_completo}"

# =============================================
# 5. SESIONES
# =============================================
class Sesion(models.Model):
    id_sesion = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    token_sesion = models.CharField(max_length=255, unique=True)
    ip_origen = models.CharField(max_length=45, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_expiracion = models.DateTimeField()
    activa = models.BooleanField(default=True)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    dispositivo = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = 'sesiones'
        verbose_name = 'Sesión'
        verbose_name_plural = 'Sesiones'
    
    def __str__(self):
        return f"Sesión {self.id_usuario.username} - {self.fecha_inicio}"

# =============================================
# 6. PERFILES_EMPLEADOS
# =============================================
class PerfilEmpleado(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, db_column='id_empleado')
    biografia = models.TextField(blank=True, null=True)
    habilidades = models.JSONField(default=list)
    experiencia_laboral = models.JSONField(default=list)
    educacion = models.JSONField(default=list)
    certificaciones = models.JSONField(default=list)
    idiomas = models.JSONField(default=list)
    redes_sociales = models.JSONField(default=dict)
    preferencias_notificaciones = models.JSONField(default=dict)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'perfiles_empleados'
        verbose_name = 'Perfil de Empleado'
        verbose_name_plural = 'Perfiles de Empleados'
    
    def __str__(self):
        return f"Perfil de {self.id_empleado.nombre_completo}"

# =============================================
# 7. NOTIFICACIONES
# =============================================
class Notificacion(models.Model):
    TIPO_CHOICES = [
        ('info', 'Información'),
        ('warning', 'Advertencia'),
        ('error', 'Error'),
        ('success', 'Éxito'),
    ]
    
    CATEGORIA_CHOICES = [
        ('sistema', 'Sistema'),
        ('seguridad', 'Seguridad'),
        ('trabajo', 'Trabajo'),
        ('personal', 'Personal'),
    ]
    
    id_notificacion = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    titulo = models.CharField(max_length=200)
    mensaje = models.TextField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='info')
    categoria = models.CharField(max_length=12, choices=CATEGORIA_CHOICES, default='sistema')
    leida = models.BooleanField(default=False)
    fecha_lectura = models.DateTimeField(blank=True, null=True)
    url_accion = models.CharField(max_length=255, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_expiracion = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'notificaciones'
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.titulo} - {self.id_usuario.username}"

# =============================================
# 8. ACTIVIDADES_USUARIO
# =============================================
class ActividadUsuario(models.Model):
    id_actividad = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    accion = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    modulo = models.CharField(max_length=50, blank=True, null=True)
    ip_origen = models.CharField(max_length=45, blank=True, null=True)
    datos_adicionales = models.JSONField(default=dict)
    fecha_actividad = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'actividades_usuario'
        verbose_name = 'Actividad de Usuario'
        verbose_name_plural = 'Actividades de Usuario'
        ordering = ['-fecha_actividad']
    
    def __str__(self):
        return f"{self.accion} - {self.id_usuario.username} - {self.fecha_actividad}"

# =============================================
# 9. LOG_SISTEMA
# =============================================
class LogSistema(models.Model):
    NIVEL_CHOICES = [
        ('DEBUG', 'Debug'),
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    ]
    
    id_log = models.AutoField(primary_key=True)
    nivel = models.CharField(max_length=10, choices=NIVEL_CHOICES)
    mensaje = models.TextField()
    modulo = models.CharField(max_length=50, blank=True, null=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, db_column='id_usuario')
    ip_origen = models.CharField(max_length=45, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    datos_contexto = models.JSONField(default=dict)
    fecha_log = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'log_sistema'
        verbose_name = 'Log del Sistema'
        verbose_name_plural = 'Logs del Sistema'
        ordering = ['-fecha_log']
    
    def __str__(self):
        return f"{self.nivel} - {self.mensaje[:50]}... - {self.fecha_log}"
