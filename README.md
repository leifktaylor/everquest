# PyEQ
### Set of commandline tools to assist in large scale Everquest Boxing

## Getting started:

### pyeq_settings.yml
(Required) Must give correct paths to your everquest and mq2 folders here

### pyeq_settings/characters.txt
(Required} Must add character names, account names, and passwords here

### pyeq_settings/sessions.yml
Create login sessions here, using the character names defined in characters.txt

### Running PyEQ:
Once you have defined your sessions (in pyeq_settings/sessions.yml), go to your command prompt and run:
```
python pyeq.py <session_name>
```

### Troubleshooting:
1. It is highly recommended that you put your everquest binaries, and mq2, within this folder.
2. If autologin is being finicky, try manually using Mq2AutoLogin first, so that it is enabled,
then rerun.
3. Make sure you have all the dependencies to run PyEQ.  That is, Python 2.6 or greater, pyaml, and jinja2.
To download jinja2 and pyaml, simply issue this command (once you have installed python) from the commandline:
```
pip install jinja2
pip install pyaml
```