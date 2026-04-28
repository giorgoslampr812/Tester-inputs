Simple python scripts to prepare L0MDT tester inputs 

Script descriptions 

A and C are ATLAS detector sides in the barrel

rpc_pt.py: Calculates pt,pt_threshold and charge for sector logic word, using a fit of the RPC coordinates. 

com_bit_rpc_{A,C}: For every trigger word that the pT fit worked it calculates the full 192 bit stream ( 32 header ,128 word , 32 trailer). This uniquely defines an event that can be utilized for the tester. 
