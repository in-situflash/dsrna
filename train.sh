#
# in oiginal paper
# batch size = 128
#

for i in 31
do
python3 train.py \
    --auxiliary \
    --cutout \
    --seed $i \
    --layers 20 \
    --epochs 600 --batch_size 64 --learning_rate 0.025 \
    --grad_clip 5 --drop_path_prob 0.3 --init_channels 36 \
    --momentum 0.9 --weight_decay 3e-5 --arch PCDARTS$i
done