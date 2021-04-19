Chat = {
    'ChatID': 1,
    'Rang': 44,
    'Name': 'Rutukute',
    'Description': 'gerrynikoll@gmail.com',
    'FounderID': 1,

    'Members': [Member.object, Member.object, Member.object, Member.object],
    'Messages': [Message.object, Message.object, Message.object, Message.object]

    'Integrations': [Integration.YouTube, Integration.Twitch],
    'Country': [country.Ukraine],
    'Language': [language.ukrainian],
    'Interest': [Interest.Dota2, Interest.Satisfactory, Interest.IT],

    'isPublic': True,
    'isBanned': Ban.No,
    'CreateDate': '19.04.2021 | 16:21:45'
}

Member = {
    'UserID': 1,
    'Permissions': [Permission.admin, Permission.write, Permission.DeteleMessage],
    'Joined': '19.04.2021 | 16:21:45'
}

Message = {
    'MessageID': 1,
    'From': 1, #member ID
    'Type': MessageType.plainText,
    'isDelete': False,
    'SendDate': '19.04.2021 | 16:21:45'
}