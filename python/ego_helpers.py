#!/usr/bin/python3

import os
import json
import glob
import importlib.machinery
import sys

# Ego Helpers module.
#
# Copyright 2017 Daniel Robbins and Funtoo Solutions, Inc.
# See LICENSE.txt for terms of distribution. 

def get_install_path(settings):
	if "global" in settings and "install_path" in settings["global"]:
		return settings["global"]["install_path"]
	else:
		return "/usr/share/ego"

def get_ego_module(install_path, modname):
	loader = importlib.machinery.SourceFileLoader(modname, '%s/modules/%s.ego' % (install_path, modname))
	try:
		return loader.load_module()
	except FileNotFoundError:
		return None

def run_ego_module(install_path, modname, config, args):
	mod = get_ego_module(install_path, modname)
	if mod:
		mod.main(install_path, config, args)
	else:
		print(color.RED + "Error: ego module \"%s\" not found." % modname + color.END)
		sys.exit(1)

class EgoConfig(object):

	def __init__(self, root, settings):
		self.ego_dir = root
		self.ego_mods_dir = "%s/modules" % self.ego_dir
		self.ego_mods_info_dir = "%s/modules-info" % self.ego_dir
		self.ego_mods = []
		self.ego_mods_info = {}
		if os.path.isdir(self.ego_mods_dir):
			for match in glob.glob(self.ego_mods_dir + "/*.ego"):
				self.ego_mods.append(match.split("/")[-1][:-4])
		for mod in self.ego_mods:
			inf_path = self.ego_mods_info_dir + "/" + mod + ".json"
			if os.path.exists(inf_path):
				with open(inf_path,"r") as inf:
					self.ego_mods_info[mod] = json.loads(inf.read())
			else:
				self.ego_mods_info[mod] = {}
		self.settings = settings

	def available_modules(self):
		for x in self.ego_mods:
			yield x, self.ego_mods_info[x]

class ColorType(str):
	pass

class color:
	PURPLE = ColorType('\033[95m')
	CYAN = ColorType('\033[96m')
	DARKCYAN = ColorType('\033[36m')
	DARKBLUEBG = ColorType('\033[48;5;018m')
	BLUE = ColorType('\033[94m')
	GREEN = ColorType('\033[92m')
	YELLOW = ColorType('\033[93m')
	RED = ColorType('\033[91m')
	BOLD = ColorType('\033[1m')
	UNDERLINE = ColorType('\033[4m')
	END = ColorType('\033[0m')
	AUTOFLUSH = ColorType("")

def header(info):
	print("\n=== "+color.BOLD+color.GREEN+info+color.END+": ===\n")

# vim: ts=4 sw=4 noet
