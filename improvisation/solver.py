def calc_base(_c):
    c = bin(_c)[2:]
    # The last character of flag is '\n'(0b0000_1010), 
    # (i.e. flag.bit_length % 8 == 4)
    # so we need zero-paddings at the beginning of ciphertext
    while len(c) % 8 != 4:
        c = '0' + c
    c = c[:64]
    m = int.from_bytes(b'CakeCTF{', 'little')
    # m.bit_length() == 63, so r_64 <- 0
    m = '0' + bin(m)[2:]
    r = ''
    for i in range(64):
        # r_i = c_i ^ m_i
        r = str(int(c[i])^int(m[-(i+1)])) + r
    return int(r,2)

def LFSR_call(_r, bitlength):
    r = _r
    r_ls = []
    for i in range(bitlength):
        r_ls.append(r & 1)
        b = (r & 1) ^\
            ((r & 2) >> 1) ^\
            ((r & 8) >> 3) ^\
            ((r & 16) >> 4)
        r = (r >> 1) | (b << 63)
    return r_ls

def decrypt(_c, ls):
    c = bin(_c)[2:]
    # the same reason as above
    while len(c) % 8 != 4:
        c = '0' + c

    m = ''
    for i in range(len(c)):
        # m_i = c_i ^ r_i
        m += str(int(c[i])^ls[i])
    return int(m[::-1], 2).to_bytes(len(ls)//8+1, 'little')

def main():
    c = 0x58566f59979e98e5f2f3ecea26cfb0319bc9186e206d6b33e933f3508e39e41bb771e4af053
    # r_1 ~ r_64 calculation
    r = calc_base(c)
    # r_65 ~ calclation based on the information of (r_1, ..., r_64)
    r_ls = LFSR_call(r, (c.bit_length()//8)*8+4)
    
    print(decrypt(c, r_ls))

main()