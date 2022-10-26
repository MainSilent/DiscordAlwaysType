import logging
import argparse

from os.path import exists

from packages.SendRequest import SendRequest
from packages.UserConfig import UserConfig
from packages.file_utility import addLoggingLevel, file_create, file_read

LOGGING_FORMAT = "[%(asctime)s - %(levelname)s]: %(message)s"
LOGGING_DATE_FORMAT = "%Y/%m/%d %H:%M:%S"
USERCONFIG_FILENAME = "userconfig"

def argsparser() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Discord Typing Bot")
	parser.add_argument("-t", "--token", help="Discord token")
	parser.add_argument("-c", "--channel_id", help="Channel ID")
	parser.add_argument("-f", "--file", help="File to read from", default=USERCONFIG_FILENAME)
	parser.add_argument("-o", "--output", help="File to write to", default=USERCONFIG_FILENAME)
	parser.add_argument(
		"-np", "--no-persist", 
		help="Forbid program from persisting token and channel id to a file",
		action="store_true", 
		default=False
	)
	parser.add_argument(
		"-v", "--verbose", 
		help="Verbose logging", 
		action="store_const", 
		dest="loglevel", 
		const=logging.VERBOSE,
		default=logging.INFO
	)
	parser.add_argument(
		"-d", "--debug", 
		help="Debug logging", 
		action="store_const", 
		dest="loglevel",
		const=logging.DEBUG,
		default=logging.INFO
	)
	return parser.parse_args()


def main():
	addLoggingLevel("VERBOSE", logging.INFO - 5)
	args = argsparser()

	logging.basicConfig(level=args.loglevel, format=LOGGING_FORMAT, datefmt=LOGGING_DATE_FORMAT)
	logging.info("Starting...")

	user = UserConfig()
	is_need_to_create_file: bool = False

	# parsing token and channel id from terminal args
	logging.verbose("Checking for existing userconfig file...")
	if args.token:
		logging.verbose("Token provided...")
		user.token = args.token
		is_need_to_create_file = True
	if args.channel_id:
		logging.verbose("Channel ID provided...")
		user.channel_id = args.channel_id
		is_need_to_create_file = True

	# Token and channel id specified in the terminal args; skip reading file
	if not user.token and not user.channel_id:
		logging.verbose("No token or channel id provided from terminal; checking file config...")
		# Check if file exists
		if exists(args.file):
			logging.verbose(f"File {args.file} exists, reading...")
			success, data = file_read(args.file)
			if success:
				logging.verbose("Reading successful...")
				user = UserConfig(data["token"], data["channel_id"])
			else:
				logging.error(f"Failed to read {args.file}")
		else:
			logging.warning(f"No config file exists, requesting user's input manually")
			is_need_to_create_file = True
			user.request_token()
			user.request_channel_id()

	# Manual user input
	if user.token is None:
		is_need_to_create_file = True
		logging.warning("Token is not set, requesting user's input manually")
		user.request_token()
	if user.channel_id is None:
		is_need_to_create_file = True
		logging.warning("Channel ID is not set, requesting user's input manually")
		user.request_channel_id()
	
	# Create file
	if args.no_persist:
		logging.verbose("Not persisting token and channel id to a file")
		is_need_to_create_file = False
		
	if is_need_to_create_file:
		logging.verbose("Creating/updating userconfig file...")
		file_create(
			args.output,
			token=user.token, 
			channel_id=user.channel_id
		)
		is_need_to_create_file = False

	logging.info(f"You can change the token and channel_id by editing the {args.file} file")
	logging.info(f"Start typing...")
	SendRequest(user).run()

if __name__ == "__main__":
	main()
	exit(0)