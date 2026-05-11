import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, FancyBboxPatch
from matplotlib.lines import Line2D

fig, ax = plt.subplots(figsize=(13, 7), facecolor='#0d1117')
ax.set_facecolor('#0d1117')
ax.set_xlim(-0.3, 12.3)
ax.set_ylim(-0.3, 7.8)
ax.axis('off')

# ── Geometry ─────────────────────────────────────────────────────
TOOTH_W   = 1.05
SLOT_W    = 0.70
PITCH     = TOOTH_W + SLOT_W   # 1.75
N_TEETH   = 6
N_SLOTS   = 5

Y_BORE    = 0.0
Y_BACK    = 0.6     # back iron top
Y_TOOTH_B = 0.6
Y_TOOTH_T = 3.6
Y_GAP_B   = 3.6
Y_GAP_T   = 4.4
Y_PM_B    = 4.4
Y_PM_T    = 5.7
Y_YOKE_T  = 6.3

# Tooth left edges
tooth_x = [i * PITCH for i in range(N_TEETH)]
# Slot centres
slot_cx  = [tooth_x[i] + TOOTH_W + SLOT_W / 2 for i in range(N_SLOTS)]

SLOT_LABEL_Y = (Y_TOOTH_B + Y_TOOTH_T) / 2 - 0.3

# ── Back iron ────────────────────────────────────────────────────
total_w = tooth_x[-1] + TOOTH_W
ax.add_patch(Rectangle((tooth_x[0], Y_BORE), total_w, Y_BACK - Y_BORE,
                        color='#1c2128', zorder=1))

# ── Teeth ────────────────────────────────────────────────────────
for tx in tooth_x:
    ax.add_patch(Rectangle((tx, Y_TOOTH_B), TOOTH_W, Y_TOOTH_T - Y_TOOTH_B,
                            color='#2d333b', zorder=2, linewidth=0.5,
                            edgecolor='#444c56'))

# ── Slot interiors (slightly lighter) ────────────────────────────
for scx in slot_cx:
    ax.add_patch(Rectangle((scx - SLOT_W/2, Y_TOOTH_B), SLOT_W,
                            Y_TOOTH_T - Y_TOOTH_B,
                            color='#161b22', zorder=2))

# ── PM pole pitch: slightly wider than tooth pitch (24/22 ratio) ─
POLE_PITCH = PITCH * (24 / 22)  # ≈ 1.909
# Place poles so they roughly span the teeth
# First pole starts slightly before tooth 0
pole_start = tooth_x[0] - 0.3
poles = []  # (x_start, x_end, is_N)
x = pole_start
pole_idx = 0
while x < tooth_x[-1] + TOOTH_W + 0.5:
    is_N = (pole_idx % 2 == 0)
    poles.append((x, x + POLE_PITCH, is_N))
    x += POLE_PITCH
    pole_idx += 1

# Draw bell yoke
ax.add_patch(Rectangle((tooth_x[0] - 0.3, Y_PM_T), total_w + 0.6,
                        Y_YOKE_T - Y_PM_T, color='#21262d', zorder=3))

# Draw PM segments
for (px0, px1, is_N) in poles:
    col = '#7b241c' if is_N else '#1a5276'
    px0c = max(px0, tooth_x[0] - 0.3)
    px1c = min(px1, tooth_x[-1] + TOOTH_W + 0.3)
    if px1c <= px0c:
        continue
    ax.add_patch(Rectangle((px0c + 0.02, Y_PM_B), px1c - px0c - 0.04,
                            Y_PM_T - Y_PM_B, color=col, zorder=4, alpha=0.92))
    mid_x = (px0c + px1c) / 2
    ax.text(mid_x, (Y_PM_B + Y_PM_T) / 2, 'N' if is_N else 'S',
            ha='center', va='center', fontsize=13, color='#ecf0f1',
            fontweight='bold', zorder=5)

# ── Air gap label ─────────────────────────────────────────────────
ax.text(-0.2, (Y_GAP_B + Y_GAP_T) / 2, 'air\ngap',
        ha='right', va='center', fontsize=7.5, color='#8b949e',
        fontfamily='monospace')
ax.plot([-0.1, -0.1], [Y_GAP_B, Y_GAP_T], color='#444c56', lw=0.8)

# ── Determine PM polarity at each slot centre ─────────────────────
def pm_at(x):
    for (px0, px1, is_N) in poles:
        if px0 <= x < px1:
            return +1 if is_N else -1
    return 0

slot_pm = [pm_at(cx) for cx in slot_cx]

# ── Slot assignments for illustration (A+/B- commutation) ────────
# Choose a visually clear subset:
# Show slots that all produce the same-direction force (max torque condition)
# ● under N → RIGHT,  × under S → RIGHT
# Assign conductors for clarity:
#   slot 0: B- (dot, green)  under S → RIGHT ✓
#   slot 1: A+ (dot, red)    under N → RIGHT ✓
#   slot 2: A- (cross, red)  under S → RIGHT ✓
#   slot 3: B+ (cross, green) under N... → LEFT ✗ (show this one differently)
#   slot 4: B- (dot, green)  under S → RIGHT ✓

# Override PM assignment to guarantee a clean pedagogical layout
# N | S | N | S | N  pattern spanning our slots:
slot_pm_override = [-1, +1, -1, +1, -1]   # S, N, S, N, S
slot_currents    = [+1, +1, -1, -1, +1]   # dot, dot, cross, cross, dot
slot_phases      = ['B', 'A', 'A', 'B', 'B']
slot_active      = [True, True, True, False, True]  # slot 3 is C (off)

# Recompute PM polarity for our override
pole_polarity = slot_pm_override  # S=−1, N=+1
# Force: sign = -(I × B)
# ● under S: -(+1 × −1) = +1 → RIGHT
# ● under N: -(+1 × +1) = −1 → LEFT
# × under N: -(−1 × +1) = +1 → RIGHT
# × under S: -(−1 × −1) = −1 → LEFT

# Re-override to guarantee all active = RIGHT for clarity
# slot 0: dot, S → +1 RIGHT ✓
# slot 1: dot, N → −1 LEFT ✗ -- make it × under N instead
slot_currents[1] = -1   # cross
slot_phases[1]   = 'A'  # A-
# × under N: force = -(−1 × +1) = +1 → RIGHT ✓

# slot 2: cross, S → -(−1 × −1) = −1 LEFT ✗ -- make it dot under S
slot_currents[2] = +1
slot_phases[2]   = 'A'  # A+
# ● under S: -(+1 × −1) = +1 → RIGHT ✓

# slot 3: off (C phase)
slot_currents[3] = 0
slot_active[3]   = False

# slot 4: dot, S → RIGHT ✓ (keep)

# Recalculate forces
force_dir = []  # +1=RIGHT, −1=LEFT, 0=none
for i in range(N_SLOTS):
    if slot_currents[i] == 0:
        force_dir.append(0)
    else:
        fd = -(slot_currents[i] * pole_polarity[i])
        force_dir.append(fd)

# Recompute PM layout to match override polarity
# We'll just draw PM colours based on override
override_pm_cols = ['#1a5276', '#7b241c', '#1a5276', '#7b241c', '#1a5276', '#7b241c']
override_pm_labels = ['S', 'N', 'S', 'N', 'S', 'N']

# Redraw PM segments using simple equal-width bands matching slot regions
pm_bounds = [
    (-0.3, slot_cx[0] + SLOT_W/2),
    (slot_cx[0] + SLOT_W/2, slot_cx[1] + SLOT_W/2),
    (slot_cx[1] + SLOT_W/2, slot_cx[2] + SLOT_W/2),
    (slot_cx[2] + SLOT_W/2, slot_cx[3] + SLOT_W/2),
    (slot_cx[3] + SLOT_W/2, slot_cx[4] + SLOT_W/2),
    (slot_cx[4] + SLOT_W/2, total_w + 0.3),
]
# Clear and redraw PM region
ax.add_patch(Rectangle((-0.3, Y_PM_B), total_w + 0.6, Y_PM_T - Y_PM_B,
                        color='#0d1117', zorder=3))
for k, (bx0, bx1) in enumerate(pm_bounds):
    ax.add_patch(Rectangle((bx0 + 0.02, Y_PM_B), bx1 - bx0 - 0.04,
                            Y_PM_T - Y_PM_B,
                            color=override_pm_cols[k], zorder=4, alpha=0.92))
    ax.text((bx0+bx1)/2, (Y_PM_B+Y_PM_T)/2, override_pm_labels[k],
            ha='center', va='center', fontsize=12, color='#ecf0f1',
            fontweight='bold', zorder=5)

# ── B field lines (radial, in air gap + into teeth) ───────────────
GAP_MID = (Y_GAP_B + Y_GAP_T) / 2
for k, (bx0, bx1) in enumerate(pm_bounds):
    is_N = override_pm_labels[k] == 'N'
    n_lines = 3
    xs = np.linspace(bx0 + 0.3, bx1 - 0.3, n_lines)
    for lx in xs:
        if lx < -0.2 or lx > total_w + 0.2:
            continue
        col = '#cc6666' if is_N else '#6699cc'
        if is_N:
            # N: B points DOWN (from bell into stator)
            ax.annotate('', xy=(lx, Y_GAP_B + 0.02), xytext=(lx, Y_GAP_T - 0.02),
                        arrowprops=dict(arrowstyle='->', color=col,
                                        lw=1.2, mutation_scale=8), zorder=6)
            # Extend into tooth
            ax.plot([lx, lx], [Y_TOOTH_B + 0.1, Y_GAP_B],
                    color=col, lw=0.9, alpha=0.5, zorder=6)
        else:
            # S: B points UP (from stator into bell)
            ax.annotate('', xy=(lx, Y_GAP_T - 0.02), xytext=(lx, Y_GAP_B + 0.02),
                        arrowprops=dict(arrowstyle='->', color=col,
                                        lw=1.2, mutation_scale=8), zorder=6)
            ax.plot([lx, lx], [Y_TOOTH_B + 0.1, Y_GAP_B],
                    color=col, lw=0.9, alpha=0.5, zorder=6)

# ── B field label ─────────────────────────────────────────────────
ax.text(total_w + 0.4, (Y_GAP_B + Y_GAP_T) / 2, 'B',
        ha='left', va='center', fontsize=12, color='#cc6666',
        fontweight='bold', fontfamily='monospace')

# ── Conductor symbols ─────────────────────────────────────────────
COND_Y = SLOT_LABEL_Y + 0.2
PC = {'A': '#e74c3c', 'B': '#2ecc71', 'C': '#3498db'}

for i, cx in enumerate(slot_cx):
    cur = slot_currents[i]
    ph  = slot_phases[i]
    col = PC.get(ph, '#666')

    if cur == 0:
        # C phase — dim circle
        circ = plt.Circle((cx, COND_Y), 0.22, color='#3498db',
                           alpha=0.2, zorder=7)
        ax.add_patch(circ)
        ax.text(cx, COND_Y, 'C', ha='center', va='center',
                fontsize=7, color='#3498db', alpha=0.4, fontfamily='monospace')
        continue

    circ = plt.Circle((cx, COND_Y), 0.22, color=col, alpha=0.85, zorder=7)
    ax.add_patch(circ)
    if cur > 0:
        # dot = out of page
        ax.plot(cx, COND_Y, '.', ms=6, color='white', zorder=8)
        ax.text(cx, COND_Y - 0.55, '● out', ha='center', va='top',
                fontsize=7, color=col, fontfamily='monospace')
    else:
        # cross = into page
        d = 0.10
        for dx, dy in [(-d,d),(d,-d)]:
            ax.plot([cx-d, cx+d], [COND_Y+dy, COND_Y-dy], '-',
                    lw=1.5, color='white', zorder=8)
        ax.text(cx, COND_Y - 0.55, '× in', ha='center', va='top',
                fontsize=7, color=col, fontfamily='monospace')

    # Phase label above conductor
    ax.text(cx, COND_Y + 0.38, ph + ('+' if cur > 0 else '−'),
            ha='center', va='bottom', fontsize=8, color=col,
            fontfamily='monospace', fontweight='bold')

# ── Force arrows on active conductors ────────────────────────────
F_ARROW_Y = COND_Y
F_LEN = 1.0
F_COL = '#FFD700'

for i, cx in enumerate(slot_cx):
    fd = force_dir[i]
    if fd == 0:
        continue
    dx = fd * F_LEN
    ax.annotate('', xy=(cx + dx*0.9, F_ARROW_Y - 0.95),
                 xytext=(cx, F_ARROW_Y - 0.95),
                 arrowprops=dict(arrowstyle='->', color=F_COL,
                                 lw=2.2, mutation_scale=14), zorder=9)

# F label
ax.text(slot_cx[0] + F_LEN + 0.1, F_ARROW_Y - 0.92, 'F',
        ha='left', va='center', fontsize=11, color=F_COL,
        fontweight='bold', fontfamily='monospace')
ax.text(slot_cx[0] - F_LEN*0.5, F_ARROW_Y - 1.35,
        'F = I L × B', ha='center', va='top',
        fontsize=8.5, color=F_COL, fontfamily='monospace')

# ── Direction labels ──────────────────────────────────────────────
ax.text(-0.25, Y_YOKE_T + 0.1, 'Bell (rotating)',
        ha='left', va='bottom', fontsize=9, color='#8b949e',
        fontfamily='monospace', style='italic')
ax.text(-0.25, Y_BORE - 0.25, 'Stator (fixed)',
        ha='left', va='top', fontsize=9, color='#8b949e',
        fontfamily='monospace', style='italic')

# Radial direction arrow
ax.annotate('', xy=(total_w + 0.1, Y_GAP_T + 0.2),
             xytext=(total_w + 0.1, Y_GAP_B - 0.2),
             arrowprops=dict(arrowstyle='<->', color='#8b949e', lw=1.0))
ax.text(total_w + 0.25, (Y_GAP_B + Y_GAP_T)/2, 'radial\n(r̂)',
        ha='left', va='center', fontsize=7.5, color='#8b949e',
        fontfamily='monospace')

# Tangential direction arrow
ax.annotate('', xy=(total_w*0.7, Y_BORE - 0.1),
             xytext=(total_w*0.4, Y_BORE - 0.1),
             arrowprops=dict(arrowstyle='->', color='#8b949e', lw=1.0))
ax.text(total_w*0.55, Y_BORE - 0.22, 'tangential (θ̂)  →  torque direction',
        ha='center', va='top', fontsize=7.5, color='#8b949e',
        fontfamily='monospace')

# ── Cross-product inset box ───────────────────────────────────────
bx = 9.8; by = 0.4; bw = 2.3; bh = 3.0
ax.add_patch(FancyBboxPatch((bx, by), bw, bh,
                             boxstyle='round,pad=0.1',
                             facecolor='#161b22', edgecolor='#30363d',
                             linewidth=1.0, zorder=10))
ax.text(bx + bw/2, by + bh - 0.15, 'F = IL × B',
        ha='center', va='top', fontsize=10, color='#FFD700',
        fontfamily='monospace', fontweight='bold', zorder=11)

# Draw three arrows for I, B, F
cx0 = bx + bw/2; cy0 = by + bh/2 - 0.1
arrow_len = 0.6

def draw_inset_arrow(x0, y0, dx, dy, label, col, label_off=(0.1, 0.1)):
    ax.annotate('', xy=(x0+dx, y0+dy), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='->', color=col,
                                lw=2.0, mutation_scale=12), zorder=12)
    ax.text(x0+dx+label_off[0], y0+dy+label_off[1], label,
            ha='center', va='center', fontsize=9, color=col,
            fontfamily='monospace', fontweight='bold', zorder=12)

# I: out of page (dot at centre)
ax.plot(cx0, cy0, 'o', ms=10, color='#e74c3c', zorder=12)
ax.plot(cx0, cy0, '.', ms=4,  color='white',   zorder=13)
ax.text(cx0 + 0.05, cy0 + 0.38, 'I (out)',
        ha='center', va='bottom', fontsize=8, color='#e74c3c',
        fontfamily='monospace', zorder=12)

# B: downward (N pole above)
draw_inset_arrow(cx0, cy0 + 0.0, 0, -arrow_len, 'B\n(radial)',
                 '#cc6666', label_off=(0.35, -0.25))

# F: rightward
draw_inset_arrow(cx0, cy0, arrow_len, 0, 'F\n(tang.)',
                 '#FFD700', label_off=(0.15, -0.28))

ax.text(cx0, cy0 - arrow_len - 0.45, '⊙ × ↓ = →',
        ha='center', va='top', fontsize=8, color='#8b949e',
        fontfamily='monospace', zorder=12)

# ── Legend ────────────────────────────────────────────────────────
from matplotlib.patches import Patch
ax.legend(handles=[
    Patch(color='#e74c3c', label='Phase A'),
    Patch(color='#2ecc71', label='Phase B'),
    Patch(color='#3498db', alpha=0.3, label='Phase C (off)'),
    Patch(color='#7b241c', label='N pole'),
    Patch(color='#1a5276', label='S pole'),
    Line2D([0],[0], color='#FFD700', lw=2, label='Force F'),
    Line2D([0],[0], color='#cc6666', lw=1.5, label='B field (N→)'),
    Line2D([0],[0], color='#6699cc', lw=1.5, label='B field (→S)'),
], loc='upper right', facecolor='#161b22', edgecolor='#30363d',
   labelcolor='#c9d1d9', fontsize=8.5, framealpha=0.95)

ax.set_title('Unwrapped air gap  —  A high / B low  (max torque position)\n'
             'Each active conductor: F = IL × B → tangential force → torque on bell',
             color='#c9d1d9', fontsize=11, pad=10)

plt.tight_layout(pad=0.4)
plt.savefig('/Users/max/repos/maxsimmonds.engineer/assets/foc_gifs/13_unwrapped_teeth.png',
            dpi=160, bbox_inches='tight', facecolor='#0d1117')
plt.close()
print("Done")
