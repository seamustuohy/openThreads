all: treelib
	mkdir packages

treelib:
	@echo "Installing tree library"
	mkdir packages/treelib
	cd packages/treelib && sudo pip install -U treelib --record files.txt


clean:
	cd packages/treelib && sudo pip uninstall treelib || cat files.txt | xargs rm -rf
