# smashbot
## Contributing
Contact me or open a PR if you'd like to contribute to this project.

## CI/CD
This repo is automatically deployed to a Google Cloud Compute VM every time master is pushed. Unfortunately, this currently results in some downtime as the VM is stopped and restarted. I'm running this thing out of pocket at the moment, so haven't implemented any kind of High Availability functionality. 

## Commands
**Command**|**Description**
:-----|:-----
8!register switch\_tag switch\_code|Register in player list
8!update tag\|code value|Update profile attributes
8!playerlist|List players in server
8!profile @mention\|discord\_name\|switch\_tag|View profile of user (omit to view self)
8!whois @mention\|discord\_name\|switch\_tag|Same as profile
8!imain\|ipocket\|iplay add\|remove fighter|Add/remove a fighter to/from your repertoire
8!remove fighter|Removes a fighter from your repertoire
8!whoplays fighter|Find players in this server who use a fighter
8!fighter fighter|View details/costumes for a fighter
8!hmu|Marks you as looking for a match
8!nothx|Marks you as not looking for a match
8!letsplay|Pings everyone looking for a match
8!coinflip|Self-explanatory