import tensorflow as tf
import pandas as pd
import sys
from pathlib import Path
filename = 'model_limit'
path = str(Path(__file__))
final_path = path[:path.find(filename) + len(filename)]
sys.path.append(final_path)
from gs_param.get_params import load_fit_data
import numpy as np
X, Y, x_test, y_test=load_fit_data("微加贷", 1, important=0.1)
print(np.array(X).shape,np.array(Y).shape)
train_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": np.array(X)},
      y=np.array(Y),
      num_epochs=None,
      shuffle=True)

test_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={"x": np.array(x_test)},
      y=np.array(y_test),
      num_epochs=64,
      shuffle=False)

# Feature columns describe how to use the input.
feature_columns = [tf.feature_column.numeric_column("x", shape=[X.shape[1]])]
# Or estimator using an optimizer with a learning rate decay.
estimator = tf.estimator.DNNClassifier(
    feature_columns=feature_columns,
    # Two hidden layers of 10 nodes each.
    hidden_units=[16, 8],
    # The model must choose between 2 classes.
    n_classes=2)
estimator.train(input_fn=train_input_fn)
metrics = estimator.evaluate(input_fn=test_input_fn)
print(metrics)
# predictions = estimator.predict(input_fn=input_fn_predict)