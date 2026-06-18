#!/usr/bin/env python3
"""
Odin Fitness — Agregar nueva máquina
Uso: python3 add_machine.py
"""
import json, os, subprocess

MACHINES_FILE = os.path.join(os.path.dirname(__file__), "machines.json")

print("\n🔱 ODIN FITNESS — Agregar nueva máquina\n")
print("Completá los datos de la nueva máquina:\n")

machine = {}
machine["id"]            = input("ID (slug, ej: curl-scott):          ").strip()
machine["name"]          = input("Nombre (ej: Curl en Scott):          ").strip()
machine["code"]          = input("Código catálogo (ej: BH05):          ").strip()
machine["muscle_primary"]= input("Músculo principal (ej: Bíceps):      ").strip()

muscles_raw              = input("Músculos trabajados (separados por coma): ").strip()
machine["muscles"]       = [m.strip() for m in muscles_raw.split(",")]

machine["cover_emoji"]   = input("Emoji representativo (ej: 💪):       ").strip() or "💪"
machine["difficulty"]    = input("Dificultad [Principiante/Intermedio]: ").strip() or "Principiante"
machine["video_placeholder"] = input("URL del video YouTube embed (ej: https://www.youtube.com/embed/XXXX): ").strip()
machine["description"]   = input("Descripción breve de la máquina:     ").strip()

print("\nAjustes básicos (ingresá uno por línea, ENTER vacío para terminar):")
machine["setup"] = []
while True:
    step = input(f"  Ajuste {len(machine['setup'])+1}: ").strip()
    if not step:
        break
    machine["setup"].append(step)

print("\nCómo usarla (pasos, ENTER vacío para terminar):")
machine["how_to"] = []
while True:
    step = input(f"  Paso {len(machine['how_to'])+1}: ").strip()
    if not step:
        break
    machine["how_to"].append(step)

print("\nErrores comunes (ENTER vacío para terminar):")
machine["common_errors"] = []
while True:
    err = input(f"  Error {len(machine['common_errors'])+1}: ").strip()
    if not err:
        break
    machine["common_errors"].append(err)

print("\nConsejos de ejecución (ENTER vacío para terminar):")
machine["tips"] = []
while True:
    tip = input(f"  Consejo {len(machine['tips'])+1}: ").strip()
    if not tip:
        break
    machine["tips"].append(tip)

# Load existing machines
with open(MACHINES_FILE) as f:
    machines = json.load(f)

# Check for duplicate ID
if any(m["id"] == machine["id"] for m in machines):
    print(f"\n❌ Error: Ya existe una máquina con el ID '{machine['id']}'")
    exit(1)

machines.append(machine)

with open(MACHINES_FILE, "w", encoding="utf-8") as f:
    json.dump(machines, f, ensure_ascii=False, indent=2)

print(f"\n✅ Máquina '{machine['name']}' agregada a machines.json")
print("🔄 Regenerando todas las páginas y QR codes...\n")

subprocess.run(["python3", os.path.join(os.path.dirname(__file__), "generate.py")])

print(f"\n🔗 URL: /{machine['id']}.html")
print(f"📱 QR:  qr-codes/qr-{machine['id']}.png")
print("\n¡Listo! No te olvides de hacer deploy con: vercel --prod")
