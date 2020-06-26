import pandas

sample_dir=['condor_out_Signal_list','condor_out_QCD120_list','condor_out_QCD600_list','condor_out_QCD1000_list']

for dir_ in sample_dir:

	
	fhand = open(dir_ + '/numb.txt')
	NGen = 0
	for line in fhand:
		line=line.rstrip()
		x=int(line.split(":")[1])
		NGen += x
	fhand.close()
	print(dir_,NGen)
