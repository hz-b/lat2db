#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thurs 1 Feb 1

@author: Meghan McAteer
"""

import numpy as np
import at
from itertools import chain

def bessy2_TL() -> at.Lattice:
    
    # Global parameters
    energy = 0.629e9


    # Dipole settings and slicing
    SEK1S12B_angle = -0.194/2 * 611*2/(611+338)
    SEK2S12B_angle = -0.194/2 * 338*2/(611+338)
    B1MT_angle = 22 * np.pi/180
    B2MT_angle = 0.1352
    SEK1D1R_angle = 3.771 * np.pi/180
    SEK2D1R_angle = 3.825 * np.pi/180
    KIK3D1R_angle = -0.01
    KIK4D1R_angle = 0.01
    
    # bending_entrance_angle = np.pi*2/bending_number/2 
    # bending_exit_angle = np.pi*2/bending_number/2 
    #bending_fullgap=0.050
    #bending_entrance_fint=0.5
    #bending_exit_fint=0.5
    
    # quad effective lengths and strengths according to document from 2004 ('20040111_transferlineMagnetFitParameters.pdf')
    len_QL = 0.2619;
    len_QS = 0.2123;
    GperA_QL = 0.06834 / 0.2619 ;
    GperA_QS = 0.05556 / 0.2123 ;
    
    # Sextupole settings based on power supply configurations
    
              
    # Line definition
    line=[
        at.Dipole('SEK1S12B', 0.70, SEK1S12B_angle, EntranceAngle=0*SEK1S12B_angle/2, ExitAngle=0*SEK1S12B_angle/2),  # one septum is much stronger than the other
        at.Drift('DU_FOMZ1T', 0.075000),
        at.Monitor('FOMZ1T'),
        at.Drift('DU_SEK2S12B', 0.075000),
        at.Dipole('SEK2S12B', 0.70, SEK2S12B_angle, EntranceAngle=0*SEK2S12B_angle/2, ExitAngle=0*SEK2S12B_angle/2),  # one septum is much stronger than the other
        at.Drift('DU_FOMZ2T', 0.258000),
        at.Monitor('FOMZ2T'),
        at.Drift('DU_BPMZ1T', 0.065000),
        at.Monitor('BPMZ1T'),
        at.Drift('DU_H1MT', 0.965000),
        at.Corrector('H1MT', 0.1, [0, 0], rad_per_amp=-0.0006617),
        at.Corrector('V1MT', 0.1, [0, 0], rad_per_amp=0.0006617),
        at.Drift('DU_Q1MT', 0.314050),
        at.Quadrupole('Q1MT', len_QL, 0, polarity=-1, grad_per_amp=GperA_QL),
        at.Drift('DU_SLZ1T', 0.144050),
        at.Monitor('SLZ1T'),
        at.Drift('DU_Q2MT', 0.144050),
        at.Quadrupole('Q2MT', len_QL, 0, polarity=1, grad_per_amp=GperA_QL),
        at.Drift('DU_SLZ2T', 0.144050),
        at.Monitor('SLZ2T'),
        at.Drift('DU_Q3MT', 0.144050),
        at.Quadrupole('Q3MT', len_QL, 0, polarity=1, grad_per_amp=GperA_QL),
        at.Drift('DU_FOMZ3T', 0.199050),
        at.Monitor('FOMZ3T'),
        at.Drift('DU_BPMZ2T', 0.090000),
        at.Monitor('BPMZ2T'),
        at.Drift('DU_H2MT', 0.075000),
        at.Corrector('H2MT', 0.1, [0, 0], rad_per_amp=-0.0006617),
        at.Corrector('V2MT', 0.1, [0, 0], rad_per_amp=0.0006617),
        at.Drift('DU_B1M1T', 0.235000),
        at.Dipole('B1M1T', 1.778000, B1MT_angle, EntranceAngle=B1MT_angle/2, ExitAngle=B1MT_angle/2),
        at.Drift('DU_FOMZ4T', 0.288000),
        at.Monitor('FOMZ4T'),
        at.Drift('DU_BPMZ3T', 0.065000),
        at.Monitor('BPMZ3T'),
        at.Drift('DU_Q4MT', 0.141050),
        at.Quadrupole('Q4MT', len_QL, 0, polarity=1, grad_per_amp=GperA_QL),
        at.Drift('DU_H3MT', 0.043050),
        at.Corrector('H3MT', 0.1, [0, 0], rad_per_amp=-0.0006617),
        at.Corrector('V3MT', 0.1, [0, 0], rad_per_amp=0.0006617),
        at.Drift('DU_Q5MT', 0.045050),
        at.Quadrupole('Q5MT', len_QL, 0, polarity=-1, grad_per_amp=GperA_QL),
        at.Drift('DU_H4MT', 3.097050),
        at.Corrector('H4MT', 0.1, [0, 0], rad_per_amp=-0.0006617),
        at.Corrector('V4MT', 0.1, [0, 0], rad_per_amp=0.0006617),
        at.Drift('DU_H5MT', 1.601000),
        at.Corrector('H5MT', 0.1, [0, 0], rad_per_amp=-0.0006617),
        at.Corrector('V5MT', 0.1, [0, 0], rad_per_amp=0.0006617),
        at.Drift('DU_FOMZ5T', 0.171000),
        at.Monitor('FOMZ5T'),
        at.Drift('DU_BPMZ4T', 0.065000),
        at.Monitor('BPMZ4T'),
        at.Drift('DU_Q7MT', 0.129050),
        at.Quadrupole('Q7MT', len_QL, 0, polarity=-1, grad_per_amp=GperA_QL),
        at.Drift('DU_Q8MT', 0.288100),
        at.Quadrupole('Q8MT', len_QL, 0, polarity=1, grad_per_amp=GperA_QL),
        at.Drift('DU_Q9MT',  0.288100),
        at.Quadrupole('Q9MT', len_QL, 0, polarity=-1, grad_per_amp=GperA_QL),
        at.Drift('DU_H6MT',  0.585050),
        at.Corrector('H6MT', 0.1, [0, 0], rad_per_amp=-0.0006617),
        at.Corrector('V6MT', 0.1, [0, 0], rad_per_amp=0.0006617),
        at.Drift('DU_FOMZ6T', 0.220000),
        at.Monitor('FOMZ6T'),
        at.Drift('DU_BPMZ5T', 0.065000),
        at.Monitor('BPMZ5T'),
        at.Drift('DU_B1M2T', 0.224000 ),
        at.Dipole('B1M2T', 1.778000, B1MT_angle, EntranceAngle=B1MT_angle/2, ExitAngle=B1MT_angle/2),
        at.Drift('DU_Q10MT', 0.243850),
        at.Quadrupole('Q10MT', len_QS, 0, polarity=-1, grad_per_amp=GperA_QS),
        at.Drift('DU_H7MT', 0.027850),
        at.Corrector('H7MT', 0.1, [0, 0], rad_per_amp=-0.0006617),
        at.Drift('DU_Q11MT', 0.059850),
        at.Quadrupole('Q11MT', len_QS, 0, polarity=-1, grad_per_amp=GperA_QS),    
        at.Drift('DU_V7MT',  0.027850),
        at.Corrector('V7MT', 0.1, [0, 0], rad_per_amp=0.0006617),
        at.Drift('DU_Q12MT', 0.059850 ),
        at.Quadrupole('Q12MT', len_QS, 0, polarity=1, grad_per_amp=GperA_QS),
        at.Drift('DU_FOMZ7T', 0.142850 ),
        at.Monitor('FOMZ7T'),
        at.Drift('DU_B2MT', 0.167),
        at.Dipole('B2MT', 1.02, B2MT_angle, EntranceAngle=B2MT_angle/2, ExitAngle=B2MT_angle/2),
        at.Drift('DU_V8MT',  0.231000 ),
        at.Corrector('V8MT', 0.1, [0, 0], rad_per_amp=0.0006617),
        at.Drift('DU_SLZ3T', 0.169000),
        at.Monitor('SLZ3T'),
        at.Drift('DU_FOMZ8T', 0.336000),
        at.Monitor('FOMZ8T'),
        at.Drift('DU_SEK1D1R' , 0.2554),
        at.Dipole('SEK1D1R', 0.555, SEK1D1R_angle, EntranceAngle=0*SEK1D1R_angle, ExitAngle=0),  # edge angles need to be confirmed
        at.Drift('DU_SEK2D2R', 0.093),
        at.Dipole('SEK2D2R', 0.555, SEK2D1R_angle, EntranceAngle=0*SEK2D1R_angle, ExitAngle=0),  # edge angles need to be confirmed
        at.Drift('DU_FOMZ2D1R', 0.0515),
        at.Monitor('FOMZ2D1R'),
        at.Drift('DU_KIK3D1R', 0.2635),
        at.Dipole('KIK3D1R', 0.595, KIK3D1R_angle),
        at.Drift('DU_KIK4D1R', 0.4560),
        at.Dipole('KIK4D1R', 0.595, KIK4D1R_angle)
        ]


        
    # Expand line until list completely flattened
    while any(isinstance(x, list) for x in line):
        line = list(chain.from_iterable(i if isinstance(i, list) else [i] for i in line))

    # Build the lattice  
    line = at.Lattice(line,name='bessy2_TL',energy=energy)
    
     
    return line

if __name__ == '__main__':
    line = bessy2_TL()    