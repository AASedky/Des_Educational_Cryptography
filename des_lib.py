def rotate(strg,n):
    return strg[n:] + strg[:n]
def to_bin64(b) :
    return (bin(int(b,16))[2:]).zfill(64)
def to_bin48(b):
    return (bin(int(b,16))[2:]).zfill(48)
def to_hex (h):
    return (hex(int(h,2))[2:])
##### one round #############
def s_boxes_(XOR_res,s_boxes):
    com="" #data combine
    j=0
    for i in range (0,48,6):
        row=""
        column=""
        row+=XOR_res[i]+XOR_res[i+5] #b1b6
        nrow=int(row,2)  #to decimal
        column+=XOR_res[i+1]+XOR_res[i+2]+XOR_res[i+3]+XOR_res[i+4] #b2b3b4b5
        ncolumn=int(column,2) #to decimal 
        sn=s_boxes[j]
        j+=1
        com+=(bin(int(str(sn[nrow][ncolumn]),10))[2:]).zfill(4) # 4 bit each block
    return com
def f_dash(expansion_table,rn,kn,s_boxes,f_p_table) :
     data=""     
     for i in range (48) :##expand
        data+=rn[expansion_table[i]-1]
     XOR_res=int(data,2)^int(kn,2) ## convert string to binary to apply XOR
     XOR_res=(bin(int(str(XOR_res),10))[2:]).zfill(48) #save 48 bit  
     data_combine=s_boxes_(XOR_res,s_boxes)
     per_data=""
     for j in range (32) : #permutaion table
         per_data+=data_combine[f_p_table[j]-1]
     return per_data
def roundx (expansion_table,data,kn,s_boxes,f_p_table) :
    ln=""
    rn=""
    for i in range(32) :
        ln+=data[i]
    for j in range (32,64):
        rn+=data[j]
    print('ln\t{0}\trn\t{1}\tround key\t{2}'.format(to_hex(ln),to_hex(rn),to_hex(kn)))
    r_n_dash=f_dash(expansion_table,rn,kn,s_boxes,f_p_table)
    rn1=int(ln,2)^int(r_n_dash,2)
    rn1=(bin(int(str(rn1),10))[2:]).zfill(32)
    res=''
    res+=rn+rn1
    return res
####################
def init_per(IP,binary) :
    res=""
    for i in range(64) :
        res+=binary[IP[i]-1]
    return res
#######################
def key_per(c0,d0,key):
    k_c=""
    k_d="" 
    for i in range(28) :
        k_c+=key[c0[i]-1]
        k_d+=key[d0[i]-1]
    return k_c, k_d
#######################
def generation_key(key_choice,k_c,k_d,ind,op):
    k_Dash=""
    k_n=""
    if not (ind == 0 or ind == 1 or ind == 8 or ind == 15) :
        if op == 'e': #encryption
            k_c=rotate(k_c,1)## 1 left extra in this rounds
            k_d=rotate(k_d,1)
            
        elif op == 'd' and ind != 0: #no rotaion in round one
           k_c=rotate(k_c,-1)## 1 right extra in this rounds
           k_d=rotate(k_d,-1)
    if op == 'e' : 
      k_c=rotate(k_c,1)## 1 left
      k_d=rotate(k_d,1)
       
        
    elif op == 'd' and ind !=0 :
        k_c=rotate(k_c,-1)## 1 right 
        k_d=rotate(k_d,-1)
    k_Dash+=k_c
    k_Dash+=k_d
    for i in range(48) :
        k_n+=k_Dash[key_choice[i]-1]      
    return k_Dash , k_n,k_c,k_d
####################################
def final_per(IP_inv,data):
    final_data=''
    for i in range (64):
        final_data+=data[IP_inv[i]-1]
    return final_data
###################################
def swap_bin(data):
    res=''
    for i in range (32,64):
        res+=data[i]
    for i in range (0,32):
        res+=data[i]
    return res
