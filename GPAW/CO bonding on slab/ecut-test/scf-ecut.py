from ase import Atoms
from ase.build import fcc111, add_adsorbate, bulk
from ase.io import read, write
from gpaw import GPAW, PW

adsorbate = Atoms('CO')
adsorbate[1].z = 1.43 #panjang ikatan CO

a = 4.046 #lattice Al
slab = fcc111('Al', (1, 1, 3), a=a, vacuum=10.0)
add_adsorbate(slab, adsorbate, 1.8, 'ontop')

for ecut in range(750, 951, 50):
        calc = GPAW(mode=PW(ecut),
                xc='PBE',
                kpts=(6, 6, 1),
                parallel={'band': 1},
                txt='scf-ecut_%d.txt' %ecut)
        slab.calc=calc
        slab.get_potential_energy()
