# Spring-mass simulator
A 2D interactive spring-mass simulator built using python and its libraries like numpy and pygame.

About this project.
This project simulates a mass and spring attached to a rigid surface where the mass moves with various 
forces acting on it like gravity, spring-force and damping force.
I created this project since I wanted to apply my therotical knowledge that I learned in school practically and figure out how simulations work.

Features:
- interactive simulation - you can see how springs behave and also drag the mass
- Hooke's law - uses hooke's law to simulate spring behaviour
- damping - the oscillation slowly loses energy due to damping just like irl
- numerical simulation - in each frame physics is calculated 20 times so there is less error

Equations used in this project:
- Hooke's law: F = -Kx
- Newton's 2nd law: F = ma
- Damping eqn in 2D = - Damping coefficient x velocity

Built with:
- python
- numpy
- pygame

Ignore:
numpy folder, pygame folder, rough folder 
because before this project I had zero knowledge about pygame, numpy and simulating physics I had to learn those so I experimented in those folder.

How to run:
1. install python 3, if you haven't
2. to install numpy and pygame paste this in terminal: pip install pygame-ce numpy
3. downlaod the spring_mass.py from my github repository
4. run the code using vs code or other code editor.

Additional info:
I created this project to visualize physics behaviour to learn more clearly since I'm a visual learner and AI is only used to for learning, clearing doubts and ideas, I tried creating a more advanced 
system with semi-annulus, 3 springs and a rolling mass inside it but failed, I realized I lack the knowledge to create those after all I'm just a high school kid but I'll be trying in future to create those complex simulation as I learn more. I was learning physics and trying to create that system for this project but due to time constraint I'm unable to but I'll be improving it in future projects.
