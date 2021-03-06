python nmt.py \
    --attention=scaled_luong \
    --src=et --tgt=en \
    --vocab_prefix=data/et-en/vocab2  \
    --train_prefix=data/et-en/train \
    --dev_prefix=data/et-en/dev  \
    --test_prefix=data/et-en/test \
    --out_dir=tmp/nmt_eten_ep_model \
    --num_train_steps=20000 \
    --steps_per_stats=500 \
    --num_layers=2 \
    --num_units=128 \
    --dropout=0.2 \
    --metrics=bleu
