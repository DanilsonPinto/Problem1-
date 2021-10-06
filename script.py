import psutil, os, time
import sys

DEFAULT_WRITE_PATH = "./logs.txt"

if len(sys.argv) != 3:
	print("Script Error!\nUsage of script:\npython3 script.py [exec_path] [interval_time]")
	sys.exit()

# create path and interval_time variables
exec_path = sys.argv[1]
interval_time = sys.argv[2]

# teste exec_path
if not os.path.exists(exec_path):
	print(f"Script Error!\nPath {exec_path} doesn't exist!")
	sys.exit()

if not os.access(exec_path, os.X_OK):
	print(f"Script Error!\nPath {exec_path} is not executable!")
	sys.exit()

# teste interval_time
if '-' in interval_time:
	print(f"Script Error!\nInterval time cannot have '-'!")
	sys.exit()

if not interval_time.isnumeric():
	print(f"Script Error!\nInterval time is not numeric (must be integer!)")
	sys.exit()

# test writing path
try:
	with open(DEFAULT_WRITE_PATH, 'w') as file:
		file.write("")
except Exception:
	print(f"Script Error!\nLog writing wasn't possible!")
	sys.exit()

interval_time = int(interval_time)

cmd = exec_path.split()

process = psutil.Popen(cmd)
print(f'process is {process}')

def byte_to_gigabyte(byte_num):
	return round(byte_num / 1073741824, 3)

print(f"PID: {process.pid}")
with open(DEFAULT_WRITE_PATH, 'a') as file:
	header = "RSS_usage(gbs), VMS_usage(gbs), CPU_pct_usage(%), fd_num(int)\n"
	file.write(header)

while(True):
	rss_gb = str(byte_to_gigabyte(process.memory_info().rss))
	vms_gb = str(byte_to_gigabyte(process.memory_info().vms))
	cpu_usage = str(process.cpu_percent(0.0001))
	fd_str = str(process.num_fds())
	with open(DEFAULT_WRITE_PATH, 'a') as file:
		info_str = ",".join([rss_gb, vms_gb, cpu_usage, fd_str])
		file.write(info_str + "\n")
	time.sleep(interval_time)
