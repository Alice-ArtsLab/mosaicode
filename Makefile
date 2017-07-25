clean:

	#rm -rfv mosaicomponents/*.pyc mosaicomponents/*.py,cache mosaicomponents/__pycache__
	#rm -rfv *.pyc *.py,cache __pycache__
	#rm -rfv test/*.pyc test/*.py,cache test/__pycache__

	#Pasta mosaicode
	rm -rfv mosaicode/*.pyc mosaicode/*.py,cache mosaicode/__pycache__ None *.mscd

		#Pasta mosaicode/control/
		rm -rfv mosaicode/control/*.pyc mosaicode/control/*.py,cache mosaicode/control/__pycache__ mosaicode/control/None mosaicode/control/*.mscd

		#Pasta mosaicode/extensions
		rm -rfv mosaicode/extensions/*.pyc mosaicode/extensions/*.py,cache mosaicode/extensions/__pycache__

		#Pasta mosaicode/persistence
		rm -rfv mosaicode/persistence/*.pyc mosaicode/persistence/*.py,cache mosaicode/persistence/__pycache__

		#Pasta mosaicode/utils
		rm -rfv mosaicode/utils/*.pyc mosaicode/utils/*.py,cache mosaicode/utils/__pycache__

		#Pasta mosaicode/GUI
		rm -rfv mosaicode/GUI/*.pyc mosaicode/GUI/*.py,cache mosaicode/GUI/__pycache__

			#Pasta mosaicode/GUI/components/
			rm -rfv mosaicode/GUI/components/*.pyc mosaicode/GUI/components/*.py,cache mosaicode/GUI/components/__pycache__

		#Pasta mosaicode/model
		rm -rfv mosaicode/model/*.pyc mosaicode/model/*.py,cache mosaicode/model/__pycache__

		#Pasta mosaicode/plugins
		rm -rfv mosaicode/plugins/*.pyc mosaicode/plugins/*.py,cache mosaicode/plugins/__pycache__

			#Pasta mosaicode/plugins/C
			rm -rfv mosaicode/plugins/C/*.pyc mosaicode/plugins/C/*.py,cache mosaicode/plugins/C/__pycache__

				#Pasta mosaicode/plugins/C/openCV
				rm -rfv mosaicode/plugins/C/openCV/*.pyc mosaicode/plugins/C/openCV/*.py,cache mosaicode/plugins/C/openCV/__pycache__

		#Pasta mosaicode/plugins/javascript
		rm -rfv mosaicode/plugins/javascript/*.pyc mosaicode/plugins/javascript/*.py,cache mosaicode/plugins/javascript/__pycache__

			#Pasta mosaicode/plugins/javascript/webaudio
			rm -rfv mosaicode/plugins/javascript/webaudio/*.pyc mosaicode/plugins/javascript/webaudio/*.py,cache mosaicode/plugins/javascript/webaudio/__pycache__

		#Pasta mosaicode/utils/
		rm -rfv mosaicode/utils/*.pyc mosaicode/utils/*.py,cache mosaicode/utils/__pycache__



		#Pasta test
		rm -rfv test/*.pyc test/*.py,cache test/__pycache__

			#Pasta test/control/
			rm -rfv test/control/*.pyc test/control/*.py,cache test/control/__pycache__ test/control/None test/control/*.mscd

			#Pasta test/extensions
			rm -rfv test/extensions/*.pyc test/extensions/*.py,cache test/extensions/__pycache__

			#Pasta test/persistence
			rm -rfv test/persistence/*.pyc test/persistence/*.py,cache test/persistence/__pycache__

			#Pasta test/utils
			rm -rfv test/utils/*.pyc test/utils/*.py,cache test/utils/__pycache__

			#Pasta test/GUI
			rm -rfv test/GUI/*.pyc test/GUI/*.py,cache test/GUI/__pycache__

				#Pasta test/GUI/components/
				rm -rfv test/GUI/components/*.pyc test/GUI/components/*.py,cache test/GUI/components/__pycache__

			#Pasta test/model
			rm -rfv test/model/*.pyc test/model/*.py,cache test/model/__pycache__

			#Pasta test/plugins
			rm -rfv test/plugins/*.pyc test/plugins/*.py,cache test/plugins/__pycache__

				#Pasta test/plugins/C
				rm -rfv test/plugins/C/*.pyc test/plugins/C/*.py,cache test/plugins/C/__pycache__

					#Pasta test/plugins/C/openCV
					rm -rfv test/plugins/C/openCV/*.pyc test/plugins/C/openCV/*.py,cache test/plugins/C/openCV/__pycache__

			#Pasta test/plugins/javascript
			rm -rfv test/plugins/javascript/*.pyc test/plugins/javascript/*.py,cache test/plugins/javascript/__pycache__

				#Pasta test/plugins/javascript/webaudio
				rm -rfv test/plugins/javascript/webaudio/*.pyc test/plugins/javascript/webaudio/*.py,cache test/plugins/javascript/webaudio/__pycache__

			#Pasta test/utils/
			rm -rfv test/utils/*.pyc test/utils/*.py,cache test/utils/__pycache__


	sudo rm -rfv mosaicode.egg-info
	clear

coverage:
	sudo coverage run --source=. setup.py test
	coverage report -m
	coverage html

clean_coverage:
	rm -rfv htmlcov
	clear

update_to_github:

update_your_folder:

install:
	sudo python setup.py install

uninstall:
	sudo ./uninstall.sh
