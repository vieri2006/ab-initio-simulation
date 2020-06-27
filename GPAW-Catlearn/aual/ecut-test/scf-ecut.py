from ase import Atoms
from ase.io import read, write
from gpaw import GPAW, PW
from ase.constraints import FixAtoms

atoms=read('../aual_1.xsf')
mask = [atom.position[2] < 8 for atom in atoms]
fixlayers = FixAtoms(mask=mask)
atoms.set_constraint(fixlayers)
atoms.set_pbc([1,1,1])

for ecut in range(100, 300, 50):
        calc = GPAW(mode=PW(ecut),
                xc='PBE',
                kpts=(4, 4, 4),
                parallel={'band': 1},
                txt='scf-ecut_%d.txt' %ecut)
        atoms.calc=calc
        atoms.get_potential_energy()
