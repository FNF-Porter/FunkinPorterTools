from abc import ABC
from typing import Generic, TypeVar

from pathlib import Path

from . import Objects

T = TypeVar("T")

class BaseRegistry(ABC, Generic[T]):

	instance = None

	def __init__(self, id:str, dataPath:str) -> None:
		
		self.id = id
		self.path = dataPath

		self.entries:dict[str, T] = {}

		self.instance = self

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

class SongRegistry(BaseRegistry[Objects.ChartTemplate]):

	def __init__(self):
		super().__init__("SONG", "data")

	def listData(self) -> list:
		array = []

		for item in Path(ModManager.modName, self.path).iterdir():
			if item.is_dir():
				array.append(item.name)

		return array
	
	def createData(self, obj):
		return Objects.PsychChart(Path(ModManager.modName) / self.path / obj)

class ModManager:

	modName = ""
	songs = SongRegistry()

	@staticmethod
	def setup(modName:str):
		ModManager.modName = modName
		ModManager.songs.loadEntries()

	@staticmethod
	def getSongs():
		return list(ModManager.songs.entries.keys())