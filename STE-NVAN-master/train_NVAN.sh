CKPT=ckpt_NVAN_0230_20191217_32
TRAIN_INFO=../Annotated_data/test_info.npy
TEST_INFO=../Annotated_data/train_info.npy
TRAIN_TXT=../Annotated_data/test_path.txt
TEST_TXT=../Annotated_data/train_path.txt
QUERY_INFO=../Annotated_data/query_IDX.npy
ulimit -c unlimited
ulimit unlimited
python3 train_NL.py --train_txt $TRAIN_TXT --train_info $TRAIN_INFO  --batch_size 8 \
                     --test_txt $TEST_TXT  --test_info  $TEST_INFO   --query_info $QUERY_INFO \
                     --n_epochs 200 --lr 0.0001 --lr_step_size 50 --optimizer adam --ckpt $CKPT --log_path loss.txt --class_per_batch 3 \
                     --model_type 'resnet50_NL' --num_workers 8 --track_per_class 2 --S 8 --latent_dim 2048 --temporal Done  --track_id_loss \
                     --non_layers  0 2 3 0
