# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 11:54:04 2019

@author: luiggi
"""

#import h5py
#import numpy as np
#f = h5py.File("mytestfile.hdf5", "w")

# Python program creating a 
# context manager 

class ContextManager(): 
	def __init__(self): 
		print('init method called') 
		
	def __enter__(self): 
		print('enter method called') 
		return self
	
	def __exit__(self, exc_type, exc_value, exc_traceback): 
		print('exit method called') 


with ContextManager() as manager: 
	print('with statement block') 

# Python program showing 
# file management using  
# context manager 
  
class FileManager(): 
    def __init__(self, filename, mode): 
        self.filename = filename 
        self.mode = mode 
        self.file = None
          
    def __enter__(self): 
        self.file = open(self.filename, self.mode) 
        return self.file
      
    def __exit__(self, exc_type, exc_value, exc_traceback): 
        self.file.close() 
  
# loading a file  
with FileManager('test.txt', 'w') as f: 
    f.write('Test') 
  
print(f.closed) 


# Python program shows the 
# connection management 
# for MongoDB 

#from pymongo import MongoClient 
#
#class MongoDBConnectionManager(): 
#	def __init__(self, hostname, port): 
#		self.hostname = hostname 
#		self.port = port 
#		self.connection = None
#
#	def __enter__(self): 
#		self.connection = MongoClient(self.hostname, self.port) 
#		return self
#
#	def __exit__(self, exc_type, exc_value, exc_traceback): 
#		self.connection.close() 
#
## connecting with a localhost 
#with MongoDBConnectionManager('localhost', '27017') as mongo: 
#	collection = mongo.connection.SampleDb.test 
#	data = collection.find({'_id': 1}) 
#	print(data.get('name')) 
