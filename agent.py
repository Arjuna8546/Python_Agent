import platform
import psutil
import os
import shutil
import requests

def get_system_info():
    info = {}
    
    info['hostname'] = platform.node()
    info['os'] = platform.system() + " " + platform.release()
    info['processor'] = platform.processor() or platform.machine()
    info['cpu_cores'] = psutil.cpu_count(logical=False)
    info['cpu_threads'] = psutil.cpu_count(logical=True)

    virtual_mem = psutil.virtual_memory()
    info['ram_total_gb'] = round(virtual_mem.total / (1024 ** 3), 2)
    info['ram_used_gb'] = round(virtual_mem.used / (1024 ** 3), 2)
    info['ram_available_gb'] = round(virtual_mem.available / (1024 ** 3), 2)

    total, used, free = shutil.disk_usage(os.path.abspath(os.sep))
    info['storage_total_gb'] = round(total / (1024 ** 3), 2)
    info['storage_used_gb'] = round(used / (1024 ** 3), 2)
    info['storage_free_gb'] = round(free / (1024 ** 3), 2)

    return info

def get_flat_process_list():
    process_list = []
    for proc in psutil.process_iter(['pid', 'ppid', 'name', 'memory_percent', 'cpu_percent']):
        try:
            info = proc.info
            process_list.append({
                'pid': info['pid'],
                'ppid': info['ppid'],
                'name': info['name'],
                'memory_percent': round(info['memory_percent'], 2),
                'cpu_percent': round(info['cpu_percent'], 2)
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return process_list

print(get_system_info())
print(get_flat_process_list())