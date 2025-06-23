#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 14:56:46 2024

@author: Teresia Olsson, teresia.olsson@helmholtz-berlin.de
"""

import numpy as np
import at
from itertools import chain

def mlsLattice() -> at.Lattice:
    
    # ---- Global ring parameters ----
    harmonic_number = 80
    energy = 629e6
    
    # ---- Dipole settings ----
    n_dipoles = 8
    dipole_length = 1.2
    bending_angle = np.pi*2/n_dipoles
    entrance_angle = np.pi*2/n_dipoles/2
    exit_angle = np.pi*2/n_dipoles/2
    
    # ---- Quadrupole settings based on power supply configurations ----
    VQ1     =  2.9624
    VQ1_SEP =  2.4746
    VQ2K    = -4.50667
    VQ2L    = -4.17499
    VQ3K    =  5.00574
    VQ3L    =  5.19192
    
    # ---- Sextupole settings based on power supply configurations ----
    # This needs to be updated!
    #//SEXTUPOLE DEFINITION  // xi_x=xi_y=+1
    VS1 =    0.0
    VS2 =    0.0
    #//VS1 =   89.5039;
    #//VS2 = -108.271;
    VS3 =    0.0
    
    #--------------------------
    #S1M2K1RP,S1M1L2RP, S1M2L4RP, S1M1K1RP
    #VS1P1=0.0
    #--------------------------
    #S1M2L2RP, S1M1K3RP, S1M2K3RP, S1M1L4RP
    #VS1P2=0.0
    #--------------------------
    #S2M2K1RP, S2M1L2RP, S2M2L4RP, S2M1K1RP
    #VS2P1=0.0
    #--------------------------
    #S2M2L2RP, S2M1K3RP, S2M2K3RP, S2M1L4RP
    #VS2P2=0.0
    #--------------------------
    #S3M2K1RP ,S3M1L2RP, S3M2L4RP, S3M1K1RP
    #VS3P1=0.0
    #--------------------------
    #S3M2L2RP, S3M1K3RP, S3M2K3RP, S3M1L4RP
    #VS3P2=0.0
    #--------------------------    
    
    # ---- Octupole settings based on power supply configurations ----
    VO1 = 0.0
    
    # ---- Cavity settings ----
    rf_frequency = 499654096.6666665
    main_cavity_voltage = 500e3
    
    # ---- Lattice ----
    
    # Lattice starts in middle of the injection straight
    
    first_half_of_K1 = [\
        at.Marker('SEP_MARKER'),\
        at.Drift('DKL2K1RP_1',1.2034),\
        at.Monitor('BPMZ5K1RP'),\
        at.Drift('DKL2K1RP_2',0.0466),\
        at.Sextupole('S3M2K1RP',0.1,h=VS3,Corrector='HV',KickAngle=[0,0]),\
        at.Drift('D1L4K1RP',0.15),\
        at.Quadrupole('Q3M2K1RP',0.2,k=VQ3K),\
        at.Drift('D1L5K1RP',0.15),\
        at.Quadrupole('Q2M2K1RP',0.2,k=VQ2K),\
        at.Drift('D3L3K1RP_1',0.054),\
        at.Monitor('BPMZ6K1RP'),\
        at.Drift('D3L3K1RP_2',0.371),\
        at.Dipole('BM2K1RP',dipole_length, bending_angle,EntranceAngle=entrance_angle, ExitAngle=exit_angle,FullGap=0.025*2,FringeInt1=0.5,FringeInt2=0.5),\
        at.Drift('D3L4K1RP',0.425),\
        at.Sextupole('S2M2K1RP',0.1,h=VS2,Corrector='V',KickAngle=[0,0]),\
        at.Drift('D4L2K1RP_1',0.049),\
        at.Monitor('BPMZ7K1RP'),\
        at.Drift('D4L2K1RP_2',0.251),\
        at.Sextupole('S1M2K1RP',0.1,h=VS1,Corrector='H',KickAngle=[0,0]),\
        at.Drift('D1L6K1RP',0.15),\
        at.Quadrupole('Q1M2K1RP',0.2,k=VQ1_SEP),\
        at.Drift('D2L2K1RP',0.125),\
        at.Octupole('OMK1RP', 0.1, [0,0,0,0], [0,0,0,VO1]),\
        ]
        
    L2 = [\
        at.Drift('D2L1L2RP_1',0.054),\
        at.Monitor('BPMZ1L2RP'),\
        at.Drift('D2L1L2RP_2',0.071),\
        at.Quadrupole('Q1M1L2RP',0.2,k=VQ1),\
        at.Drift('D1L1L2RP',0.15),\
        at.Sextupole('S1M1L2RP',0.1,h=VS1,Skew='CQ'),\
        at.Drift('D4L1L2RP',0.3),\
        at.Sextupole('S2M1L2RP',0.1,h=VS2,Corrector='V',KickAngle=[0,0]),\
        at.Drift('D3L1L2RP_1',0.054),\
        at.Monitor('BPMZ2L2RP'),\
        at.Drift('D3L1L2RP_2',0.371),\
        at.Dipole('BM1L2RP',dipole_length, bending_angle,EntranceAngle=entrance_angle, ExitAngle=exit_angle,FullGap=0.025*2,FringeInt1=0.5,FringeInt2=0.5),\
        at.Drift('D3L2L2RP_1',0.4122),\
        at.Monitor('BPMZ3L2RP'),\
        at.Drift('D3L2L2RP_2',0.0128),    
        at.Quadrupole('Q2M1L2RP',0.2,k=VQ2L),\
        at.Drift('D1L2L2RP',0.15),\
        at.Quadrupole('Q3M1L2RP',0.2,k=VQ3L),\
        at.Drift('D1L3L2RP',0.15),\
        at.Sextupole('S3M1L2RP',0.1,h=VS3,Corrector='HV',KickAngle=[0,0]),\
        at.Drift('DLL1L2RP_1',0.0466),\
        at.Monitor('BPMZ4L2RP'),\
        at.Drift('DLL1L2RP_2',2.9534),\
        at.Marker('U125'),\
        at.Drift('DLL2L2RP_1',2.9534),\
        at.Monitor('BPMZ5L2RP'),\
        at.Drift('DLL2L2RP_2',0.0466),\
        at.Sextupole('S3M2L2RP',0.1,h=VS3,Corrector='HV',KickAngle=[0,0]),\
        at.Drift('D1L4L2RP',0.15),\
        at.Quadrupole('Q3M2L2RP',0.2,k=VQ3L),\
        at.Drift('D1L5L2RP',0.15),\
        at.Quadrupole('Q2M2L2RP',0.2,k=VQ2L),\
        at.Drift('D3L3L2RP_1',0.054),\
        at.Monitor('BPMZ6L2RP'),\
        at.Drift('D3L3L2RP_2',0.371),\
        at.Dipole('BM2L2RP',dipole_length, bending_angle,EntranceAngle=entrance_angle, ExitAngle=exit_angle,FullGap=0.025*2,FringeInt1=0.5,FringeInt2=0.5),\
        at.Drift('D3L4L2RP',0.425),\
        at.Sextupole('S2M2L2RP',0.1,h=VS2,Corrector='V',KickAngle=[0,0]),\
        at.Drift('D4L2L2RP_1',0.049),\
        at.Monitor('BPMZ7L2RP'),\
        at.Drift('D4L2L2RP_2',0.251),\
        at.Sextupole('S1M2L2RP',0.1,h=VS1,Skew='CQ'),\
        at.Drift('D1L6L2RP',0.15),\
        at.Quadrupole('Q1M2L2RP',0.2,k=VQ1),\
        at.Drift('D2L2L2RP',0.125),\
        at.Octupole('OML2RP', 0.1, [0,0,0,0], [0,0,0,VO1]),\
        ]    
  
    K3 = [\
        at.Drift('D2L1K3RP_1',0.054),\
        at.Monitor('BPMZ1K3RP'),\
        at.Drift('D2L1K3RP_2',0.071),\
        at.Quadrupole('Q1M1K3RP',0.2,k=VQ1),\
        at.Drift('D1L1K3RP',0.15),\
        at.Sextupole('S1M1K3RP',0.1,h=VS1,Corrector='H',KickAngle=[0,0]),\
        at.Drift('D4L1K3RP',0.3),\
        at.Sextupole('S2M1K3RP',0.1,h=VS2,Corrector='V',KickAngle=[0,0]),\
        at.Drift('D3L1K3RP_1',0.054),\
        at.Monitor('BPMZ2K3RP'),\
        at.Drift('D3L1K3RP_2',0.371),\
        at.Dipole('BM1K3RP',dipole_length, bending_angle,EntranceAngle=entrance_angle, ExitAngle=exit_angle,FullGap=0.025*2,FringeInt1=0.5,FringeInt2=0.5),\
        at.Drift('D3L2K3RP_1',0.4122),\
        at.Monitor('BPMZ3K3RP'),\
        at.Drift('D3L2K3RP_2',0.0128),\
        at.Quadrupole('Q2M1K3RP',0.2,k=VQ2K),\
        at.Drift('D1L2K3RP',0.15),\
        at.Quadrupole('Q3M1K3RP',0.2,k=VQ3K),\
        at.Drift('D1L3K3RP',0.15),\
        at.Sextupole('S3M1K3RP',0.1,h=VS3,Corrector='HV',KickAngle=[0,0]),\
        at.Drift('DKL1K3RP_1',0.0466),\
        at.Monitor('BPMZ4K3RP'),\
        at.Drift('DKL1K3RP_2',1.2034),\
        at.Drift('DKL2K3RP_1',1.2034),\
        at.Monitor('BPMZ5K3RP'),\
        at.Drift('DKL2K3RP_2',0.0466),\
        at.Sextupole('S3M2K3RP',0.1,h=VS3,Corrector='HV',KickAngle=[0,0]),\
        at.Drift('D1L4K3RP',0.15),\
        at.Quadrupole('Q3M2K3RP',0.2,k=VQ3K),\
        at.Drift('D1L5K3RP',0.15),\
        at.Quadrupole('Q2M2K3RP',0.2,k=VQ2K),\
        at.Drift('D3L3K3RP_1',0.054),\
        at.Monitor('BPMZ6K3RP'),\
        at.Drift('D3L3K3RP_2',0.371),\
        at.Dipole('BM2K3RP',dipole_length, bending_angle,EntranceAngle=entrance_angle, ExitAngle=exit_angle,FullGap=0.025*2,FringeInt1=0.5,FringeInt2=0.5),\
        at.Drift('D3L4K3RP',0.425),\
        at.Sextupole('S2M2K3RP',0.1,h=VS2,Corrector='V',KickAngle=[0,0]),\
        at.Drift('D4L2K3RP_1',0.049),\
        at.Monitor('BPMZ7K3RP'),\
        at.Drift('D4L2K3RP_2',0.251),\
        at.Sextupole('S1M2K3RP',0.1,h=VS1,Corrector='H',KickAngle=[0,0]),\
        at.Drift('D1L6K3RP',0.15),\
        at.Quadrupole('Q1M2K3RP',0.2,k=VQ1),\
        at.Drift('D2L2K3RP',0.125),\
        at.Octupole('OMK3RP', 0.1, [0,0,0,0], [0,0,0,VO1]),\
        ]  
        
    L4 = [\
        at.Drift('D2L1L4RP_1',0.054),\
        at.Monitor('BPMZ1L4RP'),\
        at.Drift('D2L1L4RP_2',0.071),\
        at.Quadrupole('Q1M1L4RP',0.2,k=VQ1),\
        at.Drift('D1L1L4RP',0.15),\
        at.Sextupole('S1M1L4RP',0.1,h=VS1,Skew='CQ'),\
        at.Drift('D4L1L4RP',0.3),\
        at.Sextupole('S2M1L4RP',0.1,h=VS2,Corrector='V',KickAngle=[0,0]),\
        at.Drift('D3L1L4RP_1',0.054),\
        at.Monitor('BPMZ2L4RP'),\
        at.Drift('D3L1L4RP_2',0.371),\
        at.Dipole('BM1L4RP',dipole_length, bending_angle,EntranceAngle=entrance_angle, ExitAngle=exit_angle,FullGap=0.025*2,FringeInt1=0.5,FringeInt2=0.5),\
        at.Drift('D3L2L4RP_1',0.4122),\
        at.Monitor('BPMZ3L4RP'),\
        at.Drift('D3L2L4RP_2',0.0128),\
        at.Quadrupole('Q2M1L4RP',0.2,k=VQ2L),\
        at.Drift('D1L2L4RP',0.15),\
        at.Quadrupole('Q3M1L4RP',0.2,k=VQ3L),\
        at.Drift('D1L3L4RP',0.15),\
        at.Sextupole('S3M1L4RP',0.1,h=VS3,Corrector='HV',KickAngle=[0,0]),\
        at.Drift('DLL1L4RP_1',0.0466),\
        at.Monitor('BPMZ4L4RP'),\
        at.Drift('DLL1L4RP_2',2.8034),\
        at.RFCavity('CAV',0.3,main_cavity_voltage,rf_frequency,harmonic_number,energy),\
        at.Drift('DLL2L4RP_1',2.8034),\
        at.Monitor('BPMZ5L4RP'),\
        at.Drift('DLL2L4RP_2',0.0466),\
        at.Sextupole('S3M2L4RP',0.1,h=VS3,Corrector='HV',KickAngle=[0,0]),\
        at.Drift('D1L4L4RP',0.15),\
        at.Quadrupole('Q3M2L4RP',0.2,k=VQ3L),\
        at.Drift('D1L5L4RP',0.15),\
        at.Quadrupole('Q2M2L4RP',0.2,k=VQ2L),\
        at.Drift('D3L3L4RP_1',0.054),\
        at.Monitor('BPMZ6L4RP'),\
        at.Drift('D3L3L4RP_2',0.371),\
        at.Dipole('BM2L4RP',dipole_length, bending_angle,EntranceAngle=entrance_angle, ExitAngle=exit_angle,FullGap=0.025*2,FringeInt1=0.5,FringeInt2=0.5),\
        at.Drift('D3L4L4RP',0.425),\
        at.Sextupole('S2M2L4RP',0.1,h=VS2,Corrector='V',KickAngle=[0,0]),\
        at.Drift('D4L2L4RP_1',0.049),\
        at.Monitor('BPMZ7L4RP'),\
        at.Drift('D4L2L4RP_2',0.251),\
        at.Sextupole('S1M2L4RP',0.1,h=VS1,Skew='CQ'),\
        at.Drift('D1L6L4RP',0.15),\
        at.Quadrupole('Q1M2L4RP',0.2,k=VQ1),\
        at.Drift('D2L2L4RP',0.125),\
        at.Octupole('OML4RP', 0.1, [0,0,0,0], [0,0,0,VO1]),\
        ]
      
    second_half_of_K1 = [\
        at.Drift('D2L1K1RP_1',0.054),\
        at.Monitor('BPMZ1K1RP'),\
        at.Drift('D2L1K1RP_2',0.071),\
        at.Quadrupole('Q1M1K1RP',0.2,k=VQ1_SEP),\
        at.Drift('D1L1K1RP',0.15),\
        at.Sextupole('S1M1K1RP',0.1,h=VS1,Corrector='H',KickAngle=[0,0]),\
        at.Drift('D4L1K1RP',0.3),\
        at.Sextupole('S2M1K1RP',0.1,h=VS2,Corrector='V',KickAngle=[0,0]),\
        at.Drift('D3L1K1RP_1',0.054),\
        at.Monitor('BPMZ2K1RP'),\
        at.Drift('D3L1K1RP_2',0.371),\
        at.Dipole('BM1K1RP',dipole_length, bending_angle,EntranceAngle=entrance_angle, ExitAngle=exit_angle,FullGap=0.025*2,FringeInt1=0.5,FringeInt2=0.5),\
        at.Drift('D3L2K1RP_1',0.4122),\
        at.Monitor('BPMZ3K1RP'),\
        at.Drift('D3L2K1RP_2',0.0128),\
        at.Quadrupole('Q2M1K1RP',0.2,k=VQ2K),\
        at.Drift('D1L2K1RP',0.15),\
        at.Quadrupole('Q3M1K1RP',0.2,k=VQ3K),\
        at.Drift('D1L3K1RP',0.15),\
        at.Sextupole('S3M1K1RP',0.1,h=VS3, Corrector='HV',KickAngle=[0,0]),\
        at.Drift('DKL1K1RP_1',0.0466),\
        at.Monitor('BPMZ4K1RP'),\
        at.Drift('DKL1K1RP_2',1.2034),\
        ]
        
    # ---- Ring definition ----
    
    ring = [first_half_of_K1, L2, K3, L4, second_half_of_K1]
        
    # Expand ring until list completely flattened
    while any(isinstance(x, list) for x in ring):
        ring = list(chain.from_iterable(i if isinstance(i, list) else [i] for i in ring))
          
    # Build the lattice  
    ring = at.Lattice(ring,name='MLS',energy=energy,periodicity=1)
    
    # Turn cavity and radiation on so 6D calculations is default
    ring.enable_6d()
    
    # Set main cavity phases
    ring.set_cavity_phase(cavpts='CAV')
    
    return ring

if __name__ == '__main__':
    ring = mlsLattice()
