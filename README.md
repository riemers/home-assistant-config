# home-assistant-config <a href="https://travis-ci.org/riemers/home-assistant-config"><img src="https://travis-ci.org/riemers/home-assistant-config.svg?branch=master"/></a>

Just my home assistant configuration, like many others, but this is mine..

Fun things, warn on sonos if girlfriend is coming home, how long it will take her before she comes home (including traffic)
Disable lights outside, tell on sonos "don't do that" since its light outside if people do switch the lights

Nice things, battery component. Shows all your battery powered items easily.

***
How to see all ip's from all containers (needed it sometimes)
```bash
docker inspect --format='{{.Name}} - {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -aq)
```
Make a secrets file for travis, will replace _url screts with dummy urls.
```bash
for i in `cut -f1 -d":" secrets.yaml`;do;echo $i: $(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1);done | sed 's/_url:.*/_url: https:\/\/www.some.url.com/' |sed 's/latitude:.*/latitude: -27.121978/'|sed 's/longitude:.*/longitude: -109.288981/' > travis_secrets.yaml
```