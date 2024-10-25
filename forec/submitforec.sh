#!/bin/bash

username=ajohns14 
 
whichcase[1]=20190430
whichcase[2]=20190501
whichcase[3]=20190502
whichcase[4]=20190503
whichcase[5]=20190506
whichcase[6]=20190507
whichcase[7]=20190508
whichcase[8]=20190509
whichcase[9]=20190510
whichcase[10]=20190513
whichcase[11]=20190514
whichcase[12]=20190515
whichcase[13]=20190516
whichcase[14]=20190518
whichcase[15]=20190520
whichcase[16]=20190521
whichcase[17]=20190522
whichcase[18]=20190523
whichcase[19]=20190524
whichcase[20]=20190527
whichcase[21]=20190528
whichcase[22]=20190529
whichcase[23]=20190530
whichcase[24]=20190531
whichcase[25]=20210427
whichcase[26]=20210428
whichcase[27]=20210430
whichcase[28]=20210503
whichcase[29]=20210504
whichcase[30]=20210505
whichcase[31]=20210506
whichcase[32]=20210507
whichcase[33]=20210510
whichcase[34]=20210511
whichcase[35]=20210512
whichcase[36]=20210513
whichcase[37]=20210514
whichcase[38]=20210517
whichcase[39]=20210519
whichcase[40]=20210520
whichcase[41]=20210521
whichcase[42]=20210524
whichcase[43]=20210525
whichcase[44]=20210526
whichcase[45]=20210527
whichcase[46]=20210528
whichcase[47]=20210531
whichcase[48]=20210601
whichcase[49]=20210602
whichcase[50]=20210603
whichcase[51]=20210604

whichcase[52]=20220428
whichcase[53]=20220429
whichcase[54]=20220502
whichcase[55]=20220503
whichcase[56]=20220504
whichcase[57]=20220505 
whichcase[58]=20220506
whichcase[59]=20220509
whichcase[60]=20220510
whichcase[61]=20220511 
whichcase[62]=20220512 
whichcase[63]=20220513 
whichcase[64]=20220516
whichcase[65]=20220517
whichcase[66]=20220518
whichcase[67]=20220519
whichcase[68]=20220520
whichcase[69]=20220523
whichcase[70]=20220524
whichcase[71]=20220525
whichcase[72]=20220526
whichcase[73]=20220527
whichcase[74]=20220531
whichcase[75]=20220601
whichcase[76]=20220602
whichcase[77]=20220603


 
kjob=52 #case
while [ ${kjob} -le 77 ];do #61,73

echo "case ${kjob}"

itm=0
while [ ${itm} -le 0 ];do   


isev=0
while [ ${isev} -le 7 ];do  

  
sed "s/YYYY/${whichcase[${kjob}]}/g" forec_loo_22.slm > next.slm
#sed "s/YYYY/${whichcase[${kjob}]}/g" forec_tr1921.slm > next.slm
#sed "s/YYYY/${whichcase[${kjob}]}/g" forec_loo.slm > next.slm
sed -i "s/TTTT/${itm}/g" next.slm 
sed -i "s/SSSS/${isev}/g" next.slm 
sed -i "s/UUUU/${username}/g" next.slm 


sbatch next.slm
sleep 0.5


isev=$((isev+1))
done


itm=$((itm+1))
done


kjob=$((kjob+1))
done






