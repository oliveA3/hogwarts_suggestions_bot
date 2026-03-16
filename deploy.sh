#!/bin/bash

# Script para subir cambios del bot Hogwarts a GitHub

# 1. Añadir todos los cambios
git add .

# 2. Crear commit con mensaje automático (puedes editarlo)
git commit -m "Actualización automática del bot Hogwarts"

# 3. Subir a la rama main
git push origin main
