import os 
import sys
import random
import sqlite3
from collections import defaultdict

con=sqlite3.connect('question_sch.db')
con.execute('CREATE TABLE IF NOT EXISTS elements (question_id Int NOT NULL,genre_name TEXT, question_object TEXT NOT NULL, question_property TEXT NOT NULL, correct_ans TEXT,reference TEXT,question_eng TEXT, age Int,number_of_views Int,is_updated Int) ;')
conn=con.cursor()

files=os.listdir('chem_folder')
properties=defaultdict(int)
for i in files:
	# print(i)
	i=i.strip()
	file=open('chem_folder/'+i,'r')
	temp=file.readlines()
	first=set()
	for j in temp:
		first.add(j.strip())
	for j in first:
		properties[j]+=1

final_properties=[]
for i in properties:
	properties[i]/=len(files)
	if properties[i]>=0.75:
		final_properties.append(i)

print(final_properties)

count=1
for i in files:
	i=i.strip()
	file=open('chem_folder/'+i,'r')
	genre="Chemical elements"
	temp=file.readlines()
	first=set()
	for j in temp:
		first.add(j.strip())
	for j in final_properties:
		if j not in first:
			question='तत्व '+str(i)+ ' का '+ '\"' +str(j)+'\"'+' क्या है?'
			conn.execute("INSERT INTO elements (question_id,genre_name, question_object, question_property) VALUES (?,?,?,?);",(count,genre,str(i),str(j)))
			con.commit()
			print(count)
			count+=1
print(count)
