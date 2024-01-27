'''
Leave the following as is. It imports the qc and defines certain constants.
The constants are not defined in the module as to facilitate using X iso qcsim.X

'''
import qcsim

# 1- bit operators
I='I'
X='X'
Y='Y'
Z='Z'
S='S'
T='T'
H='H'

# 2- bit operators
c_not='c_not'
c_Z='c_Z'
swap='swap'

# 3- bit operators
cc_not='cc_not'

'''
Now you can change whatever you want!!

There are different ways to interface with the qc-sim. The 1st way is by doing indivual gate actions.

'''
       

# let's first start a computer with 3 bits
qc=qcsim.create_quantum_computer(3)

# the computer creates a gatelist and a statevector. Let's print it out:
print ('gatelist:',qc.gatelist)
# as you can see it is filled with unitary gates

print ('statevector:',qc.statevector)

# The statevector can also displayed differently.:
qc.print_statevector()

# let's put the state in 
qc.statevector[0]=1
# this means all qubits are equal to zero!
# let's put a not gate on bit 0:
    
qc.gatelist [0]=X

# let's execute the gatelist:
    
qc.execute_gates(qc.gatelist)

# for ccnot and ccnot gates we need a different method:
qc.execute_2bit_gate(c_not,0,2)

# we can also determine the entanglement:
qc.determine_entanglement()

# no entanglement!
# let's put bit 1 in superposition with a Hadamard gate:

qc.gatelist [0]=H

# execute: 
qc.execute_gates(qc.gatelist)

# and a cnot!
qc.execute_2bit_gate(c_not,0,2)

# Now we have entanglement!
qc.determine_entanglement()

print ('press return!')
wait_for_user_to_press=input()

"""
We can also create a quantumcomputer with a real program (instead of individual gate actions)!

"""
# for this we start the computer differently (the second number is the "timeline". How many gates do you want to program?)

qc=qcsim.create_quantum_computer(4,6)

# the command for adding a gate to our "timeline" is very simple:
    
qc.qg(0,X,0)

# now we have added a not gate at time 0 (1st param) and bit 0 (last param)

qc.qg(0,X,1)

# we can add a second not gate in the same timestep (but for a different bit)

# we can have a look at our "program"
print (qc.global_gatelist)

# But an easier way is:
qc.show_global_gatelist()

# let's add some gates
qc.qg(2,c_not,0,2)
qc.qg(3,c_not,1,2)
qc.qg(4,cc_not,0,1,3)
# please note! only 1 c_not or cc_not is allowed per timestep!

# Let's look at the total program:
qc.show_global_gatelist()

print ('press return!')
wait_for_user_to_press=input()


# we can execute the program   
# the following flag disables the logging info
qc.show_execution=False
qc.execute_global_gatelist()

wait_for_user_to_press=input()

# let's look at the result:
qc.print_statevector()
# please note: bit 2 is xor bit 0 and 1
#  bit 3 is and of bit 0 and 1!

# this simple scenario shows the working of a classical computer (xor and and gate)

qc.set_bits('0000')
qc.execute_global_gatelist('s')

qc.set_bits('1000')
qc.execute_global_gatelist('s')

qc.set_bits('0100')
qc.execute_global_gatelist('s')

qc.set_bits('1100')
qc.execute_global_gatelist('s')
qc.measure_statevector()

print ('press return!')
wait_for_user_to_press=input()

# but with a Hadamard gate it becomes QM!!!
qc.qg(0,H,0)
qc.set_bits('1100')
qc.execute_global_gatelist('s')
qc.determine_entanglement()
qc.measure_statevector()

# We can also use graphical output 
qc.show_global_gatelist_graphical()

print ('press return!')
wait_for_user_to_press=input()
qc.measure_statevector_graphical()