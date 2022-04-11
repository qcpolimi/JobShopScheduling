import argparse
import os
from job_shop_experiment import JobShopExperiment

parser = argparse.ArgumentParser()
parser.add_argument('-f','--folder', help='Folder for the experiment results', required=True)
args = parser.parse_args()

path = os.path.abspath(args.folder)
os.makedirs(path, exist_ok=False)

exp = JobShopExperiment(path)

exp.run_square_problem(11,1,max_timespan=12) 
