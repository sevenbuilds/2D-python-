import math 
import pygame 
import numpy as np
from sys import exit

#constants values 
#assuming values in SI units and 100pxl is considered to be 1m.
M = 1.0  # assuming kg
K = 15.0 # spring stiffness
L0 = 200 # rest length of spring in pxl
G = 900  # 900 pxls /s^2
DAMPING = 0.15
SUBSTEPS = 20
MIN_LENGTH = 25.0

W, H = 800, 600
ANCHOR = np.array([W / 2, 80])

def reset():
    pos = ANCHOR + np.array([140, L0 + 40])
    vel = np.zeros(2)
    return pos, vel

def calculate_forces(pos, vel):
    """This should return total force, gravity and spring force"""
    distance = pos - ANCHOR
    length = np.linalg.norm(distance)
    unit_vector = distance / length
    f_spring = -K * (length - L0) * unit_vector   # using hooke's law F = -Kx
    f_gravity = np.array([0.0, M * G])            # weight downwards in vertical component
    f_damping = -DAMPING * vel                    # damping formula for 2D
    total_force = f_spring + f_gravity + f_damping
    return total_force, f_gravity, f_spring

def step(pos, vel, dt):
    f, _, _ = calculate_forces(pos, vel)
    vel = vel + (f / M) * dt
    pos = pos + vel * dt
    d = pos - ANCHOR
    length = np.linalg.norm(d)

    if length < MIN_LENGTH:
        direction = d / length if length > 1e-8 else np.array([1.0, 0.0])
        pos = ANCHOR + direction * MIN_LENGTH
        # Remove velocity directed into the anchor
        radial_velocity = np.dot(vel, direction)
        if radial_velocity < 0:
            # vel in opposite direction
            vel -= radial_velocity * direction
    # need to return in order pos then vel
    return pos, vel

def spring_points(a, b, coils=9, width=13.0, lead=0.1, loop=7, samples=240):
    distance = b - a
    length = np.linalg.norm(distance)
    unit_vector = distance / length
    normal = np.array([-unit_vector[1], unit_vector[0]])
    start = a + unit_vector * length * lead
    body = length * ( 1 - 2 * lead)
    pts = [a , start]
    for i in range(samples + 1):
        t = i / samples
        phase = 2 * math.pi * coils * t
        along = body * t - loop * (1 - math.cos(phase))   # cos is horizontal change so it makes it go forward and backward
        side =  width * math.sin(phase)       # sin is vertical change so it make wave 
        pts.append(start + unit_vector * along + normal * side)
    pts.append(b)
    return pts

def pivot_point(surface, color, point, radius):
    #pygame.draw.circle(surface,color,center,radius,width)
    pygame.draw.circle(surface, color, point.astype(int), radius)
    pygame.draw.circle(surface, (160,160,160), point.astype(int), radius, 2)
    pygame.draw.circle(surface, (160,160,160), point.astype(int), 2)

def arrow(surface, color, start, vec, scale=0.12):
    end = start + vec * scale
    distance = end - start
    length = np.linalg.norm(distance)
    if length < 4:
        return
    pygame.draw.line(surface, color, start, end,3)
    ang = math.atan2(end[1] - start[1], end[0] - start[0])
    for s in (+1,-1):
        tip = end - 10 * np.array([math.cos(ang + s * 0.45), math.sin(ang + s * 0.45)])
        pygame.draw.line(surface, color, end, tip, 3)

def main():
    pygame.init()
    surface = pygame.display.set_mode((W,H))
    title = pygame.display.set_caption("Spring-mass system under gravity")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 16)

    running = True
    dragging = False
    show_forces = True
    trail = []
    pos, vel = reset()
    while running:
        frame_dt = min(clock.tick(60) / 1000.0, 1/30)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                exit()
            # type is for event and key is for keys
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                    exit()
                elif e.key == pygame.K_r:
                    pos, vel = reset()
                    trail.clear()
                elif e.key == pygame.K_f:
                    show_forces = not show_forces
            elif e.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = e.pos
                if np.linalg.norm(mouse_pos - pos) < 30:
                    dragging = True
            elif e.type == pygame.MOUSEBUTTONUP:
                dragging = False

        if dragging:
            # its mouse.get_pos() not mouse.getmousepos() and pos should be a numpy array
            pos = np.array(pygame.mouse.get_pos(), float)
            vel = np.zeros(2)
        else:
            dt = frame_dt / SUBSTEPS
            for _ in range(SUBSTEPS):
                pos, vel = step(pos, vel, dt)

        trail.append(tuple(pos))
        trail = trail[-120:]

        # ----- render part ------

        surface.fill((18,17,13))
        pygame.draw.line(surface, (0,0,0), (ANCHOR[0] - 82, ANCHOR[1]), (ANCHOR[0] + 82, ANCHOR[1]), 25)
        pygame.draw.line(surface, (10,9,21), (ANCHOR[0] - 80, ANCHOR[1]), (ANCHOR[0] + 80, ANCHOR[1]), 20)
        pivot_point(surface, (0,0,0), ANCHOR, 10)

        if len(trail) > 2:
            pygame.draw.lines(surface, (51,51,255), False, trail, 2)

        pts = spring_points(ANCHOR, pos)
        pygame.draw.lines(surface, (128,128,128), False, pts, 3)
        pygame.draw.circle(surface, (255,153,51), pos.astype(int), 22)
        pygame.draw.circle(surface, (204,102,0), pos.astype(int), 22, 3)

        if show_forces:
            _, f_gravity, f_spring = calculate_forces(pos, vel)
            arrow(surface, (102,102,225), pos, f_gravity)
            arrow(surface, (153, 255, 153), pos, f_spring)

        distance = pos - ANCHOR
        length = np.linalg.norm(distance)
        pe_g = -M * G * pos[1]
        pe_s = 0.5 * K * (length - L0) ** 2
        KE = 0.5 * M * ( vel @ vel)
        lines = [
            f"Kinetic energy: {KE:2.4f}  | Gravitational PE: {pe_g:2.4f}",
            f"length: {length:4.4f}   |  Spring PE: {pe_s:4.4f}   |  rest-length: 200px",
            "purple = gravity | green = spring force"
            "drag the weights | F arrows | R reset"]

        for i, v in enumerate(lines):
            surface.blit(font.render(v, True, (170, 175, 190)), (12, 10 + i * 20))

        pygame.display.flip()
    
    pygame.quit()
            
if __name__ == "__main__":
    main()