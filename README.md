# Purpose: compute course objective fulfillment percentage.
## Rationale: it is tedious to compute course objective fulfillment
    percentage, which is a measurement of students' performance in a course.
## Usage: python analyze.py
## Required files:

   - **students.txt:** a plain text file where each row contains student number and student name, separated by a TAB#
   - **tasks.json:** a plain text file in JSON format specifying the course objectives and tasks in this course.
                 Each task is associated to at least one course objective (co). Each co in a task has an associated weight.
                 Make sure that all weights across tasks sum to 100.

## Limitations:
 _~~~~For simplicity, I recommend associating one and only one co to each
 task, whether the task is an assignment, a quiz, a lab, or a test
 question.  In the case of having more than one co's in a task, a
 student's score in this task will be proportionally distributed
 among these co's according the co's weights.  This treatment is a
 simplification, since in reality two students with the same task
 score may have a different score distribution among different co's.
 For example, a task is associated to two course objectives, co1 and
 co2, with weights 2 and 2, respectively.  Student A achieved a score
 of 2 in this task, with 2 in co1 and 0 in co2.  Student B achieved a
 same score in this task, but with 0 in co1 and 2 in co2.  This
 software does not consider this difference.  It will assign 1 to co1
 and 1 to co2, for both student A and student B.  That is why I
 suggest using a single course objective for each task, to avoid this
 simplification.  Having more than one course objective in a task
 might indicate that this task's goal is not specific enough.  You
 could break down the task into several sub-tasks such that each
 sub-task corresponds to only one course objective._~~~~

## Copyright (C) 2019, 2020 Hui Lan

## Contact the author if you encounter any problems: Hui Lan <lanhui@zjnu.edu.cn>
