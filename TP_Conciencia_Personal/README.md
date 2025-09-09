# TP1 – Conciencia en el Código (Green Software)

Este proyecto mide el consumo energético y las emisiones de CO₂eq producidas por un bloque de código Python durante un tiempo determinado (por defecto 10 minutos), utilizando la librería [CodeCarbon](https://mlco2.github.io/codecarbon/).

Al finalizar la ejecución se genera un resumen con:
- Tiempo de ejecución
- Energía consumida (kWh)
- Potencia media (W)
- Emisiones de CO₂eq (kg)
- Tasa de emisión (kg/h)
- Horas de cómputo necesarias para ser compensadas por un árbol joven (30 kg/año) y adulto (300 kg/año)

Además, se guarda un archivo `emissions.csv` con el detalle técnico de la medición.

---

## Requisitos
- Python 3.12 (probado en 3.12.6)
- Sistema operativo Windows, Linux o macOS
- Entorno virtual recomendado

---

## Instalación

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Windows (PowerShell):
. .venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias
pip install codecarbon
