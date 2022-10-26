import logging

def file_create(filename: str, **kwargs) -> bool:
	desired_keys = ["token", "channel_id"]

	filtered_data: dict[str, str] = {}
	for key in desired_keys:
		if key in kwargs:
			filtered_data[key] = kwargs[key]
	
	data_string: str = ""
	for key, value in filtered_data.items():
		data_string += f"{key} = \"{value}\"\n"

	try:
		with open(filename, "w") as f:
			f.write(str(data_string))
		return True
	except Exception as e:
		logging.error(e)
		return False

def file_read(filename: str) -> tuple[bool, dict[str, str]]:
	result: dict[str, str] = {}
	try:
		with open(filename, "r") as f:
			for line in f.readlines():
				key, value = line.split("=")
				result[key.strip()] = value.strip().lstrip("\"").rstrip("\"")
		return True, result
	except Exception as e:
		logging.error(e)
		return False, {}

def addLoggingLevel(levelName, levelNum, methodName=None):
    """
	Source: https://stackoverflow.com/a/35804945
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present 

    Example
    -------
    >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5

    """
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
       raise AttributeError('{} already defined in logging module'.format(levelName))
    if hasattr(logging, methodName):
       raise AttributeError('{} already defined in logging module'.format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
       raise AttributeError('{} already defined in logger class'.format(methodName))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)
    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)