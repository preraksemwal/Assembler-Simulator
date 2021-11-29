 

import matplotlib.pyplot as plt                   # @ PRERAK @ VINEET
cycles=[]
memory_accesses=[]
memory_accesses_index=0

                                                  # @ VINEET

opcode = { "00000":"add","00001":"sub","00110":"mul","01010":"xor","01011":"or","01100":"and",
           "00010":"movB","01000":"rs","01001":"ls",
           "00011":"movC","00111":"div","01101":"not","01110":"cmp",
           "00100":"ld","00101":"st",
           "01111":"jmp","10000":"jlt","10001":"jgt","10010":"je",
           "10011":"hlt"}   

                                                  # @ VINEET

register_code = {"000":"R0","001":"R1","010":"R2","011":"R3","100":"R4","101":"R5","110":"R6","111":"FLAGS"}

                                                  # @ PRERAK

register_values = {
    "R0"    : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],  
    "R1"    : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "R2"    : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "R3"    : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "R4"    : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "R5"    : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "R6"    : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    "FLAGS" : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
}
#  @ VINEET                            V L G E  

def list_to_decimal(l):                    # @ PRERAK  
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    res=0; i=0;
    for j in range(len(l)-1,-1,-1):
        res+=l[j]*pow(2,i)
        i+=1
    return res
def decimal_to_list(val):                  # @ PRERAK
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    res=[]
    s=bin(val); s1=s[2:]; 
    if(len(s1)>=16): # overflow will be dealt with overflow function
        for i in range(-1,-17,-1):
            res.append(int(s1[i]))
        res.reverse()
    else:
        for i in range(16-len(s1)):
            res.append(0)
        for x in s1:
            res.append(int(x))
    return res
def string_to_decimal(s):                  # @ PRERAK
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    res=0; i=0;
    for j in range(len(s)-1,-1,-1):
        res+=int(s[j])*pow(2,i)
        i+=1
    return res

def overflow(val1,val2,operation):         # @ PRERAK @ VINEET
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    if(operation=="+"):
        if(val1+val2>pow(2,16)-1):
            return True
        else:
            return False
    if(operation=="-"):
        if(val1-val2<0):
            return True
        else:
            return False
    if(operation=="*"):
        if(val1*val2>pow(2,16)-1):
            return True
        else:
            return False
def compare(reg1_code,reg2_code):          # @ PRERAK 
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    val1=list_to_decimal(register_values[register_code[reg1_code]])
    val2=list_to_decimal(register_values[register_code[reg2_code]])
    if(val1<val2):
        return -1
    elif val1==val2:
        return 0
    else:
        return 1

######################################################################

import sys
memory=list(sys.stdin.read().split('\n'))   # @ PRERAK
memory.pop(-1)
for i in range(len(memory)):
    temp=[]
    for j in range(16):
        temp.append(int(memory[i][j]))    
    memory[i]=temp
for i in range(256-len(memory)):
    memory.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

pc = [0,0,0,0,0,0,0,0]

def MEM(index):                             # @ PRERAK
    return memory[index]

def RF(reg_name):                           # @ PRERAK
    return list_to_decimal(register_values[reg_name])

def print_pc_and_registers():               # @ PRERAK @ VINEET
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    ans=""
    for i in range(len(pc)):
        ans+=str(pc[i])
    ans+=" "
    for x in register_values.values():
        for j in range(len(x)):
            ans+=str(x[j])
        ans+=" "
    sys.stdout.write(ans+'\n')
def print_memory_dump():                    # @ PRERAK @ VINEET
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    for x in memory:
        ans=""
        for i in range(len(x)):
            ans+=str(x[i])
        sys.stdout.write(ans+'\n')
def reset_flags():                          # @ PRERAK @ VINEET
    global pc
    global memory
    global register_values
    global register_code
    global opcode

    register_values["FLAGS"][-1]=0
    register_values["FLAGS"][-2]=0
    register_values["FLAGS"][-3]=0
    register_values["FLAGS"][-4]=0

def plot_memory_accesses():                 # @ PRERAK
    global cycles
    global memory_accesses
    plt.plot(cycles,memory_accesses,color='b',marker='o',linestyle='-',linewidth='1',markersize=6)
    plt.title("Memory accesses  vs.  Cycles",fontsize=15)
    plt.xlabel("Cycle",fontsize=15)
    plt.ylabel("Address",fontsize=15)
    plt.show()

def EE():                                   # @ PRERAK @ VINEET
    while True:
        global pc
        global memory
        global register_values
        global register_code
        global opcode
        global cycles
        global memory_accesses
        global memory_accesses_index
        index=list_to_decimal(pc)
        current_instruction=MEM(index) 
        verdict=execute(current_instruction) 
        if(verdict==1):
            cycles.append(memory_accesses_index)
            memory_accesses_index+=1
            memory_accesses.append(list_to_decimal(pc))
            pc=decimal_to_list(list_to_decimal(pc)+1)
            pc=pc[8:]
        if(verdict==-1):
            break
    
        


def add_instruction(current_instruction):  # @ PRERAK @ VINEET
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    s=""
    for x in current_instruction:
        s+=str(x)
    reg1_code=s[7:10]
    reg2_code=s[10:13]
    reg3_code=s[13:]
    val2=list_to_decimal( register_values[register_code[reg2_code]] )
    val3=list_to_decimal( register_values[register_code[reg3_code]] )
    res=val2+val3
    reset_flags()
    if(overflow(val2,val3,'+')):   
        register_values["FLAGS"][-4]=1
    register_values[register_code[reg1_code]]=decimal_to_list(res)
    print_pc_and_registers()
def sub_instruction(current_instruction):  # @ PRERAK @ VINEET
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    s=""
    for x in current_instruction:
        s+=str(x)
    reg1_code=s[7:10]
    reg2_code=s[10:13]
    reg3_code=s[13:]
    val2=list_to_decimal( register_values[register_code[reg2_code]] )
    val3=list_to_decimal( register_values[register_code[reg3_code]] )
    res=val2-val3
    reset_flags()
    if(overflow(val2,val3,'-')):
        register_values["FLAGS"][-4]=1
    if(res>=0):
        register_values[register_code[reg1_code]]=decimal_to_list(res)
    else:
        register_values[register_code[reg1_code]]=decimal_to_list(0)
    print_pc_and_registers()
def mul_instruction(current_instruction):  # @ PRERAK @ VINEET
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    s=""
    for x in current_instruction:
        s+=str(x)
    reg1_code=s[7:10]
    reg2_code=s[10:13]
    reg3_code=s[13:]
    val2=list_to_decimal( register_values[register_code[reg2_code]] )
    val3=list_to_decimal( register_values[register_code[reg3_code]] )
    res=val2*val3
    reset_flags()
    if(overflow(val2,val3,'*')):
        register_values["FLAGS"][-4]=1
    register_values[register_code[reg1_code]]=decimal_to_list(res)
    print_pc_and_registers()
def xor_instruction(current_instruction):  # @ PRERAK @ VINEET
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    s=""
    for x in current_instruction:
        s+=str(x)
    reg1_code=s[7:10]
    reg2_code=s[10:13]
    reg3_code=s[13:]
    val2=list_to_decimal( register_values[register_code[reg2_code]] )
    val3=list_to_decimal( register_values[register_code[reg3_code]] )
    res=(val2^val3)
    register_values[register_code[reg1_code]]=decimal_to_list(res)
    reset_flags()
    print_pc_and_registers()
def or_instruction(current_instruction):   # @ PRERAK @ VINEET
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    s=""
    for x in current_instruction:
        s+=str(x)
    reg1_code=s[7:10]
    reg2_code=s[10:13]
    reg3_code=s[13:]
    val2=list_to_decimal( register_values[register_code[reg2_code]] )
    val3=list_to_decimal( register_values[register_code[reg3_code]] )
    res=(val2|val3)
    register_values[register_code[reg1_code]]=decimal_to_list(res)
    reset_flags()
    print_pc_and_registers()
def and_instruction(current_instruction):  # @ PRERAK @ VINEET
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    s=""
    for x in current_instruction:
        s+=str(x)
    reg1_code=s[7:10]
    reg2_code=s[10:13]
    reg3_code=s[13:]
    val2=list_to_decimal( register_values[register_code[reg2_code]] )
    val3=list_to_decimal( register_values[register_code[reg3_code]] )
    res=(val2&val3)
    register_values[register_code[reg1_code]]=decimal_to_list(res)
    reset_flags()
    print_pc_and_registers()



def movB_instruction(current_instruction): # @ ABHINAV 
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    s=""
    for x in current_instruction:
        s+=str(x)
    reg1_code=s[5:8]
    imm_=s[8:];
    imm=[0,0,0,0,0,0,0,0]
    for x in imm_:
        imm.append(int(x))
    register_values[register_code[reg1_code]]=imm
    reset_flags()
    print_pc_and_registers()
def ls_instruction(current_instruction):   # @ ABHINAV
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    s=""
    for x in current_instruction:
        s+=str(x)
    reg1_code=s[5:8]
    imm_=s[8:];
    imm=[0,0,0,0,0,0,0,0]
    for x in imm_:
        imm.append(int(x))
    val=list_to_decimal(register_values[register_code[reg1_code]])
    val = (val<<list_to_decimal(imm))
    register_values[register_code[reg1_code]]=decimal_to_list(val)
    reset_flags()
    print_pc_and_registers()
def rs_instruction(current_instruction):   # @ ABHINAV
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    s=""
    for x in current_instruction:
        s+=str(x)
    reg1_code=s[5:8]
    imm_=s[8:];
    imm=[0,0,0,0,0,0,0,0]
    for x in imm_:
        imm.append(int(x))
    val=list_to_decimal(register_values[register_code[reg1_code]])
    val = (val>>list_to_decimal(imm))
    register_values[register_code[reg1_code]]=decimal_to_list(val)
    reset_flags()
    print_pc_and_registers()
def movC_instruction(current_instruction): # @ ABHINAV
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    s=""
    for x in current_instruction:
        s+=str(x)
    reg1_code=s[10:13] # R3
    reg2_code=s[13:] #FLAGs
    register_values[register_code[reg1_code]]=register_values[register_code[reg2_code]].copy()
    reset_flags()
    print_pc_and_registers()
def div_instruction(current_instruction):  # @ ABHINAV
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    s=""
    for x in current_instruction:
        s+=str(x)
    reg1_code=s[10:13]
    reg2_code=s[13:]
    register_values["R0"]=decimal_to_list(int( list_to_decimal(register_values[register_code[reg1_code]]) / list_to_decimal(register_values[register_code[reg2_code]]) ) )
    register_values["R1"]=decimal_to_list( list_to_decimal(register_values[register_code[reg1_code]]) % list_to_decimal(register_values[register_code[reg2_code]]) )
    reset_flags()
    print_pc_and_registers()
def cmp_instruction(current_instruction):  # @ ABHINAV
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    s=""
    for x in current_instruction:
        s+=str(x)
    reg1_code=s[10:13]
    reg2_code=s[13:]
    verdict=compare(reg1_code,reg2_code)
    reset_flags()
    if(verdict==-1):
        register_values["FLAGS"][-3]=1
    elif (verdict==0):
        register_values["FLAGS"][-1]=1
    else:
        register_values["FLAGS"][-2]=1
    print_pc_and_registers()



def not_instruction(current_instruction):  # @ PRERAK @ VINEET
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    s=""
    for x in current_instruction:
        s+=str(x)
    reg1_code=s[10:13]
    reg2_code=s[13:]
    val= register_values[register_code[reg2_code]]
    for i in range(len(val)):
        val[i]=1-val[i]
    register_values[register_code[reg1_code]]=val
    reset_flags()
    print_pc_and_registers()
def ld_instruction(current_instruction):   # @ PRERAK @ VINEET
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    s=""
    for x in current_instruction:
        s+=str(x)
    reg1_code=s[5:8]
    index = string_to_decimal(s[8:])
    data=MEM(index)
    register_values[register_code[reg1_code]]=data
    reset_flags()
    print_pc_and_registers()
def st_instruction(current_instruction):   # @ PRERAK @ VINEET
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    s=""
    for x in current_instruction:               
        s+=str(x)                         
    reg1_code=s[5:8]
    index=string_to_decimal(s[8:])
    memory[index]=register_values[register_code[reg1_code]]
    reset_flags()
    print_pc_and_registers()
def jmp_instruction(current_instruction):  # @ PRERAK @ VINEET
    global cycles
    global memory_accesses
    global memory_accesses_index
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    s=""
    for x in current_instruction:
        s+=str(x)
    mem_addr=s[8:] #string
    reset_flags()
    print_pc_and_registers()
    cycles.append(memory_accesses_index)
    memory_accesses_index+=1
    memory_accesses.append(list_to_decimal(pc))
    pc=decimal_to_list(string_to_decimal(mem_addr))
    pc=pc[8:]
def jlt_instruction(current_instruction):  # @ PRERAK @ VINEET
    global cycles
    global memory_accesses
    global memory_accesses_index
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    s=""
    for x in current_instruction:
        s+=str(x)
    mem_addr=s[8:] #string
    if(register_values["FLAGS"][-3]==1):
        pc_=decimal_to_list(string_to_decimal(mem_addr))
        pc_=pc_[8:]
        reset_flags()
        print_pc_and_registers()
        cycles.append(memory_accesses_index)
        memory_accesses_index+=1
        memory_accesses.append(list_to_decimal(pc))
        pc=pc_
    else:
        reset_flags()
        print_pc_and_registers()
        cycles.append(memory_accesses_index)
        memory_accesses_index+=1
        memory_accesses.append(list_to_decimal(pc))
        pc=decimal_to_list(list_to_decimal(pc)+1)
        pc=pc[8:]
def jgt_instruction(current_instruction):  # @ PRERAK @ VINEET
    global cycles
    global memory_accesses
    global memory_accesses_index
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    s=""
    for x in current_instruction:
        s+=str(x)
    mem_addr=s[8:] #string
    if(register_values["FLAGS"][-2]==1):
        pc_=decimal_to_list(string_to_decimal(mem_addr))
        pc_=pc_[8:]
        reset_flags()
        print_pc_and_registers()
        cycles.append(memory_accesses_index)
        memory_accesses_index+=1
        memory_accesses.append(list_to_decimal(pc))
        pc=pc_
    else:
        reset_flags()
        print_pc_and_registers()
        cycles.append(memory_accesses_index)
        memory_accesses_index+=1
        memory_accesses.append(list_to_decimal(pc))
        pc=decimal_to_list(list_to_decimal(pc)+1)
        pc=pc[8:]
def je_instruction(current_instruction):   # @ PRERAK @ VINEET
    global cycles
    global memory_accesses
    global memory_accesses_index
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    s=""
    for x in current_instruction:
        s+=str(x)
    mem_addr=s[8:] #string
    if(register_values["FLAGS"][-1]==1):
        pc_=decimal_to_list(string_to_decimal(mem_addr))
        pc_=pc_[8:]
        reset_flags()
        print_pc_and_registers()
        cycles.append(memory_accesses_index)
        memory_accesses_index+=1
        memory_accesses.append(list_to_decimal(pc))
        pc=pc_
    else:
        reset_flags()
        print_pc_and_registers()
        pc=decimal_to_list(list_to_decimal(pc)+1)
        pc=pc[8:]


def execute(current_instruction):          # @ PRERAK @ VINEET
    global cycles
    global memory_accesses
    global memory_accesses_index
    global pc
    global memory
    global register_values
    global register_code
    global opcode
    opc=""
    for i in range(5):
        opc+=str(current_instruction[i])
    current_instruction_name=opcode[opc]
    if current_instruction_name=='add':
        add_instruction(current_instruction)
        return 1
    elif current_instruction_name=='sub':
        sub_instruction(current_instruction)
        return 1
    elif current_instruction_name=='mul':
        mul_instruction(current_instruction)
        return 1
    elif current_instruction_name=='xor':
        xor_instruction(current_instruction)
        return 1
    elif current_instruction_name=='or':
        or_instruction(current_instruction)
        return 1
    elif current_instruction_name=='and':
        and_instruction(current_instruction)
        return 1

    elif current_instruction_name=='movB':
        movB_instruction(current_instruction)
        return 1
    elif current_instruction_name=='rs':
        rs_instruction(current_instruction)
        return 1
    elif current_instruction_name=='ls':
        ls_instruction(current_instruction)
        return 1

    elif current_instruction_name=='movC':
        movC_instruction(current_instruction)
        return 1
    elif current_instruction_name=='div':
        div_instruction(current_instruction)
        return 1
    elif current_instruction_name=='not':
        not_instruction(current_instruction)
        return 1
    elif current_instruction_name=='cmp':
        cmp_instruction(current_instruction)
        return 1

    elif current_instruction_name=='ld':
        ld_instruction(current_instruction)
        return 1
    elif current_instruction_name=='st':
        st_instruction(current_instruction)
        return 1

    elif current_instruction_name=='jmp':
        jmp_instruction(current_instruction)
        return 0
    elif current_instruction_name=='jlt':
        jlt_instruction(current_instruction)
        return 0

    elif current_instruction_name=='jgt':
        jgt_instruction(current_instruction)
        return 0

    elif current_instruction_name=='je':
        je_instruction(current_instruction)
        return 0

    elif current_instruction_name=='hlt':
        print_pc_and_registers()
        cycles.append(memory_accesses_index)
        memory_accesses_index+=1
        memory_accesses.append(list_to_decimal(pc))
        return -1
        


EE()                                       # @ PRERAK @ VINEET
print_memory_dump()                        # @ PRERAK @ VINEET

plot_memory_accesses()                     # @ PRERAK


