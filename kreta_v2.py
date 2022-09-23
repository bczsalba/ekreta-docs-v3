#!/usr/bin/env python3
# Made in 2020 by https://github.com/bczsalba
# MIT License
import requests,json,hmac,base64,hashlib,datetime


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
        return "/v1/dokumentumok/uzenetek/$id";  

    trashMessage = "/api/v1/kommunikacio/postaladaelemek/kuka"
    deleteMessage = "/api/v1/kommunikacio/postaladaelemek/torles"


class User:
    def __init__(self,usr,pwd,ist,fromDate=None,toDate=None):
        self.usr = usr
        self.pwd = pwd
        self.ist = ist
        
        # userAgent and clientID
        self.userAgent = "hu.ekreta.student/1.0.5/Android/0/0"
        self.clientID = "kreta-ellenorzo-mobile-android"

        self.bearer = self.getToken()
        
        # headers used for operation other than token
        self.headers = {
            "Authorization": f"Bearer {self.bearer}",
            "User-Agent": self.userAgent
        }

    def getToken(self):
        # gets access token
        # headers: special to token
        key = bytes([98, 97, 83, 115, 120, 79, 119, 108, 85, 49, 106, 77])
        nonce = (requests.get(Kreta.IDP+KretaEndpoints.nonce)).text
        message = bytes(self.ist.upper()+nonce+self.usr.upper(), 'utf-8')
        dig = hmac.HMAC(key, message, hashlib.sha512).digest()
        generated = base64.b64encode(dig).decode()
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "User-Agent": "hu.ekreta.student/1.0.5/Android/0/0", 
            "X-AuthorizationPolicy-Key" : generated, 
            "X-AuthorizationPolicy-Version" : "v2", 
            "X-AuthorizationPolicy-Nonce" : nonce}

        # data to send
        data = {
            "userName": self.usr,
            "password": self.pwd,
            "institute_code": self.ist,
            "grant_type": "password",
            "client_id": self.clientID
        }
        
        # url: https://idp.e-kreta.hu/connect/token
        response = requests.post(
                Kreta.IDP+
                KretaEndpoints.token,
                headers=headers,
                data=data
        )

        try:
            return json.loads(response.text)["access_token"]
        except KeyError:
            # occasionally it gives a 502 error
            return response.text

    def getEvaluations(self):
        # returns evaluations (technically has a from-to data optional parameter)
        # url: https://{ist}.ekreta.hu/ellenorzo/V3/Sajat/Ertekelesek
        response = requests.get(
                Kreta.base(self.ist)+KretaEndpoints.evaluations,
                headers=self.headers
        )
        evaluations = sorted(response.json(), key=lambda x: datetime.datetime.strptime(x['KeszitesDatuma'], '%Y-%m-%dT%H:%M:%SZ'), reverse=True)
        return evaluations
    
    def getAbsences(self):
        # url: https://{ist}.ekreta.hu/ellenorzo/V3/Sajat/Mulasztasok
        response = requests.get(
                Kreta.base(self.ist)+KretaEndpoints.absences,
                headers=self.headers
        )
        return response.text

    def getTimetable(self,fromDate,toDate):
        # returns array containing lessons from fromDate to toDate
        if not fromDate or not toDate:
            fromDate = "2020-09-01"
            toDate = "2020-09-08"

        # url: https://{ist}.ekreta.hu/ellenorzo/V3/Sajat/OrarendElemek
        response = requests.get(
                Kreta.base(self.ist)+KretaEndpoints.timetable,
                params = {
                            "datumTol": fromDate,
                            "datumIg": toDate
                },
                headers = self.headers
        )
        return response.text

    def getApiLinks(self):
        # not really needed for the class
        response = requests.get(
                "http://kretamobile.blob.core.windows.net/configuration/ConfigurationDescriptor.json"
                )
        return response.text

    def getMessages(self,typeOrId):
        # url: https://eugyintezes.e-kreta.hu/api/v1/kommunikacio/postaladaelemek/{typeOrId}
        response = requests.get(
                Kreta.ADMIN+AdminEndpoints.getAllMessages(typeOrId),
                headers=self.headers
        )
        return response.text
    
    def getAnnounced(self,date=None):
        # returns announced tests/exams
        params = ( {"datumTol": date } if date else None)
        response = requests.get(
        Kreta.base(self.ist)+KretaEndpoints.announcedTests,
                headers = self.headers,
                params = params
        )
        return response.text

    def getNotes(self,date=None):
        # returns announced tests/exams
        params = ( {"datumTol": date } if date else None)
        response = requests.get(
        Kreta.base(self.ist)+KretaEndpoints.notes,
                headers = self.headers,
                params = params
        )
        return response.text

    def getInfo(self):
        # returns info about the student
        response = requests.get(
                Kreta.base(self.ist)+KretaEndpoints.student,
                headers = self.headers,
        )
        return response.text

#--------------------------------------------------------------

if __name__ == "__main__":
    print(User('username','password','institute').getInfo())
