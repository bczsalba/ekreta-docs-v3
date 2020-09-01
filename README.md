# ekreta-docs-v2
Updated documentation for version 2 of the e-kreta API.

Most of the info here is based on [Filc's](https://github.com/filcnaplo/filcnaplo) source code, and [boapps'](https://github.com/boapps/e-kreta-api-docs) v1 documentation, while the rest was hand tested.

**Note:** All examples are written in Python3, and use the requests module. An example file with a User class is in the repo, so you can see everything working.

## Other Kreta projects based on the v2 API
- [Filc](https://filcnaplo.hu): *<description needed\>*

To add your project to the list, create a pull request with it added.
## Class-based representation of all Kreta Endpoints
*taken from Filc's source*
```python 
class Kreta:
    def base(ist):
        return f"https://{ist}.ekreta.hu"
    IDP = "https://idp.e-kreta.hu"
    ADMIN = "https://eugyintezes.e-kreta.hu"
    FILES = "https://files.e-kreta.hu"

class KretaEndpoints:
    token = "/connect/token"
    notes = "/ellenorzo/V3/Sajat/Feljegyzesek"
    events = "/ellenorzo/V3/Sajat/FaliujsagElemek"
    student = "/ellenorzo/V3/Sajat/TanuloAdatlap"
    evaluations = "/ellenorzo/V3/Sajat/Ertekelesek"
    absences = "/ellenorzo/V3/Sajat/Mulasztasok"
    groups = "/ellenorzo/V3/Sajat/OsztalyCsoportok"
    classAverages = "/V3/Sajat/Ertekelesek/Atlagok/OsztalyAtlagok"
    timetable = "/ellenorzo/V3/Sajat/OrarendElemek"
    announcedTests = "/ellenorzo/V3/Sajat/BejelentettSzamonkeresek"
    homeworks = "/ellenorzo/V3/Sajat/HaziFeladatok"
    homeworkDone = "/ellenorzo/V3/Sajat/HaziFeladatok/Megoldva"
    capabilities = "/ellenorzo/V3/Sajat/Intezmenyek"

class AdminEndpoints:
    sendMessage = "/api/v1/kommunikacio/uzenetek"
    def getAllMessages(endpoint):
        return f"/api/v1/kommunikacio/postaladaelemek/{endpoint}"
    def getMessage(id):
        return f"/api/v1/kommunikacio/postaladaelemek/{id}"
   
    recipientCategories = "/api/v1/adatszotarak/cimzetttipusok"
    availableCategories = "/api/v1/kommunikacio/cimezhetotipusok"
    recipientsTeacher = "/api/v1/kreta/alkalmazottak/tanar"

    uploadAttachment = "/ideiglenesfajlok"
    def downloadAttachment(id):
        return "/v1/dokumentumok/uzenetek/$id";
    
    trashMessage = "/api/v1/kommunikacio/postaladaelemek/kuka"
    deleteMessage = "/api/v1/kommunikacio/postaladaelemek/torles"
```

## Getting list of all Kreta schools
May not work in languages with no lowercase header request, like Swift and Dart, see [BoA's note](https://github.com/boapps/e-kreta-api-docs#figyelem-ismert-probl%C3%A9m%C3%A1k-az-api-val).

**<incomplete\>**

## Getting API links
Useful so that if the api links change you don't have to update your app. 
(*found by [thegergo02](https://github.com/thegergo02)*)

**Response from server:**
```json
{
  "GlobalMobileApiUrlDEV": "https://kretaglobalmobileapiuat.ekreta.hu",
  "GlobalMobileApiUrlTEST": "https://kretaglobalmobileapitest.ekreta.hu",
  "GlobalMobileApiUrlUAT": "https://kretaglobalmobileapiuat.ekreta.hu",
  "GlobalMobileApiUrlPROD": "https://kretaglobalmobileapi2.ekreta.hu"
}
```

Technically it is available from a [normal browser](http://kretamobile.blob.core.windows.net/configuration/ConfigurationDescriptor.json) as well.

## Login & Getting access token
Returns a Bearer authenticator to be used later for most requests. 

**NOTE:** Sometimes it seems to return a 502 error, not sure why or if it's a problem I can fix.
```python
# headers & data here are special to the token operations
# get access token
response = requests.post(
	"https://idp.e-kreta.hu/connect/token",
        headers={
		"Content-Type": "application/x-www-form-urlencoded",
		"User-Agent": "hu.ekreta.student/1.0.5/Android/0/0"
	},
        data={
		"userName": "xxxxxxxxxx",
		"password": "xxxxxxxxxx",
	        "institute_code": "xxxxxxxxxx",
	        "grant_type": "password",
	        "client_id": "kreta-ellenorzo-mobile"
	}
)
```
**Response from server:**
```json
{
 "access_token":"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
 "refresh_token": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
 ...
}
```

With `grant_type=refresh_token` you can get refresh your access token:
```python
# refresh access token
response = requests.post(
	"https://idp.e-kreta.hu/connect/token",
        headers={
		"Content-Type": "application/x-www-form-urlencoded",
		"User-Agent": "hu.ekreta.student/1.0.5/Android/0/0"
	},
        data={
	        "institute_code": "xxxxxxxxxx",
	        "grant_type": "refresh_token",
	        "refresh_token": "xxxxxxxxxxx",
	        "client_id": "kreta-ellenorzo-mobile"
	}
)
```
## Get all messages
Requires a type to select endpoint, otherwise is the same as most requests.

```python
#type: beerkezett/elkuldott/torolt
response = requests.get(
		f"https://eugyintezes.e-kreta.hu/api/v1/kommunikacio/postaladaelemek/{type}",
		headers={
			"Authorization": "Bearer xxxxxxxxxx",
			"User-Agent": "hu.ekreta.student/1.0.5/Android/0/0"
		}
```
 **Response from server:**
```json
[
	{
		"azonosito": 0000000,
		"uzenetAzonosito": 000000,
		"uzenetKuldesDatum":"1970-01-01T00:00:00",
		"uzenetFeladoNev":"Xxxxx Xxxxx",
		"uzenetFeladoTitulus":"xxxxxxxxxx",
		"uzenetTargy":"xxxxxxxxx",
		"hasCsatolmany":false,
		"isElolvasva":true
	},
   ...
]
```

## Get information about a specific message
The above method is limited in message length (I think at 100 characters), so this gets more info about a specific message.

```python
# id: numeric "azonosito" value of message
response = requests.get(
	"https://eugyintezes.e-kreta.hu/api/v1/kommunikacio/postaladaelemek/{id}",
	headers={
		"Authorization": "Bearer xxxxxxxxxx",
		"User-Agent": "hu.ekreta.student/1.0.5/Android/0/0"
	}
)
```

### Important notes:
- `cimzettLista` can have either a student or a class value (as far as I can tell).


**Response from server:**

```json
{
	"azonosito": 0000000,
	"isElolvasva":true,
	"isToroltElem":false,
	"tipus": {
		"azonosito":1,
		"kod":"BEERKEZETT",
		"rovidNev":"Beérkezett üzenet",
		"nev":"Beérkezett üzenet",
		"leiras":"Beérkezett üzenet"
	},
	"uzenet": {
		"azonosito":0000000,
		"kuldesDatum": "1970-01-01T00:00:00",
		"feladoNev":"Dudás Attila",
		"feladoTitulus":"igazgató h.",
		"szoveg":"...",
		"targy":" Tájékoztató ",
		"statusz": {
			"azonosito":2,
			"kod":"KIKULDVE",
			"rovidNev": "Kiküldve",
			"nev":"Kiküldve",
			"leiras":"Kiküldve"
		},
		"cimzettLista": 
		[
			{
				"azonosito": 0000000,
				"kretaAzonosito": 00000,
				"nev":"9.A",
				"tipus": {
					"azonosito":4,
					"kod":"OSZTALY_TANULO",
					"rovidNev":"Osztály - Tanuló",
					"nev":"Osztály - Tanuló",
					"leiras":"Osztály - Tanuló"
				}
			},
			{
				"azonosito":0000000,
				"kretaAzonosito": 000000,
				"nev": "Xxxxxxx Xxxxxxx",
				"tipus": {
					"azonosito":9,
					"kod":"TANAR",
					"rovidNev":"Tanár",
					"nev":"Tanár",
					"leiras":"Tanár"
				}
			},
			...
		],
		"csatolmanyok": [
			{
	                    "azonosito": 0000000,
	                    "fajlNev": "xxxxxxx.xxx"
	                },
			...
		]
	}
}
```

## Marking message as read
*not sure yet*

## Get pre-announced tests & exams

```python
response = requests.get(
	f"{ist}.ekreta.hu/ellenorzo/V3/Sajat/BejelentettSzamonkeresek",
	headers={
		"Authorization": "Bearer xxxxxxxxxx",
		"User-Agent": "hu.ekreta.student/1.0.5/Android/0/0"
	},
	params={
		"datumTol": "1970-01-01T00:00:00"
	}
)
```
### Important notes: 
- `datumTol` is an optional parameter, without it the server returns all.
- I only have `irasbeli_temazaro_dolgozat` as a type, but logically there should be stuff like `szobeli_feleles` and others.


**Response from server:** 
```json
[
  {
    "BejelentesDatuma": "1970-01T00:00:00Z",
    "Datum": "2019-10-08T22:00:00Z",
    "Modja": {
      "Uid": "0000,irasbeli_temazaro_dolgozat",
      "Leiras": "Írásbeli témazáró dolgozat",
      "Nev": "irasbeli_temazaro_dolgozat"
    },
    "OrarendiOraOraszama": 1,
    "RogzitoTanarNeve": "Kókai Mária",
    "TantargyNeve": "Mathematics",
    "Temaja": "Combinatorics and graphs",
    "OsztalyCsoport": {
      "Uid": "88429"
    },
    "Uid": "784"
  },

```

## Get information about student

Used to be together with absences & evaluations, has since been separated with v2.
 
```python
response = requests.get(
        f"{ist}.ekreta.hu/ellenorzo/V3/Sajat/Adatlap",
        headers = { 
		"Authorization": "Bearer xxxxxxxxxx",
		"User-Agent": "hu.ekreta.student/1.0.5/Android/0/0"
	}
)
```


### Important notes:
- `"SzuletesiDatum"` represents 00:00 of the given date, but is in UTC time: `YYYY-MM-(DD-1)T23:00:00Z`.
- `"TestreszabhatoBeallitasok"` shows if the school allows things like student-submitted homeworks, showing themes of lessons, displaying class averages or even a global delay in evaluations showing up for whatever reason.

**Response from server**
```json
{
  "AnyjaNeve": "Xxxxxx Xxxxxx",
  "Cimek": [
    "City (Postcode), Street Number",
    "Xxxx (0000), Xxxxxx street 0"
  ],
  "Gondviselok": [],
  "IntezmenyAzonosito": "xxxxxxxxxx",
  "IntezmenyNev": "Xxxxxxxxxx Xxxxxxxxx",
  "Nev": "Xxxxx Xxxxx Xxxxx",
  "SzuletesiDatum": "2002-12-02T23:00:00Z",
  "SzuletesiHely": "Xxxxxxx XX Xxxxx",
  "SzuletesiNev": "Xxxxx Xxxxx Xxxxx",
  "TanevUid": "0000",
  "Uid": "000000",
  "Intezmeny": {
    "Uid": "0000",
    "RovidNev": "xxxxxxxxxx",
    "Rendszermodulok": [
      {
        "IsAktiv": true,
        "Tipus": "Eugyintezes"
      }
    ],
    "TestreszabasBeallitasok": {
      "IsDiakRogzithetHaziFeladatot": false,
      "IsTanorakTemajaMegtekinthetoEllenorzoben": true,
      "IsOsztalyAtlagMegjeleniteseEllenorzoben": false,
      "ErtekelesekMegjelenitesenekKesleltetesenekMerteke": 0
    }
  }
}
```

## Get Evaluations, Absences & Timetable
All three are acquired the same way so I'll group them together.   
Each return an array with elements in the format shown here.

```python
#endpoint: "Ertekelesek"/"Mulasztasok"/"OrarendElemek"
response = requests.get(
		f"https://{ist}.ekreta.hu/ellenorzo/V3/Sajat/{endpoint}",
		headers={
		"Authorization": "Bearer xxxxxxxxxx",
		"User-Agent": "hu.ekreta.student/1.0.5/Android/0/0"
		}
		
		# obligatory for timetable, optional for others
		params={
			"fromDate": "2020-09-01T00-00-00",
			"toDate": "2020-09-08T00-00-00"
		}
)
```

#### Response from server:
- Evaluations:
	```json
	[
		{
		    "ErtekeloTanarNeve": "Xxxxx Xxxxx",
		    "ErtekFajta": {
		      "Uid": "0,Osztalyzat",
		      "Leiras": "Elégtelen (1) és Jeles (5) között az öt alapértelmezett érték",
		      "Nev": "Osztalyzat"
		    },
		    "Jelleg": "Ertekeles",
		    "KeszitesDatuma": "1970-01-01T00:00:00Z",
		    "LattamozasDatuma": null,
		    "Mod": {
		      "Uid": "0000,type_of_eval",
		      "Leiras": "Type of Eval",
		      "Nev": "type_of_eval"
		    },
		    "RogzitesDatuma": "1970-01-01T00:00:00Z",
		    "SulySzazalekErteke": 100,
		    "SzamErtek": 0,
		    "SzovegesErtek": "Szöveg(0)",
		    "SzovegesErtekelesRovidNev": null,
		    "Tantargy": {
		      "Uid": "000000",
		      "Kategoria": {
		        "Uid": "0000,subject",
		        "Leiras": "Subject",
		        "Nev": "subject"
		      },
		      "Nev": "Subject"
		    },
		    "Tema": "...",
		    "Tipus": {
		      "Uid": "0000,evkozi_jegy_ertekeles",
		      "Leiras": "Évközi jegy/értékelés",
		      "Nev": "evkozi_jegy_ertekeles"
		    },
		    "OsztalyCsoport": {
		      "Uid": "00000"
		    },
		    "Uid": "00000000,Ertekeles"
		},
		...
	]
	```
	#### Important Notes:
	- `type_of_eval` seems to have the same values possible as Pre-Announced
	- `Leiras` looks to be the way to differentiate mid/half/endyear grades
	- `SulySzazalekErteke` is usually 100/200, but I've seen end of term grades registered at 150 so it's better to code it flexibly.
- Absences
	```json
	[
		{
		    "IgazolasAllapota": "Igazolt",
		    "IgazolasTipusa": {
		      "Uid": "0000,szuloi_igazolas",
		      "Leiras": "Szülői igazolás",
		      "Nev": "szuloi_igazolas"
		    },
		    "KesesPercben": null,
		    "KeszitesDatuma": "1970-01-01T00:00:00Z",
		    "Mod": {
		      "Uid": "1,Tanorai",
		      "Leiras": "Tanórai mulasztás",
		      "Nev": "Tanorai"
		    },
		    "Datum": "1970-01-01T00:00:00Z",
		    "Ora": {
		      "KezdoDatum": "1970-01-01T08:30:00Z",
		      "VegDatum": "2020-09-01T00:00:00Z",
		      "Oraszam": 5
		    },
		    "RogzitoTanarNeve": "Xxxxx Xxxxx",
		    "Tantargy": {
		      "Uid": "000000",
		      "Kategoria": {
		        "Uid": "0000,subject_name",
		        "Leiras": "Subject Name",
		        "Nev": "subject_name"
		      },
		      "Nev": "subject name"
		    },
		    "Tipus": {
		      "Uid": "0000,hianyzas",
		      "Leiras": "Hiányzás",
		      "Nev": "hianyzas"
		    },
		    "OsztalyCsoport": {
		      "Uid": "00000"
		    },
		    "Uid": "00000000"
		},
		...
	] 
	```
	#### Important notes:
	- `Oraszam` refers to the index of the lesson starting from 1.
	- `Leiras` again likely has a multitude of possible values that I cannot test.
- Timetable
	
	>I don't have a timetable yet as of v2, will update as soon as I do.

## Everything else
I've only listed and examplified what I think is probably the most used parts, or ones with peculiarities.

Everything else listed in the [classes](#class-based-representation-of-all-kreta-endpoints) that's not mentioned should follow the same header format as seen [above](#get-evaluations-absences--timetable).

### Contributions & Questions welcome.
