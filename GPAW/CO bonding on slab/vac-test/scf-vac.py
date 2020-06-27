from ase import Atoms
from ase.build import fcc111, add_adsorbate, bulk
from ase.io import read, write
from gpaw import GPAW, PW

adsorbate = Atoms('CO')
adsorbate[1].z = 1.43 #panjang ikatan CO

a = 4.046 #lattice Al

for vac in range(16, 21, 1):
        slab = fcc111('Al', (1, 1, 3), a=a, vacuum=vac)
        add_adsorbate(slab, adsorbate, 1.8, 'ontop')
        calc = GPAW(mode=PW(750),
                xc='PBE',
                kpts=(8, 8, 1),
                parallel={'band': 1},
                txt='scf-vac_%d.txt' %vac)
        slab.calc=calc
        slab.get_potential_energy()

