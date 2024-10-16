# 10.01.2024 Teresia Olsson, Markus Ries... translation of present BESSY II reference lattice to pyat (&review & refactor)

import numpy as np
import at
from itertools import chain

def bessy2Lattice() -> at.Lattice:
    
    # Global ring parameters
    harmonic_number = 400
    energy = 1.7e9
    
    # Dipole settings and slicing
    bending_number = 32
    bending_length = 0.855
    bending_angle = np.pi*2/bending_number
    bending_entrance_angle = np.pi*2/bending_number/2
    bending_exit_angle = np.pi*2/bending_number/2
    bending_fullgap=0.050
    bending_entrance_fint=0.5
    bending_exit_fint=0.5
    
    # Quadrupole settings based on power supply configurations
    # 16
    # Q1M1D1R,Q1M2D1R,Q1M1D2R,Q1M2D2R,Q1M1D3R,Q1M2D3R,Q1M1D4R,Q1M2D4R,Q1M1D5R,Q1M2D5R,Q1M1D6R,Q1M2D6R,Q1M1D7R,Q1M2D7R,Q1M1D8R,Q1M2D8R
    k1d=2.436378510478
    #----------------------------------------
    #----------------------------------------
    # 16
    # Q1M1T1R,Q1M2T1R,Q1M1T2R,Q1M2T2R,Q1M1T3R,Q1M2T3R,Q1M1T4R,Q1M2T4R,Q1M1T5R,Q1M2T5R,Q1M1T6R,Q1M2T6R,Q1M1T7R,Q1M2T7R,Q1M1T8R,Q1M2T8R
    k1t=2.442744469284
    #----------------------------------------
    #----------------------------------------
    # 16
    # Q2M1D1R,Q2M2D1R,Q2M1D2R,Q2M2D2R,Q2M1D3R,Q2M2D3R,Q2M1D4R,Q2M2D4R,Q2M1D5R,Q2M2D5R,Q2M1D6R,Q2M2D6R,Q2M1D7R,Q2M2D7R,Q2M1D8R,Q2M2D8R
    k2d=-1.857400277420
    #----------------------------------------
    #----------------------------------------
    # 16
    # Q2M1T1R,Q2M2T1R,Q2M1T2R,Q2M2T2R,Q2M1T3R,Q2M2T3R,Q2M1T4R,Q2M2T4R,Q2M1T5R,Q2M2T5R,Q2M1T6R,Q2M2T6R,Q2M1T7R,Q2M2T7R,Q2M1T8R,Q2M2T8R
    k2t=-1.846186515892
    #---------------------------------------- 
    # 16
    k3d1=-2.025921017529 # Q3M1D1R, Q3M2D1R
    k3d2=-2.137015029574 # Q3M1D2R, Q3M2D2R
    k3d3=-2.132523238456 # Q3M1D3R, Q3M2D3R
    k3d4=-2.141070794445 # Q3M1D4R, Q3M2D4R
    k3d5=-2.130174588469 # Q3M1D5R, Q3M2D5R
    k3d6=-2.115907383144 # Q3M1D6R, Q3M2D6R
    k3d7=-2.121082385515 # Q3M1D7R, Q3M2D7R
    k3d8=-2.144266518879 # Q3M1D8R, Q3M2D8R
    #----------------------------------------
    # 16
    k3m1t1=-2.533255113747 #Q3M1T1R
    k3m2t1=-2.483636760205 #Q3M2T1R
    k3t2  =-2.475849818289 #Q3M1T2R, Q3M2T2R
    k3t3  =-2.453370746751 #Q3M1T3R, Q3M2T3R
    k3t4  =-2.460216516724 #Q3M1T4R, Q3M2T4R
    k3t5  =-2.473072169965 #Q3M1T5R, Q3M2T5R
    k3m1t6=-2.699684425862 #Q3M1T6R
    k3m2t6=-2.371055789598 #Q3M2T6R
    k3t7  =-2.452848377941 #Q3M1T7R, Q3M2T8R
    k3m1t8=-2.492168566436 #Q3M1T8R
    k3m2t8=-2.537970509381 #Q3M2T8R
    #----------------------------------------
    # 16
    k4d1=1.401817365853 # Q4M1D1R, Q4M2D1R
    k4d2=1.477391095048 # Q4M1D2R, Q4M2D2R
    k4d3=1.484526951605 # Q4M1D3R, Q4M2D3R
    k4d4=1.493104680279 # Q4M1D4R, Q4M2D4R
    k4d5=1.479428032029 # Q4M1D5R, Q4M2D5R
    k4d6=1.482565198291 # Q4M1D6R, Q4M2D6R
    k4d7=1.474765465160 # Q4M1D7R, Q4M2D7R
    k4d8=1.492925021277 # Q4M1D8R, Q4M2D8R
    #----------------------------------------
    # 16
    k4m1t1=2.636552949711 #Q4M1T1R
    k4m2t1=2.567696910782 #Q4M2T1R
    k4t2  =2.581388047846 #Q4M1T2R, Q4M2T2R
    k4t3  =2.579115169770 #Q4M1T3R, Q4M2T3R
    k4t4  =2.581538714161 #Q4M1T4R, Q4M2T4R
    k4t5  =2.579130257516 #Q4M1T5R, Q4M2T5R
    k4m1t6=2.263202996600 #Q4M1T6R
    k4m2t6=2.565678466554 #Q4M2T6R
    k4t7  =2.583850522152 #Q4M1T7R, Q4M2T8R
    k4m1t8=2.565406220726 #Q4M1T8R
    k4m2t8=2.642899567170 #Q4M2T8R  
    #----------------------------------------
    # 16
    k5m1t1=-2.501994096088 #Q5M1T1R
    k5m2t1=-2.511531191164 #Q5M2T1R
    k5t2  =-2.577447573373 #Q5M1T2R, Q5M2T2R
    k5t3  =-2.613318049382 #Q5M1T3R, Q5M2T3R
    k5t4  =-2.589995337836 #Q5M1T4R, Q5M2T4R
    k5t5  =-2.576267191023 #Q5M1T5R, Q5M2T5R
    k5m1t6=-1.071032161447 #Q5M1T6R
    k5m2t6=-2.439246229761 #Q5M2T6R
    k5t7  =-2.595152788921 #Q5M1T7R, Q5M2T8R
    k5m1t8=-2.498907430301 #Q5M1T8R
    k5m2t8=-2.489743155393 #Q5M2T8R  
    #----------------------------------------
    kit6=-1.08082489 #QIT6
    #----------------------------------------
    
    # Sextupole settings based on power supply configurations
    # Values according to Elegant values from elog 2060
    #----------------------------------------
    #16
    #S1MD1R,S1MT1R,S1MD2R,S1MT2R,S1MD3R,S1MT3R,S1MD4R,S1MT4R,S1MD5R,S1MT5R,S1MD6R,S1MT6R,S1MD7R,S1MT7R,S1MD8R,S1MT8R
    h1=53.71159807/2
    #----------------------------------------
    #16
    #S2M1D1R,S2M2D1R,S2M1D2R,S2M2D2R,S2M1D3R,S2M2D3R,S2M1D4R,S2M2D4R,S2M1D5R,S2M2D5R,S2M1D6R,S2M2D6R,S2M1D7R,S2M2D7R,S2M1D8R,S2M2D8R
    h2d=-44.96887307/2
    #16
    #S2M1T1R,S2M2T1R,S2M1T2R,S2M2T2R,S2M1T3R,S2M2T3R,S2M1T4R,S2M2T4R,S2M1T5R,S2M2T5R,S2M1T6R,S2M2T6R,S2M1T7R,S2M2T7R,S2M1T8R,S2M2T8R
    h2t=-44.96887307/2
    #----------------------------------------
    #14
    #S3M1D2R,S3M2D2R,S3M1D3R,S3M2D3R,S3M1D4R,S3M2D4R,S3M1D5R,S3M2D5R,S3M1D6R,S3M2D6R,S3M1D7R,S3M2D7R,S3M1D8R,S3M2D8R
    h3d=-47.03/2
    h3d1=-42.37/2 #S3M1D1R, S3M2D1R
    #14
    #S3M1T1R,S3M2T1R,S3M1T2R,S3M2T2R,S3M1T3R,S3M2T3R,S3M1T4R,S3M2T4R,S3M1T5R,S3M2T5R,S3M1T7R,S3M2T7R,S3M1T8R,S3M2T8R
    h3t=-52.22/2
    h3m1t6=-40.78/2 #S3M1T6R
    h3m2t6=-40.25/2 #S3M2T6R
    #----------------------------------------
    #14
    #S4M1D2R,S4M2D2R,S4M1D3R,S4M2D3R,S4M1D4R,S4M2D4R,S4M1D5R,S4M2D5R,S4M1D6R,S4M2D6R,S4M1D7R,S4M2D7R,S4M1D8R,S4M2D8R
    h4d=42.31/2
    h4d1=33.36/2 #S4M1D1R, S4M2D1R
    #14
    #S4M1T1R,S4M2T1R,S4M1T2R,S4M2T2R,S4M1T3R,S4M2T3R,S4M1T4R,S4M2T4R,S4M1T5R,S4M2T5R,S4M1T7R,S4M2T7R,S4M1T8R,S4M2T8R
    h4t=64.87/2
    h4m1t6=33.89/2 #S4M1T6R
    h4m2t6=41.84/2 #S4M2T6R
    #----------------------------------------
    
    # Cavity settings
    rf_frequency = 499636630.20280415
    main_cavity_voltage = 350e3
    
    # Ring starts with second half of D1
    D1_secondhalf = [\
        at.Marker('MRING_START'),\
        at.Drift('DU_MSEPEXIT',0.56),\
        at.Marker('MSEPEXIT'),\
        at.Drift('DU_FOMZ2D1R',0.0555),\
        at.Marker('FOMZ2D1R'),\
        at.Drift('DU_KIK3D1R',0.245),\
        at.Drift('KIK3D1R',0.595),\
        at.Drift('DU_KIK4D1R',0.456),\
        at.Drift('KIK4D1R',0.595),\
        at.Drift('DU_BPMZ5D1R',0.2495),\
        at.Monitor('BPMZ5D1R',Group='BPM'),\
        at.Drift('DU_S4M2D1R',0.05),\
        at.Sextupole('S4M2D1R',0.16,h=h4d1,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_Q4M2D1R',0.153),\
        at.Quadrupole('Q4M2D1R',0.5,k=k4d1),\
        at.Drift('DU_S3M2D1R',0.153),\
        at.Sextupole('S3M2D1R',0.16,h=h3d1,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ6D1R',0.063),\
        at.Monitor('BPMZ6D1R',Group='BPM'),\
        at.Drift('DU_Q3M2D1R',0.09),\
        at.Quadrupole('Q3M2D1R',0.25,k=k3d1),\
        at.Drift('DU_BM2D1R',0.42),\
        at.Dipole('BM2D1R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB2D1R',0.26),\
        at.Monitor('DBLMB2D1R',Group='BLM'),\
        at.Drift('DU_Q2M2D1R',0.16),\
        at.Quadrupole('Q2M2D1R',0.2,k=k2d),\
        at.Drift('DU_BPMZ7D1R',0.244),\
        at.Monitor('BPMZ7D1R',Group='BPM'),\
        at.Drift('DU_S2M2D1R',0.063),\
        at.Sextupole('S2M2D1R',0.16,h=h2d,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_Q1M2D1R',0.288),\
        at.Quadrupole('Q1M2D1R',0.25,k=k1d),\
        at.Drift('DU_DBMLD1T1R0',0.105),\
        at.Monitor('DBMLD1T1R0',Group='BLM'),\
        at.Monitor('DBMLD1T1R',Group='BLM'),\
        at.Drift('DU_S1MT1R',0.055),\
        at.Marker('MSEC_D1_END'),\
    ]

    T1 = [\
        at.Marker('MSEC_T1_START'),\
        at.Sextupole('S1MT1R',0.21,h=h1,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ1T1R', 0.07),\
        at.Monitor('BPMZ1T1R',Group='BPM'),\
        at.Drift('DU_Q1M1T1R', 0.09),\
        at.Quadrupole('Q1M1T1R',0.25,k=k1t),\
        at.Drift('DU_S2M1T1R', 0.288),\
        at.Sextupole('S2M1T1R',0.16,h=h2t,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ2T1R', 0.128),\
        at.Monitor('BPMZ2T1R',Group='BPM'),\
        at.Drift('DU_Q2M1T1R', 0.179),\
        at.Quadrupole('Q2M1T1R',0.2,k=k2t),\
        at.Drift('DU_BM1T1R', 0.42),\
        at.Dipole('BM1T1R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB1T1R', 0.275),\
        at.Monitor('DBLMB1T1R',Group='BLM'),\
        at.Drift('DU_Q3M1T1R', 0.145),\
        at.Quadrupole('Q3M1T1R',0.25,k=k3m1t1),\
        at.Drift('DU_BPMZ3T1R', 0.09),\
        at.Monitor('BPMZ3T1R',Group='BPM'),\
        at.Drift('DU_S3M1T1R', 0.063),\
        at.Sextupole('S3M1T1R',0.16,h=h3t,Corrector='V',Skew='CQ',KickAngle=[0,0]),\
        at.Drift('DU_Q4M1T1R', 0.153),\
        at.Quadrupole('Q4M1T1R',0.5,k=k4m1t1),\
        at.Drift('DU_S4M1T1R', 0.153),\
        at.Sextupole('S4M1T1R',0.16,h=h4t,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_Q5M1T1R', 0.153),\
        at.Quadrupole('Q5M1T1R',0.2,k=k5m1t1),\
        at.Drift('DU_BPMZ4T1R', 0.092),\
        at.Monitor('BPMZ4T1R',Group='BPM'),\
        at.Drift('DU_LC1HT1R', 0.308),\
        at.RFCavity('LC1HT1R',0.084,0,rf_frequency*3,harmonic_number*3,energy,Group='CAV1500'),\
        at.Drift('DU_LC2HT1R', 0.116),\
        at.RFCavity('LC2HT1R',0.084,0,rf_frequency*3,harmonic_number*3,energy,Group='CAV1500'),\
        at.Drift('DU_LC3HT1R', 0.116),\
        at.RFCavity('LC3HT1R',0.084,0,rf_frequency*3,harmonic_number*3,energy,Group='CAV1500'),\
        at.Drift('DU_LC4HT1R', 0.116),\
        at.RFCavity('LC4HT1R',0.084,0,rf_frequency*3,harmonic_number*3,energy,Group='CAV1500'),\
        at.Drift('DU_MSEC2', 1.369),\
        at.Marker('MSEC2'),\
        at.Marker('MBAMWLS1'),\
        at.Drift('DU_BPMZ43T1R', 0.93),\
        at.Monitor('BPMZ43T1R',Group='BPM'),\
        at.Drift('DU_BPMZ5T1R', 1.431),\
        at.Monitor('BPMZ5T1R',Group='BPM'),\
        at.Drift('DU_Q5M2T1R', 0.092),\
        at.Quadrupole('Q5M2T1R',0.2,k=k5m2t1),\
        at.Drift('DU_S4M2T1R', 0.153),\
        at.Sextupole('S4M2T1R',0.16,h=h4t,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_Q4M2T1R', 0.153),\
        at.Quadrupole('Q4M2T1R',0.5,k=k4m2t1),\
        at.Drift('DU_S3M2T1R', 0.153),\
        at.Sextupole('S3M2T1R',0.16,h=h3t,Corrector='V',Skew='CQ',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ6T1R', 0.063),\
        at.Monitor('BPMZ6T1R',Group='BPM'),\
        at.Drift('DU_Q3M2T1R', 0.09),\
        at.Quadrupole('Q3M2T1R',0.25,k=k3m2t1),\
        at.Drift('DU_BM2T1R', 0.42),\
        at.Dipole('BM2T1R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB2T1R', 0.26),\
        at.Monitor('DBLMB2T1R',Group='BLM'),\
        at.Drift('DU_Q2M2T1R', 0.16),\
        at.Quadrupole('Q2M2T1R',0.2,k=k2t),\
        at.Drift('DU_BPMZ7T1R', 0.244),\
        at.Monitor('BPMZ7T1R',Group='BPM'),\
        at.Drift('DU_S2M2T1R',0.063),\
        at.Sextupole('S2M2T1R',0.16,h=h2t,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_Q1M2T1R', 0.288),\
        at.Quadrupole('Q1M2T1R',0.25,k=k1t),\
        at.Drift('DU_DBMLT1D2R0',0.085),\
        at.Monitor('DBMLT1D2R0',Group='BLM'),\
        at.Monitor('DBMLT1D2R',Group='BLM'),\
        at.Drift('DU_S1MD2R',0.075),\
        at.Marker('MSEC_T1_END'),\
        ]         
                   
    D2 = [\
        at.Marker('MSEC_D2_START'),\
        at.Sextupole('S1MD2R',0.21,h=h1,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ1D2R',0.07),\
        at.Monitor('BPMZ1D2R',Group='BPM'),\
        at.Drift('DU_Q1M1D2R',0.09),\
        at.Quadrupole('Q1M1D2R',0.25,k=k1d),\
        at.Drift('DU_DBLMB1D2R',0.128),\
        at.Monitor('DBLMB1D2R',Group='BLM'),
        at.Drift('DU_S2M1D2R',0.160),\
        at.Sextupole('S2M1D2R',0.16,h=h2d,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ2D2R',0.128),\
        at.Monitor('BPMZ2D2R',Group='BPM'),\
        at.Drift('DU_Q2M1D2R',0.179),\
        at.Quadrupole('Q2M1D2R',0.2,k=k2d),\
        at.Drift('DU_BM1D2R',0.42),\
        at.Dipole('BM1D2R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_Q3M1D2R',0.42),\
        at.Quadrupole('Q3M1D2R',0.25,k=k3d2),\
        at.Drift('DU_BPMZ3D2R',0.09),\
        at.Monitor('BPMZ3D2R',Group='BPM'),\
        at.Drift('DU_S3M1D2R',0.063),\
        at.Sextupole('S3M1D2R',0.16,h=h3d,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_Q4M1D2R',0.153),\
        at.Quadrupole('Q4M1D2R',0.5,k=k4d2),\
        at.Drift('DU_S4M1D2R',0.153),
        at.Sextupole('S4M1D2R',0.16,h=h4d,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ4D2R',0.07),
        at.Monitor('BPMZ4D2R',Group='BPM'),\
        at.Drift('DU_KDNL1KR',0.194),\
        at.Drift('KDNL1KR',0.3),\
        at.Drift('DU_FOMZ1D2R',4.634),\
        at.Monitor('FOMZ1D2R'),\
        at.Drift('DU_BPMZ5D2R',0.344),\
        at.Monitor('BPMZ5D2R',Group='BPM'),\
        at.Drift('DU_S4M2D2R',0.07),\
        at.Sextupole('S4M2D2R',0.16,h=h4d,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_Q4M2D2R',0.153),\
        at.Quadrupole('Q4M2D2R',0.5,k=k4d2),\
        at.Drift('DU_S3M2D2R',0.153),\
        at.Sextupole('S3M2D2R',0.16,h=h3d,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ6D2R',0.063),\
        at.Monitor('BPMZ6D2R',Group='BPM'),\
        at.Drift('DU_Q3M2D2R',0.09),\
        at.Quadrupole('Q3M2D2R',0.25,k=k3d2),\
        at.Drift('DU_BM2D2R',0.42),\
        at.Dipole('BM2D2R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB2D2R',0.26),\
        at.Monitor('DBLMB2D2R',Group='BLM'),\
        at.Drift('DU_Q2M2D2R',0.16),\
        at.Quadrupole('Q2M2D2R',0.2,k=k2d),\
        at.Drift('DU_BPMZ7D2R',0.244),\
        at.Monitor('BPMZ7D2R',Group='BPM'),\
        at.Drift('DU_S2M2D2R',0.063),\
        at.Sextupole('S2M2D2R',0.16,h=h2d,Corrector='V',Skew='CQ',KickAngle=[0,0]),\
        at.Drift('DU_Q1M2D2R',0.288),\
        at.Quadrupole('Q1M2D2R',0.25,k=k1d),\
        at.Drift('DU_DBMLD2T2R0',0.105),\
        at.Monitor('DBMLD2T2R0',Group='BLM'),\
        at.Monitor('DBMLD2T2R',Group='BLM'),\
        at.Drift('DU_S1MT2R',0.055),\
        at.Marker('MSEC_D2_END'),\
    ]  
    
    T2 = [\
        at.Marker('MSEC_T2_START'),\
        at.Sextupole('S1MT2R',0.21,h=h1,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ1T2R', 0.07),\
        at.Monitor('BPMZ1T2R',Group='BPM'),\
        at.Drift('DU_Q1M1T2R', 0.09),\
        at.Quadrupole('Q1M1T2R',0.25,k=k1t),\
        at.Drift('DU_S2M1T2R', 0.288),\
        at.Sextupole('S2M1T2R',0.16,h=h2t,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ2T2R', 0.128),\
        at.Monitor('BPMZ2T2R',Group='BPM'),\
        at.Drift('DU_Q2M1T2R', 0.179),\
        at.Quadrupole('Q2M1T2R',0.2,k=k2t),\
        at.Drift('DU_BM1T2R', 0.42),\
        at.Dipole('BM1T2R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB1T2R', 0.275),\
        at.Monitor('DBLMB1T2R',Group='BLM'),\
        at.Drift('DU_Q3M1T2R', 0.145),\
        at.Quadrupole('Q3M1T2R',0.25,k=k3t2),\
        at.Drift('DU_BPMZ3T2R', 0.09),\
        at.Monitor('BPMZ3T2R',Group='BPM'),\
        at.Drift('DU_S3M1T2R', 0.063),\
        at.Sextupole('S3M1T2R',0.16,h=h3t,Corrector='V',Skew='CQ',KickAngle=[0,0]),\
        at.Drift('DU_Q4M1T2R', 0.153),\
        at.Quadrupole('Q4M1T2R',0.5,k=k4t2),\
        at.Drift('DU_S4M1T2R', 0.153),\
        at.Sextupole('S4M1T2R',0.16,h=h4t,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_Q5M1T2R', 0.153),\
        at.Quadrupole('Q5M1T2R',0.2,k=k5t2),\
        at.Drift('DU_BPMZ4T2R', 0.092),\
        at.Monitor('BPMZ4T2R',Group='BPM'),\
        at.Drift('DU_HC1H1T2R',0.366),\
        at.Marker('HC1H1T2R',Group='HC_AC_1500'),\
        at.Drift('DU_HC1H2T2R',0.3),\
        at.Marker('HC1H2T2R',Group='HC_AC_1500'),\
        at.Drift('DU_HC1H3T2R',0.3),\
        at.Marker('HC1H3T2R',Group='HC_AC_1500'),\
        at.Drift('DU_CPMU20_BEG',0.385),\
        at.Marker('CPMU20_BEG'),\
        at.Drift('DU_CPMU20_MID',1.010),\
        at.Marker('CPMU20_MID'),\
        at.Drift('DU_CPMU20_END',1.010),\
        at.Marker('CPMU20_END'),\
        at.Drift('DU_HC2H1T2R',0.385),\
        at.Marker('HC2H1T2R',Group='HC_AC_1750'),\
        at.Drift('DU_HC2H2T2R',0.3),\
        at.Marker('HC2H2T2R',Group='HC_AC_1750'),\
        at.Drift('DU_HC2H3T2R',0.3),\
        at.Marker('HC2H3T2R',Group='HC_AC_1750'),\
        at.Drift('DU_BPMZ5T2R', 0.366),\
        at.Monitor('BPMZ5T2R',Group='BPM'),\
        at.Drift('DU_Q5M2T2R', 0.092),\
        at.Quadrupole('Q5M2T2R',0.2,k=k5t2),\
        at.Drift('DU_S4M2T2R', 0.153),\
        at.Sextupole('S4M2T2R',0.16,h=h4t,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_Q4M2T2R', 0.153),\
        at.Quadrupole('Q4M2T2R',0.5,k=k4t2),\
        at.Drift('DU_S3M2T2R', 0.153),\
        at.Sextupole('S3M2T2R',0.16,h=h3t,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ6T2R', 0.063),\
        at.Monitor('BPMZ6T2R',Group='BPM'),\
        at.Drift('DU_Q3M2T2R', 0.09),\
        at.Quadrupole('Q3M2T2R',0.25,k=k3t2),\
        at.Drift('DU_BM2T2R', 0.42),\
        at.Dipole('BM2T2R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB2T2R', 0.30),\
        at.Monitor('DBLMB2T2R',Group='BLM'),\
        at.Drift('DU_Q2M2T2R', 0.120),\
        at.Quadrupole('Q2M2T2R',0.2,k=k2t),\
        at.Drift('DU_BPMZ7T2R', 0.244),\
        at.Monitor('BPMZ7T2R',Group='BPM'),\
        at.Drift('DU_S2M2T2R',0.063),\
        at.Sextupole('S2M2T2R',0.16,h=h2t,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_Q1M2T2R', 0.288),\
        at.Quadrupole('Q1M2T2R',0.25,k=k1t),\
        at.Drift('DU_DBMLT2D3R0',0.105),\
        at.Monitor('DBMLT2D3R0',Group='BLM'),\
        at.Monitor('DBMLT2D3R',Group='BLM'),\
        at.Drift('DU_S1MD3R',0.055),\
        at.Marker('MSEC_T2_END'),\
        ] 
        
    D3 = [\
        at.Marker('MSEC_D3_START'),\
        at.Sextupole('S1MD3R',0.21,h=h1,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ1D3R',0.07),\
        at.Monitor('BPMZ1D3R',Group='BPM'),\
        at.Drift('DU_Q1M1D3R',0.09),\
        at.Quadrupole('Q1M1D3R',0.25,k=k1d),\
        at.Drift('DU_ED3Vo',0.118),\
        at.Monitor('ED3Vo',Group='BLM'),
        at.Monitor('ED3Vu',Group='BLM'),        
        at.Drift('DU_S2M1D3R',0.170),\
        at.Sextupole('S2M1D3R',0.16,h=h2d,Corrector='V',Skew='CQ',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ2D3R',0.128),\
        at.Monitor('BPMZ2D3R',Group='BPM'),\
        at.Drift('DU_Q2M1D3R',0.179),\
        at.Quadrupole('Q2M1D3R',0.2,k=k2d),\
        at.Drift('DU_BM1D3R',0.42),\
        at.Dipole('BM1D3R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB1D3R',0.265),\
        at.Monitor('DBLMB1D3R',Group='BLM'),
        at.Drift('DU_Q3M1D3R',0.155),\
        at.Quadrupole('Q3M1D3R',0.25,k=k3d3),\
        at.Drift('DU_BPMZ3D3R',0.09),\
        at.Monitor('BPMZ3D3R',Group='BPM'),\
        at.Drift('DU_S3M1D3R',0.063),\
        at.Sextupole('S3M1D3R',0.16,h=h3d,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_Q4M1D3R',0.153),\
        at.Quadrupole('Q4M1D3R',0.5,k=k4d3),\
        at.Drift('DU_S4M1D3R',0.153),
        at.Sextupole('S4M1D3R',0.16,h=h4d,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ4D3R',0.07),
        at.Monitor('BPMZ4D3R',Group='BPM'),\
        at.Drift('DU_FOMZ1D3R',0.343),\
        at.Monitor('FOMZ1D3R'),\
        at.Drift('DU_BPMZ5D3R',5.129),\
        at.Monitor('BPMZ5D3R',Group='BPM'),\
        at.Drift('DU_S4M2D3R',0.07),\
        at.Sextupole('S4M2D3R',0.16,h=h4d,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_Q4M2D3R',0.153),\
        at.Quadrupole('Q4M2D3R',0.5,k=k4d3),\
        at.Drift('DU_S3M2D3R',0.153),\
        at.Sextupole('S3M2D3R',0.16,h=h3d,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ6D3R',0.063),\
        at.Monitor('BPMZ6D3R',Group='BPM'),\
        at.Drift('DU_Q3M2D3R',0.09),\
        at.Quadrupole('Q3M2D3R',0.25,k=k3d3),\
        at.Drift('DU_BM2D3R',0.42),\
        at.Dipole('BM2D3R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB2D3R',0.26),\
        at.Monitor('DBLMB2D3R',Group='BLM'),\
        at.Drift('DU_Q2M2D3R',0.16),\
        at.Quadrupole('Q2M2D3R',0.2,k=k2d),\
        at.Drift('DU_BPMZ7D3R',0.244),\
        at.Monitor('BPMZ7D3R',Group='BPM'),\
        at.Drift('DU_S2M2D3R',0.063),\
        at.Sextupole('S2M2D3R',0.16,h=h2d,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_Q1M2D3R',0.288),\
        at.Quadrupole('Q1M2D3R',0.25,k=k1d),\
        at.Drift('DU_BLMU_S1MT3R0',0.105),\
        at.Monitor('DBMLD3T3R0',Group='BLM'),\
        at.Monitor('DBMLD3T3R',Group='BLM'),\
        at.Drift('DU_S1MT3R',0.055),\
        at.Marker('MSEC_D3_END'),\
    ] 
        
    T3 = [\
        at.Marker('MSEC_T3_START'),\
        at.Sextupole('S1MT3R',0.21,h=h1,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ1T3R', 0.07),\
        at.Monitor('BPMZ1T3R',Group='BPM'),\
        at.Drift('DU_Q1M1T3R', 0.09),\
        at.Quadrupole('Q1M1T3R',0.25,k=k1t),\
        at.Drift('DU_S2M1T3R', 0.288),\
        at.Sextupole('S2M1T3R',0.16,h=h2t,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ2T3R',0.128),\
        at.Monitor('BPMZ2T3R',Group='BPM'),\
        at.Drift('DU_Q2M1T3R',0.179),\
        at.Quadrupole('Q2M1T3R',0.2,k=k2t),\
        at.Drift('DU_BM1T3R', 0.42),\
        at.Dipole('BM1T3R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB1T3R', 0.265),\
        at.Monitor('DBLMB1T3R',Group='BLM'),\
        at.Drift('DU_Q3M1T3R', 0.155),\
        at.Quadrupole('Q3M1T3R',0.25,k=k3t3),\
        at.Drift('DU_BPMZ3T3R', 0.09),\
        at.Monitor('BPMZ3T3R',Group='BPM'),\
        at.Drift('DU_S3M1T3R', 0.063),\
        at.Sextupole('S3M1T3R',0.16,h=h3t,Corrector='V',Skew='CQ',KickAngle=[0,0]),\
        at.Drift('DU_Q4M1T3R', 0.153),\
        at.Quadrupole('Q4M1T3R',0.5,k=k4t3),\
        at.Drift('DU_S4M1T3R', 0.153),\
        at.Sextupole('S4M1T3R',0.16,h=h4t,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_Q5M1T3R', 0.153),\
        at.Quadrupole('Q5M1T3R',0.2,k=k5t3),\
        at.Drift('DU_BPMZ4T3R', 0.092),\
        at.Monitor('BPMZ4T3R',Group='BPM'),\
        at.Drift('DU_MWLS',2.361),\
        at.Marker('MWLS'),\
        at.Marker('MSEC6'),\
        at.Drift('DU_BPMZ5T3R', 2.361),\
        at.Monitor('BPMZ5T3R',Group='BPM'),\
        at.Drift('DU_Q5M2T3R', 0.092),\
        at.Quadrupole('Q5M2T3R',0.2,k=k5t3),\
        at.Drift('DU_S4M2T3R', 0.153),\
        at.Sextupole('S4M2T3R',0.16,h=h4t,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_Q4M2T3R', 0.153),\
        at.Quadrupole('Q4M2T3R',0.5,k=k4t3),\
        at.Drift('DU_S3M2T3R', 0.153),\
        at.Sextupole('S3M2T3R',0.16,h=h3t,Corrector='V',Skew='CQ',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ6T3R', 0.063),\
        at.Monitor('BPMZ6T3R',Group='BPM'),\
        at.Drift('DU_Q3M2T3R', 0.09),\
        at.Quadrupole('Q3M2T3R',0.25,k=k3t3),\
        at.Drift('DU_BM2T3R', 0.42),\
        at.Dipole('BM2T3R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB2T3R', 0.26),\
        at.Monitor('DBLMB2T3R',Group='BLM'),\
        at.Drift('DU_Q2M2T3R', 0.16),\
        at.Quadrupole('Q2M2T3R',0.2,k=k2t),\
        at.Drift('DU_BPMZ7T3R', 0.244),\
        at.Monitor('BPMZ7T3R',Group='BPM'),\
        at.Drift('DU_S2M2T3R',0.063),\
        at.Sextupole('S2M2T3R',0.16,h=h2t,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_Q1M2T3R', 0.288),\
        at.Quadrupole('Q1M2T3R',0.25,k=k1t),\
        at.Drift('DU_DBMLT3D4R0',0.095),\
        at.Monitor('DBMLT3D4R0',Group='BLM'),\
        at.Monitor('DBMLT3D4R',Group='BLM'),\
        at.Drift('DU_S1MD4R',0.065),\
        at.Marker('MSEC_T3_END'),\
        ]         
               
    D4 = [\
        at.Marker('MSEC_D4_START'),\
        at.Sextupole('S1MD4R',0.21,h=h1,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ1D4R',0.07),\
        at.Monitor('BPMZ1D4R',Group='BPM'),\
        at.Drift('DU_Q1M1D4R',0.09),\
        at.Quadrupole('Q1M1D4R',0.25,k=k1d),\
        at.Drift('DU_S2M1D4R',0.288),\
        at.Sextupole('S2M1D4R',0.16,h=h2d,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ2D4R',0.128),\
        at.Monitor('BPMZ2D4R',Group='BPM'),\
        at.Drift('DU_Q2M1D4R',0.179),\
        at.Quadrupole('Q2M1D4R',0.2,k=k2d),\
        at.Drift('DU_BM1D4R',0.42),\
        at.Dipole('BM1D4R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB1D4R',0.265),\
        at.Monitor('DBLMB1D4R',Group='BLM'),
        at.Drift('DU_Q3M1D4R',0.155),\
        at.Quadrupole('Q3M1D4R',0.25,k=k3d4),\
        at.Drift('DU_BPMZ3D4R',0.09),\
        at.Monitor('BPMZ3D4R',Group='BPM'),\
        at.Drift('DU_S3M1D4R',0.063),\
        at.Sextupole('S3M1D4R',0.16,h=h3d,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_Q4M1D4R',0.153),\
        at.Quadrupole('Q4M1D4R',0.5,k=k4d4),\
        at.Drift('DU_S4M1D4R',0.153),
        at.Sextupole('S4M1D4R',0.16,h=h4d,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ4D4R',0.07),
        at.Monitor('BPMZ4D4R',Group='BPM'),\
        at.Drift('DU_ED4Vu',0.44),\
        at.Monitor('ED4Vu',Group='BLM'),\
        at.Drift('DU_MSEC7',2.296),\
        at.Marker('MSEC7'),\
        at.Marker('MU49_2'),\
        at.Drift('DU_BPMZ5D4R',2.736),\
        at.Monitor('BPMZ5D4R',Group='BPM'),\
        at.Drift('DU_S4M2D4R',0.07),\
        at.Sextupole('S4M2D4R',0.16,h=h4d,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_Q4M2D4R',0.153),\
        at.Quadrupole('Q4M2D4R',0.5,k=k4d4),\
        at.Drift('DU_S3M2D4R',0.153),\
        at.Sextupole('S3M2D4R',0.16,h=h3d,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ6D4R',0.063),\
        at.Monitor('BPMZ6D4R',Group='BPM'),\
        at.Drift('DU_Q3M2D4R',0.09),\
        at.Quadrupole('Q3M2D4R',0.25,k=k3d4),\
        at.Drift('DU_BM2D4R',0.42),\
        at.Dipole('BM2D4R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB2D4R',0.26),\
        at.Monitor('DBLMB2D4R',Group='BLM'),\
        at.Drift('DU_Q2M2D4R',0.16),\
        at.Quadrupole('Q2M2D4R',0.2,k=k2d),\
        at.Drift('DU_BPMZ7D4R',0.244),\
        at.Monitor('BPMZ7D4R',Group='BPM'),\
        at.Drift('DU_S2M2D4R',0.063),\
        at.Sextupole('S2M2D4R',0.16,h=h2d,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_Q1M2D4R',0.288),\
        at.Quadrupole('Q1M2D4R',0.25,k=k1d),\
        at.Drift('DU_DBMLD4T4R0',0.095),\
        at.Monitor('DBMLD4T4R0',Group='BLM'),\
        at.Monitor('DBMLD4T4R',Group='BLM'),\
        at.Drift('DU_S1MT4R',0.065),\
        at.Marker('MSEC_D4_END'),\
    ] 
    
    T4 = [\
        at.Marker('MSEC_T4_START'),\
        at.Sextupole('S1MT4R',0.21,h=h1,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ1T4R', 0.07),\
        at.Monitor('BPMZ1T4R',Group='BPM'),\
        at.Drift('DU_Q1M1T4R', 0.09),\
        at.Quadrupole('Q1M1T4R',0.25,k=k1t),\
        at.Drift('DU_S2M1T4R', 0.288),\
        at.Sextupole('S2M1T4R',0.16,h=h2t,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ2T4R', 0.128),\
        at.Monitor('BPMZ2T4R',Group='BPM'),\
        at.Drift('DU_Q2M1T4R', 0.179),\
        at.Quadrupole('Q2M1T4R',0.2,k=k2t),\
        at.Drift('DU_BM1T4R', 0.42),\
        at.Dipole('BM1T4R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB1T4R', 0.265),\
        at.Monitor('DBLMB1T4R',Group='BLM'),\
        at.Drift('DU_Q3M1T4R', 0.155),\
        at.Quadrupole('Q3M1T4R',0.25,k=k3t4),\
        at.Drift('DU_BPMZ3T4R', 0.09),\
        at.Monitor('BPMZ3T4R',Group='BPM'),\
        at.Drift('DU_S3M1T4R', 0.063),\
        at.Sextupole('S3M1T4R',0.16,h=h3t,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_Q4M1T4R', 0.153),\
        at.Quadrupole('Q4M1T4R',0.5,k=k4t4),\
        at.Drift('DU_S4M1T4R', 0.153),\
        at.Sextupole('S4M1T4R',0.16,h=h4t,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_Q5M1T4R', 0.153),\
        at.Quadrupole('Q5M1T4R',0.2,k=k5t4),\
        at.Drift('DU_BPMZ4T4R', 0.092),\
        at.Monitor('BPMZ4T4R',Group='BPM'),\
        at.Drift('DU_UE49',2.086),\
        at.Marker('UE49'),\
        at.Marker('MSEC8'),\
        at.Marker('MUE49'),\
        at.Drift('DU_BPMZ5T4R', 2.636),\
        at.Monitor('BPMZ5T4R',Group='BPM'),\
        at.Drift('DU_Q5M2T4R', 0.092),\
        at.Quadrupole('Q5M2T4R',0.2,k=k5t4),\
        at.Drift('DU_S4M2T4R', 0.153),\
        at.Sextupole('S4M2T4R',0.16,h=h4t,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_Q4M2T4R', 0.153),\
        at.Quadrupole('Q4M2T4R',0.5,k=k4t4),\
        at.Drift('DU_S3M2T4R', 0.153),\
        at.Sextupole('S3M2T4R',0.16,h=h3t,Corrector='V',Skew='CQ',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ6T4R', 0.063),\
        at.Monitor('BPMZ6T4R',Group='BPM'),\
        at.Drift('DU_Q3M2T4R', 0.09),\
        at.Quadrupole('Q3M2T4R',0.25,k=k3t4),\
        at.Drift('DU_BM2T4R', 0.42),\
        at.Dipole('BM2T4R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB2T4R', 0.27),\
        at.Monitor('DBLMB2T4R',Group='BLM'),\
        at.Drift('DU_Q2M2T4R', 0.150),\
        at.Quadrupole('Q2M2T4R',0.2,k=k2t),\
        at.Drift('DU_BPMZ7T4R', 0.244),\
        at.Monitor('BPMZ7T4R',Group='BPM'),\
        at.Drift('DU_S2M2T4R',0.063),\
        at.Sextupole('S2M2T4R',0.16,h=h2t,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_Q1M2T4R', 0.288),\
        at.Quadrupole('Q1M2T4R',0.25,k=k1t),\
        at.Drift('DU_DBMLT4D5R0',0.105),\
        at.Monitor('DBMLT4D5R0',Group='BLM'),\
        at.Monitor('DBMLT4D5R',Group='BLM'),\
        at.Drift('DU_S1MD5R',0.055),\
        at.Marker('MSEC_T4_END'),\
        ] 
           
    D5 = [\
        at.Marker('MSEC_D5_START'),\
        at.Sextupole('S1MD5R',0.21,h=h1,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ1D5R',0.07),\
        at.Monitor('BPMZ1D5R',Group='BPM'),\
        at.Drift('DU_Q1M1D5R',0.09),\
        at.Quadrupole('Q1M1D5R',0.25,k=k1d),\
        at.Drift('DU_S2M1D5R',0.288),\
        at.Sextupole('S2M1D5R',0.16,h=h2d,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ2D5R',0.128),\
        at.Monitor('BPMZ2D5R',Group='BPM'),\
        at.Drift('DU_Q2M1D5R',0.179),\
        at.Quadrupole('Q2M1D5R',0.2,k=k2d),\
        at.Drift('DU_BM1D5R',0.42),\
        at.Dipole('BM1D5R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB1D5R',0.265),\
        at.Monitor('DBLMB1D5R',Group='BLM'),
        at.Drift('DU_Q3M1D5R',0.155),\
        at.Quadrupole('Q3M1D5R',0.25,k=k3d5),\
        at.Drift('DU_BPMZ3D5R',0.09),\
        at.Monitor('BPMZ3D5R',Group='BPM'),\
        at.Drift('DU_S3M1D5R',0.063),\
        at.Sextupole('S3M1D5R',0.16,h=h3d,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_Q4M1D5R',0.153),\
        at.Quadrupole('Q4M1D5R',0.5,k=k4d5),\
        at.Drift('DU_S4M1D5R',0.153),
        at.Sextupole('S4M1D5R',0.16,h=h4d,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ4D5R',0.07),
        at.Monitor('BPMZ4D5R',Group='BPM'),\
        at.Drift('DU_MSEC9',2.736),\
        at.Marker('MSEC9'),\
        at.Marker('MUE52'),\
        at.Drift('DU_BPMZ5D5R',2.736),\
        at.Monitor('BPMZ5D5R',Group='BPM'),\
        at.Drift('DU_S4M2D5R',0.07),\
        at.Sextupole('S4M2D5R',0.16,h=h4d,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_Q4M2D5R',0.153),\
        at.Quadrupole('Q4M2D5R',0.5,k=k4d5),\
        at.Drift('DU_S3M2D5R',0.153),\
        at.Sextupole('S3M2D5R',0.16,h=h3d,Corrector='V',Skew='CQ',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ6D5R',0.063),\
        at.Monitor('BPMZ6D5R',Group='BPM'),\
        at.Drift('DU_Q3M2D5R',0.09),\
        at.Quadrupole('Q3M2D5R',0.25,k=k3d5),\
        at.Drift('DU_BM2D5R',0.42),\
        at.Dipole('BM2D5R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB2D5R',0.26),\
        at.Monitor('DBLMB2D5R',Group='BLM'),\
        at.Drift('DU_Q2M2D5R',0.16),\
        at.Quadrupole('Q2M2D5R',0.2,k=k2d),\
        at.Drift('DU_BPMZ7D5R',0.244),\
        at.Monitor('BPMZ7D5R',Group='BPM'),\
        at.Drift('DU_S2M2D5R',0.063),\
        at.Sextupole('S2M2D5R',0.16,h=h2d,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_Q1M2D5R',0.288),\
        at.Quadrupole('Q1M2D5R',0.25,k=k1d),\
        at.Drift('DU_MARKER_VSR_APERTURETEST_01',0.15),\
        at.Marker('MARKER_VSR_APERTURETEST_01'),\
        at.Drift('DU_S1MT5R',0.01),\
        at.Marker('MSEC_D5_END'),\
    ] 
    
    T5 = [\
        at.Marker('MSEC_T5_START'),\
        at.Sextupole('S1MT5R',0.21,h=h1,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ1T5R', 0.07),\
        at.Monitor('BPMZ1T5R',Group='BPM'),\
        at.Drift('DU_Q1M1T5R', 0.09),\
        at.Quadrupole('Q1M1T5R',0.25,k=k1t),\
        at.Drift('DU_DBMLD5T5R', 0.058),\
        at.Monitor('DBMLD5T5R0',Group='BLM'),\
        at.Monitor('DBMLD5T5R',Group='BLM'),\
        at.Drift('DU_S2M1T5R', 0.23),\
        at.Sextupole('S2M1T5R',0.16,h=h2t,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ2T5R', 0.128),\
        at.Monitor('BPMZ2T5R',Group='BPM'),\
        at.Drift('DU_Q2M1T5R', 0.179),\
        at.Quadrupole('Q2M1T5R',0.2,k=k2t),\
        at.Drift('DU_BM1T5R', 0.42),\
        at.Dipole('BM1T5R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB1T5R', 0.265),\
        at.Monitor('DBLMB1T5R',Group='BLM'),\
        at.Drift('DU_Q3M1T5R', 0.155),\
        at.Quadrupole('Q3M1T5R',0.25,k=k3t5),\
        at.Drift('DU_BPMZ3T5R', 0.09),\
        at.Monitor('BPMZ3T5R',Group='BPM'),\
        at.Drift('DU_S3M1T5R', 0.063),\
        at.Sextupole('S3M1T5R',0.16,h=h3t,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_Q4M1T5R', 0.153),\
        at.Quadrupole('Q4M1T5R',0.5,k=k4t5),\
        at.Drift('DU_S4M1T5R', 0.153),\
        at.Sextupole('S4M1T5R',0.16,h=h4t,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_Q5M1T5R', 0.153),\
        at.Quadrupole('Q5M1T5R',0.2,k=k5t5),\
        at.Drift('DU_BPMZ4T5R', 0.092),\
        at.Monitor('BPMZ4T5R',Group='BPM'),\
        at.Drift('DU_MSEC10',2.361),\
        at.Marker('MSEC10'),\
        at.Marker('MUE46'),\
        at.Drift('DU_BPMZ5T5R', 2.361),\
        at.Monitor('BPMZ5T5R',Group='BPM'),\
        at.Drift('DU_Q5M2T5R', 0.092),\
        at.Quadrupole('Q5M2T5R',0.2,k=k5t5),\
        at.Drift('DU_S4M2T5R', 0.153),\
        at.Sextupole('S4M2T5R',0.16,h=h4t,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_Q4M2T5R', 0.153),\
        at.Quadrupole('Q4M2T5R',0.5,k=k4t5),\
        at.Drift('DU_S3M2T5R', 0.153),\
        at.Sextupole('S3M2T5R',0.16,h=h3t,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ6T5R', 0.063),\
        at.Monitor('BPMZ6T5R',Group='BPM'),\
        at.Drift('DU_Q3M2T5R', 0.09),\
        at.Quadrupole('Q3M2T5R',0.25,k=k3t5),\
        at.Drift('DU_BM2T5R', 0.42),\
        at.Dipole('BM2T5R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB2T5R', 0.27),\
        at.Monitor('DBLMB2T5R',Group='BLM'),\
        at.Drift('DU_Q2M2T5R', 0.150),\
        at.Quadrupole('Q2M2T5R',0.2,k=k2t),\
        at.Drift('DU_BPMZ7T5R', 0.244),\
        at.Monitor('BPMZ7T5R',Group='BPM'),\
        at.Drift('DU_S2M2T5R',0.063),\
        at.Sextupole('S2M2T5R',0.16,h=h2t,Corrector='V',Skew='CQ',KickAngle=[0,0]),\
        at.Drift('DU_Q1M2T5R', 0.288),\
        at.Quadrupole('Q1M2T5R',0.25,k=k1t),\
        at.Drift('DU_DBMLT5D6R0',0.105),\
        at.Monitor('DBMLT5D6R0',Group='BLM'),\
        at.Monitor('DBMLT5D6R',Group='BLM'),\
        at.Drift('DU_S1MD6R',0.055),\
        at.Marker('MSEC_T5_END'),\
        ]     
    
    D6 = [\
        at.Marker('MSEC_D6_START'),\
        at.Sextupole('S1MD6R',0.21,h=h1,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ1D6R',0.07),\
        at.Monitor('BPMZ1D6R',Group='BPM'),\
        at.Drift('DU_Q1M1D6R',0.09),\
        at.Quadrupole('Q1M1D6R',0.25,k=k1d),\
        at.Drift('DU_S2M1D6R',0.288),\
        at.Sextupole('S2M1D6R',0.16,h=h2d,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ2D6R',0.128),\
        at.Monitor('BPMZ2D6R',Group='BPM'),\
        at.Drift('DU_Q2M1D6R',0.179),\
        at.Quadrupole('Q2M1D6R',0.2,k=k2d),\
        at.Drift('DU_BM1D6R',0.42),\
        at.Dipole('BM1D6R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB1D6R',0.275),\
        at.Monitor('DBLMB1D6R',Group='BLM'),
        at.Drift('DU_Q3M1D6R',0.145),\
        at.Quadrupole('Q3M1D6R',0.25,k=k3d6),\
        at.Drift('DU_BPMZ3D6R',0.09),\
        at.Monitor('BPMZ3D6R',Group='BPM'),\
        at.Drift('DU_S3M1D6R',0.063),\
        at.Sextupole('S3M1D6R',0.16,h=h3d,Corrector='V',Skew='CQ',KickAngle=[0,0]),\
        at.Drift('DU_Q4M1D6R',0.153),\
        at.Quadrupole('Q4M1D6R',0.5,k=k4d6),\
        at.Drift('DU_S4M1D6R',0.153),
        at.Sextupole('S4M1D6R',0.16,h=h4d,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ4D6R',0.07),
        at.Monitor('BPMZ4D6R',Group='BPM'),\
        at.Drift('DU_B1IDSB',0.094),\
        at.Dipole('B1IDSB',0.28,0.0578788879,EntranceAngle=0.0, ExitAngle=0.0578788879),\
        at.Drift('DU_BPMZ41D6R',0.08),\
        at.Monitor('BPMZ41D6R',Group='BPM'),\
        at.Drift('DU_MU139',0.93682),\
        at.Marker('MU139'),\
        at.Drift('DU_BPMZ42D6R',0.91418),\
        at.Monitor('BPMZ42D6R',Group='BPM'),\
        at.Drift('DU_B2IDSB',0.08914),\
        at.Dipole('B2IDSB',0.56,-0.1117010721,EntranceAngle=-0.0578788879, ExitAngle=-0.0538221842),\
        at.Marker('MSEC11'),\
        at.Drift('DU_BPMZ43D6R',0.06386),\
        at.Monitor('BPMZ43D6R',Group='BPM'),\
        at.Drift('DU_MUE56_1',1.029315),\
        at.Marker('MUE56_1'),\
        at.Drift('DU_BPMZ44D6R',0.997685),\
        at.Monitor('BPMZ44D6R',Group='BPM'),\
        at.Drift('DU_B3IDSB',0.12539),\
        at.Dipole('B3IDSB',0.28,0.0538221842,EntranceAngle=0.0538221842, ExitAngle=0.0),\
        at.Drift('DU_S4M2D6R',0.1),\
        at.Sextupole('S4M2D6R',0.16,h=h4d,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_Q4M2D6R',0.153),\
        at.Quadrupole('Q4M2D6R',0.5,k=k4d6),\
        at.Drift('DU_S3M2D6R',0.153),\
        at.Sextupole('S3M2D6R',0.16,h=h3d,Corrector='V',Skew='CQ',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ6D6R',0.063),\
        at.Monitor('BPMZ6D6R',Group='BPM'),\
        at.Drift('DU_Q3M2D6R',0.09),\
        at.Quadrupole('Q3M2D6R',0.25,k=k3d6),\
        at.Drift('DU_BM2D6R',0.42),\
        at.Dipole('BM2D6R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB2D6R',0.27),\
        at.Monitor('DBLMB2D6R',Group='BLM'),\
        at.Drift('DU_Q2M2D6R',0.15),\
        at.Quadrupole('Q2M2D6R',0.2,k=k2d),\
        at.Drift('DU_BPMZ7D6R',0.244),\
        at.Monitor('BPMZ7D6R',Group='BPM'),\
        at.Drift('DU_S2M2D6R',0.063),\
        at.Sextupole('S2M2D6R',0.16,h=h2d,Corrector='V',Skew='CQ',KickAngle=[0,0]),\
        at.Drift('DU_Q1M2D6R',0.288),\
        at.Quadrupole('Q1M2D6R',0.25,k=k1d),\
        at.Drift('DU_DBMLD6T6R0',0.105),\
        at.Monitor('DBMLD6T6R0',Group='BLM'),\
        at.Monitor('DBMLD6T6R',Group='BLM'),\
        at.Drift('DU_S1MT6R',0.055),\
        at.Marker('MSEC_D6_END'),\
    ]
    
    T6 = [\
        at.Marker('MSEC_T6_START'),\
        at.Sextupole('S1MT6R',0.21,h=h1,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ1T6R', 0.07),\
        at.Monitor('BPMZ1T6R',Group='BPM'),\
        at.Drift('DU_Q1M1T6R', 0.09),\
        at.Quadrupole('Q1M1T6R',0.25,k=k1t),\
        at.Drift('DU_S2M1T6R', 0.288),\
        at.Sextupole('S2M1T6R',0.16,h=h2t,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ2T6R', 0.128),\
        at.Monitor('BPMZ2T6R',Group='BPM'),\
        at.Drift('DU_Q2M1T6R', 0.179),\
        at.Quadrupole('Q2M1T6R',0.2,k=k2t),\
        at.Drift('DU_BM1T6R', 0.42),\
        at.Dipole('BM1T6R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB1T6R', 0.265),\
        at.Monitor('DBLMB1T6R',Group='BLM'),\
        at.Drift('DU_Q3M1T6R', 0.155),\
        at.Quadrupole('Q3M1T6R',0.25,k=k3m1t6),\
        at.Drift('DU_BPMZ3T6R', 0.09),\
        at.Monitor('BPMZ3T6R',Group='BPM'),\
        at.Drift('DU_S3M1T6R', 0.063),\
        at.Sextupole('S3M1T6R',0.16,h=h3m1t6,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_Q4M1T6R', 0.153),\
        at.Quadrupole('Q4M1T6R',0.5,k=k4m1t6),\
        at.Drift('DU_S4M1T6R', 0.153),\
        at.Sextupole('S4M1T6R',0.16,h=h4m1t6,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_Q5M1T6R', 0.153),\
        at.Quadrupole('Q5M1T6R',0.2,k=k5m1t6),\
        at.Drift('DU_BPMZ4T6R', 0.092),\
        at.Monitor('BPMZ4T6R',Group='BPM'),\
        at.Drift('DU_MCPMU17_START',0.4425),\
        at.Marker('MCPMU17_START'),\
        at.Drift('DU_MCPMU17_MID',0.690002),\
        at.Marker('MCPMU17_MID'),\
        at.Drift('DU_MCPMU17_END',0.690002),\
        at.Marker('MCPMU17_END'),\
        at.Drift('DU_QIT6R',0.383409),\
        at.Quadrupole('QIT6R',0.244,k=kit6),\
#        at.Monitor('BPMZ41T6R') ?
        at.Drift('DU_BPMZ5T6R',2.272087),\
        at.Monitor('BPMZ5T6R',Group='BPM'),\
        at.Drift('DU_Q5M2T6R', 0.092),\
        at.Quadrupole('Q5M2T6R',0.2,k=k5m2t6),\
        at.Drift('DU_S4M2T6R', 0.153),\
        at.Sextupole('S4M2T6R',0.16,h=h4m2t6,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_Q4M2T6R', 0.153),\
        at.Quadrupole('Q4M2T6R',0.5,k=k4m2t6),\
        at.Drift('DU_S3M2T6R', 0.153),\
        at.Sextupole('S3M2T6R',0.16,h=h3m2t6,Corrector='V',Skew='CQ',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ6T6R', 0.063),\
        at.Monitor('BPMZ6T6R',Group='BPM'),\
        at.Drift('DU_Q3M2T6R', 0.09),\
        at.Quadrupole('Q3M2T6R',0.25,k=k3m2t6),\
        at.Drift('DU_BM2T6R', 0.42),\
        at.Dipole('BM2T6R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB2T6R', 0.27),\
        at.Monitor('DBLMB2T6R',Group='BLM'),\
        at.Drift('DU_Q2M2T6R', 0.150),\
        at.Quadrupole('Q2M2T6R',0.2,k=k2t),\
        at.Drift('DU_BPMZ7T6R', 0.244),\
        at.Monitor('BPMZ7T6R',Group='BPM'),\
        at.Drift('DU_S2M2T6R',0.063),\
        at.Sextupole('S2M2T6R',0.16,h=h2t,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_Q1M2T6R', 0.288),\
        at.Quadrupole('Q1M2T6R',0.25,k=k1t),\
        at.Drift('DU_DBMLT7D7R0',0.105),\
        at.Monitor('DBMLT6D7R0',Group='BLM'),\
        at.Monitor('DBMLT6D7R',Group='BLM'),\
        at.Drift('DU_S1MD7R',0.055),\
        at.Marker('MSEC_T6_END'),\
        ] 
    
    D7 = [\
        at.Marker('MSEC_D7_START'),\
        at.Sextupole('S1MD7R',0.21,h=h1,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ1D7R',0.07),\
        at.Monitor('BPMZ1D7R',Group='BPM'),\
        at.Drift('DU_Q1M1D7R',0.09),\
        at.Quadrupole('Q1M1D7R',0.25,k=k1d),\
        at.Drift('DU_S2M1D7R',0.288),\
        at.Sextupole('S2M1D7R',0.16,h=h2d,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ2D7R',0.128),\
        at.Monitor('BPMZ2D7R',Group='BPM'),\
        at.Drift('DU_Q2M1D7R',0.179),\
        at.Quadrupole('Q2M1D7R',0.2,k=k2d),\
        at.Drift('DU_BM1D7R',0.42),\
        at.Dipole('BM1D7R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB1D7R',0.275),\
        at.Monitor('DBLMB1D7R',Group='BLM'),
        at.Drift('DU_Q3M1D7R',0.145),\
        at.Quadrupole('Q3M1D7R',0.25,k=k3d7),\
        at.Drift('DU_BPMZ3D7R',0.09),\
        at.Monitor('BPMZ3D7R',Group='BPM'),\
        at.Drift('DU_S3M1D7R',0.063),\
        at.Sextupole('S3M1D7R',0.16,h=h3d,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_Q4M1D7R',0.153),\
        at.Quadrupole('Q4M1D7R',0.5,k=k4d7),\
        at.Drift('DU_S4M1D7R',0.153),
        at.Sextupole('S4M1D7R',0.16,h=h4d,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ4D7R',0.07),
        at.Monitor('BPMZ4D7R',Group='BPM'),\
        at.Drift('DU_MSEC13',2.736),\
        at.Marker('MSEC13'),\
        at.Marker('MUE112'),\
        at.Drift('DU_BPMZ5D7R',2.736),\
        at.Monitor('BPMZ5D7R',Group='BPM'),\
        at.Drift('DU_S4M2D7R',0.07),\
        at.Sextupole('S4M2D7R',0.16,h=h4d,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_Q4M2D7R',0.153),\
        at.Quadrupole('Q4M2D7R',0.5,k=k4d7),\
        at.Drift('DU_S3M2D7R',0.153),\
        at.Sextupole('S3M2D7R',0.16,h=h3d,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ6D7R',0.063),\
        at.Monitor('BPMZ6D7R',Group='BPM'),\
        at.Drift('DU_Q3M2D7R',0.09),\
        at.Quadrupole('Q3M2D7R',0.25,k=k3d7),\
        at.Drift('DU_BM2D7R',0.42),\
        at.Dipole('BM2D7R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB2D7R',0.25),\
        at.Monitor('DBLMB2D7R',Group='BLM'),\
        at.Drift('DU_Q2M2D7R',0.17),\
        at.Quadrupole('Q2M2D7R',0.2,k=k2d),\
        at.Drift('DU_BPMZ7D7R',0.244),\
        at.Monitor('BPMZ7D7R',Group='BPM'),\
        at.Drift('DU_S2M2D7R',0.063),\
        at.Sextupole('S2M2D7R',0.16,h=h2d,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_Q1M2D7R',0.288),\
        at.Quadrupole('Q1M2D7R',0.25,k=k1d),\
        at.Drift('DU_DBMLD7T7R0',0.095),\
        at.Monitor('DBMLD7T7R0',Group='BLM'),\
        at.Monitor('DBMLD7T7R',Group='BLM'),\
        at.Drift('DU_S1MT7R',0.065),\
        at.Marker('MSEC_D7_END'),\
    ]
    
    T7 = [\
        at.Marker('MSEC_T7_START'),\
        at.Sextupole('S1MT7R',0.21,h=h1,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ1T7R', 0.07),\
        at.Monitor('BPMZ1T7R',Group='BPM'),\
        at.Drift('DU_Q1M1T7R', 0.09),\
        at.Quadrupole('Q1M1T7R',0.25,k=k1t),\
        at.Drift('DU_S2M1T7R', 0.288),\
        at.Sextupole('S2M1T7R',0.16,h=h2t,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ2T7R', 0.128),\
        at.Monitor('BPMZ2T7R',Group='BPM'),\
        at.Drift('DU_Q2M1T7R', 0.179),\
        at.Quadrupole('Q2M1T7R',0.2,k=k2t),\
        at.Drift('DU_BM1T7R', 0.42),\
        at.Dipole('BM1T7R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB1T7R', 0.275),\
        at.Monitor('DBLMB1T7R',Group='BLM'),\
        at.Drift('DU_Q3M1T7R', 0.145),\
        at.Quadrupole('Q3M1T7R',0.25,k=k3t7),\
        at.Drift('DU_BPMZ3T7R', 0.09),\
        at.Monitor('BPMZ3T7R',Group='BPM'),\
        at.Drift('DU_S3M1T7R', 0.063),\
        at.Sextupole('S3M1T7R',0.16,h=h3t,Corrector='V',Skew='CQ',KickAngle=[0,0]),\
        at.Drift('DU_Q4M1T7R', 0.153),\
        at.Quadrupole('Q4M1T7R',0.5,k=k4t7),\
        at.Drift('DU_S4M1T7R', 0.153),\
        at.Sextupole('S4M1T7R',0.16,h=h4t,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_Q5M1T7R', 0.153),\
        at.Quadrupole('Q5M1T7R',0.2,k=k5t7),\
        at.Drift('DU_BPMZ4T7R', 0.092),\
        at.Monitor('BPMZ4T7R',Group='BPM'),\
        at.Drift('DU_MSEC14',2.361),\
        at.Marker('MSEC14'),\
        at.Marker('MBAMWLS2'),\
        at.Drift('DU_BPMZ5T7R', 2.361),\
        at.Monitor('BPMZ5T7R',Group='BPM'),\
        at.Drift('DU_Q5M2T7R', 0.092),\
        at.Quadrupole('Q5M2T7R',0.2,k=k5t7),\
        at.Drift('DU_S4M2T7R', 0.153),\
        at.Sextupole('S4M2T7R',0.16,h=h4t,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_Q4M2T7R', 0.153),\
        at.Quadrupole('Q4M2T7R',0.5,k=k4t7),\
        at.Drift('DU_S3M2T7R', 0.153),\
        at.Sextupole('S3M2T7R',0.16,h=h3t,Corrector='V',Skew='CQ',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ6T7R', 0.063),\
        at.Monitor('BPMZ6T7R',Group='BPM'),\
        at.Drift('DU_Q3M2T7R', 0.09),\
        at.Quadrupole('Q3M2T7R',0.25,k=k3t7),\
        at.Drift('DU_BM2T7R', 0.42),\
        at.Dipole('BM2T7R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB2T7R', 0.26),\
        at.Monitor('DBLMB2T7R',Group='BLM'),\
        at.Drift('DU_Q2M2T7R', 0.16),\
        at.Quadrupole('Q2M2T7R',0.2,k=k2t),\
        at.Drift('DU_BPMZ7T7R', 0.244),\
        at.Monitor('BPMZ7T7R',Group='BPM'),\
        at.Drift('DU_S2M2T7R',0.063),\
        at.Sextupole('S2M2T7R',0.16,h=h2t,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_Q1M2T7R', 0.288),\
        at.Quadrupole('Q1M2T7R',0.25,k=k1t),\
        at.Drift('DU_DBMLT7D8R0',0.105),\
        at.Monitor('DBMLT7D8R0',Group='BLM'),\
        at.Monitor('DBMLT7D8R',Group='BLM'),\
        at.Drift('DU_S1MD8R',0.055),\
        at.Marker('MSEC_T7_END'),\
        ]

    D8 = [\
        at.Marker('MSEC_D8_START'),\
        at.Sextupole('S1MD8R',0.21,h=h1,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ1D8R',0.07),\
        at.Monitor('BPMZ1D8R',Group='BPM'),\
        at.Drift('DU_Q1M1D8R',0.09),\
        at.Quadrupole('Q1M1D8R',0.25,k=k1d),\
        at.Drift('DU_S2M1D8R',0.288),\
        at.Sextupole('S2M1D8R',0.16,h=h2d,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ2D8R',0.128),\
        at.Monitor('BPMZ2D8R',Group='BPM'),\
        at.Drift('DU_Q2M1D8R',0.179),\
        at.Quadrupole('Q2M1D8R',0.2,k=k2d),\
        at.Drift('DU_BM1D8R',0.42),\
        at.Dipole('BM1D8R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB1D8R',0.265),\
        at.Monitor('DBLMB1D8R',Group='BLM'),
        at.Drift('DU_Q3M1D8R',0.155),\
        at.Quadrupole('Q3M1D8R',0.25,k=k3d8),\
        at.Drift('DU_BPMZ3D8R',0.09),\
        at.Monitor('BPMZ3D8R',Group='BPM'),\
        at.Drift('DU_S3M1D8R',0.063),\
        at.Sextupole('S3M1D8R',0.16,h=h3d,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_Q4M1D8R',0.153),\
        at.Quadrupole('Q4M1D8R',0.5,k=k4d8),\
        at.Drift('DU_S4M1D8R',0.153),
        at.Sextupole('S4M1D8R',0.16,h=h4d,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ4D8R',0.07),
        at.Monitor('BPMZ4D8R',Group='BPM'),\
        at.Drift('DU_FOMZ1D8R',0.351),\
        at.Monitor('FOMZ1D8R'),\
        at.Drift('DU_MUE49_2',2.385),\
        at.Marker('MUE49_2'),\
        at.Marker('MSEC15'),\
        at.Drift('DU_BPMZ5D8R',2.736),\
        at.Monitor('BPMZ5D8R',Group='BPM'),\
        at.Drift('DU_S4M2D8R',0.07),\
        at.Sextupole('S4M2D8R',0.16,h=h4d,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_Q4M2D8R',0.153),\
        at.Quadrupole('Q4M2D8R',0.5,k=k4d8),\
        at.Drift('DU_S3M2D8R',0.153),\
        at.Sextupole('S3M2D8R',0.16,h=h3d,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ6D8R',0.063),\
        at.Monitor('BPMZ6D8R',Group='BPM'),\
        at.Drift('DU_Q3M2D8R',0.09),\
        at.Quadrupole('Q3M2D8R',0.25,k=k3d8),\
        at.Drift('DU_BM2D8R',0.42),\
        at.Dipole('BM2D8R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB2D8R',0.26),\
        at.Monitor('DBLMB2D8R',Group='BLM'),\
        at.Drift('DU_Q2M2D8R',0.16),\
        at.Quadrupole('Q2M2D8R',0.2,k=k2d),\
        at.Drift('DU_BPMZ7D8R',0.244),\
        at.Monitor('BPMZ7D8R',Group='BPM'),\
        at.Drift('DU_S2M2D8R',0.063),\
        at.Sextupole('S2M2D8R',0.16,h=h2d,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_Q1M2D8R',0.288),\
        at.Quadrupole('Q1M2D8R',0.25,k=k1d),\
        at.Drift('DU_DBMLD8T8R0',0.105),\
        at.Monitor('DBMLD8T8R0',Group='BLM'),\
        at.Monitor('DBMLD8T8R',Group='BLM'),\
        at.Drift('DU_S1MT8R',0.055),\
        at.Marker('MSEC_D8_END'),\
    ]
            
    T8 = [\
        at.Marker('MSEC_T8_START'),\
        at.Sextupole('S1MT8R',0.21,h=h1,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ1T8R', 0.07),\
        at.Monitor('BPMZ1T8R',Group='BPM'),\
        at.Drift('DU_Q1M1T8R', 0.09),\
        at.Quadrupole('Q1M1T8R',0.25,k=k1t),\
        at.Drift('DU_S2M1T8R', 0.288),\
        at.Sextupole('S2M1T8R',0.16,h=h2t,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ2T8R', 0.128),\
        at.Monitor('BPMZ2T8R',Group='BPM'),\
        at.Drift('DU_Q2M1T8R', 0.179),\
        at.Quadrupole('Q2M1T8R',0.2,k=k2t),\
        at.Drift('DU_BM1T8R', 0.42),\
        at.Dipole('BM1T8R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB1T8R', 0.275),\
        at.Monitor('DBLMB1T8R',Group='BLM'),\
        at.Drift('DU_Q3M1T8R', 0.145),\
        at.Quadrupole('Q3M1T8R',0.25,k=k3m1t8),\
        at.Drift('DU_BPMZ3T8R', 0.09),\
        at.Monitor('BPMZ3T8R',Group='BPM'),\
        at.Drift('DU_S3M1T8R', 0.063),\
        at.Sextupole('S3M1T8R',0.16,h=h3t,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_Q4M1T8R', 0.153),\
        at.Quadrupole('Q4M1T8R',0.5,k=k4m1t8),\
        at.Drift('DU_S4M1T8R', 0.153),\
        at.Sextupole('S4M1T8R',0.16,h=h4t,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_Q5M1T8R', 0.153),\
        at.Quadrupole('Q5M1T8R',0.2,k=k5m1t8),\
        at.Drift('DU_BPMZ4T8R', 0.092),\
        at.Monitor('BPMZ4T8R',Group='BPM'),\
        at.Drift('DU_CAVH1T8R', 0.845),\
        at.RFCavity('CAVH1T8R',0.54,main_cavity_voltage,rf_frequency,harmonic_number,energy,Group='CAV500'),\
        at.Drift('DU_CAVH2T8R', 0.3755),\
        at.RFCavity('CAVH2T8R',0.54,main_cavity_voltage,rf_frequency,harmonic_number,energy,Group='CAV500'),\
        at.Drift('DU_MSEC16', 0.0605),\
        at.Marker('MSEC16'),\
        at.Drift('DU_CAVH3T8R', 0.3155),\
        at.RFCavity('CAVH3T8R',0.54,main_cavity_voltage,rf_frequency,harmonic_number,energy,Group='CAV500'),\
        at.Drift('DU_CAVH4T8R', 0.3755),\
        at.RFCavity('CAVH4T8R',0.54,main_cavity_voltage,rf_frequency,harmonic_number,energy,Group='CAV500'),\
        at.Drift('DU_BPMZ5T8R', 0.59),\
        at.Monitor('BPMZ5T8R',Group='BPM'),\
        at.Drift('DU_Q5M2T8R', 0.092),\
        at.Quadrupole('Q5M2T8R',0.2,k=k5m2t8),\
        at.Drift('DU_S4M2T8R', 0.153),\
        at.Sextupole('S4M2T8R',0.16,h=h4t,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_Q4M2T8R', 0.153),\
        at.Quadrupole('Q4M2T8R',0.5,k=k4m2t8),\
        at.Drift('DU_S3M2T8R', 0.153),\
        at.Sextupole('S3M2T8R',0.16,h=h3t,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ6T8R', 0.063),\
        at.Monitor('BPMZ6T8R',Group='BPM'),\
        at.Drift('DU_Q3M2T8R', 0.09),\
        at.Quadrupole('Q3M2T8R',0.25,k=k3m2t8),\
        at.Drift('DU_BM2T8R', 0.42),\
        at.Dipole('BM2T8R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB2T8R', 0.26),\
        at.Monitor('DBLMB2T8R',Group='BLM'),\
        at.Drift('DU_Q2M2T8R', 0.16),\
        at.Quadrupole('Q2M2T8R',0.2,k=k2t),\
        at.Drift('DU_BPMZ7T8R', 0.244),\
        at.Monitor('BPMZ7T8R',Group='BPM'),\
        at.Drift('DU_S2M2T8R',0.063),\
        at.Sextupole('S2M2T8R',0.16,h=h2t,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_Q1M2T8R', 0.288),\
        at.Quadrupole('Q1M2T8R',0.25,k=k1t),\
        at.Drift('DU_DBMLT8D1R0',0.095),\
        at.Monitor('DBMLT8D1R0',Group='BLM'),\
        at.Monitor('DBMLT8D1R',Group='BLM'),\
        at.Drift('DU_S1MD1R',0.065),\
        at.Marker('MSEC_T8_END'),\
        ]     
  
    D1_firsthalf = [\
        at.Marker('MSEC_D1_START'),\
        at.Sextupole('S1MD1R',0.21,h=h1,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ1D1R',0.07),\
        at.Monitor('BPMZ1D1R',Group='BPM'),\
        at.Drift('DU_Q1M1D1R',0.09),\
        at.Quadrupole('Q1M1D1R',0.25,k=k1d),\
        at.Drift('DU_S2M1D1R',0.288),\
        at.Sextupole('S2M1D1R',0.16,h=h2d,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ2D1R',0.128),\
        at.Monitor('BPMZ2D1R',Group='BPM'),\
        at.Drift('DU_Q2M1D1R',0.179),\
        at.Quadrupole('Q2M1D1R',0.2,k=k2d),\
        at.Drift('DU_BM1D1R',0.42),\
        at.Dipole('BM1D1R', bending_length, bending_angle,EntranceAngle=bending_entrance_angle, ExitAngle=bending_exit_angle, FullGap=bending_fullgap, FringeInt1=bending_entrance_fint, FringeInt2=bending_exit_fint,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_DBLMB1D1R',0.275),\
        at.Monitor('DBLMB1D1R',Group='BLM'),\
        at.Drift('DU_Q3M1D1R',0.145),\
        at.Quadrupole('Q3M1D1R',0.25,k=k3d1),\
        at.Drift('DU_BPMZ3D1R',0.09),\
        at.Monitor('BPMZ3D1R',Group='BPM'),\
        at.Drift('DU_S3M1D1R',0.063),\
        at.Sextupole('S3M1D1R',0.16,h=h3d1,Corrector='V',KickAngle=[0,0]),\
        at.Drift('DU_Q4M1D1R',0.153),\
        at.Quadrupole('Q4M1D1R',0.5,k=k4d1),\
        at.Drift('DU_S4M1D1R',0.153),\
        at.Sextupole('S4M1D1R',0.16,h=h4d1,Corrector='H',KickAngle=[0,0]),\
        at.Drift('DU_BPMZ4D1R',0.07),\
        at.Monitor('BPMZ4D1R',Group='BPM'),\
        at.Drift('DU_KIK1D1R',0.2295),\
        at.Drift('KIK1D1R',0.595),\
        at.Drift('DU_BPMZ41D1R',0.1265),\
        at.Monitor('BPMZ41D1R',Group='BPM'),\
        at.Drift('DU_BPMZ42D1R',0.20939),\
        at.Monitor('BPMZ42D1R',Group='BPM'),\
        #at.Drift('DU_KIK2D1R',0.13289-0.00639),\
        at.Drift('DU_KIK2D1R',0.12011),    
        at.Drift('KIK2D1R',0.595),\
        at.Drift('DU_FOMZ1D1R',0.3465),\
        at.Monitor('FOMZ1D1R'),\
        at.Drift('DU_MRING_END',0.514),\
        at.Marker('MRING_END'),\
        ]    

    # Ring definition
    ring=[D1_secondhalf, T1, D2, T2, D3, T3 , D4, T4, D5, T5, D6, T6, D7, T7, D8, T8, D1_firsthalf]
        
    # Expand ring until list completely flattened
    while any(isinstance(x, list) for x in ring):
        ring = list(chain.from_iterable(i if isinstance(i, list) else [i] for i in ring))
          
    # Build the lattice  
    ring = at.Lattice(ring,name='BESSY II',energy=energy)
     
    # Turn cavity and radiation on
    ring.enable_6d()
    
    # Set cavpts to point to main cavities
    ring.cavpts = ring.get_uint32_index('CAV*')
    
    # Set only main cavity phases
    ring.set_cavity_phase(cavpts=ring.cavpts)
    
    return ring

if __name__ == '__main__':
    ring = bessy2Lattice()
