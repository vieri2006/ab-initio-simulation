from ase import Atoms
from ase.build import fcc111, add_adsorbate, bulk
from ase.io import read, write
from gpaw import GPAW, PW

a = 3.597 #lattice Cu
bulk = bulk('Cu','fcc', a=a)

for ecut in range(300, 951, 50):
        calc = GPAW(mode=PW(ecut),
                xc='PBE',
                kpts=(6, 6, 6),
                parallel={'band': 1},
                txt='scf-ecut_%d.txt' %ecut)
        bulk.calc=calc
        bulk.get_potential_energy()
