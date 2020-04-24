from mitmproxy import ctx
import json

TRUMPET_IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/6/6d/Posaune.jpg"

class SlackInterceptor:
    def __init__(self):
        self.ids_to_ban = set()

    def bwaaah(self, text):
        return 'bwah bwah'

    @property
    def banned_users(self):
        return set(ctx.options.bannedusers.strip().split(","))
    
    def load(self, loader):
        loader.add_option(
            name = "bannedusers",
            typespec = str, # see https://github.com/mitmproxy/mitmproxy/issues/3015
            default = '',
            help = "Ignore these slack user ids (comma sep list)",
        )

    def handle_message(self, msg):
        msg['text'] = self.bwaaah(msg['text'])
        msg['blocks'] = []
        msg['attachments'] = []
        msg['elements'] = []
        if 'files' in msg:
            for f in msg['files']:
                self.ids_to_ban.add(f['id'])
                f['title'] = self.bwaaah(f['title'])
                f['name'] = self.bwaaah(f['name'])
                f['mimetype'] = 'image/jpeg'
                f['filetype'] = 'jpeg'
                f['pretty_type'] = 'JPEG'
                f['url_private'] = TRUMPET_IMAGE_URL
                f['url_private_download'] = TRUMPET_IMAGE_URL
                f['permalink'] = TRUMPET_IMAGE_URL
                for k in f.keys():
                    if 'thumb_' in k and ('_h' not in k) and ('_w' not in k) and (k != "thumb_tiny"):
                        f[k] = TRUMPET_IMAGE_URL
        if msg.get('subtype') == 'message_changed':
            self.handle_message(msg['message'])
        return msg
        
    def response(self, flow):
        response = flow.response
        if response.headers.get('content-type') == 'application/json; charset=utf-8':
            content = response.get_content()
            data = json.loads(content)

            if 'history' in data or 'messages' in data:
                history = data.get('history', {}).get('messages') or data.get('messages')
                for cur_message in history:
                    if (not isinstance(cur_message, str)) and (cur_message.get('user') in self.banned_users) and (cur_message.get('type') == "message"):
                        self.handle_message(cur_message)
                response.text = json.dumps(data)

                        
            if 'file' in data:
                f = data['file']
                if (not isinstance(f, str)) and f['id'] in self.ids_to_ban:
                    f['name'] = self.bwaaah(f['name'])
                    f['title'] = self.bwaaah(f['title'])
                    f['mimetype'] = 'image/jpeg'
                    f['filetype'] = 'jpeg'
                    f['pretty_type'] = 'jpeg'
                    f['url_private'] = TRUMPET_IMAGE_URL
                    f['url_private_download'] = TRUMPET_IMAGE_URL
                    f['permalink'] = TRUMPET_IMAGE_URL
                    for k in f.keys():
                        if 'thumb_' in k and ('_h' not in k) and ('_w' not in k) and (k != "thumb_tiny"):
                            f[k] = TRUMPET_IMAGE_URL
                response.text = json.dumps(data)
        
    def websocket_message(self, flow):
        cur_message = json.loads(flow.messages[-1].content)
        if cur_message.get('type') == "message":
            if cur_message.get('user') in self.banned_users:
                self.handle_message(cur_message)
                flow.messages[-1].content = json.dumps(cur_message)
            if cur_message.get('subtype') == 'message_changed' and cur_message.get('message',{}).get('user') in self.banned_users:
                self.handle_message(cur_message)
                flow.messages[-1].content = json.dumps(cur_message)

addons = [
    SlackInterceptor()
]
