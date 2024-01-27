'''
===================================================================

 ██████╗  ██████╗    ███████╗██╗███╗   ███╗
██╔═══██╗██╔════╝    ██╔════╝██║████╗ ████║
██║   ██║██║         ███████╗██║██╔████╔██║
██║▄▄ ██║██║         ╚════██║██║██║╚██╔╝██║
╚██████╔╝╚██████╗    ███████║██║██║ ╚═╝ ██║
 ╚══▀▀═╝  ╚═════╝    ╚══════╝╚═╝╚═╝     ╚═╝
                                           
qc-sim, a quantum simulator @ Bart Bozon 

===================================================================
'''

import numpy as np
import copy

try:
    import matplotlib.pyplot as plt
except ImportError:
    print ("ERROR : matplotlib not found, no graphical output")

try:
    from HersheyFonts import HersheyFonts #https://pypi.org/project/Hershey-Fonts/
    thefont = HersheyFonts()
    thefont.load_default_font()
    thefont.normalize_rendering(40)
except ImportError:
    print ("ERROR : HersheyFonts not found")

I_m=np.zeros((2,2),dtype='csingle')
I_m[0][0]=1
I_m[0][1]=0
I_m[1][0]=0
I_m[1][1]=1

x_m=np.zeros((2,2),dtype='csingle')
x_m[0][0]=0
x_m[0][1]=1
x_m[1][0]=1
x_m[1][1]=0

y_m=np.zeros((2,2),dtype='csingle')
y_m[0][0]=0
y_m[0][1]=-1j
y_m[1][0]=1j
y_m[1][1]=0

z_m=np.zeros((2,2),dtype='csingle')
z_m[0][0]=1
z_m[0][1]=0
z_m[1][0]=0
z_m[1][1]=-1

s_m=np.zeros((2,2),dtype='csingle')
s_m[0][0]=1
s_m[0][1]=0
s_m[1][0]=0
s_m[1][1]=1j

t_m=np.zeros((2,2),dtype='csingle')
t_m[0][0]=1
t_m[0][1]=0
t_m[1][0]=0
t_m[1][1]=np.sqrt(0.5)+np.sqrt(0.5)*1j

hadamard_m=np.zeros((2,2),dtype='csingle')
hadamard_m[0][0]=0.5**0.5
hadamard_m[0][1]=0.5**0.5
hadamard_m[1][0]=0.5**0.5
hadamard_m[1][1]=-0.5**0.5

c_not_m=np.zeros((4,4),dtype='csingle')
c_not_m[0][0]=1
c_not_m[1][1]=1
c_not_m[2][3]=1
c_not_m[3][2]=1

c_z_m=np.zeros((4,4),dtype='csingle')
c_z_m[0][0]=1
c_z_m[1][1]=1
c_z_m[2][2]=1
c_z_m[3][3]=-1

swap_m=np.zeros((4,4),dtype='csingle')
swap_m[0][0]=1
swap_m[1][2]=1
swap_m[2][1]=1
swap_m[3][3]=1

cc_not_m=np.zeros((8,8),dtype='csingle')
cc_not_m[0][0]=1
cc_not_m[1][1]=1
cc_not_m[2][2]=1
cc_not_m[3][3]=1
cc_not_m[4][4]=1
cc_not_m[5][5]=1
cc_not_m[6][7]=1
cc_not_m[7][6]=1

gates={  
        'X':x_m,  
        'Y':y_m,  
        'Z':z_m,  
        'S':s_m,  
        'T':t_m,  
        'H':hadamard_m,  
        'I':I_m, 
        'c_not':c_not_m,
        'c_Z':c_z_m,
        'swap':swap_m,
        'cc_not':cc_not_m
}  

I='I'
X='X'
Y='Y'
Z='Z'
S='S'
T='T'
H='H'

c_not='c_not'
c_Z='c_Z'
swap='swap'
cc_not='cc_not'

two_bit_gates={c_not,c_Z,swap}
three_bit_gates={cc_not}

class create_quantum_computer:
    W  = '\033[0m'  # white (normal)
    R  = '\033[31m' # red
    G  = '\033[32m' # green
    O  = '\033[33m' # orange
    B  = '\033[34m' # blue
    P  = '\033[35m' # purple
    def __init__(self,*argument):
        if len(argument)<1:
            print (self.R+'error: you have not determined how many bits the computer should have')
        if len(argument)>0:    
            n=argument[0]
            self.start_print = ['' for x in range(n)]
            self.end_print = ['' for x in range(n)]
            self.statevector=np.zeros((2**n),dtype='csingle')
            self.statevector[0]=1 # initialize the system with zero's
            self.order_list=[]
            self.show_execution=True
            for i in range (0,n):
                self.order_list.append(n-i-1)
            self.amount_of_bits=n
            self.gatelist = ['I' for x in range(n)]
        if len(argument)>1:  
            t=argument[1]
            self.global_gatelist = [['I' for x in range(n)] for y in range(t)]                
    def execute_gates(self,gl):
        if self.show_execution:
            print (self.W+'============= Execute gates =====================')
        self.calc_matrix=1
        for g in gl:
            if self.show_execution:
                print (g)
            self.calc_matrix=np.kron(self.calc_matrix,gates[g])
            #print (calc_matrix)
        #print (statevector)
        self.statevector=self.calc_matrix.dot(self.statevector)
        #print (statevector)
    def print_statevector(self):
        i=0
        print (self.W+'============= Statevector =======================')
        for s in self.statevector:
            stri='0000000000'+"{0:b}".format(i)
            if abs(s.real) <0.01 :
                sreal='0.00'
            else:
                sreal=(str((s.real))+'   ')[0:4]
            if abs(s.imag) <0.01 :
                simag='0.00'
            else:
                simag=(str((s.real))+'   ')[0:4]
            stri=sreal+' '+simag+'i |'+stri[-self.amount_of_bits:]+'>'
            #stri=(str((s.real))+'   ')[0:4]+' '+(str((s.imag))+'   ')[0:4]+'i |'+stri[-amount_of_bits:]+'>'
            #num=str(100*abs(s)**2)
            #stri=num[0:3]+'% |'+stri[-3:]+'>'
            print (stri)
            i=i+1    
    def measure_statevector(self):
        i=0
        print (self.W+'============= Perform virtual measurement =======')
        for s in self.statevector:
            if abs(s)>0.01:
                stri='0000000000'+"{0:b}".format(i)
                stri=str(100*abs(s)**2)[0:5]+'% |'+stri[-self.amount_of_bits:]+'>'
                #num=str(100*abs(s)**2)
                #stri=num[0:3]+'% |'+stri[-3:]+'>'
                print (stri)
            i=i+1    
    def measure_statevector_graphical(self):
        i=0
        labels=[]
        results=[]
        for s in self.statevector:
            stri='0000000000'+"{0:b}".format(i)
            stri='|'+stri[-self.amount_of_bits:]+'>'
            labels.append(stri)
            stri=abs(s)**2           
            results.append(stri)
            i=i+1
        if self.amount_of_bits>4 :    
            fig = plt.figure(figsize=(20,11))
        else:
            fig = plt.figure(figsize=(9,4))
        ax = fig.add_axes([0,0,1,1])
        ax.barh(labels,results)
        plt.show()            
    def __bring_2_lines_to_top(self,a,b):
        self.intermediate_order_list=copy.deepcopy(self.order_list)
        in1 = self.intermediate_order_list.index(a)
        dum=self.intermediate_order_list[-1]
        self.intermediate_order_list[-1]=self.intermediate_order_list[in1]
        self.intermediate_order_list[in1]=dum
        in1 = self.intermediate_order_list.index(b)
        dum=self.intermediate_order_list[-2]
        self.intermediate_order_list[-2]=self.intermediate_order_list[in1]
        self.intermediate_order_list[in1]=dum
    def __bring_3_lines_to_top(self,a,b,c):
        self.intermediate_order_list=copy.deepcopy(self.order_list)
        in1 = self.intermediate_order_list.index(a)
        dum=self.intermediate_order_list[-1]
        self.intermediate_order_list[-1]=self.intermediate_order_list[in1]
        self.intermediate_order_list[in1]=dum
        in1 = self.intermediate_order_list.index(b)
        dum=self.intermediate_order_list[-2]
        self.intermediate_order_list[-2]=self.intermediate_order_list[in1]
        self.intermediate_order_list[in1]=dum
        in1 = self.intermediate_order_list.index(c)
        dum=self.intermediate_order_list[-3]
        self.intermediate_order_list[-3]=self.intermediate_order_list[in1]
        self.intermediate_order_list[in1]=dum        
    def __determine_swap_vector(self):
        self.swap_vector = [None] * (2**len(self.order_list))
        la=self.order_list
        #print (la)
        s1=[]
        for i in range (0,2**len(la)):
            s1.append(set())
            for j in range (0,len(la)):
                if (i&(2**j))>0:
                    s1[i].add(la[j])
        la=self.intermediate_order_list
        s2=[]
        #print (la)
        for i in range (0,2**len(la)):
            s2.append(set())
            for j in range (0,len(la)):
                if (i&(2**j))>0:
                    s2[i].add(la[j])
        for i in range (len(s1)):
            for j in range (len(s2)):
                if s1[i]==s2[j]:                
                    self.swap_vector[i]=j
        #print (swap_vector)        
    def __swap_bits(self):
        self.new_statevector=copy.deepcopy(self.statevector)
        for i in range(len(self.statevector)):
            self.new_statevector[self.swap_vector[i]]=self.statevector[i]
            #new_statevector[i]=statevector[swap_vector[i]]
        self.statevector=copy.deepcopy(self.new_statevector)    
    def __swap_back(self):
        self.new_statevector=copy.deepcopy(self.statevector)
        for i in range(len(self.statevector)):
            #new_statevector[swap_vector[i]]=statevector[i]
            self.new_statevector[i]=self.statevector[self.swap_vector[i]]
        self.statevector=copy.deepcopy(self.new_statevector)    
    def execute_2bit_gate(self,type_gate,a,b):
        self.__bring_2_lines_to_top(a,b)
        self.__determine_swap_vector()                
        self.__swap_bits()
        #print_statevector()
        self.gatelist_local =[type_gate]
        while (len (self.gatelist_local))<(self.amount_of_bits-1):
            self.gatelist_local.append('I')
        self.execute_gates(self.gatelist_local)
        # do calculation
        #print_statevector()
        self.__swap_back()    
    def execute_3bit_gate(self,type_gate,a,b,c):
        self.__bring_3_lines_to_top(a,b,c)
        self.__determine_swap_vector()                
        self.__swap_bits()
        #print_statevector()
        self.gatelist_local =[type_gate]
        while (len (self.gatelist_local))<(self.amount_of_bits-2):
            self.gatelist_local.append('I')
        self.execute_gates(self.gatelist_local)
        #print_statevector()
        # do calculation
        self.__swap_back()    
    def determine_entanglement(self):
        print (self.W+'============= Determine Entanglement ============')
        for i in range (self.amount_of_bits):
            for j in range (i):
                if i==j :
                    pass
                else:
                    s00=0
                    s11=0
                    s10=0
                    s01=0
                    for k in range (len(self.statevector)):
                        if (k&2**i)>0 and (k&2**j)>0:
                            s11=s11+self.statevector[k]
                        if (k&2**i)<1 and (k&2**j)>0:
                            s01=s01+self.statevector[k]
                        if (k&2**i)>0 and (k&2**j)<1:
                            s10=s10+self.statevector[k]
                        if (k&2**i)<1 and (k&2**j)<1:
                            s00=s00+self.statevector[k]
                    if (2*abs(s00*s11-s01*s10))>0.01:
                        entang=str(2*abs(s00*s11-s01*s10))
                    else:
                        entang='0.0'
                    print (self.amount_of_bits-i-1,self.amount_of_bits-j-1, ' -> ',entang[0:4])    
    def execute_global_gatelist(self,*argument):
        print (self.W+"============= Execute Global Gate list ==========")
        sp=self.__convert_statevector_to_bits()
        graph=False
        if len(argument)>0:
            if (argument[0]=='g'):
                graph=True
                graphtel=1
        for i in range (self.amount_of_bits):
            if sp[i*2]>0.95:
                self.start_print[i]='0 '
            elif sp[i*2+1]>0.95:
                self.start_print[i]='1 '
            else:
                self.start_print[i]='? '         
        for gloli in self.global_gatelist:
            if (gloli[0] in two_bit_gates) or (gloli[0]in three_bit_gates):
                if gloli[0] in two_bit_gates :
                    self.execute_2bit_gate(gloli[0],gloli[1],gloli[2])
                if gloli[0] in three_bit_gates :
                    self.execute_3bit_gate(gloli[0],gloli[1],gloli[2],gloli[3])
            else:
                self.execute_gates(gloli)
            if graph:
                self.show_global_gatelist_graphical(graphtel)
                graphtel=graphtel+1
            #print_statevector()
        sp=self.__convert_statevector_to_bits()
        for i in range (self.amount_of_bits):
            if sp[i*2]>0.95:
                self.end_print[i]=' 0'
            elif sp[i*2+1]>0.95:
                self.end_print[i]=' 1'
            else:
                self.end_print[i]=' ?'         
        if len(argument)>0:
            if (argument[0]=='s') or (argument[0]=='show'):
                self.show_global_gatelist()
        self.start_print = ['' for x in range(self.amount_of_bits)]
        self.end_print = ['' for x in range(self.amount_of_bits)]
        print()    
    def set_bits(self,a):
        if len(a)==self.amount_of_bits:
            sum=0
            for b in a:
                if b=='1':
                    sum=2*sum+1
                else:
                    sum=2*sum+0
            for i in range(len(self.statevector)):
                self.statevector[i]=0                
            self.statevector[sum]=1                
        else:
            print(self.R+'error: set_bits has not the right amount of bits')
            print('we need ',self.amount_of_bits,', you gave ',len(a))    
    def __convert_statevector_to_bits(self):
        bits = [0 for x in range(2*self.amount_of_bits)]
        for i in range(len(self.statevector)):
            for j in range (self.amount_of_bits):
                if i & 2**(self.amount_of_bits-j-1) ==0:
                    bits[2*j]=bits[2*j]+abs(self.statevector[i])**2
                else:
                    bits[2*j+1]=bits[2*j+1]+abs(self.statevector[i])**2
        return bits    
    
    def show_global_gatelist_graphical(self,*argument):
        plt.figure(figsize=(20,11),dpi=100)
        plt.xlim([0, 200])
        plt.ylim([0, 110])
        if len(argument)>0:
            showtill=argument[0]
        else:
            showtill=len(self.global_gatelist)
        for j in range (showtill):
            if self.global_gatelist[j][0] in two_bit_gates or self.global_gatelist[j][0] in three_bit_gates :
                if self.global_gatelist[j][0] in two_bit_gates:
                    if self.global_gatelist[j][0]=='c_not':
                        for i in range (self.amount_of_bits):
                            plt.arrow( 6*j,105-i*10,6,0,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                        s=self.global_gatelist[j][1]
                        e=self.global_gatelist[j][2]
                        plt.arrow(3+6*j,105-s*10,0,(s-e)*10,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                        thefont.normalize_rendering(200)
                        for (x1, y1), (x2, y2) in thefont.lines_for_text('.'):
                                plt.arrow((x1)/10+0.3+6*j,(y1)/10+97-s*10,(x2-x1)/10,(y2-y1)/10,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                        thefont.normalize_rendering(100)
                        for (x1, y1), (x2, y2) in thefont.lines_for_text('o'):
                                plt.arrow((x1)/10+6*j,(y1)/10+100-e*10,(x2-x1)/10,(y2-y1)/10,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                    if self.global_gatelist[j][0]=='c_Z':
                        s=self.global_gatelist[j][1]
                        e=self.global_gatelist[j][2]
                        for i in range (self.amount_of_bits):
                            if i==e:
                                pass
                            else:
                                plt.arrow( 6*j,105-i*10,6,0,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                        plt.arrow(3+6*j,105-s*10,0,(s-e)*10,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                        thefont.normalize_rendering(200)
                        for (x1, y1), (x2, y2) in thefont.lines_for_text('.'):
                                plt.arrow((x1)/10+0.3+6*j,(y1)/10+97-s*10,(x2-x1)/10,(y2-y1)/10,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                        thefont.normalize_rendering(40)
                        i=e
                        for (x1, y1), (x2, y2) in thefont.lines_for_text('Z'):
                                plt.arrow((x1)/10+2+6*j,(y1)/10+102-i*10,(x2-x1)/10,(y2-y1)/10,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                        plt.arrow(6*j,105-i*10,1,0,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                        plt.arrow(1+6*j,105-i*10-3,0,5,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                        plt.arrow(1+6*j,105-i*10-3,5,0,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                        plt.arrow(1+6*j,105-i*10+2,5,0,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                        plt.arrow(6+6*j,105-i*10-3,0,5,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)

                    if self.global_gatelist[j][0]=='swap':
                        s=self.global_gatelist[j][1]
                        e=self.global_gatelist[j][2]
                        for i in range (self.amount_of_bits):
                            if i==s or i==e:
                                pass
                            else:
                                plt.arrow( 6*j,105-i*10,6,0,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                        plt.arrow(6*j,105-s*10,1,0,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                        plt.arrow(6*j,105-e*10,1,0,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                        plt.arrow(5+6*j,105-s*10,1,0,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                        plt.arrow(5+6*j,105-e*10,1,0,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                        plt.arrow(1+6*j,105-s*10,4,(s-e)*10,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                        plt.arrow(1+6*j,105-e*10,4,(e-s)*10,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                if self.global_gatelist[j][0] in three_bit_gates:
                    if self.global_gatelist[j][0]=='cc_not':
                        for i in range (self.amount_of_bits):
                            plt.arrow( 6*j,105-i*10,6,0,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                        s=self.global_gatelist[j][1]
                        s2=self.global_gatelist[j][2]
                        e=self.global_gatelist[j][3]
                        plt.arrow(3+6*j,105-s*10,0,(s-e)*10,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                        thefont.normalize_rendering(200)
                        for (x1, y1), (x2, y2) in thefont.lines_for_text('.'):
                                plt.arrow((x1)/10+0.3+6*j,(y1)/10+97-s*10,(x2-x1)/10,(y2-y1)/10,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                        for (x1, y1), (x2, y2) in thefont.lines_for_text('.'):
                                plt.arrow((x1)/10+0.3+6*j,(y1)/10+97-s2*10,(x2-x1)/10,(y2-y1)/10,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                        thefont.normalize_rendering(100)
                        for (x1, y1), (x2, y2) in thefont.lines_for_text('o'):
                                plt.arrow((x1)/10+6*j,(y1)/10+100-e*10,(x2-x1)/10,(y2-y1)/10,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                                                    
            else:
                for i in range (self.amount_of_bits):
                    if self.global_gatelist[j][i]=='I':
                        plt.arrow( 6*j,105-i*10,6,0,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                    else: 
                        thefont.normalize_rendering(40)
                        for (x1, y1), (x2, y2) in thefont.lines_for_text(self.global_gatelist[j][i][0]):
                                plt.arrow((x1)/10+2+6*j,(y1)/10+102-i*10,(x2-x1)/10,(y2-y1)/10,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                        plt.arrow(6*j,105-i*10,1,0,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                        plt.arrow(1+6*j,105-i*10-3,0,5,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                        plt.arrow(1+6*j,105-i*10-3,5,0,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                        plt.arrow(1+6*j,105-i*10+2,5,0,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                        plt.arrow(6+6*j,105-i*10-3,0,5,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
        if len(argument)>0:
            posp=0
            for i in range (len(self.statevector)):
                thefont.normalize_rendering(40)
                s=self.statevector[i]
                stri='0000000000'+"{0:b}".format(i)
                if abs(s.real) <0.01 :
                    sreal='0.00'
                else:
                    sreal=(str((s.real))+'   ')[0:4]
                if abs(s.imag) <0.01 :
                    simag='0.00'
                else:
                    simag=(str((s.real))+'   ')[0:4]
                stri=sreal+' '+simag+'i |'+stri[-self.amount_of_bits:]+'>'
                if abs(s)>0.01:
                    for (x1, y1), (x2, y2) in thefont.lines_for_text(stri):
                        plt.arrow((x1)/10+2+6*(showtill+2),(y1)/10+102-posp*6,(x2-x1)/10,(y2-y1)/10,width=0.01,head_width=0.01, head_length=0.0,length_includes_head=True)
                    plt.arrow(30+2+6*(showtill+2)+self.amount_of_bits*3,104-posp*6,abs(s)**2*20.,0,width=4,head_width=0.01, head_length=0.0,length_includes_head=True)
                    posp=posp+1
        plt.axis('off')
        plt.savefig('@@@',dpi=100)

        plt.show()            
        return



    def show_global_gatelist(self):
        print()
        for j in range (self.amount_of_bits):
            print(self.start_print[j], end = '')
            for i in range(len(self.global_gatelist)):
                 print (u'\u2500', end = '')
                 if  (self.global_gatelist[i][0] in two_bit_gates) or (self.global_gatelist[i][0] in three_bit_gates):
                      if  self.global_gatelist[i][0] in two_bit_gates:
                        if self.global_gatelist[i][1]==j:
                            if self.global_gatelist[i][0]==swap :
                                if self.global_gatelist[i][1]> self.global_gatelist[i][2] :
                                    print (u'\u2518', end = '')
                                else:
                                    print (u'\u2510', end = '')
                            else:                            
                                print (u'\u2022', end = '')
                        elif self.global_gatelist[i][2]==j:
                            if self.global_gatelist[i][0]==swap :
                                if self.global_gatelist[i][1]< self.global_gatelist[i][2]: 
                                    print (u'\u2518', end = '')
                                else:
                                    print (u'\u2510', end = '')                                
                            elif self.global_gatelist[i][0]==c_Z :
                                print (u'\u2022', end = '')
                            else:                            
                             print (u'\u004F', end = '')
                        elif self.global_gatelist[i][2]>j and self.global_gatelist[i][1]<j:
                             print (u'\u253c', end = '')
                        elif self.global_gatelist[i][2]<j and self.global_gatelist[i][1]>j:
                             print (u'\u253c', end = '')
                        else:
                             print (u'\u2500', end = '')
                             
                      if  self.global_gatelist[i][0]in three_bit_gates :
                        if (self.global_gatelist[i][1]==j) or  (self.global_gatelist[i][2]==j) :
                             print (u'\u2022', end = '')
                        elif self.global_gatelist[i][3]==j:
                             print (u'\u004F', end = '')
                        elif self.global_gatelist[i][3]>j and self.global_gatelist[i][1]<j:
                             print (u'\u253c', end = '')
                        elif self.global_gatelist[i][3]<j and self.global_gatelist[i][1]>j:
                             print (u'\u253c', end = '')
                        else:
                            print (u'\u2500', end = '')
                 else:                
                    if self.global_gatelist[i][j]=='I':
                        print (u'\u2500', end = '')
                    else:
                        print (self.global_gatelist[i][j], end = '')
            print(self.end_print[j])    
    def qg(self,*arguments):
        if len(arguments)<3:
            print (self.R+'error: missing information in gate definition')
            print (arguments)
            return
        t=arguments[0]
        if type(t)==int :
            if t>(len(self.global_gatelist)-1):
                print (self.R+'error: the timestep is past the last step of you global_gatelist')
                print (arguments)
                return                
        else:
            print (self.R+'error: time step is not an integer')
            print (arguments)
            return
        gate_type=arguments[1]
        which_bit=arguments[2]
        if type(which_bit)==int :
            pass
        else:
            print (self.R+'error: bit designation is not an integer')
            print (arguments)
            return
        if which_bit>(self.amount_of_bits-1):
            print (self.R+'error: bit does not exist')
            print (arguments)
            return
        if gate_type in gates:
            pass
        else:
            print (self.R+'error: gate type does not exist')
            print (arguments)
            return
        if (gate_type in two_bit_gates) or (gate_type in three_bit_gates) :
            if len(set(self.global_gatelist[t]))>1 :
                print (self.R+'warning: you overwrite an existing gate on qubit')
                print (arguments)
                return            
            if gate_type in two_bit_gates:
                self.global_gatelist[t]=[gate_type]
                self.global_gatelist[t].append(which_bit)
                if len(arguments)<4:
                    print (self.R+'error: missing bit designation')
                    print (arguments)
                    return
                which_bit=arguments[3]
                if type(which_bit)==int :
                    pass
                else:
                    print (self.R+'error: bit designation is not an integer')
                    print (arguments)
                    return
                self.global_gatelist[t].append(which_bit)
            if gate_type in three_bit_gates:
                self.global_gatelist[t]=[gate_type]
                self.global_gatelist[t].append(which_bit)
                if len(arguments)<5:
                    print (self.R+'error: missing bit designation(s)')
                    print (arguments)
                    return
                which_bit=arguments[3]
                if type(which_bit)==int :
                    pass
                else:
                    print (self.R+'error: bit designation is not an integer')
                    print (arguments)
                    return
                self.global_gatelist[t].append(which_bit)
                which_bit=arguments[4]
                if type(which_bit)==int :
                    pass
                else:
                    print (self.R+'error: bit designation is not an integer')
                    print (arguments)
                    return
                self.global_gatelist[t].append(which_bit)
        else:
            if (self.global_gatelist[t][0] in two_bit_gates) or (self.global_gatelist[t][0] in three_bit_gates) :
                print (self.R+'error: a 2-bit or 3-bit gate is already present')
                print(arguments)
                return
            if self.global_gatelist[t][which_bit]=='I':
                self.global_gatelist[t][which_bit]=gate_type
            else:
                self.global_gatelist[t][which_bit]=gate_type
                print (self.R+'warning: you overwrite an existing gate on qubit:')
                print(arguments)
                return
def help():
    print('_____________________________________________________________')
    print('QCSIM')    
    print('Written by Bart Bozon.')    
    print()
    print('This module implements a simulation of a quantumcomputer in python')    
    print()
    print('qc=qcsim.create_quantum_computer(n,t)')   
    print('   creates a quantumcomputer object (qc) with n bits and t timeline')
    print('   if you ommit the t the computer has no global_gatelist.')
    print()
    print('qc.qg(t,X,n)')
    print('   creates a pauli-X gate on bit n at time t')
    print()
    print('qc.show_global_gatelist()')
    print('   shows the gates you have programmed')
    print()
    print('qc.set_bits(bitstring)')
    print('   set the bits according to your bitstring')
    print()
    print('qc.execute_global_gatelist()')
    print('   execute the program')
    print('   add the string show as argument to show the program')
    print()
    print('qc.measure_statevector()')
    print('   gives the probability a statevector is realized if measured')
    print('   the wave function is not really collapsed!')
    print()
    print('qc.print_statevector()')
    print('   shows the wavefunctions of the qubits')
    print()
    print('qc.determine_entanglement()')
    print('   calculates the entanglement of the qubits')
    print()
    print('qc.show_execution=False')
    print('   dis/enables logging output')
    print('_____________________________________________________________')
    print()
    
print ('\033[34m',end='')
print (' ██████╗  ██████╗    ███████╗██╗███╗   ███╗') 
print ('██╔═══██╗██╔════╝    ██╔════╝██║████╗ ████║') 
print ('██║   ██║██║         ███████╗██║██╔████╔██║')
print ('██║▄▄ ██║██║         ╚════██║██║██║╚██╔╝██║')
print ('╚██████╔╝╚██████╗    ███████║██║██║ ╚═╝ ██║')
print (' ╚══▀▀═╝  ╚═════╝    ╚══════╝╚═╝╚═╝     ╚═╝')
print ('\033[0m')
print ('module qcsim loaded.')
print ('designed by Bart Bozon')
print ('for best visual output, put font on consolas, size 15')
print ('qcsim.help() for help')
print ()