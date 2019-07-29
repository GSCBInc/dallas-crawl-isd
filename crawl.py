from app.main import application

import logging

if __name__ == '__main__':
	logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
	app = application()
	app.start()