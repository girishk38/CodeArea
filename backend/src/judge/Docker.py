import os
import logging
import time
from enum import Enum
from hashlib import md5 as MD5
from random import randint
from inspect import getframeinfo, currentframe
from .Language import LANGUAGE, TWO_STEP, get_lang_id_by_extension
from glob import glob

LOGFILE_NAME = 'judge.log'

logging.basicConfig(filename=LOGFILE_NAME, level=logging.INFO)
filename = getframeinfo(currentframe()).filename


# Enum class for error sending
# return by: Docker.execute
class Status(Enum):
	SUCCESS = 0
	TIMEOUT = 31744
	RUNTIME_ERROR = 256
	# compilation error code is not genuine
	COMPILATION_ERROR = 257
	INTERNAL_ERROR = 404
	PROBLEM_OUTPUT_NOT_FOUND = 403
	CORRECT = 1
	WRONG = -1


class Docker:
	'''
	Docker:	Initialize docker container and run program of user and destroy container
	container : string format for command to create container
	'''
	container = "docker run -d -it --network none --name {name} -v {source}:/{target} virtual_machine:latest 1>{devnull} 2>&1"
	# container_no_internet = "docker connect none {name}"
	##################################
	#    change here for devnull 	 #
	# CONTAINER_RUNTIME = os.devnull #
	##################################
	# last container id is stored in container.log
	CONTAINER_RUNTIME = os.devnull

	def __init__(self, timeout, memory_limit, language_id, code, source_path, md5_result, test_case_list ,md5_name, md5_input, target_folder, solutionFile):
		'''
		:param timeout: max time limit for code execution
		:param memory_limit: max memory limit for code execution
		:param language_id: user programming language id option on submission
		:param code: user submitted code in string
		:param source_path: path to user folder e.g. /home/$USER/temp/userData/judge
		:param md5_result: result.out file | filecmp.compare(expected_output)
		:param md5_name: container name md5
		:param md5_input: input.in for stdin program
		:param folder: folder in container e.g.  /md5_name or /app
		'''
		try:
			self.solutionFile = solutionFile
			self.timeout = timeout
			self.memory_limit = memory_limit
			self.language_id = language_id
			self.code = code
			self.target_folder = target_folder
			self.path = source_path
			self.output = md5_result
			self.test_case_list = test_case_list
			self.name = md5_name
			self.input = md5_input
			logging.info('[{}]\n\tDocker instance created'.format(time.asctime()))
		except Exception as e:
			logging.critical("\n\nCritical: " + str(time.asctime()) + "\n\t(file, line) = (" + filename + ", " + getframeinfo(currentframe()).lineno +")\n\t"+  str(e) + "\n\n")
			exit(-1)

	def prepare(self):
		'''
		prepare: Create container for user program | from image virtual_image
		'''
		try:
			container_command = Docker.container.format(name=self.name, source=self.path, target=self.target_folder,
														devnull=Docker.CONTAINER_RUNTIME)
			# container_internet = Docker.container_no_internet.format(name=self.name)
			os.system(container_command)
			# os.system(container_internet)
			return True
		except Exception as e:
			logging.critical("\n\nCritical: " + str(time.asctime()) + "\n\t(file, line) = (" + filename + ", " + getframeinfo(currentframe()).lineno +")\n\t"+  str(e) + "\n\n")
			return False

	def execute(self):
		'''
		execute : to write user program to {path}/CodeArea.{extension} and run
		return : Status of programm | SUCCESS, TIMEOUT, RUNTIME_ERROR, COMPILATION_ERROR, INTERNAL_ERROR
		'''
		try:
			file_path = '{path}/CodeArea.{lang}'.format(path=self.path,
														lang=LANGUAGE[self.language_id]['extension'])
			input_path = '/{folder}/{input_md5}_{test}.in'
			output_path = '/{folder}/{output}_{test}.out'
			path = "/{}".format(self.target_folder)
			# write user.code to corrosponding CodeArea file
			with open(file_path, 'w') as fp:
				fp.write(self.code)

			# check if language is compiled or interpreted
			# if self.language_id > TWO_STEP then language is compiled
			two_step = (self.language_id > TWO_STEP)
			if self.solutionFile != "":
				lang_id = get_lang_id_by_extension(self.solutionFile)
			if not two_step:
				# interpreted languages
				result_list = []
				for t in self.test_case_list:
					# print("\n\nTestCaseList: ", t, "\n\n")
					output_file = output_path.format(folder=self.target_folder, output=self.output, test=t)
					input_file = input_path.format(folder=self.target_folder, input_md5=self.input, test=t)
					execute_command = "{command1} <{input_file} >{output} 2>&1"\
					.format(command1=LANGUAGE[self.language_id]['command1'].format(path),
						input_file=input_file, output=output_file)

					docker_command = "docker exec {name} sh -c 'ulimit -v {memory_limit}; timeout {timeout} {command}'"\
						.format(name=self.name,memory_limit=self.memory_limit, timeout=self.timeout, command=execute_command)
					logging.info("\n\nDockerCommand: {}\n\n".format(docker_command))
					status = self.execute_one_by_one(docker_command)
					# print("\n\nStatus: ", status.name, "\n\n")
					if self.solutionFile != "":
						if status.name == "SUCCESS":
							self.update_output_testcase(lang_id, output_file, input_file, path)
					result_list.append(status)

				return_val = result_list

			else:
				# compiled languages
				# command to compile
				compile_path = '/{folder}/{output}.out'.format(folder=self.target_folder,
																output=self.output)
				compile_command = "{command1} >{output} 2>&1"\
					.format(command1=LANGUAGE[self.language_id]['command1'].format(path), output=compile_path)

				# run in docker
				docker_command = "docker exec {name} sh -c '{command}'".format(name=self.name, command=compile_command)
				os.system(docker_command)

				# if compile sucess
				if os.path.isfile('{}/{}'.format(self.path, LANGUAGE[self.language_id]['binary'])):

					# command to execute binary
					result_list = []
					for t in self.test_case_list:
						output_file = output_path.format(folder=self.target_folder, output=self.output, test=t)
						input_file = input_path.format(folder=self.target_folder, input_md5=self.input, test=t)
						execute_command = "{command2} <{input_file} >{output} 2>&1"\
							.format(command2=LANGUAGE[self.language_id]['command2'].format(path),
									input_file=input_file, output=output_file)
						docker_command = "docker exec {name} sh -c 'ulimit -v {memory_limit}; timeout {timeout} {command}'"\
							.format(name=self.name,memory_limit=self.memory_limit, timeout=self.timeout, command=execute_command)

						status = self.execute_one_by_one(docker_command)

						# check if solutionFile exist
						# update output_file if testcase pass or fail (by solution program)
						if self.solutionFile != "":
							if status.name == "SUCCESS":
								self.update_output_testcase(lang_id, input_file, output_file, path)
						result_list.append(status)

					return_val = result_list

				else:
					# if not success in compilation
					return_val = [Status.COMPILATION_ERROR] * len(self.test_case_list)

			# destroy docker container
			self.destroy()
			return return_val
		except Exception as e:
			logging.critical("\n\nCritical: " + str(time.asctime()) + "\n\t(file, line) = (" + filename + ", " + getframeinfo(currentframe()).lineno +")\n\t"+  str(e) + "\n\n")
			self.destroy()
			# for internal error | e.g. not able to create file CodeArea
			return [Status.INTERNAL_ERROR] * len(self.test_case_list)


	def execute_one_by_one(self, command):
		status = os.system(command)
		print("status value = ", status)
		if status is 0:
			return Status.SUCCESS
		elif status >> 8 is 124:
			return Status.TIMEOUT
		else:
			return Status.RUNTIME_ERROR

	def update_output_testcase(self, lang_id, output_file, input_file, path):
		two_step = (lang_id > TWO_STEP)
		if not two_step:
			exec_command = "{command} {input1} {input2}"\
				.format(command=LANGUAGE[lang_id]["command1"].format(path), input1=input_file ,input2=output_file)
			docker_check_soln = "docker exec {name} sh -c 'timeout {timeout} {command}'" \
				.format(name=self.name, timeout=5 * self.timeout, command=exec_command)
			os.system(docker_check_soln)
		else:
			compile_path = '/{folder}/{output}'.format(folder=self.target_folder, output=self.solutionFile)
			compile_command = "{command1} >{output} 2>&1" \
				.format(command1=LANGUAGE[lang_id]['command1'].format(path), output=compile_path)

			# run in docker
			docker_command = "docker exec {name} sh -c '{command}'".format(name=self.name, command=compile_command)
			os.system(docker_command)

			exec_command = "{command} {input1} {input2}"\
				.format(command=LANGUAGE[lang_id]["command2"].format(path), input1=input_file, input2=output_file)
			docker_check_soln = "docker exec {name} sh -c 'timeout {timeout} {command}'"\
				.format(name=self.name, timeout=5*self.timeout, command=exec_command)
			os.system(docker_check_soln)

	def destroy(self):
		'''
		Destroy the docker container
		'''
		try:
			give_permission = "docker exec {name} sh -c 'chmod -R 666 {source}/*'".format(name=self.name, source=self.target_folder)
			stop_container = "docker container stop {name} 1>{devnull} 2>&1".format(name=self.name, devnull=Docker.CONTAINER_RUNTIME)
			remove_container = "docker container rm {name} 1>{devnull} 2>&1".format(name=self.name, devnull=Docker.CONTAINER_RUNTIME)
			os.system(give_permission)
			os.system(stop_container)
			os.system(remove_container)
			#logging.info('[{}]\n\tContainer removed'.format(time.asctime()))
		except Exception as e:
			logging.critical("\n\nCritical: " + str(time.asctime()) + "\n\t(file, line) = (" + filename + ", " + getframeinfo(currentframe()).lineno +")\n\t"+  str(e) + "\n\n")


def random_md5(size):
	'''
	Generate random string md5 | for security reasons
	'''
	try:
		universe = '0qwe1rty2uio3pas4dfg5hjk6lzx7cvb8nm9'
		rand_string = ''
		for i in range(size):
			rand_string += universe[randint(0, len(universe)-1)]
		rand_string = rand_string.encode()

		#logging.info('[{}]\n\trandom string of size {} = {}'.format(time.asctime(), size, rand_string))
		hash = str(MD5(rand_string).hexdigest())
		return hash
	except Exception as e:
		logging.critical("\n\nCritical: " + str(time.asctime()) + "\n\t(file, line) = (" + filename + ", " + getframeinfo(currentframe()).lineno +")\n\t"+  str(e) + "\n\n")
		return False
