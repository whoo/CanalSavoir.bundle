TITLE="Canal Savoir"
ICON = "icon-default.png"
ART = 'bg-default.jpg'

URL ="http://www.canalsavoir.tv/videosurdemande"
BASE = "http://www.canalsavoir.tv"

Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

ObjectContainer.title1 = TITLE
ObjectContainer.view_group = 'List'
ObjectContainer.art = R(ART)

DirectoryObject.thumb = R(ICON)
DirectoryObject.art = R(ART)
VideoClipObject.thumb = R(ICON)
VideoClipObject.art = R(ART)

videos=[]

def Start():
    Log.Debug("DD: CanalSavoir")
    HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'
    
    page=    HTML.ElementFromURL(URL,errors='ignore')

    for a in page.xpath('//h2[@class="thematique"]'):
#        Log.Debug(a[0].tail)
        title=a[0].tail.strip()
        cat={}
        items=[]
        if (title!=""):
            url=a.getparent().getnext().xpath(".//div[@class='grille__item']/a")
            cat['Categorie']=title
            cat["items"]=items
            for u in url:
                vids={}
                link=BASE+u.get('href')
                img=BASE+u.xpath("./div/img")[0].get('src')
                stitle=u.xpath("./div[@class='caption']/h4")[0].text
                vids['link']=link
                vids['img']=img
                vids['title']=stitle
                items.append(vids)
#                Log.Debug(stitle)
        Log.Debug(title+" %d"%len(items))
#g(stitle.text)

        videos.append(cat) 
#    Log.Debug(videos)

        



@handler('/video/canalsavoir',TITLE)
def MainMenu():
    oc = ObjectContainer()

    for k,categorie in enumerate(videos):
        title = categorie['Categorie']
        oc.add( DirectoryObject(key = Callback(Categorie,categorie=k), title=title, thumb=R(ICON)))


    return oc 


def Categorie(categorie):
    oc =ObjectContainer(title2=videos[categorie]['Categorie'])
    Log.Debug(len(videos[categorie]['items']))

    for c in videos[categorie]['items']:
        # Log.Debug(k)
        oc.add(VideoClipObject(url=c['link'],title=c['title'],thumb=c['img'],art=R(ICON)))
        
    
    return oc
