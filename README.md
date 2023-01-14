# Lightning Segmentation

### This repo is for practicing using our workflow.



## Setup:

### Conda environment

1. Install Anaconda package manager with Python version 3.9 from [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (recommended because of small size) or [full Anaconda](https://docs.anaconda.com/anaconda/install/index.html) (includes graphical user interface for package management).
2. Verify that the pip3 (Python 3's official package manager) is installed by entering `pip3 -v` in the terminal. If it is not installed, install it, perhaps using [this tutorial](https://www.activestate.com/resources/quick-reads/how-to-install-and-use-pip3/).
3. [Create](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file) the conda environment `jtml` from the `environment.yml` using the command `conda env create -f environment.yml`.
4. Activate the conda env with `conda activate jtml`.
5. There may be other dependencies that you can install using conda or pip3.

### [WandB](https://wandb.ai/) - our logging system.

1. Create an account from the website and send the email you used to Sasank (to get invited to the Wandb team).

## Use:

1. Be in the LitJTML directory (use the `cd` command to change the directory to the `blah/blah/LitJTML/` directory).
2. To fit (train) a model, call `python scripts/fit.py my_config` where `my_config` is the name of the config.py file in the `config/` directory.
    - The config file should specify the model, data, and other parameters.
