def get_maintenance_time():
    try:
        with open('/flags/maintenance.on', 'r') as f:
            retry_after = f.readline().strip()
        return retry_after
    except FileNotFoundError:
        return '3600'
