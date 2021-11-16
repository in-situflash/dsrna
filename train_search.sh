# Architecture Search PC-DARTS
for i in 31
do
python3 train_search.py \
--seed $i \
--train_mode PC-DARTS \
--layers 8 --epochs 50 --init_channels 16 \
--learning_rate 0.025 --batch_size 128 --momentum 0.9 --weight_decay 3e-4 \
--arch_learning_rate 3e-4 --arch_weight_decay 1e-3 
done

# Architecture Search DSRNA-JB
for i in 72
do
python3 train_search.py \
--seed $i \
--train_mode DSRNA-JB \
--layers 8 --epochs 50 --init_channels 16 \
--learning_rate 0.025 --batch_size 128 --momentum 0.9 --weight_decay 3e-4 \
--arch_learning_rate 3e-4 --arch_weight_decay 1e-3 
done
