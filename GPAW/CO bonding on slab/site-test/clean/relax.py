from ase import Atoms
from gpaw import GPAW, PW
from ase.optimize import BFGS
from ase.build import fcc111, add_adsorbate, bulk
from gpaw import GPAW, PW
from ase.io import read, write
from ase.constraints import FixAtoms

a = 4.046 #lattice Al

slab = fcc111('Al', (1, 1, 3), a=a, vacuum=10)
c = FixAtoms(indices=[0])
slab.set_constraint(c)

calc = GPAW(mode=PW(750),
        xc='PBE',
        kpts=(8, 8, 1),
        parallel={'band': 1},
        txt='relax-clean.txt')
slab.calc=calc
slab.get_potential_energy()

relax = BFGS(slab, logfile='bfgs.log', trajectory='clean.traj')
relax.run(fmax=0.05)
energy = slab.get_potential_energy()

