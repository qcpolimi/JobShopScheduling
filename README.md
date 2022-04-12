# Job Shop Scheduling
This repository hosts the code in support of the article "Evaluating the Job Shop Scheduling Problem on a D-Wave Quantum Annealer", published on Nature Scientific Reports as part of the "Quantum information and computing" guest edited collection. 

Additional visualizations and tables from the article are available in the extra folder.

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
