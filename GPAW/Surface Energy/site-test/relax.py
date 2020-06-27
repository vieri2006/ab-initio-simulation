from ase import Atoms
from gpaw import GPAW, PW
from ase.optimize import BFGS
from ase.build import fcc111, add_adsorbate, bulk
from gpaw import GPAW, PW
from ase.constraints import FixAtoms

a = 3.597 #lattice Cu
slab = fcc111('Cu', (1, 1, 3), a=a, vacuum=4)
calc = GPAW(mode=PW(850),
            xc='PBE',
            kpts=(4, 4, 1),
            parallel={'band': 1},
            txt='relax.txt')

c = FixAtoms(indices=[0])
slab.set_constraint(c)

slab.calc=calc
slab.get_potential_energy()

relax = BFGS(slab, logfile='bfgs.log', trajectory='slab.traj')
relax.run(fmax=0.005)

