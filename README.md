# ignore-abhi
A mitmproxy plugin to block/ignore problematic users in slack. Anything a blocked user says is replaced with nonsensee "bwaaaah"s and all images they uploaded are replaced with trumpet images.

This probably works for the apps but I haven't tested it since it's difficulty to force them to use this proxy or accept our certificate.

This will probably break when slack updates their backend.

# Instructions
* Install mitmproxy
* Configure your browser to point at said proxy
* Install mitmproxy's certificate in said browser (the generated cert should live in ~/.mitmproxy)
* Determine the user IDs of the users you want to ignore (they look something like `U2925636U`). You can get this by looking at the HTML or going to their user profile and looking at the URL..       
* Invoke mitmproxy via something like `mitmdump -q --allow-hosts slack  -s ./ignore.py --set bannedusers=$CSV_LIST_OF_USER_IDS_TO_BAN`

