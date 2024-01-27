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

'''

qc=qcsim.create_quantum_computer(3,6)  # create quantum computer with 4 bits & 6 timeslices

qc.qg(1,X,0)                     # add a not gate on timeslice 0 and bit 1 
qc.qg(1,H,1)                     # add a hadamard gate on timeslice 1 and bit 1 
qc.qg(3,c_not,1,2)               # add a c_not gate on timeslice 3 and bit 1 and 3

qc.show_execution=False          # set to true for logging info
qc.execute_global_gatelist('s')  # show the circuit & execute
qc.determine_entanglement()      # see which bits are entangled   
qc.print_statevector()

print ()
print ('In this simple example we show the behavior of different q-gates.')
print ('The X gate (on bit 0) simply flips the bit.')
print ('The H gate (on bit 1) brings the bit in superposition.')
print ('The c_not gate (on bit 1 and 2) flips bit 2 depending on bit 1.')
print ('As bit 1 is in superposition the two bits become entangled.')
print ('The value of the bits cannot be determined independly.')
print ('This is also reflected in the state vector.')
print ('We will have 50% chance of measuring both bits low and 50% of measuring both bits high.')
