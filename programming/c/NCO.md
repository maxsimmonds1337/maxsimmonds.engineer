# The Numerically Controlled Oscillator

Recently, I came across the need to generate a sine wave with variable frequency and amplitude. My first "go to method!" was a look up table, or LUT. The LUT didn't feel right, the code was long and messy. For each discrete amplitude change, I had another LUT (which I admit, I should have been able to do some math to fix that but when trying to get it to work, it was clipping and all sorts). Any way, here's the LUTs:

```C

//amplitude reduces in increments of 20%

unsigned int sine_full_5[1024] = {70,70,70,71,71,72,72,72,73,73,74,74,75,75,75,76,76,77,77,78,78,78,79,79,80,80,81,81,81,82,82,83,83,83,84,84,85,85,86,86,86,87,87,88,88,88,89,89,90,90,90,91,91,92,92,93,93,93,94,94,95,95,95,96,96,96,97,97,98,98,98,99,99,100,100,100,101,101,102,102,102,103,103,103,104,104,104,105,105,106,106,106,107,107,107,108,108,108,109,109,110,110,110,111,111,111,112,112,112,113,113,113,114,114,114,115,115,115,116,116,116,116,117,117,117,118,118,118,119,119,119,120,120,120,120,121,121,121,122,122,122,122,123,123,123,123,124,124,124,125,125,125,125,126,126,126,126,127,127,127,127,128,128,128,128,128,129,129,129,129,130,130,130,130,130,131,131,131,131,131,132,132,132,132,132,133,133,133,133,133,133,134,134,134,134,134,134,134,135,135,135,135,135,135,135,136,136,136,136,136,136,136,136,137,137,137,137,137,137,137,137,137,137,138,138,138,138,138,138,138,138,138,138,138,138,138,138,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,139,138,138,138,138,138,138,138,138,138,138,138,138,138,138,137,137,137,137,137,137,137,137,137,137,136,136,136,136,136,136,136,136,135,135,135,135,135,135,135,134,134,134,134,134,134,134,133,133,133,133,133,133,132,132,132,132,132,131,131,131,131,131,130,130,130,130,130,129,129,129,129,128,128,128,128,128,127,127,127,127,126,126,126,126,125,125,125,125,124,124,124,123,123,123,123,122,122,122,122,121,121,121,120,120,120,120,119,119,119,118,118,118,117,117,117,116,116,116,116,115,115,115,114,114,114,113,113,113,112,112,112,111,111,111,110,110,110,109,109,108,108,108,107,107,107,106,106,106,105,105,104,104,104,103,103,103,102,102,102,101,101,100,100,100,99,99,98,98,98,97,97,96,96,96,95,95,95,94,94,93,93,93,92,92,91,91,90,90,90,89,89,88,88,88,87,87,86,86,86,85,85,84,84,83,83,83,82,82,81,81,81,80,80,79,79,78,78,78,77,77,76,76,75,75,75,74,74,73,73,72,72,72,71,71,70,70,70,69,69,68,68,67,67,67,66,66,65,65,64,64,64,63,63,62,62,61,61,61,60,60,59,59,58,58,58,57,57,56,56,56,55,55,54,54,53,53,53,52,52,51,51,51,50,50,49,49,49,48,48,47,47,46,46,46,45,45,44,44,44,43,43,43,42,42,41,41,41,40,40,39,39,39,38,38,37,37,37,36,36,36,35,35,35,34,34,33,33,33,32,32,32,31,31,31,30,30,29,29,29,28,28,28,27,27,27,26,26,26,25,25,25,24,24,24,23,23,23,23,22,22,22,21,21,21,20,20,20,19,19,19,19,18,18,18,17,17,17,17,16,16,16,16,15,15,15,14,14,14,14,13,13,13,13,12,12,12,12,11,11,11,11,11,10,10,10,10,9,9,9,9,9,8,8,8,8,8,7,7,7,7,7,6,6,6,6,6,6,5,5,5,5,5,5,5,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,5,5,5,5,5,5,5,6,6,6,6,6,6,7,7,7,7,7,8,8,8,8,8,9,9,9,9,9,10,10,10,10,11,11,11,11,11,12,12,12,12,13,13,13,13,14,14,14,14,15,15,15,16,16,16,16,17,17,17,17,18,18,18,19,19,19,19,20,20,20,21,21,21,22,22,22,23,23,23,23,24,24,24,25,25,25,26,26,26,27,27,27,28,28,28,29,29,29,30,30,31,31,31,32,32,32,33,33,33,34,34,35,35,35,36,36,36,37,37,37,38,38,39,39,39,40,40,41,41,41,42,42,43,43,43,44,44,44,45,45,46,46,46,47,47,48,48,49,49,49,50,50,51,51,51,52,52,53,53,53,54,54,55,55,56,56,56,57,57,58,58,58,59,59,60,60,61,61,61,62,62,63,63,64,64,64,65,65,66,66,67,67,67,68,68,69,69};

unsigned int sine_full_4[1024] = {54,54,54,54,55,55,55,56,56,56,57,57,57,58,58,58,59,59,59,60,60,60,61,61,61,62,62,62,63,63,63,64,64,64,65,65,65,66,66,66,66,67,67,67,68,68,68,69,69,69,70,70,70,71,71,71,72,72,72,72,73,73,73,74,74,74,75,75,75,75,76,76,76,77,77,77,78,78,78,78,79,79,79,80,80,80,80,81,81,81,82,82,82,82,83,83,83,83,84,84,84,85,85,85,85,86,86,86,86,87,87,87,87,88,88,88,88,89,89,89,89,90,90,90,90,91,91,91,91,92,92,92,92,92,93,93,93,93,94,94,94,94,94,95,95,95,95,95,96,96,96,96,96,97,97,97,97,97,98,98,98,98,98,99,99,99,99,99,99,100,100,100,100,100,100,101,101,101,101,101,101,101,102,102,102,102,102,102,102,103,103,103,103,103,103,103,103,104,104,104,104,104,104,104,104,104,105,105,105,105,105,105,105,105,105,105,105,105,106,106,106,106,106,106,106,106,106,106,106,106,106,106,106,106,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,106,106,106,106,106,106,106,106,106,106,106,106,106,106,106,106,105,105,105,105,105,105,105,105,105,105,105,105,104,104,104,104,104,104,104,104,104,103,103,103,103,103,103,103,103,102,102,102,102,102,102,102,101,101,101,101,101,101,101,100,100,100,100,100,100,99,99,99,99,99,99,98,98,98,98,98,97,97,97,97,97,96,96,96,96,96,95,95,95,95,95,94,94,94,94,94,93,93,93,93,92,92,92,92,92,91,91,91,91,90,90,90,90,89,89,89,89,88,88,88,88,87,87,87,87,86,86,86,86,85,85,85,85,84,84,84,83,83,83,83,82,82,82,82,81,81,81,80,80,80,80,79,79,79,78,78,78,78,77,77,77,76,76,76,75,75,75,75,74,74,74,73,73,73,72,72,72,72,71,71,71,70,70,70,69,69,69,68,68,68,67,67,67,66,66,66,66,65,65,65,64,64,64,63,63,63,62,62,62,61,61,61,60,60,60,59,59,59,58,58,58,57,57,57,56,56,56,55,55,55,54,54,54,54,53,53,53,52,52,52,51,51,51,50,50,50,49,49,49,48,48,48,47,47,47,46,46,46,45,45,45,44,44,44,43,43,43,42,42,42,41,41,41,41,40,40,40,39,39,39,38,38,38,37,37,37,36,36,36,35,35,35,35,34,34,34,33,33,33,32,32,32,32,31,31,31,30,30,30,29,29,29,29,28,28,28,27,27,27,27,26,26,26,25,25,25,25,24,24,24,24,23,23,23,22,22,22,22,21,21,21,21,20,20,20,20,19,19,19,19,18,18,18,18,17,17,17,17,16,16,16,16,15,15,15,15,15,14,14,14,14,13,13,13,13,13,12,12,12,12,12,11,11,11,11,11,10,10,10,10,10,9,9,9,9,9,8,8,8,8,8,8,7,7,7,7,7,7,6,6,6,6,6,6,6,5,5,5,5,5,5,5,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,6,6,6,6,6,6,6,7,7,7,7,7,7,8,8,8,8,8,8,9,9,9,9,9,10,10,10,10,10,11,11,11,11,11,12,12,12,12,12,13,13,13,13,13,14,14,14,14,15,15,15,15,15,16,16,16,16,17,17,17,17,18,18,18,18,19,19,19,19,20,20,20,20,21,21,21,21,22,22,22,22,23,23,23,24,24,24,24,25,25,25,25,26,26,26,27,27,27,27,28,28,28,29,29,29,29,30,30,30,31,31,31,32,32,32,32,33,33,33,34,34,34,35,35,35,35,36,36,36,37,37,37,38,38,38,39,39,39,40,40,40,41,41,41,41,42,42,42,43,43,43,44,44,44,45,45,45,46,46,46,47,47,47,48,48,48,49,49,49,50,50,50,51,51,51,52,52,52,53,53,53};

unsigned int sine_full_3[1024] = {38,38,38,39,39,39,39,40,40,40,40,41,41,41,41,41,42,42,42,42,43,43,43,43,44,44,44,44,44,45,45,45,45,46,46,46,46,47,47,47,47,47,48,48,48,48,49,49,49,49,49,50,50,50,50,51,51,51,51,51,52,52,52,52,53,53,53,53,53,54,54,54,54,54,55,55,55,55,56,56,56,56,56,57,57,57,57,57,58,58,58,58,58,59,59,59,59,59,59,60,60,60,60,60,61,61,61,61,61,62,62,62,62,62,62,63,63,63,63,63,64,64,64,64,64,64,65,65,65,65,65,65,66,66,66,66,66,66,66,67,67,67,67,67,67,68,68,68,68,68,68,68,69,69,69,69,69,69,69,69,70,70,70,70,70,70,70,70,71,71,71,71,71,71,71,71,72,72,72,72,72,72,72,72,72,72,73,73,73,73,73,73,73,73,73,73,73,74,74,74,74,74,74,74,74,74,74,74,74,74,74,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,74,74,74,74,74,74,74,74,74,74,74,74,74,74,73,73,73,73,73,73,73,73,73,73,73,72,72,72,72,72,72,72,72,72,72,71,71,71,71,71,71,71,71,70,70,70,70,70,70,70,70,69,69,69,69,69,69,69,69,68,68,68,68,68,68,68,67,67,67,67,67,67,66,66,66,66,66,66,66,65,65,65,65,65,65,64,64,64,64,64,64,63,63,63,63,63,62,62,62,62,62,62,61,61,61,61,61,60,60,60,60,60,59,59,59,59,59,59,58,58,58,58,58,57,57,57,57,57,56,56,56,56,56,55,55,55,55,54,54,54,54,54,53,53,53,53,53,52,52,52,52,51,51,51,51,51,50,50,50,50,49,49,49,49,49,48,48,48,48,47,47,47,47,47,46,46,46,46,45,45,45,45,44,44,44,44,44,43,43,43,43,42,42,42,42,41,41,41,41,41,40,40,40,40,39,39,39,39,38,38,38,38,38,37,37,37,37,36,36,36,36,35,35,35,35,35,34,34,34,34,33,33,33,33,32,32,32,32,32,31,31,31,31,30,30,30,30,29,29,29,29,29,28,28,28,28,27,27,27,27,27,26,26,26,26,25,25,25,25,25,24,24,24,24,23,23,23,23,23,22,22,22,22,22,21,21,21,21,20,20,20,20,20,19,19,19,19,19,18,18,18,18,18,17,17,17,17,17,17,16,16,16,16,16,15,15,15,15,15,14,14,14,14,14,14,13,13,13,13,13,12,12,12,12,12,12,11,11,11,11,11,11,10,10,10,10,10,10,10,9,9,9,9,9,9,8,8,8,8,8,8,8,7,7,7,7,7,7,7,7,6,6,6,6,6,6,6,6,5,5,5,5,5,5,5,5,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,9,9,9,9,9,9,10,10,10,10,10,10,10,11,11,11,11,11,11,12,12,12,12,12,12,13,13,13,13,13,14,14,14,14,14,14,15,15,15,15,15,16,16,16,16,16,17,17,17,17,17,17,18,18,18,18,18,19,19,19,19,19,20,20,20,20,20,21,21,21,21,22,22,22,22,22,23,23,23,23,23,24,24,24,24,25,25,25,25,25,26,26,26,26,27,27,27,27,27,28,28,28,28,29,29,29,29,29,30,30,30,30,31,31,31,31,32,32,32,32,32,33,33,33,33,34,34,34,34,35,35,35,35,35,36,36,36,36,37,37,37,37,38,38};

unsigned int sine_full_2[1024] = {22,22,22,22,23,23,23,23,23,23,23,23,24,24,24,24,24,24,24,25,25,25,25,25,25,25,25,26,26,26,26,26,26,26,27,27,27,27,27,27,27,27,28,28,28,28,28,28,28,29,29,29,29,29,29,29,29,30,30,30,30,30,30,30,30,31,31,31,31,31,31,31,31,32,32,32,32,32,32,32,32,32,33,33,33,33,33,33,33,33,34,34,34,34,34,34,34,34,34,35,35,35,35,35,35,35,35,35,36,36,36,36,36,36,36,36,36,36,37,37,37,37,37,37,37,37,37,37,38,38,38,38,38,38,38,38,38,38,38,39,39,39,39,39,39,39,39,39,39,39,40,40,40,40,40,40,40,40,40,40,40,40,40,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,44,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,40,40,40,40,40,40,40,40,40,40,40,40,40,39,39,39,39,39,39,39,39,39,39,39,38,38,38,38,38,38,38,38,38,38,38,37,37,37,37,37,37,37,37,37,37,36,36,36,36,36,36,36,36,36,36,35,35,35,35,35,35,35,35,35,34,34,34,34,34,34,34,34,34,33,33,33,33,33,33,33,33,32,32,32,32,32,32,32,32,32,31,31,31,31,31,31,31,31,30,30,30,30,30,30,30,30,29,29,29,29,29,29,29,29,28,28,28,28,28,28,28,27,27,27,27,27,27,27,27,26,26,26,26,26,26,26,25,25,25,25,25,25,25,25,24,24,24,24,24,24,24,23,23,23,23,23,23,23,23,22,22,22,22,22,22,22,21,21,21,21,21,21,21,21,20,20,20,20,20,20,20,19,19,19,19,19,19,19,19,18,18,18,18,18,18,18,17,17,17,17,17,17,17,17,16,16,16,16,16,16,16,15,15,15,15,15,15,15,15,14,14,14,14,14,14,14,14,13,13,13,13,13,13,13,13,12,12,12,12,12,12,12,12,12,11,11,11,11,11,11,11,11,10,10,10,10,10,10,10,10,10,9,9,9,9,9,9,9,9,9,8,8,8,8,8,8,8,8,8,8,7,7,7,7,7,7,7,7,7,7,6,6,6,6,6,6,6,6,6,6,6,5,5,5,5,5,5,5,5,5,5,5,4,4,4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,6,6,6,7,7,7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8,8,8,9,9,9,9,9,9,9,9,9,10,10,10,10,10,10,10,10,10,11,11,11,11,11,11,11,11,12,12,12,12,12,12,12,12,12,13,13,13,13,13,13,13,13,14,14,14,14,14,14,14,14,15,15,15,15,15,15,15,15,16,16,16,16,16,16,16,17,17,17,17,17,17,17,17,18,18,18,18,18,18,18,19,19,19,19,19,19,19,19,20,20,20,20,20,20,20,21,21,21,21,21,21,21,21,22,22,22};

unsigned int sine_full_1[1024] = {6,6,6,6,6,6,6,6,6,6,6,6,6,6,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,6,6,6,6,6};

```

As you can see, for decent resolution, the length of the LUT get's quite high. Having to have several for different amplitudes is also not great, though, as mentioned, I think that could be changed. Another thing that could be changed to slightly increased coding complexity would be a quarter wave LUT. Since a sine wave is periodic, that is, it repeates, you can utilise this to your advantage. You could repeate every $$ \frac{\pi}}{4} $$ , so long as you initally go through the LUT from the 0th element, up to n, and then go from the nth element down to the 0th, and repeate again, but with negative outputs. This isn't uncommon for applications that are short of memory. Another interesting point is that you can use the same LUT for waves with different phase shifts, by simply having another pointer to the LUT. If you wanted it to be 180 degress out, then you'd place the other pointer in the middle of the LUT. Of course, this phase shift if limited by the length of the LUT. If you only had 4 points, you'd have one coarse sinewave, and only be able to have a minimum phase shift of 90 degrees!

However, given I hadn't done an NCO before, and the fact that it would be easier to adjust the frequency on the fly, along with the peak to peak amplitude, I went with the NCO!

## Theory

To outline how and why this works, let's breakdown the theory. First, we need to understand a little bit about what a phasor is (though, I'm sure you remember from old math lessons!)

![image](https://user-images.githubusercontent.com/58208872/185100570-939f1f9f-1f90-47bf-a2f4-2cfbf1e0fdc3.png)

The above image shows a phasor of length 1, on what we shall call the complex plane. The x direction are real numbers, and the y are "imaginary". While this may seem a little abstract, it's useful for a whole number of applications, including phasors!

You may have noticed the phasor pointing in a different direction. This is said to have rotated by 90 degrees. In the complex plane, we can say we have multiplied by "i". The explanation for this is as follows. Imagine we have a phasor in the complex plane, x+iy. If x was 1, and y was 0, we would have the graph plotted in the first sequence above. Now, if we are to multiply by 'i' (which has been defined as the square root of minus 1) then we get:

$$ i(x + i \cdot y ) = i \cdot x + i^2 \cdot y $$

We know that:

$$ i = \sqrt-1 $$

$$ i^2 = -1 $$

So, finally, we get:

$$ x \cdot i - y$$

This has the affect of _rotating_ a phasor. This is more apparent if we assign values to x and y. Let's say that x is initally 1, and y is 0.:

$$ phasor_1 = 1 + i \cdot 0  = 1 $$

This is plotted on the graph below:

![Plotted with graphPlotter!](/programming/python/images/db4d17ec23c011ed80eac821587c6744.png)

If we now multiply by 'i', we get:

$$ phasor_2 = i(1 + 0i) = 0 + i$$

This, plotted on a graph, looks like the following:

![Plotted with graphPlotter!](/programming/python/images/2a88c8be23c211ed80eac821587c6744.png)
If we did this one more time, multiply by i, we rotate again:

$$ phasor_3= i(0 + i) = 0 + i^2 = -1$$

We know it's -1 from the math outlined a bit futher up. We can then plot this on a graph too:

![Plotted with graphPlotter!](/programming/python/images/391276ac246011edbb64c821587c6744.png)

So we can now understand how, with complex numbers, we are able to rotate phasors. If we now plot these on a time series graph, that is, after each rotation we plot either it's y (imaginary) or x (real) component against time we can start to see how to get a sinewave output. Let's plot the imaginary component of the above graphs on a time series graph:

![Plotted with graphPlotter! cmd = .. x 0 1 2 3 4 y 1 0 -1 0 1 t Imaginary vs Time](/programming/python/images/5f5de49e252e11edbb64c821587c6744.png)

It's doesn't yet look sinusoildal, mainly because we are simply jumping from quadrant to quadrant. If we were to add more data points, we might see something interesting come about:

```graphPlotter
.. x 0 1 2 3 4 5 6 7 8 9 10 11 12 y 0.5	0.866 1 0.866 0.5 0 -0.5 -0.866 -1 -0.866 -0.5 0 t Imaginary Vs Time
```

Now we're getting somewhere! This is indeed looking like a sine wave, but why, we might ask ourselves? Well, that comes down to some triginometry! If we want to get the y values (imaginary) of each phasor, we can use trignometery, since the phasor makes a right angled triangle with the axes:


We can say, then , that if the length of this phasor is simply 1, because we're on the "unit circle", then:

$$ sin(\theta) = \frac{O}{H} $$

The "H", or hypotenus, in this case is 1 (it's a phasor of length 1), and "O", is the y value that we want, so this equation becomes:

$$ 1 \cdot sin(\theta) = y $$

If we plot this for each value of theta as we progress around the circle, we get the graph above, nice!

Linking this together, we know that we can multiply phasors to give a rotation, we know that as we go around the unit cicle in the complex domain, that's the same as a sine wave in the time domain. The last couple of peices to this puzzle are, how do we know what phasor we should multiply by each time, and how often should we do it!?

### Choosing the Phasor
## C code

The code for implimenting the NCO is quite simple, and so I will show it all below:

```C
#include "NCO.h"		// contains the structs and variable definitions


// function to compute the 32 bit complex multiplication
T_COMPLEX32 Complex_MUT(T_COMPLEX32 a, T_COMPLEX32 b) {
	T_COMPLEX32 result;

	T_INT64 ar = (T_INT64) a.real;	// declare a variable that's 64 bits long, from the real component of a.
	T_INT64 ai = (T_INT64) a.imag;	// declare a variable that's 64 bits long, from the real component of a.
	T_INT64 br = (T_INT64) b.real;	// declare a variable that's 64 bits long, from the real component of a.
	T_INT64 bi = (T_INT64) b.imag;	// declare a variable that's 64 bits long, from the real component of a.
 
	T_INT64 cr = ar*br - ai*bi;	// compute the real component
	T_INT64 ci = ar*bi + ai*br;	// compute the imag component
 
//	T_INT64 cr = ar*br - ai*bi;	// compute the real component
//	T_INT64 ci = ar*bi - ai*br;	// compute the imag component

	result.real = (T_INT32) (cr >> 31);	// truncate the 64 bit value to a 32 bit, and typedef it
	result.imag = (T_INT32) (ci >> 31);	// truncate the 64 bit value to a 32 bit, and typedef it

	return result;
}
```

### NCO

In essence, it is a complex multiplication of the old phasor, with the constant "phasor advance". This is the phasor that rotates the current phasor by a given amount, and affects it's frequency and amplitude. This function is called in an ISR (interupt service routine) that is set to trigger every 100KHz:

```C
//interrupt service routine for the timer
void TIM3_IRQHandler(void) {

	GPIOA->ODR |= GPIO_ODR_OD10;
	
	signed long tmp,phasor_scaled = 0;
	int offset = 0;	

	phasor = Complex_MUT(phasor, PHASE_ADVANCE_1000);	// perform the complex MUT

	// // this should stop the amplitude decay
	// if(counter >= 1000) {
	// 	counter = 0;
	// 	T_COMPLEX32 phasor = {.real = -2147483647, .imag = 0}; // reset the phasor, to stop drifting
	// } else {
	// 	counter++; //inc counter
	// }

	// check to see if we have looped the number of times we want to rate limit
	if(loopCounter >= loopCounterMax) {

		// check to see if there has been a change in setpoint, if not, then no need to rate limit
		if(pwmGainCurrent != pwmGainSetPoint) pwmGainCurrent = rateLimiter(pwmGainCurrent, pwmGainSetPoint, pwmRateLimit);

		if(freqCurrent != freqSetPoint) freqCurrent = rateLimiter(freqCurrent, freqSetPoint, freqRateLimit);
		
		loopCounter = 0; // reset the loop counter
	} else {
		// if we're not ready to update the rate, leave as is and inc counter
		loopCounter++;
	}

	phasor_scaled = (phasor.real / 100) *  pwmGainCurrent; // scale the phasor, by the current gain

	tmp =(((phasor_scaled)>>9)*500>>23); // we then need to scale the 2^31 val to a number betwee 0 and 500 (the auto reload reg)
	offset = (((PHASE_ADVANCE_1000.real)>>9)*500>>23); // this adds the DC offset, since we need to be centered about 1.65V
	DC = (int)tmp+ (offset); // add the DC offset to the AC signal

	int freqChange = freqCurrent % 100; // get the change from 100
	
	if( (freqCurrent-100) < 0) {
		TIM3->ARR = 100 + (100-freqChange); // I will fix this later to convert to frequency
	} else if ((freqCurrent-100) > 0) {
		TIM3->ARR = 100-freqChange; // I will fix this later to convert to frequency
	} else {
		TIM3->ARR = 100; // otherwise, it must be 100, so set it.
	}

	TIM1->CCR1 = (DC); //update the capture control register with the phasor
	TIM3->SR = 0;		// clear the status reg

	GPIOA->ODR &= ~(GPIO_ODR_OD10);

}
```

Line 9 shows the function call. 

### Rate Limiter

The code below then impliments a rate limiter. This could have been written better, and not use a loop counter (rather, another timer interrupt), but it works. It limits the rate of the frequency changes (IE, if someone wants to go from 100Hz to 150Hz, it doesn't do this in one go, or that might damage the cryo-cooler), as well as the amplitude of the signal, for the same reason. 

There is some initial checking of the of the set point versus the current value, to see if there is a need to call the "rateLimiter" function. If the set point is different to the current value, then we may need to coerce the value before updating the register that handles the frequency or amplitude.

```C
int rateLimiter(int current, int setPoint, int rateLimit) {
	// if current != set point

	// check against limit
	//if negative
	// if positive
	// else

	// if rate limit is less that the current gain minus set point, then ...
	// ... we want to increase the gain, but limitied by the rate ...
	// ... we change the current value only (which is used to affect the pwm) and the user changes the desired set point
	if(rateLimit < (current - setPoint)) {
		current -= rateLimit;
	} else if(rateLimit > (current - setPoint)) { // if it's greater, then we need to reduce by rateLimit
		current += rateLimit;
	} else { // if we're within the rateLimit setting, just set to the desired set point
		current = setPoint;		
	}

	return current; // send it back to the caller
}
```

The above code is found in [my STM32 drivers repo](https://github.com/maxsimmonds1337/SSC/blob/main/Drivers/Simmo/SSC.c) (at some point, I'll make this library a submodule, and that can be included into my projects). This contains many helper functions that were used on a project, including setting the frequency (which, of course, then results in the calling of the rateLimiter function), setting the amplitude, requesting the frequency and amplitude, setting the rate limiters, and a few others.

The rateLimiter function essentially checks the direction of the change (IE, is the user requesting to go from 100Hz to 80, a negative direction, or are they requesting to go to 120Hz, a positive change). At the same time, it checks to see if the requested change is larger than a variable called "rateLimit". This is set by the user, and allows you to adjust how fast changes happen. If the change in set point is larger than this value, it's coerced to change only by this much. Finally, it returns the new value.

### Scaling

Since the NCO is using 32 bit integers for the multiplication (in an attempt to reduce rounding errors as much as possible) and the registers that are used to control amplitude (or rather duty cycle, but let's not get into that now!) are much smaller than that. In fact, the timers that are used are only 16 bits wide, and since we're running at 50MHZ, and triggering at 100KHz, we're not using much of that width at all. Without digressing too much, the code to setup the timer is below:

```C
void timer_init_3(void) {
	
	RCC->APB1ENR |= RCC_APB1ENR_TIM3EN; // enable the timer

	// set up the timer parameters
	TIM3->CR1 &= ~(TIM_CR1_CEN); //ensure clock is off
	TIM3->PSC = 5 - 1;  // incoming clock is 50mhz, so this will scale it to 1mhz
	TIM3->ARR = 100; // 100 * 0.1us = 10us interrupt (100khz)
	TIM3->DIER |= TIM_DIER_UIE; //enable timer interrupts

	NVIC_SetPriority(TIM3_IRQn, 0x01); // set priority
	NVIC_EnableIRQ(TIM3_IRQn); // enable the IRQ

	TIM3->CR1 |= TIM_CR1_CEN; //enable the counter
}
```

The comments help in the understanding (since the registers we're affecting obfuscate quite a bit). The PSC, or prescaler, is set to 5, (actually 4 but, you know, 0 indexing), this drops the incoming system clock to 1MHZ. We then set the ARR, or Auto Reload Register, to 100. This means that it will retrigger (and cause an interrupt when it overflows and resets) after 100 ticks of the sys clock, or, 1MHz/100 = 100KHz.

What's important here, and the reasons for the digression is that we're using only <7bit's of the 16 bit timer, and that's why it needs scaling. At least, for the frequency changes that is. The duty cycle has a differnt full scale, and this is set to 500. The duty cycle is run off hardware timer (timer 1) which is a little more advance, and so can do things like PWM (pulse width modulation) with ease. This clock is also many bits wide (either 16 or 32, I can't remember) but since the system clock is running at 50MHz, and there's no prescaler this time (to give more discrete levels of PWM, 500 in fact compared to 100 with the same prescaler). So, the ARR register in this case is set to 500, which meaans that 100% duty cycle is given at DC = 500, and that's the new scaling we need.

A quick bit of math, the reason 500 is 9 bits, is we're using the binary system, so base 2. If we want to know how many bits are required, then we do:

$$ ceil(log_2(500)) = 9 $$

```C
phasor_scaled = (phasor.real / 100) *  pwmGainCurrent; // scale the phasor, by the current gain

tmp =(((phasor_scaled)>>9)*500>>23); // we then need to scale the 2^31 val to a number betwee 0 and 500 (the auto reload reg)
	offset = (((PHASE_ADVANCE_1000.real)>>9)*500>>23); // this adds the DC offset, since we need to be centered about 1.65V
	DC = (int)tmp+ (offset); // add the DC offset to the AC signal
```

The scaling seems a bit complex at first, but there is a reason for it. "phase_scaled" is the inital 31 bit number, adjusted by a percentage. So if "pwmGainCurren" was 50, then phasor_scaled would be halved, but still a 31 bit number. This can mostly be ignored for the sake of scaling.

tmp takes the phasor, and bit shifts it right 9 times. The reason for that is when we multiply by another number, their respective widths get summed. For Example, here's a snippet of code that does the above:

```C
#include<stdio.h>
//#include<math.h>

typedef long T_INT32;
typedef short T_INT16;
typedef unsigned short T_UNT32;
typedef long long T_INT64;

typedef struct {
    T_INT32 real;
    T_INT32 imag;
} complex_32;

int main(void) {

    complex_32 phasor; //declares a phasor
    complex_32 PHASE_ADVANCE_1000;
    
    int pwmGainCurrent = 100; // set this to 100% first
    int DC; // this is over written so doesn't need initialiseing with a value
    
    PHASE_ADVANCE_1000.real = 2147441247;
    PHASE_ADVANCE_1000.imag = 13492949;
    
    phasor.real = pow(2,31);
    
    printf("Phasor before scaling %ld, #bits is %d\n", phasor.real, (int)ceil(log2(phasor.real)));
    
    T_INT32 phasor_scaled = (phasor.real / 100) *  pwmGainCurrent; // scale the phasor, by the current gain
    
    printf("Phasor after scaling %ld, #bits is %d\n", phasor_scaled, (int)ceil(log2(phasor_scaled)));

    T_INT32 tmp =((phasor_scaled)>>9); // we then need to scale the 2^31 val to a number betwee 0 and 500 (the auto reload reg)
	
    printf("Tmp after 9 bit shift %ld, #bits is %d\n", tmp, (int)ceil(log2(tmp)));

    tmp *= 500;
    
    printf("Tmp after mut with 500 %ld, #bits is %d\n", tmp, (int)ceil(log2(tmp)));
    
    tmp = tmp >> 23;
        
    printf("Tmp after 23 bit RHS %ld, #bits is %d\n", tmp, (int)ceil(log2(tmp)));
    
    T_INT32 offset = (((PHASE_ADVANCE_1000.real)>>9)*500>>23); // this adds the DC offset, since we need to be centered about 1.65V
    
	DC = (int)tmp+ (offset); // add the DC offset to the AC signal
    
    printf("DC after addition with offset: %ld, #bits is %d\n", DC, (int)ceil(log2(DC)));
    
    return 0;
}
```

If we run this, we get the following output:

```
Phasor before scaling 2147483648, #bits is 31
Phasor after scaling 2147483600, #bits is 31
Tmp after 9 bit shift 4194303, #bits is 22
Tmp after mut with 500 2097151500, #bits is 31
Tmp after 23 bit RHS 249, #bits is 8
DC after addition with offset: 498, #bits is 9
```

We can see that, after the 9 bit shift, we get a number that's 22 bits wide, or 31-9. We then multiply it by the full scale, or 500, which is 9 bits wide, and we go back up to a 31 bit wide number. Finally, we right shift by 23, dropping the result to 8 bits.

The last thing we do (which is a nuance of the electronics, so not important here) is to shift the DC up by 50%, or an "offset". This I won't go into, but it's important to understand that here be have essentially added another 9 bit number. Adding is different to multiplying, the widths don't add (you might expect a 18 bit number) but that's not the case. You can think of it, though, by a multiplication of 2 (if offset == tmp). In which case, we'd have a 1 bit number, plus an 8 bit, which gives the 9 bits, which we required.

As can be seen, the output is just less than 500 (due to some rounding) which is what we wanted!

### Updating the Registers

The final part then is to update the registers with the correct values. There's two that need setting, one for the frequency, and one for the duty cycle, which we mentinoed sets the amplitude.

```C
	int freqChange = freqCurrent % 100; // get the change from 100
	
	if( (freqCurrent-100) < 0) {
		TIM3->ARR = 100 + (100-freqChange); // I will fix this later to convert to frequency
	} else if ((freqCurrent-100) > 0) {
		TIM3->ARR = 100-freqChange; // I will fix this later to convert to frequency
	} else {
		TIM3->ARR = 100; // otherwise, it must be 100, so set it.
	}

	TIM1->CCR1 = (DC); //update the capture control register with the phasor
	TIM3->SR = 0;		// clear the status reg

	GPIOA->ODR &= ~(GPIO_ODR_OD10);
  ```
  
  The code above, an extract from the main one posted above, does just that. We first want to know how much the frequency has changed by (because we use this to scale the auto reload register, and it works inversly to requency, since it's units are essentially seconds, and we're working with per second). We get the percentage change, and then adjust the ARR accordingly.
  
  For the duty cycle, it's quite simple now we've done all the scaling, and simply write it to the register.
  
  That's all folks!
