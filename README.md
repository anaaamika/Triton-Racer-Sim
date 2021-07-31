# Triton-Racer-Sim
An autonomous robocar simulation client, designed to work with [donkey gym](https://github.com/tawnkramer/gym-donkeycar).

![](cover.png)

The project is inspired by, and has taken reference from [donkeycar](https://www.donkeycar.com/).

## Progress
Driving and training pipeline is up and running.

LiDAR added in dev branch

## Features
* Speed-based models
* Throttle and steering lock at launch
* Adjustable image resolution in donkey gym
* Ability to reset the car to startline
* Ability to break
* Inter-deployable models with donkeycar (throttle-based models only)
* Compatability with donkeycar parts

## Install

**Installing on a laptop/desktop/server: follow host setup and repo download.**

**Installing on a Jetson series SBC: follow Jetson setup and repo download.**

### Set up Environment on Host Windows / Ubuntu / MacOS
1. Install [miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
2. `conda create -n tritonracer python=3.8`
3. `conda activate tritonracer`
4. `pip install docopt pyserial tensorflow==2.3.0 scikit-image pillow keras==2.3.0 opencv-python opencv-contrib-python pygame==2.0.0.dev10 Shapely simple-pid`
5. `conda install scikit-learn`
6. If you are going to use donkey simulator: set up [donkey gym](http://docs.donkeycar.com/guide/simulator/#install) in this environment (omit `conda activate donkey` in the original installation procedure)
    1. If you have a donkeycar installation with donkey gym setup, navigate to the donkey gym repository. If not, find a suitable place and `git clone https://github.com/tawnkramer/gym-donkeycar`
    2. Make sure you are still in tritonracer environment `conda activate tritonracer`
    3. `pip install -e .[gym-donkeycar]`

### Set up Environment on Nvidia Jetson series
1. Check python3 version to be 3.6-3.8 `python3 --version`. If not, install and update python3.
2. Install virtualenv `sudo apt-get install virtualenv`
3. Create a new environment `python3 -m virtualenv -p python3 tritonracer`
4. Invoke tritonracer environment `source ~/tritonracer/bin/activate`
4. Install [tensorflow for Jetson](https://docs.nvidia.com/deeplearning/frameworks/install-tf-jetson-platform/index.html)
5. Install dependencies `python3 -m pip install docopt pyserial pillow keras pygame scikit-image`
6. More on the hardware setup later.

### Download TritonRacer Repo and Create a Car (Both Host PCs and Jetson)
1. `git clone https://github.com/Triton-AI/Triton-Racer-Sim`
2. Copy `Triton-Racer-Sim/TritonRacerSim/car_templates/` folder to somewhere outside the repository (and optionally rename it). This is your car folder, like "d3" of donkeycar.
3. **IMPORTANT:** Go to your car folder, open manage.py and edit line 15 to be your path to the `Triton-Racer-Sim` repo in your system `sys.path.append('/home/haoru/Projects/Triton-Racer-Sim/')`

## Manual

### Config File

Now the `car_templates` folder comes with a `myconfig.yaml`. `manage.py generateconfig` has been depreciated.

### Drive the Car to Collect Data

`python manage.py drive`

**IMPORTANT: by default data collection is turned OFF**

**Joystick mapping may differ on different platforms. Use `python manage.py joystick` to invoke custom joystick mapping wizard.**

Officially supported joysticks: PS4 (3), XBox, F710, G28, Switch

Use a PS4 joystick (Ubuntu):
* Left X axis: steering
* Right Y axis: throttle
* Right Trigger: breaking (simulator)
* Circle: toggle recording
* Triangle: delete 100 records
* Square: reset the car
* Share: switch driving mode

Use an XBOX joystick (Ubuntu):
* Left X axis: steering
* Right Y axis: throttle
* Right Trigger: breaking
* B: toggle recording
* Y: delete 100 records
* X: reset the car
* Back (below XBOX icon on the left): switch driving mode 

Use a G28 Driving Wheel (oof)
* Steering, throttle and breaking are mapped to the corresponding equipment
* The rest is the same as PS4

Data recorded can be found in data/records_x/

### Before Training

If you have a recent NVIDIA GPU: install [CUDA support for tensorflow](https://www.tensorflow.org/install/gpu)

Note: If you have CUDA installed, and tensorflow says `Could not load dynamic library 'libcublas.so.10'` and falls back to CPU during training, add these lines to your ~/.bashrc:

    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/extras/CUPTI/lib64
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-10.2/lib64

### Train a Model

`python manage.py train --tub data/records_1 --model ./models/pilot.h5` 

* `--tub`: path to the data folder
* `--model`: where you would like to put your model (.h5 file)
* `--transfer`: (optional) which old model you would like to train upon

**IMPORTANT:** `--tub` and `--model` params are mandatory.

RAM usage (120 * 160 image, 7000 Records): 8GB

VRAM usage (120 * 160 image, 128 batch size): 3GB

**IMPORTANT** If you run into insufficient memory issue, follow [this](https://linuxize.com/post/how-to-add-swap-space-on-ubuntu-18-04/) guide to pre-allocate space for Ubuntu swap file (Allocate more than the size of your physical RAM). Windows users, click [here](https://answers.microsoft.com/en-us/windows/forum/windows_10-performance/how-to-increase-virtual-memory-in-windows-10-a/46dacaf5-15cf-4f5d-9d5a-cba1401ae4c9). If you do this, your system may stall momentarily duing training, but that's still better than the training getting killed.

See below for available model types.

### Test the Model

`python manage.py drive --model ./models/pilot.h5`

The car will still go to human mode by default. Use your joystick to switch between modes:

* Full human control
* Human throttle + AI steering
* Full AI control

### Migrate Component from Donkeycar, or Write Your Own
How to write your custom component for tritonracer:

1. Subclass the Component class `from TritonRacerSim.components.component import Component`.
2. Define the names of the inputs and outputs for the component in the constructor `super().__init__(self, inputs=['cam/img'], outputs=['ai/steering', 'ai/throttle'], threaded=False)`
3. Implement `step(self, *args)`. Called when the car's main loop iterate through its parts at 20Hz (equivalent to `run()` of donkeycar). Expect args to have the same number of elements as defined in the inputs, and remember to return the same number of outputs as defined in the outputs.
4. Implement `thread_step(self)` if it is a component with its own thread of, for example, polling information from peripherals. thread_step is started before the car starts (equivalent to `update()` of donkeycar). Remember to put a loop, and some delay time inbetween, for the code to run periodically.
5. (Optional) Implement other APIs `onStart(self)`, `onShutdown(self)`, `getName(self)`
6. Add your component in manage.py's `assemble_car()`: `car.addComponent(my_component)`

## Roadmap

Features to come:
1. ~~RNN & LSTM~~
2. Reinforcement learning
3. ~~Migration to real car~~
4. ~~Image filtering~~
5. Packaging the software
6. Merging with donkeycar


## Wiki

### Calibration

Calibration is required before driving an **ACTUAL** car.

1. Go to `myconfig.yaml`. Choose a `sub_board_type`, and fill out the corresponding configurations.
2. For VESC: put your calibrations under `vesc` (e.g. `max_forward_rpm`).
3. For every board else: put your calibrations under `calibration` (e.g. `max_forward_pwm`).  
4. In your car folder, `python manage.py calibrate --steering`. Enter a couple values to test max left, right, and neutral steering. Write them down.
5. After that, `python manage.py calibrate --throttle`. Enter a couple values to test max forward, reverse, and neutral (neutral not required for VESC). Write them down.
6. Go back to `myconfig.yaml` and change these values.

### Data Post Processing

### Image post processing

Collected data without a filter, but want to change mind? No problem. 

1. Check filter configurations in `myconfig.yaml` under `img_preprocessing`.
2. `python manage.py postprocess --source original_folder --destination --new_data_folder --filter`

### Latency post processing

Collected data with a different latency setting, but want to change mind? No problem.

`python manage.py postprocess --source original_folder --destination --new_data_folder --latency`

And follow the wizard.

### Model Types
#### CNN_2D

Input: image array (H\*W\*C)

Output: steering [-1, 1], throttle [-1, 1]

Required config section: `ai_model`, `cam`

#### CNN_2D_SPD_FTR

Input: image array (H\*W\*C), speed

Output: steering [-1, 1], throttle [-1, 1]

Required config section: `ai_model`, `cam`

#### CNN_2D_SPD_CTL

Input: image array (H\*W\*C)

Output: steering [-1, 1], speed

Required config section: `ai_model`, `cam`, `speed_control`
#### CNN_2D_FULL_HOUSE (Depreciated)

Input: image array (H\*W\*C), speed, cross-track error

Output: steering [-1, 1], throttle [-1, 1]

Required config section: `ai_model`, `cam`

#### CNN_2D_SPD_CTL_BREAK_INDICATION

Input: image array (H\*W\*C), break indicator {0, 1}

Output: steering [-1, 1], speed

Required config section: `ai_model`, `cam`, `location_tracker`

#### CNN_3D

Not implemented

#### RNN

Not implemented

#### LSTM

Input: image array (H\*W\*C), speed

Output: steering [-1, 1], throttle [-1, 1]

Required config section: `ai_model`, `cam`, `speed_control`

#### RESNET_CATEGORICAL_SPD_CTL

Input: image array (H\*W\*C)

Output: steering [-1, 1], speed category

Required config section: `ai_model`, `cam`, `speed_control`

#### PID

Not a neural network. Only a PID line follower.

Required config section: `location_tracker`

### VESC

Using a VESC (6 or 4.2) enables speed control. A serial cable is connected from the SBC to the VESC, which is programmed with "servo out" firmware so that the VESC controls both throttle and steering.

#### Installation

1. Follow [this](https://docs.google.com/document/d/1rhdnBL0FwiG_Hzo2K9oM__andg5ioL1QOSigaqqmhyk/edit#heading=h.eglctplfxbbb) document to set up the VESC.
2. On SBC, make sure you are in `tritonracer` environment.
3. `git clone https://github.com/LiamBindle/PyVESC`
4. `cd PyVESC  `
5. `python -m pip install -e .` 

#### Configuration

1. Follow the installation section
2. Follow the calibration section
3. Check `max_forward_current` and `max_reverse_current` in `myconfig.yaml`. They are used in human driving.