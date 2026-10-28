"""
Stage 1: a real rocking half-ring that rolls without slipping on the ground.

Physics runs in SI units (metres, kg, seconds). pygame only DRAWS the result.
State = (theta, omega).  theta > 0 means the body has turned clockwise on screen,
so it rolls to the right.  This is valid while |theta| < 90 degrees; past that the
contact point leaves the arc and the body must pivot over the cut corner (stage 2).

Keys:  R = reset     ESC = quit
"""
import math
import numpy as np
import pygame

# ---------------------------------------------------------------- drawing
W, H = 800, 600
GROUND_Y = 400                 # screen y of the ground line
PX_PER_M = 400                 # 400 px = 1 m, so R = 0.25 m is 100 px on screen

# ---------------------------------------------------------------- the body (SI)
R_OUT = 0.25                   # outer radius [m]   (100 px)
R_IN = 0.20                    # inner radius [m]   (80 px). Use 0 for a solid half-disk
MASS = 1.0                     # [kg]
g = 9.81                       # [m/s^2]
DAMPING = 0.0                  # rolling resistance [N*m*s/rad]. 0 = rocks forever
THETA0 = 0.4                   # starting tilt [rad]

# Mass properties of a uniform half-ring:
#   E   = distance from the arc centre down to the centre of mass
#   I_G = moment of inertia about the centre of mass
E = 4 * (R_OUT**3 - R_IN**3) / (3 * math.pi * (R_OUT**2 - R_IN**2))
I_G = MASS * (R_OUT**2 + R_IN**2) / 2 - MASS * E**2


# ---------------------------------------------------------------- physics
def inertia(theta):
    """Effective moment of inertia about the contact point. It changes as the body rocks."""
    return I_G + MASS * (R_OUT**2 + E**2 - 2 * R_OUT * E * math.cos(theta))


def accel(theta, omega):
    """theta'' from  J*theta'' + M*R*e*sin(theta)*omega^2 + M*g*e*sin(theta) + c*omega = 0"""
    return -(MASS * R_OUT * E * math.sin(theta) * omega**2
             + MASS * g * E * math.sin(theta)
             + DAMPING * omega) / inertia(theta)


def rk4_step(theta, omega, dt):
    """One Runge-Kutta 4 step: much more accurate than the simple 'omega += alpha*dt'."""
    k1t, k1w = omega, accel(theta, omega)
    k2t, k2w = omega + 0.5 * dt * k1w, accel(theta + 0.5 * dt * k1t, omega + 0.5 * dt * k1w)
    k3t, k3w = omega + 0.5 * dt * k2w, accel(theta + 0.5 * dt * k2t, omega + 0.5 * dt * k2w)
    k4t, k4w = omega + dt * k3w, accel(theta + dt * k3t, omega + dt * k3w)
    return (theta + dt / 6 * (k1t + 2 * k2t + 2 * k3t + k4t),
            omega + dt / 6 * (k1w + 2 * k2w + 2 * k3w + k4w))


def energy(theta, omega):
    """Kinetic + potential energy. Stays constant when DAMPING = 0 (a built-in correctness test)."""
    return 0.5 * inertia(theta) * omega**2 + MASS * g * (R_OUT - E * math.cos(theta))


def contact_forces(theta, omega):
    """Ground reaction on the body from Newton's 2nd law on the centre of mass.
    Returns (F, N): friction (positive = pushes right) and normal force, both in newtons."""
    alpha = accel(theta, omega)
    ax = (R_OUT - E * math.cos(theta)) * alpha + E * math.sin(theta) * omega**2
    ay = E * math.sin(theta) * alpha + E * math.cos(theta) * omega**2
    return MASS * ax, MASS * (g + ay)


# ---------------------------------------------------------------- geometry
def arc_centre(theta):
    """Rolling without slipping: the arc centre moves R*theta sideways and stays R above ground."""
    return np.array([R_OUT * theta, R_OUT])


def to_screen(p):
    """Physics coordinates (x right, y up, metres) -> pygame pixels (y down)."""
    return (W / 2 + p[0] * PX_PER_M, GROUND_Y - p[1] * PX_PER_M)


def outline(theta):
    """Pixel polygon of the half-ring at tilt theta."""
    beta = np.linspace(-math.pi / 2, math.pi / 2, 60)      # angle around the body
    a = beta - theta                                       # the body is turned by theta
    unit = np.column_stack([np.sin(a), -np.cos(a)])        # direction from the arc centre
    ring = np.vstack([R_OUT * unit, R_IN * unit[::-1]])    # outer edge, then inner edge back
    return [to_screen(p) for p in ring + arc_centre(theta)]


def centre_of_mass(theta):
    return arc_centre(theta) + E * np.array([-math.sin(theta), -math.cos(theta)])


# ---------------------------------------------------------------- pygame
def draw(screen, font, theta, omega, e0, tipped):
    screen.fill((255, 255, 255))
    pygame.draw.line(screen, (0, 0, 0), (W / 2 - 300, GROUND_Y), (W / 2 + 300, GROUND_Y), 4)
    pts = outline(theta)
    pygame.draw.polygon(screen, (210, 210, 210), pts)
    pygame.draw.polygon(screen, (0, 0, 0), pts, 3)
    c = to_screen(arc_centre(theta))
    g = to_screen(centre_of_mass(theta))
    pygame.draw.line(screen, (200, 0, 0), c, g, 2)
    pygame.draw.circle(screen, (0, 0, 200), c, 5)          # arc centre
    pygame.draw.circle(screen, (200, 0, 0), g, 6)          # centre of mass

    fric, normal = contact_forces(theta, omega)
    lines = [f"theta = {math.degrees(theta):7.2f} deg",
             f"energy change = {(energy(theta, omega) - e0) / e0 * 100:+.4f} %",
             f"normal force N = {normal:6.2f} N   (weight = {MASS * g:.2f} N)",
             f"friction F = {fric:+6.2f} N   (needs mu >= {abs(fric) / normal:.2f})"]
    for i, txt in enumerate(lines):
        screen.blit(font.render(txt, True, (0, 0, 0)), (20, 20 + 26 * i))
    if tipped:
        msg = "Past 90 deg: the contact point has left the arc. Needs stage 2.  Press R to reset."
        screen.blit(font.render(msg, True, (200, 0, 0)), (20, 130))


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Stage 1 - rocking half-ring")
    font = pygame.font.SysFont("Consolas", 14)
    clock = pygame.time.Clock()

    theta, omega = THETA0, 0.0
    e0 = energy(theta, omega)
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
                pygame.quit()
                return
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_r:
                theta, omega = THETA0, 0.0
                e0 = energy(theta, omega)

        tipped = abs(theta) >= math.pi / 2
        if not tipped:
            for _ in range(4):                              # 4 physics steps per frame
                theta, omega = rk4_step(theta, omega, 1 / 240)

        draw(screen, font, theta, omega, e0, tipped)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()