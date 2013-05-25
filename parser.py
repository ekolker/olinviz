"""

Eric Kolker
parser.py
RepO data parser script/database builder
Created 2013.05.24 ...yeah, post grad.

"""

import csv, math, sys


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

	future:
		'courses'	-> dict; keys:
			'title'	-> list of course titles (strings)
			'id'	-> list of course id numbers (strings)
		'terms'	-> dict; keys:
			list of terms (int)	->	term name (strings)
	"""

	majors = student.setdefault('majors', dict())
	majors[term] = major

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
	gaps = []
	newest = past_term
	while newest != present_term:
		# build up the term

		gaps.append(newest)

		if newest[4] == 'F':
			# fall? just switch to spring
			newest = newest[0:4] + 'S'
		else:
			# it's spring. increment the years, switch to fall




	return gaps



def build_majorpaths(students):
	'''
	based on the majors, build up a majorpath; store it as 'majorpath'
	'''
	for s in students.keys():
		majors = students[s]['majors']	#dict
		terms = majors.keys()
		terms.sort()

		majorpath = ''
		
		# fill in any gap terms. in this case, these are all LOA.
		for index in range(1, len(terms)):
			past = terms[index - 1]
			present = terms[index]

			# are we back to back?
			# or
			# front 1/2 of present = back 1/2 of past and S->F
			if 	((not (past[0:4] == present[0:4]) and \
				not (past[4] == 'S' and present[4] == 'F')) or \
				(int(past[2:4]) != int(present[0:2]) and \
				past[4] == 'S' and present[4] == 'F')):
				print index, terms, past, present, past[2:4], present[0:2]
				# we have some gaps to fill!

				gap_terms = fill_gap_terms(past, present)


	return students



def main(name):

	print 'activate!\n'

	rawdata = csv.reader(file("data.csv", "rU"), dialect = 'excel')
	
	students = dict()
	
	dicts = [students]

	for enrollment in rawdata:
		# process each enrollment
		dicts = process_enrollment(enrollment, dicts)
	
	# calculate each student's majorpath
	students = build_majorpaths(students)


	print '\ndone'



if __name__ == '__main__':
	main(*sys.argv)
	