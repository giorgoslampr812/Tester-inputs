Simple python scripts to prepare L0MDT tester inputs 

Script descriptions for MDT hit extraction

A and C are ATLAS detector sides in the barrel.

rpc_pt.py: Calculates pt,pt_threshold and charge for sector logic word, using a fit of the RPC coordinates. 

com_bit_rpc_{A,C}.py: For every trigger word that the pT fit worked it calculates the full 192 bit stream ( 32 header ,128 word , 32 trailer). This uniquely defines an event that can be utilized for the tester. 

mdt_filt_{A,C}.py: Utilizing the r,z coordinates of the RPC trigger words, selects hits from an area +-12 cms (half length of mezzanine card), isolating the MDT hits for emulation. 

eta_window_mdt_filt_{A,C}.py: Utilizing the eta coordinate of the RPC trigger words, selects MDT hits for a tunable Deta area close to the RPC coordinates. Slightly improved implementation over the mdt_filt as it naturally increases based on the distance to the IP. 

hit_offset_{A,C}.py: From the skimmed MDT hits from the previous two algorithms, selects the 2 hottest mezzanines per MDT layer for the emulation. 

filt_hitmap_{A,C}.py: Runs on the hit_offset outputs and makes sanity plots to check that algorithms worked correctly. 

Workflow- How to run: 

Firstly, an active CERN account is needed. Then the following repository https://gitlab.cern.ch/atlas-tdaq-phase2-l0mdt-electronics/gateware-validation/tv should be cloned and instructions to run should be followed. Important is to do recursive clone for the subdirectories. 

Run 
