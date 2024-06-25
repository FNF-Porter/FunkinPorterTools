"""
A class full of constants needed for chart conversion.
"""

DIFFICULTIES:list[str] = ["easy", "normal", "hard"]

STAGES:dict[str, str] = {
	"stage": "mainStage"
}

CHARACTERS:dict[str, str] = {
	"pico-player": "pico-playable"
}

CHART_METADATA = {
	"version": "1.0.0",
	"songName": "Unknown",
	"artist": "Unknown",

	"difficulties": [],
	"player": "bf",
	"girlfriend": "gf",
	"opponent": "dad",
	"stage": "stage",

	"timeChanges": [],
	"generatedBy": "FNF Mod Converter"
}

BASE_CHART_METADATA = {
	"version": "2.2.0",
	"songName": "Unknown",
	"artist": "Unknown",
	"looped": False,

	"offsets": {
		"instrumental": 0,
		"altInstrumentals": {},
		"vocals": {}
	},

	"playData": {
		"album": "volume1",
		"previewStart": 0,
		"previewEnd": 15000,
		"songVariations": [],
		"difficulties": [],
		"characters": {
			"player": "bf",
			"girlfriend": "gf",
			"opponent": "dad",
			"instrumental": "",
			"altInstrumentals": []
		},
		"stage": "mainStage",
		"noteStyle": "funkin",
		"ratings": {}
	},

	"timeFormat": "ms",
	"timeChanges": [],
	"generatedBy": "FNF Mod Converter"
}

BASE_CHART = {
	"version": "2.0.0",
	"scrollSpeed": {},
	"events": [],
	"notes": {},
	"generatedBy": "FNF Mod Converter"
}

CHARACTER = {
	"version": "1.0.0",
	"name": None,
	"assetPath": None,
	"singTime": None,
	"isPixel": None,
	"scale": None,
	"healthIcon": {
		"id": None,
		"isPixel": None,
		"flipX": False,
		"scale": 1
	},
	"animations": []
}

ANIMATION = {
	"name": None,
	"prefix": None,
	"offsets": [0, 0]
}