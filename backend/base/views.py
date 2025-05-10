from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import json
from .models import SystemDetail, ProcessDetail
from django.forms.models import model_to_dict

@method_decorator(csrf_exempt,name='dispatch')
class AddAgentDetails(View):
    def post(self, request):
        try:
            resdata = json.loads(request.body)
            data = resdata.get('system_detail')
            hostname = data.get('hostname')
            agent, created = SystemDetail.objects.update_or_create(
                hostname=hostname,
                defaults={
                    'os_name': data.get('os'),
                    'processor': data.get('processor'),
                    'total_cores': data.get('cpu_cores'),
                    'total_threads': data.get('cpu_threads'),
                    'ram_total': data.get('ram_total_gb'),
                    'ram_used': data.get('ram_used_gb'),
                    'ram_available': data.get('ram_available_gb'),
                    'storage_total': data.get('storage_total_gb'),
                    'storage_used': data.get('storage_used_gb'),
                    'storage_free': data.get('storage_free_gb'),
                }
            )

            process_list = resdata.get('process_detail', [])  
            updated_processes = self.refresh_process_data(process_list, agent) 

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'agent_room',
                {
                    'type': 'send_process_update',
                    'data': {
                        'system_detail': model_to_dict(agent),
                        'process_detail': [model_to_dict(p) for p in updated_processes],
                    }
                }
            )

            return JsonResponse({"message": "Agent details and process data saved successfully"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def refresh_process_data(self, process_list, system_obj):
        existing_processes = {p.pid: p for p in ProcessDetail.objects.filter(system=system_obj)}

        new_processes = {p['pid']: p for p in process_list}

        process_objects_to_create = []
        processes_to_update = []
        pid_to_delete = set(existing_processes.keys()) - set(new_processes.keys()) 

        for pid, new_process in new_processes.items():
            existing_process = existing_processes.get(pid)
            if existing_process:
                if (existing_process.cpu_usage != new_process['cpu_usage'] or
                    existing_process.memory_usage != new_process['memory_usage'] or
                    existing_process.name != new_process['name'] or
                    existing_process.ppid != new_process['ppid']):
                    existing_process.cpu_usage = new_process['cpu_usage']
                    existing_process.memory_usage = new_process['memory_usage']
                    existing_process.name = new_process['name']
                    existing_process.ppid = new_process['ppid']
                    processes_to_update.append(existing_process)
            else:
                new_process_obj = ProcessDetail(
                    system=system_obj,
                    pid=new_process['pid'],
                    ppid=new_process['ppid'],
                    name=new_process['name'],
                    cpu_usage=new_process['cpu_usage'],
                    memory_usage=new_process['memory_usage'],
                    parent_process=None  
                )
                process_objects_to_create.append(new_process_obj)

        processes_to_delete = ProcessDetail.objects.filter(pid__in=pid_to_delete, system=system_obj)

        if process_objects_to_create:
            ProcessDetail.objects.bulk_create(process_objects_to_create)

        if processes_to_update:
            ProcessDetail.objects.bulk_update(processes_to_update, ['cpu_usage', 'memory_usage', 'name', 'ppid'])

        if processes_to_delete:
            processes_to_delete.delete()

        updated_processes = ProcessDetail.objects.filter(system=system_obj)
        process_dict = {p.pid: p for p in updated_processes}

        to_update_parent_processes = []
        for process in updated_processes:
            parent = process_dict.get(process.ppid)
            if parent and process.parent_process != parent:
                process.parent_process = parent
                to_update_parent_processes.append(process)

        if to_update_parent_processes:
            ProcessDetail.objects.bulk_update(to_update_parent_processes, ['parent_process'])
            
        return list(updated_processes)
            
class Home(View):
    def get(self,request):
        return render(request,"index.html")
    
class SubprocessView(View):
    def get(self, request, pid):
        subprocesses = ProcessDetail.objects.filter(ppid=pid)
        data = [
            {
                'pid': proc.pid,
                'name': proc.name,
            } for proc in subprocesses
        ]
        return JsonResponse(data, safe=False)
