#!/usr/bin/env python3
"""
Odin Fitness - QR Machine Pages Generator
Genera las páginas HTML de cada máquina y los QR codes correspondientes.
"""

import json
import os
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image, ImageDraw, ImageFont

# ─── CONFIG ──────────────────────────────────────────────────────────────────
BASE_URL = "https://odin-fitness.vercel.app"  # Cambiar por tu dominio real
OUTPUT_DIR = "/home/claude/odin-qr"
QR_DIR = f"{OUTPUT_DIR}/qr-codes"
MACHINES_FILE = f"{OUTPUT_DIR}/machines.json"

# ─── LOAD DATA ───────────────────────────────────────────────────────────────
with open(MACHINES_FILE) as f:
    machines = json.load(f)

# ─── HTML TEMPLATE ───────────────────────────────────────────────────────────
def generate_machine_html(machine):
    muscles_html = "".join(
        f'<span class="muscle-tag">{m}</span>' for m in machine["muscles"]
    )
    setup_html = "".join(
        f'<li><span class="step-num">{i+1:02d}</span><span>{step}</span></li>'
        for i, step in enumerate(machine["setup"])
    )
    how_html = "".join(
        f'<li><span class="step-num">{i+1:02d}</span><span>{step}</span></li>'
        for i, step in enumerate(machine["how_to"])
    )
    errors_html = "".join(
        f'<li><span class="icon-x">✕</span><span>{e}</span></li>'
        for e in machine["common_errors"]
    )
    tips_html = "".join(
        f'<li><span class="icon-check">✓</span><span>{t}</span></li>'
        for t in machine["tips"]
    )

    # Video embed (YouTube iframe or placeholder)
    video_html = f'''
    <div class="video-container">
        <iframe
            src="{machine['video_placeholder']}"
            title="Video: {machine['name']}"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen>
        </iframe>
    </div>'''

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
    <meta name="theme-color" content="#0A0A0A">
    <meta name="description" content="Guía de uso: {machine['name']} — Odin Fitness">
    <title>{machine['name']} · Odin Fitness</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Barlow+Condensed:wght@600;700;800&display=swap" rel="stylesheet">
    <style>
        /* ── RESET & BASE ─────────────────────────────────── */
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        
        :root {{
            --black:       #0A0A0A;
            --dark:        #111111;
            --surface:     #181818;
            --surface-2:   #1F1F1F;
            --border:      #2A2A2A;
            --border-light: #333333;
            --gold:        #C8A951;
            --gold-dim:    #9E8140;
            --gold-glow:   rgba(200,169,81,0.15);
            --white:       #F5F5F5;
            --white-dim:   #AAAAAA;
            --white-faint: #666666;
            --error:       #E05454;
            --success:     #4CAF82;
            --font-display: 'Barlow Condensed', sans-serif;
            --font-body:    'Inter', sans-serif;
            --radius:       12px;
            --radius-sm:    8px;
        }}

        html {{
            font-size: 16px;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        body {{
            background: var(--black);
            color: var(--white);
            font-family: var(--font-body);
            min-height: 100vh;
            overflow-x: hidden;
        }}

        /* ── HEADER ───────────────────────────────────────── */
        .site-header {{
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(10,10,10,0.95);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border);
            padding: 14px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .logo-mark {{
            display: flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
        }}
        .logo-icon {{
            width: 32px;
            height: 32px;
            background: var(--gold);
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            font-weight: 800;
            color: var(--black);
            font-family: var(--font-display);
            letter-spacing: -0.5px;
        }}
        .logo-text {{
            font-family: var(--font-display);
            font-size: 18px;
            font-weight: 700;
            color: var(--white);
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }}
        .logo-text span {{
            color: var(--gold);
        }}
        .header-code {{
            font-family: var(--font-body);
            font-size: 11px;
            color: var(--white-faint);
            background: var(--surface);
            border: 1px solid var(--border);
            padding: 4px 8px;
            border-radius: 4px;
            letter-spacing: 0.5px;
        }}

        /* ── HERO ─────────────────────────────────────────── */
        .hero {{
            background: var(--dark);
            padding: 32px 20px 28px;
            border-bottom: 1px solid var(--border);
            position: relative;
            overflow: hidden;
        }}
        .hero::before {{
            content: '';
            position: absolute;
            top: -60px;
            right: -40px;
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, var(--gold-glow) 0%, transparent 70%);
            pointer-events: none;
        }}
        .hero-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: var(--gold-glow);
            border: 1px solid rgba(200,169,81,0.3);
            color: var(--gold);
            font-size: 11px;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 20px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 16px;
        }}
        .hero-badge::before {{
            content: '';
            width: 6px;
            height: 6px;
            background: var(--gold);
            border-radius: 50%;
            display: inline-block;
        }}
        .hero-emoji {{
            font-size: 52px;
            line-height: 1;
            margin-bottom: 12px;
            display: block;
            filter: drop-shadow(0 0 20px rgba(200,169,81,0.3));
        }}
        .hero-title {{
            font-family: var(--font-display);
            font-size: 42px;
            font-weight: 800;
            line-height: 1;
            text-transform: uppercase;
            letter-spacing: -0.5px;
            margin-bottom: 8px;
        }}
        .hero-title span {{
            color: var(--gold);
        }}
        .hero-sub {{
            font-size: 14px;
            color: var(--white-dim);
            font-weight: 400;
            line-height: 1.5;
            max-width: 300px;
        }}
        .hero-muscles {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-top: 20px;
        }}
        .muscle-tag {{
            font-size: 11px;
            font-weight: 500;
            color: var(--white-dim);
            background: var(--surface);
            border: 1px solid var(--border-light);
            padding: 4px 10px;
            border-radius: 20px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .muscle-tag:first-child {{
            background: var(--gold-glow);
            border-color: rgba(200,169,81,0.3);
            color: var(--gold);
        }}
        .hero-difficulty {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: 16px;
            font-size: 12px;
            color: var(--white-faint);
        }}
        .difficulty-dot {{
            width: 8px;
            height: 8px;
            background: var(--success);
            border-radius: 50%;
        }}

        /* ── SECTION STRUCTURE ────────────────────────────── */
        .content {{
            padding: 0 0 40px;
        }}
        .section {{
            padding: 24px 20px;
            border-bottom: 1px solid var(--border);
        }}
        .section:last-child {{
            border-bottom: none;
        }}
        .section-label {{
            font-size: 10px;
            font-weight: 700;
            color: var(--gold);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 6px;
        }}
        .section-title {{
            font-family: var(--font-display);
            font-size: 22px;
            font-weight: 700;
            text-transform: uppercase;
            margin-bottom: 16px;
            line-height: 1;
        }}

        /* ── VIDEO ────────────────────────────────────────── */
        .video-section {{
            padding: 20px;
            background: var(--dark);
            border-bottom: 1px solid var(--border);
        }}
        .video-container {{
            position: relative;
            width: 100%;
            padding-bottom: 56.25%;
            border-radius: var(--radius);
            overflow: hidden;
            background: var(--surface);
            border: 1px solid var(--border-light);
        }}
        .video-container iframe {{
            position: absolute;
            top: 0; left: 0;
            width: 100%;
            height: 100%;
        }}
        .video-label {{
            font-size: 11px;
            color: var(--white-faint);
            margin-top: 10px;
            text-align: center;
        }}

        /* ── DESCRIPTION ──────────────────────────────────── */
        .description-text {{
            font-size: 15px;
            line-height: 1.65;
            color: var(--white-dim);
        }}

        /* ── STEP LISTS ───────────────────────────────────── */
        .step-list {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}
        .step-list li {{
            display: flex;
            align-items: flex-start;
            gap: 12px;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-sm);
            padding: 14px;
        }}
        .step-num {{
            font-family: var(--font-display);
            font-size: 18px;
            font-weight: 800;
            color: var(--gold);
            min-width: 28px;
            line-height: 1.2;
        }}
        .step-list li span:last-child {{
            font-size: 14px;
            line-height: 1.5;
            color: var(--white-dim);
        }}

        /* ── ICON LISTS ───────────────────────────────────── */
        .icon-list {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        .icon-list li {{
            display: flex;
            align-items: flex-start;
            gap: 12px;
            padding: 12px 14px;
            border-radius: var(--radius-sm);
            font-size: 14px;
            line-height: 1.5;
        }}
        .icon-x, .icon-check {{
            font-size: 14px;
            font-weight: 700;
            min-width: 20px;
            height: 20px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            margin-top: 1px;
        }}
        .icon-x {{
            background: rgba(224,84,84,0.15);
            color: var(--error);
        }}
        .icon-check {{
            background: rgba(76,175,130,0.15);
            color: var(--success);
        }}
        .error-list li {{
            background: rgba(224,84,84,0.05);
            border: 1px solid rgba(224,84,84,0.15);
            color: #D4AAAA;
        }}
        .tips-list li {{
            background: rgba(76,175,130,0.05);
            border: 1px solid rgba(76,175,130,0.15);
            color: #A8CFBB;
        }}

        /* ── DIVIDER ──────────────────────────────────────── */
        .gold-divider {{
            height: 2px;
            background: linear-gradient(90deg, var(--gold) 0%, transparent 100%);
            margin: 0;
            opacity: 0.6;
        }}

        /* ── CTA COMERCIAL ────────────────────────────────── */
        .cta-section {{
            padding: 32px 20px;
            background: linear-gradient(135deg, #0F0E09 0%, var(--dark) 100%);
            border-top: 1px solid rgba(200,169,81,0.2);
        }}
        .cta-eyebrow {{
            font-size: 10px;
            font-weight: 700;
            color: var(--gold);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 8px;
        }}
        .cta-title {{
            font-family: var(--font-display);
            font-size: 28px;
            font-weight: 800;
            text-transform: uppercase;
            line-height: 1.1;
            margin-bottom: 10px;
        }}
        .cta-title em {{
            color: var(--gold);
            font-style: normal;
        }}
        .cta-sub {{
            font-size: 14px;
            color: var(--white-dim);
            line-height: 1.5;
            margin-bottom: 24px;
        }}
        .cta-buttons {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        .btn {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            padding: 16px 20px;
            border-radius: var(--radius-sm);
            font-size: 14px;
            font-weight: 600;
            text-decoration: none;
            border: none;
            cursor: pointer;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
            letter-spacing: 0.3px;
        }}
        .btn:active {{
            transform: scale(0.98);
        }}
        .btn-whatsapp {{
            background: #25D366;
            color: #fff;
            box-shadow: 0 4px 20px rgba(37,211,102,0.25);
        }}
        .btn-whatsapp:active {{
            box-shadow: 0 2px 10px rgba(37,211,102,0.2);
        }}
        .btn-catalog {{
            background: var(--gold);
            color: var(--black);
            box-shadow: 0 4px 20px rgba(200,169,81,0.25);
            font-weight: 700;
        }}
        .btn-budget {{
            background: transparent;
            color: var(--white);
            border: 1px solid var(--border-light);
        }}
        .btn-icon {{
            font-size: 18px;
        }}
        .cta-trust {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 16px;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid var(--border);
        }}
        .trust-item {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 2px;
        }}
        .trust-num {{
            font-family: var(--font-display);
            font-size: 20px;
            font-weight: 800;
            color: var(--gold);
        }}
        .trust-label {{
            font-size: 10px;
            color: var(--white-faint);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            text-align: center;
        }}
        .trust-sep {{
            width: 1px;
            height: 32px;
            background: var(--border);
        }}

        /* ── FOOTER ───────────────────────────────────────── */
        .site-footer {{
            background: var(--black);
            border-top: 1px solid var(--border);
            padding: 20px;
            text-align: center;
        }}
        .footer-logo {{
            font-family: var(--font-display);
            font-size: 16px;
            font-weight: 700;
            color: var(--white-faint);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 6px;
        }}
        .footer-logo span {{ color: var(--gold); }}
        .footer-sub {{
            font-size: 11px;
            color: var(--white-faint);
            opacity: 0.6;
        }}

        /* ── SCROLL ANIMATION ─────────────────────────────── */
        @media (prefers-reduced-motion: no-preference) {{
            .fade-in {{
                opacity: 0;
                transform: translateY(16px);
                animation: fadeUp 0.5s ease forwards;
            }}
            .fade-in:nth-child(2) {{ animation-delay: 0.1s; }}
            .fade-in:nth-child(3) {{ animation-delay: 0.2s; }}
            @keyframes fadeUp {{
                to {{ opacity: 1; transform: translateY(0); }}
            }}
        }}
    </style>
</head>
<body>

    <!-- HEADER -->
    <header class="site-header">
        <a href="/" class="logo-mark">
            <div class="logo-icon">O</div>
            <span class="logo-text">Odin <span>Fitness</span></span>
        </a>
        <span class="header-code">{machine['code']}</span>
    </header>

    <!-- HERO -->
    <section class="hero">
        <div class="hero-badge">{machine['muscle_primary']}</div>
        <span class="hero-emoji">{machine['cover_emoji']}</span>
        <h1 class="hero-title">{machine['name']}</h1>
        <p class="hero-sub">Guía completa de uso y técnica</p>
        <div class="hero-muscles">{muscles_html}</div>
        <div class="hero-difficulty">
            <span class="difficulty-dot"></span>
            <span>{machine['difficulty']}</span>
        </div>
    </section>

    <div class="gold-divider"></div>

    <!-- CONTENIDO PRINCIPAL -->
    <main class="content">

        <!-- VIDEO -->
        <div class="video-section">
            {video_html}
            <p class="video-label">Video demostrativo de técnica correcta</p>
        </div>

        <!-- DESCRIPCIÓN -->
        <section class="section">
            <div class="section-label">Sobre esta máquina</div>
            <h2 class="section-title">¿Para qué sirve?</h2>
            <p class="description-text">{machine['description']}</p>
        </section>

        <!-- CONFIGURACIÓN -->
        <section class="section" style="background: var(--dark);">
            <div class="section-label">Antes de empezar</div>
            <h2 class="section-title">Ajustes Básicos</h2>
            <ol class="step-list">{setup_html}</ol>
        </section>

        <!-- CÓMO USAR -->
        <section class="section">
            <div class="section-label">Ejecución</div>
            <h2 class="section-title">Cómo Usarla</h2>
            <ol class="step-list">{how_html}</ol>
        </section>

        <!-- ERRORES COMUNES -->
        <section class="section" style="background: var(--dark);">
            <div class="section-label">Evitá lesiones</div>
            <h2 class="section-title">Errores Comunes</h2>
            <ul class="icon-list error-list">{errors_html}</ul>
        </section>

        <!-- CONSEJOS -->
        <section class="section">
            <div class="section-label">Optimizá tus resultados</div>
            <h2 class="section-title">Consejos de Ejecución</h2>
            <ul class="icon-list tips-list">{tips_html}</ul>
        </section>

        <!-- CTA COMERCIAL -->
        <section class="cta-section">
            <div class="cta-eyebrow">Odin Fitness — Equipamiento Profesional</div>
            <h2 class="cta-title">¿Querés equipar tu <em>gimnasio</em>?</h2>
            <p class="cta-sub">Equipamiento de nivel profesional importado. Financiación en cuotas fijas en dólares. Armado incluido.</p>

            <div class="cta-buttons">
                <a href="https://wa.me/541134673115?text=Hola%20Odin%20Fitness%2C%20estoy%20interesado%20en%20equipar%20mi%20gimnasio%20%F0%9F%92%AA"
                   class="btn btn-whatsapp" target="_blank" rel="noopener">
                    <span class="btn-icon">💬</span>
                    Hablar con un asesor
                </a>
                <a href="https://wa.me/541134673115?text=Hola%2C%20quisiera%20recibir%20el%20cat%C3%A1logo%20de%20Odin%20Fitness"
                   class="btn btn-catalog" target="_blank" rel="noopener">
                    <span class="btn-icon">📋</span>
                    Solicitar Catálogo
                </a>
                <a href="https://wa.me/541134673115?text=Hola%2C%20quisiera%20solicitar%20un%20presupuesto%20para%20mi%20gimnasio"
                   class="btn btn-budget" target="_blank" rel="noopener">
                    <span class="btn-icon">📊</span>
                    Pedir Presupuesto
                </a>
            </div>

            <div class="cta-trust">
                <div class="trust-item">
                    <span class="trust-num">+500</span>
                    <span class="trust-label">Equipos instalados</span>
                </div>
                <div class="trust-sep"></div>
                <div class="trust-item">
                    <span class="trust-num">6M</span>
                    <span class="trust-label">Garantía</span>
                </div>
                <div class="trust-sep"></div>
                <div class="trust-item">
                    <span class="trust-num">4M</span>
                    <span class="trust-label">Entrega</span>
                </div>
            </div>
        </section>

    </main>

    <!-- FOOTER -->
    <footer class="site-footer">
        <div class="footer-logo">Odin <span>Fitness</span></div>
        <p class="footer-sub">Av. Figueroa Alcorta 3351, Palermo, Buenos Aires</p>
    </footer>

</body>
</html>'''


# ─── INDEX PAGE ──────────────────────────────────────────────────────────────
def generate_index_html(machines):
    cards_html = ""
    for m in machines:
        muscles_preview = ", ".join(m["muscles"][:2])
        cards_html += f'''
        <a href="/{m['id']}.html" class="machine-card">
            <div class="card-emoji">{m['cover_emoji']}</div>
            <div class="card-info">
                <div class="card-code">{m['code']}</div>
                <div class="card-name">{m['name']}</div>
                <div class="card-muscles">{muscles_preview}</div>
            </div>
            <div class="card-arrow">→</div>
        </a>'''

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#0A0A0A">
    <title>Máquinas · Odin Fitness</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Barlow+Condensed:wght@600;700;800&display=swap" rel="stylesheet">
    <style>
        *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
        :root{{
            --black:#0A0A0A;--dark:#111;--surface:#181818;--border:#2A2A2A;
            --gold:#C8A951;--gold-glow:rgba(200,169,81,0.12);
            --white:#F5F5F5;--white-dim:#AAA;--white-faint:#666;
            --font-display:'Barlow Condensed',sans-serif;
            --font-body:'Inter',sans-serif;
        }}
        body{{background:var(--black);color:var(--white);font-family:var(--font-body);min-height:100vh;}}
        .header{{position:sticky;top:0;z-index:10;background:rgba(10,10,10,.95);backdrop-filter:blur(12px);border-bottom:1px solid var(--border);padding:14px 20px;display:flex;align-items:center;gap:10px;}}
        .logo-icon{{width:32px;height:32px;background:var(--gold);border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:800;color:#000;font-family:var(--font-display);}}
        .logo-text{{font-family:var(--font-display);font-size:18px;font-weight:700;text-transform:uppercase;}}
        .logo-text span{{color:var(--gold);}}
        .hero{{padding:32px 20px 24px;border-bottom:1px solid var(--border);}}
        .hero-label{{font-size:10px;color:var(--gold);text-transform:uppercase;letter-spacing:2px;font-weight:700;margin-bottom:8px;}}
        .hero-title{{font-family:var(--font-display);font-size:36px;font-weight:800;text-transform:uppercase;margin-bottom:8px;}}
        .hero-title span{{color:var(--gold);}}
        .hero-sub{{font-size:14px;color:var(--white-dim);line-height:1.5;}}
        .machines-list{{padding:16px 20px;display:flex;flex-direction:column;gap:10px;}}
        .machine-card{{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:16px;display:flex;align-items:center;gap:14px;text-decoration:none;color:inherit;transition:border-color .2s ease;}}
        .machine-card:active{{border-color:var(--gold);}}
        .card-emoji{{font-size:32px;flex-shrink:0;}}
        .card-info{{flex:1;min-width:0;}}
        .card-code{{font-size:10px;color:var(--white-faint);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:2px;}}
        .card-name{{font-family:var(--font-display);font-size:20px;font-weight:700;text-transform:uppercase;line-height:1.1;}}
        .card-muscles{{font-size:12px;color:var(--white-dim);margin-top:4px;}}
        .card-arrow{{color:var(--gold);font-size:18px;flex-shrink:0;}}
        .footer{{padding:24px 20px;text-align:center;border-top:1px solid var(--border);margin-top:8px;}}
        .footer-logo{{font-family:var(--font-display);font-size:14px;color:var(--white-faint);text-transform:uppercase;}}
        .footer-logo span{{color:var(--gold);}}
    </style>
</head>
<body>
    <header class="header">
        <div class="logo-icon">O</div>
        <div class="logo-text">Odin <span>Fitness</span></div>
    </header>
    <section class="hero">
        <div class="hero-label">Guías de Uso</div>
        <h1 class="hero-title">Máquinas <span>Odin</span></h1>
        <p class="hero-sub">Escaneá el QR de cada máquina o seleccioná una de la lista para ver su guía de uso completa.</p>
    </section>
    <div class="machines-list">{cards_html}</div>
    <footer class="footer">
        <div class="footer-logo">Odin <span>Fitness</span></div>
    </footer>
</body>
</html>'''


# ─── QR GENERATOR ────────────────────────────────────────────────────────────
def generate_qr(machine_id, machine_name):
    url = f"{BASE_URL}/{machine_id}.html"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=3,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        color_mask=SolidFillColorMask(
            front_color=(200, 169, 81),
            back_color=(15, 15, 15)
        )
    )
    
    # Convert to PIL Image for compositing
    img_pil = img.convert("RGB")
    
    # Add label below QR
    final_w = img_pil.size[0]
    label_h = 60
    final = Image.new("RGB", (final_w, img_pil.size[1] + label_h), (15, 15, 15))
    final.paste(img_pil, (0, 0))
    
    draw = ImageDraw.Draw(final)
    try:
        font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    except:
        font_big = ImageFont.load_default()
        font_small = font_big
    
    # Machine name
    text_y = img.size[1] + 10
    draw.text((final_w//2, text_y), machine_name, font=font_big, fill=(200, 169, 81), anchor="mt")
    draw.text((final_w//2, text_y + 26), "ODIN FITNESS", font=font_small, fill=(100, 100, 100), anchor="mt")
    draw.text((final_w//2, text_y + 42), "Escaneá para ver la guía", font=font_small, fill=(70, 70, 70), anchor="mt")
    
    qr_path = f"{QR_DIR}/qr-{machine_id}.png"
    final.save(qr_path)
    return qr_path


# ─── MAIN EXECUTION ──────────────────────────────────────────────────────────
print("🔱 Odin Fitness — Generando páginas web y QR codes...\n")

os.makedirs(QR_DIR, exist_ok=True)

# Generate machine pages
for machine in machines:
    html = generate_machine_html(machine)
    filepath = f"{OUTPUT_DIR}/machines/{machine['id']}.html"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ Página: /{machine['id']}.html  →  {machine['name']}")

# Generate index
index_html = generate_index_html(machines)
with open(f"{OUTPUT_DIR}/index.html", "w", encoding="utf-8") as f:
    f.write(index_html)
print(f"  ✓ Índice: /index.html")

# Generate QR codes
print("\n📱 Generando QR codes...\n")
for machine in machines:
    qr_path = generate_qr(machine["id"], machine["name"])
    print(f"  ✓ QR: {qr_path}")

print(f"\n✅ Todo generado en {OUTPUT_DIR}/")
print(f"   {len(machines)} páginas HTML + {len(machines)} QR codes + 1 índice")
