# SYSTEM/PROCESS PERFORMANCE MONITORING
### Simple humble cross platform (Windows/Linux) system and process resource data logging application.

<br>

Useful if you just want to data log resource information to CSV files, and nothing more.

Uses PSUTIL for system information gathering: https://github.com/giampaolo/psutil

Uses FILELOCK for ensuring only one instance is running: https://github.com/tox-dev/py-filelock

Configurable rolling csv data and application log outputs.

<br>

Currently logs the following system and process resource utilization (non exhaustive list):
___

CPU SYSTEM
 - number of logical cores
 - per core usage percentage
 - time percentages eg. user, idle
 - per core frequency
 - load averages 1, 5, and 15min

CPU PER PROCESS
 - time percentages eg. user, idle
 - usage percentage

DISK SYSTEM
 - per physical disk usage percentage
 - per physical disk read and write bytes per second

DISK PER PROCESS
 - per process disk read and write bytes per second

MEMORY SYSTEM
 - usage percentage

MEMORY PER PROCESS
 - rss usage percentage
 - vms usage percentage

NETWORK SYSTEM
- per nic sent and recv bytes per seconds

<br>
<br>
<br>

# INSTALLING
### Dependencies required to use this application.
```python
filelock==3.6.0
psutil==5.9.0
```

### Clone the application from GitHub.
```
git clone https://github.com/William-Brumble/perf_mon.git
```

### Install the dependencies into a virtual environment.
Windows:
```
py -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Linux:
```
python3 -m venv venv
source .\venv\bin\activate
pip install -r requirements.txt
```
<br>
<br>
<br>

# CONFIGURING
Use the helper script <span style="color:red">**configurator.py**</span> to configure the logger to the desired settings.

```python
configurator.add_section("main")
configurator.set("main", "scan_rate", "1") # Log interval in seconds

configurator.add_section("paths")
configurator.set("paths", "log_data", "./data_sets/") # CSV data output directory
configurator.set("paths", "log_app", "./logs/") # Application log output directory

configurator.add_section("filenames")
configurator.set("filenames", "log_data", "data.log") # CSV data output file names
configurator.set("filenames", "log_app", "app.log") # Application log output file name

configurator.add_section("processes")
configurator.set("processes", "name", "System Idle Process")
#configurator.set("processes", "name", "INSERT_NAME_HERE")
#configurator.set("processes", "name", "INSERT_NAME_HERE")
# ...

configurator.add_section("app_logger")
configurator.set("app_logger", "max_bytes", "2000000") # Application information log file sizes
configurator.set("app_logger", "num_files", "2") # Number of application information log files
configurator.set("app_logger", "silence_logs", "0") # Log application data? 0 for no, 1 for yes

configurator.add_section("data_logger")
configurator.set("data_logger", "max_bytes", "2000000") # Resource log file sizes
configurator.set("data_logger", "num_files", "500") # Number of resource log files
```
Leaving the add sections alone as they are required by the application, while changing only the method's third argument.\
For example to change the data log output path change the following:

```python
configurator.set("paths", "log_data", "./data_sets/")
```

```python
configurator.set("paths", "log_data", "./some_other_directory/")
```
<span style="color:red">***!NB If an config file already exists, running the helper script will delete it.***</span>\
<br>
The following example configuration sets the logger up to log system and process data <span style="color:red">**every second**</span> up to <span style="color:red">**1GB**</span> split between <span style="color:red">**500**</span> files, into <span style="color:red">**./data_sets/data.log**</span> files, and stores application information up to <span style="color:red">**4MB**</span>, split between <span style="color:red">**2**</span> files into <span style="color:red">**./logs/app.log**</span> files.

```ini
[main]
scan_rate = 1

[paths]
log_data = ./data_sets/
log_app = ./logs/

[filenames]
log_data = data.log
log_app = app.log

[processes]
name = System Idle Process

[app_logger]
max_bytes = 2000000
num_files = 2
silence_logs = 0

[data_logger]
max_bytes = 2000000
num_files = 500
```
<br>
<br>
<br>

# USING
Windows:
```
.\venv\Scripts\activate
python main.py
```
Linux:
```
source .\venv\bin\activate
python main.py
```

<br>
<br>
<br>

# LICENSE
This repositories source code is licensed under MIT, refer to dependant libraries for their licenses.