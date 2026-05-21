"""Configuracion general del reto."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "01_datos"
MODEL_DIR = ROOT / "03_modelos"
FIGURE_DIR = ROOT / "05_figuras"

SEED = "RETO3_ANALISIS_OSCAR_2026"

# H no esta definida en esta fase. El PDF pide disenar H.
# No fijar aqui un valor numerico hasta aprobar el procedimiento de diseno.
ALTURA_H_EXTREMO_M = None
PROFUNDIDAD_APOYO_INTERIOR_M = None
