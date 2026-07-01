# 🐳 dockerInstall_PostGIS_GDAL_Pygeoapi

Recetas Docker para levantar entornos de desarrollo con **PostGIS**, **GDAL** y **pygeoapi**, cada uno con múltiples enfoques de instalación.

## Estructura del proyecto

```
├── POSTGIS_easyInstall/       # PostGIS vía apt (Ubuntu 22.04, PG 14 + PostGIS 3)
├── POSTGIS_fromImage/         # PostGIS desde imagen oficial postgis/postgis (PG 17 + PostGIS 3.5)
├── POSTGIS_fromSource/        # PostGIS compilado desde fuente (PG 17.5 + PostGIS 3.5.2)
├── GDAL_easyInstall/          # GDAL vía apt (Ubuntu 22.04)
├── GDAL_fromImage/            # GDAL desde imagen oficial OSGeo (ghcr.io/osgeo/gdal)
├── GDAL_fromSource/           # GDAL compilado desde fuente vía cmake
├── Pygeoapi_fromGIT/          # pygeoapi desde release de GitHub, sobre imagen GDAL base
└── Pygeoapi_fromGIT_custom/   # (placeholder)
```

Cada directorio es independiente e incluye su propio `Dockerfile`, `docker-compose.yml` y scripts de verificación.

---

## Enfoques de instalación

Cada componente ofrece tres variantes:

- **easyInstall** — Instala el paquete desde los repositorios `apt` de Ubuntu. Rápido, pero la versión depende del repo oficial de Ubuntu. Se puede parametrizar la imagen base de Ubuntu.
- **fromImage** — Usa la imagen Docker oficial del proyecto (ej. `postgis/postgis`, `ghcr.io/osgeo/gdal`). Ya viene con el software preinstalado y listo para usar. Se puede parametrizar el tag de la imagen para cambiar la versión.
- **fromSource** — Descarga el código fuente y lo compila manualmente (ej. `cmake`, `make`, `make install`). Más lento pero permite elegir versiones exactas y opciones de compilación mediante ARG de Docker.

Todas las variantes aceptan parámetros configurables vía `ARG` en los Dockerfiles (ver [tabla más abajo](#versiones-configurables-vía-arg)).

---

## PostGIS

Tres variantes que exponen PostgreSQL + PostGIS en el puerto **5432**.  
Credenciales por defecto: `usuario` / `pass` / base de datos `postgis`.

```bash
cd POSTGIS_easyInstall
docker compose -f docker-compose_dockerfile_easyInstall.yml up --build
```

```bash
cd POSTGIS_fromImage
docker compose -f docker-compose_dockerfile_fromImage.yml up --build
```

```bash
cd POSTGIS_fromSource
docker compose -f docker-compose_dockerfile_fromSource.yml up --build
```

El contenedor ejecuta `checkPOSTGIS.py` al arrancar para verificar que PostGIS está operativo.

**Persistencia:** los datos se almacenan en `./postgis_data/`.

---

## GDAL

Tres variantes que instalan GDAL y sus bindings Python, ejecutan `checkGDAL.py` y finalizan (no son servicios persistentes).

```bash
cd GDAL_easyInstall
docker compose -f docker-compose_dockerfile_easyInstall.yml up --build
```

```bash
cd GDAL_fromImage
docker compose -f docker-compose_dockerfile_fromImage.yml up --build
```

```bash
cd GDAL_fromSource
docker compose -f docker-compose_dockerfile_fromSource.yml up --build
```

---

## pygeoapi

**pygeoapi** es un servidor Python que implementa los estándares OGC API (Open Geospatial Consortium). Permite publicar y consultar datos geoespaciales (features, coberturas, mapas, STAC, procesos) a través de una API REST.

Esta variante construye una imagen `gdal_base` a partir de `GDAL_easyInstall` y luego instala pygeoapi sobre ella. Sirve en el puerto **5000**.

```bash
cd Pygeoapi_fromGIT
make -f Makefile_pygeoapi_fromGIT up
```

O paso a paso:

```bash
docker build -t gdal_base -f ../GDAL_easyInstall/dockerfile_easyInstall .
docker build -t dockerfile_pygeoapi_from_git -f dockerfile_Pygeoapi_fromGIT .
docker compose -f docker-compose_dockerfile_Pygeoapi_fromGIT.yml up --build
```

Acceder en [http://localhost:5000](http://localhost:5000).

---

## Versiones configurables vía ARG

| Componente | ARG | Defecto |
|---|---|---|
| POSTGIS (fromImage) | `PG_Version` | `17-3.5` |
| POSTGIS (fromSource) | `PG_Version` / `POSTGIS_Version` | `17.5` / `3.5.2` |
| GDAL (fromImage) | `GDAL_VERSION` | `3.10.2` |
| GDAL (fromSource) | `GDAL_VERSION` | `3.10.2` |
| pygeoapi | `version_pygeoapi` | `0.20.0` |
| GDAL (todos) | `version_NUMPY` | `2.2.4` |

---

## Notas

- Proyecto educativo / en desarrollo.
- No usar en producción sin cambiar credenciales y certificados SSL.
- `Pygeoapi_fromGIT_custom/` está vacío — en desarrollo, contendrá un pygeoapi con complementos y plugins extra.