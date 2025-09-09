import time, math, os
from codecarbon import OfflineEmissionsTracker

# ----------------------------
# Parámetros
# ----------------------------
MINUTES = float(os.getenv("RUN_MINUTES", "10"))
DURATION_S = int(MINUTES * 60)

# Factor de Emisión (Argentina 2022):
# 0.3966 tCO2e/MWh  =>  0.3966 kgCO2e/kWh   (del PDF de cátedra)
FE_KG_PER_KWH = 0.3966

# Consumos de árboles (del PDF de cátedra)
TREE_YOUNG_KG_PER_YEAR = 30.0    # recién plantado
TREE_ADULT_KG_PER_YEAR = 300.0   # adulto

def simple_cpu_work():
    # Tarea para ocupar CPU sin dependencias
    total = 0.0
    for i in range(1, 20_000):
        total += math.sqrt((i * i) % 97)
    return total

def main():
    tracker = OfflineEmissionsTracker(
        country_iso_code="ARG",          # usa FE de Argentina
        measure_power_secs=1,            # muestreo 1 s
        log_level="error",               # menos ruido en consola
        output_dir=".",                  # genera emissions.csv en el cwd
        save_to_file=True
    )

    print(f"⏱️ Ejecutando carga durante {MINUTES:.2f} minutos...")
    t0 = time.time()
    tracker.start()

    # ----------------------------
    # Bucle principal (carga)
    # ----------------------------
    junk = 0.0
    try:
        while (time.time() - t0) < DURATION_S:
            junk += simple_cpu_work()
    except KeyboardInterrupt:
        print("\nInterrumpido por usuario. Cerrando medición...")

    emissions_kg = tracker.stop()  # kg CO2eq
    elapsed_s = time.time() - t0
    elapsed_h = elapsed_s / 3600.0

    # ----------------------------
    # Cálculos solicitados
    # ----------------------------
    # Energía aproximada a partir del FE (kWh)
    energy_kwh = emissions_kg / FE_KG_PER_KWH if FE_KG_PER_KWH > 0 else 0.0
    # Potencia media (W) = (kWh * 1000) / h
    avg_power_w = (energy_kwh * 1000.0) / elapsed_h if elapsed_h > 0 else 0.0
    # Tasa de emisión (kg/h)
    kg_per_h = emissions_kg / elapsed_h if elapsed_h > 0 else 0.0

    # Horas para compensar con árboles
    hours_for_30 = TREE_YOUNG_KG_PER_YEAR / kg_per_h if kg_per_h > 0 else float("inf")
    hours_for_300 = TREE_ADULT_KG_PER_YEAR / kg_per_h if kg_per_h > 0 else float("inf")

    # ----------------------------
    # Resumen en consola
    # ----------------------------
    print("\n================= RESUMEN TP1 – Conciencia en el código =================")
    print(f"Tiempo de ejecución             : {elapsed_s:,.1f} s ({elapsed_h:.4f} h)")
    print(f"Energía aproximada              : {energy_kwh:.6f} kWh")
    print(f"Potencia media                  : {avg_power_w:.2f} W")
    print(f"CO₂e total                      : {emissions_kg:.6f} kg")
    print(f"Tasa de emisión                 : {kg_per_h:.6f} kg/h")
    print(f"Horas p/compensar (árbol 30 kg) : {hours_for_30:,.2f} h")
    print(f"Horas p/compensar (árbol 300 kg): {hours_for_300:,.2f} h")
    print("Archivo con detalle             : ./emissions.csv (CodeCarbon)")
    print("==========================================================================")
    # Evita que 'junk' sea optimizado (no afecta a resultados, solo carga la CPU)
    if junk == 0.123456789:
        print(".")

if __name__ == "__main__":
    main()
