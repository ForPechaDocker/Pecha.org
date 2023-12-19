import urllib.request, urllib.error, urllib.parse
from urllib.error import HTTPError
import json
import os
from pprint import pprint
from time import sleep
from datetime import datetime
from bson import json_util

apikey = "DTtpkMoBgRQuXkZ2k9C9tqWHfd7vjA51hA8hbjkfwbs"
BASEPATH = os.path.dirname(os.path.abspath(__file__))   # path to `Pecha.org/tools`

#baseURL = "https://pecha.org/"
baseURL = "http://127.0.0.1:8000/"

baseURL = "https://pecha.org/"
#baseURL = "http://127.0.0.1:8000/"
#region APIs
def get_term(termSTR):
    """
    Get term values for variable `termSTR`.
        `termSTR`: str, term name
    """
    url = baseURL + "api/terms/" + urllib.parse.quote(termSTR)
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
        print(response.read().decode('utf-8'))
    except HTTPError as e:
        print('Error code: ', e.code)
        print(e.read().decode('utf-8'))


def post_term(termEnSTR, termHeSTR):
    """
    Post term for category in different language.
    You MUST post term before posting any category.
        `termEnSTR`: str, primary `en` term (chinese),
        `termHeSTR`: str, primary `he` term (བོད་ཡིག)
    """
    url = baseURL + "api/terms/" + urllib.parse.quote(termEnSTR)
    indexJSON = json.dumps({
        "name": termEnSTR,
        "titles": [
            {
                "text": termEnSTR,
                "lang": "en",
                "primary": True
            },
            {
                "text": termHeSTR,
                "lang": "he",
                "primary": True
            }
        ]
    })
    values = {
        'json': indexJSON, 
        'apikey': apikey,
        'update': True,
    }
    data = urllib.parse.urlencode(values)
    binary_data = data.encode('ascii')
    req = urllib.request.Request(url, binary_data, method="POST")
    try:
        response = urllib.request.urlopen(req)
        res = response.read().decode('utf-8')
        print(res)
        # term conflict
        if "error" in res and "A Term with the title" in res and "in it already exists" in res:
            return {"status": False, "term_conflict": res}
        return {"status": True}
    except HTTPError as e:
        print('Error code: ', e.code)
        print(e.read())
        return {"status": False, "error": e.read()}


def get_category(pathSTR):
    """
    Check full category path for variable `pathSTR`.
        `pathSTR`: str, example: "Indian Treatises/Madyamika/The way of the bodhisattvas"
    """
    url = baseURL + "api/category/" + urllib.parse.quote(pathSTR)
    req = urllib.request.Request(url, method="GET")

    try:
        response = urllib.request.urlopen(req)
        res = response.read().decode('utf-8')
        print(res)
        if "error" not in res:
            return True
        elif "already exists" in res["error"]:
            return True
        return False
    except HTTPError as e:
        print('Error code: ', e.code)
        print(e.read())
        return False


def post_category(pathLIST):
    """
    Post path for article categorizing.
    You MUST use post_term() before using post_category().
        `pathLIST`: list of str, 
    if you want to post path = "Indian Treatises/Madyamika/The way of the bodhisattvas"
        => post_category(["Indian Treatises"])
        => post_category(["Indian Treatises", "Madyamika"])
        => post_category(["Indian Treatises", "Madyamika", "The way of the bodhisattvas"])
    """
    url = baseURL + "api/category"
    category = {
        "sharedTitle": pathLIST[-1],
        "path": pathLIST
    }
    indexJSON = json.dumps(category)
    values = {
        'json': indexJSON, 
        'apikey': apikey
    }

    data = urllib.parse.urlencode(values)
    binary_data = data.encode('ascii')
    req = urllib.request.Request(url, binary_data)

    try:
        response = urllib.request.urlopen(req)
        res = response.read().decode('utf-8')
        print(res)
        if "error" not in res:
            return True
        elif "already exists" in res:
            return True
        return False
    except HTTPError as e:
        print('Error code: ', e.code)
        print(e.read())
        return False


def get_index(indexSTR):
    """
    Get Index information for article name `indexSTR`.
        `indexSTR`: str, article en name
    """
    url = "%s/%s?with_content_counts=1" % (baseURL + "api/v2/raw/index", indexSTR.replace(" ", "_"))
    req = urllib.request.Request(url, method="GET")
    try:
        response = urllib.request.urlopen(req)
        pprint(json.loads(response.read().decode('utf-8')))
    except HTTPError as e:
        print('Error code: ', e.code)
        print(e.read().decode('utf-8'))


def post_index(indexSTR, pathLIST, titleLIST):
    """
    Post index value for article settings.
        `indexSTR`: str, article title,
        `catLIST`: list of str, category list (see post_category() for example),
        `titleLIST`: list of json, title name in different language,
            titleLIST = {
                "lang": "en/he",
                "text": "Your en/he title",
                "primary": True (You must have a primary title for each language)
            }
    """
    url =  baseURL + "api/v2/raw/index/" + urllib.parse.quote(indexSTR.replace(" ", "_"))
    index = {
        "title" : indexSTR,
        "categories": pathLIST,
        "schema" : {
            "titles" : titleLIST,
            "key" : indexSTR,
            "nodeType" : "JaggedArrayNode",
            #"lengths" : [4, 50],
            "depth" : 2,
            "sectionNames" : ["Chapter", "Paragraph"],
            "addressTypes" : ["Integer", "Integer"]
        }
    }    
    indexJSON = json.dumps(index)
    values = {
        'json': indexJSON, 
        'apikey': apikey,
    }
    data = urllib.parse.urlencode(values)
    binary_data = data.encode('ascii')
    req = urllib.request.Request(url, binary_data)
    try:
        response = urllib.request.urlopen(req)
        res = response.read().decode('utf-8')
        print(res)
        if "error" in res and "already exists." not in res:
            return False
        return True
    except HTTPError as e:
        print('Error code: ', e.code)
        print(e.read())
        return False

def get_text(indexSTR):
    """
    Get text value for article `indexSTR`.
        `indexSTR`: str, article name
    """
    url = "%s/%s?pad=0" % (baseURL + "api/texts", urllib.parse.quote(indexSTR))
    req = urllib.request.Request(url, method="GET")
    try:
        response = urllib.request.urlopen(req)
        print(response.read().decode('utf-8'))
    except HTTPError as e:
        print('Error code: ', e.code)
        print(e.read().decode('utf-8'))


def post_text(indexSTR, textDICT):
    """
    Post text to article `indexSTR`.
        `indexSTR`: str, article name,
        `textDICT`: dict, text value
            textDICT = {
            "versionTitle": "Your version title",
            "versionSource": "Version source url",
            "language": "en/he",
            "text": [
                [
                    "Paragraph 1 row 1",
                    "Paragraph 1 row 2",
                    ...
                ],
                [
                    "Paragraph 2 row 1",
                    "Paragraph 2 row 2",
                    ...
                ],
                ...
            ]
        }
    """
    textJSON = json.dumps(textDICT)
    indexSTR = indexSTR.replace(" ", "_")
    url = baseURL + "api/texts/%s?count_after=1" % (urllib.parse.quote(indexSTR))
    values = {'json': textJSON, 'apikey': apikey}
    data = urllib.parse.urlencode(values)
    binary_data = data.encode('ascii')
    req = urllib.request.Request(url, binary_data)
    try:
        response = urllib.request.urlopen(req)
        res = response.read().decode('utf-8')
        print(res)
        if "error" not in res:
            return True
        return False
    except HTTPError as e:
        print('Error code: ', e.code)
        print(e.read().decode("utf-8"))
        return False


def get_link(linkSTR, with_text=1):
    """
    Get links for article/section/row `linkSTR`
        `linkSTR`: str, article/section/row name
            article  => linkSTR = "The way of the bodhisattvas"
            section  => linkSTR = "The way of the bodhisattvas.1"
            sections => linkSTR = "The way of the bodhisattvas.1-2"
            row      => linkSTR = "The way of the bodhisattvas.1:1"
            rows     => linkSTR = "The way of the bodhisattvas.1:1-3"
    """
    linkSTR = linkSTR.replace(" ", "_")
    linkURL = ""
    for c in linkSTR:
        if ord(c) > 128:
            linkURL += urllib.parse.quote(c)
        else:
            linkURL += c
    url = baseURL + "api/links/%s?with_text=%d" % (linkURL, with_text)
    req = urllib.request.Request(url, method="GET")
    try:
        response = urllib.request.urlopen(req)
        print(response.read().decode("utf-8"))
    except (HTTPError) as e:
        print('Error code: ', e.code)
        print(e.read())


def post_link(refLIST, typeSTR):
    """
    Post references for articles.
        `refLIST`: list of str, articles to reference
            refLIST = [
                "Article_1.1:2",    # First article/section/row
                "Article_2.1:2"     # Second
            ]
        `typeSTR`: str, reference type
            The Sefaria team have provided several types:
                - commentary
                - quotation
                - reference
                - summary
                - explication
                - related
    """
    url = baseURL + "api/links/"
    link = {
        "refs": refLIST,
        "type": typeSTR
    }
    textJSON = json.dumps(link)
    values = {'json': textJSON, 'apikey': apikey}
    data = urllib.parse.urlencode(values)
    binary_data = data.encode('ascii')
    req = urllib.request.Request(url, binary_data)
    try:
        response = urllib.request.urlopen(req)
        res = response.read().decode('utf-8')
        print(res)
        if "error" not in res:
            return True
        elif "Link already exists" in res["error"]:
            return True
        return False
    except (HTTPError) as e:
        print('Error code: ', e.code)
        print(e.read())
        return False

def post_sheet(titleSTR, sourceLIST):
    """
    Post reference sheet named `titleSTR` for custom messages.
        `titleSTR`: str, sheet name
        `sourceLIST`: list of dict, sheet references
            sourceLIST = [
                {
                    "ref": "Article1.1:1",
                    "heRef": "Article1_he.1:1",
                    "text": {
                        "en":"<p>Article1 reference</p>",
                        "he":"<p>Article1 reference in he</p>"
                    },
                },
                {
                    "ref": "Article2.2",
                    "heRef": "Article2_he.2",
                    "text": {
                        "en":"<p>Article2 reference</p>",
                        "he":"<p>Article2 reference in he</p>"
                    },
                },
                ...
            ]
    """
    url = baseURL + "api/sheets/"
    sheetJSON = {
        "status": "public",
        "title": titleSTR,
        "sources": sourceLIST,
        "summary": "",
        "options": {
            "numbered": 0,
            "boxed": 0,
            "bsd": 0,
            "language": "bilingual",    # display in both language
            "layout": "sideBySide",     # en/he layout setting
            "langLayout": "heRight",    # needed if layout = "sideBySide"
            "divineNames": "noSub",     # G-d？
            "collaboration": "none",
            "assignable": 0,
            "highlightMode": 0,
        }
    }
    sheetDumpJSON = json.dumps(sheetJSON)
    values = {'json': sheetDumpJSON, 'apikey': apikey}
    data = urllib.parse.urlencode(values)
    binary_data = data.encode('ascii')
    req = urllib.request.Request(url, binary_data)
    try:
        response = urllib.request.urlopen(req)
        print(response.read().decode('utf-8'))
    except HTTPError as e:
        print('Error code: ', e.code)
        print(e.read()) 


def post_webpage(webpage):
    """
    Post webpage reference.
        `webpage`: dict
            webpage = {
                "siteName": "reference site name",
                "url": "reference url",    # unique
                "title": "display title",
                "refs": [
                    "Article1.1:1",
                    "Article2.1:1"
                ],
                "expandedRefs": [
                    "Article1.1:1",
                    "Article2.1:1"
                ],
                "lastUpdated": datetime.now(),
                "description": "display description"
            }
    """
    url = baseURL + "api/linker-track"
    webpageJSON = json.dumps(webpage, default=json_util.default)
    values = {'json': webpageJSON, 'apikey': apikey}
    data = urllib.parse.urlencode(values)
    binary_data = data.encode('ascii')
    req = urllib.request.Request(url, binary_data, method="POST")
    try:
        response = urllib.request.urlopen(req)
        res = response.read().decode('utf-8')
        print(res)
        if "saved" in res:
            return True
        else:
            return False
    except HTTPError as e:
        print('Error code: ', e.code)
        print(e.read())
        return False

def get_related(titleSTR):
    """
    Get all reference value of article `titleSTR`.
        `titleSTR`: str, article name,
    """
    url = baseURL + "api/related/{}".format(urllib.parse.quote(titleSTR))
    values = {'private': True, 'apikey': apikey}
    data = urllib.parse.urlencode(values)
    binary_data = data.encode('ascii')
    req = urllib.request.Request(url, binary_data, method="GET")
    try:
        response = urllib.request.urlopen(req)
        print(response.read().decode('utf-8'))
    except HTTPError as e:
        print('Error code: ', e.code)
        print(e.read())


#endregion

#region test
"""
examples for APIs
"""
def test_category():
    post_term("Category_1", "Category_1_he")
    category = ['Library_1', 'Category_1']
    post_category(category)


def test_book():
    post_index("Article_1", ['Library_1', 'Category_1'], [ 
                {
                    "lang" : "en",
                    "text" : "Article_1",
                    "primary" : True
                }, 
                {
                    "lang" : "he",
                    "text" : "Article_1_he",
                    "primary" : True
                },
                {
                    "lang" : "he",
                    "text" : "Article_1_in_he"
                }
    ])


def test_text():
    text = {
        "versionTitle": "version1",
        "versionSource": "http://www.example.com/version1",
        "language": "en",
        "isBaseText": True,
        "text": [
            ["Chapter_1  row_1", "Chapter_1  row_2", "Chapter_1  row_3"],
            ["Chapter_2  row_1", "Chapter_2  row_2", "Chapter_2  row_3"],
        ]
    }
    
    # First parameter is name of article
    post_text("Article_1", text)






def test_link():
    link = [
        {
            "refs": [
                "Article_1.1:1",
                "Article_1.2:1"
            ],
            "type": "commentary",
        }
    ]
    
    post_link(link)

def test_sheet():
    sheet = {"title": "test sheet", "sources": [
        {
            "ref": "Article_1.1:1-3",
            "heRef": "Aritcle_1_he.1:1-3",
            "text": {
                "en":"<p>test sheet</p>",
                "he":"<p>test sheet in he</p>"
            },
        },
        {
            "ref": "Article_1.2:1",
            "heRef": "Article_1_he.2:1",
            "text": {
                "en":"<p>test sheet 2</p>",
                "he":"<p>test sheet 2 in he</p>"
                },
        }
    ]}
    post_sheet(sheet)



def test_webpage():
    webpage = {
        "siteName": "Google",
        "url": "https://www.google.com/search?q=hi",
        "title": "test Google",
        "refs": [
            "Article_1.1:1",
            "Article_1.2:1"
        ],
        "expandedRefs": [
            "Article_1.1:1",
            "Article_1.2:1"
        ],
        "lastUpdated": datetime.now(),
        "description": "test description"
    }
    post_webpage(webpage)


#endregion


#region Add file
"""
Data-adding directory default in `Pecha.org/tools/data`
"""
def add_by_file(fileSTR):
    """
    Read a text file and add.
    """
    success = True
    print("==========={}===========".format(fileSTR))
    try:
        with open("{}/data/texts/{}".format(BASEPATH, fileSTR), mode='r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print('[Error] opening file: ', e)
        return

    payload = {
        "bookKey": "",
        "categoryEn": [],
        "categoryHe": [],
        "textEn": [],
        "textHe": [],
    }
    for lang in data:
        if lang == "source":
            for lv1 in data[lang]:
                payload["categoryEn"].append([lv1])
                for lv2 in data[lang][lv1]:
                    payload["categoryEn"].append([lv1, lv2])
                    for lv3 in data[lang][lv1][lv2]:
                        payload["categoryEn"].append([lv1, lv2, lv3])
                        for book in data[lang][lv1][lv2][lv3]:
                            thisType = type(data[lang][lv1][lv2][lv3][book])
                            if thisType == dict:    # 要再往下追一層
                                payload["categoryEn"].append([lv1, lv2, lv3, book])
                                for version in data[lang][lv1][lv2][lv3][book]:
                                    if type(data[lang][lv1][lv2][lv3][book][version]) != list:
                                        print("[Error] version is not list")
                                        return
                                    else:
                                        payload["bookKey"] = book
                                        payload["textEn"].append(data[lang][lv1][lv2][lv3][book])
                            elif thisType == list:  # 已經是內文了
                                payload["bookKey"] = lv3
                                payload["textEn"].append(data[lang][lv1][lv2][lv3])
        elif lang == "target":  # 藏文
            for lv1 in data[lang]:
                payload["categoryHe"].append([lv1])
                for lv2 in data[lang][lv1]:
                    payload["categoryHe"].append([lv1, lv2])
                    for lv3 in data[lang][lv1][lv2]:
                        payload["categoryHe"].append([lv1, lv2, lv3])
                        for book in data[lang][lv1][lv2][lv3]:
                            thisType = type(data[lang][lv1][lv2][lv3][book])
                            if thisType == dict:    # 要再往下追一層
                                payload["categoryHe"].append([lv1, lv2, lv3, book])
                                for version in data[lang][lv1][lv2][lv3][book]:
                                    if type(data[lang][lv1][lv2][lv3][book][version]) != list:
                                        print("[Error] version is not list")
                                        return
                                    else:
                                        payload["textHe"].append(data[lang][lv1][lv2][lv3][book])
                            elif thisType == list:  # 已經是內文了
                                payload["textHe"].append(data[lang][lv1][lv2][lv3])
        else:
            print("[Error] Unknown language")
            return

    # 先新增每一個路徑
    print("==post_category==")
    for i in range(len(payload["categoryEn"])):
        response = post_term(payload["categoryEn"][i][-1], payload["categoryHe"][i][-1])
        if not response["status"]:
            if "term_conflict" in response:
                with open("{}/data/texts/conflict.txt".format(BASEPATH), mode='a', encoding='utf-8') as f:
                    f.write(fileSTR+": "+response["term_conflict"]+"\n")
            success = False
        if not post_category(payload["categoryEn"][i]):
            success = False

    # 新增書的資料
    print("==post_index==")
    titleLIST = []

    for i in range(len(payload["textEn"])):
        if i == 0:
            titleLIST.append({"lang": "en", "text": list(payload["textEn"][0].keys())[i], "primary": True, })
        else:   # 如果有不只一個版本
            titleLIST.append({"lang": "en", "text": list(payload["textEn"][0].keys())[i], })
    for i in range(len(payload["textHe"])):
        if i == 0:
            titleLIST.append({"lang": "he", "text": list(payload["textHe"][0].keys())[i], "primary": True,})
        else:   # 如果有不只一個版本
            titleLIST.append({"lang": "he", "text": list(payload["textHe"][0].keys())[i], })
    if not post_index(payload["bookKey"], payload["categoryEn"][-1], titleLIST):
        success = False

    # 新增內文
    print("==post_text==")
    for i in range(len(payload["textEn"])):
        enKey = list(payload["textEn"][0].keys())[i]
        enText = {
            "versionTitle": enKey,
            "versionSource": "http://www.example.com/{}".format(enKey.replace(" ", "_")),
            "language": "en",
            "text": payload["textEn"][0][enKey]
        }
        if i == 0:
            enText["isBaseText"] = True
        if not post_text(payload["bookKey"], enText):
            success = False
    for i in range(len(payload["textHe"])):
        heKey = list(payload["textHe"][0].keys())[i]
        heText = {
            "versionTitle": heKey,
            "versionSource": "http://www.example.com/{}".format(heKey.replace(" ", "_")),
            "language": "he",
            "text": payload["textHe"][0][heKey]
        }
        if i == 0:
            heText["isBaseText"] = True
        if not post_text(payload["bookKey"], heText):
            success = False

    if success:
        with open("{}/data/texts/success.txt".format(BASEPATH), mode='a', encoding='utf-8') as f:
            f.write(fileSTR+"\n")
        return True
    else:
        return False


def add_texts():
    """
    Add all text files in `/data/texts`.
    """
    dataLIST = os.listdir("{}/data/texts".format(BASEPATH))
    try:    # Added text save to `success.txt`
        with open("{}/data/texts/success.txt".format(BASEPATH), mode='r', encoding='utf-8') as f:
            successLIST = f.read().split("\n")
    except:
        successLIST = []
    
    count = 0
    for data in dataLIST:
        count += 1
        print("{}/{}".format(count, len(dataLIST)))
        if data in successLIST:
            continue
        elif data == "success.txt":
            continue
        successBOOL = add_by_file(data)
        # 有錯誤先終止
        if not successBOOL:
            print("=== [Failed] ===")
            return
        print("=== [Finished] {} ===".format(data))
        sleep(3)

def add_sheets():
    """
    Add all sheet files in `/data/sheets`.
    """
    print("============ add_sheets ============")
    fileLIST = os.listdir("{}/data/sheets".format(BASEPATH))
    try:    # Added sheets save to `success.txt`
        with open("{}/data/sheets/success.txt".format(BASEPATH), mode='r', encoding='utf-8') as f:
            successLIST = f.read().split("\n")
    except:
        successLIST = []
    print(successLIST)
    for file in fileLIST:
        if file in successLIST:
            continue
        elif file == "success.txt":
            continue
        
        with open("{}/data/sheets/{}".format(BASEPATH, file), "r", encoding="utf-8") as f:
            sheet= json.load(f)
        post_sheet(sheet["title"], sheet["sheet"])
        sleep(3)
    

def add_refs():
    """
    Add all ref files in `/data/refs`.
    """
    print("============ add_refs ============")
    fileLIST = os.listdir("{}/data/refs".format(BASEPATH))
    try:    # Added refs save to `success.txt`
        with open("{}/data/refs/success.txt".format(BASEPATH), mode='r', encoding='utf-8') as f:
            successLIST = f.read().split("\n")
    except:
        successLIST = []
    failedLIST = []
    print(successLIST)
    for file in fileLIST:
        if file in successLIST:
            continue
        elif file == "success.txt":
            continue
        elif file == "failed.txt":
            continue
        
        with open("{}/data/refs/{}".format(BASEPATH, file), "r", encoding="utf-8") as f:
            refLIST = json.load(f)
        for ref in refLIST:
            # Separate refs since the API only support adding 2 refs at the same time.
            for i in range(0, len(ref["refs"])-1):
                for j in range(i+1, len(ref["refs"])):
                    successBOOL = post_link([ref["refs"][i], ref["refs"][j]], ref["type"])
                    # Failed
                    if not successBOOL:
                        failedLIST.append({[ref["refs"][i], ref["refs"][j]], ref["type"]})
        with open("{}/data/refs/success.txt".format(BASEPATH), mode='a', encoding='utf-8') as f:
            f.write(file+"\n")
        print("=== [Finished] {} ===".format(file))
        sleep(3)
    with open("{}/data/refs/failed.txt".format(BASEPATH), mode='w+', encoding='utf-8') as f:
        json.dump(failedLIST, f, indent=4, ensure_ascii=False)
def add_webpages():
    """
    Add all webpage files in `/data/webpages`.
    """
    print("============ add_webpages ============")
    fileLIST = os.listdir("{}/data/webpages".format(BASEPATH))
    try:
        with open("{}/data/webpages/success.txt".format(BASEPATH), mode='r', encoding='utf-8') as f:
            successLIST = f.read().split("\n")
    except:
        successLIST = []
    failedLIST = []
    
    count = 0
    for file in fileLIST:
        count += 1
        print("{}/{}".format(count, len(fileLIST)))
        if file in successLIST:
            continue
        elif file == "success.txt":
            continue
        
        with open("{}/data/webpages/{}".format(BASEPATH, file), "r", encoding="utf-8") as f:
            webpageLIST = json.load(f)
        for webpage in webpageLIST:
            webpage["lastUpdated"] = datetime.now()
            successBOOL = post_webpage(webpage)
            # 失敗
            if not successBOOL:
                failedLIST.append(webpage)
        with open("{}/data/webpages/success.txt".format(BASEPATH), mode='a', encoding='utf-8') as f:
            f.write(file+"\n")
        print("=== [Finished] {} ===".format(file))
        sleep(5)
    with open("{}/data/webpages/failed.txt".format(BASEPATH), mode='w+', encoding='utf-8') as f:
        json.dump(failedLIST, f, indent=4, ensure_ascii=False)




#endregion


def categorizeData():
    """
    Separate files by file name.
    """
    if not os.path.exists("{}/data".format(BASEPATH)):
        print("'/data' not exist！")
        return
    
    if not os.path.exists("{}/data/toBeAdd".format(BASEPATH)):
        print("There's no data to be add！")
        return
    
    categoryLIST = os.listdir("{}/data/toBeAdd".format(BASEPATH))
    for category in categoryLIST:
        fileLIST = os.listdir("{}/data/toBeAdd/{}".format(BASEPATH, category))
        for file in fileLIST:
            # webpages
            if "_webpg.json" in file:
                os.replace("{}/data/toBeAdd/{}/{}".format(BASEPATH, category, file), "{}/data/webpages/{}".format(BASEPATH, file))
            # refs
                # not using yet
            # sheets 
                # not using yet
            # texts
            else:
                os.replace("{}/data/toBeAdd/{}/{}".format(BASEPATH, category, file), "{}/data/webpages/{}".format(BASEPATH, file))


def main():
    """
    Add all files in `/data`
    """
    print("========= texts =========")
    if not os.path.exists("{}/data/texts".format(BASEPATH)):
        os.mkdir("{}/data/texts".format(BASEPATH))
    add_texts()
    
    print("========= sheets =========")
    if not os.path.exists("{}/data/sheets".format(BASEPATH)):
        os.mkdir("{}/data/sheets".format(BASEPATH))
    add_sheets()
    
    print("========= refs =========")
    if not os.path.exists("{}/data/refs".format(BASEPATH)):
        os.mkdir("{}/data/refs".format(BASEPATH))
    add_refs()
    
    print("========= webpages =========")
    if not os.path.exists("{}/data/webpages".format(BASEPATH)):
        os.mkdir("{}/data/webpages".format(BASEPATH))
    add_webpages()


if __name__ == "__main__":
    #categorizeData()

    main()