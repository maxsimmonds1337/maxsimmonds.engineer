"""
Generates three GIFs for the how_bldc_works.md article:
  14_force_reversal.gif   — bell moves, force flips, why commutation is needed
  15_trap_commutation.gif — 6-step trap, MMF jumps 60° at a time, torque ripple
  16_bemf.gif             — spinning bell, flux change through coil, voltage waveform
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Rectangle, FancyBboxPatch

# ══════════════════════════════════════════════════════════════════
# GIF 1: Force reversal  (unwrapped, bell slides right)
# ══════════════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(11, 5), facecolor='#0d1117')

TOOTH_W = 1.05; SLOT_W = 0.70; PITCH = TOOTH_W + SLOT_W
N_TEETH = 5
tooth_x0 = np.array([i * PITCH for i in range(N_TEETH)])
slot_cx0  = tooth_x0[:-1] + TOOTH_W + SLOT_W / 2

# Bell spans slightly wider than stator
BELL_W = 2.2 * PITCH      # two PM poles visible at a time
POLE_PITCH = BELL_W / 2   # one pole per half bell width

Y_TOOTH_B = 1.0; Y_TOOTH_T = 3.2
Y_GAP_B   = 3.2; Y_GAP_T   = 3.9
Y_PM_B    = 3.9; Y_PM_T    = 5.0
STATOR_W  = tooth_x0[-1] + TOOTH_W
COND_Y    = (Y_TOOTH_B + Y_TOOTH_T) / 2

# Fixed coil: slot 1 (between tooth 1 and 2), always dot (current out)
COIL_SLOT = 1
coil_cx = slot_cx0[COIL_SLOT]

FRAMES_FR = 80

def draw_fr(frame):
    ax1.clear()
    ax1.set_facecolor('#0d1117')
    ax1.set_xlim(-0.3, STATOR_W + 0.3)
    ax1.set_ylim(0.3, 5.8)
    ax1.axis('off')

    # Bell offset: slides from left to right over 80 frames
    bell_offset = (frame / FRAMES_FR) * 2 * POLE_PITCH - POLE_PITCH * 0.5

    # Back iron
    ax1.add_patch(Rectangle((0, 0.3), STATOR_W, 0.7, color='#1c2128', zorder=1))

    # Teeth
    for tx in tooth_x0:
        ax1.add_patch(Rectangle((tx, Y_TOOTH_B), TOOTH_W, Y_TOOTH_T - Y_TOOTH_B,
                                 color='#2d333b', zorder=2))
    # Slots
    for scx in slot_cx0:
        ax1.add_patch(Rectangle((scx - SLOT_W/2, Y_TOOTH_B), SLOT_W,
                                 Y_TOOTH_T - Y_TOOTH_B, color='#161b22', zorder=2))

    # Bell yoke (moves)
    ax1.add_patch(Rectangle((-0.3, Y_PM_T), STATOR_W + 0.6, 0.5,
                             color='#21262d', zorder=3))

    # Two PM poles (N then S) on the sliding bell
    for pole_i in range(-1, 4):
        px = bell_offset + pole_i * POLE_PITCH
        is_N = (pole_i % 2 == 0)
        col = '#7b241c' if is_N else '#1a5276'
        px0 = max(px + 0.02, -0.3)
        px1 = min(px + POLE_PITCH - 0.02, STATOR_W + 0.3)
        if px1 <= px0: continue
        ax1.add_patch(Rectangle((px0, Y_PM_B), px1 - px0,
                                 Y_PM_T - Y_PM_B, color=col, alpha=0.92, zorder=4))
        mid = (px0 + px1) / 2
        ax1.text(mid, (Y_PM_B + Y_PM_T) / 2,
                 'N' if is_N else 'S', ha='center', va='center',
                 fontsize=12, color='#ecf0f1', fontweight='bold', zorder=5)

    # B field at coil centre
    def get_pm_at(x):
        for pole_i in range(-1, 4):
            px = bell_offset + pole_i * POLE_PITCH
            if px <= x < px + POLE_PITCH:
                return +1 if (pole_i % 2 == 0) else -1
        return 0

    pm = get_pm_at(coil_cx)
    b_col = '#cc6666' if pm > 0 else '#6699cc'
    b_label = '↓ B' if pm > 0 else '↑ B'
    ax1.annotate('', xy=(coil_cx, Y_GAP_B + 0.05 if pm > 0 else Y_GAP_T - 0.05),
                 xytext=(coil_cx, Y_GAP_T - 0.05 if pm > 0 else Y_GAP_B + 0.05),
                 arrowprops=dict(arrowstyle='->', color=b_col, lw=2, mutation_scale=12),
                 zorder=6)

    # Conductor (always dot)
    circ = plt.Circle((coil_cx, COND_Y), 0.20, color='#e74c3c', zorder=7)
    ax1.add_patch(circ)
    ax1.plot(coil_cx, COND_Y, '.', ms=5, color='white', zorder=8)

    # Force arrow
    # F direction: -(current × pm) = -(+1 × pm) = -pm
    fd = -pm   # +1=right, -1=left
    f_col = '#FFD700' if fd > 0 else '#e74c3c'
    f_label = '→ F (helps)' if fd > 0 else '← F (opposes!)'
    if fd != 0:
        ax1.annotate('', xy=(coil_cx + fd*0.85, COND_Y - 0.75),
                     xytext=(coil_cx, COND_Y - 0.75),
                     arrowprops=dict(arrowstyle='->', color=f_col,
                                     lw=2.5, mutation_scale=14), zorder=9)
        ax1.text(coil_cx + fd*1.0, COND_Y - 0.78, f_label,
                 ha='center' if fd > 0 else 'center',
                 va='center', fontsize=8, color=f_col, fontfamily='monospace')

    # Progress indicator
    pct = frame / FRAMES_FR
    ax1.text(STATOR_W/2, 5.55,
             f'Bell position: {pct*100:.0f}%  of one pole pitch →',
             ha='center', fontsize=9, color='#8b949e', fontfamily='monospace')

    ax1.set_title('Force reversal — same current, bell rotates → pole polarity flips → force reverses\n'
                  'Solution: reverse the current at the right moment  (commutation)',
                  color='#c9d1d9', fontsize=10, pad=6)

ani1 = FuncAnimation(fig1, draw_fr, frames=FRAMES_FR, interval=60)
ani1.save('14_force_reversal.gif', writer=PillowWriter(fps=15))
plt.close(fig1)
print("GIF 1 done")

# ══════════════════════════════════════════════════════════════════
# GIF 2: 6-step trapezoidal commutation  (outrunner cross-section)
# ══════════════════════════════════════════════════════════════════
fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(12, 6),
                                   facecolor='#0d1117',
                                   gridspec_kw={'width_ratios': [1, 1]})
for ax in (ax2a, ax2b):
    ax.set_facecolor('#0d1117')

R_BELL = 1.0; R_ST_OUT = 0.70; R_ST_IN = 0.46
Q = 12; P = 8   # simplified 12N8P for clarity

slot_mech = np.array([i * 2*np.pi/Q for i in range(Q)])
# Simple 12N8P phase assignment: ABCABCABCABC with alternating polarity
phase_seq = ['A+','B+','C+','A-','B-','C-','A+','B+','C+','A-','B-','C-']

PC = {'A': '#e74c3c', 'B': '#2ecc71', 'C': '#3498db'}

# 6 commutation steps for 3-phase motor
# (high_phase, low_phase, mmf_angle_electrical)
STEPS = [
    ('A', 'B', 330), ('A', 'C',  30), ('B', 'C',  90),
    ('B', 'A', 150), ('C', 'A', 210), ('C', 'B', 270),
]

HOLD = 18   # frames per step
TOTAL_FRAMES = len(STEPS) * HOLD

def get_current(slot_idx, high_ph, low_ph):
    ph_str = phase_seq[slot_idx]
    ph = ph_str[0]; pol = ph_str[1]
    if ph == high_ph:
        return +1 if pol == '+' else -1
    elif ph == low_ph:
        return -1 if pol == '+' else +1
    return 0

def draw_trap(frame):
    ax2a.clear(); ax2b.clear()
    for ax in (ax2a, ax2b):
        ax.set_facecolor('#0d1117')

    step_idx = frame // HOLD
    within   = frame % HOLD
    high_ph, low_ph, mmf_deg = STEPS[step_idx]
    mmf_rad = np.deg2rad(mmf_deg)

    # Rotor angle: advances slowly
    rotor_deg = (frame / TOTAL_FRAMES) * 360 / (P/2)
    rotor_rad = np.deg2rad(rotor_deg)

    th = np.linspace(0, 2*np.pi, 300)

    # ── Left panel: motor cross-section ──────────────────────────
    ax2a.set_xlim(-1.6, 1.6); ax2a.set_ylim(-1.6, 1.6)
    ax2a.set_aspect('equal'); ax2a.axis('off')

    # Bell
    for r0, r1, col in [(R_BELL, R_BELL+0.18, '#21262d')]:
        xs = np.concatenate([r0*np.cos(th), r1*np.cos(th[::-1])])
        ys = np.concatenate([r0*np.sin(th), r1*np.sin(th[::-1])])
        ax2a.fill(xs, ys, color=col)

    # PM segments
    for ki in range(P):
        pa = rotor_rad + ki * 2*np.pi/P
        is_N = (ki % 2 == 0)
        col = '#7b241c' if is_N else '#1a5276'
        th_s = np.linspace(pa+0.04, pa+2*np.pi/P-0.04, 20)
        xs = np.concatenate([R_BELL*np.cos(th_s), (R_BELL+0.16)*np.cos(th_s[::-1])])
        ys = np.concatenate([R_BELL*np.sin(th_s), (R_BELL+0.16)*np.sin(th_s[::-1])])
        ax2a.fill(xs, ys, color=col, alpha=0.9)

    # Back iron
    xs = np.concatenate([(R_ST_IN-0.08)*np.cos(th), (R_ST_IN-0.16)*np.cos(th[::-1])])
    ys = np.concatenate([(R_ST_IN-0.08)*np.sin(th), (R_ST_IN-0.16)*np.sin(th[::-1])])
    ax2a.fill(xs, ys, color='#21262d')

    # Teeth and currents
    tooth_span = 0.7 * (2*np.pi/Q)
    slot_r = (R_ST_IN + R_ST_OUT)/2
    for si in range(Q):
        a = slot_mech[si]
        th_t = np.linspace(a-tooth_span/2, a+tooth_span/2, 12)
        xs = np.concatenate([R_ST_IN*np.cos(th_t), R_ST_OUT*np.cos(th_t[::-1])])
        ys = np.concatenate([R_ST_IN*np.sin(th_t), R_ST_OUT*np.sin(th_t[::-1])])
        ax2a.fill(xs, ys, color='#2d333b')

        cur = get_current(si, high_ph, low_ph)
        ph = phase_seq[si][0]
        col = PC[ph] if cur != 0 else '#666666'
        sx = slot_r * np.cos(a); sy = slot_r * np.sin(a)
        ax2a.plot(sx, sy, 'o', ms=7, color=col, alpha=1.0 if cur!=0 else 0.2)
        if cur > 0:
            ax2a.plot(sx, sy, '.', ms=3, color='white')
        elif cur < 0:
            d = 0.045
            for sgn in [1, -1]:
                ax2a.plot([sx-d, sx+d], [sy+sgn*d, sy-sgn*d], '-', lw=1, color='white')

    # MMF vector
    ax2a.annotate('', xy=(0.6*np.cos(mmf_rad), 0.6*np.sin(mmf_rad)),
                  xytext=(0,0),
                  arrowprops=dict(arrowstyle='->', color='#FFD700',
                                  lw=3, mutation_scale=18))
    ax2a.text(0.82*np.cos(mmf_rad), 0.82*np.sin(mmf_rad), 'MMF',
              ha='center', va='center', fontsize=9, color='#FFD700',
              fontfamily='monospace', fontweight='bold')

    # Rotor flux vector
    ax2a.annotate('', xy=(0.45*np.cos(rotor_rad), 0.45*np.sin(rotor_rad)),
                  xytext=(0,0),
                  arrowprops=dict(arrowstyle='->', color='#e74c3c',
                                  lw=2, mutation_scale=14))

    delta = abs(mmf_deg - rotor_deg) % 360
    if delta > 180: delta = 360 - delta
    torque_pct = abs(np.sin(np.deg2rad(delta)))

    ax2a.set_title(f'Step {step_idx+1}/6:  {high_ph}+  {low_ph}−\n'
                   f'MMF = {mmf_deg}°   δ = {delta:.0f}°   τ = {torque_pct:.2f} × max',
                   color='#c9d1d9', fontsize=9, pad=6)

    # ── Right panel: torque ripple bar chart ──────────────────────
    ax2b.set_xlim(-0.5, 6.5); ax2b.set_ylim(0, 1.25)
    ax2b.set_facecolor('#0d1117')
    ax2b.spines['bottom'].set_color('#444c56')
    ax2b.spines['left'].set_color('#444c56')
    ax2b.spines['top'].set_visible(False)
    ax2b.spines['right'].set_visible(False)
    ax2b.tick_params(colors='#8b949e', labelsize=8)
    ax2b.set_xticks(range(6))
    ax2b.set_xticklabels([f'Step {i+1}' for i in range(6)],
                          color='#8b949e', fontsize=7.5)
    ax2b.set_ylabel('Torque (normalised)', color='#8b949e', fontsize=8)
    ax2b.axhline(1.0, color='#2ecc71', lw=1, ls='--', alpha=0.5, label='ideal (FOC)')

    # Show torque for each step given current rotor position
    for si, (hp, lp, md) in enumerate(STEPS):
        d = abs(md - rotor_deg) % 360
        if d > 180: d = 360 - d
        t = abs(np.sin(np.deg2rad(d)))
        col = '#FFD700' if si == step_idx else '#444c56'
        ax2b.bar(si, t, color=col, alpha=0.9, width=0.6, zorder=3)

    ax2b.axhline(0.5, color='#e74c3c', lw=0.8, ls=':', alpha=0.6)
    ax2b.text(6.1, 0.5, 'min\n(sin30°)', va='center', fontsize=7,
              color='#e74c3c', fontfamily='monospace')
    ax2b.set_title('Torque per commutation step\n(varies as rotor moves through each step)',
                   color='#c9d1d9', fontsize=9, pad=6)
    ax2b.legend(fontsize=8, facecolor='#161b22', edgecolor='#30363d',
                labelcolor='#c9d1d9', loc='upper right')

ani2 = FuncAnimation(fig2, draw_trap, frames=TOTAL_FRAMES, interval=80)
ani2.save('15_trap_commutation.gif', writer=PillowWriter(fps=12))
plt.close(fig2)
print("GIF 2 done")

# ══════════════════════════════════════════════════════════════════
# GIF 3: Back EMF  (one coil, flux sweeping through, voltage output)
# ══════════════════════════════════════════════════════════════════
fig3, (ax3a, ax3b) = plt.subplots(2, 1, figsize=(10, 7),
                                   facecolor='#0d1117',
                                   gridspec_kw={'height_ratios': [1.4, 1]})
for ax in (ax3a, ax3b):
    ax.set_facecolor('#0d1117')

FRAMES_BEMF = 100
voltage_history = []

def draw_bemf(frame):
    ax3a.clear(); ax3b.clear()
    for ax in (ax3a, ax3b):
        ax.set_facecolor('#0d1117')

    # Unwrapped view: bell slides, one coil fixed
    POLE_P = 3.0
    bell_offset = (frame / FRAMES_BEMF) * 2 * POLE_P

    ax3a.set_xlim(-0.5, 10.5); ax3a.set_ylim(0.0, 6.5); ax3a.axis('off')

    stator_w = 10.0
    # Back iron
    ax3a.add_patch(Rectangle((0, 0.2), stator_w, 0.6, color='#1c2128'))
    # Two teeth for one coil
    for tx in [3.5, 5.8]:
        ax3a.add_patch(Rectangle((tx, 0.8), 1.0, 2.8, color='#2d333b'))
    # Slot between teeth
    ax3a.add_patch(Rectangle((4.5, 0.8), 1.3, 2.8, color='#161b22'))
    # Coil wires (go side and return side)
    circ_L = plt.Circle((4.5 + 0.25, 1.7), 0.22, color='#e74c3c', zorder=5)
    circ_R = plt.Circle((4.5 + 1.05, 1.7), 0.22, color='#e74c3c', zorder=5)
    ax3a.add_patch(circ_L); ax3a.add_patch(circ_R)

    # Bell yoke
    ax3a.add_patch(Rectangle((-0.5, 4.3), stator_w+1, 0.7, color='#21262d'))

    # PM poles (sliding)
    phi_through_coil = 0.0
    for pole_i in range(-1, 5):
        px = bell_offset + pole_i * POLE_P - 5.0
        is_N = (pole_i % 2 == 0)
        col = '#7b241c' if is_N else '#1a5276'
        px0 = max(px+0.05, -0.5); px1 = min(px+POLE_P-0.05, stator_w+0.5)
        if px1 <= px0: continue
        ax3a.add_patch(Rectangle((px0, 3.6), px1-px0, 0.7, color=col, alpha=0.92))
        mid = (px0+px1)/2
        ax3a.text(mid, 3.95, 'N' if is_N else 'S',
                  ha='center', va='center', fontsize=11, color='#ecf0f1',
                  fontweight='bold')

        # Flux through coil (coil centre at x=5.15)
        coil_x = 5.15
        if px0 < coil_x < px1:
            frac = (coil_x - px0) / (px1 - px0)
            phi_through_coil += (+1 if is_N else -1) * np.sin(frac * np.pi)

    # Air gap label
    ax3a.text(-0.4, 3.2, 'air gap', fontsize=7, color='#8b949e',
              fontfamily='monospace', va='center')

    # B field at coil
    b_at_coil = phi_through_coil
    b_col = '#cc6666' if b_at_coil > 0.2 else ('#6699cc' if b_at_coil < -0.2 else '#666666')
    if abs(b_at_coil) > 0.1:
        direction = -1 if b_at_coil > 0 else 1
        for bx in [4.75, 5.15]:
            ax3a.annotate('',
                          xy=(bx, 3.6 if direction < 0 else 0.8+0.05),
                          xytext=(bx, 3.6-0.05 if direction < 0 else 0.8+2.8),
                          arrowprops=dict(arrowstyle='->', color=b_col,
                                          lw=1.5, mutation_scale=9))

    # Flux linkage = dΦ/dt → voltage (approximate as sin)
    phase = (frame / FRAMES_BEMF) * 4 * np.pi
    voltage = -np.sin(phase) * 2.5   # scaled for display
    voltage_history.append(voltage)
    if len(voltage_history) > FRAMES_BEMF:
        voltage_history.pop(0)

    # Induced voltage symbol on coil
    v_col = '#2ecc71' if voltage > 0 else '#e74c3c'
    ax3a.text(4.5 + 0.65, 1.7,
              f'V = {voltage:+.1f}',
              ha='center', va='center', fontsize=9, color=v_col,
              fontfamily='monospace', fontweight='bold',
              bbox=dict(boxstyle='round,pad=0.3', facecolor='#161b22',
                        edgecolor=v_col, alpha=0.9))

    ax3a.text(5.0, 6.2,
              'Faraday: V = −N dΦ/dt    faster spin → bigger dΦ/dt → bigger V',
              ha='center', va='top', fontsize=9, color='#8b949e',
              fontfamily='monospace')
    ax3a.set_title('Back EMF — spinning bell sweeps PM flux through stator coil → induces voltage',
                   color='#c9d1d9', fontsize=10, pad=6)

    # ── Voltage waveform ──────────────────────────────────────────
    ax3b.set_xlim(0, FRAMES_BEMF); ax3b.set_ylim(-3.2, 3.2)
    ax3b.spines['bottom'].set_color('#444c56')
    ax3b.spines['left'].set_color('#444c56')
    ax3b.spines['top'].set_visible(False)
    ax3b.spines['right'].set_visible(False)
    ax3b.axhline(0, color='#444c56', lw=0.8)
    ax3b.tick_params(colors='#8b949e', labelsize=8)
    ax3b.set_ylabel('BEMF  (V)', color='#8b949e', fontsize=8)
    ax3b.set_xlabel('Time →  (proportional to rotor position)', color='#8b949e', fontsize=8)

    if len(voltage_history) > 1:
        xs = list(range(len(voltage_history)))
        ax3b.plot(xs, voltage_history, color='#2ecc71', lw=2)
        ax3b.plot(xs[-1], voltage_history[-1], 'o', ms=6, color='#FFD700')

    # KV annotation
    ax3b.text(FRAMES_BEMF*0.02, 2.8,
              'KV = RPM / V_peak  (motor velocity constant)',
              fontsize=8.5, color='#FFD700', fontfamily='monospace')

ani3 = FuncAnimation(fig3, draw_bemf, frames=FRAMES_BEMF, interval=70)
ani3.save('16_bemf.gif', writer=PillowWriter(fps=14))
plt.close(fig3)
print("GIF 3 done")
