# Test DSRNA-JB
for i in 72 64
do
python3 ../test.py \
--auxiliary \
--cutout \
--seed $i \
--arch DSRNAJB$i \
--model_path ../EXP/$i.pt \
--layers 8 --init_channels 16 \
--batch_size 128 \
--test_mode ADV
done