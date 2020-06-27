from ase import Atoms
from ase.io import read, write
from gpaw import GPAW, PW
from ase.constraints import FixAtoms

atoms=read('../heptamer_1.xsf')
mask = [atom.position[2] < 13 for atom in atoms]
fixlayers = FixAtoms(mask=mask)
atoms.set_constraint(fixlayers)
atoms.set_pbc([1,1,1])

for k in range(2, 11, 1):
        calc = GPAW(mode=PW(150),
                xc='PBE',
                kpts=(k, k, k),
                parallel={'band': 1},
                txt='scf-k_%02d.txt' %k)
        atoms.calc=calc
        atoms.get_potential_energy()
