import requests
import asyncio
import aiohttp

#Flickr ID
#Use https://www.webfx.com/tools/idgettr/ if their flickr page has their name in the link instead of the id.
user_id = ""

url = f"https://www.flickr.com/photos/{user_id}/"
response = requests.get(url).text
f = response.find('followerCount')
followers = ""
for i in response[f + 15:f + 20]:
  if i.isdigit():
    followers += i
print(f"Followers: {int(followers)}")

async def fetch_photos(user_id, current_page):
    url = "https://api.flickr.com/services/rest"
    querystring = {
        "per_page": "500",
        "page": f"{current_page}",
        "extras": "can_addmeta,can_comment,can_download,can_print,can_share,contact,content_type,count_comments,count_faves,count_views,date_taken,date_upload,description,icon_urls_deep,isfavorite,ispro,license,media,needs_interstitial,owner_name,owner_datecreate,path_alias,perm_print,realname,rotation,safety_level,secret_k,secret_h,url_sq,url_q,url_t,url_s,url_n,url_w,url_m,url_z,url_c,url_l,url_h,url_k,url_3k,url_4k,url_f,url_5k,url_6k,url_o,visibility,visibility_source,o_dims,publiceditability,system_moderation",
        "get_user_info": "1",
        "jump_to": "",
        "user_id": user_id,
        "view_as": "use_pref",
        "sort": "use_pref",
        "viewerNSID": "",
        "method": "flickr.people.getPhotos",
        "csrf": "",
        "api_key": "9346028454335bdbc829f3b9a2b6f639",
        "format": "json",
        "hermes": "1",
        "hermesClient": "1",
        "reqId": "1abcaf31-8850-4f97-88f3-ae0e819ad925",
        "nojsoncallback": "1"
    }
    headers = {
        "authority": "api.flickr.com",
        "accept": "*/*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "cookie": "xb=070076; localization=en-us%3Bin%3Bin; sp=9978a3f5-11a6-4add-b198-912418c0cd5b; ccc=%7B%22needsConsent%22%3Afalse%2C%22managed%22%3A0%2C%22changed%22%3A0%2C%22info%22%3A%7B%22cookieBlock%22%3A%7B%22level%22%3A0%2C%22blockRan%22%3A0%7D%7D%2C%22freshServerContext%22%3Atrue%7D; __ssid=ca2ace3173f76a6250ad959ec1e2b78; liqpw=1440; session_id=ffca8baf-b286-4f1e-bc0d-d16cce98ee3a; liqph=620; _sp_ses.df80=*; __gads=ID=d54de52ed0833f5e:T=1700377348:RT=1710686506:S=ALNI_MaZwYJuW-2pNQEELGSuJKi6ttXPZA; __gpi=UID=00000c8d962547e0:T=1700377348:RT=1710686506:S=ALNI_MaUFfQAHIrOtB6kDtCLlFdyTCA3Lw; __eoi=ID=7505f301707d1ddd:T=1705715231:RT=1710686506:S=AA-AfjZpPGRrvDLirYomz8sAh7c8; adCounter=5; AMCVS_48E815355BFE96970A495CD0%40AdobeOrg=1; AMCV_48E815355BFE96970A495CD0%40AdobeOrg=281789898%7CMCMID%7C44256541386120365893831038181914422322%7CMCAAMLH-1711292012%7C12%7CMCAAMB-1711292012%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1710694412s%7CNONE%7CvVersion%7C4.1.0; vp=828%2C654%2C1%2C15%2Cphotolist-container%3A828%2Cgroup-pool-preview-view%3A1124%2Cgallery-page-view%3A1152%2Cshowcase-container%3A912%2Cprofile-container%3A1140%2Calbums-list-page-view%3A828%2Calbum-page-view%3A1081%2Csearch-photos-everyone-view%3A800%2Csearch-photos-yours-view%3A1425%2Csearch-photos-contacts-view%3A1425%2Cfavorites-page-view%3A1140%2Cexplore-page-view%3A1140; _sp_id.df80=56b47e62-8984-422a-b93a-ff7e3f3f48e0.1700377318.171.1710687227.1710681954.5cfc5dca-3167-4a80-94d1-a4a2ff50cf57.568290d0-c9dc-4171-a2ba-d840bc75e8f6.ed57a2dc-b71e-4aae-8629-82f694095c7b.1710686504673.40",
        "origin": "https://www.flickr.com",
        "pragma": "no-cache",
        "referer": "https://www.flickr.com/",
        "sec-ch-ua": 'Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    async with aiohttp.ClientSession() as session:
      async with session.get(url, headers=headers, params=querystring) as response:
          return await response.json()

async def main(user_id):
    current_page = 1
    faves = 0
    views = 0
    comments = 0
    while True:
        response = await fetch_photos(user_id, current_page)
        for photo in response['photos']['photo']:
            faves += int(photo["count_faves"])
            views += int(photo["count_views"])
            comments += int(photo["count_comments"])
        if response['photos']['pages'] == current_page:
            break
        current_page += 1
    print(f"Total Faves: {faves}")
    print(f"Total Views: {views}")
    print(f"Total Comments: {comments}")
      
asyncio.run(main(user_id))
