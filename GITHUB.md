# 🚀 Guía Rápida de Publicación en GitHub

Esta guía te ayudará a publicar la Plataforma de Análisis de Cámaras Trampa en GitHub.

---

## 📋 Requisitos Previos

- [ ] Tener una cuenta de GitHub ([crear cuenta](https://github.com/signup))
- [ ] Tener Git instalado en tu computadora ([descargar Git](https://git-scm.com/downloads))

---

## 🔧 Pasos para Publicar

### 1. Crear Repositorio en GitHub

1. Inicia sesión en [GitHub](https://github.com)
2. Haz clic en el botón **"+"** en la esquina superior derecha
3. Selecciona **"New repository"**
4. Configura el repositorio:
   - **Repository name**: `camara-trampa-analyzer`
   - **Description**: `Plataforma profesional para análisis de datos de cámaras trampa - Extracción de metadatos EXIF y generación de reportes Excel`
   - **Visibility**: Public (para que otros puedan usarlo)
   - **NO marques** "Initialize this repository with a README" (ya tenemos uno)
5. Haz clic en **"Create repository"**

### 2. Inicializar Git en tu Proyecto

Abre PowerShell o CMD en la carpeta del proyecto y ejecuta:

```bash
cd C:\Users\erick\.gemini\antigravity\scratch\camara-trampa-analyzer
git init
```

### 3. Configurar Git (Primera vez)

Si es tu primera vez usando Git, configura tu nombre y email:

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"
```

### 4. Agregar Archivos al Repositorio

```bash
git add .
```

### 5. Hacer el Primer Commit

```bash
git commit -m "Initial commit: Plataforma de Análisis de Cámaras Trampa v1.0"
```

### 6. Conectar con GitHub

Reemplaza `TU-USUARIO` con tu nombre de usuario de GitHub:

```bash
git remote add origin https://github.com/TU-USUARIO/camara-trampa-analyzer.git
git branch -M main
git push -u origin main
```

Si te pide autenticación, usa tu **Personal Access Token** de GitHub.

---

## 🏷️ Agregar Topics al Repositorio

En la página de tu repositorio en GitHub:

1. Haz clic en el ícono de engranaje ⚙️ junto a "About"
2. En "Topics", agrega:
   - `camera-trap`
   - `wildlife`
   - `exif`
   - `streamlit`
   - `data-analysis`
   - `conservation`
   - `spanish`
   - `ecology`
3. Guarda los cambios

---

## 📝 Crear un Release (Opcional)

Para marcar la versión 1.0:

1. Ve a la pestaña **"Releases"** en tu repositorio
2. Haz clic en **"Create a new release"**
3. Configura:
   - **Tag version**: `v1.0.0`
   - **Release title**: `Versión 1.0 - Lanzamiento Inicial`
   - **Description**: Describe las características principales
4. Haz clic en **"Publish release"**

---

## ✅ Verificación

Tu repositorio debe tener:

- ✅ README.md visible en la página principal
- ✅ Todos los archivos del proyecto
- ✅ Topics configurados
- ✅ Licencia MIT visible

---

## 🔗 Compartir el Proyecto

Una vez publicado, comparte el enlace:

```
https://github.com/TU-USUARIO/camara-trampa-analyzer
```

---

## 📚 Recursos Adicionales

- [Documentación de Git](https://git-scm.com/doc)
- [Guía de GitHub](https://docs.github.com/es)
- [Markdown Guide](https://www.markdownguide.org/)

---

**¡Listo! Tu proyecto está ahora disponible públicamente en GitHub** 🎉
