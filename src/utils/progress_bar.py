from utils import UI_colors


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█') -> None:

	# Calc the percentage to show
	percent = round(100.0 * (iteration / float(total)), 1)

	# Calc the amount of bar to be filled
	filled_length = int(length * iteration // total)

	# Create the bar string to be showed
	bar = fill * filled_length + '-' * (length - filled_length)

	# Prints the loading bar
	UI_colors.print_blue(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')

	# Print new line on complete
	if iteration == total:
		print()
KB = 1024
MB = 1048576
GB = 1073741824

def toHumanReadable(bytes):
    inKB = round(bytes / KB, 2)
    inMB = round(bytes / MB, 2) 
    inGB = round(bytes / GB, 2) 
    if inGB:
        return str(inGB)+" GB"
    elif inMB:
        return str(inMB)+" MB"
    elif inKB:
        return str(inKB)+" KB"
    else:
        return str(bytes)+ " bytes"
