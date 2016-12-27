import indicoio
import datetime
from slackStats import machine
from slackStats import topicsExtraction
from slackclient import SlackClient
import time
import re
BOT_NAME = 'pyslack'
indicoio.config.api_key = '5e333d60f62bd9e7d1a654e07f7c9772'
slack_client = SlackClient('xoxb-80204070758-VU08V6O4xDOL4eHtc1K8Fj6U')
BOT_ID='U2C6022NA'
AT_BOT = "<@" + BOT_ID + ">:"
EXAMPLE_COMMAND='senti'
stats={}
def Send_Stat(text, channel):
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=text, as_user=True)

def handle_messages(command,channel):
    if channel not in stats:
        stats[channel]={"count":0,'actionMessages':[],'allMessages':[],"links":[],"topics":[]}
    stats[channel]["count"]+=1
    stats[channel]["allMessages"].append(command)
    if "http://" in command or "https" in command:
        GRUBER_URLINTEXT_PAT = re.compile(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
        okay=re.findall(GRUBER_URLINTEXT_PAT,command)
        """url= re.findall(r'.*(http.*)>',command)[0]
        stats[channel]["links"].append(url)
        print(url)"""
        for links in okay:
            if "|" in links[0]:
                linkss=links[0][:links[0].index('|')]
                stats[channel]["links"].append(linkss)
            elif len(links)>1:
                stats[channel]["links"].append(links[0])
    if machine.main(command)==True:
        stats[channel]["actionMessages"].append(command)

    if command == "stats":
        generateReport()

def generateReport():
    for channels in stats:
        count=stats[channels]["count"]
        linkss=""
        actions=""
        if len(stats[channels])>0:
            for links in stats[channels]["links"]:
                linkss+=links+" ,"
            linkss = linkss[:len(linkss) - 1]
        else:
            linkss="No links"
        if len(stats[channels]["actionMessages"])>0:
            for messages in stats[channels]["actionMessages"]:
                actions+=messages+"\n"
        else:
            action="No Action Messages"
        hashtags=""
        if len(stats[channels]["allMessages"]) > 0:
            for text in stats[channels]["allMessages"]:
                hashtags+=text+"\n"
            hashtags=topicsExtraction.suggest(hashtags)
        else:
            hashtags="No topics to display"
        finalText="Count of messages today:"+str(count)+"\nActions:"+actions+"\nLinks:"+linkss+"\nTopics:"+hashtags
        Send_Stat(finalText,channels)


def parse_slack_output(slack_rtm_output):

    output_list = slack_rtm_output
    #print(str(output_list))
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and output['user']!='U2C6022NA':
                if  AT_BOT in output['text']:
                    return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']

                else:
                    return output['text'].strip().lower(), \
                           output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1   # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_messages(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
            if datetime.datetime.now().hour==10 and datetime.datetime.now().minute==20 and datetime.datetime.now().second==0:
                generateReport()
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
