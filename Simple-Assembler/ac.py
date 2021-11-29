#  @PRERAK  instructions     -> instructions for which binary to be generated
#  @PRERAK  var_instructions -> variable declarations only
#  @PRERAK  address          -> tells us the instruction's address
#  @PRERAK  opcode           -> dictionary ..stores opcode for each key (say 'mul')
#  @PRERAK  register_code    -> dictionary..stores code for each register as key
###############################################################################################
import sys
l=list(sys.stdin.read().split('\n'))

for i in range(len(l)):
    buff=l[i].split() # @PRERAK  ignore the extra spaces
    s_="" 
    for x in buff:
        s_+=x
        s_+=" "
    ss=s_[:-1]   # to ignore extra space
    l[i]=ss

var_instructions=[]
instructions=[]
labels={}
count=0; var_count=0;

for i in range(len(l)):
    if(l[i]==''):
        continue

    temp = l[i].split(' ') #  @PRERAK  temp=['label2:' , 'mov' , 'R1' , '$5']
    if(temp[0][-1]==':'):
        label_str = temp[0][:-1]
        if(len(temp)==1):  # if only label definition is there
            continue
        if(temp[1]=='var'):
            labels[label_str]=[var_count,-1]  #  @PRERAK  -1 is dummmy to identify var labels
            var_count += 1
        else:
            labels[label_str]=count
            count += 1
        temp = temp[1:] #  @PRERAK  temp=['mov' , 'R1' , '$5'], if more than one lable ERROR
        buff=""
        for x in temp[0:-1]:
            buff=buff+x+" "
        buff+=temp[-1]      #  @PRERAK  now its as if label was never there
        if(buff[0:3]!="var"):
            instructions.append(buff)
            instructions[-1]=instructions[-1].split(' ')
        else:
            var_instructions.append(buff)
            var_instructions[-1]=var_instructions[-1].split(' ')


    else:
        if(l[i][0:3]!="var"):
            count += 1
            instructions.append(l[i])
            instructions[-1]=instructions[-1].split(' ')
        else:
            var_count += 1
            var_instructions.append(l[i])
            var_instructions[-1]=var_instructions[-1].split(' ')


for x in labels.keys():
    if(type(labels[x])==type([])):
        labels[x]=len(instructions)+labels[x][0]


# @PRERAK                                                   (TARGET INSTRUCTION)
# @PRERAK instruc address i -> if i<len(instructions) => instructions[address[i]]
# @PRERAK                  ->     >                  => var_instructions[address[i]]
address = list(range(0,len(instructions))) + list(range(0,len(var_instructions)))

#  @PRERAK 
##############################################################################################
# print("instructions     -> ",instructions);print();print("var_instructions -> ",var_instructions);print();print("address          -> ",address);print();print("labels           -> ",labels);print("l\t\t",l);
##############################################################################################

#  @PRERAK  dictionaries for opcode and register's code

opcode = { "add":"00000","sub":"00001","mul":"00110","xor":"01010","or":"01011","and":"01100",
           "movB":"00010","rs":"01000","ls":"01001",
           "movC":"00011","div":"00111","not":"01101","cmp":"01110",
           "ld":"00100","st":"00101",
           "jmp":"01111","jlt":"10000","jgt":"10001","je":"10010",
           "hlt":"10011"}   
register_code = {"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}
R0 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
R1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
R2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
R3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
R4 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
R5 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
R6 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

#   @PRERAK                       V  L  G  E
FLAGS = [0,0,0,0,0,0,0,0,0,0,0,0, 0, 0, 0, 0]


def binary(current_instruction,current_instruction_type): #  @PRERAK  return binary eq. as string
    if(current_instruction[0]=='mov'):
        if(current_instruction_type=='B'):
            s = opcode["movB"]
        else:
            s = opcode["movC"]
    else:
        s = opcode[current_instruction[0]]

    if(current_instruction_type=='A'):
        s+="00"
        s+=register_code[current_instruction[1]]
        s+=register_code[current_instruction[2]]
        s+=register_code[current_instruction[3]]

    

    elif(current_instruction_type=='B'):
        s+=register_code[current_instruction[1]]
        n=int(current_instruction[2][1:])
        s1=str(bin(n))[2:]
        if(len(s1)<8):
            for i in range(8-len(s1)):
                s+="0"
        s+=s1


    elif(current_instruction_type=='C'):
        s+="00000"
        s+=register_code[current_instruction[1]]
        s+=register_code[current_instruction[2]]

    
    elif(current_instruction_type=='D'):
        s+=register_code[current_instruction[1]]
        for i in range(len(var_instructions)):
            if(var_instructions[i][-1]==current_instruction[2]):
                addr=len(instructions)+i
                s1=str(bin(addr))[2:]
                if(len(s1)<8):
                    for i in range(8-len(s1)):
                        s+="0"
                s+=s1
                break
        

    elif(current_instruction_type=='E'):  #  @PRERAK  JUMP TO LABEL
        s+="000"
        goto_label=current_instruction[1]
        for x in labels.keys():
            if(x==goto_label):
                addr=labels[x]
                s1=str(bin(addr))[2:]
                if(len(s1)<8):
                    for i in range(8-len(s1)):
                        s+="0"
                s+=s1
                break
    

    elif(current_instruction_type=='F'):
        s+="00000000000"


    return s


def instruction_type(current_instruction):    #  @PRERAK  tell type of passed instrcn.

    if(current_instruction[0]=='add' or current_instruction[0]=='sub' or current_instruction[0]=='mul' or current_instruction[0]=='or' or current_instruction[0]=='xor' or current_instruction[0]=='and'):
        return 'A'
    if(current_instruction[0]=='rs' or current_instruction[0]=='ls'):
        return 'B'
    if(current_instruction[0]=='div' or current_instruction[0]=='not' or current_instruction[0]=='cmp'):
        return 'C'
    if(current_instruction[0]=='st' or current_instruction[0]=='ld'):
        return 'D'
    if(current_instruction[0]=='je' or current_instruction[0]=='jgt' or current_instruction[0]=='jlt' or current_instruction[0]=='jmp'):
        return 'E'
    if(current_instruction[0]=='hlt'):
        return 'F'
    if(current_instruction[0]=='mov'):       # @PRERAK  we deal with 'mov' separately
        if(current_instruction[-1][0]=='$'):
            return 'B'
        else:
            return 'C'




################################################################################################################
###########################    ERRORS   ########################################################################
################################################################################################################


# @ABHINAV        @ PRERAK    @ VINEET

error_line=-9
state=-8

def no_of_statements_till_now_instrn(l,i):
    count_var=0; count_norm=0;
    for j in range(len(l)):
        if(l[j]==''):
            continue

        temp=l[j].split()
        if(temp[0][-1]==':'): # label
            if(len(temp)!=1 and temp[1][0]=='v'):
                count_var+=1
            else:
                count_norm+=1
        else: # no label
            if(temp[0][0]=='v'):
                count_var+=1
            else:
                count_norm+=1
        if(count_norm==i+1):
            break
    return count_var+count_norm


def no_of_statements_till_now_var(l,i):
    count_var=0; count_norm=0;
    for j in range(len(l)):
        if(l[j]==''):
            continue
        temp=l[j].split()
        if(temp[0][-1]==':'): # label
            if(temp[1][0]=='v'):
                count_var+=1
            else:
                count_norm+=1
        else: # no label
            if(temp[0][0]=='v'):
                count_var+=1
            else:
                count_norm+=1
        if(count_var==i+1):
            break
    return count_var+count_norm

def hlt_error(instructions):
    global error_line   
    if( len(instructions)==0 or instructions[-1]!=['hlt']):
        error_line=-1
        return True # no hlt in end
    count=0
    for j in range(len(instructions)):
        if(instructions[j]==['hlt']):
            count+=1
            if(j<len(instructions)-1):
                error_line=len(var_instructions)+j+1
                return True  # multiple hlt
    if(count<1):
        error_line=-3
        return True  # no hlt at all
    return False
def label_error(instructions,var_instructions):
    global error_line
    global state

    for i in range(len(instructions)):   
        if(instructions[i][0][-1]==':'):
            error_line=no_of_statements_till_now_instrn(l,i) 
            state=1
            return True   # double label
        if(instruction_type(instructions[i])=='E'):
            if(instructions[i][-1] not in labels.keys()):
                error_line=no_of_statements_till_now_instrn(l,i)   
                state=2
                return True # undefined label

    for i in range(len(var_instructions)):
        if(var_instructions[i][0][-1]==':'):
            error_line=no_of_statements_till_now_var(l,i)  
            state=3 
            return True # double label
    return False     



def illegal_imm_error(instructions):
    global error_line
    for i in range(len(instructions)):
        if(instruction_type(instructions[i])=='B'):
            num = int(instructions[i][-1][1:])
            if(num<0 or num>255):
                error_line=len(var_instructions)+i+1
                return True
    return False
def illegal_flags_error(instructions):
    global error_line
    for i in range(len(instructions)):
        if(instructions[i][-1]=='FLAGS'):
            if(instructions[i][0]!='mov'):
                error_line=no_of_statements_till_now_instrn(l,i)  
                return True
        typ=instruction_type(instructions[i])
        if(typ=='A'):
            if(instructions[i][1]=='FLAGS' or instructions[i][2]=='FLAGS'):
                error_line=no_of_statements_till_now_instrn(l,i)   
                return True
        elif(typ=='B'):
            if(instructions[i][1]=='FLAGS'):
                error_line=no_of_statements_till_now_instrn(l,i)   
                return True
        elif(typ=='C'):
            if(instructions[i][1]=='FLAGS'):
                error_line=no_of_statements_till_now_instrn(l,i)  
                return True
        else:
            if(typ=='D' and instructions[i][1]=='FLAGS'):  
                error_line=no_of_statements_till_now_instrn(l,i)  
                return True
    return False
def typo_error(instructions):
    global state
    global error_line
    for i in range(len(instructions)): 
        if( len(instructions[i])==1 and instructions[i]!=['hlt']):
            state=0   # fkg;typ
            error_line=len(var_instructions)+i+1
            return True
        if( (instructions[i][0] not in opcode.keys()) and (instructions[i][0]!='mov') ):
            state=1 # opcode typo
            error_line=len(var_instructions)+i+1
            return True
        typ = instruction_type(instructions[i])
        if(typ=='A' or typ=='B' or  typ=='C' or  typ=='D'):
            if(instructions[i][1] not in register_code.keys()):
                state=2  # first register's typo
                error_line=len(var_instructions)+i+1
                return True
        if(typ=='A'):
            if((instructions[i][2] not in register_code.keys()) or (instructions[i][3] not in register_code.keys())):
                state=2 # second or third reg's typo
                error_line=len(var_instructions)+i+1
                return True
        if(typ=='C'):
            if(instructions[i][2] not in register_code.keys()):
                state=2 # second reg's typo
                error_line=len(var_instructions)+i+1
                return True
def length_error(instructions): # var_instrucions
    global error_line

    for j in range(len(var_instructions)):
        if(len(var_instructions[j])!=2):
            error_line=j+1
            return True

    for i in range(len(instructions)):
        typ=instruction_type(instructions[i])
        num=len(instructions[i])
        if(typ=='A' and num!=4):
            error_line=len(var_instructions)+i+1
            return True
            
        elif((typ=='B' or typ=='C' or typ=='D') and num!=3):
            error_line=len(var_instructions)+i+1
            return True

        elif(typ=='E' and num!=2):
            error_line=len(var_instructions)+i+1
            return True

        elif(typ=='F' and num!=1):
            error_line=len(var_instructions)+i+1
            return True
        return False
def var_error(l):
    global error_line
    global state
    flag=0
    count_norm=0
    count_var=0
    for i in range(len(l)):
        if(l[i]==''):
            continue
        if(flag==0):
            temp=l[i].split()
            if(temp[0][-1]==':'): # label
                if(temp[1][0]=='v'):
                    count_var+=1
                else:
                    flag=1
                    count_norm+=1
            else: # no label
                if(temp[0][0]=='v'):
                    count_var+=1
                else:
                    flag=1
                    count_norm+=1
        elif(flag==1):
             temp=l[i].split()
             if(temp[0][-1]==':'): # label
                if(temp[1][0]!='v'):
                    count_norm+=1
                else:
                    flag=2
                    count_var+=1
             else: # no label
                if(temp[0][0]!='v'):
                    count_norm+=1
                else:
                    flag=2
                    count_var+=1


        if(flag==2):
            error_line=count_var+count_norm
            state=1   # not all var on top
            return True

    buff=[]
    for x in var_instructions:
        buff.append(x[1])

    for i in range(len(instructions)):
        if(instruction_type(instructions[i])=='D'):
            if(instructions[i][-1] not in buff):
                error_line=len(var_instructions)+i+1
                state=2
                return True # undefined var

    return False


def error(instructions):

    if(label_error(instructions,var_instructions)):
        if(state==1 or state==3):
            sys.stderr.write("Label ERROR : Syntax Error at line  ")
            sys.stdout.write(str(error_line))
        elif(state==2):
            sys.stderr.write("Label ERROR : Undefined label at line  ")
            sys.stdout.write(str(error_line))
        return True
    if(hlt_error(instructions)):
        if(error_line==-1):
            sys.stderr.write("hlt ERROR : no 'hlt' statement in the end")
        elif error_line==-3:
            sys.stderr.write("hlt ERROR : no 'hlt' statement found !")
        else:
            sys.stderr.write("hlt ERROR : invalid 'hlt' statement at line  ")
            sys.stdout.write(str(error_line))
        return True
    if(illegal_imm_error(instructions)):
        sys.stderr.write("Immediate Value ERROR : immediate value out of bounds at line  ")
        sys.stdout.write(str(error_line))
        return True
    if(illegal_flags_error(instructions)):
        sys.stderr.write("Flag ERROR : Invalid syntax for FLAGS at line  ")
        sys.stdout.write(str(error_line))
        return True
    if(length_error(instructions)):   
        sys.stderr.write("Invalid instruction ERROR : Invalid Syntax at line  ")
        sys.stdout.write(str(error_line))
        return True
    if(typo_error(instructions)):
        if(state==0):
            sys.stderr.write("Typo ERROR : Invalid Syntax at line  ")
            sys.stdout.write(str(error_line))
        elif(state==1):
            sys.stderr.write("Typo ERROR : Invalid instruction at line  ")
            sys.stdout.write(str(error_line))
        elif(state==2):
            sys.stderr.write("Typo ERROR : Invalid Register syntax at line  ")
            sys.stdout.write(str(error_line))
        return True
    if(var_error(l)):
        if(state==1):
            sys.stderr.write("Variable ERROR : Invalid variable declaration at line  ")
            sys.stdout.write(str(error_line))
        else:
            sys.stderr.write("Variable ERROR : Undefined variable at line  ")
            sys.stdout.write(str(error_line))
        return True

    
    
if(error(instructions)):
    exit()
##########################################################################


for i in range(len(instructions)):  #  @PRERAK  simply iterate on instructions
    print(binary(instructions[i],instruction_type(instructions[i])))
