"""
Spring + mass under gravity (elastic pendulum), live animation.

Run:   pip install pygame numpy
       python spring_mass.py

Controls:
  Mouse drag : grab the weight and pull it, release to let go
  F          : toggle force arrows (free body diagram)
  R          : reset
  ESC        : quit
"""
import math
import numpy as np
import pygame
# ---------------- physics parameters (pixels, seconds) ----------------
M = 1.0          # mass
K = 15.0         # spring stiffness
L0 = 200.0       # spring rest length
G = 900.0        # gravity (px/s^2, +y is down on screen)
DAMPING = 0.15   # air drag coefficient
SUBSTEPS = 20    # physics steps per frame (keeps it stable)

W, H = 800, 700
ANCHOR = np.array([W / 2, 80.0])


def reset():
    pos = ANCHOR + np.array([140.0, L0 + 40.0])   # start off to the side
    vel = np.zeros(2)
    return pos, vel


def forces(pos, vel):
    """Return (total, gravity, spring) forces on the mass."""
    d = pos - ANCHOR
    length = np.linalg.norm(d)
    u = d / length                                # unit vector anchor -> mass
    f_spring = -K * (length - L0) * u             # Hooke's law
    f_gravity = np.array([0.0, M * G])
    f_drag = -DAMPING * vel
    return f_spring + f_gravity + f_drag, f_gravity, f_spring


def step(pos, vel, dt):
    """Semi-implicit (symplectic) Euler: stable for oscillators."""
    f, _, _ = forces(pos, vel)
    vel = vel + (f / M) * dt
    pos = pos + vel * dt
    return pos, vel


# ---------------- drawing ----------------
def spring_points(a, b, coils=9, width=13.0, loop=7.0, lead=0.10, samples=240):
    """Coil spring like a textbook diagram (helix seen from the side).

    Each point moves sideways with sin() and also back/forth along the
    axis with cos(). Together that traces the looping coil shape.
    Straight leads at both ends connect to the pivots.
    """
    d = b - a
    length = np.linalg.norm(d)
    u = d / length
    n = np.array([-u[1], u[0]])
    start = a + (u * length * lead)
    body = length * (1 - 2 * lead)
    pts = [a, start]
    for i in range(samples + 1):
        t = i / samples
        phase = 2 * math.pi * coils * t
        along = body * t - loop * (1 - math.cos(phase))
        side = width * math.sin(phase)
        pts.append(start + u * along + n * side)
    pts.append(b)
    return pts


def draw_pivot(surf, p, r=6):
    """Small open circle with a dot, like the joints in your diagram."""
    pygame.draw.circle(surf, (18, 20, 28), p.astype(int), r)
    pygame.draw.circle(surf, (230, 230, 240), p.astype(int), r, 2)
    pygame.draw.circle(surf, (230, 230, 240), p.astype(int), 2)


def arrow(surf, color, start, vec, scale=0.12):
    end = start + vec * scale
    if np.linalg.norm(end - start) < 4:
        return
    pygame.draw.line(surf, color, start, end, 3)
    ang = math.atan2(end[1] - start[1], end[0] - start[0])
    for s in (+1, -1):
        tip = end - 10 * np.array([math.cos(ang + s * 0.45), math.sin(ang + s * 0.45)])
        pygame.draw.line(surf, color, end, tip, 3)


def main():
    pygame.init() #initalize the subsystems of pygame like sound, graphics etc
    screen = pygame.display.set_mode((W, H)) #defining W and H also creating display surface object
    pygame.display.set_caption("Spring-mass under gravity") # title
    clock = pygame.time.Clock() #creating a Clock object 
    font = pygame.font.SysFont("consolas", 16)

    pos, vel = reset()
    dragging = False
    show_forces = True #This controls whether the force arrows are displayed.
    trail = []

    running = True
    while running:
        frame_dt = min(clock.tick(60) / 1000.0, 1 / 30)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                elif e.key == pygame.K_f:
                    show_forces = not show_forces
                elif e.key == pygame.K_r:
                    pos, vel = reset()
                    trail.clear()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                mouse = np.array(e.pos, float)
                if np.linalg.norm(mouse - pos) < 30:
                    dragging = True
            elif e.type == pygame.MOUSEBUTTONUP:
                dragging = False

        if dragging:
            pos = np.array(pygame.mouse.get_pos(), float)
            vel = np.zeros(2)
        else:
            dt = frame_dt / SUBSTEPS
            for _ in range(SUBSTEPS):
                pos, vel = step(pos, vel, dt)

        trail.append(tuple(pos))
        trail = trail[-120:]

        # ---- render ----
        screen.fill((18, 20, 28))
        # pygame.draw.line(surface, color, start_pos, end_pos, width)
        pygame.draw.line(screen, (90, 95, 110), (ANCHOR[0] - 80, ANCHOR[1]),
                         (ANCHOR[0] + 80, ANCHOR[1]), 6)

        if len(trail) > 2:
            pygame.draw.lines(screen, (60, 90, 140), False, trail, 2)

        pts = spring_points(ANCHOR, pos)
        pygame.draw.aalines(screen, (200, 205, 220), False, pts)
        pygame.draw.lines(screen, (200, 205, 220), False, pts, 2)
        pygame.draw.circle(screen, (240, 120, 60), pos.astype(int), 22)
        pygame.draw.circle(screen, (255, 200, 150), pos.astype(int), 22, 2)
        draw_pivot(screen, ANCHOR)

        if show_forces:
            _, fg, fs = forces(pos, vel)
            arrow(screen, (90, 220, 120), pos, fg)    # gravity (green)
            arrow(screen, (240, 80, 80), pos, fs)     # spring (red)

        length = np.linalg.norm(pos - ANCHOR)
        ke = 0.5 * M * float(vel @ vel)
        pe_g = -M * G * pos[1]
        pe_s = 0.5 * K * (length - L0) ** 2
        lines = [f"spring length: {length:6.1f} (rest {L0:.0f})",
                 f"KE: {ke:9.0f}   PE: {pe_g + pe_s:9.0f}",
                 "green = gravity, red = spring force",
                 "drag the weight | F arrows | R reset"]
        for i, t in enumerate(lines):
            screen.blit(font.render(t, True, (170, 175, 190)), (12, 10 + i * 20))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()