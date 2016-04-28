#!/usr/bin/python

import os, sys
import numpy as np
from six.moves import cPickle as pickle

def convertSeq(inputFile):
  ''' convert sequences to integers '''
  f = open(inputFile, 'r')
  geneNameList = []
  f_total = f.readlines()
  len_f = len(f_total)
  print "Total records: ", len_f
  f2 = open(inputFile + ".digit.txt", "a")
  seq_digit = []
  i = 0
  r = 0 # column
  c = 0 # row
  array_size = 0
  line_count = 0
  for line in f_total:
#    if line_count > 1:
#      continue

    seq = line.strip()
#      if i>len_seq:
#        continue
    
    if line_count % 1000 == 0:
      print str(line_count) + " processed."
    if not array_size:
      len_seq = int(len(seq))
#      len_seq = 196 #for irregular sizes
      array_size = int(np.sqrt(len_seq))
#      print "seq len:", len_seq, "how many seq:", len_f, "array size:", array_size
#      print len_seq*len_f, len_f*array_size*array_size
      array_result = np.arange(len_seq*len_f).reshape(len_f,array_size,array_size)
    else:
      pass
   
    plus_mode = 1
    pos_index = 0
    r = 0; c =0; i=0
#    print "len_seq", len_seq
  #  print "seq", seq
    for i in range(len_seq):
   #   print "seq[i]", seq[i], "i", i
#      print "i", i 
      change_mode = array_size*2
      if i%(change_mode)==0 and i != 0:
        plus_mode *= -1
#      if True:  
    #  print "i:", i, "r:", r, "c:", c, "plus_mode:", plus_mode
#      print 'Before digit assign.....'
#      print "i:", i, "r:", r, "c:", c, "plus_mode:", plus_mode, "array_result:", "pos_index:", pos_index, array_result[line_count, r,c]
      try:
        if seq[i] == 'a' or seq[i] == 'A':
          array_result[line_count, r,c] = 1
        elif seq[i] == 't' or seq[i] == 'T':
          array_result[line_count,r,c] = 2
        elif seq[i] == 'g' or seq[i] == 'G':
          array_result[line_count,r,c] = 3
        elif seq[i] == 'c' or seq[i] == 'C':
          array_result[line_count,r,c] = 4
        else:
          array_result[line_count,r,c] = 0
      except IndexError:
        array_result[line_count,r,c] = 0
#      print 'After digit assign.....'
#      print "i:", i, "r:", r, "c:", c, "plus_mode:", plus_mode, "array_result:", "pos_index:", pos_index, array_result[line_count, r,c]
#      print "digit check:", i%(change_mode-1)
#      if pos_index == 3 and (i%(change_mode-1)==0) and i!=0:
#        print "true..."
 #     print "array_result:", array_result[line_count,r,c], "line_count", line_count, "r", r, "c", c, "pos_index", pos_index
 #     print "i", i, "r", r, "c", c, "pos_index", pos_index, "plus_mode", plus_mode
      if plus_mode == 1:
        if pos_index == 0:
          c += 1; pos_index +=1
        elif  pos_index == 1:
          r += 1; pos_index +=1
        elif  pos_index == 2:
          c -= 1; pos_index += 1
        elif  pos_index == 3 and (i-c/2.0)%(change_mode-1)!=0 and i!=0:
          r +=1;  pos_index = 0
        elif pos_index == 3 and ((i-c/2.0)%(change_mode-1)==0) and i!=0:
#          print "(i-c/2.0)", (i-c/2.0)
   #     elif pos_index == 3 and ((i%(change_mode-1)==0)  or (i-(array_size-1) != 0)):
          c +=2;  pos_index = 0
          
 
      elif plus_mode == -1:
        if pos_index == 0:
          c += 1; pos_index +=1
        elif  pos_index == 1:
          r -= 1; pos_index +=1
        elif  pos_index == 2:
          c -= 1; pos_index += 1
        elif  pos_index == 3  and  ((i-c/2.0)%(change_mode-1)!=0) and i!=0:
          r -= 1;  pos_index = 0
        elif  pos_index == 3 and  ((i-c/2.0)%(change_mode-1)==0) and i!=0:
          c +=2;  pos_index = 0
#      print "i", i, "r", r, "c", c, "pos_index", pos_index, "plus_mode", plus_mode
    line_count += 1
  
  print array_result[0,:,:]
  if array_result.shape[0]%2==0:
    half = array_result.shape[0]/2
  else:
    half = (array_result.shape[0]-1)/2
#https://stackoverflow.com/questions/3685265/how-to-write-a-multidimensional-array-to-a-text-file

#  with file(inputFile + 'array_result_3d.txt', 'w') as outfile:
#    for data_slice in array_result:
#      np.savetxt(outfile, data_slice, fmt='%d')

  pickle_file = inputFile + 'array_result_3d.txt.pickle1'

  try:
    with open(pickle_file, 'wb') as f:
        pickle.dump(array_result[0:10000], f, pickle.HIGHEST_PROTOCOL)

  except Exception as e:
    print('Unable to save data to', pickle_file, ':', e)
    raise
    
  f.close()

#  pickle_file2 = inputFile + 'array_result_3d.txt.pickle2'

#  try:
#    with open(pickle_file2, 'wb') as f:
#        pickle.dump(array_result[half:], f, pickle.HIGHEST_PROTOCOL)

#  except Exception as e:
#    print('Unable to save data to', pickle_file2, ':', e)
#    raise

#  f.close()

      
#  np.savetxt(inputFile + ".digit.txt", array_result)
  return array_result


if __name__ == '__main__':
 # try:
  if True:
    print 'It produces SystemError when large dim array is produced'
    print "https://github.com/numpy/numpy/issues/2396"
    cmd4 = 'rm ' + sys.argv[1]+'.digit.txt'
    os.system(cmd4)
    print "Removing existing seq file related to input file: InputfileName.bed"
    print "Total number of records"
    cmd3 = "wc -l " + sys.argv[1]
    os.system(cmd3)
    print 'input file: ', sys.argv[1]
#    print "Generating a bed file from inputfile (1st argv; gene names), padding (2nd argv: bp), and ucsc refGene table.............."
    convertSeq(sys.argv[1])
#    print "Generated a padded bed file with " + sys.argv[2] + " bp." 

    
 # except IndexError as e:
 #   print "The first argv is a file including DNA sequences. "





#/sas/seq5/kyeongsj/app/twoBitToFa http://hgdownload.cse.ucsc.edu/gbdb/hg19/hg19.2bit hg19_test.fa -seq=$chr -start=$start -end=$end
