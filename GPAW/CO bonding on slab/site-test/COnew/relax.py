from ase import Atoms
from gpaw import GPAW, PW
from ase.optimize import BFGS
from ase.build import fcc111, add_adsorbate, bulk
from gpaw import GPAW, PW
from ase.io import read, write
from ase.constraints import FixAtoms

adsorbate = Atoms('CO')
adsorbate[1].z = 1.43 #panjang ikatan CO
adsorbate.center(vacuum=5)

c = FixAtoms(indices=[0])
adsorbate.set_constraint(c)

calc = GPAW(mode=PW(750),
        xc='PBE',
        parallel={'band': 1},
        txt='relax-co.txt')
adsorbate.calc=calc
adsorbate.get_potential_energy()

relax = BFGS(adsorbate, logfile='bfgs.log', trajectory='co.traj')
relax.run(fmax=0.05)
