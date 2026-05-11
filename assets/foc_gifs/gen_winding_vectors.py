import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

Q = 24; P = 22
alpha_e = (P / 2) * (360.0 / Q)  # 165°/slot

slot_angles_deg = [(n * alpha_e) % 360 for n in range(Q)]
slot_angles_rad = np.deg2rad(slot_angles_deg)

def assign_phase(a):
    a = a % 360
    if a >= 330 or a < 30:  return 'A+'
    elif a < 90:             return 'C-'
    elif a < 150:            return 'B+'
    elif a < 210:            return 'A-'
    elif a < 270:            return 'C+'
    else:                    return 'B-'

phases = [assign_phase(a) for a in slot_angles_deg]

PC = {'A+': '#e74c3c', 'A-': '#c0392b',
      'B+': '#2ecc71', 'B-': '#27ae60',
      'C+': '#3498db', 'C-': '#2980b9'}

# Phase A vectors after current reversal
a_vecs_deg = []
for i, ph in enumerate(phases):
    if ph == 'A+': a_vecs_deg.append(slot_angles_deg[i])
    elif ph == 'A-': a_vecs_deg.append((slot_angles_deg[i] + 180) % 360)

a_vecs_deg_sorted = sorted(a_vecs_deg)
a_vecs_rad = np.deg2rad(a_vecs_deg_sorted)

rx = sum(np.cos(v) for v in a_vecs_rad)
ry = sum(np.sin(v) for v in a_vecs_rad)
resultant_mag = np.sqrt(rx**2 + ry**2)
kd = resultant_mag / 8

# ── GIF 1: Star of Slots ─────────────────────────────────────────
fig1, ax1 = plt.subplots(figsize=(7, 7), facecolor='#0d1117')

def draw_sos(frame):
    ax1.clear()
    ax1.set_facecolor('#0d1117')
    ax1.set_xlim(-1.75, 1.75); ax1.set_ylim(-1.75, 1.75)
    ax1.set_aspect('equal'); ax1.axis('off')

    th = np.linspace(0, 2*np.pi, 300)
    ax1.plot(np.cos(th), np.sin(th), color='#30363d', lw=1)

    sectors = ['A+','C-','B+','A-','C+','B-']
    sec_cols = ['#e74c3c','#3498db','#2ecc71','#e74c3c','#3498db','#2ecc71']
    for k in range(6):
        bd = np.deg2rad(k * 60 - 30)
        ax1.plot([0, 1.45*np.cos(bd)], [0, 1.45*np.sin(bd)],
                 color='#30363d', lw=0.7, ls='--')
        ca = np.deg2rad(k * 60)
        ax1.text(1.6*np.cos(ca), 1.6*np.sin(ca), sectors[k],
                 ha='center', va='center', fontsize=9,
                 color=sec_cols[k] + '99', fontfamily='monospace', fontweight='bold')

    n_show = min(frame + 1, Q)
    for i in range(n_show):
        a = slot_angles_rad[i]
        ph = phases[i]
        col = PC[ph]
        is_A = 'A' in ph
        lw = 2.8 if is_A else 1.0
        alpha = 1.0 if is_A else 0.3

        ax1.annotate('', xy=(np.cos(a), np.sin(a)), xytext=(0, 0),
                     arrowprops=dict(arrowstyle='->', color=col,
                                     lw=lw, alpha=alpha, mutation_scale=11))
        ax1.text(1.18*np.cos(a), 1.18*np.sin(a), str(i+1),
                 ha='center', va='center', fontsize=7, color=col,
                 alpha=alpha, fontfamily='monospace')

    if frame >= Q + 8:
        # Normalised resultant direction
        scale = resultant_mag / 8
        ax1.annotate('', xy=(scale*np.cos(np.arctan2(ry,rx)),
                              scale*np.sin(np.arctan2(ry,rx))),
                     xytext=(0, 0),
                     arrowprops=dict(arrowstyle='->', color='#FFD700',
                                     lw=3.5, mutation_scale=20))
        ax1.text(0, -1.65,
                 f'Phase A resultant   kd = {kd:.4f}',
                 ha='center', fontsize=10.5, color='#FFD700',
                 fontfamily='monospace', fontweight='bold')

    ax1.set_title('Star of Slots  —  24N22P\nPhase A = red  |  others faded',
                  color='#c9d1d9', fontsize=11, pad=8)

ani1 = FuncAnimation(fig1, draw_sos, frames=Q + 30, interval=130)
ani1.save('09_star_of_slots.gif', writer=PillowWriter(fps=7))
plt.close(fig1)
print("GIF 1 done")

# ── GIF 2: Tip-to-tail addition ───────────────────────────────────
fig2, ax2 = plt.subplots(figsize=(9, 6), facecolor='#0d1117')

SHADES = ['#ff6b6b','#e74c3c','#ff4444','#c0392b',
          '#ff6b6b','#e74c3c','#ff4444','#c0392b']
FRAMES_TT = 8 * 8 + 35

def draw_tiptail(frame):
    ax2.clear()
    ax2.set_facecolor('#0d1117')
    ax2.set_xlim(-0.8, 9.5); ax2.set_ylim(-2.5, 2.5)
    ax2.set_aspect('equal'); ax2.axis('off')

    n_shown = min(frame // 8 + 1, 8)

    cx, cy = 0.0, 0.0
    for i in range(n_shown):
        vx = np.cos(a_vecs_rad[i])
        vy = np.sin(a_vecs_rad[i])
        nx, ny = cx + vx, cy + vy
        ax2.annotate('', xy=(nx, ny), xytext=(cx, cy),
                     arrowprops=dict(arrowstyle='->', color=SHADES[i],
                                     lw=2.5, mutation_scale=14))
        perp = np.deg2rad(a_vecs_deg_sorted[i] + 90)
        lx = (cx + nx)/2 + 0.22*np.cos(perp)
        ly = (cy + ny)/2 + 0.22*np.sin(perp)
        ax2.text(lx, ly, f'{int(a_vecs_deg_sorted[i])}°',
                 fontsize=8.5, color=SHADES[i], ha='center', va='center',
                 fontfamily='monospace')
        cx, cy = nx, ny

    # Resultant once all shown
    if n_shown == 8 and frame >= 8 * 8 + 10:
        ax2.annotate('', xy=(rx, ry), xytext=(0, 0),
                     arrowprops=dict(arrowstyle='->', color='#FFD700',
                                     lw=3.5, mutation_scale=20))
        ax2.text(rx/2, ry - 0.45,
                 f'|R| = {resultant_mag:.3f}', fontsize=10,
                 color='#FFD700', ha='center', fontfamily='monospace')
        ax2.text(rx/2, ry - 0.85,
                 f'kd = {kd:.4f}', fontsize=11,
                 color='#FFD700', ha='center', fontfamily='monospace',
                 fontweight='bold')
        # Ghost max
        ax2.annotate('', xy=(8, 0), xytext=(0, 0),
                     arrowprops=dict(arrowstyle='->', color='#ffffff1a',
                                     lw=1.5, mutation_scale=12))
        ax2.text(8.35, 0.12, '8.0 (max)', fontsize=8, color='#ffffff33',
                 va='center', fontfamily='monospace')

    ax2.text(4.0, -2.3,
             f'Adding vector {min(n_shown,8)} / 8  —  Phase A EMF phasors  (tip-to-tail)',
             ha='center', fontsize=9.5, color='#8b949e', fontfamily='monospace')
    ax2.set_title('Phase A: Tip-to-Tail Vector Addition',
                  color='#c9d1d9', fontsize=12, pad=8)

ani2 = FuncAnimation(fig2, draw_tiptail, frames=FRAMES_TT, interval=80)
ani2.save('10_vector_addition.gif', writer=PillowWriter(fps=12))
plt.close(fig2)
print("GIF 2 done")

# ── GIF 3: Rotor force ────────────────────────────────────────────
fig3, ax3 = plt.subplots(figsize=(7, 7), facecolor='#0d1117')

R_BELL = 1.0
R_TOOTH_OUT = 0.70
R_TOOTH_IN  = 0.46
FRAMES_RF = 100

def draw_rotor_force(frame):
    ax3.clear()
    ax3.set_facecolor('#0d1117')
    ax3.set_xlim(-1.65, 1.65); ax3.set_ylim(-1.65, 1.65)
    ax3.set_aspect('equal'); ax3.axis('off')

    th = np.linspace(0, 2*np.pi, 300)
    t = frame / FRAMES_RF * 2 * np.pi

    rotor_mech = t * 0.7                  # bell rotates
    rotor_flux_angle = rotor_mech         # PM flux direction
    mmf_angle = rotor_flux_angle + np.pi/2  # FOC keeps MMF 90° ahead

    # Bell ring
    for r0, r1, col in [(R_BELL, R_BELL+0.18, '#21262d')]:
        xs = np.concatenate([r0*np.cos(th), r1*np.cos(th[::-1])])
        ys = np.concatenate([r0*np.sin(th), r1*np.sin(th[::-1])])
        ax3.fill(xs, ys, color=col)

    # PM segments on bell
    for pi in range(P):
        pa = rotor_mech + pi * 2*np.pi / P
        is_N = (pi % 2 == 0)
        col = '#922b21' if is_N else '#1a5276'
        th_s = np.linspace(pa + 0.04, pa + 2*np.pi/P - 0.04, 20)
        xs = np.concatenate([R_BELL*np.cos(th_s),
                             (R_BELL+0.16)*np.cos(th_s[::-1])])
        ys = np.concatenate([R_BELL*np.sin(th_s),
                             (R_BELL+0.16)*np.sin(th_s[::-1])])
        ax3.fill(xs, ys, color=col, alpha=0.9)
        # N/S label on every other pole
        if pi % 2 == 0:
            mid_a = pa + np.pi/P
            rlab = R_BELL + 0.08
            ax3.text(rlab*np.cos(mid_a), rlab*np.sin(mid_a),
                     'N' if is_N else 'S',
                     ha='center', va='center', fontsize=5.5,
                     color='#ecf0f1', fontweight='bold')

    # Stator back-iron
    ax3.fill_between(th*0 + R_TOOTH_IN - 0.06,  # placeholder
                     -2, -2)  # blank
    back_xs = np.concatenate([(R_TOOTH_IN-0.06)*np.cos(th),
                               (R_TOOTH_IN-0.14)*np.cos(th[::-1])])
    back_ys = np.concatenate([(R_TOOTH_IN-0.06)*np.sin(th),
                               (R_TOOTH_IN-0.14)*np.sin(th[::-1])])
    ax3.fill(back_xs, back_ys, color='#21262d')

    # Stator teeth + current indicators
    for si in range(Q):
        slot_a = si * 2*np.pi / Q
        tw = 0.75 * (2*np.pi/Q)
        th_t = np.linspace(slot_a - tw/2, slot_a + tw/2, 12)
        xs = np.concatenate([R_TOOTH_IN*np.cos(th_t),
                             R_TOOTH_OUT*np.cos(th_t[::-1])])
        ys = np.concatenate([R_TOOTH_IN*np.sin(th_t),
                             R_TOOTH_OUT*np.sin(th_t[::-1])])
        ax3.fill(xs, ys, color='#2d333b', alpha=0.95)

        ph = phases[si]
        col = PC[ph]
        base = 'A' if 'A' in ph else ('B' if 'B' in ph else 'C')
        offset = 0 if base == 'A' else (2*np.pi/3 if base == 'B' else 4*np.pi/3)
        current = np.cos(t - offset) * (-1 if ph[1] == '-' else 1)

        slot_r = (R_TOOTH_IN + R_TOOTH_OUT) / 2
        sx = slot_r * np.cos(slot_a)
        sy = slot_r * np.sin(slot_a)
        if abs(current) > 0.15:
            marker = '●' if current > 0 else '✕'
            ax3.text(sx, sy, marker, ha='center', va='center',
                     fontsize=6, color=col,
                     alpha=min(1.0, abs(current) * 1.4))

    # Net stator MMF vector
    mmf_scale = 0.52
    ax3.annotate('', xy=(mmf_scale*np.cos(mmf_angle),
                          mmf_scale*np.sin(mmf_angle)),
                 xytext=(0, 0),
                 arrowprops=dict(arrowstyle='->', color='#FFD700',
                                 lw=3.0, mutation_scale=20))
    ax3.text(0.72*np.cos(mmf_angle), 0.72*np.sin(mmf_angle),
             'MMF', ha='center', va='center', fontsize=9,
             color='#FFD700', fontfamily='monospace', fontweight='bold')

    # Rotor flux vector
    flux_scale = 0.40
    ax3.annotate('', xy=(flux_scale*np.cos(rotor_flux_angle),
                          flux_scale*np.sin(rotor_flux_angle)),
                 xytext=(0, 0),
                 arrowprops=dict(arrowstyle='->', color='#e74c3c',
                                 lw=2.5, mutation_scale=16))
    ax3.text(0.58*np.cos(rotor_flux_angle), 0.58*np.sin(rotor_flux_angle),
             'Φ_r', ha='center', va='center', fontsize=9,
             color='#e74c3c', fontfamily='monospace', fontweight='bold')

    # 90° arc
    arc_r = 0.24
    arc_th = np.linspace(rotor_flux_angle, mmf_angle, 40)
    ax3.plot(arc_r*np.cos(arc_th), arc_r*np.sin(arc_th),
             color='#ffffff55', lw=1.5, ls='--')
    mid_a = (rotor_flux_angle + mmf_angle) / 2
    ax3.text(0.34*np.cos(mid_a), 0.34*np.sin(mid_a), '90°',
             ha='center', va='center', fontsize=8,
             color='#ffffff88', fontfamily='monospace')

    # Tangential force arrow on bell
    tang_a = rotor_flux_angle + np.pi  # torque direction
    tr = R_BELL + 0.28
    ax3.annotate('',
                 xy=((tr+0.18)*np.cos(tang_a + 0.2),
                     (tr+0.18)*np.sin(tang_a + 0.2)),
                 xytext=(tr*np.cos(tang_a), tr*np.sin(tang_a)),
                 arrowprops=dict(arrowstyle='->', color='#2ecc71',
                                 lw=2.5, mutation_scale=16))
    ax3.text((tr+0.35)*np.cos(tang_a+0.12), (tr+0.35)*np.sin(tang_a+0.12),
             'τ', ha='center', va='center', fontsize=14,
             color='#2ecc71', fontweight='bold')

    ax3.set_title('Outrunner — Net MMF vs Rotor Flux → Torque\nFOC keeps MMF ⊥ Φ_rotor for max torque',
                  color='#c9d1d9', fontsize=10, pad=8)

    from matplotlib.lines import Line2D
    ax3.legend(handles=[
        Line2D([0],[0], color='#FFD700', lw=2.5, label='Stator MMF'),
        Line2D([0],[0], color='#e74c3c', lw=2.5, label='Rotor flux Φ_r'),
        Line2D([0],[0], color='#2ecc71', lw=2.5, label='Torque τ'),
    ], loc='lower left', facecolor='#161b22', edgecolor='#30363d',
       labelcolor='#c9d1d9', fontsize=8)

ani3 = FuncAnimation(fig3, draw_rotor_force, frames=FRAMES_RF, interval=60)
ani3.save('11_rotor_force.gif', writer=PillowWriter(fps=16))
plt.close(fig3)
print("GIF 3 done")
