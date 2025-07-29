"""
Script para poblar la base de datos SQLite con datos iniciales
Ejecutar con: python populate_db.py
"""

import os
import django
import sys

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mybackend.settings')
django.setup()

from api.models import Departamento, Rol

def populate_database():
    print("🚀 Poblando base de datos con datos iniciales...")
    
    # Crear departamentos
    departamentos_data = [
        {
            'nombre': 'Administración',
            'descripcion': 'Gestión financiera, recursos humanos y jurídica',
            'estado': 'activo'
        },
        {
            'nombre': 'IT',
            'descripcion': 'Tecnología de la información y sistemas',
            'estado': 'activo'
        },
        {
            'nombre': 'Operaciones',
            'descripcion': 'Instalación, mantenimiento y monitoreo de proyectos',
            'estado': 'activo'
        }
    ]
    
    print("📁 Creando departamentos...")
    for dept_data in departamentos_data:
        dept, created = Departamento.objects.get_or_create(
            nombre=dept_data['nombre'],
            defaults=dept_data
        )
        if created:
            print(f"  ✅ Creado: {dept.nombre}")
        else:
            print(f"  ℹ️  Ya existe: {dept.nombre}")
    
    # Crear roles
    roles_data = [
        {
            'nombre': 'CEO - Gerente General',
            'id_departamento': Departamento.objects.get(nombre='Administración'),
            'descripcion': 'Dirección estratégica y representación legal',
            'nivel_acceso': 'admin',
            'permisos_sistema': {
                "dashboard": True,
                "usuarios": True,
                "reportes": True,
                "configuracion": True
            }
        },
        {
            'nombre': 'Gerencia Jurídica',
            'id_departamento': Departamento.objects.get(nombre='Administración'),
            'descripcion': 'Contratos y cumplimiento regulatorio',
            'nivel_acceso': 'avanzado',
            'permisos_sistema': {
                "dashboard": True,
                "contratos": True,
                "reportes": True
            }
        },
        {
            'nombre': 'Recursos Humanos',
            'id_departamento': Departamento.objects.get(nombre='Administración'),
            'descripcion': 'Gestión de personal y capacitación',
            'nivel_acceso': 'intermedio',
            'permisos_sistema': {
                "dashboard": True,
                "empleados": True,
                "capacitacion": True
            }
        },
        {
            'nombre': 'CISO',
            'id_departamento': Departamento.objects.get(nombre='IT'),
            'descripcion': 'Seguridad de la información y ciberseguridad',
            'nivel_acceso': 'admin',
            'permisos_sistema': {
                "dashboard": True,
                "seguridad": True,
                "logs": True,
                "usuarios": True
            }
        },
        {
            'nombre': 'Desarrollador',
            'id_departamento': Departamento.objects.get(nombre='IT'),
            'descripcion': 'Desarrollo y mantenimiento de aplicaciones',
            'nivel_acceso': 'avanzado',
            'permisos_sistema': {
                "dashboard": True,
                "desarrollo": True,
                "logs": True
            }
        },
        {
            'nombre': 'Administrador de Sistemas',
            'id_departamento': Departamento.objects.get(nombre='IT'),
            'descripcion': 'Gestión de infraestructura tecnológica',
            'nivel_acceso': 'avanzado',
            'permisos_sistema': {
                "dashboard": True,
                "sistemas": True,
                "monitoreo": True
            }
        },
        {
            'nombre': 'Ingeniero de Proyectos',
            'id_departamento': Departamento.objects.get(nombre='Operaciones'),
            'descripcion': 'Diseño y supervisión técnica de proyectos',
            'nivel_acceso': 'avanzado',
            'permisos_sistema': {
                "dashboard": True,
                "proyectos": True,
                "reportes": True
            }
        },
        {
            'nombre': 'Técnico de Campo',
            'id_departamento': Departamento.objects.get(nombre='Operaciones'),
            'descripcion': 'Instalación y mantenimiento en campo',
            'nivel_acceso': 'basico',
            'permisos_sistema': {
                "dashboard": True,
                "mantenimiento": True
            }
        }
    ]
    
    print("👤 Creando roles...")
    for rol_data in roles_data:
        rol, created = Rol.objects.get_or_create(
            nombre=rol_data['nombre'],
            id_departamento=rol_data['id_departamento'],
            defaults=rol_data
        )
        if created:
            print(f"  ✅ Creado: {rol.nombre}")
        else:
            print(f"  ℹ️  Ya existe: {rol.nombre}")
    
    print("\n🎉 ¡Base de datos poblada exitosamente!")
    print(f"📊 Total departamentos: {Departamento.objects.count()}")
    print(f"👥 Total roles: {Rol.objects.count()}")
    print("\n🚀 Ahora puedes ejecutar: python manage.py runserver")

if __name__ == '__main__':
    populate_database()
