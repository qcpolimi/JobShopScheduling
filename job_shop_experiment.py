from job_shop_scheduler import get_jss_bqm
from numpy.random import randint 
import time
import neal
from tabu import TabuSampler
from utils import generate_gannt
import matplotlib.pyplot as plt
import seaborn as sns

class JobShopExperiment:
    def __init__(self,datadir):
        self.datadir = datadir

    def get_problem(self,
                machines: int,
                jobs: int, 
                ops: int, 
                time: int or list, 
                ordering : str = 'cycle') -> dict:
        
        if not isinstance(time, list):
            time = [time,time]
        self.problem = dict()
        
        for i in range(jobs):
            if ordering=='cycle':                
                if machines > jobs:
                    op = [('machine' + str(j % machines),randint(time[0],time[1]+1)) for j in range(i*ops,ops+(i*ops))]
                else:
                    op = [('machine' + str(j % machines),randint(time[0],time[1]+1)) for j in range(i,ops+i)]
            elif ordering=='rand':
                op = [('machine' + str(randint(0,machines)),randint(time[0],time[1]+1)) for _ in range(ops)]
            elif ordering == 'randEven':
                assert machines == ops, 'the problem needs to be square'
                op = [('machine' + str(j % machines),randint(time[0],time[1]+1)) for j in range(i,ops+i)]
                random.shuffle(op)
            self.problem['job' + str(i)] = op
        
        return self.problem
        
    def get_square_problem(self,
                           size, 
                           op_time):
        s = size
        self.get_problem(s,s,s,op_time,'cycle')
        
    def get_bqm(self,
                max_timespan, 
                stitch_kwargs):
    
        start = time.time()
        self.bqm, self.t_one_start, self.t_precedence, self.t_share_machine, self.t_remove_absurd_times, self.t_stitcher, self.t_edit_bqm = get_jss_bqm(self.problem, max_timespan, stitch_kwargs = stitch_kwargs)
        end = time.time()
        
        self.t_bqm = end - start    
        
        self.num_var = len(self.bqm.variables)
        self.num_var_jobs = len([x[1] for x in enumerate(self.bqm.variables) if x[1][0] == 'j'])
        self.num_var_aux = len([x[1] for x in enumerate(self.bqm.variables) if x[1][0] == 'a'])
        
        # 1 = fully connected, 0 = only linear biases
        self.connectivity = len(self.bqm.quadratic) / (self.num_var*(self.num_var-1)//2) 
        
    def simulated_annealing(self):
        sampler = neal.SimulatedAnnealingSampler()
        start = time.time() 
        self.sa_sampleset = sampler.sample(self.bqm, chain_strength=2, num_reads=1000)
        end = time.time()
        self.t_sa = end - start
        self.sa_best_sol= self.sa_sampleset.first.energy
        
        generate_gannt(self.problem, self.sa_sampleset.first.sample, self.datadir,'gannt_sa')
        
        sa_hist = self.sa_sampleset.to_pandas_dataframe()
        sns.histplot(sa_hist['energy'],bins=100,color='b')
        plt.savefig(self.datadir + '/hist_sa.png')


    def tabu_search(self):
        sampler = TabuSampler()
        start = time.time()
        self.tabu_sampleset = sampler.sample(self.bqm, chain_strength=2, num_reads=1000)
        end = time.time()
        self.t_tabu = end - start
        self.tabu_best_sol= self.tabu_sampleset.first.energy
        
        generate_gannt(self.problem, self.tabu_sampleset.first.sample, self.datadir,'gannt_tabu')

        tabu_hist = self.tabu_sampleset.to_pandas_dataframe()
        sns.histplot(tabu_hist['energy'],bins=100,color='b')
        plt.savefig(self.datadir + '/hist_tabu.png')


    def quantum_annealing(self):
        samp = DWaveSampler('Advantage_system1.1')
        sampler = EmbeddingComposite(samp)
        start = time.time()
        self.qa_sampleset = sampler.sample(self.bqm, chain_strength=2, num_reads=1000, return_embedding=True)
        end = time.time()
        self.t_qa = end - start
        self.qa_best_sol= self.qa_sampleset.first.energy
        
        generate_gannt(self.problem, self.qa_sampleset.first.sample, self.datadir,'gannt_qa')

        self.embedding = qa_sampleset.info['embedding_context']['embedding']
        
        # contains the mapping from logical qubits to physical qubits 
        self.qubits = [len(value) for value in self.embedding.values()]
        self.num_qubits = sum(self.qubits)

        #chain of max length
        self.max_chain = max(self.qubits)



        self.qpu_sampling_time = qa_sampleset.info['timing']['qpu_sampling_time']
        self.qpu_anneal_time_per_sample = qa_sampleset.info['timing']['qpu_anneal_time_per_sample']
        self.qpu_readout_time_per_sample = qa_sampleset.info['timing']['qpu_readout_time_per_sample']
        self.qpu_access_time = qa_sampleset.info['timing']['qpu_access_time']
        self.qpu_access_overhead_time = qa_sampleset.info['timing']['qpu_access_overhead_time']
        self.qpu_programming_time = qa_sampleset.info['timing']['qpu_programming_time']
        self.qpu_delay_time_per_sample = qa_sampleset.info['timing']['qpu_delay_time_per_sample']
        self.post_processing_overhead_time = qa_sampleset.info['timing']['post_processing_overhead_time']
        self.total_post_processing_time = qa_sampleset.info['timing']['total_post_processing_time']
        
        self.problem_id = qa_sampleset.info['problem_id']



    def run_square_problem(self,
                           size,
                           op_time,
                           simulated_annealing = True,
                           tabu_search = True,
                           quantum_annealing = False, 
                           max_timespan = None, 
                           max_graph_size = None):
        
        self.get_square_problem(size,op_time)
        
        if max_timespan is None:
            max_timespan = size
        
        if max_graph_size is None:
            max_graph_size = size

        self.get_bqm(max_timespan, {'max_graph_size':max_graph_size, 'min_classical_gap':2.0})
            
        if simulated_annealing:
            self.simulated_annealing()
        
        if tabu_search:
            self.tabu_search()
        
#        if quantum_annealing:
#            self.quantum_annealing()
        
