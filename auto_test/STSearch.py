import sys,getopt,os
import time
'''
Directory: <working directory>/src/xx.v
Command Example: 
'''
try:
    opts, args = getopt.getopt(sys.argv[1:],"hr:",["preprocess=","run="])
except getopt.getopt.GetoptError:
    print("STSearch.py -r <verilogfile>")
    sys.exit(2)

target_verilog = ""
abs_path = os.path.abspath(__file__)
abs_dirpath = os.path.abspath(os.path.dirname(__file__))
abs_workpath = os.getcwd()

for opt, arg in opts:
    if opt == '-h':
        print('STSearch.py -r <verilogfile>')
        sys.exit()
    elif opt in ("-r", "--run"):
        target_verilog = arg

if not os.path.exists(abs_workpath+"/"+target_verilog):
    print("Target verilog is not existed")
    exit(0)
else:
    abs_target_verilog = abs_workpath+"/"+target_verilog


pp_cmd = "/home/ziyue/researchlib/iverilog/bin/iverilog "+\
    abs_target_verilog+" "+\
    "-v -o "+abs_workpath+"/conquest_dut.v "+\
    "-t conquestMulti "+\
    "-ptb="+abs_workpath+"/conquest_tb.v "+\
    "-pclk=clock "+\
    "-preset=reset "+\
    "-preset_edge=1 "+\
    "-punroll=2 "+\
    "-prandom_sim=3"

# Generate branch_ids   
if not os.path.exists(abs_workpath+"/branch_ids"):
    os.system(pp_cmd+" > /dev/null 2>&1 &")

time.sleep(0.1)

if not os.path.exists(abs_workpath+"/branch_ids"):
    print("The branch_ids is generated in this run.")

# Get branch_id
branch_ids_file = open('branch_ids','rb')
branch_ids = branch_ids_file.readlines()
for i in range(len(branch_ids)):
    branch_ids[i] = int(branch_ids[i])

# delete visited.log
if os.path.exists(abs_workpath+"/visited.log"):
    os.remove(abs_workpath+"/visited.log")

if not os.path.exists(abs_workpath+"/visited.log"):
    visited_log = open(abs_workpath+"/visited.log",'w')
    visited_log.write("")
    visited_log.close()

if os.path.exists(abs_workpath+"/Experiment_Result.txt"):
    Exp_res = open(abs_workpath+"/Experiment_Result.txt",'a+')
    Exp_res.writelines("\n")
    Exp_res.close()
else:
    print("No experiment result file")

os.system("iverilog -o conc_run.vvp conquest_tb.v conquest_dut.v")

conquest_dut_file = open('conquest_dut.v')
conquest_dut = conquest_dut_file.read()

for branch_id in branch_ids:
    flag_str = r'";A '+str(branch_id)+'\"'
    if conquest_dut.find(flag_str)==-1:
        continue
    print("Current branch id",branch_id)
    branch_id_file = open('branch_id','w')
    branch_id_file.write(str(branch_id))
    branch_id_file.close()
    os.system(pp_cmd+" > /dev/null 2>&1")
    time.sleep(0.1)

if os.path.exists(abs_workpath+"/Experiment_Result.txt"):
    res = open(abs_workpath+"/Experiment_Result.txt",encoding='utf-8')
    res_str = res.read()
    cur_cycle_res = res_str.split("\n\n")[-1]
    cur_cycle_res_lines = cur_cycle_res.splitlines()
    total_res_time = 0
    total_res_cycle = 0
    for items in cur_cycle_res_lines:
        item = items.split(" ")
        if len(item)>1:
            res_time = item[1]
            res_cycle = item[2]
            total_res_time += float(res_time[:-3])
            total_res_cycle += int(res_cycle)
    print("Time: ",total_res_time, "  Cycle:", total_res_cycle)
    res.close()