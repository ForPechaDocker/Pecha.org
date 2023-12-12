
## Indajara API for Pecha.org 

Using indajaraAPI.py upload data to Pecha.org.

---------------------------
## To Do

Put data files with JSON format into `/data` and execute indajaraAPI.py

The API currently supports 4 types of files:
1. Texts/Article (Display on the main windows)
2. Translation (Display on the Resource List)
3. Web Link for Texts (Display on the Resource List)
4. Commentary, Reference, Summary (Display on the Resource List)
5. Sheets (Display on the Resource List)

#### 1) Texts/Article

Put your JSON files (file name is arbitrary) into `/data/texts` and execute indajaraAPI.py

The sample file description:

    {
        "中文": {
            "Category 1": {
                "Category 2": {
                    "Category 3": {
                        "The Title of Texts": {
                            "The Version Title of the Texts": [
                                [
                                    "section 1, sentence 1 (corresponds to the position in the "བོད་ཡིག" data)",
                                    "section 1, sentence 2",
                                    "section 1, sentence 3",
                                    "section 1, sentence 4",
                                    "section 1, sentence 5"
                                ],
                                [
                                    "section 2, sentence 1",
                                    "section 2, sentence 2",
                                    "section 2, sentence 3",
                                    "section 2, sentence 4",
                                    "section 2, sentence 5"
                                ]
                            ]
                        }
                    }
                }
            }
        },
        "བོད་ཡིག": {
            "Category 1'": {
                "Category 2'": {
                    "Category 3'": {
                        "The Title of Texts'": {
                            "The Version Title of the Texts'": [
                                [
                                    "section 1', sentence 1' (corresponds to the position in the "中文" data)",
                                    "section 1', sentence 2'",
                                    "section 1', sentence 3'",
                                    "section 1', sentence 4'",
                                    "section 1', sentence 5'"
                                ],
                                [
                                    "section 2', sentence 1'",
                                    "section 2', sentence 2'",
                                    "section 2', sentence 3'",
                                    "section 2', sentence 4'",
                                    "section 2', sentence 5'"
                                ]
                            ]
                        }
                    }
                }
            }
        }
    }

A sample file with parallel texts:

    {
        "中文": {
            "佛陀的話": {
                "經": {
                    "寶積部": {
                        "《大寶積經・43 普明菩薩會》[t310_43|toh87]": {
                            "《大寶積經・43 普明菩薩會》[t310_43|toh87]": [
                                [
                                    "大寶積經卷第一百一十二失譯附秦錄勘同編入普明菩薩會第四十三",
                                    "",
                                    "如是我聞：一時",
                                    "佛在王舍城耆闍崛山中，",
                                    "與大比丘眾八千人俱。 菩薩摩訶薩萬六千人，皆是阿惟越致，從諸佛土而來集會，悉皆一生當成無上正真大道。"
                                ],
                                [
                                    "",
                                    "答言：「自利不可得故。」",
                                    "答言：「所作不可得故。」",
                                    "又問：「汝等煩惱盡耶？」",
                                    "答言：「一切諸法畢竟無盡相故。」"
                                ]
                            ]
                        }
                    }
                }
            }
        },
        "བོད་ཡིག": {
            "སངས་རྒྱས་གསུམ": {
                "མདོ་སྡེ་": {
                    "རིན་བཀུཏ་མདོ་": {
                        "འཕགས་པ་འོད་སྲུང་གི་ལེའུ་ཞེས་བྱ་བ་ཐེག་པ་ཆེན་པོའི་མདོ [toh87|t310_43]": {
                            "འཕགས་པ་འོད་སྲུང་གི་ལེའུ་ཞེས་བྱ་བ་ཐེག་པ་ཆེན་པོའི་མདོ [toh87|t310_43]": [
                                [
                                    "འཕགས་པ་འོད་སྲུང་གི་ལེའུ་ཞེས་བྱ་བ་ཐེག་པ་ཆེན་པོའི་མདོ། །",
                                    "སངས་རྒྱས་དང་། བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །",
                                    "འདི་སྐད་བདག་གིས་ཐོས་པ་དུས་གཅིག་ན།",
                                    "བཅོམ་ལྡན་འདས་རྒྱལ་པོའི་ཁབ་ནི་བྱ་རྒོད་ཀྱི་ཕུང་པོའི་རི་ལ།",
                                    "དགེ་སློང་བརྒྱད་སྟོང་གི་དགེ་སློང་གི་དགེ་ འདུན་ཆེན་པོ་དང་། བྱང་ཆུབ་སེམས་དཔའ་སངས་རྒྱས་ཀྱི་ཞིང་སྣ་ཚོགས་ནས། འདུས་པ་ཁྲི་དྲུག་སྟོང་ཐམས་ཅད་ཀྱང་འདི་ལྟ་སྟེ། བླ་ན་མེད་པ་ཡང་དག་པར་རྫོགས་པའི་བྱང་ཆུབ་ཏུ་སྐྱེ་བ་གཅིག་གིས་ཐོགས་པ་ཤ་སྟག་དང་ཐབས་ཅིག་ཏུ་བཞུགས་ཏེ།"
                                ],
                                [
                                    "སྨྲས་པ། ངར་འཛིན་པ་དང་། ང་ཡིར་འཛིན་པ་ཡོངས་སུ་ཤེས་པས་སོ། །",
                                    "",
                                    "",
                                    "སྨྲས་པ། ཁྱེད་ཀྱི་ཉོན་མོངས་པ་ཟད་དམ།",
                                    "སྨྲས་པ། ཆོས་ཐམས་ཅད་གཏན་དུ་ ཟད་པའི་ཕྱིར་རོ། །"
                                ]
                            ]
                        }
                    }
                }
            }
        }
    }

#### Note:
1. Do not change the 2 keys "中文" and "བོད་ཡིག" in the first-level of dictionary/hash. Other content can be replaced in any language.

2. The level of category can be reduced or increased, but the upper(key="中文") and lower(key="བོད་ཡིག") levels must correspond, and cannot be a null value.

3. Category1 corresponding to Category1' will be regarded by the system as a unique key value and Category2 to Category2' and so on. If Category1 to Category X shows in a new file, this file can not be imported into the database.

4. "The Title of Texts" and "The Version Title of the Texts" follow the same unique key rule as Categories. And "Categories", "Titles", and "Version Titles" can not be empty.

5. The section and sentence can be empty like this:
    "The Version Title of the Texts'": []

6. Although the default setting divides "categories" and "texts" into two major classes, Chinese("中文") and Tibetan("བོད་ཡིག"), they can also be regarded as a main category and a parallel category, and texts in the same language or various languages ​​can be included as needed.

#### 2) Translation

Put your JSON files (file name is arbitrary) into `/data/texts` and execute indajaraAPI.py

The sample file description:

    {
        "中文": {
            "Category 1": {
                "Category 2": {
                    "Category 3": {
                        "The Title of Texts": {
                            "The Version Title of the Texts I": [
                                [
                                    "section 1, sentence 1",
                                    "section 1, sentence 2",
                                    "section 1, sentence 3",
                                    "section 1, sentence 4",
                                    "section 1, sentence 5"
                                ]
                            ],
                            "The Version Title of the Texts II": [
                                [
                                    "section 1, sentence 1",
                                    "section 1, sentence 2",
                                    "section 1, sentence 3",
                                    "section 1, sentence 4",
                                    "section 1, sentence 5"
                                ]
                            ]
                        }
                    }
                }
            }
        },
        "བོད་ཡིག": {
            "Category 1'": {
                "Category 2'": {
                    "Category 3'": {
                        "The Title of Texts'": {
                            "The Version Title of the Texts'": []
                        }
                    }
                }
            }
        }
    }

#### Note:
Sentences in diferent version will display on the Resource List erea.

#### 3) Web Link for Sentence

Put your JSON files (file name is arbitrary) into `/data/webpages` and execute indajaraAPI.py

A sample file:

    [
        {
            "siteName": "CBETA Online Reader",
            "url": "https://cbetaonline.dila.edu.tw/zh/T11n0310_p0623b05",
            "title": "CBETA: T0310",
            "refs": [
                "[The Title of Texts] [section_number]:[sentence_number]"
            ],
            "lastUpdated": "2023-11-11"
        },
        {
            "siteName": "CBETA Online Reader",
            "url": "https://cbetaonline.dila.edu.tw/zh/T11n0310_p0623b06",
            "title": "CBETA: T0310",
            "refs": [
                "《大寶積經・40 淨信童女會》[t310_40|toh84] 2:1"
            ],
            "lastUpdated": "2023-11-11"
        },
    ]

#### Note:
In "refs": [ "[The Title of Texts] [section_number]:[sentence_number]" ], the [section_number]:[sentence_number] refers to the content of "The Version Title of the Texts" under [The Title of Texts].

#### 4) Commentary, Reference, Summary

Put your JSON files (file name is arbitrary) into `/data/refs` and execute indajaraAPI.py

A sample file:

    [
        {
            "refs": [
                "[A The Title of Texts] [section_number]:[sentence_number]",
                "[A The Title of Texts] [section_number]:[sentence_number-sentence_number]"
            ],
            "type": "reference",
        },
        {
            "refs": [
                "文章名稱A 2:1-3", 
                "文章名稱Z 1:3"
            ],
            "type": "summary",
        }
    ]

#### Note:
1. In the case of "[The Title of Texts] 2:1-3", "2:1-3" stands for the first 3 sentences in the second section.

2. The reference links will display on the Resource List.

#### 5) Sheet for Additional Notes

Put your JSON files (file name is arbitrary) into `/data/sheets` and execute indajaraAPI.py

A sample file:

    {
    "title": "Sheet Title",
    "sheet": [
        {
            "ref": "[The Title of Texts] 2:1",
            "heRef": "[The Title of Texts] 2:1",
            "text": {
                "en": "<p>Notes we want to add for the ref above</p>",
                "he": "<p>Notes we want to add for the heRef above</p>"
            }
        },
        {
            "ref": "[The Title of Texts] 2:1",
            "heRef": "[The Title of Texts] 2:1",
            "text": {
                "en": "<p>Notes we want to add for the ref above</p>",
                "he": "<p>Notes we want to add for the heRef above</p>"
            }
        }
    ]
}
