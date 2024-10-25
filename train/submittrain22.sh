#!/bin/bash

username=ajohns14 

 
whichcase[0]=20220428
whichcase[1]=20220429
whichcase[2]=20220502
whichcase[3]=20220503
whichcase[4]=20220504
whichcase[5]=20220505 
whichcase[6]=20220506
whichcase[7]=20220509
whichcase[8]=20220510
whichcase[9]=20220511 
whichcase[10]=20220512 
whichcase[11]=20220513 
whichcase[12]=20220516
whichcase[13]=20220517
whichcase[14]=20220518
whichcase[15]=20220519
whichcase[16]=20220520
whichcase[17]=20220523
whichcase[18]=20220524
whichcase[19]=20220525
whichcase[20]=20220526
whichcase[21]=20220527
whichcase[22]=20220531
whichcase[23]=20220601
whichcase[24]=20220602
whichcase[25]=20220603
whichcase[26]=999


icase=0
while [ ${icase} -le 25 ];do #51

itm=0
while [ ${itm} -le 0 ];do   

isev=0
while [ ${isev} -le 7 ];do #5   

sed "s/TTTT/${itm}/g" train_loo22.slm > next.slm
sed -i "s/SSSS/${isev}/g" next.slm 
sed -i "s/CCCC/${whichcase[${icase}]}/g" next.slm 
sed -i "s/UUUU/${username}/g" next.slm 

sbatch next.slm
sleep 0.5
isev=$((isev+1))
done

itm=$((itm+1))
done


icase=$((icase+1))
done




