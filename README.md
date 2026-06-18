# 🔱 Odin Fitness — Sistema QR de Máquinas

Sistema web estático ultra-simple para mostrar guías de uso de cada máquina mediante QR codes.

**Sin base de datos. Sin login. Sin servidor. Costo: $0.**

---

## 📁 Estructura del proyecto

```
odin-qr/
├── machines.json          ← FUENTE DE VERDAD: datos de todas las máquinas
├── generate.py            ← Genera HTML + QR codes automáticamente
├── add_machine.py         ← Agregar nueva máquina interactivamente
├── vercel.json            ← Config de deployment en Vercel
├── index.html             ← Página principal con listado de máquinas
├── machines/              ← Páginas HTML generadas (una por máquina)
│   ├── prensa-45.html
│   ├── hack-squat.html
│   ├── remo-bajo.html
│   ├── press-pecho.html
│   ├── jalon-dorsal.html
│   └── smith-machine.html
└── qr-codes/              ← QR codes generados (uno por máquina)
    ├── qr-prensa-45.png
    ├── qr-hack-squat.png
    └── ...
```

---

## 🚀 Instalación (una sola vez)

### 1. Requisitos
```bash
python3 --version     # Necesitás Python 3.8+
pip install qrcode[pil] pillow
```

### 2. Clonar / copiar el proyecto
```bash
# Si usás GitHub (recomendado):
git init
git add .
git commit -m "Odin Fitness QR System v1"
```

### 3. Configurar tu dominio en generate.py
Abrí `generate.py` y cambiá esta línea:
```python
BASE_URL = "https://odin-fitness.vercel.app"  # ← Tu dominio real
```

### 4. Generar todo
```bash
python3 generate.py
```

---

## 🌐 Deploy en Vercel (GRATIS — menos de 5 minutos)

Vercel es la opción más simple y tiene **plan gratuito ilimitado para sitios estáticos**.

### Opción A: Desde GitHub (Recomendado)

1. Creá un repo en GitHub y subí el proyecto
2. Andá a [vercel.com](https://vercel.com) → Sign up con GitHub
3. "Add New Project" → Seleccioná tu repo
4. Framework: **Other** (sitio estático)
5. Click **Deploy** — listo en 30 segundos

Tu URL quedará: `https://odin-fitness.vercel.app`

### Opción B: Vercel CLI

```bash
npm i -g vercel
cd odin-qr
vercel        # Primera vez
vercel --prod # Actualizaciones
```

### Dominio propio (opcional)
En Vercel Dashboard → Settings → Domains → Agregar `maquinas.odinfitness.com.ar`
Costo adicional: solo el dominio (~$10/año).

---

## 📱 Cómo usar los QR codes

Los QR codes están en la carpeta `qr-codes/`. Cada uno contiene la URL de su máquina.

**Para imprimir y pegar en la máquina:**
1. Abrí el PNG del QR de la máquina correspondiente
2. Imprimí en tamaño mínimo 5×5 cm (recomendado 8×8 cm)
3. Laminalo o usá un porta-tarjeta acrílico para protegerlo
4. Pegalo en un lugar visible de la máquina

**Formato recomendado para el sticker:**
- Tamaño: 10×10 cm
- Impresión: láser o inyección de tinta a 300 dpi
- Papel: adhesivo mate o satinado

---

## ➕ Agregar una nueva máquina

### Método 1: Interactivo (más fácil)
```bash
python3 add_machine.py
```
Te guía paso a paso y regenera todo automáticamente.

### Método 2: Manual en machines.json
Agregá un nuevo objeto al array en `machines.json`:
```json
{
  "id": "curl-scott",
  "name": "Curl en Scott",
  "code": "BH05",
  "muscle_primary": "Bíceps",
  "muscles": ["Bíceps", "Braquial", "Braquiorradial"],
  "cover_emoji": "💪",
  "difficulty": "Principiante",
  "video_placeholder": "https://www.youtube.com/embed/TU_VIDEO_ID",
  "description": "Descripción de la máquina...",
  "setup": [
    "Ajuste 1...",
    "Ajuste 2..."
  ],
  "how_to": [
    "Paso 1...",
    "Paso 2..."
  ],
  "common_errors": [
    "Error 1...",
    "Error 2..."
  ],
  "tips": [
    "Consejo 1...",
    "Consejo 2..."
  ]
}
```

Luego regenerá:
```bash
python3 generate.py
vercel --prod
```

---

## 🎥 Agregar videos reales

Cada máquina tiene un campo `video_placeholder` con una URL de YouTube embed.

Para cambiar el video de una máquina:
1. Encontrá el video en YouTube
2. Copiá el ID del video (lo que va después de `watch?v=`)
3. En `machines.json` cambiá la URL a: `https://www.youtube.com/embed/TU_ID`
4. Regenerá con `python3 generate.py`

Si querés usar tus propios videos (recomendado para contenido branded):
- Subí a YouTube como "no listado" (nadie lo puede buscar, solo quien tenga el link)
- Usá la URL embed del video tuyo

---

## 📞 Actualizar datos de contacto

En `generate.py`, cerca de la función `generate_machine_html`, actualizá:
- Número de WhatsApp: cambiá `541134673115` por tu número con código de país
- Dirección: buscá "Av. Figueroa Alcorta 3351"

---

## 🔮 Roadmap — Próximas versiones

La arquitectura actual permite escalar sin reescribir nada:

| Feature | Cómo agregarlo |
|---------|---------------|
| **Academia Odin** | Nueva sección en cada máquina con videos de rutinas |
| **Biblioteca de ejercicios** | Nueva página `/ejercicios/` con filtros |
| **Soporte técnico** | Formulario que abre WhatsApp con datos pre-cargados |
| **Manuales PDF** | Link de descarga en cada página de máquina |
| **Multi-idioma** | Duplicar machines.json en inglés, misma estructura |
| **Portal distribuidores** | Página separada con password básico en JS |
| **Analytics** | Agregar Plausible.io (GDPR-friendly, gratis para 1 sitio) |
| **Panel admin** | Netlify CMS sobre el mismo repositorio |

---

## 💰 Costos mensuales

| Servicio | Costo |
|---------|-------|
| Vercel (hosting) | $0 |
| GitHub (código) | $0 |
| YouTube (videos) | $0 |
| Dominio propio (opcional) | ~$1/mes |
| **Total** | **$0 – $1/mes** |

---

## 🛠️ Comandos rápidos

```bash
# Regenerar todo (después de editar machines.json)
python3 generate.py

# Agregar máquina nueva interactivamente
python3 add_machine.py

# Deploy a producción
vercel --prod

# Ver el sitio localmente (cualquier opción sirve)
python3 -m http.server 8080
# Luego abrí: http://localhost:8080/index.html
```
