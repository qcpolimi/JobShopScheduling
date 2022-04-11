from collections import defaultdict 

def convert_jobs(jobs):
   '''
   Convert jobs notation, stripping the unnecessary text
   
   example with 2 machines, 3 jobs of 2 operations each with time 1 or 2
   
   jobs = get_model(2,3,2,[1,2]) =
   {'job0': [('machine0', 2), ('machine1', 2)],
   'job1': [('machine1', 1), ('machine0', 2)],
   'job2': [('machine0', 1), ('machine1', 2)]}
   
   output: 
       defaultdict(list,
           {0: [(0, 2), (1, 2)], 1: [(1, 1), (0, 2)], 2: [(0, 1), (1, 2)]})
   '''
   k = defaultdict(list) 
   for key,value in jobs.items():
       k[int(key[3:])] = [(int(v[0][7:]),v[1]) for v in value]
   return k

def convert_solution(solution):     
    '''
    Convert solution notation
    
    example with 2 machines, 2 jobs of 2 operations each with time 1:
    sampleset.first.sample = 
    {'job0_0,0': 1,
    'job0_0,1': 0,
    'job0_1,1': 1,
    'job0_1,2': 0,
    'job1_0,0': 1,
    'job1_0,1': 0,
    'job1_1,1': 1,
    'job1_1,2': 0}
   
    output:
        defaultdict(list, {0: [0, 1], 1: [0, 1]})
    '''
    l = defaultdict(list)
    #convert solution from exact
    for key,value in solution.items():
        if value != 0 and key[0] != 'a':
           # l[int(key[3])] += [int(key[7])]
            lista = key.split('_')
            j = int(lista[0][3:])  
            t = int(lista[1].split(',')[-1])
            l[j] += [t]
    return l

def get_result(jobs, solution):
    max_time = 0
    for job, operations in jobs.items():
        max_time = max(max_time, solution[job][-1] + int(operations[-1][1]))
    return max_time

def transformToMachineDict(jobs: dict, solution: dict) -> dict:
    """Given a solution to a problem from the first argument,
    produces a dictionary indicating the work timeline for each machine.

    Args:
        jobs (dict): description of an instance

        solution (dict): solution to an instance:
        {"job_1": [start_time_of_operation_1, start_time_of_operation_2],
         "job_2": [start_time_of_operation_1, start_time_of_operation_2]}

    Returns: 

        machineDict(dict):
        {"machine_1": [(job, time_of_operation_start, length), (..., ..., ...), ...],
         "machine_2:: [(..., ..., ...), ...], ...}
    """
    machine_dict = defaultdict(list)
    for key, value in solution.items():
        for i in range(len(value)):
    #        print('riga: ', i)
    #        print((key, val, jobs[key][i][1]))
            machine_dict[jobs[key][i][0]].append((key, value[i], jobs[key][i][1]))
    return machine_dict

def generate_gannt(jobs, solution, datadir, name):
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatch
    import seaborn as sns

    jobs = convert_jobs(jobs)
    solution = convert_solution(solution)
    colors = sns.color_palette("Spectral", n_colors=len(jobs))

    rectangles = []
    machine_dict = transformToMachineDict(jobs, solution)
    t_max = get_result(jobs, solution) + 2
    fig, ax = plt.subplots(figsize=(4, 4))
    #ax.set_aspect(aspect=1.5)
    for machine, operations in machine_dict.items():
        # print('machine: ',machine+1)
     #   print('operations: ',operations)
        for idx,operation in enumerate(operations):
            # print('job num: ', operation[0])
            # print('begin: ', operation[1])
            # print('lasts: ', operation[2],end='\n\n')
            # plt.gca().add_patch(plt.Rectangle(
            #      (operation[1], machine), operation[2] - 0.1, 0.9)
            rectangles.append((str(operation[0]), mpatch.Rectangle(
                (operation[1], machine + 1.5), operation[2] - 0.2, 0.9,facecolor=colors[operation[0]], edgecolor = 'black',alpha=0.5),))   
    for r in rectangles:
        ax.add_artist(r[1])
        rx, ry = r[1].get_xy()
        cx = rx + r[1].get_width() / 2.0
        cy = ry + r[1].get_height() / 2.0
    
        ax.annotate(str(int(r[0])+1), (cx, cy), color='black', weight='bold',
                    fontsize=8, ha='center', va='center')
      
    ax.set_xlim(0,  t_max)
    ax.set_ylim(1, len(jobs) + 2)
    ax.set_xticks(range(0, t_max))
    ax.set_yticks(range(1, len(jobs) + 2))
    ax.set_yticklabels(['', *map(str, range(1, len(jobs) + 1))])
    ax.tick_params(left=False)
    ax.set_ylabel('Machines')
    ax.set_xlabel('Time Units')
    fig.savefig(datadir + '/gannt_' + name + '.png')
    plt.clf()

