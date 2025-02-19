#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 13:56:20 2023

@author: jeromeguterl
"""


from particle_distribution import *
from surface_elements import *
from io_gitrm import *
fn = "/Users/jeromeguterl/development/gitrm/nathd_example.cfg"
fe = SurfaceElements(fn)
fe.save('test.pkl')
fee = SurfaceElements.load('test.pkl')
fe.Plot(GroupID=547)
fe.ShowNormals()
mass = 183
els = fe.get_elements(547)
print(len(els))
for el in els:
    p = ParticleDistribution(1000, mass)
    E = p.generate('Thomson')
    theta = p.generate('SinCos')
    phi = p.generate('Uniform', x=np.linspace(0, 2*np.pi, p.np))

    p.compute_velocity(E, theta, phi)
    p.generate_positions(el)
    el.p = p
    el.p.globalId = np.zeros((p.np,), dtype=int) + int(el.global_id)


def make_particle_source(els):
    attrs = ['x', 'y', 'z', 'vx', 'vy', 'vz', 'globalId']

    dic = dict((attr, np.hstack([getattr(el.p, attr)
               for el in els])) for attr in attrs)
    dic['np'] = len(dic['x'])
    return dic


source = make_particle_source(els)
fn = 'particle_source_test_int4.nc'
write_particle_source(fn, source)

# Set positions of particles

# class SE():
#     def __init__(el):
#         el.v1 = [1, 0, 0]
#         el.v2 = [0, 0, 1]
#         el.v3 = [0, 1, 0]

# el = SE()

# generate_positions(p, el)
# plt.figure()
# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# ax.scatter(x[:, 0], x[:, 1], x[:, 2])
