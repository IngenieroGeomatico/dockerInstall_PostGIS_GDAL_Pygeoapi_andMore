#!/bin/bash


if [ -z "$(ls -A /var/lib/postgresql/data 2>/dev/null)" ]; then
    echo "Directorio /var/lib/postgresql/data vacío. Copiando datos iniciales..."
    cp -R /var/lib/postgresql/data_backup/* /var/lib/postgresql/data/
    
else
    echo "Directorio de datos ya contiene información. No se realiza copia."
fi

chown -R postgres:postgres /var/lib/postgresql/data
chmod 0700 /var/lib/postgresql/data



# Verificar si PostgreSQL ya está en ejecución
if [ -f /var/lib/postgresql/data/postmaster.pid ]; then
    echo "PostgreSQL ya está en ejecución. Eliminando el archivo postmaster.pid..."
    rm -f /var/lib/postgresql/data/postmaster.pid
fi

# Detener cualquier instancia de PostgreSQL en ejecución
echo "Deteniendo cualquier instancia de PostgreSQL en ejecución..."
su - postgres -c "/usr/lib/postgresql/14/bin/pg_ctl -D /var/lib/postgresql/data stop || echo 'No se encontró ninguna instancia en ejecución.'"



# Iniciar PostgreSQL con un tiempo de espera mayor
echo "Iniciando el servicio de PostgreSQL..."
su - postgres -c "/usr/lib/postgresql/14/bin/pg_ctl -D /var/lib/postgresql/data -l /var/lib/postgresql/logfile start -t 120 "

cat /var/lib/postgresql/logfile

# Esperar a que el servicio esté disponible
echo "Esperando a que PostgreSQL esté disponible..."
i=1
while [ $i -le 20 ]; do
    if su - postgres -c 'psql -c "SELECT 1;" ' > /dev/null 2>&1; then
        echo "PostgreSQL está disponible."
        break
    fi
    echo "Intento $i: PostgreSQL no está disponible, esperando 10 segundos..."
    sleep 10
    i=$((i + 1))
done

if [ $i -gt 20 ]; then
    echo "Error: PostgreSQL no se levantó después de 20 intentos. Revisando logs..."
    cat /var/lib/postgresql/logfile
    # exit 1
fi

