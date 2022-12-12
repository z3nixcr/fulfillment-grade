# Solve UnicodeDecodeError - https://blog.csdn.net/blmoistawinde/article/details/87717065
import _locale
import codecs
import json
import os
import sys

_locale._getdefaultlocale = (lambda *args: ['zh_CN', 'utf8'])


def get_task_information(fname):
    with open(fname) as json_data:
        d = json.load(json_data)
    return d


def get_student_information(fname):
    result = []

    with open(fname) as f:
        for line in f:
            line = line.strip()
            lst = line.split('\t')
            if len(lst) != 2:
                print('File %s does not have two columns.' % fname)
                sys.exit()
            result.append((lst[0], lst[1]))
    return result


def get_max_score(d):
    """
    Return the maximum allowable score in a task.  The maximum score is the sum of all values across all
    course objectives.
    """
    result = 0
    for k in d:
        result += int(d[k])
    return result


def get_student_number(fname):
    d = {}

    # If a file has BOM (Byte Order Marker) character, stop.
    with open(fname, 'r+b') as f:
        s = f.read()
        if s.startswith(codecs.BOM_UTF8):
            print('\nERROR: The file %s contains BOM character.  Remove that first.' % fname)
            sys.exit()

    f = open(fname)
    for line in f:
        line = line.strip()
        if not line.startswith('#'):
            lst = line.split('\t')
            sno = lst[0]  # student number
            d[sno] = lst[2]  # score
    f.close()
    return d


def make_individual_grade_files(grade_dir, task_dict, student_lst):
    if not os.path.exists(grade_dir):
        os.mkdir(grade_dir)
    for task in task_dict['tasks']:
        fname = task + '.txt'
        new_file = os.path.join(grade_dir, fname)
        if not os.path.exists(new_file):
            print('Create file %s. You need to fill out students\'s scores in this file.' % new_file)
            f = open(new_file, 'w')
            f.write('#' + task + '\n')
            f.write('\t'.join(['#student.no', 'student.name', 'score']) + '\n')
            for student in student_lst:
                f.write('\t'.join([student[0], student[1], '0']) + '\n')
            f.close()
        else:
            inconsistency = 0
            d = get_student_number(new_file)
            for student in student_lst:
                sno = student[0]
                if not sno in d:
                    inconsistency = 1
                    print(f'Warning: %s is in the new student file, but is not in {task}.' % sno)
            student_numbers = [student[0] for student in student_lst]
            for sno in d:
                if not sno in student_numbers:
                    inconsistency = 1

            if inconsistency == 1:
                f = open(new_file, 'w')
                f.write('#' + task + '\n')
                f.write('\t'.join(['#student.no', 'student.name', 'score']) + '\n')
                for student in student_lst:
                    if student[0] in d:
                        """Set the student score for that grade if available"""
                        f.write('\t'.join([student[0], student[1], '%s' % d[student[0]]]) + '\n')
                    else:
                        """Set score to 0 for this assigment if score not available for this student"""
                        print('Giving this student a score of 0 for this assigment.\n')
                        f.write('\t'.join([student[0], student[1], '0']) + '\n')
                f.close()


def make_score_dict(fname):
    d = {}
    f = open(fname)
    lines = f.readlines()
    f.close()
    for line in lines:
        line = line.strip()
        if not line.startswith('#'):
            lst = line.split('\t')
            sno = lst[0]
            score = lst[2]
            d[sno] = score
    return d


def get_scores_for_each_student(grade_dir, task_dict):
    d = {}
    for task in task_dict['tasks']:
        fname = task + '.txt'
        new_file = os.path.join(grade_dir, fname)
        if os.path.exists(new_file):
            d[task] = make_score_dict(new_file)
        else:
            print('Warning: grade file %s not found.' % new_file)

    return d


def get_objective_total(d):
    """ For each objective, get its total by summing all tasks."""
    objective_lst = d['course.objectives']
    result = []
    check_sum = 0
    for o in objective_lst:
        total = 0
        for task in d['tasks']:
            for co in d['tasks'][task]:
                if co == o:
                    total += d['tasks'][task][co]
        check_sum += total
        result.append((o, total))
    if check_sum != 100:
        print('Objective total is not 100 (%d instead). Make sure you have divide the objective scores across task correctly.' % check_sum)
        sys.exit()
    return result  # [(objective1, value1), (objective2, value2), ...]


def check_availability(fname):
    if not os.path.exists(fname):
        print('The required file %s does not exist.' % fname)
        sys.exit()


# main
GRADE_DIR = 'grade'
TASK_FILE = 'tasks.json'  # required file containing course objectives and tasks.
check_availability(TASK_FILE)
STUDENT_FILE = 'students.txt'  # required file containing student numbers and student names.
check_availability(STUDENT_FILE)
GRADE_FILE = 'grade_file.xls'  # output
software_information = 'Course Objective Fulfillment Calculator\nCopyright (C) 2019 Hui Lan (lanhui@zjnu.edu.cn)'
n = max([len(s) for s in software_information.split('\n')])
banner = '%s\n%s\n%s' % ('-' * n, software_information, '-' * n)
print(banner)

task_dict = get_task_information(TASK_FILE)
student_lst = get_student_information(STUDENT_FILE)
make_individual_grade_files(GRADE_DIR, task_dict, student_lst)

# output results to terminal and file
head_lst = ['student.no', 'student.name']
task_lst = sorted(task_dict['tasks'])
head_lst.extend(task_lst)

file_content = '\t'.join(head_lst) + '\tTotal\n'

score_dict = get_scores_for_each_student(GRADE_DIR, task_dict)

course_object_cumulative_score = {}
for co in task_dict['course.objectives']:
    course_object_cumulative_score[co] = 0

for s in student_lst:
    sno = s[0]
    sname = s[1]
    result = '%s\t%s\n' % (sno, sname)
    file_content += '%s\t%s' % (sno, sname)
    total = 0
    for task in task_lst:
        score = score_dict[task][sno]
        total_score = get_max_score(task_dict['tasks'][task])
        if float(score) > total_score:
            print('Warning: student %s\'s score greater than maximum score in task %s' % (sno + '_' + sname, task))
            sys.exit()
        else:
            result += '    %s:%s\t' % (task, score)
            file_content += '\t%s' % score
            total += float(score)
            for co in task_dict['course.objectives']:
                if co in task_dict['tasks'][task]:
                    my_share = 1.0 * float(score) * task_dict['tasks'][task][co] / total_score
                    course_object_cumulative_score[co] += my_share
                    result += ' [%4.1f] ' % my_share
                else:
                    result += ' [%4.1f] ' % (0)
        result += '\n'
    result += '    ---\n    Total:%4.1f\n' % total
    file_content += '\t%4.1f\n' % total
    # print(result)

f = open(GRADE_FILE, 'w')
f.write(file_content)
f.close()
print('Check spreadsheet %s.' % GRADE_FILE)

objective_total = get_objective_total(task_dict)
num_student = len(student_lst)
for x in objective_total:
    co = x[0]
    value = x[1]
    percentage = 100 * course_object_cumulative_score[co] / (value * num_student)
    print('Course objective %s is %.0f%% satisfied.' % (co, percentage))
