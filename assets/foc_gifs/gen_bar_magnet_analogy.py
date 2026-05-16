"""
2-pole 3-slot outrunner: Phase A high / Phase B low.

Shows field lines from the A+B coil pair using 2D Biot-Savart (A_z contours).
Contours of A_z are field lines — same principle as stream function in axisymmetric FD.

Conductor positions verified with Biot-Savart:
  - Tooth A (30°): left slot @15° = +z (out), right slot @45° = -z (in)  → N pole
  - Tooth B (150°): left slot @135° = -z (in), right slot @165° = +z (out) → S pole
  - Tooth C (270°): inactive (floating phase)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

fig, ax = plt.subplots(figsize=(10, 10), facecolor='#0d1117')
ax.set_facecolor('#0d1117')
ax.set_xlim(-1.85, 1.85)
ax.set_ylim(-1.85, 1.85)
ax.set_aspect('equal')
ax.axis('off')

# ── Geometry ──────────────────────────────────────────────────────────────────
R_BACK     = 0.48   # stator back-iron outer radius
R_TOOTH_IN = 0.48
R_TOOTH_OUT = 0.95
R_BELL_IN  = 1.10
R_BELL_OUT = 1.42

th = np.linspace(0, 2 * np.pi, 600)

# Stator back iron
ax.fill(R_BACK * np.cos(th), R_BACK * np.sin(th), color='#2d333b', zorder=1)

# 3 teeth at 30°, 150°, 270°
TOOTH_HALF = 22  # half-width degrees
PHASE_COLS = {'A': '#e74c3c', 'B': '#2ecc71', 'C': '#3498db'}

for phase, deg in [('A', 30), ('B', 150), ('C', 270)]:
    a = np.deg2rad(deg)
    hw = np.deg2rad(TOOTH_HALF)
    th_t = np.linspace(a - hw, a + hw, 25)
    xs = np.concatenate([R_TOOTH_IN * np.cos(th_t), R_TOOTH_OUT * np.cos(th_t[::-1])])
    ys = np.concatenate([R_TOOTH_IN * np.sin(th_t), R_TOOTH_OUT * np.sin(th_t[::-1])])
    ax.fill(xs, ys, color='#2d333b', zorder=2)
    col = PHASE_COLS[phase]
    alpha = 0.85 if phase != 'C' else 0.3
    ax.plot(R_TOOTH_OUT * np.cos(th_t), R_TOOTH_OUT * np.sin(th_t),
            color=col, lw=2.2, alpha=alpha, zorder=3)
    r_lbl = R_TOOTH_OUT + 0.11
    ax.text(r_lbl * np.cos(a), r_lbl * np.sin(a), phase,
            ha='center', va='center', color=col, fontsize=14,
            fontweight='bold', alpha=alpha, zorder=10)

# Bell ring
xs = np.concatenate([R_BELL_IN * np.cos(th), R_BELL_OUT * np.cos(th[::-1])])
ys = np.concatenate([R_BELL_IN * np.sin(th), R_BELL_OUT * np.sin(th[::-1])])
ax.fill(xs, ys, color='#21262d', zorder=3)

# N magnet (top arc, 32°–148°)
th_N = np.deg2rad(np.linspace(33, 147, 60))
xs = np.concatenate([R_BELL_IN * np.cos(th_N), R_BELL_OUT * np.cos(th_N[::-1])])
ys = np.concatenate([R_BELL_IN * np.sin(th_N), R_BELL_OUT * np.sin(th_N[::-1])])
ax.fill(xs, ys, color='#7b241c', alpha=0.92, zorder=4)
rm = (R_BELL_IN + R_BELL_OUT) / 2
ax.text(rm * np.cos(np.deg2rad(90)), rm * np.sin(np.deg2rad(90)),
        'N', ha='center', va='center', fontsize=13, color='white', fontweight='bold', zorder=5)

# S magnet (bottom arc, 212°–328°)
th_S = np.deg2rad(np.linspace(213, 327, 60))
xs = np.concatenate([R_BELL_IN * np.cos(th_S), R_BELL_OUT * np.cos(th_S[::-1])])
ys = np.concatenate([R_BELL_IN * np.sin(th_S), R_BELL_OUT * np.sin(th_S[::-1])])
ax.fill(xs, ys, color='#1a5276', alpha=0.92, zorder=4)
ax.text(rm * np.cos(np.deg2rad(270)), rm * np.sin(np.deg2rad(270)),
        'S', ha='center', va='center', fontsize=13, color='white', fontweight='bold', zorder=5)

# ── Conductors ────────────────────────────────────────────────────────────────
# Each tooth coil has two slot conductors — one on each side of the tooth.
# Signs verified analytically: tooth A → N, tooth B → S.
R_C = 0.68

wires = [
    (15,  +1, '#e74c3c'),   # A left slot:  out of page (●)
    (45,  -1, '#e74c3c'),   # A right slot: into page  (×)
    (135, -1, '#2ecc71'),   # B left slot:  into page  (×)
    (165, +1, '#2ecc71'),   # B right slot: out of page (●)
]

wire_xy = []
for deg, I, col in wires:
    a = np.deg2rad(deg)
    x0, y0 = R_C * np.cos(a), R_C * np.sin(a)
    wire_xy.append((x0, y0, I))
    s = 0.042
    if I > 0:
        ax.plot(x0, y0, 'o', ms=10, color=col, zorder=8)
        ax.plot(x0, y0, '.', ms=4, color='white', zorder=9)
    else:
        ax.plot(x0, y0, 'o', ms=10, color=col, zorder=8)
        ax.plot([x0 - s, x0 + s], [y0 - s, y0 + s], '-', lw=1.8, color='white', zorder=9)
        ax.plot([x0 + s, x0 - s], [y0 - s, y0 + s], '-', lw=1.8, color='white', zorder=9)

# ── A_z field via 2D Biot-Savart ──────────────────────────────────────────────
# A_z from a line current I: A_z ∝ -I * ln(r)
# Field lines = contours of A_z  (B = curl A → B·∇A_z = 0 in 2D)
N_GRID = 500
ext = 1.75
x = np.linspace(-ext, ext, N_GRID)
y = np.linspace(-ext, ext, N_GRID)
X, Y = np.meshgrid(x, y)

Az = np.zeros((N_GRID, N_GRID))
for x0, y0, I in wire_xy:
    r2 = (X - x0) ** 2 + (Y - y0) ** 2
    r2 = np.maximum(r2, 1e-5)
    Az += I * (-np.log(np.sqrt(r2)))

R_GRID = np.sqrt(X ** 2 + Y ** 2)

# Show field lines inside the stator and in the air gap; hide inside bell iron
mask = (R_GRID > 0.12) & (R_GRID < R_BELL_IN)
Az_plot = np.where(mask, Az, np.nan)

# Pick contour levels from the air-gap region (where the interesting loops cross)
mask_gap = (R_GRID > R_TOOTH_OUT + 0.01) & (R_GRID < R_BELL_IN - 0.01)
az_gap = Az[mask_gap]
lo, hi = np.percentile(az_gap, [4, 96])
n_levels = 35
levels = np.linspace(lo, hi, n_levels)

ax.contour(X, Y, Az_plot, levels=levels,
           colors='#4a8fcc', linewidths=0.85, alpha=0.70, zorder=6)

# ── N / S pole labels on tooth tips ──────────────────────────────────────────
# Tooth A is the N pole of the equivalent bar magnet, tooth B is S
for label, deg, col in [('N', 30, '#e74c3c'), ('S', 150, '#2ecc71')]:
    a = np.deg2rad(deg)
    r_tip = R_TOOTH_OUT - 0.14
    ax.text(r_tip * np.cos(a), r_tip * np.sin(a), label,
            ha='center', va='center', fontsize=12, color=col,
            fontweight='bold', zorder=11,
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#0d1117',
                      edgecolor=col, alpha=0.85))

# ── Vectors ───────────────────────────────────────────────────────────────────
# Stator MMF: from B(S at 150°) toward A(N at 30°) → points in +x direction
ax.annotate('', xy=(0.58, 0.0), xytext=(-0.58, 0.0),
            arrowprops=dict(arrowstyle='->', color='#f39c12', lw=2.8, mutation_scale=20),
            zorder=13)
ax.text(0, -0.14, 'Stator MMF (q-axis)', ha='center', va='top',
        fontsize=9, color='#f39c12', fontweight='bold', zorder=13)

# Rotor flux: S (bottom) to N (top) → points in +y direction
ax.annotate('', xy=(0.0, 0.52), xytext=(0.0, -0.42),
            arrowprops=dict(arrowstyle='->', color='#9b59b6', lw=2.0,
                            mutation_scale=16),
            zorder=13)
ax.text(0.10, 0.08, 'Rotor\nflux', ha='left', va='center',
        fontsize=8.5, color='#9b59b6', zorder=13)

# 90° arc between the two vectors
arc_r = 0.22
arc_th = np.linspace(np.deg2rad(0), np.deg2rad(90), 40)
ax.plot(arc_r * np.cos(arc_th), arc_r * np.sin(arc_th),
        color='#ffffff', lw=1.0, alpha=0.45, zorder=13)
ax.text(0.18, 0.12, '90°', ha='left', va='bottom',
        fontsize=8, color='#ffffff', alpha=0.6, zorder=13)

# ── "Bar magnet" annotation box ───────────────────────────────────────────────
txt = ("A + B coil pair ≡ bar magnet\n"
       "  ← S (tooth B)  |  N (tooth A) →\n"
       "PM 'sees' this as one bar magnet,\n"
       "90° ahead of its own flux.")
ax.text(0.98, 0.98, txt, transform=ax.transAxes,
        ha='right', va='top', fontsize=8.5, color='#8b949e',
        fontfamily='monospace',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#161b22',
                  edgecolor='#30363d', alpha=0.9))

# ── Title ─────────────────────────────────────────────────────────────────────
ax.set_title('2-pole 3-slot outrunner  ·  Phase A high / Phase B low\n'
             'Blue lines = A+B field lines   '
             'Tooth A = N pole, Tooth B = S pole of equivalent bar magnet',
             color='#c9d1d9', fontsize=10, pad=12)

# ── Legend ────────────────────────────────────────────────────────────────────
legend_els = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#e74c3c',
           markersize=8, label='Phase A conductors'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#2ecc71',
           markersize=8, label='Phase B conductors'),
    Line2D([0], [0], color='#4a8fcc', lw=1.5, label='Stator field lines'),
    Line2D([0], [0], color='#f39c12', lw=2.2, label='Stator MMF vector'),
    Line2D([0], [0], color='#9b59b6', lw=2.0, label='Rotor flux vector'),
    mpatches.Patch(color='#7b241c', label='N pole (bell PM)'),
    mpatches.Patch(color='#1a5276', label='S pole (bell PM)'),
]
ax.legend(handles=legend_els, loc='lower right',
          facecolor='#161b22', edgecolor='#30363d',
          labelcolor='#c9d1d9', fontsize=8.5, framealpha=0.92)

plt.tight_layout(pad=0.5)
out = '/Users/max/repos/maxsimmonds.engineer/assets/foc_gifs/17_bar_magnet_analogy.png'
plt.savefig(out, dpi=160, bbox_inches='tight', facecolor='#0d1117')
plt.close()
print(f"Saved: {out}")
