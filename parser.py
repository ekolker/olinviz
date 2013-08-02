"""

Eric Kolker
parser.py
RepO data parser script/database builder
Created 2013.05.24 ...yeah, post grad.

"""

import csv, math, sys, json


def process_student(students, enrollment):
	'''
	add the enrollment to the dictionary called students
	'''
	
	# break out the enrollment data
	identifier = enrollment[0].strip()
	term = enrollment[1].strip()
	gender = enrollment[2].strip()
	year = enrollment[3].strip()
	major = enrollment[4].strip()
	concentration = enrollment[5].strip()
	course_id = enrollment[6].strip()
	course_title = enrollment[7].strip()

	# add the student to the dictionary by their ID number
	student = students.setdefault(identifier, dict())

	"""
	students

	currently implemented:
	'ID number'	-> dict; keys:
		'majors'	-> dict; keys:
			term name (string) -> major (strings)
		'gender'	-> 'M' or 'F'

	future:
		'courses'	-> dict; keys:
			'title'	-> list of course titles (strings)
			'id'	-> list of course id numbers (strings)
		'terms'	-> dict; keys:
			list of terms (int)	->	term name (strings)
	"""

	# add in the major at that particular term
	majors = student.setdefault('majors', dict())
	majors[term] = major

	# add the gender
	student.setdefault('gender', gender)

	return students



def process_enrollment(enrollment, dicts = [dict()]):

	"""
	build up all the various dictionaries that hold the data

	enrollment 	-	data from an enrollment, broken down as per below
	dicts 		-	a list of dictionaries
	"""

	'''
	Field contents:
		Random ID
		AcadYr_Session
		Gender Code
		Session Classification Code
		Session Major 1 Description
		Concentration 1 Description
		Course Work Course Number
		Course Work Course Title    
	'''

	# break out the enrollment data
	identifier = enrollment[0].strip()
	term = enrollment[1].strip()
	gender = enrollment[2].strip()
	year = enrollment[3].strip()
	major = enrollment[4].strip()
	concentration = enrollment[5].strip()
	course_id = enrollment[6].strip()
	course_title = enrollment[7].strip()

	# break out the dictionaries
	students = dicts[0]

	# process the student
	students = process_student(students, enrollment)

	# return the updated dictionaries
	return [students]
	

def fill_gap_terms(past_term, present_term):
	'''
	fill in gaps in enrollment history due to LOA
	'''
	gaps = []
	newest = past_term
	while newest != present_term:
		# build up the gap terms
		gaps.append(newest)

		# update the term for next time
		if newest[4] == 'F':
			# fall? just switch to spring
			newest = newest[0:4] + 'S'
		else:
			# it's spring. increment the years, switch to fall
			ref = newest[2:4]
			newest = ref + str('%02d' % (int(ref) + 1)) + 'F'

	return gaps


def fill_away_status(majors):
	'''
	Figure out if the student skipped a semester (or more) and if 
	they studied abroad
	'''

	terms = majors.keys()
	terms.sort()
	trick = {'F':'S', 'S':'F'}

	for i in range(len(terms) - 1):
		# compare adjacesnt indicies
		past = terms[i]
		present = terms[i + 1]

		if past[0:4] == present[0:4]:
			# same year = we're good: 0910S, 0910F. spring before fall, always
			pass
		elif (past[2:4] == present[0:2]) and \
				not (past[4] == present[4]):
			# also good: 0809F 0910S
			pass
		else:
			# we skipped something!
			temp = past
			while (temp != present):
				if temp[4] == 'S':
					temp = temp[0:4] + 'F'
				else:
					temp = temp[2:4] + str('%02d' % ((int(temp[2:4]) + 1) % 100)) + 'S'
				majors[temp] = 'LOA'

	return majors


def build_majorpaths(students):
	'''
	based on the majors, build up a majorpath; store it as 'majorpath'
	'''
	for s in students.keys():
		majors = students[s]['majors']	#dict
		terms = majors.keys()
		terms.sort()

		majors = fill_away_status(majors)

		# # fill in any gap terms
		# gap_terms = []
		# for index in range(1, len(majors.keys())):
		# 	past = terms[index - 1]
		# 	present = terms[index]

		# 	# print past, present
			
		# 	# are we back to back?
		# 	# or
		# 	# front 1/2 of present = back 1/2 of past and S->F
		# 	if 	((not (past[0:4] == present[0:4]) and \
		# 		not (past[4] == 'S' and present[4] == 'F')) or \
		# 		(int(past[2:4]) != int(present[0:2]) and \
		# 		past[4] == 'S' and present[4] == 'F')):
		# 		# print index, terms, past, present, past[2:4], present[0:2]
		# 		# we have some gaps to fill!

		# 		temp = fill_gap_terms(past, present)
		# 		for t in temp:
		# 			gap_terms.append(t)

		# # add in the gap terms. in this case, all LOA.
		# for g in gap_terms:
		# 	majors[g] = 'LOA'

		# print majors

		terms.sort()
		majorpath = ''

		# build the majorpath
		for t in terms:
			val = majors[t]
			while len(val) < 3:
				val = val + ' '

			majorpath = majorpath + val

		# add it to the dictionary
		students[s]['majorpath'] = majorpath

	return students


def separate_years(students):
	'''
	build a dict called start_years which stores the id numbers of students
	in each entering class. used to filter by entry year for viz purposes
	'''
	start_years = dict()

	for s in students.keys():
		# for each student, figure out their entry year
		first_year = min(students[s]['majors'].keys())[0:2]

		# add them to the appropriate list
		start_years.setdefault(first_year, []).append(s)

	return start_years



def separate_genders(students):
	'''
	build a dictionary called gender with keys 'M' and 'F' which
	map to lists of id numbers (string) to be used with students
	'''

	gender = {'M' : [], 'F' : []}
	women = {}
	men = {}

	for id_number in students.keys():
		if students[id_number]['gender'] == 'M':
			gender['M'].append(id_number) 
			men[id_number] = students[id_number]
		else:
			gender['F'].append(id_number)
			women[id_number] = students[id_number]

	return (women, men, gender)



def generate_nodes(students, tag = '', node_number = 0):
	'''
	build up the dictionary of nodes (declared majors at a particular
	semester) and node id numbers (used to link the nodes) 
	tag is used to tag the nodes (i.e. by gnder and class year)
	'''
	nodes = {}
	backwards = {}
	# keys:     [3 digit semester #][3 character major name]
	# values:   unique node ID number

	for student in students.values():

		for semester in range(1, len(student['majorpath']) / 3 + 1):

			# slice the majorpath
			major = student['majorpath'][3 * semester - 3: 3 * semester]

			# build up the node name
			potential_node_name = str('%02d' % semester) + major + tag

			if potential_node_name in nodes.keys():
				continue
				# node exists, no need to add it
			else:
				# otherwise, add it, and gove it a unique ID
				nodes.setdefault(potential_node_name, node_number)
				backwards.setdefault(node_number, potential_node_name)
				node_number = node_number + 1

	return (nodes, backwards)



def generate_links(students, nodes):
	'''
	Build up a dictionary of links between nodes. These repreent transitions 
	between declared majors at the ntersection of semesters.
	'''
	links = {}

	# loop through the students
	for student in students.values():
		majorpath = student['majorpath']

		# loop through the semesters for which we have data
		for semester in range(1, len(majorpath) / 3):
			# calculate the past and current semester representations
			start_semester = str('%02d' % semester)
			end_semester = str('%02d' % (semester + 1))

			# calculate the start and end majors
			start_major = majorpath[3 * semester - 3 : 3 * semester]
			end_major = majorpath[3 * semester : 3 * semester + 3]

			# pick out the source and sink nodes
			start_node_name = start_semester + start_major
			end_node_name = end_semester + end_major

			start_node_id = nodes[start_node_name]
			end_node_id = nodes[end_node_name]

			# add the change into the links dictionary
			# start_name + end_name (string) -> dict
			swap = links.setdefault(start_node_name + end_node_name, \
				{"source" : start_node_id, \
				"target" : end_node_id, \
				"value" : 0})

			swap['value'] = swap['value'] + 1

	return links



def build_json(backwards_nodes, links, filename, header, size):
	'''
	Write the output file so that the data can be visualized using 
	d3 and sankey.
	'''
	out = open(filename, "w")

	# we need the reverse nodes dictionary so we can sort by key
	contents_nodes = []
	for node_id in sorted(backwards_nodes.keys()):
		contents_nodes.append({'name' : backwards_nodes[node_id]})

	contents = {'nodes' : contents_nodes, 'links' : links.values(), \
		'header' : header, 'size' : size}

	print filename + ':\t writing . . .',
	out.write(json.dumps(contents, ensure_ascii = False, indent = 4) + "\n")
	out.close()

	print 'done!'



def generate_output(students, filename, header, tags = ''):
	'''
	use the dict (or list of dicts) students to build an output .json
	file filename with header header to be visualized

	tags are used to separate different dict's worth of data
	'''

	if tags == '':
		# we only have one dict to visualize

		# build the nodes for the sankey chart
		(nodes, backwards) = generate_nodes(students)

		# make the links
		links = generate_links(students, nodes)

		header = header + ' (' + str(len(students.keys())) + ' Oliners)'
		# build the json!
		build_json(backwards, links, filename, header, len(students.keys()))

	else:
		# we have mutiple to visualize. declare everything, append as we go
		nodes = {}
		backwards = {}
		links = []

		for subset in students:
			# loop through the different dicts of students
			(more_nodes, more_backwards) = generate_nodes(subset, \
				len(nodes.values()))

			nodes.update(more_nodes)
			backwards.update(more_backwards)

		# we have all our nodes, now generate the links!
		# realization: this will be hard...





def main(name):

	print 'activate!\n'

	rawdata = csv.reader(file("data2.csv", "rU"), dialect = 'excel')

	print 'file open...\n'
	
	# ths will hold the students (keyed by id number)
	students = dict()
	
	# to be expanded as functionality is needed
	dicts = [students]

	for enrollment in rawdata:
		# process each enrollment
		dicts = process_enrollment(enrollment, dicts)
	
	# calculate each student's majorpath
	students = build_majorpaths(students)

	# filter... currently this added functionality is not used
	start_years = separate_years(students)
	# year (string) -> list of id number (string)

	olin_class_of = {}
	# grad_year (string) -> dict
	# 	id (string) -> student
	# go through each start year...
	for start_year in start_years.keys():
		# ...but reference them by their graduation year
		grad_year = str(int(start_year) + 2004)
		
		# make a dict in preparation
		this_graduating_class = {}
		for student_id_number in start_years[start_year]:
			# add each student to the dict
			this_graduating_class[student_id_number] = \
				students[student_id_number]

		# add the dict to olin_class_of
		olin_class_of[grad_year] = this_graduating_class

		# output!
		generate_output(this_graduating_class, grad_year + '_all.json', \
			'Class of ' + grad_year)



	(women, men, gender) = separate_genders(students)
	# women and men = students-like dicts
	# gender = 'M' and 'F' -> list of id number (string)

	# battle of the sexes!

	# build some .json files!
	# all olin students ever
	generate_output(students, 'olin.json', 'All of Olin')

	# ladies
	generate_output(women, 'women.json', 'All of Olin\'s women')
	# gentlemen
	generate_output(men, 'men.json', 'All of Olin\'s men')

	



	print '\ncomputation complete'



if __name__ == '__main__':
	main(*sys.argv)
	