# Blog 1 - A Free Subway...

So, today during lunch a friend of mine bet me that I wouldn't be able to, within 6 months, ride my OneWheel from my house to Subway (that's 2.4km from my house, or about 10mins on a bike). If I do, he'll buy me a sub, but if I don't, I have to buy him a sub... So, I had better get to work!

## ESC Firmware

Yesterday I was looking a bit more into the firmware. Today, I [forked](https://github.com/maxsimmonds1337/bldc) the code to take a better look at what board versions the firware supports. The README states to run the make command to see, and that's what I did:

![image](https://user-images.githubusercontent.com/58208872/182473172-c226f924-aa3d-48e9-93a5-c11369bcb009.png)

From this, a list of boards can be seen, currently they are:

**supported boards are**:
100_250
100_250_no_limits
100_500
100_500_no_limits
140_300
40
410
410_0005ohm
410_005ohm
410_no_limits
45
46
46_0005ohm
46_33k
48
49
60
60_75
60_75_mk2
60_75_mk2_no_limits
60_75_no_limits
60_mk3
60_mk3_no_limits
60_mk4
60_mk4_no_limits
60_mk5
60_mk5_no_limits
60_mk6
**60_mk6_no_limits**
60_no_limits
60v2_alva
60v2_alva_mk2
75_300
75_300_no_limits
75_300_r2
75_300_r2_no_limits
75_300_r3
75_300_r3_no_limits
75_600
75_600_no_limits
Cheap_FOCer_2
Little_FOCer
Little_FOCer_V3
Little_FOCer_V3_1
a200s_v2.1
a200s_v2.2
a50s_12s
a50s_6s
axiom
das_mini
das_rs
edu
edu_no_limits
es19
gesc
hd60
hd60_no_limits
hd75
hd75_no_limits
luna_bbshd
mbot
mini4
r2
raiden7
rd2
resc
rh
stormcore_100d
stormcore_100d_no_limits
stormcore_100d_parallel
stormcore_100d_v2
stormcore_100d_v2_no_limits
stormcore_100dx
stormcore_100dx_no_limits
stormcore_100dx_parallel
stormcore_100s
stormcore_100s_no_limits
stormcore_60d
stormcore_60d+
stormcore_60d+_no_limits
stormcore_60d_no_limits
stormcore_60dxs
stormcore_60dxs_no_limits
uavc_omega
uavc_qcube
ubox_single
ubox_single_100
ubox_single_75
ubox_v1_75_micro
ubox_v1_75_typec
ubox_v2_100
ubox_v2_75
unity
unity_no_limits
uxv_sr
warrior6

Only one looks similar - 60_mk6_no_limits. I will dig around to see if there's anything more concrete on the nomenclature.
