# Test PC-DARTS
for i in 31
do
python3 ../test.py \
--auxiliary \
--cutout \
--seed $i \
--arch PCDARTS$i \
--model_path ../EXP/pcdarts$i.pt \
--layers 20 --init_channels 36 \
--batch_size 64 \
--test_mode ADV
done

# Test DSRNA-JB
#for i in 72
for i in 64
do
python3 ../test.py \
--auxiliary \
--cutout \
--seed $i \
--arch DSRNAJB$i \
--attack PGD10 \
--model_path ../EXP/dsrnajb$i.pt \
--layers 20 --init_channels 36 \
--batch_size 64 \
--test_mode ADV
done
