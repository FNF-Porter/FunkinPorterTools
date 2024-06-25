from . import Utils, Constants
import json, logging
from pathlib import Path
from copy import deepcopy

class ChartMetadata:
	def __init__(self):
		self.version:str = "1.0.0"
		self.songName:str = "Unknown"
		self.artist:str = "Unknown"
		self.difficulties:list[str] = []

		self.player:str = "bf"
		self.girlfriend:str = "gf"
		self.opponent:str = "dad"
		self.stage:str = "stage"

		self.events:list = []
		self.charts:dict[str, dict] = {}
		self.scrollSpeed:dict[str, float] = {}

		self.timeChanges:list = []
		self.generatedBy:str = "FNF Mod Converter"

class ChartTemplate:

	rename = {}
	chartsFolder = ""

	def __init__(self, path: Path) -> None:
		self.path = path

		self.metadata = ChartMetadata()

		self.jsonData:dict = {}
		self.sampleChart:dict = {}

		self.create()

		logging.info(f"New chart was created!")

	def getValue(self, key:str, json:dict = None):
		if (json == None):
			json = self.sampleChart

		return json.get(self.rename.get(key, key), None)
	
	def updateMetadata(self, *keys:str) -> dict:
		for key in keys:
			value = self.getValue(key)

			if (value != None):
				setattr(self.metadata, key, value)
	
	def getSongData(self, json:dict) -> dict:
		return json
	
	def parseNoteData(self, json:dict) -> dict:
		return {}

	def parseDifficulty(self, file:str) -> str:
		return file

	def create(self) -> None:
		
		metadata = self.metadata
		difficulties:list[str] = metadata.difficulties
		unorderedDiffs = set()

		for file in self.path.iterdir():
			if not file.suffix == ".json":
				continue

			fileName = file.stem

			with open(file, "r") as f:
				fileJson = self.getSongData(json.load(f))

				if fileJson != None:
					difficulty = self.parseDifficulty(fileName)
					unorderedDiffs.add(difficulty)

					notes = self.parseNoteData(fileJson)

					metadata.charts[difficulty] = notes.get("notes")
					metadata.scrollSpeed[difficulty] = notes.get("scrollSpeed")

					self.sampleChart = fileJson

		for difficulty in Constants.DIFFICULTIES:
			if difficulty in unorderedDiffs:
				difficulties.append(difficulty)
				unorderedDiffs.remove(difficulty)

		difficulties.extend(unorderedDiffs)
		del unorderedDiffs

		self.updateMetadata("songName", "player", "girlfriend", "opponent", "stage")

		self.onCreate()

	def onCreate(self):
		pass

	@staticmethod
	def convertTo(chart):
		pass

class LegacyChart(ChartTemplate):

	rename = {
		"songName": "song",
		"player": "player1",
		"girlfriend": "gfVersion",
		"opponent": "player2"
	}

	def parseDifficulty(self, file: str) -> str:
		splitFile = file.split("-")
		fileLen = len(splitFile)

		if fileLen > 2:
			return splitFile[-1]
		elif fileLen > 1 and file != self.path.stem:
			return splitFile[1]

		return "normal"
	
	def getSongData(self, json: dict) -> dict:
		return json.get("song")
	
	def parseNoteData(self, json: dict):
		chart:dict = {"notes": [], "timeChanges": [], "events": [], "scrollSpeed": 1.0}
		noteSections:list = json.pop("notes")

		chart["scrollSpeed"] = json.get("speed")

		for section in noteSections:
			mustHit = section["mustHitSection"]

			for note in section.get("sectionNotes"):
				time = note[0]
				data = note[1]
				length = note[2]

				if not mustHit:
					data = (data + 4) % 8

				chart["notes"].append(Utils.note(time, data, length))

		return chart

class PsychChart(LegacyChart):
	pass

class BaseChart(ChartTemplate):

	@staticmethod
	def convert(cChart:ChartTemplate) -> dict:
		metadata = deepcopy(Constants.BASE_CHART_METADATA)
		chart = deepcopy(Constants.BASE_CHART)

		cMetadata = cChart.metadata

		# Shortcuts

		playData = metadata["playData"]
		characters = playData["characters"]

		metadata["songName"] = cMetadata.songName
		metadata["artist"] = cMetadata.artist
		
		playData["difficulties"] = cMetadata.difficulties
		playData["stage"] = Utils.stage(cMetadata.stage)

		characters["player"] = Utils.character(cMetadata.player)
		characters["girlfriend"] = Utils.character(cMetadata.girlfriend)
		characters["opponent"] = Utils.character(cMetadata.opponent)

		for diff in cMetadata.difficulties:
			playData["ratings"][diff] = 0
			chart["scrollSpeed"][diff] = cMetadata.scrollSpeed[diff]
			chart["notes"][diff] = cMetadata.charts[diff]

		return {"m": metadata, "c": chart}

"""
class ChartObject:
	"" "
	A convenient way to store chart metadata.

	Args:
		path (str): The path where the song's chart data is stored.
	"" "
	def __init__(self, path: str) -> None:
		self.songPath = path
		self.songName:str = os.path.basename(path)

		self.difficulties:list = []
		self.metadata:dict = Constants.BASE_CHART_METADATA.copy()
		self.psychCharts:dict = {}

		self.chart:dict = Constants.BASE_CHART.copy()

		self.initCharts()
		self.setMetadata()

		logging.info(f"Chart for {self.metadata.get('songName')} was created!")

	def initCharts(self):
		charts = self.psychCharts
		difficulties = self.difficulties

		unorderedDiffs = set()

		for file in os.listdir(self.songPath):
			if not file.endswith(".json"):
				continue
			
			fileName = file[:-5]
			splitFile = fileName.split("-")
			fileLen = len(splitFile)

			difficulty = "normal"

			if fileLen > 2:
				difficulty = splitFile[-1]
			elif fileLen > 1 and fileName != self.songName:
				difficulty = splitFile[1]

			with open(os.path.join(self.songName, file), "r") as f:
				fileJson = json.load(f).get("song")

				if fileJson == None:
					continue

				unorderedDiffs.add(difficulty)
				charts[difficulty] = fileJson

		for difficulty in Constants.DIFFICULTIES:
			if difficulty in unorderedDiffs:
				difficulties.append(difficulty)
				unorderedDiffs.remove(difficulty)

		difficulties.extend(unorderedDiffs)
		del unorderedDiffs

	def setMetadata(self):
		# Chart used to get character data (ASSUMING all charts use the same characters and stages)
		sampleChart = self.psychCharts.get(self.difficulties[0])
		metadata = self.metadata

		ratings:dict = {}

		for diff in self.difficulties:
			ratings[diff] = 0

		metadata["songName"] = sampleChart.get("song").replace("-", " ").title()

		metadata["playData"]["difficulties"] = self.difficulties
		metadata["playData"]["characters"]["player"] = Utils.character(sampleChart.get("player1"))
		metadata["playData"]["characters"]["girlfriend"] = Utils.character(sampleChart.get("gfVersion", sampleChart.get("player3")))
		metadata["playData"]["characters"]["opponent"] = Utils.character(sampleChart.get("player2"))
		metadata["playData"]["stage"] = Utils.stage(sampleChart.get("stage"))

		metadata["ratings"] = ratings
		metadata["timeChanges"].append(Utils.timeChange(0, sampleChart.get("bpm"), 4, 4, 0, [4, 4, 4, 4]))

		self.stepCrochet = 15000 / sampleChart.get("bpm")
		self.sampleChart = sampleChart

	def convert(self):
		logging.info(f"Chart conversion for {self.metadata.get('songName')} started!")

		for diff, chart in self.psychCharts.items():
			self.chart["scrollSpeed"][diff] = chart.get("speed")
			self.chart["notes"][diff] = []

			notes = self.chart["notes"][diff]

			for section in chart.get("notes"):
				mustHit = section["mustHitSection"]

				for note in section.get("sectionNotes"):
					if not mustHit: # gonna improve this tomorrow too lazy to think tonight
						if note[1] > 3:
							note[1] -= 4
						else:
							note[1] += 4

					notes.append(Utils.note(note[0], note[1], note[2]))

		events = self.chart["events"]
		prevMustHit = self.sampleChart["notes"][0]["mustHitSection"]
		events.append(Utils.focusCamera(0, prevMustHit))

		steps = 0

		for section in self.sampleChart.get("notes"):
			mustHit = section["mustHitSection"]
			if (prevMustHit != mustHit):
				events.append(Utils.focusCamera(steps * self.stepCrochet, mustHit))
				prevMustHit = mustHit

			steps += section["sectionBeats"] * 4

		logging.info(f"Chart conversion for {self.metadata.get('songName')} was completed!")

	def save(self):
		savePath = os.path.join("output", self.songName)

		with open(os.path.join(savePath, f'{self.songName}-metadata.json'), 'w') as f:
			json.dump(self.metadata, f, indent=2)

		with open(os.path.join(savePath, f'{self.songName}-chart.json'), 'w') as f:
			json.dump(self.chart, f, indent=2)

		logging.info(f"Saving {self.metadata.get('songName')} to {savePath}")
"""