# Progress visualization parameters
import time

disp_progress_type = 'Sharp'  # 'Progress' - progress bar, 'Status' - status line, 'Sharps' - sharps progress bar
progress_update_time = 0.00001  # inner status update frequency (in seconds)



pbar_width = 11

# list of table columns
# label|header|header_alignment|column_alignment|column_width
table_format = [
    ['iter', 'Iter.', 'c', 'c', 6],
    ['time', 'Time', 'c', 'c', 9],
    ['fevals', 'F.Evals', 'c', 'c', 15],
    ['res', 'Result', 'c', '_l', 22],
    ['stall', 'Stall', 'c', 'c', 9],
    ['progress', 'Progress', '_l', '_l', pbar_width]
]

table_format_callback = table_format.copy()
table_format_callback.insert(4, ['callback', 'Callback Result', 'c', 'c', 22])

def print_init(has_callback):
    print("\n\nStarting random mutations...")
    print_formatted_header(has_callback)


def draw_pbar(pbar_type, i, n, completed):
    size = 2 * (pbar_width - 2)
    if n == 1:
        progress = size
    else:
        progress = size if completed else int((i + 1) / (n - 1) * size)
        progress = min(progress, size)
    if pbar_type == 'Progress':
        pbar = "█" * int(progress / 2) + "▋" * (progress % 2)
    elif pbar_type == 'Status':
        pbar = f"{i + 1}/{n}"
    else:
        pbar = '#' * progress + '-' * (size - progress)
    return pbar


last_status_time = 0
fevals = ''
callback = ''


def print_status(multiline, with_callback, status):
    global last_status_time, fevals, callback
    pause = time.time() - last_status_time
    i = status.i
    n = status.n
    newiter = i is None
    if (pause < progress_update_time) and (not newiter):
        return
    last_status_time = time.time()
    elapsed = "{:.0f}".format(status.time) + "s"
    pbar = draw_pbar(disp_progress_type, i, n, newiter)

    if multiline:
        if not newiter:
            data = {'iter': status.iteration, 'time': elapsed, 'progress': pbar, 'callback': status.callback_result}
            print_formatted(data, with_callback, newline=False)
        else:
            stall = f"{status.stall}/{status.n_stall}"
            data = {'iter': status.iteration, 'time': elapsed, 'fevals': status.fevals, 'res': status.last_best_f, 'stall': stall,
                    'progress': pbar, 'callback': status.callback_result}
            print_formatted(data, with_callback, newline=True)
    else:
        if newiter:
            fevals = status.fevals
            callback = status.callback_result

        stall = f"{status.stall}/{status.n_stall}"
        data = {'iter': status.iteration, 'time': elapsed, 'fevals': fevals, 'res': status.last_best_f, 'stall': stall,
                'progress': pbar, 'callback': callback}
        print_formatted(data, with_callback, newline=False)


def align(s: str, length: int, alignment: str):
    transfroms = {
        'c': str.center,
        'l': str.ljust,
        'r': str.rjust,
        '_l': lambda s, l: (" " + s).ljust(l)
    }
    return transfroms[alignment](s, length)


def print_formatted_header(has_callback):
    table = table_format_callback if has_callback else table_format
    wrapped = [align(col[1], col[4], col[2]) for col in table]
    print("\r" + "|".join(wrapped))


def print_formatted(data:dict, with_callback, newline):
    table = table_format_callback if with_callback else table_format
    wrapped = [align(str(data.get(col[0], '')), col[4], col[3]) for col in table]
    if newline:
        print("\r" + "|".join(wrapped))
    else:
        print("\r" + "|".join(wrapped), end='')



