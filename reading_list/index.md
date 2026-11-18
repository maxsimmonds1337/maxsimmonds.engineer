# Reading List
---

A curated list of books, papers, and ideas across the fields I think matter most right now — physical AI, space, energy, and biotech. Annotated with why I added each one.

Status key: **queued** · **reading** · **done**

---

## Physical AI — Robotics & Humanoids

The question I haven't answered yet: are humanoids actually the right form factor, or are they a local maximum because humans built the world for themselves? Project Cederick is my attempt to get a feel for this from first principles.

| Status | Item | Why |
|---|---|---|
| queued | **Modern Robotics: Mechanics, Planning, and Control** — Lynch & Park | The rigorous reference. Covers SE(3), screw theory, trajectory optimisation. Free at modernrobotics.org. For when I want to go beyond heuristic kinematics. |
| queued | **Probabilistic Robotics** — Thrun, Burgard & Fox | Kalman filters, particle filters, SLAM. The foundations of any robot that needs to know where it is. |
| queued | *Learning to Walk in Minutes Using Massively Parallel Deep RL* — Rudin et al. (ETH Zurich, 2022) | The paper that made legged locomotion feel approachable. 4000 robots in sim simultaneously. The methodology is directly applicable to Cederick. |
| queued | *Eureka: Human-Level Reward Design via Coding LLMs* — Ma et al. (2023) | LLMs writing and iterating reward functions autonomously. The direction everything is heading. |
| queued | *Dexterous In-Hand Manipulation* — OpenAI (2019) | Rubik's cube with a robot hand. Still the best reference for sim-to-real methodology. |

---

## Reinforcement Learning

I use SAC every day on xdoubledot. I want to understand the whole landscape, not just the algorithm I'm running.

| Status | Item | Why |
|---|---|---|
| reading | **Reinforcement Learning: An Introduction** — Sutton & Barto | The bible. Free at incompleteideas.net. I keep skipping back to it every time I hit something confusing. |
| queued | **Algorithms for Decision Making** — Kochenderfer, Wheeler & Wray | More practical than Sutton. Covers POMDPs, MDPs, planning under uncertainty. Free PDF. |
| done | *Soft Actor-Critic: Off-Policy Maximum Entropy Deep RL* — Haarnoja et al. (2018) | The algorithm at the heart of xdoubledot Aegis. Read the original. |
| queued | *CrossQ: Batch Normalization in Deep RL for Improved Sample Efficiency* — Bhatt et al. (2024) | The SAC→CrossQ upgrade we're targeting. State of the art for continuous control. |
| queued | *Human-level Control through Deep Reinforcement Learning* — Mnih et al. (2015) | The DQN paper. Atari from pixels. Worth reading even if it's old — the framing is still useful. |

---

## Space & Propulsion

This is home territory. I want to go deeper on EP and mission design.

| Status | Item | Why |
|---|---|---|
| queued | **Fundamentals of Electric Propulsion: Ion and Hall Thrusters** — Goebel & Katz | The EP bible. Has the HET chapter. Should have read this before starting xdoubledot, honestly. |
| queued | **Rocket Propulsion Elements** — Sutton & Biblarz | The chemical propulsion reference. For understanding what we're competing against and complementing. |
| queued | **Space Mission Analysis and Design** (SMAD) — Wertz & Larson | The mission design reference. Delta-V budgets, orbit mechanics, mass budgets. Useful when thinking about where xdoubledot hardware actually fits. |
| queued | *BHT-200 Hall Thruster Performance Characterisation* — Szabo et al. (IEPC, 2005) | The ground truth we compare against in xdoubledot simulation. |

---

## Energy

The biggest unsolved engineering problem on Earth. Even if I never work directly in energy, understanding it changes how you think about almost everything else.

| Status | Item | Why |
|---|---|---|
| queued | **Energy and Civilization: A History** — Vaclav Smil | The best book on what energy actually is and how it drove human civilisation. Dense, worth it. Smil is relentlessly empirical — no hype. |
| queued | **The Grid** — Gretchen Bakke | America's aging electrical grid. Accessible and surprisingly alarming. Relevant background if you care about electrification, EVs, any of it. |
| queued | **How to Avoid a Climate Disaster** — Bill Gates | Practical breakdown of which technologies move the needle at scale, and by how much. He gets into actual numbers. |
| queued | **Commonwealth Fusion Systems** — follow their progress (cfs.energy) | SPARC tokamak. They hit their 20T magnet target in 2021. If this works, it changes everything. |
| queued | **Helion Energy** — follow (helionenergy.com) | Microsoft signed a 20MW offtake agreement for 2028. Different fusion approach (FRC — field-reversed configuration). |
| queued | **Form Energy** — follow (formenergy.com) | Iron-air batteries for multi-day grid storage. The piece the grid actually needs that lithium can't do. |

---

## Biotech & Pharma

I don't have a background here. But the convergence of AI and biology feels like the biggest science story of the next 20 years. Worth at least knowing the terrain.

| Status | Item | Why |
|---|---|---|
| queued | **The Code Breaker** — Walter Isaacson | CRISPR and Jennifer Doudna. The best accessible book on gene editing. Isaacson does a good job on the science without dumbing it down. |
| queued | **The Song of the Cell** — Siddhartha Mukherjee | What cells actually are. Best accessible biology since The Double Helix. Mukherjee writes science like a novelist. |
| queued | **Regenesis** — George Church | Synthetic biology's potential. Church is extremely speculative but he's usually early, not wrong. |
| queued | *AlphaFold3* — Abramson et al. (DeepMind, 2024) | Protein structure and molecular interaction prediction. The moment AI actually changed biology — and it's only getting started. |
| queued | **Recursion Pharmaceuticals** — follow (recursion.com) | AI drug discovery using phenomics at scale. Example of what applying ML rigorously to a new domain looks like in practice. |

---

## Left Field

Things that don't fit a domain but feel important.

| Status | Item | Why |
|---|---|---|
| queued | **A Thousand Brains** — Jeff Hawkins | Reference frame theory of intelligence. Interesting if you're thinking about physical AI at a deeper level — proposes that the cortex is doing something much simpler (and more general) than we think. |
| queued | **The Alignment Problem** — Brian Christian | AI alignment without the doomsday framing. Good grounding in what the actual concerns are, since we're all building AI systems now. |
| queued | **Oklo** — small modular fission reactor (oklo.com) | NRC-licensed. Backpack-scale nuclear. If this gets deployed at scale, it changes remote power, space, and propulsion economics. |
| queued | **Lifespan** — David Sinclair | Longevity science. Sinclair is controversial but the underlying biology of aging (NAD+, sirtuins, epigenetic reprogramming) is genuinely interesting and moving fast. |
| reading | **Microwave Engineering** — David Pozar (4th ed.) | The RF/microwave reference. Working through it alongside transmission line and Smith chart work. |
