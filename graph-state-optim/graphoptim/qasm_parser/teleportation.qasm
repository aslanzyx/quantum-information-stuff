qreg q[3];
creg c[3];

h q[1];
h q[2];
cz q[1],q[2];
cz q[0],q[1];
h q[0];
h q[1];