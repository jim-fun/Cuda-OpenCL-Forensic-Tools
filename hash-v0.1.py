"""
Python Cuda/OpenCL Forensic Testing Program
Copyright (C) 2012 James A. Meyer

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
#!/usr/bin/env python
#import pycuda.gpuarray as gpuarray
#import pycuda.driver as cuda
#import pycuda.autoinit
import numpy,time, hashlib, sys, thread

infile = "test.file2"
dest2 = ".csv"

infile = sys.argv[1]
#hashalg = sys.argv[2]
runs = sys.argv[2]
dest1 = sys.argv[3]
destr = dest1

def calc_hash_gpu(dest1,runs,infile,hashalg):
	#print "thread1"
	OUT = open(dest1,'a')
	output = "Processing Unit","Hashing Alg","Loop","Hash","Input File","Array load time","Hash time","Total time"
	output = str(output)+'\n'
	output = output.replace("'","")
	output = output.replace(")","")
	output = output.replace("(","")
	OUT.write(output)

	for x in range(0,int(runs)):
		FH = open(infile, 'rb')
		FHFILE = FH.read()
		t0 = time.time()
		np = numpy.array(FHFILE)
		a_gpu = gpuarray.to_gpu(np)
		t1 = time.time()
		a_gpu_out = (hashlib.new(str(hashalg),np.tostring(a_gpu)).hexdigest())
		execute_time = time.time()
		output = "gpu",hashalg,x,a_gpu_out,infile, t1-t0,execute_time-t1,execute_time-t0
		output = str(output)+'\n'
		output = output.replace("'","")
		output = output.replace(")","")
		output = output.replace("(","")
		OUT.write(output)
		a_gpu = ''
	FH.close()
	OUT.close()
	print 'Check the output file %s for the results.' % (dest1)

def calc_hash_cpu(dest1,runs,infile,hashalg):
	OUT = open(dest1,'a')
	output = "Processing Unit","Hashing Alg","Loop","Hash","Input File","Array load time","Hash time","Total time"
	output = str(output)+'\n'
	output = output.replace("'","")
	output = output.replace(")","")
	output = output.replace("(","")
	OUT.write(output)

	for x in range(0,int(runs)):
		FH = open(infile, 'rb')
		t0 = time.time()
		np = numpy.array(FH.read())
		t1 = time.time()
		a_gpu_out = hashlib.new(str(hashalg),str(np)).hexdigest()
		execute_time = time.time()
		output = "cpu",hashalg,x,a_gpu_out,infile, t1-t0,execute_time-t1,execute_time-t0
		output = str(output)+'\n'
		output = output.replace("'","")
		output = output.replace(")","")
		output = output.replace("(","")
		OUT.write(output)

	print "Check the output file %s for the results." % (dest1)

hashalg = ['md5', 'sha1',  'sha256',  'sha512']
for hashalgx in range(len(hashalg)):
	for x in range(0,int(destr)):
		hashalgy = str(hashalg[hashalgx])
		dest0 = "hash-gpu-"
		dest1 = dest0+ hashalgy + "-" + str(x + 1) + dest2
		#calc_hash_gpu(dest1, runs, infile, hashalgy)
		dest0 = "hash-cpu-"
		dest1 = dest0+ hashalgy + "-" + str(x + 1) + dest2
		calc_hash_cpu(dest1, runs, infile, hashalgy)

