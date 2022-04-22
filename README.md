[![Repo DOI](https://zenodo.org/badge/419178547.svg)](https://doi.org/10.1038/s41598-022-10169-0)

# Job Shop Scheduling
This repository hosts the code in support of the article "Evaluating the Job Shop Scheduling Problem on a D-Wave Quantum Annealer", published on Nature Scientific Reports as part of the "Quantum information and computing" guest edited collection. See the websites of our [quantum computing group](https://quantum.polimi.it/) for more information on our teams and works.

If you wish to cite this work, please do so using the following BibTex format:
```
@article{Carugno2022,
author={Carugno, Costantino
and Ferrari Dacrema, Maurizio
and Cremonesi, Paolo},
title={Evaluating the job shop scheduling problem on a D-wave quantum annealer},
journal={Nature Scientific Reports},
year={2022},
month={Apr},
day={21},
volume={12},
number={1},
pages={6539},
issn={2045-2322},
doi={10.1038/s41598-022-10169-0},
url={https://doi.org/10.1038/s41598-022-10169-0}
}
```

Further visualizations and tables from the article experiments are available in the extra folder.

## Installation
You can try the code by installing the supporting libraries. 

Create a virtual environment to avoid corrupting your ecosystem:
```
$ python -m venv jss
$ source jss/bin/activate
```

Install the requirements:
```
$ pip install -r requirements.txt
```

## Running the demo
Run the experiment with the following command and substitute NEW_EXPERIMENT_FOLDER_PATH with the path where you want to save your visualizations
`python ./runner.py -f NEW_EXPERIMENT_FOLDER_PATH`
