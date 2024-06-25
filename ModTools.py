from abc import ABC
from typing import Generic, TypeVar

from pathlib import Path

from . import Objects

T = TypeVar("T")

class BaseRegistry(ABC, Generic[T]):

	def __init__(self, id:str, dataPath:Path) -> None:
		
		self.id = id
		self.path = dataPath

		self.entries:dict[str, T] = {}

	def listData(self) -> list:
		return []

	def createData(self, obj):
		return None

	def loadEntries(self) -> None:
		objects = self.listData()

		for obj in objects:
			try:
				entry = self.createData(obj)
			except Exception as e:
				print("OOPS!", e)
			
			if entry != None:
				self.entries[obj] = entry
	
	def clearEntries(self) -> None:
		for entry in self.entries:
			del entry
		
		self.entries.clear()

	def getEntry(self, name:str):
		return self.entries.get(name, None)

class Mod:

	def __init__(self, name:str, path:str = ""):
		self.name = name
		self.path = name

		self.songs = SongRegistry(self)
		self.songs.loadEntries()

	def getSongs(self):
		return list(self.songs.entries.keys())

class SongRegistry(BaseRegistry[Objects.ChartTemplate]):

	def __init__(self, mod:Mod):
		self.mod = mod
		super().__init__("SONG", Path(mod.path, "data"))

	def listData(self) -> list:
		array = []

		for item in self.path.iterdir():
			if item.is_dir():
				array.append(item.name)

		return array
	
	def createData(self, obj):
		return Objects.PsychChart(self.path / obj)