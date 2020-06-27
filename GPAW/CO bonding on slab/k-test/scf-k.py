from ase import Atoms
from ase.build import fcc111, add_adsorbate, bulk
from ase.io import read, write
from gpaw import GPAW, PW

adsorbate = Atoms('CO')
adsorbate[1].z = 1.43 #panjang ikatan CO

a = 4.046 #lattice Al
slab = fcc111('Al', (1, 1, 3), a=a, vacuum=10.0)
add_adsorbate(slab, adsorbate, 1.8, 'ontop')

for k in range(2, 11, 1):
        calc = GPAW(mode=PW(750),
                xc='PBE',
                kpts=(k, k, 1),
                parallel={'band': 1},
                txt='scf-k_%d.txt' %k)
        slab.calc=calc
        slab.get_potential_energy()
