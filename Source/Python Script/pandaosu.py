#!/usr/bin/python
from colorama import Fore, Back, Style
from datetime import datetime
import sys
import os
import schedule
import MySQLdb
import requests
import json
import re

def StrSplit(text, str):
    try:
        return text.split(str[0])[1].split(str[1])[0]
    except Exception as e:
        print ("Split Failed\n[0] " + str[0] + "[1] " + str[1])
        exit()

class Osu_BeatmapDown:
    def __init__(self):
        # Database Connect
        # input id, pass, database
        self.db = MySQLdb.connect("localhost","id","password","database")
        self.cursor = self.db.cursor()

    def DB_Add(self, id, artist, creatorId, creator, title, category):
        try:
            # check artist
            self.cursor.execute("SELECT name FROM osu_artists WHERE LCASE(name) = '%s'" % artist.lower())
            Cnt_Artist = self.cursor.fetchall()
            # check creatorId
            self.cursor.execute("SELECT id FROM osu_creators WHERE id = '%s'" % creatorId)
            Cnt_Creator = self.cursor.fetchall()
            # check beatmapid
            self.cursor.execute("SELECT id FROM osu_beatmaps WHERE id = '%s'" % id)
            beatmapId = self.cursor.fetchall()

            #TODO 다운받고 쿼리 추가 // osu_beatmaps 테이블에 추가해야함.
            if len(Cnt_Artist) == 0:
                self.cursor.execute("INSERT INTO osu_artists (name) VALUES ('%s')" % artist)
            if len(Cnt_Creator) == 0:
                self.cursor.execute("INSERT INTO osu_creators (id, name) VALUES ('%s', '%s')" % (creatorId, creator))
            if len(beatmapId) == 0:
                self.cursor.execute("SELECT idx FROM osu_artists WHERE LCASE(name) = '%s'" % artist.lower())
                artist_idx = self.cursor.fetchall()
                self.cursor.execute("INSERT INTO osu_beatmaps (id, artist, creator, title, category) VALUES"
                    "('%s', '%s', '%s', '%s', '%s')" % (id, artist_idx[0][0], creatorId, title, category))
        finally:
            self.db.commit()

    def Beatmap_Download(self, url):
        try:
            if url == None:
                print ("URL Error")
                exit()

            # FileName : '[id].osz'
            FileName = url.split('/')[-1]  + '.osz'
            FilePath = 'HDD/OSU/beatmaps/'+ FileName

            # 파일 존재유무 체크
            if os.path.exists(FilePath):
                print (Back.RED + Fore.WHITE + "%s Exist" % FileName + Style.RESET_ALL)
                return None

            rq = requests.get(url, stream=True, cookies=self.cookie)

            # 파일크기 가져온후 None값일시 존재하지 않는 파일
            filesize = rq.headers.get('content-length')
            if filesize == None:
                print ('%s Download Failed'% FileName)
                return None
            else:
                filesize = int(filesize)

            # File Download Progressbar
            with open(FilePath, 'wb') as f:
                dl = 0
                for chunk in rq.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

                        dl += len(chunk)
                        done = int(50 * dl / filesize)
                        sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
                        sys.stdout.flush()
            sys.stdout.write(" Download Success\n")
            return True
        except Exception as e:
            raise

    def OSU_GETBeatmaps(self, Rank):
        rq = requests.get("https://osu.ppy.sh/p/beatmaplist?m=-1&r=%s" % Rank + "&g=0&la=0")
        BeatmapCreator = re.finditer(
            r"beatmap' id='(?P<id>[^']*)'((?!artist)[\s\S])*"
            "class='artist'>(?P<artist>[^<]*)[^.]*"
            "class='title'>(?P<title>[^<]*)[^.]*"
            "mapped by<\/span> <a href='\/u\/(?P<creatorId>[^']*)[^>]*>(?P<creator>[^<]*)",
            rq.content.decode(),
            flags=re.I)

        # DB Connect
        Osu_BeatmapDown()

        beatmaps_list = []
        for item in BeatmapCreator:
            beatmaps_list.append(item.groupdict())
        for i, item in enumerate(beatmaps_list):
            print ("ID %s\nArtist %s\nTitle %s\nCreator %s[%s]" % (item['id'], item['artist'], item['title'], item['creator'], item['creatorId']))
            if (self.Beatmap_Download("https://osu.ppy.sh/d/%s" % item['id']) == True):
                self.DB_Add(item['id'], item['artist'], item['creatorId'], item['creator'], item['title'], Rank)

        self.cursor.close()
        self.db.close()
        return print ("Download Complete!")

    def OSU_Cookie(self, rq):
        sid = StrSplit(rq.text, ["&sid=","\""] )
        uid = StrSplit(rq.text, ["u/","\""] )

        self.cookie = {
            'phpbb3_2cjk5_sid': sid,
            'phpbb3_2cjk5_u': uid
        }

    def OSU_Login(self):
        OSU_URL = 'https://osu.ppy.sh/forum/ucp.php?mode=login'
        headers = {
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
           'Referer': 'https://osu.ppy.sh/forum/ucp.php?mode=login',
           'Content-Type': 'application/x-www-form-urlencoded'
        }

        payload = {
            'username': 'ID',
            'password': 'PW',
            'redirect': 'index.php',
            'login': 'Login'
        }
        # URL : https://osu.ppy.sh (Login)
        rq = requests.post(OSU_URL, data=payload, headers=headers)
        # GET Cookie
        self.OSU_Cookie(rq)

        if rq.text.find("You have specified an incorrect") != -1:
            print ("Failed")
            return False

        print("Success Login")
        return True

    def func_Download(self):
        # Login
        if self.OSU_Login() == True:
            print (Back.RED + Fore.WHITE + "Choose Rank \nDefault : None\tRanked & Approved : 0\tApproved : 6\tQualified : 11" + Style.RESET_ALL)

            # Rank값이 비어있으면 '6(Approved)' // Download
            while True:
                Rank = input()
                if ((Rank == '') | (Rank == '0') | (Rank == '6') | (Rank == '11')): break
                else: print (Back.RED + Fore.WHITE + "Choose Rank \nDefault : None\tRanked & Approved : 0\tApproved : 6\tQualified : 11" + Style.RESET_ALL)

            self.OSU_GETBeatmaps(6 if Rank == '' else Rank)
        else:
            exit()

        # Download every 3 hours
        schedule.every(3).hours.do(self.OSU_GETBeatmaps, (6 if Rank == '' else Rank))
        while True:
            schedule.run_pending()

    def func_Remove(self):
        Msg = "input the id value you want to delete"
        print (Msg)

        beatmapId = input()
        while True:
            if (beatmapId == '') | (beatmapId.isdigit() == False):
                print (Msg)
            else:
                self.cursor.execute("SELECT * FROM osu_beatmaps WHERE id = '{0}'".format(beatmapId))
                Cnt_beatmap = self.cursor.fetchall()

                if len(Cnt_beatmap) == 0:
                    print ("Dose not Exist id value")
                    exit()
                else:
                    self.cursor.execute("DELETE FROM osu_beatmaps WHERE id = '{0}'".format(beatmapId))
                    self.db.commit()
                    print ("Success")
                    exit()

# Entry
def Init():
    if len(sys.argv) == 1:
        print ("Option Error")
        exit()
    if sys.argv[1] not in resultMap:
        print("'{0}' does not exist\n-------------\nKey List\n-------------\ni (Install)\n-------------".format(sys.argv[1]))
        exit()

resultMap = {
  # i : OSU Beatmap Download
  "i":Osu_BeatmapDown().func_Download,
  "r":Osu_BeatmapDown().func_Remove
}

Init()
result = resultMap.get(sys.argv[1])()
