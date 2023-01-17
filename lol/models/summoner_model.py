import json

class Summoner(object):

  def __init__(self, id, accountId, puuid, name, profileIconId, revisionDate, summonerLevel):
    self.id = id
    self.accountId = accountId
    self.puuid = puuid
    self.name = name
    self.profileIconId = profileIconId
    self.revisionDate = revisionDate
    self.summonerLevel = summonerLevel  

  def __str__(self):
    return self.name

  def to_json(self):
    return json.dumps(self, default=vars)

  def from_json(payload):
    return Summoner(**json.loads(payload))