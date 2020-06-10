import genInteraction_new
import genNegativeData
import genLabelData
import genVecs
import train
import warnings
import sys
import os
import CTCF
from optparse import OptionParser


def parse_args():
	parser = OptionParser(usage="CTCF Interaction Prediction", add_help_option=False)
	parser.add_option("-f", "--feature", default=100, help="Set the number of features of Word2Vec model")
	parser.add_option("-w","--word",default = 6)
	parser.add_option("-r","--range",default = 250)
	parser.add_option("-c","--cell",default = 'gm12878')
	parser.add_option("-t","--total",default = False)
	parser.add_option("-d","--direction",default = 'conv')
	parser.add_option("-p","--chipseq", default = True)

	(opts, args) = parser.parse_args()
	return opts

def makepath(cell,direction):
	if os.path.exists("../Temp/%s" %(cell)) == False:
		os.makedirs("../Temp/%s" %(cell))
	if os.path.exists("../Temp/%s/%s" %(cell,direction)) == False:
		os.makedirs("../Temp/%s/%s" %(cell,direction))

def run(word,feature,range,cell,total,direction,use_chipseq):
	warnings.filterwarnings("ignore")
	makepath(cell,direction)
	cell_input = cell
	if use_chipseq:
		cell_output = "%s_%s" %(cell, "allData")
	else:
		cell_output = "%s_%s" %(cell, "noChIP")

	#if total!=False:
	#	print "Dealing with CTCF Motif Databese"
	#	CTCF.run(cell)


	if not os.path.isfile("../Temp/%s/CTCF.csv" %(cell_output)):
		print "Dealing with CTCF Motif Database"
		CTCF.run(cell_input, cell_output, use_chipseq)

	if not os.path.isfile("../Temp/%s/CH.csv" %(cell_output)):
		print "Mapping Motifs to CHIA-PET"
		genInteraction_new.run(cell_input, cell_output)

	if not os.path.isfile("../Temp/%s/%s/Negative.csv"%(cell_output,direction)):
		print "Generating Negative Data"
		genNegativeData.run(cell_output,direction)

	if not os.path.isfile("../Temp/%s/%s/LabelData.csv"%(cell_output,direction)):
		genLabelData.run(cell_output, direction)

	#not influenced by ChIP-seq, therefore own directory
	if not os.path.isfile("../Temp/%s/Unsupervised"%(cell_input)):
		print "Build unsupervised model (word2vec)"
		genVecs.Unsupervised(int(range),int(word),cell)


	if not os.path.isfile("../Temp/%s/%s/LabelSeq"%(cell_input,direction)):
		genVecs.gen_Seq(int(range),cell_output,direction)
	if not os.path.isfile("../Temp/%s/%s/datavecs.npy"%(cell_input,direction)):
		genVecs.run(word,feature,cell_input, cell_output,direction)

	train.run(word,feature,cell_output,direction)

def main():
	opts = parse_args()
	run(opts.word,opts.feature,opts.range,opts.cell,opts.total,opts.direction, opts.chipseq)

if __name__ == '__main__':
	main()
