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
    
    # Global ring parameters
    harmonic_number = 80
    energy = 629e6
    
    # Dipole settings and slicing
    n_dipoles = 8
    dipole_length = 1.2
    bending_angle = np.pi*2/n_dipoles
    entrance_angle = np.pi*2/n_dipoles/2
    exit_angle = np.pi*2/n_dipoles/2
    
    # Quadrupole settings based on power supply configurations
    #//QUADRUPOLE DEFINITION // Qx=3.178,Qy=2.232,alpha_0=0.03
    VQ1     =  2.9624
    VQ1_SEP =  2.4746
    VQ2K    = -4.50667
    VQ2L    = -4.17499
    VQ3K    =  5.00574
    VQ3L    =  5.19192
    
    # Sextupole settings based on power supply configurations
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
    
    
    # Octupole settings based on power supply configurations
    VO1 = 0.0
    
    # Cavity settings
    rf_frequency = 499654096.6666665
    main_cavity_voltage = 500e3/2.0
    
#    CAV: RFCAVITY,L=0.15,VOLT=-0.5/2.0,HARMON=80,no_cavity_totalpath=true; // 1/2 RF CAV    
   
    # at.Marker('QPD00')
    # at.Marker('QPD01')
    # at.Marker('IR')
    # at.Marker('THZ')
    # at.Marker('VUV')
    # at.Marker('EUV')
    # at.Marker('QNIM')
           
# //DIPOLE DEFINITION
# //BBSBEND: SBEND, L=1.2, ANGLE=PI/4;
# //BBDIPEDGE1: dipedge, h=PI/4./1.2,E1=PI/8.,hgap=0.025,FINT=0.5;
# //BBDIPEDGE2: dipedge, h=PI/4./1.2,E1=PI/8.,hgap=0.025,FINT=0.5;
# //BB: line=(BBDIPEDGE1,BBSBEND,BBDIPEDGE2);
# BBSBENDquarter: SBEND, L=1.2/4, ANGLE=PI/4/4;
# BBDIPEDGE1: dipedge, h=PI/4./1.2,E1=PI/8.,hgap=0.025,FINT=0.5;
# BBDIPEDGE2: dipedge, h=PI/4./1.2,E1=PI/8.,hgap=0.025,FINT=0.5;
# BB1: line=(BBDIPEDGE1,BBSBENDquarter,BBSBENDquarter,BBSBENDquarter,BBSBENDquarter,BBDIPEDGE2);
# BB2: line=(BBDIPEDGE1,BBSBENDquarter,BBSBENDquarter,BBSBENDquarter,BBSBENDquarter,BBDIPEDGE2);
# BB3: line=(BBDIPEDGE1,BBSBENDquarter,QPD01,BBSBENDquarter,QNIM,BBSBENDquarter,BBSBENDquarter,BBDIPEDGE2);
# BB4: line=(BBDIPEDGE1,BBSBENDquarter,EUV,BBSBENDquarter,VUV,BBSBENDquarter,BBSBENDquarter,BBDIPEDGE2);
# BB5: line=(BBDIPEDGE1,BBSBENDquarter,THZ,BBSBENDquarter,BBSBENDquarter,BBSBENDquarter,BBDIPEDGE2);
# BB6: line=(BBDIPEDGE1,BBSBENDquarter,IR,BBSBENDquarter,QPD00,BBSBENDquarter,BBSBENDquarter,BBDIPEDGE2);
# BB7: line=(BBDIPEDGE1,BBSBENDquarter,BBSBENDquarter,BBSBENDquarter,BBSBENDquarter,BBDIPEDGE2);
# BB8: line=(BBDIPEDGE1,BBSBENDquarter,BBSBENDquarter,BBSBENDquarter,BBSBENDquarter,BBDIPEDGE2);


    first_half_of_K1 = [\
        at.Marker('SEP_MARKER'),\
        at.Drift('DK',1.25),\
        at.Monitor('BPMZ5K1RP'),\
        at.Sextupole('S3M2K1RP',0.1,h=VS3,Corrector='HV',KickAngle=[0,0]),\
        at.Drift('D1',0.15),\
        at.Quadrupole('Q3M2K1RP',0.2,k=VQ3K),\
        at.Drift('D1',0.15),\
        at.Quadrupole('Q2M2K1RP',0.2,k=VQ2K),\
        at.Drift('D3',0.425),\
        at.Monitor('BPMZ6K1RP'),\
        at.Dipole('BM2K1RP',dipole_length, bending_angle,EntranceAngle=entrance_angle, ExitAngle=exit_angle,FullGap=0.025*2,FringeInt1=0.5,FringeInt2=0.5),\
        at.Drift('D3',0.425),\
        at.Sextupole('S2M2K1RP',0.1,h=VS2,Corrector='V',KickAngle=[0,0]),\
        at.Monitor('BPMZ7K1RP'),\
        at.Drift('D4',0.3),\
        at.Sextupole('S1M2K1RP',0.1,h=VS1,Corrector='H',KickAngle=[0,0]),\
        at.Drift('D1',0.15),\
        at.Quadrupole('Q1M2K1RP',0.2,k=VQ1_SEP),\
        at.Drift('D2',0.125),\
        at.Octupole('OMK1RP', 0.1, [0,0,0,0], [0,0,0,VO1]),\
        at.Drift('D2',0.125),\
        ]
        
    L2 = [\
        at.Monitor('BPMZ1L2RP'),\
        at.Quadrupole('Q1M1L2RP',0.2,k=VQ1),\
        at.Drift('D1',0.15),\
        at.Sextupole('S1M1L2RP',0.1,h=VS1,Skew='CQ'),\
        at.Drift('D4',0.3),\
        at.Sextupole('S2M1L2RP',0.1,h=VS2,Corrector='V',KickAngle=[0,0]),\
        at.Monitor('BPMZ2L2RP'),\
        at.Drift('D3',0.425),\
        at.Dipole('BM1L2RP',dipole_length, bending_angle,EntranceAngle=entrance_angle, ExitAngle=exit_angle,FullGap=0.025*2,FringeInt1=0.5,FringeInt2=0.5),\
        at.Drift('D3',0.425),\
        at.Quadrupole('Q2M1L2RP',0.2,k=VQ2L),\
        at.Monitor('BPMZ3L2RP'),\
        at.Drift('D1',0.15),\
        at.Quadrupole('Q3M1L2RP',0.2,k=VQ3L),\
        at.Drift('D1',0.15),\
        at.Sextupole('S3M1L2RP',0.1,h=VS3,Corrector='HV',KickAngle=[0,0]),\
        at.Monitor('BPMZ4L2RP'),\
        at.Drift('DL',3.0),\
        at.Marker('UND_MARKER'),\
        at.Drift('DL',3.0),\
        at.Sextupole('S3M2L2RP',0.1,h=VS3,Corrector='HV',KickAngle=[0,0]),\
        at.Monitor('BPMZ5L2RP'),\
        at.Drift('D1',0.15),\
        at.Quadrupole('Q3M2L2RP',0.2,k=VQ3L),\
        at.Drift('D1',0.15),\
        at.Quadrupole('Q2M2L2RP',0.2,k=VQ2L),\
        at.Monitor('BPMZ6L2RP'),\
        at.Drift('D3',0.425),\
        at.Dipole('BM2L2RP',dipole_length, bending_angle,EntranceAngle=entrance_angle, ExitAngle=exit_angle,FullGap=0.025*2,FringeInt1=0.5,FringeInt2=0.5),\
        at.Drift('D3',0.425),\
        at.Monitor('BPMZ7L2RP'),\
        at.Sextupole('S2M2L2RP',0.1,h=VS2,Corrector='V',KickAngle=[0,0]),\
        at.Drift('D4',0.3),\
        at.Sextupole('S1M2L2RP',0.1,h=VS1,Skew='CQ'),\
        at.Drift('D1',0.15),\
        at.Quadrupole('Q1M2L2RP',0.2,k=VQ1),\
        at.Drift('D2',0.125),\
        at.Octupole('OML2RP', 0.1, [0,0,0,0], [0,0,0,VO1]),\
        ]    
  
    K3 = [\
        at.Drift('D2',0.125),\
        at.Monitor('BPMZ1K3RP'),\
        at.Quadrupole('Q1M1K3RP',0.2,k=VQ1),\
        at.Drift('D1',0.15),\
        at.Sextupole('S1M1K3RP',0.1,h=VS1,Corrector='H',KickAngle=[0,0]),\
        at.Drift('D4',0.3),\
        at.Sextupole('S2M1K3RP',0.1,h=VS2,Corrector='V',KickAngle=[0,0]),\
        at.Monitor('BPMZ2K3RP'),\
        at.Drift('D3',0.425),\
        at.Dipole('BM1K3RP',dipole_length, bending_angle,EntranceAngle=entrance_angle, ExitAngle=exit_angle,FullGap=0.025*2,FringeInt1=0.5,FringeInt2=0.5),\
        at.Drift('D3',0.425),\
        at.Quadrupole('Q2M1K3RP',0.2,k=VQ2K),\
        at.Monitor('BPMZ3K3RP'),\
        at.Drift('D1',0.15),\
        at.Quadrupole('Q3M1K3RP',0.2,k=VQ3K),\
        at.Drift('D1',0.15),\
        at.Sextupole('S3M1K3RP',0.1,h=VS3,Corrector='HV',KickAngle=[0,0]),\
        at.Monitor('BPMZ4K3RP'),\
        at.Drift('DK',1.25),\
        at.Drift('DK',1.25),\
        at.Sextupole('S3M2K3RP',0.1,h=VS3,Corrector='HV',KickAngle=[0,0]),\
        at.Drift('D1',0.15),\
        at.Monitor('BPMZ5K3RP'),\
        at.Quadrupole('Q3M2K3RP',0.2,k=VQ3K),\
        at.Drift('D1',0.15),\
        at.Monitor('BPMZ6K3RP'),\
        at.Quadrupole('Q2M2K3RP',0.2,k=VQ2K),\
        at.Drift('D3',0.425),\
        at.Dipole('BM2K3RP',dipole_length, bending_angle,EntranceAngle=entrance_angle, ExitAngle=exit_angle,FullGap=0.025*2,FringeInt1=0.5,FringeInt2=0.5),\
        at.Drift('D3',0.425),\
        at.Sextupole('S2M2K3RP',0.1,h=VS2,Corrector='V',KickAngle=[0,0]),\
        at.Monitor('BPMZ7K3RP'),\
        at.Drift('D4',0.3),\
        at.Sextupole('S1M2K3RP',0.1,h=VS1,Corrector='H',KickAngle=[0,0]),\
        at.Drift('D1',0.15),\
        at.Quadrupole('Q1M2K3RP',0.2,k=VQ1_SEP),\
        at.Drift('D2',0.125),\
        at.Octupole('OMK3RP', 0.1, [0,0,0,0], [0,0,0,VO1]),\
        at.Drift('D2',0.125),\
        ]  
        
    L4 = [\
        at.Monitor('BPMZ1L4RP'),\
        at.Quadrupole('Q1M1L4RP',0.2,k=VQ1),\
        at.Drift('D1',0.15),\
        at.Sextupole('S1M1L4RP',0.1,h=VS1,Skew='CQ'),\
        at.Drift('D4',0.3),\
        at.Sextupole('S2M1L4RP',0.1,h=VS2,Corrector='V',KickAngle=[0,0]),\
        at.Monitor('BPMZ2L4RP'),\
        at.Drift('D3',0.425),\
        at.Dipole('BM1L4RP',dipole_length, bending_angle,EntranceAngle=entrance_angle, ExitAngle=exit_angle,FullGap=0.025*2,FringeInt1=0.5,FringeInt2=0.5),\
        at.Drift('D3',0.425),\
        at.Quadrupole('Q2M1L4RP',0.2,k=VQ2L),\
        at.Drift('D1',0.15),\
        at.Monitor('BPMZ3L4RP'),\
        at.Quadrupole('Q3M1L4RP',0.2,k=VQ3L),\
        at.Drift('D1',0.15),\
        at.Sextupole('S3M1L4RP',0.1,h=VS3,Corrector='HV',KickAngle=[0,0]),\
        at.Monitor('BPMZ4L4RP'),\
        at.Drift('DL_CAV',2.85),\
        at.RFCavity('CAV',0.15,main_cavity_voltage,rf_frequency,harmonic_number,energy),\
        at.Marker('CAV_MARKER'),\
        at.RFCavity('CAV',0.15,main_cavity_voltage,rf_frequency,harmonic_number,energy),\
        at.Drift('DL_CAV',2.85),\
        at.Monitor('BPMZ5L4RP'),\
        at.Sextupole('S3M2L4RP',0.1,h=VS3,Corrector='HV',KickAngle=[0,0]),\
        at.Drift('D1',0.15),\
        at.Quadrupole('Q3M2L4RP',0.2,k=VQ3L),\
        at.Drift('D1',0.15),\
        at.Quadrupole('Q2M2L4RP',0.2,k=VQ2L),\
        at.Monitor('BPMZ6L4RP'),\
        at.Drift('D3',0.425),\
        at.Dipole('BM2L4RP',dipole_length, bending_angle,EntranceAngle=entrance_angle, ExitAngle=exit_angle,FullGap=0.025*2,FringeInt1=0.5,FringeInt2=0.5),\
        at.Drift('D3',0.425),\
        at.Sextupole('S2M2L4RP',0.1,h=VS2,Corrector='V',KickAngle=[0,0]),\
        at.Monitor('BPMZ7L4RP'),\
        at.Drift('D4',0.3),\
        at.Sextupole('S1M2L4RP',0.1,h=VS1,Skew='CQ'),\
        at.Drift('D1',0.15),\
        at.Quadrupole('Q1M2L4RP',0.2,k=VQ1),\
        at.Drift('D2',0.125),\
        at.Octupole('OML4RP', 0.1, [0,0,0,0], [0,0,0,VO1]),\
        at.Drift('D2',0.125),\
        ]
      
    second_half_of_K1 = [\
        at.Quadrupole('Q1M1K1RP',0.2,k=VQ1),\
        at.Monitor('BPMZ1K1RP'),\
        at.Drift('D1',0.15),\
        at.Sextupole('S1M1K1RP',0.1,h=VS1,Corrector='H',KickAngle=[0,0]),\
        at.Drift('D4',0.3),\
        at.Sextupole('S2M1K1RP',0.1,h=VS2,Corrector='V',KickAngle=[0,0]),\
        at.Monitor('BPMZ2K1RP'),\
        at.Drift('D3',0.425),\
        at.Dipole('BM1K1RP',dipole_length, bending_angle,EntranceAngle=entrance_angle, ExitAngle=exit_angle,FullGap=0.025*2,FringeInt1=0.5,FringeInt2=0.5),\
        at.Drift('D3',0.425),\
        at.Quadrupole('Q2M1K1RP',0.2,k=VQ2K),\
        at.Monitor('BPMZ3K1RP'),\
        at.Drift('D1',0.15),\
        at.Quadrupole('Q3M1K1RP',0.2,k=VQ3K),\
        at.Drift('D1',0.15),\
        at.Sextupole('S3M1K1RP',0.1,h=VS3, Corrector='HV',KickAngle=[0,0]),\
        at.Monitor('BPMZ4K1RP'),\
        at.Drift('DK',1.25),\
        ]
        
    # Ring definition 
    ring=[first_half_of_K1, L2, K3, L4, second_half_of_K1]
        
    # Expand ring until list completely flattened
    while any(isinstance(x, list) for x in ring):
        ring = list(chain.from_iterable(i if isinstance(i, list) else [i] for i in ring))
          
    # Build the lattice  
    ring = at.Lattice(ring,name='mls',energy=energy,periodicity=1)
    
    # Turn cavity and radiation on
    ring.enable_6d() # Should 6D be default?
    
    # Set main cavity phases
    ring.set_cavity_phase(cavpts='CAV')
    
    return ring

if __name__ == '__main__':
    ring = mlsLattice()