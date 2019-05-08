import pynder
import robobrowser
import re

MOBILE_USER_AGENT = r"Tinder/7.5.3 (iPhone; iOS 10.3.2; Scale/2.00)"
# MOBILE_USER_AGENT = r"Mozilla/5.0 (Linux; U; en-gb; KFTHWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Silk/3.16 Safari/535.19"
# FB_AUTH = "https://www.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&display=touch&state=%7B%22challenge%22%3A%22IUUkEUqIGud332lfu%252BMJhxL4Wlc%253D%22%2C%220_auth_logger_id%22%3A%2230F06532-A1B9-4B10-BB28-B29956C71AB1%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&default_audience=friends&return_scopes=true&auth_type=rerequest&client_id=464891386855067&ret=login&sdk=ios&logger_id=30F06532-A1B9-4B10-BB28-B29956C71AB1&ext=1470840777&hash=AeZqkIcf-NEW6vBd"
FB_AUTH = "https://m.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&display=touch&state=%7B%22challenge%22%3A%22IUUkEUqIGud332lfu%252BMJhxL4Wlc%253D%22%2C%220_auth_logger_id%22%3A%2230F06532-A1B9-4B10-BB28-B29956C71AB1%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&default_audience=friends&return_scopes=true&auth_type=rerequest&client_id=464891386855067&ret=login&sdk=ios&logger_id=30F06532-A1B9-4B10-BB28-B29956C71AB1&ext=1470840777&hash=AeZqkIcf-NEW6vBd"

def get_access_token(email, password):
    s = robobrowser.RoboBrowser(user_agent=MOBILE_USER_AGENT, parser="lxml")
    s.open(FB_AUTH)
    f = s.get_form()
    f["pass"] = password
    f["email"] = email
    s.submit_form(f)
    f = s.get_form()
    if f.submit_fields.get('__CONFIRM__'):
        s.submit_form(f, submit=f.submit_fields['__CONFIRM__'])
    else:
        raise Exception("Couldn't find the continue button. Maybe you supplied the wrong login credentials? Or maybe Facebook is asking a security question?")
    access_token = re.search(r"access_token=([\w\d]+)", s.response.content.decode()).groups()[0]
    return access_token


FBTOKEN = str(get_access_token('komarekzm@gmail.com', '1abracham'))

print(FBTOKEN)
FBID = "100007971436724"
# FBTOKEN= "YOUR_FB_TOKEN"

session = pynder.Session(facebook_id=FBID, facebook_token=FBTOKEN)
friends = session.get_fb_friends()

# Print the names of all facebook friends using Tinder Social.
print(", ".join([x.name for x in friends]))

# Get the user_info of these facebook friends.
user_info_objects = []
for friend in friends:
    user_info_objects.append(friend.get_tinder_information())

# Print the bios.
for user_info, friend in zip(user_info_objects, friends):
    print("=" * 50)
    # Use Friend.name, as user_info.name only contains first name.
    print(friend.name)
    print(friend.facebook_link)
    print("-" * 50)
    print(user_info.bio)
print("=" * 50)
