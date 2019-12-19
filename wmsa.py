#~@b1n4r1b01

import idaapi, idc, plistlib
import os, inspect

LINE_COLOR = 0xE3BEDD
FILE_COLOR = 0x00FF00


def decodehash(hash):
	cur_file = inspect.getsourcefile(lambda: 0)			# https://github.com/NeatMonster/AMIE
	cur_path = os.path.dirname(os.path.abspath(cur_file))
	list = "hash.plist"
	pl = plistlib.readPlist(os.path.join(cur_path, list))
	try:
		file = pl[hash]
		return file
	except:
		return -1

def dostuff():
	count = 0
	adr = idaapi.get_imagebase()
	end = idc.get_segm_attr(adr, idc.SEGATTR_END)
	while(adr < end):

		ins = idc.GetMnem(adr)
		ln = idc.GetOpnd(adr, 1)[1:]
		if ins == "MOV" and idc.GetOpnd(adr, 0) == "W8" and int(ln, 16) < 0xFFF and int(ln, 16) > 0xA and "AA" not in ln:
																				#there are comments at top rite?	#-ftrivial-auto-var-init=pattern
			SetColor(adr, CIC_ITEM, LINE_COLOR)

		if ins == "MOVE":
			hash = (idc.GetOpnd(adr, 1)[1:])
			if len(str(hash)) >= 16 and len(str(hash)) < 20 and hash > 0xF000000000000000:
					file = decodehash(hash)
					if file != -1:
						isn = "WMSA            "+file
						set_manual_insn(adr, isn)
						SetColor(adr, CIC_ITEM, FILE_COLOR)
						count+=1
		adr+=4

	print "[WMSA] Total hashes decoded (non-unique) : " + str(count)


class stuff(idaapi.plugin_t):

	flags = idaapi.PLUGIN_HIDE
	comment = "Wouldn't have existed without Jacques Fortier and team"
	help = "" 
	wanted_name = "WMSA: Where My Strings At?"
	wanted_hotkey = ""

	def init(self):
		dostuff()
		return 0

	def term(self):
		pass
	def run(self, arg):
		pass


def PLUGIN_ENTRY():
	return stuff()
