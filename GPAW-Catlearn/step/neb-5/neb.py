from ase.neb import NEB
from ase.optimize import BFGS, MDMin
import matplotlib.pyplot as plt
from catlearn.optimize.mlneb import MLNEB
from ase.neb import NEBTools
import copy
from catlearn.optimize.tools import plotneb

from ase import Atoms
from gpaw import GPAW, PW
from ase.io import read
from ase.constraints import FixAtoms
from ase.parallel import parprint

from gpaw.mpi import rank, size

import logging
import timeit as time

""" 
    Toy model rearrangement of Pt heptamer island on Pt(111).
    This example contains: 
    1. Optimization of the initial and final end-points of the reaction path. 
    2.A. NEB optimization using CI-NEB as implemented in ASE. 
    2.B. NEB optimization using our machine-learning surrogate model.
    3. Comparison between the ASE NEB and our ML-NEB algorithm.
"""

# 1. Structural relaxation. ##################################################

#setup awal
fo1='../optimize/step_1_catlearn.traj'
fo2='../optimize/step_2_catlearn.traj'
ecut=250
xc='PBE'
kpts=(4,4,4)

# Setup logger
logging.basicConfig(filename='time.log', filemode='a', format='%(message)s')

# Setup calculator:
calc = GPAW(mode=PW(ecut),
            xc=xc,
            kpts=kpts,
            parallel={'band': 1},
            txt='gpaw.txt')

# Set number of images
n_images = 5
n_images = n_images-2

# 1.1. Structures:
slab_initial = read(fo1)
slab_final = read(fo2)

# 2.A. NEB using ASE

initial_ase = slab_initial
final_ase = slab_final

n = size // n_images      # number of cpu's per image
j = 1 + rank // n  # my image number
assert n_images * n == size

images_ase = [initial_ase]

for i in range(n_images):
    ranks = range(i * n, (i + 1) * n)
    image = initial_ase.copy()

    if rank in ranks:

        calc_ase = GPAW(mode=PW(ecut),
                    xc=xc,
                    kpts=kpts,
                    parallel={'band': 1},
                    txt='neb{}.txt'.format(j),
                    communicator=ranks)

        image.set_calculator(calc_ase)

    images_ase.append(image)

images_ase.append(final_ase)

neb_ase = NEB(images_ase, parallel=True, climb=True)
neb_ase.interpolate(method='idpp')

qn_ase = MDMin(neb_ase, logfile='neb_ase.log', trajectory='neb_ase.traj')
itime=time.default_timer()
qn_ase.run(fmax=0.05)
logging.warning('ase =   %s', time.default_timer()-itime)

# 2.B. NEB using CatLearn

neb_catlearn = MLNEB(start=slab_initial, end=slab_final,
                     ase_calc=calc,
                     n_images=n_images+2,
                     interpolation='idpp', restart=False)

itime=time.default_timer()
neb_catlearn.run(fmax=0.05, trajectory='ML-NEB.traj')
logging.warning('mlneb =   %s', time.default_timer()-itime)

# 3. Summary of the results

# NEB ASE:
logging.warning('Summary of the results: ')

atoms_ase = read('neb_ase.traj', ':')
n_eval_ase = len(atoms_ase) - 2 * (len(atoms_ase)/n_images)

logging.warning('Number of function evaluations CI-NEB implemented in ASE: %d', n_eval_ase)

# ML-NEB:
atoms_catlearn = read('evaluated_structures.traj', ':')
n_eval_catlearn = len(atoms_catlearn) - 2
logging.warning('Number of function evaluations CatLearn: %d', n_eval_catlearn)

# Comparison:
logging.warning('The ML-NEB algorithm required {} times less number of function evaluations than the standard NEB algorithm.'.format(n_eval_ase/n_eval_catlearn))

# Plot ASE NEB:
'''
nebtools_ase = NEBTools(images_ase)

Sf_ase = nebtools_ase.get_fit()[2]
Ef_ase = nebtools_ase.get_fit()[3]

Ef_neb_ase, dE_neb_ase = nebtools_ase.get_barrier(fit=False)
nebtools_ase.plot_band()

plt.show()
'''
# Plot ML-NEB predicted path and show images along the path:
plotneb(trajectory='ML-NEB.traj', view_path=False)

