import basic
import os
import time
from web3.middleware import geth_poa_middleware
from OgFileHandle import upload


CURRENT_PATH = os.getcwd()
MABI_OF_CONTRACT = os.path.join(CURRENT_PATH, 'Solidity','mnew_contract_abi.json')
ChainControl = 10
uri = "mongodb+srv://nagi:nagi@cluster0.ohv5gsc.mongodb.net/nagidb"


def do_line():
  SIZE = os.get_terminal_size()
  COL = SIZE.columns
  LINE = SIZE.lines
  print("-"*COL)

def word_line(word):
  SIZE = os.get_terminal_size()
  COL = SIZE.columns
  LINE = SIZE.lines
  actual_col = COL - len(word)
  halfofcol = actual_col / 2
  print("-"*int(halfofcol) + word + "-"*int(halfofcol))


while True:
	text = input('0g3 >>> ')
	if text.strip() == "": continue
	result, error = basic.run('<stdin>', text)

	if error:
		print(error.as_string())
	elif result and not isinstance(result, list):
		if len(result.elements) == 1:
			print(repr(result.elements[0])) 
		else:
			print(repr(result))
	else:
    ############################################### For Web3 ##########################################################
		start_time = time.time()
		#-------------------------------------------Og3--------------------------------------------------------
		end_time = time.time()
		#-----------------------------------mango----------------------------------------------------
		current_dir = os.path.dirname(os.path.abspath(__file__))
		parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
		og3datapath = os.path.join(parent_dir, 'CompilerResult.og3data')
		with open(og3datapath, 'w') as Data:
			Data.write(str(result))
   
		js_code = """
			const { NHFile } = require('zerog-da-sdk');
			const path = require('path');

			const asd = async () => {
				const filePath = path.resolve(__dirname, 'CompilerResult.og3data');
				const file = await NHFile.fromFilePath(filePath);
				const [tree, err] = await file.merkleTree();
				if (err === null) {
					console.log(tree.rootHash());
				}
				await file.close();
			}
			asd();
		"""
		upload(js_code, str(result))
		# Calculate the elapsed time
		elapsed_time = end_time - start_time
		if result[2].get('ack','') or result[2].get('ackBc','') :
			do_line()
		print("Program Executed within: " + str(result[1][8])+"s","\t\t\t Blockchain Execution Time: " + str(elapsed_time))
		do_line()
  