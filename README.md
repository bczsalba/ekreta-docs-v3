# ekreta-docs v3

### Notice: I no longer have access to a Kreta account. As such, I am looking for a maintainer to take over this project and allow it to remain up to date. <a href="mailto:bczsalba@gmail.com">Email me</a> for details!

Updated documentation for version 3 of the e-kreta API.

Most of the info here is based on [Filc's](https://github.com/filcnaplo/filcnaplo) source code and [boapps'](https://github.com/boapps/e-kreta-api-docs) v1 documentation, while the rest was hand tested.

The repository also contains a Python program to access most functions, and as a sort of example of usage.

## General Disclaimer
It seems that not all schools use the `ekreta.hu` API link. If you get an `HTTP 301 - Moved Permanently` response, try changing your domain to `e-kreta.hu` instead. ([#4](https://github.com/bczsalba/ekreta-docs-v3/issues/4))


## Kreta projects based on the new API
- [Filc](https://filcnaplo.hu): An unnofficial e-diary application for the e-Kreta system.
- [Asztal](https://github.com/bczsalba/asztal): Terminal-based e-Kreta client.
- [kreta-cli](https://github.com/daaniiieel/kreta-cli): A command line interface for KRÉTA's latest v3 api
- [Táblafilc](http://tablafilc.samunemeth.hu): A grade calculator program for students ([GitHub](https://github.com/samunemeth/tablafilc)).
<!-- above this line ^-->
To add your project to the list, create a pull request with it added.


## Table of contents
### 1. [Other projects](#other-kreta-projects-based-on-the-v2-api)
### 2. [Endpoints & API links](#kreta-endpoints--api-links)
 * [Endpoints](#class-based-representation-of-all-kreta-endpoints)
 * [Getting API links](#getting-current-api-links)
### 3. [Kreta schools](#getting-list-of-all-kreta-schools)
### 4. [Requesting access & refresh tokens](#access--refresh-token)
 * [Access token (Bearer)](#access-token)
 * [Refresh token](#refresh-token)
### 5. [Messages](#messages)
 * [Overview](#get-all-messages)
 * [Individual message info](#get-information-about-a-specific-message)
 * [Marking messages read](#marking-message-as-read)
### 6. [Pre-announced tests & exams](#get-pre-announced-tests--exams)
### 7. [Information about student](#get-information-about-student)
### 8. [Student values](#get-evaluations-absences--timetable)
 * [Evaluations](#--evaluations)
 * [Absences](#--absences)
 * [Timetable](#--timetable)
### 9. [Other](#everything-else)



## Kreta Endpoints & API links
### Class-based representation of all Kreta Endpoints
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
    nonce = "/nonce"
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
        return "/v1/dokumentumok/uzenetek/$id"
    
    trashMessage = "/api/v1/kommunikacio/postaladaelemek/kuka"
    deleteMessage = "/api/v1/kommunikacio/postaladaelemek/torles"
```

### Getting current API links

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

## Getting list of all Kreta schools
May not work in languages with no lowercase header request, like Swift and Dart, see [BoA's note](https://github.com/boapps/e-kreta-api-docs#figyelem-ismert-probl%C3%A9m%C3%A1k-az-api-val).

```bash
curl -H "apiKey: 7856d350-1fda-45f5-822d-e1a2f3f1acf0"  https://kretaglobalmobileapi2.ekreta.hu:443/api/v3/Institute
```

**Response from server**
```bash
[
    {
        "instituteId": 0000,
        "instituteCode": "xxxxxxxxxxx",
        "name": "Xxxxx Xxxx Xxxxxx",
        "city": "Xxxxxx",
        "url": "https://xxxxxxxxxxx.e-kreta.hu",
        "advertisingUrl": "",
        "informationImageUrl": "https://kretamobile.blob.core.windows.net/advertisement/nati_app.gif",
        "informationUrl": "",
        "featureToggleSet": {}
    },
    ...
]
```

## Access & Refresh token

### Access token
Returns a Bearer authenticator to be used later for most requests. 

**NOTE:** Sometimes it seems to return a 502 error, not sure why or if it's a problem I can fix.

**NOTE:** To simplify the `X-AuthorizationPolicy-Key` and `X-AuthorizationPolicy-Nonce` header information, please refer to the `kreta_v2.py` file.

```bash
curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -H "User-Agent: hu.ekreta.student/1.0.5/Android/0/0" -H "X-AuthorizationPolicy-Key: xxx" -H "X-AuthorizationPolicy-Version: v2" -H "X-AuthorizationPolicy-Nonce: xxx" -d 'userName=xxxxxxxx&password=xxxxxxxxx&institute_code=xxxxxxxxx&grant_type=password&client_id=kreta-ellenorzo-mobile-android' https://idp.e-kreta.hu/connect/token
```

**Response from server:** 
```json 
{
 "access_token":"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
 "refresh_token": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
 ...
}
```

### Refresh token
With `grant_type=refresh_token` you can then refresh your access token:

```bash
curl -H "Content-Type: application/x-www-form-urlencoded" -H "User-Agent: hu.ekreta.student/1.0.5/Android/0/0" -d "institute_code=xxxxxxxxx&refresh_token=xxxxxxxxxxxx&grant_type=refresh_token&client_id=kreta-ellenorzo-mobile-android" https://idp.e-kreta.hu/connect/token
```

## Messages
### Get all messages
Requires the same headers as all GET requests, but also needs an endpoint that can be `beerkezett`, `elkuldott` or `torolt`.
```bash
curl -H 'Authorization: Bearer xxxxxxxx' -H 'User-Agent: hu.ekreta.student/1.0.5/Android/0/0' https://eugyintezes.e-kreta.hu/api/v1/kommunkacio/postaladaelemek/$type
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

### Get information about a specific message
The above method is limited in message length (I think to 100 characters), so this gets more info about a specific messages denoted by it's numeric `id`.

```bash
curl -H 'Authorization: Bearer xxxxxxxx' -H 'User-Agent: hu.ekreta.student/1.0.5/Android/0/0' https://eugyintezes.e-kreta.hu/api/v1/kommunkacio/postaladaelemek/$ID
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

### Marking message as read
*not sure yet*

## Get pre-announced tests & exams
```bash
curl -H 'Authorization: Bearer xxxxxxxx' -H 'User-Agent: hu.ekreta.student/1.0.5/Android/0/0' "https://"$ist"ekreta.hu.ellenorzo/V3/Sajat/BejelentettSzamonkeresek?datumTol=null"
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
]
```

## Get information about student

Used to be together with absences & evaluations, but has it since been separated with v2.

```bash
curl -H 'Authorization: Bearer xxxxxxxx' -H 'User-Agent: hu.ekreta.student/1.0.5/Android/0/0' "https://"$institute".ekreta.hu/ellenorzo/V3/Sajat/Adatlap"
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
  "Gondviselok": [
    {
      "EmailCim": "xxxxxxxxx@xxxxx.com",
      "Nev": "Xxxxxxx Xxxxxx",
      "Telefonszam": "+xxxxxxxxxxx",
      "IsTorvenyesKepviselo": true,
      "Uid": "xxxxx"
    }
  ],
  "IntezmenyAzonosito": "xxxxxxxxxx",
  "IntezmenyNev": "Xxxxxxxxxx Xxxxxxxxx",
  "Nev": "Xxxxx Xxxxx Xxxxx",
  "SzuletesiDatum": "2002-12-02T23:00:00Z",
  "SzuletesiEv": 2002,
  "SzuletesiHonap": 12,
  "SzuletesiNap": 02,
  "SzuletesiHely": "Xxxxxxx XX Xxxxx",
  "SzuletesiNev": "Xxxxx Xxxxx Xxxxx",
  "TanevUid": "0000",
  "Uid": "000000",
  "Bankszamla": {
    "BankszamlaSzam": null,
    "BankszamlaTulajdonosTipusId": null,
    "BankszamlaTulajdonosNeve": null,
    "IsReadOnly": false
  },
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
      "ErtekelesekMegjelenitesenekKesleltetesenekMerteke": 0,
      "KovetkezoTelepitesDatuma": "2021-05-04T19:00:00Z"
    }
  }
}
```

## Get Evaluations, Absences & Timetable
`$endpoint` refers to the data requested: `Ertekelesek`/`Mulasztasok`/`OrarendElemek`.

`datumTol` & `datumIg` is required for timetable, while optional for the other two.

```bash
curl -H 'Authorization: Bearer xxxxxxxx' -H 'User-Agent: hu.ekreta.student/1.0.5/Android/0/0' "https://"$institute".ekreta.hu/ellenorzo/V3/Sajat/"$endpoint"?datumTol=2020-09-01T00-00-00&datumIg=2020-09-08T00-00-00"
```


### Responses from server:
### - Evaluations:
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
### - Absences
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
### - Timetable
```json
[
  {
    "Allapot": {
      "Uid": "1,Naplozott",
      "Leiras": "Naplózott",
      "Nev": "Naplozott"
    },
    "BejelentettSzamonkeresUids": [],
    "BejelentettSzamonkeresUid": null,
    "Datum": "1970-01-01T00:00:00Z",
    "HelyettesTanarNeve": null,
    "IsTanuloHaziFeladatEnabled": false,
    "KezdetIdopont": "1970-01-01T00:00:00Z",
    "Nev": "xxxxxxx",
    "Oraszam": 0,
    "OraEvesSorszama": 0,
    "OsztalyCsoport": {
      "Uid": "000000",
      "Nev": "xxx xxx xxx"
    },
    "HaziFeladatUid": null,
    "IsHaziFeladatMegoldva": false,
    "TanarNeve": "Xxxxx Xxxxxx",
    "Tantargy": {
      "Uid": "000000",
      "Kategoria": {
        "Uid": "0000,xxxx_xxxx",
        "Leiras": "Xxxxx Xxxx",
        "Nev": "xxxx_xxxx"
      },
      "Nev": "Spanish"
    },
    "TanuloJelenlet": {
      "Uid": "0000,Xxxxx",
      "Leiras": "...",
      "Nev": "Xxxx"
    },
    "Tema": "...",
    "TeremNeve": "xxx",
    "Tipus": {
      "Uid": "0,XxxxxXxxx",
      "Leiras": "Xxxx Xxxx",
      "Nev": "XxxxxXxxx"
    },
    "Uid": "0000000,Xxxxxxxx,1970-01-01T00:00:00Z",
    "VegIdopont": "1970-01-01T00:15:00Z"
  },
  ...
]
```

## Everything else
I've only listed and examplified what I think is probably the most used parts, or ones with peculiarities.

Everything else listed in the [classes](#class-based-representation-of-all-kreta-endpoints) that's not mentioned should follow the same header format as seen [above](#get-evaluations-absences--timetable).

### Contributions & Questions welcome.
