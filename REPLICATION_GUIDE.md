# Guía de Replicación para Otras Máquinas 🚀

## 📋 Para Replicar Este Backend en Otra Máquina

### ✅ Prerequisitos en la Nueva Máquina

1. **Python 3.8+** instalado
2. **XAMPP** instalado y configurado
3. **Git** (opcional, para clonar el proyecto)

### 🔧 Pasos de Instalación

#### 1. Copiar/Clonar el Proyecto
```bash
# Opción A: Copiar la carpeta completa del backend
# Opción B: Clonar desde repositorio
git clone [URL_DEL_REPO] backend
cd backend
```

#### 2. Instalar Dependencias de Python
```bash
# Instalar todas las dependencias
pip install -r requirements.txt

# Esto instalará automáticamente:
# - Django
# - djangorestframework  
# - django-cors-headers
# - PyMySQL (para conectar con MySQL)
```

#### 3. Configurar XAMPP en la Nueva Máquina

##### A. Iniciar Servicios:
- ✅ Apache
- ✅ MySQL

##### B. Crear Base de Datos:
1. Ir a `http://localhost/phpmyadmin`
2. Ir a la pestaña "SQL"
3. Ejecutar el script completo de `XAMPP_DATABASE_SETUP.sql`

#### 4. Configurar Conexión de Red (Si es necesario)

##### Para acceso desde otras máquinas a esta base de datos:

**Opción A: Solo cambiar IP en Django (recomendado)**
- En `settings.py`, cambiar `HOST` por la IP de la máquina con XAMPP
- Ejemplo: `'HOST': '192.168.1.100'`

**Opción B: Configurar MySQL para acceso remoto**
```sql
-- En phpMyAdmin, ejecutar:
GRANT ALL PRIVILEGES ON figger_energy.* TO 'root'@'%' IDENTIFIED BY '';
FLUSH PRIVILEGES;
```

### 🖥️ Configuraciones por Escenario

#### Escenario 1: Todo en Una Máquina
```python
# settings.py
DATABASES = {
    'default': {
        'HOST': '127.0.0.1',  # localhost
    }
}
```

#### Escenario 2: Backend y Base de Datos en Máquinas Separadas
```python
# En la máquina del backend, settings.py
DATABASES = {
    'default': {
        'HOST': '192.168.1.100',  # IP de la máquina con XAMPP
    }
}
```

#### Escenario 3: Frontend, Backend, y BD en Máquinas Separadas
```python
# Máquina Backend - settings.py
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '192.168.1.100',  # IP del backend
    '192.168.1.101',  # IP del frontend
]

DATABASES = {
    'default': {
        'HOST': '192.168.1.102',  # IP de la máquina con XAMPP
    }
}

CORS_ALLOWED_ORIGINS = [
    "http://192.168.1.101",  # IP del frontend
    "http://192.168.1.101:3000",  # Si usa React
    "http://192.168.1.101:8080",  # Si usa Vue
]
```

### 🚀 Ejecutar el Backend

```bash
# Para acceso local solamente
python manage.py runserver

# Para permitir acceso desde otras máquinas
python manage.py runserver 0.0.0.0:8000
```

### 🧪 Verificar que Funciona

#### 1. Test Local:
```
http://localhost:8000/api/status/
```

#### 2. Test desde Otra Máquina:
```
http://[IP_DE_LA_MAQUINA]:8000/api/status/
```

### 📝 Archivo de Configuración Rápida

Crea un archivo `config.py` para cambios rápidos:

```python
# config.py
# Cambiar estas variables según la máquina

# IP de la máquina con XAMPP/MySQL
DATABASE_HOST = '127.0.0.1'  # Cambiar por IP de la máquina con BD

# IP de la máquina con Frontend
FRONTEND_IP = '127.0.0.1'  # Cambiar por IP del frontend

# IP de esta máquina (Backend)
BACKEND_IP = '127.0.0.1'  # Cambiar por IP de esta máquina
```

### 🔍 Solución de Problemas

#### Error: "Can't connect to MySQL server"
- ✅ Verificar que XAMPP MySQL está corriendo
- ✅ Verificar la IP en `HOST` en settings.py
- ✅ Verificar que el puerto 3306 está abierto

#### Error: "Access denied"
- ✅ Verificar usuario y password en settings.py
- ✅ XAMPP usa `root` con password vacía por defecto

#### Error: "No module named 'PyMySQL'"
```bash
pip install PyMySQL
```

#### Error: Firewall bloqueando conexiones
- Abrir puerto 3306 (MySQL) en firewall
- Abrir puerto 8000 (Django) en firewall

### 📊 Estructura de IPs de Ejemplo

```
Máquina A (Frontend):     192.168.1.101
Máquina B (Backend):      192.168.1.102  
Máquina C (BD/XAMPP):     192.168.1.103

Configuración en Backend (Máquina B):
- DATABASE_HOST = '192.168.1.103'
- ALLOWED_HOSTS = ['192.168.1.102', '192.168.1.101']
- CORS_ALLOWED_ORIGINS = ['http://192.168.1.101']
```

### ⚡ Quick Start Script

Crea un archivo `start.bat` (Windows) o `start.sh` (Linux):

```bash
@echo off
echo Iniciando Backend Figger Energy...
echo.
echo 1. Verificando XAMPP...
curl -s http://localhost/phpmyadmin > nul
if %errorlevel% neq 0 (
    echo ERROR: XAMPP no está corriendo o phpMyAdmin no es accesible
    pause
    exit
)

echo 2. Iniciando Django...
python manage.py runserver 0.0.0.0:8000
```

### ✅ Checklist de Replicación

- [ ] Python instalado en nueva máquina
- [ ] XAMPP instalado y MySQL corriendo
- [ ] Proyecto copiado/clonado
- [ ] `pip install -r requirements.txt` ejecutado
- [ ] Base de datos creada con script SQL
- [ ] IP configurada en settings.py
- [ ] Firewall configurado (puertos 3306, 8000)
- [ ] `python manage.py runserver 0.0.0.0:8000` funciona
- [ ] API responde desde otras máquinas

---

**¡Con esta configuración puedes replicar el backend en cualquier máquina con XAMPP!** 🎉
