"""
Two images explaining partial vs total derivatives visually.

T(x, y) = x² + xy, point of interest (1, 1).

  Partial ∂T/∂x = 2x + y → at (1,1) = 3   (y frozen)
  Partial ∂T/∂y = x       → at (1,1) = 1   (x frozen)
  Total dT/dx along y=x   → at x=1  = 4   (both moving)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ── Surface ───────────────────────────────────────────────────────────────────
def T(x, y): return x**2 + x * y

x0, y0, z0 = 1.0, 1.0, T(1.0, 1.0)   # = (1, 1, 2)
dT_dx = 2 * x0 + y0   # = 3
dT_dy = x0             # = 1

x = np.linspace(0.0, 2.2, 60)
y = np.linspace(0.0, 2.2, 60)
X, Y = np.meshgrid(x, y)
Z = T(X, Y)

DARK = '#0d1117'
SURFACE_COL = '#1f6aa5'


def style_ax(ax):
    ax.set_facecolor(DARK)
    ax.tick_params(colors='#8b949e', labelsize=8)
    for pane in [ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane]:
        pane.fill = False
        pane.set_edgecolor('#30363d')
    ax.xaxis.label.set_color('#c9d1d9')
    ax.yaxis.label.set_color('#c9d1d9')
    ax.zaxis.label.set_color('#c9d1d9')
    ax.set_xlabel('x', labelpad=6)
    ax.set_ylabel('y', labelpad=6)
    ax.set_zlabel('T(x,y)', labelpad=6)
    ax.grid(False)


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 1 — Partial derivatives
# ══════════════════════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(13, 9), facecolor=DARK)
ax = fig.add_subplot(111, projection='3d')
style_ax(ax)
ax.view_init(elev=22, azim=225)

# Surface (translucent)
ax.plot_surface(X, Y, Z, alpha=0.22, color=SURFACE_COL, linewidth=0, zorder=1)

# Tangent plane at (1,1,2): T ≈ z0 + dT_dx*(x-x0) + dT_dy*(y-y0)
tx = np.linspace(0.2, 1.8, 12)
ty = np.linspace(0.2, 1.8, 12)
TX, TY = np.meshgrid(tx, ty)
TZ = z0 + dT_dx * (TX - x0) + dT_dy * (TY - y0)
ax.plot_surface(TX, TY, TZ, alpha=0.18, color='#f39c12', linewidth=0, zorder=2)
ax.text(1.9, 0.3, z0 + dT_dx * 0.9 + dT_dy * (-0.7) + 0.3,
        'tangent\nplane', color='#f39c12', fontsize=8, alpha=0.8)

# Surface slice at y=1 (red curve — what you "see" when y is frozen)
xs = np.linspace(0.0, 2.2, 80)
ax.plot(xs, np.ones_like(xs), T(xs, 1.0),
        color='#e74c3c', lw=1.2, alpha=0.5, linestyle='--', zorder=3)

# Surface slice at x=1 (green curve — what you see when x is frozen)
ys = np.linspace(0.0, 2.2, 80)
ax.plot(np.ones_like(ys), ys, T(1.0, ys),
        color='#2ecc71', lw=1.2, alpha=0.5, linestyle='--', zorder=3)

# Partial ∂T/∂x: tangent line along x, y held at 1
t = np.linspace(-0.7, 0.7, 40)
ax.plot(x0 + t, np.ones_like(t), z0 + dT_dx * t,
        color='#e74c3c', lw=3.0, zorder=6, label='∂T/∂x = 3  (y frozen at 1)')

# Partial ∂T/∂y: tangent line along y, x held at 1
ax.plot(np.ones_like(t), y0 + t, z0 + dT_dy * t,
        color='#2ecc71', lw=3.0, zorder=6, label='∂T/∂y = 1  (x frozen at 1)')

# Point
ax.scatter([x0], [y0], [z0], color='white', s=60, zorder=10)
ax.text(x0 + 0.05, y0 + 0.05, z0 + 0.15, '(1, 1, 2)', color='white',
        fontsize=9, fontweight='bold')

# Slope annotations on the tangent lines
ax.text(x0 + 0.55, 1.0, z0 + dT_dx * 0.55 + 0.1,
        'slope = 3', color='#e74c3c', fontsize=8.5)
ax.text(1.0, y0 + 0.45, z0 + dT_dy * 0.45 + 0.1,
        'slope = 1', color='#2ecc71', fontsize=8.5)

ax.set_title('Partial derivatives  —  T(x,y) = x² + xy\n'
             'Each partial freezes one variable and measures slope in the other direction',
             color='#c9d1d9', fontsize=11, pad=14)

leg = ax.legend(loc='upper left', facecolor='#161b22', edgecolor='#30363d',
                labelcolor='#c9d1d9', fontsize=9, framealpha=0.92)

# Annotation box
note = ("∂T/∂x: stand at (1,1), face east (+x).\n"
        "Freeze y=1. Slope of hill eastward = 3.\n\n"
        "∂T/∂y: same point, face north (+y).\n"
        "Freeze x=1. Slope of hill northward = 1.")
ax.text2D(0.98, 0.04, note, transform=ax.transAxes,
          ha='right', va='bottom', fontsize=8.5, color='#8b949e',
          fontfamily='monospace',
          bbox=dict(boxstyle='round,pad=0.5', facecolor='#161b22',
                    edgecolor='#30363d', alpha=0.92))

plt.tight_layout()
out1 = '/Users/max/repos/maxsimmonds.engineer/assets/math/01_partial_derivative.png'
plt.savefig(out1, dpi=160, bbox_inches='tight', facecolor=DARK)
plt.close()
print(f"Saved: {out1}")


# ══════════════════════════════════════════════════════════════════════════════
# IMAGE 2 — Total derivative
# ══════════════════════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(13, 9), facecolor=DARK)
ax = fig.add_subplot(111, projection='3d')
style_ax(ax)
ax.view_init(elev=22, azim=210)

# Surface
ax.plot_surface(X, Y, Z, alpha=0.22, color=SURFACE_COL, linewidth=0, zorder=1)

# Path y=x on the surface: (t, t, 2t²)
t_path = np.linspace(0.05, 2.1, 120)
ax.plot(t_path, t_path, T(t_path, t_path),
        color='#f39c12', lw=2.5, zorder=5, label='Path: y = x  on surface')

# Point
ax.scatter([x0], [y0], [z0], color='white', s=60, zorder=10)
ax.text(x0 + 0.05, y0 + 0.12, z0 + 0.18, '(1, 1, 2)', color='white',
        fontsize=9, fontweight='bold')

# Partial ∂T/∂x (y frozen) — dashed red for comparison
t = np.linspace(-0.65, 0.65, 40)
ax.plot(x0 + t, np.ones_like(t), z0 + dT_dx * t,
        color='#e74c3c', lw=2.2, linestyle='--', alpha=0.75, zorder=6,
        label='∂T/∂x = 3  (y frozen — partial)')

# Total derivative tangent along path y=x
# Path: p(t) = (t, t, 2t²)  →  dp/dt = (1, 1, 4t)  →  at t=1: (1, 1, 4)
# As a line from (1,1,2): direction (1,1,4), normalise x-step to match partial scale
s = np.linspace(-0.65, 0.65, 40)
# x advances by s, y advances by s (since dy/dx=1), z advances by 4s
ax.plot(x0 + s, y0 + s, z0 + 4.0 * s,
        color='#9b59b6', lw=3.0, zorder=7,
        label='dT/dx = 4  (along path — total)')

# Slope annotations
ax.text(x0 + 0.5, 1.0, z0 + dT_dx * 0.5 + 0.15,
        '∂T/∂x = 3', color='#e74c3c', fontsize=8.5, alpha=0.85)
ax.text(x0 + 0.42, y0 + 0.42, z0 + 4.0 * 0.42 + 0.15,
        'dT/dx = 4', color='#9b59b6', fontsize=8.5)

ax.set_title('Total derivative  —  T(x,y) = x² + xy\n'
             'Along path y=x, both x and y change together — slope is steeper',
             color='#c9d1d9', fontsize=11, pad=14)

leg = ax.legend(loc='upper left', facecolor='#161b22', edgecolor='#30363d',
                labelcolor='#c9d1d9', fontsize=9, framealpha=0.92)

note = ("Total derivative along path y=x:\n\n"
        "  dT/dx = ∂T/∂x + ∂T/∂y · dy/dx\n"
        "        =   3   +   1   ·   1\n"
        "        = 4\n\n"
        "The extra +1 comes from y also rising\n"
        "as you walk — ∂T/∂y · dy/dx accounts\n"
        "for that extra contribution.")
ax.text2D(0.98, 0.04, note, transform=ax.transAxes,
          ha='right', va='bottom', fontsize=8.5, color='#8b949e',
          fontfamily='monospace',
          bbox=dict(boxstyle='round,pad=0.5', facecolor='#161b22',
                    edgecolor='#30363d', alpha=0.92))

plt.tight_layout()
out2 = '/Users/max/repos/maxsimmonds.engineer/assets/math/02_total_derivative.png'
plt.savefig(out2, dpi=160, bbox_inches='tight', facecolor=DARK)
plt.close()
print(f"Saved: {out2}")
