import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Arc
from matplotlib.lines import Line2D

fig, ax = plt.subplots(figsize=(11, 11), facecolor='#0d1117')
ax.set_facecolor('#0d1117')
ax.set_xlim(-2.3, 2.3)
ax.set_ylim(-2.3, 2.3)
ax.set_aspect('equal')
ax.axis('off')

Q = 24; P = 22

# Radii
R_BELL_IN  = 1.30
R_BELL_OUT = 1.55
R_TOOTH_OUT = 1.20
R_TOOTH_IN  = 0.78
R_BORE_OUT  = 0.72

th = np.linspace(0, 2*np.pi, 500)

# ── Slot positions (mechanical) ──────────────────────────────────
slot_mech = np.array([i * 2*np.pi / Q for i in range(Q)])

# Phase assignments (0-indexed) from star-of-slots for 24N22P
A_plus  = [0, 2, 11, 13]   # slots 1,3,12,14
A_minus = [1, 12, 14, 23]  # slots 2,13,15,24
B_plus  = [3, 5, 16, 18]   # slots 4,6,17,19
B_minus = [4, 6, 15, 17]   # slots 5,7,16,18
C_plus  = [8, 10, 19, 21]
C_minus = [7, 9, 20, 22]

slot_phase = [''] * Q
for i in A_plus:  slot_phase[i] = 'A+'
for i in A_minus: slot_phase[i] = 'A-'
for i in B_plus:  slot_phase[i] = 'B+'
for i in B_minus: slot_phase[i] = 'B-'
for i in C_plus:  slot_phase[i] = 'C+'
for i in C_minus: slot_phase[i] = 'C-'

# A high (+1), B low (−1), C floating (0)
# A+ → dot (+1), A− → cross (−1)
# B+ → cross (B reversed, −1), B− → dot (B reversed, +1)
current = np.zeros(Q)
for i in A_plus:  current[i] = +1.0
for i in A_minus: current[i] = -1.0
for i in B_plus:  current[i] = -1.0
for i in B_minus: current[i] = +1.0

# ── Rotor position for near-maximum torque with A+B− ─────────────
# Current space vector for A+B− points at −30° (Clarke transform)
# Max torque: rotor flux 90° behind → rotor flux at −120° = 240°
# Mechanical angle = electrical / (P/2) = 240/11 ≈ 21.8°
theta_rotor = np.deg2rad(21.8)

# ── PM polarity at each slot ─────────────────────────────────────
def pm_polarity(mech_angle, theta_r):
    """N=+1, S=−1"""
    angle = (mech_angle - theta_r) % (2*np.pi)
    pole_idx = int(angle / (2*np.pi / P))
    return +1 if pole_idx % 2 == 0 else -1

pm_pol = np.array([pm_polarity(a, theta_rotor) for a in slot_mech])

# ── Force on each conductor: F = I × L × B, tangential ──────────
# dot (+z) under N (B inward, −r̂): F = (+ẑ)×(−r̂) = −θ̂ (CW)
# dot (+z) under S (B outward, +r̂): F = (+ẑ)×(+r̂) = +θ̂ (CCW)
# → force_sign = −(current × pm_pol)
# CCW tangential unit vector at angle φ = (−sinφ, cosφ)

force_tang = np.zeros(Q)   # +1=CCW, −1=CW
for i in range(Q):
    if current[i] == 0:
        continue
    force_tang[i] = -(current[i] * pm_pol[i])

# Cartesian force vectors (acting at R_TOOTH_OUT radius)
force_xy = np.array([
    (force_tang[i] * (-np.sin(slot_mech[i])),
     force_tang[i] *   np.cos(slot_mech[i]))
    for i in range(Q)
])
net_force = force_xy.sum(axis=0)
net_torque = force_tang[force_tang != 0].sum()   # scalar, proportional to τ

# ── Draw back-iron ring ──────────────────────────────────────────
xs = np.concatenate([R_BORE_OUT*np.cos(th), R_TOOTH_IN*np.cos(th[::-1])])
ys = np.concatenate([R_BORE_OUT*np.sin(th), R_TOOTH_IN*np.sin(th[::-1])])
ax.fill(xs, ys, color='#21262d', zorder=1)

# ── Draw stator teeth ────────────────────────────────────────────
tooth_span = 0.72 * (2*np.pi / Q)
for i in range(Q):
    a = slot_mech[i]
    th_t = np.linspace(a - tooth_span/2, a + tooth_span/2, 15)
    xs = np.concatenate([R_TOOTH_IN*np.cos(th_t), R_TOOTH_OUT*np.cos(th_t[::-1])])
    ys = np.concatenate([R_TOOTH_IN*np.sin(th_t), R_TOOTH_OUT*np.sin(th_t[::-1])])
    ax.fill(xs, ys, color='#2d333b', zorder=2)

# ── Draw bell ring ───────────────────────────────────────────────
xs = np.concatenate([R_BELL_IN*np.cos(th), R_BELL_OUT*np.cos(th[::-1])])
ys = np.concatenate([R_BELL_IN*np.sin(th), R_BELL_OUT*np.sin(th[::-1])])
ax.fill(xs, ys, color='#21262d', zorder=3)

# ── Draw PM segments ─────────────────────────────────────────────
for k in range(P):
    pa = theta_rotor + k * 2*np.pi / P
    is_N = (k % 2 == 0)
    col = '#7b241c' if is_N else '#1a5276'
    th_s = np.linspace(pa + 0.02, pa + 2*np.pi/P - 0.02, 25)
    xs = np.concatenate([R_BELL_IN*np.cos(th_s), R_BELL_OUT*np.cos(th_s[::-1])])
    ys = np.concatenate([R_BELL_IN*np.sin(th_s), R_BELL_OUT*np.sin(th_s[::-1])])
    ax.fill(xs, ys, color=col, alpha=0.92, zorder=4)
    mid_a = pa + np.pi/P
    rl = (R_BELL_IN + R_BELL_OUT) / 2
    ax.text(rl*np.cos(mid_a), rl*np.sin(mid_a),
            'N' if is_N else 'S',
            ha='center', va='center', fontsize=5.5,
            color='#ecf0f1', fontweight='bold', zorder=5)

# ── Current symbols and force arrows ────────────────────────────
slot_r = (R_TOOTH_IN + R_TOOTH_OUT) / 2
ARROW_SCALE = 0.42

PC = {'A': '#e74c3c', 'B': '#2ecc71', 'C': '#3498db'}

for i in range(Q):
    a = slot_mech[i]
    ph = slot_phase[i]
    cur = current[i]
    base = ph[0] if ph else 'C'
    col = PC.get(base, '#666666')

    sx = slot_r * np.cos(a)
    sy = slot_r * np.sin(a)

    if cur == 0:
        # C phase — dim dot
        ax.plot(sx, sy, 'o', ms=4, color='#3498db', alpha=0.25, zorder=6)
        continue

    # Current symbol
    if cur > 0:
        ax.plot(sx, sy, 'o', ms=6, color=col, zorder=7)
        ax.plot(sx, sy, '.', ms=2.5, color='white', zorder=8)
    else:
        ax.plot(sx, sy, 'o', ms=6, color=col, zorder=7)
        ax.plot([sx-0.022, sx+0.022], [sy-0.022, sy+0.022], '-', lw=1.2,
                color='white', zorder=8)
        ax.plot([sx+0.022, sx-0.022], [sy-0.022, sy+0.022], '-', lw=1.2,
                color='white', zorder=8)

    # Force arrow (tangential, from outer tooth face)
    ft = force_tang[i]
    if ft == 0:
        continue
    arr_col = '#FFD700' if ft > 0 else '#e67e22'
    ox = R_TOOTH_OUT * np.cos(a)
    oy = R_TOOTH_OUT * np.sin(a)
    dx = ft * (-np.sin(a)) * ARROW_SCALE
    dy = ft *   np.cos(a)  * ARROW_SCALE
    ax.annotate('', xy=(ox + dx, oy + dy), xytext=(ox, oy),
                arrowprops=dict(arrowstyle='->', color=arr_col,
                                lw=1.8, mutation_scale=10), zorder=9)

# ── Net force vector (at centre) ─────────────────────────────────
nf_scale = 0.07  # scale down so it fits nicely at centre
nfx = net_force[0] * nf_scale
nfy = net_force[1] * nf_scale
ax.annotate('', xy=(nfx, nfy), xytext=(0, 0),
            arrowprops=dict(arrowstyle='->', color='#FFD700',
                            lw=3.5, mutation_scale=22), zorder=10)

# ── Net torque arc on bell ────────────────────────────────────────
arc_r = R_BELL_OUT + 0.15
if net_torque > 0:   # CCW
    arc_th = np.linspace(np.deg2rad(200), np.deg2rad(340), 60)
    arrow_nudge = +0.14
else:                # CW  (our case)
    arc_th = np.linspace(np.deg2rad(340), np.deg2rad(200), 60)
    arrow_nudge = -0.14

ax.plot(arc_r*np.cos(arc_th), arc_r*np.sin(arc_th),
        color='#2ecc71', lw=2.8, zorder=10)
end_a = arc_th[-1]
ax.annotate('',
            xy=(arc_r*np.cos(end_a + arrow_nudge),
                arc_r*np.sin(end_a + arrow_nudge)),
            xytext=(arc_r*np.cos(end_a), arc_r*np.sin(end_a)),
            arrowprops=dict(arrowstyle='->', color='#2ecc71',
                            lw=2.8, mutation_scale=18), zorder=10)
ax.text(0, -(arc_r + 0.18), 'τ  (CW)' if net_torque < 0 else 'τ  (CCW)',
        ha='center', va='center', fontsize=13, color='#2ecc71', fontweight='bold')

# ── Labels ───────────────────────────────────────────────────────
# Net force label
ax.text(nfx + 0.12, nfy + 0.08, 'Net F', fontsize=9,
        color='#FFD700', fontfamily='monospace', fontweight='bold', zorder=11)

# Title
ax.set_title('24N22P Outrunner  —  Phase A High / Phase B Low\n'
             'Yellow arrows = EM force on each conductor   '
             'Green arc = net torque on bell',
             color='#c9d1d9', fontsize=11, pad=10)

# ── Math annotation box ───────────────────────────────────────────
math_txt = (
    "F = I·L×B  (tangential)\n"
    f"Active slots: A(×8) + B(×8) = 16 conductors\n"
    f"Force tally:  CCW={int((force_tang>0).sum())}   CW={int((force_tang<0).sum())}   off={int((force_tang==0).sum())}\n"
    f"Net torque ∝  {net_torque:+.1f} units\n"
    "Net linear force ≈ 0  (forces cancel, torque adds)"
)
ax.text(0.98, 0.02, math_txt, transform=ax.transAxes,
        ha='right', va='bottom', fontsize=8.5, color='#8b949e',
        fontfamily='monospace',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#161b22',
                  edgecolor='#30363d', alpha=0.9))

# ── Legend ────────────────────────────────────────────────────────
legend_els = [
    Line2D([0],[0], marker='o', color='w', markerfacecolor='#e74c3c',
           markersize=8, label='Phase A (high)'),
    Line2D([0],[0], marker='o', color='w', markerfacecolor='#2ecc71',
           markersize=8, label='Phase B (low)'),
    Line2D([0],[0], marker='o', color='w', markerfacecolor='#3498db',
           markersize=8, label='Phase C (off)', alpha=0.4),
    Line2D([0],[0], color='#FFD700', lw=2, label='EM force (CCW)'),
    Line2D([0],[0], color='#e67e22', lw=2, label='EM force (CW)'),
    Line2D([0],[0], color='#2ecc71', lw=2, label='Net torque τ'),
    mpatches.Patch(color='#7b241c', label='N pole'),
    mpatches.Patch(color='#1a5276', label='S pole'),
]
ax.legend(handles=legend_els, loc='lower right',
          facecolor='#161b22', edgecolor='#30363d',
          labelcolor='#c9d1d9', fontsize=8.5,
          framealpha=0.92)

plt.tight_layout(pad=0.5)
plt.savefig('/Users/max/repos/maxsimmonds.engineer/assets/foc_gifs/12_commutation_step.png',
            dpi=160, bbox_inches='tight', facecolor='#0d1117')
plt.close()
print(f"Saved. CCW forces: {int((force_tang>0).sum())}, CW: {int((force_tang<0).sum())}, net torque: {net_torque:.1f}")
