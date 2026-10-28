import numpy as np
import pygame
import math
from sys import exit 

W, H = 800, 600
MIDPOINT = np.array([W / 2, 400])

R_OUT = 0.25
R_IN = 0.20
GROUND_H = 400
MASS = 1.0                              #kg
THETA0 = 0.4                            # in radians
g = 9.8                                 # m/s^2
DAMPING = 0.5                           # Nms/rad

# colors
white = (255,255,255)
black = (0,0,0)
BG = (36,38,43)
SPRING_REST = (239, 159, 39)                # amber at rest
SPRING_COMP = (55, 138, 221)                # blue when compressed
SPRING_STRETCH = (226, 75, 74)              # red when stretched
GROUND_C = (58, 58, 56)
GROUND_EDGE = (136, 135, 128)
SPRING_OUTLINE = (20, 20, 22)
TEXT_C = (180, 178, 169)
FORCE_SPRING = (175, 169, 236)              # lavender
FORCE_DAMP = (237, 147, 177)                # pink

# equations
# E = distance from center to COM of hallow semi circle 
# I_G = Moment of inertia  about the center of mass (how hard it is to spin as COM goes far form rotation point)

E = 4 * (R_OUT**3 - R_IN**3) / 3 * math.pi * (R_OUT**2 - R_IN**2)
I_G = MASS * (R_OUT**2 - R_IN**2) / 2 - MASS * E**2

def moment_of_inertia(theta):
    # moment of inertia about the contact point.
    return MASS * (R_OUT**2 - R_IN**2) / 2 + MASS * (E**2 + R_OUT**2 - 2 * E * R_OUT * math.cos(theta))

def acceleration(theta, omega):
    lever_arm = math.sqrt(E**2 + R_OUT**2 - 2 * E * R_OUT * math.cos(theta))
    angle = math.asin(E * math.sin(theta) / lever_arm)
    g_torque = -MASS * g * lever_arm * math.sin(angle) 
    f_damping = -DAMPING * omega
    """ When the body tilts outward, the inertia gets bigger. If ω stayed the same,
    the kinetic energy would go up for free, and that’s not allowed.
    So ω has to drop a bit more than gravity alone would make it drop.

    That extra drop in ω is this term. It slows the spin-up when tilting outward,
    so it has the same sign as gravity’s pull (negative).
    """
    correction = MASS

def energy(theta, omega):
    # KE about I and angular vel and PE from contact point to COM height
    KE = 0.5 * moment_of_inertia(theta) * omega**2
    PE = MASS * g * (R_OUT - E * math.cos(theta))
    return KE + PE

def main():
    pygame.init()
    surface = pygame.display.set_mode((W,H))
    clock = pygame.time.Clock()
    title = pygame.display.set_caption("Physics simulation of rocking semi circle.")
    font = pygame.font.SysFont(("Consolas"), 16)
    mid_point_text = font.render(("mid-point"), True, TEXT_C)

    running = True
    theta, omega = THETA0, 0.0
    initial_energy = energy(theta, omega)
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                    exit()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                theta, omega = THETA0, 0.0
                initial_energy = energy(theta, omega)

        #----- rendering part -------
                    
        surface.fill(BG)
        pygame.draw.rect(
            surface,
            GROUND_C, 
            (0,GROUND_H,W,200))
        pygame.draw.line(surface,GROUND_EDGE,(0, GROUND_H),(800, GROUND_H),4)

        #----- slash lines -----
        for x in range(0, 800, 20):
            pygame.draw.line(surface, GROUND_EDGE, (x + 10, GROUND_H), (x, GROUND_H + 10), 2)
        for y in range(GROUND_H, 200, -20):
            pygame.draw.line(surface, GROUND_EDGE, (MIDPOINT[0], y), (MIDPOINT[0], y + 10), 2)

        #----- text ------
        surface.blit(mid_point_text, (MIDPOINT[0] - 40, MIDPOINT[1] + 20))

        pygame.display.flip()
    pygame.quit()
            
if __name__ == "__main__":
    main()

