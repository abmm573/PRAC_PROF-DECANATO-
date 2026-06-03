import os
import uuid
import aiofiles
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path

enrutador = APIRouter()

# Definir rutas base para almacenamiento local
DIRECTORIO_BASE = Path("archivos_subidos")
DIRECTORIO_PDFS = DIRECTORIO_BASE / "pdfs"
DIRECTORIO_PORTADAS = DIRECTORIO_BASE / "portadas"

# Crear directorios si no existen al iniciar
DIRECTORIO_PDFS.mkdir(parents=True, exist_ok=True)
DIRECTORIO_PORTADAS.mkdir(parents=True, exist_ok=True)

@enrutador.post("/subir/revista/")
async def subir_archivos_revista(
    archivo_pdf: UploadFile = File(...), 
    archivo_portada: UploadFile = File(...)
):
    # 1. Validar extensiones
    if not archivo_pdf.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="El documento debe ser un PDF válido.")
    if not archivo_portada.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="La portada debe ser una imagen (PNG, JPG, JPEG).")

    # 2. Generar nombres únicos (UUID) manteniendo la extensión original
    extension_pdf = Path(archivo_pdf.filename).suffix
    extension_portada = Path(archivo_portada.filename).suffix
    
    nombre_unico_pdf = f"{uuid.uuid4()}{extension_pdf}"
    nombre_unico_portada = f"{uuid.uuid4()}{extension_portada}"

    ruta_pdf = DIRECTORIO_PDFS / nombre_unico_pdf
    ruta_portada = DIRECTORIO_PORTADAS / nombre_unico_portada

    # 3. Guardar archivos asíncronamente en el servidor local
    try:
        async with aiofiles.open(ruta_pdf, 'wb') as pdf_salida:
            contenido = await archivo_pdf.read()
            await pdf_salida.write(contenido)
            
        async with aiofiles.open(ruta_portada, 'wb') as portada_salida:
            contenido = await archivo_portada.read()
            await portada_salida.write(contenido)
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"Error al guardar los archivos: {str(e)}")

    # 4. Retornar las rutas relativas para guardarlas en PostgreSQL
    return {
        "mensaje": "Archivos subidos correctamente",
        "ruta_pdf": f"/archivos_subidos/pdfs/{nombre_unico_pdf}",
        "ruta_portada": f"/archivos_subidos/portadas/{nombre_unico_portada}"
    }