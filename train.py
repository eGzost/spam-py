import numpy as np
import os
from tflite_model_maker import configs
from tflite_model_maker import ExportFormat
from tflite_model_maker import model_spec
from tflite_model_maker import text_classifier
from tflite_model_maker.text_classifier import DataLoader

import tensorflow as tf
assert tf.__version__.startswith('2')
tf.get_logger().setLevel('ERROR')

spec = model_spec.get('average_word_vec')
spec.num_words = 200_000
spec.seq_len = 2000
spec.wordvec_dim = 22

data = DataLoader.from_csv(
    filename='messages.csv',
    text_column='Message',
    label_column='Category',
    model_spec=spec,
    delimiter=',',
    shuffle=True,
    is_training=True
)

train_data, test_data = data.split(0.9)

model = text_classifier.create(
    train_data,
    model_spec=spec,
    epochs=100,
    validation_data=test_data
)

model.export(
    export_dir='./exported',
    export_format=[
        ExportFormat.LABEL,
        ExportFormat.VOCAB,
        ExportFormat.TFLITE
    ]
)