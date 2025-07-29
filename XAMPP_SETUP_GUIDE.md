# Configuración con XAMPP - Guía Paso a Paso 🚀

## ✅ Prerequisitos

1. **XAMPP instalado y corriendo**
2. **Apache y MySQL iniciados en XAMPP**
3. **phpMyAdmin accesible en http://localhost/phpmyadmin**

## 📋 Pasos para Configurar la Base de Datos

### 1. Crear la Base de Datos en phpMyAdmin

1. **Abrir phpMyAdmin**: Ve a `http://localhost/phpmyadmin`
2. **Ir a SQL**: Haz clic en la pestaña "SQL" en la parte superior
3. **Ejecutar el script**: Copia y pega todo el contenido del archivo `XAMPP_DATABASE_SETUP.sql`
4. **Ejecutar**: Haz clic en "Continuar" o "Go"

### 2. Verificar la Creación

Después de ejecutar el script, deberías ver:
- ✅ Base de datos `figger_energy` creada
- ✅ 9 tablas creadas
- ✅ 3 departamentos insertados
- ✅ 8 roles insertados

### 3. Configurar Django para XAMPP

La configuración ya está lista en `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'figger_energy',
        'USER': 'root',  # XAMPP default user
        'PASSWORD': '',  # XAMPP default password (empty)
        'HOST': '127.0.0.1',  # XAMPP localhost
        'PORT': '3306',  # XAMPP default MySQL port
    }
}
```

## 🔧 Instalar Dependencias de Python

Ejecuta estos comandos en orden:

```bash
# 1. Instalar mysqlclient para conectar con MySQL
pip install mysqlclient

# 2. Si mysqlclient falla, usar PyMySQL como alternativa
pip install PyMySQL
```

### Si mysqlclient da problemas, usar PyMySQL:

Agrega esto al inicio de `mybackend/settings.py`:

```python
import pymysql
pymysql.install_as_MySQLdb()
```

## 🚀 Ejecutar Django

### 1. Hacer migraciones de Django (opcional, las tablas ya existen)

```bash
python manage.py makemigrations
python manage.py migrate --fake-initial
```

### 2. Crear superusuario para Django Admin

```bash
python manage.py createsuperuser
```

### 3. Ejecutar el servidor

```bash
# Para acceso local
python manage.py runserver

# Para acceso desde otras máquinas (VMs)
python manage.py runserver 0.0.0.0:8000
```

## 🧪 Probar la Conexión

### 1. Verificar status de la API:
```
http://127.0.0.1:8000/api/status/
```

### 2. Ver departamentos:
```
http://127.0.0.1:8000/api/departamentos/
```

### 3. Admin de Django:
```
http://127.0.0.1:8000/admin/
```

## 📊 URLs de phpMyAdmin

- **phpMyAdmin**: `http://localhost/phpmyadmin`
- **Base de datos**: `figger_energy`
- **Usuario**: `root`
- **Password**: (vacío)

## 🔍 Solución de Problemas Comunes

### Error: "No module named 'MySQLdb'"
```bash
pip install mysqlclient
# o
pip install PyMySQL
```

### Error: "Access denied for user 'root'@'localhost'"
- Verificar que XAMPP MySQL está corriendo
- Verificar credenciales en phpMyAdmin

### Error: "Can't connect to MySQL server"
- Asegurar que MySQL está iniciado en XAMPP Control Panel
- Verificar que el puerto 3306 está libre

### Error: "Table doesn't exist"
- Ejecutar el script SQL completo en phpMyAdmin
- Verificar que la base de datos `figger_energy` existe

## 🎯 URLs Importantes

### Para Desarrollo Local:
- **API Base**: `http://127.0.0.1:8000/api/`
- **Django Admin**: `http://127.0.0.1:8000/admin/`
- **phpMyAdmin**: `http://localhost/phpmyadmin`
- **XAMPP Control**: `http://localhost/dashboard`

### Para VMs (cambiar IPs):
- **API Base**: `http://[IP_VM_BACKEND]:8000/api/`
- **Django Admin**: `http://[IP_VM_BACKEND]:8000/admin/`

## 📱 Testing con curl

```bash
# Status check
curl -X GET http://127.0.0.1:8000/api/status/

# Get departments
curl -X GET http://127.0.0.1:8000/api/departamentos/

# Get roles
curl -X GET http://127.0.0.1:8000/api/roles/

# Get statistics
curl -X GET http://127.0.0.1:8000/api/estadisticas/generales/
```

## 🗂️ Estructura de la Base de Datos

```
figger_energy/
├── departamentos (3 registros)
├── roles (8 registros)
├── empleados (vacía, lista para usar)
├── usuarios (vacía, lista para usar)
├── sesiones (vacía)
├── perfiles_empleados (vacía)
├── notificaciones (vacía)
├── actividades_usuario (vacía)
└── log_sistema (vacía)
```

## ✅ Checklist Final

- [ ] XAMPP corriendo (Apache + MySQL)
- [ ] Base de datos `figger_energy` creada en phpMyAdmin
- [ ] Script SQL ejecutado exitosamente
- [ ] `pip install mysqlclient` completado
- [ ] Django settings configurado para XAMPP
- [ ] `python manage.py runserver` funciona
- [ ] API responde en `http://127.0.0.1:8000/api/status/`
- [ ] phpMyAdmin muestra las tablas con datos

## 🎉 ¡Listo para Usar!

Una vez completados todos los pasos, tu backend estará:
- ✅ Conectado a XAMPP MySQL
- ✅ Con datos iniciales cargados
- ✅ APIs funcionando
- ✅ Listo para conectar con frontend
- ✅ Preparado para despliegue en VMs

---

**¡Tu sistema Figger Energy está listo para funcionar con XAMPP!** 🚀
