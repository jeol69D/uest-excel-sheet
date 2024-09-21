# Usar imagen oficial de Python
FROM python:3.9-slim

# Crear y usar el directorio de trabajo
WORKDIR /app

# Copiar solo requirements.txt primero para instalar dependencias
COPY requirements.txt .

# Instalar las dependencias (si cambian los requirements, esto será reconstruido)
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto 8000
EXPOSE 8000

# Comando para ejecutar la app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
