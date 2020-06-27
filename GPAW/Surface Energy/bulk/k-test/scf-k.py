from ase import Atoms
from ase.build import fcc111, add_adsorbate, bulk
from ase.io import read, write
from gpaw import GPAW, PW

a = 3.597 #lattice Cu
bulk = bulk('Cu','fcc', a=a)

for k in range(2, 9, 1):
        calc = GPAW(mode=PW(850),
                xc='PBE',
                kpts=(k, k, k),
                parallel={'band': 1},
                txt='scf-ecut_%d.txt' %k)
        bulk.calc=calc
        bulk.get_potential_energy()
