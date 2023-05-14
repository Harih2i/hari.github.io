from os import walk
import re
from datetime import datetime
from croniter import croniter

class Frequency():
	five = 0
	ten = 0
	fifteen = 0
	thirty = 0
	one_hour = 0
	three_hour = 0

def calculate_freq(cron_expression, freq_obj):
	print("cron_expression:", cron_expression)
	current_datetime = datetime.now()
	try:
		cron = croniter(cron_expression, current_datetime)

		next_datetime = cron.get_next(datetime)
		next2_datetime = cron.get_next(datetime)

		interval = int((next2_datetime - next_datetime).total_seconds())

		if interval == 300:
			freq_obj.five += 1
		elif interval == 600:
			freq_obj.ten += 1
		elif interval == 900:
			freq_obj.fifteen += 1
		elif interval == 1800:
			freq_obj.thirty += 1
		elif interval == 3600:
			freq_obj.one_hour += 1
		elif interval > 3600:
			freq_obj.three_hour += 1
	except Exception as err:
		pass

def collect_mls_data(jobs, freq_obj):

	try:

		mls_list_data = list()
		partial_jobs = dict()

		frequency_array = list()
		

		for job in jobs:
			mls_id = re.search('-mls_id=(\d+)', job).group(1)
			if mls_id not in partial_jobs:
				partial_jobs[mls_id] = []
				partial_jobs[mls_id].append(job)
			else:
				partial_jobs[mls_id].append(job)

		for k1, v1 in partial_jobs.items():
			mls_dataset = dict()
			mls_dataset['mls_id'] = k1
			mls_dataset['commands'] = v1
			mls_list_data.append(mls_dataset)

		find = re.compile(r"^[^.]*")
		for each_job in jobs:
			# print("each_job:", each_job)
			cron_fr = re.search(find, each_job).group(0)
			print("cron_fr:", cron_fr.split(' /opt')[0])
			# if not cron_fr:
			# 	find = re.compile(r"^[^ /]*")
			# 	print("cron_fr2:", cron_fr)
			# 	cron_fr = re.search(find, each_job).group(0)
			calculate_freq(cron_fr.split(' /opt')[0], freq_obj)

		# print("freq_obj:", freq_obj.one_hour)

		label_elem = {"five":"5mins", "ten":"10mins", "fifteen":"15mins",
				"thirty":"30mins", "one_hour":"1hour", "three_hour":">3hours"}
		
		for k2, v2 in label_elem.items():
			frequency_dict = dict()
			frequency_dict['label'] = v2
			frequency_dict['value'] = getattr(freq_obj, k2)
			frequency_array.append(frequency_dict)


		return mls_list_data, frequency_array

	except Exception as err:
		print("Error happened:", str(err))

def collect_file_data(filepath, freq_obj):

	jobs = list()
	print("filepath:", filepath)
	print("freq_obj:", freq_obj)
	for file in filepath:
		# print("file:", file)
		with open('crontab/'+file) as fo:
			for line in fo:
				if line and not re.match('#',line) and re.search('mls_id',line):
					jobs.append(line)
	mls_list_data, frequency_array = collect_mls_data(jobs, freq_obj)

	return mls_list_data, frequency_array

def main():
	cron_object = dict()
	dataset = dict()

	cron_files = ('image','download','post-converter','mlsparser')
	cron_files = ('image','converter','mlsparser','download')
	filenames = next(walk('crontab'), (None, None, []))[2]

	for number_cron in cron_files:
		cron_object[number_cron] = []
		for file in filenames:
			if re.search(number_cron, file, re.IGNORECASE):
				cron_object[number_cron].append(file)

	print("cron_object:",cron_object)
	for key, val in cron_object.items():
		freq_obj = Frequency()
		if key == 'download':
			val = [x for x in val if not x.startswith('image-downloader')]
			print("val:",val)
		mls_list_data, frequency_array = collect_file_data(val, freq_obj)
		if key == 'download':
			dataset['scheduler'] = mls_list_data
			dataset['scheduler'+'_frequency'] = frequency_array

		if key == 'mlsparser':
			dataset['normalizer'] = mls_list_data
			dataset['normalizer'+'_frequency'] = frequency_array
		else:
			dataset[key] = mls_list_data
			dataset[key+'_frequency'] = frequency_array

		print("dataset:",dataset)
		print("***********************************************************")
	return dataset

