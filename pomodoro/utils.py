import os


def get_task_sessions(sessions):
    task_histories = dict()
    for q in sessions:
        key = (q.task.project.title, q.task)
        if key in task_histories.keys():
            task_histories[key].append(q)
        else:
            task_histories[key] = [q]
    return task_histories

# def calculate_duration(queryset) -> int:
#     total_duration = 0
#     for obj in queryset:
#         histories = obj.history_set.all()
#         for history in histories:
#             duration = history.get_duration()
#             if duration == -1:
#                 return -1
#             total_duration += duration
#     return total_duration


def get_tasks_duration(task_histories: dict) -> dict:
    task_duration = dict()
    for key in task_histories.keys():
        duration = calculate_duration(task_histories[key])
        task_duration[key] = duration
    return task_duration


def calculate_duration(histories: list) -> int:
    total_duration = 0

    for history in histories:
        duration = history.get_duration()
        if duration == -1:
            pass
        total_duration += duration

    return total_duration
#
# base_dir = "/home/oussama/Desktop/الفلاش_الدعوي"
# result = os.scandir(base_dir)
# dirs_files = dict()


def sort_entries(entries):
    dirs = []
    files = []
    for entry in entries:
        if entry.is_dir():
            dirs.append(entry)
        elif entry.is_file():
            files.append(entry)
    dirs.sort(key=str)
    files.sort(key=str)
    return files + dirs

files = list()
def list_files_name(base_dir, entries, sep=''):

    entries = sort_entries(entries)
    for entry in entries:
        if entry.is_dir():
            print(entry.name, sep)
            files.append([entry.name, 'dir'])
            base_dir = os.path.join(base_dir, entry.name)
            entries = os.scandir(base_dir)
            sep += '    '
            list_files_name(base_dir, entries, sep)
            base_dir = os.path.split(base_dir)[0]
            sep = sep[:len(sep)-4]

        elif entry.is_file():
            file_name = os.path.splitext(entry.name)[0]
            files.append([file_name, 'file'])
            print(os.path.splitext(entry.name)[0], sep)
    return files

# list_files_name(entries=result)
# print(">>>>>>>>>>>>>>", files[][0])
