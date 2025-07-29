# Guía de Configuración para Despliegue en VM

## 1. Configuración de Base de Datos

### Cambiar la configuración en `mybackend/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'figger_energy',
        'USER': 'tu_usuario_mariadb',  # Cambiar por tu usuario
        'PASSWORD': 'tu_password_mariadb',  # Cambiar por tu password
        'HOST': 'IP_DE_TU_VM_BD',  # Cambiar por la IP de la VM donde está la BD
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}
```

## 2. Configuración de Hosts Permitidos

### Agregar las IPs de tus VMs a `ALLOWED_HOSTS`:

```python
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    'IP_DE_TU_VM_BACKEND',    # IP donde estará el backend
    'IP_DE_TU_VM_FRONTEND',   # IP donde estará el frontend
    'IP_DE_TU_VM_BD',         # IP donde está la base de datos
]
```

## 3. Configuración CORS para Comunicación entre VMs

```python
CORS_ALLOWED_ORIGINS = [
    "http://IP_DE_TU_VM_FRONTEND",
    "http://IP_DE_TU_VM_FRONTEND:80",
    "http://IP_DE_TU_VM_FRONTEND:8080",
    "http://IP_DE_TU_VM_FRONTEND:3000",  # Si usas React/Vue en puerto 3000
]

# Para desarrollo, puedes usar:
CORS_ALLOW_ALL_ORIGINS = True  # ⚠️ Solo para desarrollo, NO en producción
```

## 4. Comandos para Configurar el Entorno

### Instalar dependencias:
```bash
pip install -r requirements.txt
```

### Crear y aplicar migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Crear superusuario:
```bash
python manage.py createsuperuser
```

### Ejecutar servidor:
```bash
# Para desarrollo local
python manage.py runserver

# Para permitir conexiones externas (desde otras VMs)
python manage.py runserver 0.0.0.0:8000
```

## 5. Configuración de MariaDB en la VM

### Asegúrate de que MariaDB permita conexiones remotas:

1. Editar `/etc/mysql/mariadb.conf.d/50-server.cnf`:
```bash
bind-address = 0.0.0.0  # Permitir conexiones desde cualquier IP
```

2. Crear usuario para conexión remota:
```sql
CREATE USER 'tu_usuario'@'%' IDENTIFIED BY 'tu_password';
GRANT ALL PRIVILEGES ON figger_energy.* TO 'tu_usuario'@'%';
FLUSH PRIVILEGES;
```

3. Reiniciar MariaDB:
```bash
sudo systemctl restart mariadb
```

## 6. Puertos que Deben Estar Abiertos

- **Backend VM**: Puerto 8000 (Django)
- **Base de Datos VM**: Puerto 3306 (MariaDB)
- **Frontend VM**: Puerto 80/443 (Web server)

## 7. Endpoints de la API

Una vez configurado, tu API estará disponible en:

### Endpoints Principales:
- `GET /api/status/` - Estado de la API
- `GET /api/departamentos/` - Lista departamentos
- `POST /api/departamentos/` - Crear departamento
- `GET /api/empleados/` - Lista empleados
- `POST /api/empleados/` - Crear empleado
- `GET /api/empleados/buscar/?q=término` - Buscar empleados
- `GET /api/estadisticas/generales/` - Estadísticas generales
- `GET /api/config-vm/` - Información de configuración

### Formato de Respuesta:
```json
{
    "success": true,
    "data": {},
    "message": "Mensaje descriptivo",
    "count": 0
}
```

## 8. Pruebas de Conectividad

### Desde la VM del Backend, probar conexión a BD:
```bash
mysql -h IP_DE_VM_BD -u tu_usuario -p figger_energy
```

### Desde la VM del Frontend, probar conexión al Backend:
```bash
curl http://IP_DE_VM_BACKEND:8000/api/status/
```

## 9. Configuración de Producción

### Para producción, cambiar en `settings.py`:
```python
DEBUG = False
SECRET_KEY = 'tu-clave-secreta-muy-segura'

# Usar un servidor web real (nginx + gunicorn)
# Configurar SSL/HTTPS
# Configurar logs apropiados
```

## 10. Monitoreo y Logs

### Los logs del sistema se guardan en la tabla `log_sistema`
### Para ver logs en tiempo real:
```bash
python manage.py shell
>>> from api.models import LogSistema
>>> logs = LogSistema.objects.order_by('-fecha_log')[:10]
>>> for log in logs: print(f"{log.nivel}: {log.mensaje}")
```

## 11. Backup de Base de Datos

```bash
mysqldump -h IP_DE_VM_BD -u tu_usuario -p figger_energy > backup_figger_energy.sql
```

## 12. Restaurar Base de Datos

```bash
mysql -h IP_DE_VM_BD -u tu_usuario -p figger_energy < backup_figger_energy.sql
```
