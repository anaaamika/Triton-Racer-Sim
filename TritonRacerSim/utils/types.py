from enum import Enum

class ModelType(Enum):
    CNN_2D = 'cnn_2d' # takes image, predicts throttle and steering
    CNN_2D_SPD_FTR = 'cnn_2d_speed_as_feature' # takes image and speed, predicts throttle and steering
    CNN_2D_SPD_CTL = 'cnn_2d_speed_control' # takes image, predicts speed and steering
    CNN_2D_FULL_HOUSE = 'cnn_2d_full_house'
    CNN_2D_SPD_CTL_BREAK_INDICATION = 'cnn_2d_speed_control_break_indication'
    CNN_3D = 'cnn_3d' # takes a sequence of images, predicts throttle and steering
    RNN = 'rnn' # same as 3D CNN
    LSTM = 'lstm'
    RESNET_CATEGORICAL_SPEED_CONTROL = 'resnet_categorical_speed_control'
    PID = 'pid' # No neural network. Use a PID controller.

