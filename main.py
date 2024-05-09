import requests

# https://wiki.openstreetmap.org/wiki/API_v0.6#GPS_traces


offset = 0.01

# balade avec les filles et Mariel 
longitude = 17.11304
latitude = -24.99131

# longue balade avec Noemie geo:17.187975,-25.104049;crs=wgs84;u=0
longitude = 17.187975
latitude = -25.104049

print(
    f"https://www.openstreetmap.org/?mlat={longitude}&mlon={latitude}#map=19/{longitude}/{latitude}"
)


def loadGPX(gpxfile, page=0):
    bbox = ",".join(
        [
            str(latitude - offset),
            str(longitude - offset),
            str(latitude + offset),
            str(longitude + offset),
        ]
    )
    url = f"https://api.openstreetmap.org/api/0.6/trackpoints?page={page}&bbox={bbox}"
    resp = requests.get(url)
    with open(f"{page}-{gpxfile}", "wb") as f:
        f.write(resp.content)


def parseGPX(gpxfile, page=0):
    f = open(f"{page}-{gpxfile}", "r")
    trkpt_count = 0
    for x in f:
        if "<trkpt" in x:
            trkpt_count += 1
        if "<name>" in x:
            print()
            x = x.replace("<name>", "").replace("</name>", "").strip()
            print("Name: ", x)
        if "<desc>" in x:
            x = x.replace("<desc>", "").replace("</desc>", "").strip()
            print("Description: ", x)
        if "<url>" in x:
            x = x.replace("<url>", "").replace("</url>", "").strip()
            uniq_id = x.split("/")[-1]
            print("https://www.openstreetmap.org" + x)
            resp = requests.get(f"https://www.openstreetmap.org/trace/{uniq_id}/data")
            with open(f"{uniq_id}.gpx", "wb") as f:
                f.write(resp.content)

    print("Number of trackpoints: ", trkpt_count)
    return trkpt_count


def main():
    gpx = "example.gpx"
    page = 0
    loadGPX(gpx, page)
    while parseGPX(gpx, page) == 5000:
        page += 1
        loadGPX(gpx, page)


if __name__ == "__main__":
    main()