import os 
import sys

master_file = sys.argv[1]
outfile_prefix = str(sys.argv[2])
split_iter  = int(sys.argv[3])

list_dict = dict()
if '.txt' not in master_file:
    print("the input file should be txt file")
else:
    with open(master_file) as _file:
        it = 0
        lines = _file.readlines()
        for line_p in lines[it:]:
            file_list = []
            for line in lines[it:]:
                it = it+1
                #print(it)
                file_list.append(line)
                if it%split_iter == 0 and it != 0:
                    keyname = 'split_'+str(it)
                    list_dict[keyname] = file_list
                    break
                    
    new_lines = []
    for key in list_dict.keys():
        with open(key+'.txt','w') as outfile:
            outfile.writelines(list_dict[key])
            new_lines.append("python3 picoNtuplizer.py -v 2p5 -o "+outfile_prefix+"_"+key+" -i "+key+".txt\n")
            outfile.close()
        print('file', f'{key}.txt  created')

    with open('localjob_submit.sh','w') as shell:
        shell.writelines(new_lines)
        shell.close()

    print('Please submit the job by => bash localjob_submit.sh')
            
