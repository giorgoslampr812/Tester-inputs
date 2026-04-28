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

Run on this file https://mattermost.web.cern.ch/files/7jc1qu4fpbbrmyrr13ja7b35he/public?h=2f6D4tjJVDqZAvaGqCKWIR1dPqplhZvq4t9Yc8eomoc to produce tests vectors following the repository instructions. It will take roughly 1-2 hours. 

In the TVOutputs directory you should now have a subdirectory named CSV which contains directories with names B_A_1, B_C_1 ,.. etc. Here you can run the python scripts. 

The scripts should be run with the following order. 

For RPC: rpc_pt.py -> com_bit_rpc_{A,C}.py. 

For MDT: mdt_filt_{A,C}.py OR eta_window_mdt_filt_{A,C}.py -> hit_offset_{A,C}.py and optionally filt_hitmap_{A,C}.py for sanity checks. If it gives errors its because output directories don't exist so please make them with mkdir command. The python enviroment can be the one set up by the TV framework. 

Congraturations, now you should have the correct hits and sector logic words so you can proceed to the next level of the emulation. 

Making the tester inputs
