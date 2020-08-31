# ekreta-docs-v2
Updated documentation for version 2 of the e-kreta API.

Most of the info here is based on [boapps'](https://github.com/boapps/e-kreta-api-docs) v1 documentation and [Filc's](https://github.com/boapps/filcnaplo/filcnaplo) source code, while the rest was hand tested.

# Other Kreta projects based on the v2 API
- [Filc](https://filcnaplo.hu): *<description needed\>*

To add your project to the list, create a pull request with it added.
# Class-based representation of all Kreta Endpoints
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
    exams = "/ellenorzo/V3/Sajat/BejelentettSzamonkeresek"
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

# Getting list of all Kreta schools
May not work in languages with no uppercase header request, like Swift and Dart, see [BoA's note](https://github.com/boapps/e-kreta-api-docs#figyelem-ismert-probl%C3%A9m%C3%A1k-az-api-val).

TO BE CONTINUED
