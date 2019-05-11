import re

p = re.compile(r'\d+-\d+-\d+\s+\d+:\d+:\d+\s+([A-Z]+)[^[]*\[([^]]+)\]')
comps = {}
for line in open('/usr/share/hassio/homeassistant/home-assistant.log').readlines():
    m = p.match(line)
    if m:
        comp = (m.group(2), m.group(1))
        comps[comp] = comps.get(comp, 0) + 1
for comp in sorted(comps.items(), key=lambda x: x[1], reverse=True):
    print(comp[0][0])
