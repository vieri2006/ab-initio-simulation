from ase import Atoms
from gpaw import GPAW
from gpaw import PW
from ase.optimize import GPMin, LBFGS, FIRE
from catlearn.optimize.mlmin import MLMin
from ase.io import read
from ase.constraints import FixAtoms
from ase.parallel import parprint
import logging
import timeit as time

"""
    Structure relaxation of NH3 using GPAW.
    DFT Benchmark using MLMin, GPMin, LBFGS and FIRE.
"""
# Change these values
fo1='step_1'
fo2='step_2'
ecut = 250
kpts = (4,4,4)

# Setup logger
logging.basicConfig(filename='time.log', filemode='a', format='%(message)s')

# Setup calculator:
calc = GPAW(mode=PW(ecut),
            xc='PBE',
            kpts=kpts,
            parallel={'band': 1},
            txt='gpaw.txt')

#########FIRST IMAGE####################
# 1. Build Atoms Object.
###############################################################################

# 1.1. Set up structure:

atoms=read('../'+fo1+'.xsf')
mask = [atom.position[2] < 17 for atom in atoms]
fixlayers = FixAtoms(mask=mask)
atoms.set_constraint(fixlayers)
atoms.set_pbc([1,1,1])

# 2. Benchmark.
###############################################################################
'''
# 2.C Optimize using LBFGS.
initial_lbfgs = atoms.copy()
initial_lbfgs.set_calculator(calc)
lbfgs_opt = LBFGS(initial_lbfgs, trajectory=fo1+'_lbfgs.traj')
itime=time.default_timer()
lbfgs_opt.run(fmax=0.01)
logging.warning('lbfgs =   %s', time.default_timer()-itime)
 
# 2.D Optimize using FIRE.
initial_fire = atoms.copy()
initial_fire.set_calculator(calc)
fire_opt = FIRE(initial_fire, trajectory=fo1+'_fire.traj')
itime=time.default_timer()
fire_opt.run(fmax=0.01)
logging.warning('fires =   %s', time.default_timer()-itime)
'''
# 2.A. Optimize structure using MLMin (CatLearn).
initial_mlmin = atoms.copy()
initial_mlmin.set_calculator(calc)
mlmin_opt = MLMin(initial_mlmin, trajectory=fo1+'_catlearn.traj')
itime=time.default_timer()
mlmin_opt.run(fmax=0.01, kernel='SQE')
logging.warning('mlmin =   %s', time.default_timer()-itime)

# 3. Summary of the results:
###############################################################################

print('\n Summary of the results:\n ------------------------------------')

fire_results = read(fo1+'_fire.traj', ':')
logging.warning('Number of function evaluations using FIRE:             %s',
         len(fire_results))

lbfgs_results = read(fo1+'_lbfgs.traj', ':')
logging.warning('Number of function evaluations using LBFGS:            %s',
         len(lbfgs_results))

catlearn_results = read(fo1+'_catlearn.traj', ':')
logging.warning('Number of function evaluations using MLMin (CatLearn): %s',
         len(catlearn_results))

########FINAL IMAGE#########

# 1. Build Atoms Object.
###############################################################################

# 1.1. Set up structure:

atoms=read('../'+fo2+'.xsf')
mask = [atom.position[2] < 17 for atom in atoms]
fixlayers = FixAtoms(mask=mask)
atoms.set_constraint(fixlayers)
atoms.set_pbc([1,1,1])

# 2. Benchmark.
###############################################################################

# 2.C Optimize using LBFGS.
initial_lbfgs = atoms.copy()
initial_lbfgs.set_calculator(calc)
lbfgs_opt = LBFGS(initial_lbfgs, trajectory=fo2+'_lbfgs.traj')
itime=time.default_timer()
lbfgs_opt.run(fmax=0.01)
logging.warning('lbfgs =   %s', time.default_timer()-itime)

# 2.D Optimize using FIRE.
initial_fire = atoms.copy()
initial_fire.set_calculator(calc)
fire_opt = FIRE(initial_fire, trajectory=fo2+'_fire.traj')
itime=time.default_timer()
fire_opt.run(fmax=0.01)
logging.warning('fires =   %s', time.default_timer()-itime)

# 2.A. Optimize structure using MLMin (CatLearn).
initial_mlmin = atoms.copy()
initial_mlmin.set_calculator(calc)
mlmin_opt = MLMin(initial_mlmin, trajectory=fo2+'_catlearn.traj')
itime=time.default_timer()
mlmin_opt.run(fmax=0.01, kernel='SQE')
logging.warning('mlmin =   %s', time.default_timer()-itime)

# 3. Summary of the results:
###############################################################################

print('\n Summary of the results:\n ------------------------------------')

fire_results = read(fo2+'_fire.traj', ':')
logging.warning('Number of function evaluations using FIRE:             %s',
         len(fire_results))

lbfgs_results = read(fo2+'_lbfgs.traj', ':')
logging.warning('Number of function evaluations using LBFGS:            %s',
         len(lbfgs_results))

catlearn_results = read(fo2+'_catlearn.traj', ':')
logging.warning('Number of function evaluations using MLMin (CatLearn): %s',
         len(catlearn_results))

