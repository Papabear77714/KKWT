import os
# Use the package we installed
import logging
import random

from slack_bolt import App, Say, BoltContext
from slack_sdk import WebClient

logging.basicConfig(level=logging.DEBUG)

tips = [
    "Always make sure that you update the Request URL when restarting ngrok",
    "Make sure you check your scopes when an API method does not work",
    "Every API call has a scope check that you use the correct ones and when calling something new add that scope on Slack",
    "After changing the scope you need to install your App again",
    "Every Event you want to use, you need to subscribe to on Slack",
    "Every Slack command needs the Request URL",
    "The Bot token is on the Basics Page",
    "The Slack Signing Secret is on the OAuth & Permission page",
    "Limit the scopes to what you really need",
    "You can add collaborators to your Slack App under Collaborators, they need to be in the workspace",
    "To use buttons you need to enable Interactive Components",
    "Always go in tiny steps, use the logger or print statements to see where you are and if events reach your app",
    "If the user does something on Slack always send a response, even if it is just an emoji",
    "Your App can use on the users behalf, you need to get User Scopes in that case. Later this would lead to having to save user tokes",
    "Do not plan to much, do simple things first, when you get these done then start to dream big",
    "Storing persistent data in a DB makes sense, when you are not familiar with it maybe a dict in a file might be enough for now",
    "Oauth -- so authenticating the app and user is important when distributing your app, while locally developing it is not that important yet, get some functionality going first",
    "Have the Slack API, Slack Events and your Slack Build App page open in your browser to have fast access",
    "Slash commands need to be unique in a workspace, so do append your bots name to them"
]

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

@app.event("app_mention")
def event_test(body, say, logger, client):
    logger.info(body)
    # say(f"Hello there you <@{body['event']['user']}> :smile:!")

    client.chat_postEphemeral(channel=body['event']['channel'], user=body['event']['user'], text=f"Hello there you <@{body['event']['user']}> :smile:!")

@app.event("member_joined_channel")
def member_joined_channel(event, client, logger):
    logger.info(event)
    channelInfo = client.conversations_info(channel=event['channel'])
    
    if (channelInfo['channel']['name'] == 'intro'):
        block = [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"Hello there <@{event['user']}> would you like to introduce yourself?"
                        }
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Yes",
                                    "emoji": True
                                },
                                "value": "click_me_123",
                                "action_id": "yes_button" ## NOT implemented yet
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Nope",
                                    "emoji": True
                                },
                                "value": "click_me_123",
                                "action_id": "nope_button"
                            }
                        ]
                    }
                ]
        client.chat_postMessage(channel=event['channel'], blocks = block)

@app.action("nope_button")
def nope_button_clicked(ack, body, action, logger, client, say):
    logger.info(body)
    ack()
    newBlock = [body['message']['blocks'][0]]
    newBlock.append({
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": ":cry: shame on you for not introducing yourself"
                        }
                    })
    client.chat_update(channel=body['channel']['id'], ts=body['message']['ts'], blocks = newBlock)

@app.command("/py_tips")
def command_tip(ack, body, command, logger, client):
    ack()
    logger.info(command)
    block = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":smile: You asked for a tip, here you go"
                    }
                }
            ]
    attach = [
                {
                    "color": "#f2c744",
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"{random.choice(tips)}"
                            }
                        }
                    ]
                }
            ]
    client.chat_postMessage(channel=command['channel_id'], blocks = block, attachments=attach)

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
