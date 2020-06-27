from ase import Atoms
from ase.build import fcc111, add_adsorbate, bulk
from ase.io import read, write
from gpaw import GPAW, PW

a = 3.597 #lattice Cu

for vac in range(1,5, 1):
        slab = fcc111('Cu', (1, 1, 3), a=a, vacuum=vac)
        calc = GPAW(mode=PW(850),
                xc='PBE',
                kpts=(5, 5, 1),
                parallel={'band': 1},
                txt='scf-vac_%d.txt' %vac)
        slab.calc=calc
        slab.get_potential_energy()

