from ase import Atoms
from ase.build import fcc111, add_adsorbate, bulk
from ase.io import read, write
from gpaw import GPAW, PW

a = 3.597 #lattice Cu
slab = fcc111('Cu', (1, 1, 3), a=a, vacuum=10.0)

for k in range(2, 11, 1):
        calc = GPAW(mode=PW(850),
                xc='PBE',
                kpts=(k, k, 1),
                parallel={'band': 1},
                txt='scf-k_%d.txt' %k)
        slab.calc=calc
        slab.get_potential_energy()
