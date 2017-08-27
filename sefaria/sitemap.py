"""
sitemap.py - generate sitemaps of all available texts for search engines.

Outputs sitemaps and sitemapindex to the first entry of STATICFILES_DIRS.
"""
import os
from datetime import datetime

from sefaria.model import *
from sefaria.system.database import db
from sefaria.summaries import flatten_toc
from settings import STATICFILES_DIRS


def chunks(l, n):
    """
    Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


class SefariaSiteMapGenerator(object):

    hostnames = {
        'en': 'https://www.sefaria.org',
        'he': 'https://www.sefaria.org.il'
    }

    static_urls = [
        "",
        "/explore",
        "/translation-requests",
        "/contribute",
        "/texts",
        "/activity",
        "/educators",
        "/sheets",
        "/sheets/public",
        "/sheets/tags",
        "/developers",
        "/login",
        "/register",
        "/related-projects",
        "/copyright-policy",
        "/terms",
        "/privacy-policy",
        "/updates",
        "/people",
        "/people/Talmud"
    ]


    def __init__(self, interfaceLang='en'):
        self._interfaceLang = interfaceLang
        self._hostname = self.get_hostname_by_lang(self._interfaceLang)

    def get_hostname_by_lang(self, interfaceLang):
        return self.hostnames[interfaceLang]

    def generate_texts_sitemaps(self):
        """
        Create sitemap for each text section for which content is available.
        Returns the number of files written (each sitemap can have only 50k URLs)
        """
        refs = library.ref_list()
        urls = [self._hostname + "/" + oref.url() for oref in refs]

        maps = list(chunks(urls, 40000))

        for n in range(len(maps)):
            self.write_urls(maps[n], "texts-sitemap%d.txt" % n)

        return len(maps)

    def generate_texts_toc_sitemap(self):
        """
        Creates a sitemap for each text table of contents page.
        """
        titles = flatten_toc(library.get_toc())
        urls = [self._hostname + "/" + Ref(title).url() for title in titles]
        self.write_urls(urls, "text-toc-sitemap.txt")

    def generate_categories_sitemap(self):
        """
        Creates sitemap for each category page.
        """
        toc = library.get_toc()
        def cat_paths(toc):
            paths = []
            for t in toc:
                cat = t.get("category", None)
                if cat:
                    cat = cat.replace(" ", "%20")
                    paths.append(cat)
                    subpaths = cat_paths(t["contents"])
                    paths = paths + [cat + "/" + sp for sp in subpaths]
            return paths
        paths = cat_paths(toc)
        urls = [self._hostname + "/texts/" + p for p in paths]
        self.write_urls(urls, "categories-sitemap.txt")

    def generate_sheets_sitemap(self):
        """
        Creates a sitemap for each public source sheet.
        """
        query = {"status": "public"}
        public = db.sheets.find(query).distinct("id")
        urls = [self._hostname + "/sheets/" + str(id) for id in public]

        self.write_urls(urls, "sheets-sitemap.txt")

    def generate_people_sitemap(self):
        urls = [self._hostname + "/person/{}".format(p.key.replace(" ", "%20")) for p in PersonSet()]
        self.write_urls(urls, "person-sitemap.txt")

    def generate_static_sitemap(self):
        """
        Creates a sitemap of static content listed above.
        """
        self.write_urls([self._hostname + "/" + url for url in self.static_urls], "static-sitemap.txt")


    def write_urls(self, urls, filename):
        """
        Writes the list URLS, one per line, to filename.
        """
        out = STATICFILES_DIRS[0] + "sitemaps/" + self._interfaceLang + "/" + filename
        f = open(out, 'w')
        for url in urls:
            f.write(url.encode('utf-8') + "\n")
        f.close()


    def generate_sitemap_index(self, sitemaps):
        now = datetime.now().strftime("%Y-%m-%d")
        xml = ""
        for m in sitemaps:
            xml += """
               <sitemap>
                  <loc>%s/static/sitemaps/%s</loc>
                  <lastmod>%s</lastmod>
               </sitemap>
               """ % (self._hostname, m, now)

        sitemapindex = """<?xml version="1.0" encoding="UTF-8"?>
            <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            %s
            </sitemapindex>
            """ % xml

        out = STATICFILES_DIRS[0] +  "sitemaps/" + self._interfaceLang + "/sitemapindex.xml"
        f = open(out, 'w')
        f.write(sitemapindex)
        f.close()


    def generate_sitemaps(self):
        """
        Creates all sitemap files then creates and index file for all.
        """
        self.generate_static_sitemap()
        self.generate_sheets_sitemap()
        self.generate_texts_toc_sitemap()
        self.generate_categories_sitemap()
        self.generate_people_sitemap()
        n = self.generate_texts_sitemaps()

        maps = ["static-sitemap.txt", "categories-sitemap.txt", "text-toc-sitemap.txt", "person-sitemap.txt", "sheets-sitemap.txt"]
        maps += ["texts-sitemap%d.txt" % i for i in range(n)]

        self.generate_sitemap_index(maps)