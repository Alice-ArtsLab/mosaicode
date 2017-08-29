clean:

	#rm -rfv mosaicomponents/*.pyc mosaicomponents/*.py,cache mosaicomponents/__pycache__
	#rm -rfv *.pyc *.py,cache __pycache__
	#rm -rfv test/*.pyc test/*.py,cache test/__pycache__

	#Pasta Raiz
	rm -rfv *.pyc *.py,cache __pycache__ None *.mscd *.txt

		#Pasta mosaicode
		rm -rfv mosaicode/*.pyc mosaicode/*.py,cache mosaicode/__pycache__ mosaicode/None mosaicode/*.mscd

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

			#Pasta mosaicode/blockmodels
			rm -rfv mosaicode/blockmodels/*.pyc mosaicode/blockmodels/*.py,cache mosaicode/blockmodels/__pycache__

				#Pasta mosaicode/blockmodels/C
				rm -rfv mosaicode/blockmodels/C/*.pyc mosaicode/blockmodels/C/*.py,cache mosaicode/blockmodels/C/__pycache__

					#Pasta mosaicode/blockmodels/C/openCV
					rm -rfv mosaicode/blockmodels/C/openCV/*.pyc mosaicode/blockmodels/C/openCV/*.py,cache mosaicode/blockmodels/C/openCV/__pycache__

			#Pasta mosaicode/blockmodels/javascript
			rm -rfv mosaicode/blockmodels/javascript/*.pyc mosaicode/blockmodels/javascript/*.py,cache mosaicode/blockmodels/javascript/__pycache__

				#Pasta mosaicode/blockmodels/javascript/webaudio
				rm -rfv mosaicode/blockmodels/javascript/webaudio/*.pyc mosaicode/blockmodels/javascript/webaudio/*.py,cache mosaicode/blockmodels/javascript/webaudio/__pycache__

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

				#Pasta test/blockmodels
				rm -rfv test/blockmodels/*.pyc test/blockmodels/*.py,cache test/blockmodels/__pycache__

					#Pasta test/blockmodels/C
					rm -rfv test/blockmodels/C/*.pyc test/blockmodels/C/*.py,cache test/blockmodels/C/__pycache__

						#Pasta test/blockmodels/C/openCV
						rm -rfv test/blockmodels/C/openCV/*.pyc test/blockmodels/C/openCV/*.py,cache test/blockmodels/C/openCV/__pycache__

				#Pasta test/blockmodels/javascript
				rm -rfv test/blockmodels/javascript/*.pyc test/blockmodels/javascript/*.py,cache test/blockmodels/javascript/__pycache__

					#Pasta test/blockmodels/javascript/webaudio
					rm -rfv test/blockmodels/javascript/webaudio/*.pyc test/blockmodels/javascript/webaudio/*.py,cache test/blockmodels/javascript/webaudio/__pycache__

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

test_normal:
	sudo python setup.py test

#update_to_github:
#	git add .
#	git commit -m "<>"
#	git push

#update_your_folder:
#	git fetch
#	git pull

install:
	sudo python setup.py install

uninstall:
	sudo ./uninstall.sh
	sudo rm -rfv /home/lucas/mosaicode
