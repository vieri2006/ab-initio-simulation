from ase import Atoms
from ase.build import fcc111, add_adsorbate, bulk
from ase.io import read, write
from gpaw import GPAW, PW

a = 3.597 #lattice Cu
slab = fcc111('Cu', (1, 1, 3), a=a, vacuum=10.0)

for ecut in range(300, 951, 50):
        calc = GPAW(mode=PW(ecut),
                xc='PBE',
                kpts=(6, 6, 1),
                parallel={'band': 1},
                txt='scf-ecut_%d.txt' %ecut)
        slab.calc=calc
        slab.get_potential_energy()
