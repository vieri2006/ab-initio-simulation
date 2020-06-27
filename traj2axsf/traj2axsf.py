#!/usr/bin/python

import sys, getopt
from ase.io.trajectory import Trajectory
from ase.visualize import view
from ase.io import read, write
import os

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('traj2axsf.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('traj2axsf.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    
    assert inputfile != '' and outputfile != '', 'USE: traj2axsf.py -i <inputfile> -o <outputfile>'
    
    traj=Trajectory(inputfile)
    l=len(traj)

    for i,atoms in enumerate(traj):
        write(outputfile+'-%d.xsf'%(i),atoms)
    
    wfile = open(outputfile+'.axsf', "w")
    wfile.write("ANIMSTEPS %d\n" % (l))
    
    rfile = open(outputfile+'-0.xsf', "r")
    for i in range(0,5):
        wfile.write(rfile.readline())
    wfile.close()
    
    wfile = open(outputfile+'.axsf', "a")
    for i in range(0,l):
        rfile = open(outputfile+'-%d.xsf' % (i), "r")
        for j in range(0,6):
            rfile.readline()
        wfile.write("\nPRIMCOORD %d\n" % (i+1))
        wfile.write(rfile.read())
    rfile.close()
    wfile.close()
    for i in range(0,l):
        os.remove(outputfile+"-%d.xsf" % (i))

if __name__ == "__main__":
   main(sys.argv[1:])
