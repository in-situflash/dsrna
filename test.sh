# Test PC-DARTS
for i in 31
do
python3 test.py \
--auxiliary \
--cutout \
--seed $i \
--arch PCDARTS$i \
--model_path EXP/pcdarts$i.pt \
--layers 20 --init_channels 36 \
--batch_size 64
done

# Test DSRNA-JB
for i in 72
do
python3 test.py \
--auxiliary \
--cutout \
--seed $i \
--arch DSRNAJB$i \
--model_path EXP/dsrnajb$i.pt \
--layers 20 --init_channels 36 \
--batch_size 64
done
