# -*- coding: utf-8 -*-
BASE_URL     = 'http://www.tvcatchup.com'
CHANNELS_URL = '%s/channels.html' % (BASE_URL)
ICON_URL     = 'http://images-cache.tvcatchup.com/NEW/images/channels/hover/channel_%s.png'

####################################################################################################

def Start():
  Plugin.AddPrefixHandler('/video/tvcatchup', MainMenu, 'TVCatchup', 'icon-default.png', 'art-default.jpg')
  Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')
  MediaContainer.art = R('art-default.jpg')
  HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12'

####################################################################################################

def MainMenu():
  dir = MediaContainer(viewGroup='InfoList', title1='TVCatchup Channel List')

  channels = HTML.ElementFromURL(CHANNELS_URL, errors='ignore').xpath('//ul[@id="logos"]/li/a')
  for channel in channels:
    title = channel.get('title').strip()
    url = BASE_URL + channel.get('href')
    id = channel.xpath('./parent::li')[0].get('id').rsplit('_', 1)[1]
    dir.Append(WebVideoItem(url, title=title, thumb=Function(GetThumb, channel_id=id)))

  dir.Append(PrefsItem('Settings', thumb=R('icon-prefs.png')))
  return dir

####################################################################################################

def GetThumb(channel_id):
  try:
    data = HTTP.Request(ICON_URL % (channel_id), cacheTime=CACHE_1MONTH).content
    return DataObject(data, 'image/png')
  except:
    return Redirect(R('icon-default.png'))
