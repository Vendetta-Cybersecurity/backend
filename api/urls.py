from django.urls import path
from . import views

urlpatterns = [
    # Rutas básicas de prueba
    path('empty/', views.empty_json, name='empty-json'),
    path('status/', views.api_status, name='api-status'),
    path('config-vm/', views.configuracion_vm, name='config-vm'),
    
    # Rutas para Departamentos
    path('departamentos/', views.departamentos_list, name='departamentos-list'),
    path('departamentos/<int:id_departamento>/', views.departamento_detail, name='departamento-detail'),
    
    # Rutas para Roles
    path('roles/', views.roles_list, name='roles-list'),
    path('roles/departamento/<int:id_departamento>/', views.roles_por_departamento, name='roles-por-departamento'),
    
    # Rutas para Empleados
    path('empleados/', views.empleados_list, name='empleados-list'),
    path('empleados/<int:id_empleado>/', views.empleado_detail, name='empleado-detail'),
    path('empleados/buscar/', views.buscar_empleados, name='buscar-empleados'),
    
    # Rutas para Usuarios
    path('usuarios/', views.usuarios_list, name='usuarios-list'),
    
    # Rutas para Notificaciones
    path('notificaciones/usuario/<int:id_usuario>/', views.notificaciones_usuario, name='notificaciones-usuario'),
    path('notificaciones/<int:id_notificacion>/marcar-leida/', views.marcar_notificacion_leida, name='marcar-notificacion-leida'),
    
    # Rutas para Estadísticas y Reportes
    path('estadisticas/generales/', views.estadisticas_generales, name='estadisticas-generales'),
    path('estadisticas/departamentos/', views.estadisticas_departamentos, name='estadisticas-departamentos'),
]