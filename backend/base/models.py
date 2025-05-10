from django.db import models

class SystemDetail(models.Model):
    hostname = models.CharField(max_length=255)
    os_name = models.CharField(max_length=255)
    processor = models.CharField(max_length=255)
    total_cores = models.IntegerField()
    total_threads = models.IntegerField()
    ram_total = models.FloatField()
    ram_used = models.FloatField()
    ram_available = models.FloatField()
    storage_total = models.FloatField()
    storage_used = models.FloatField()
    storage_free = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class ProcessDetail(models.Model):
    system = models.ForeignKey(SystemDetail, on_delete=models.CASCADE, related_name='processes')
    pid = models.IntegerField()
    name = models.CharField(max_length=255)
    ppid = models.IntegerField()
    cpu_usage = models.FloatField()
    memory_usage = models.FloatField()
    parent_process = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)

