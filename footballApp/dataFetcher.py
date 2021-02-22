import os, requests
from dateutil.parser import parse as dateparser
import subprocess # just to call an arbitrary command e.g. 'ls'

host = "http://127.0.0.1:8000/"

def updateFiles(dir_name, end_new, end_old, player_id):

    name_of_new = end_new
    name_of_old = end_old

    # create file
    if not any(fname.endswith(end_new) for fname in os.listdir(dir_name)):
        f = open(dir_name + end_new, 'w')
        f.close()

    for fname in os.listdir(dir_name):
        if fname.endswith(end_new):
            name_of_new = dir_name + fname
        elif fname.endswith(end_old):
            name_of_old = dir_name + fname

    last_date = name_of_new[len(dir_name):-len(end_new)]
    header_req = requests.head(host + "players/" + player_id, headers={"If-Modified-Since": last_date.strip()})

    if header_req.status_code == 304:
        print("No changes")
    elif header_req.status_code == 302:
        # new -> old
        get_req = requests.get(host + "players/" + player_id)
        with open(name_of_old, 'w') as file:
            file.write(get_req.text)
            file.flush()

        os.rename(name_of_new, name_of_new.replace("new", "old"))
        os.rename(name_of_old, dir_name + header_req.headers['Last-Modified'] + " " + end_new)
    elif header_req.status_code == 404:
        os.remove(name_of_new)
    else:
        print("Error" + header_req.status_code.__str__())

    print("done")


def getDetail(player_id):

    dir_name = "fetchedData/detail/"
    end_new = name_of_new = "players" + player_id + "_new.json"
    end_old = name_of_old = "players" + player_id + "_old.json"

    # change current dir
    os.chdir(os.path.dirname(dir_name))

    # create files
    if not any(fname.endswith(end_new) for fname in os.listdir(".")):
        f = open(end_new, 'x')
        f.close()
    if not any(fname.endswith(end_old) for fname in os.listdir(".")):
        f = open(end_old, 'x')
        f.close()

    for fname in os.listdir("."):
        if fname.endswith(end_new):
            name_of_new = fname
        elif fname.endswith(end_old):
            name_of_old = fname

    last_date = name_of_new[:-16]
    header_req = requests.get(host + "players/"+player_id, headers={"If-Modified-Since": last_date.strip()})

    if header_req.status_code == 304:
        print("No changes")
    elif header_req.status_code == 302:
        # new -> old
        # os.rename('old_name.txt','new_name.txt')
        get_req = requests.get(host + "players/"+player_id)
        with open(name_of_old, 'w') as file:
            file.write(get_req.text)
        os.rename(name_of_new, name_of_new.replace("new", "old"))
        os.rename(name_of_old, header_req.headers['Last-Modified'] + " " + end_new)
    else:
        print("Error")

def main():
    # get whole list
    dir_name = "fetchedData/list/"
    old_name = "players_old.json"
    new_name = "players_new.json"
    updateFiles(dir_name, new_name, old_name, "")

    # get one player
    while (1):
        player_id = input()

        dir_name = "fetchedData/detail/"
        old_name = "player" + player_id + "_old.json"
        new_name = "player" + player_id + "_new.json"
        updateFiles(dir_name, new_name, old_name, player_id + "/")


if __name__ == '__main__':
    main()
