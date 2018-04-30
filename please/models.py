from django.db import models

# Create your models here.
class SlackAskUs(models.Model):
    
    token=models.TextField(default='')
    team_id=models.TextField(default='')
    team_domain=models.TextField(default='')
    enterprise_id=models.TextField(default='')
    enterprise_name=models.TextField(default='')
    channel_id=models.TextField(default='')
    channel_name=models.TextField(default='')
    user_id=models.TextField(default='')
    user_name=models.TextField(default='')
    command=models.TextField(default='')
    text=models.TextField(default='')
    response_url=models.TextField(default='')
    trigger_id=models.TextField(default='')

    def __str__(self):
        return str(self.token)

class Log(models.Model):
    logtext = models.TextField(default="")
    timestamp = models.TimeField()

    def __str__(self):
        return str(self.timestamp)
      
class AuthenticatedSpaces(models.Model):
    access_token = models.TextField()
    scope= models.TextField()
    user_id= models.TextField()
    team_name= models.TextField()
    team_id= models.TextField(primary_key=True)
    incoming_webhook_channel= models.TextField()
    incoming_webhook_channel_id= models.TextField()
    incoming_webhook_configuration_url= models.TextField()
    incoming_webhook_url= models.TextField()
    bot_user_id= models.TextField()
    bot_access_token= models.TextField()

    def __str__(self):
      return str(self.team_name)