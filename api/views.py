from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
import json

from .models import (
    Departamento, Rol, Empleado, Usuario, Sesion, 
    PerfilEmpleado, Notificacion, ActividadUsuario, LogSistema
)
from .serializers import (
    DepartamentoSerializer, RolSerializer, EmpleadoSerializer, EmpleadoCreateSerializer,
    UsuarioSerializer, SesionSerializer, PerfilEmpleadoSerializer, 
    NotificacionSerializer, ActividadUsuarioSerializer, LogSistemaSerializer,
    EmpleadoResumenSerializer, DepartamentoConEmpleadosSerializer, 
    UsuarioConPerfilSerializer, NotificacionesUsuarioSerializer,
    EstadisticasDepartamentoSerializer, EstadisticasGeneralesSerializer
)

# =============================================
# VISTAS BÁSICAS DE PRUEBA
# =============================================

@api_view(['GET'])
def empty_json(request):
    """
    Returns an empty JSON object
    """
    return Response({})

@api_view(['GET'])
def api_status(request):
    """
    Returns API status with database connection info
    """
    try:
        # Test database connection
        total_empleados = Empleado.objects.count()
        total_departamentos = Departamento.objects.count()
        
        return Response({
            'status': 'API is running',
            'message': 'Django REST API backend is working',
            'database': 'Connected to MariaDB',
            'stats': {
                'total_empleados': total_empleados,
                'total_departamentos': total_departamentos,
                'timestamp': timezone.now()
            }
        })
    except Exception as e:
        return Response({
            'status': 'API is running',
            'message': 'Django REST API backend is working',
            'database': f'Database connection error: {str(e)}',
            'timestamp': timezone.now()
        }, status=status.HTTP_200_OK)

# =============================================
# VISTAS PARA DEPARTAMENTOS
# =============================================

@api_view(['GET', 'POST'])
def departamentos_list(request):
    """
    GET: Lista todos los departamentos
    POST: Crea un nuevo departamento
    """
    if request.method == 'GET':
        departamentos = Departamento.objects.all()
        serializer = DepartamentoSerializer(departamentos, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'count': len(serializer.data)
        })
    
    elif request.method == 'POST':
        serializer = DepartamentoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Departamento creado exitosamente',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def departamento_detail(request, id_departamento):
    """
    GET: Obtiene un departamento específico
    PUT: Actualiza un departamento
    DELETE: Elimina un departamento
    """
    try:
        departamento = Departamento.objects.get(id_departamento=id_departamento)
    except Departamento.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Departamento no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = DepartamentoConEmpleadosSerializer(departamento)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    elif request.method == 'PUT':
        serializer = DepartamentoSerializer(departamento, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Departamento actualizado exitosamente',
                'data': serializer.data
            })
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        departamento.delete()
        return Response({
            'success': True,
            'message': 'Departamento eliminado exitosamente'
        }, status=status.HTTP_204_NO_CONTENT)

# =============================================
# VISTAS PARA ROLES
# =============================================

@api_view(['GET', 'POST'])
def roles_list(request):
    """
    GET: Lista todos los roles
    POST: Crea un nuevo rol
    """
    if request.method == 'GET':
        roles = Rol.objects.select_related('id_departamento').all()
        serializer = RolSerializer(roles, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'count': len(serializer.data)
        })
    
    elif request.method == 'POST':
        serializer = RolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Rol creado exitosamente',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def roles_por_departamento(request, id_departamento):
    """
    GET: Lista roles de un departamento específico
    """
    roles = Rol.objects.filter(id_departamento=id_departamento, estado='activo')
    serializer = RolSerializer(roles, many=True)
    return Response({
        'success': True,
        'data': serializer.data,
        'count': len(serializer.data)
    })

# =============================================
# VISTAS PARA EMPLEADOS
# =============================================

@api_view(['GET', 'POST'])
def empleados_list(request):
    """
    GET: Lista todos los empleados con filtros opcionales
    POST: Crea un nuevo empleado
    """
    if request.method == 'GET':
        empleados = Empleado.objects.select_related('id_departamento', 'id_rol').all()
        
        # Filtros opcionales
        estado = request.GET.get('estado')
        departamento = request.GET.get('departamento')
        
        if estado:
            empleados = empleados.filter(estado=estado)
        if departamento:
            empleados = empleados.filter(id_departamento=departamento)
        
        serializer = EmpleadoSerializer(empleados, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'count': len(serializer.data)
        })
    
    elif request.method == 'POST':
        serializer = EmpleadoCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Empleado creado exitosamente',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def empleado_detail(request, id_empleado):
    """
    GET: Obtiene un empleado específico
    PUT: Actualiza un empleado
    DELETE: Elimina un empleado (cambiar estado a inactivo)
    """
    try:
        empleado = Empleado.objects.select_related('id_departamento', 'id_rol').get(id_empleado=id_empleado)
    except Empleado.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Empleado no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = EmpleadoSerializer(empleado)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    elif request.method == 'PUT':
        serializer = EmpleadoSerializer(empleado, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Empleado actualizado exitosamente',
                'data': serializer.data
            })
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        empleado.estado = 'inactivo'
        empleado.fecha_salida = timezone.now().date()
        empleado.save()
        return Response({
            'success': True,
            'message': 'Empleado dado de baja exitosamente'
        })

# =============================================
# VISTAS PARA USUARIOS
# =============================================

@api_view(['GET', 'POST'])
def usuarios_list(request):
    """
    GET: Lista todos los usuarios
    POST: Crea un nuevo usuario
    """
    if request.method == 'GET':
        usuarios = Usuario.objects.select_related('id_empleado').all()
        serializer = UsuarioConPerfilSerializer(usuarios, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'count': len(serializer.data)
        })
    
    elif request.method == 'POST':
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Usuario creado exitosamente',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# =============================================
# VISTAS PARA NOTIFICACIONES
# =============================================

@api_view(['GET'])
def notificaciones_usuario(request, id_usuario):
    """
    GET: Lista notificaciones de un usuario específico
    """
    notificaciones = Notificacion.objects.filter(id_usuario=id_usuario).order_by('-fecha_creacion')
    
    # Filtros opcionales
    leida = request.GET.get('leida')
    tipo = request.GET.get('tipo')
    
    if leida is not None:
        notificaciones = notificaciones.filter(leida=leida.lower() == 'true')
    if tipo:
        notificaciones = notificaciones.filter(tipo=tipo)
    
    serializer = NotificacionesUsuarioSerializer(notificaciones, many=True)
    return Response({
        'success': True,
        'data': serializer.data,
        'count': len(serializer.data)
    })

@api_view(['PUT'])
def marcar_notificacion_leida(request, id_notificacion):
    """
    PUT: Marca una notificación como leída
    """
    try:
        notificacion = Notificacion.objects.get(id_notificacion=id_notificacion)
        notificacion.leida = True
        notificacion.fecha_lectura = timezone.now()
        notificacion.save()
        
        return Response({
            'success': True,
            'message': 'Notificación marcada como leída'
        })
    except Notificacion.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Notificación no encontrada'
        }, status=status.HTTP_404_NOT_FOUND)

# =============================================
# VISTAS PARA ESTADÍSTICAS Y REPORTES
# =============================================

@api_view(['GET'])
def estadisticas_generales(request):
    """
    GET: Obtiene estadísticas generales del sistema
    """
    try:
        total_empleados = Empleado.objects.count()
        empleados_activos = Empleado.objects.filter(estado='activo').count()
        total_departamentos = Departamento.objects.filter(estado='activo').count()
        total_roles = Rol.objects.filter(estado='activo').count()
        usuarios_activos = Usuario.objects.filter(estado='activo').count()
        sesiones_activas = Sesion.objects.filter(activa=True).count()
        notificaciones_no_leidas = Notificacion.objects.filter(leida=False).count()
        
        data = {
            'total_empleados': total_empleados,
            'empleados_activos': empleados_activos,
            'total_departamentos': total_departamentos,
            'total_roles': total_roles,
            'usuarios_activos': usuarios_activos,
            'sesiones_activas': sesiones_activas,
            'notificaciones_no_leidas': notificaciones_no_leidas
        }
        
        serializer = EstadisticasGeneralesSerializer(data)
        return Response({
            'success': True,
            'data': serializer.data,
            'timestamp': timezone.now()
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error al obtener estadísticas: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def estadisticas_departamentos(request):
    """
    GET: Obtiene estadísticas por departamento
    """
    try:
        departamentos = Departamento.objects.annotate(
            total_empleados=Count('empleado'),
            empleados_activos=Count('empleado', filter=Q(empleado__estado='activo')),
            empleados_inactivos=Count('empleado', filter=Q(empleado__estado='inactivo')),
            empleados_suspendidos=Count('empleado', filter=Q(empleado__estado='suspendido'))
        ).values(
            'id_departamento', 'nombre', 'total_empleados', 
            'empleados_activos', 'empleados_inactivos', 'empleados_suspendidos'
        )
        
        serializer = EstadisticasDepartamentoSerializer(departamentos, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'count': len(serializer.data)
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error al obtener estadísticas de departamentos: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# =============================================
# VISTAS PARA BÚSQUEDA
# =============================================

@api_view(['GET'])
def buscar_empleados(request):
    """
    GET: Busca empleados por nombre, email o documento
    """
    query = request.GET.get('q', '')
    if not query:
        return Response({
            'success': False,
            'message': 'Parámetro de búsqueda requerido (q)'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    empleados = Empleado.objects.filter(
        Q(nombres__icontains=query) |
        Q(apellidos__icontains=query) |
        Q(email__icontains=query) |
        Q(numero_documento__icontains=query)
    ).select_related('id_departamento', 'id_rol')[:20]  # Limitar a 20 resultados
    
    serializer = EmpleadoResumenSerializer(empleados, many=True)
    return Response({
        'success': True,
        'data': serializer.data,
        'count': len(serializer.data),
        'query': query
    })

# =============================================
# VISTA PARA CONFIGURACIÓN DE VM
# =============================================

@api_view(['GET'])
def configuracion_vm(request):
    """
    GET: Información para configurar la conexión en VM
    """
    return Response({
        'success': True,
        'message': 'Configuración para despliegue en VM',
        'instructions': {
            'database': {
                'host': 'Cambiar localhost por la IP de la VM de base de datos',
                'settings_file': 'mybackend/settings.py',
                'variable': 'DATABASES[\'default\'][\'HOST\']'
            },
            'allowed_hosts': {
                'description': 'Agregar las IPs de las VMs a ALLOWED_HOSTS',
                'settings_file': 'mybackend/settings.py',
                'variable': 'ALLOWED_HOSTS'
            },
            'cors': {
                'description': 'Configurar CORS para permitir requests entre VMs',
                'settings_file': 'mybackend/settings.py',
                'variable': 'CORS_ALLOWED_ORIGINS'
            }
        },
        'current_config': {
            'debug': True,
            'database_host': 'localhost',
            'allowed_hosts': ['localhost', '127.0.0.1', '0.0.0.0']
        }
    })