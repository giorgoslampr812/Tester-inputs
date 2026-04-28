import pandas as pd
import numpy as np
import re
for i in range(1, 17):
 CSV_IN = f"B_A_{i}/B_A_{i}_rpc_with_pt_charge.csv"
 CSV_OUT = f"B_A_{i}/B_A_{i}_rpc_bit_192.csv"

 # --- helper functions ---
 def int_to_bits(value, width):
    return format(int(value), f"0{width}b")

 def tc_to_bits(tc):
    val = int(tc) if not pd.isna(tc) else 0
    return format(min(max(0,val),7),"03b")

 def float_to_eta_bits(eta):
    val = 0 if pd.isna(eta) else int(round((eta + 2.7)/0.00033))
    val = min(max(0,val), 2**14-1)
    return format(val,"014b")

 def float_to_phi_bits(phi):
    val = 0 if pd.isna(phi) else int(round((phi + np.pi)/0.012))
    val = min(max(0,val), 2**9-1)
    return format(val,"09b")

 def pt_threshold_to_bits(pt_thr):
    val = 0 if pd.isna(pt_thr) else int(pt_thr)
    val = min(max(0,val),15)
    return format(val,"04b")

 def charge_to_bits(charge):
    val = 0 if pd.isna(charge) else int(charge)
    return "1" if val else "0"

 def coincidence_to_bits(coinc):
    val = 0 if pd.isna(coinc) else int(coinc)
    val = min(max(0,val),7)
    return format(val,"03b")

 def z_rpc_to_bits(z_val):
    val = 0 if pd.isna(z_val) else int(round(z_val / 16))
    val = min(max(0,val),1023)
    return format(val,"010b")

 def generate_32bit_header(row):
    bcid = int(row.get("BCID",0))
    bcid_bits = int_to_bits(bcid,12)

    nTC_val = int(row.get("nTC",0))
    nTC_bits = int_to_bits(nTC_val & 0b111,3)
    overflow_bit = "1" if nTC_val > 7 else "0"

    sector = str(row.get("sector",""))
    m = re.match(r"B[M|C](\d+)", sector)
    n_val = int(m.group(1)) if m else 0
    n_val = n_val - 1 if n_val >= 1 else 0
    n_bits = int_to_bits(n_val & 0b1111,4)

    reserved_bits = "0"*12

    return bcid_bits + nTC_bits + overflow_bit + n_bits + reserved_bits

 def crc8_from_bits(bit_string, poly=0x07):
    bits = [int(b) for b in bit_string]
    bits += [0]*8
    poly_bits = [int(b) for b in f"{poly:08b}"]
    for i in range(len(bit_string)):
        if bits[i]==1:
            for j in range(8):
                bits[i+j] ^= poly_bits[j]
    crc_bits = bits[-8:]
    return "".join(str(b) for b in crc_bits)

# --- read CSV ---
 df = pd.read_csv(CSV_IN)

 mTC_streams = []
 header_32bit_streams = []
 trailer_streams = []
 complete_streams = []

 COMMA_8BIT = "11100000"  # K28.5 comma

 for idx, row in df.iterrows():
    # 128-bit mTC
    tc_bits = tc_to_bits(row.get("TC",0))
    eta_bits = float_to_eta_bits(row.get("Eta",0))
    phi_bits = float_to_phi_bits(row.get("Phi",0))
    pt_bits = pt_threshold_to_bits(row.get("pt_threshold",0))
    charge_bit = charge_to_bits(row.get("charge",0))
    coinc_bits = coincidence_to_bits(row.get("coincidence",0))
    z3_bits = z_rpc_to_bits(row.get("z_RPC3",0))
    z2_bits = z_rpc_to_bits(row.get("z_RPC2",0))
    z1_bits = z_rpc_to_bits(row.get("z_RPC1",0))
    z0_bits = z_rpc_to_bits(row.get("z_RPC0",0))
    reserved_54 = "0"*54

    mTC_bits = (tc_bits + eta_bits + phi_bits + pt_bits + charge_bit +
                coinc_bits + z3_bits + z2_bits + z1_bits + z0_bits +
                reserved_54)
    mTC_streams.append(mTC_bits)

    # 32-bit header
    header_bits = generate_32bit_header(row)
    header_32bit_streams.append(header_bits)

    # 32-bit trailer: 8-bit comma + 8-bit CRC + 16-bit reserved
    crc_bits = crc8_from_bits(header_bits + mTC_bits)
    trailer_bits = COMMA_8BIT + crc_bits + "0"*16
    trailer_streams.append(trailer_bits)

    # 192-bit complete: header + mTC + trailer
    complete_bits = header_bits + mTC_bits + trailer_bits
    complete_streams.append(complete_bits)

 # --- add columns ---
 df["mTC"] = mTC_streams
 df["header_32bit"] = header_32bit_streams
 df["trailer"] = trailer_streams
 df["complete"] = complete_streams

 # --- save CSV ---
 df.to_csv(CSV_OUT, index=False)
 print(f"Saved {CSV_OUT} with mTC (128), header_32bit (32), trailer (32) and complete (192) streams")

