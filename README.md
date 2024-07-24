# pygo_API

Python Module to access the YGOProDeck API

## Instalation

```bash
pip install pygo-API==0.1.0
```

## YGOProDeck Params and API queries

API queries:

|query|usage|params|
|---|---|---|
|name|get card by string|string|
|archetype|get cards of specific archetype|string|
|level|get cards of specific level|int|
|atribute|get cards of specific atribute|string|
|banlist|only returns if card is on chosen banlist|string|
|cardset|get cards from declared set|string|
|fname|search card by partial name|string|
|race|get cards of specific attribute|string|
|format|get cards from chosen fromat|string|
|linkmarker|filter by link markers|string|
|misc|add YGOProDeck specific data to JSON dict|yes|
|staple|show cards considered staple|yes|
|startdate|exclude cards relesed before set date|yyyy-mm-dd|
|enddate|exclude cards relesed after set date|yyyy-mm-dd|
|type|filter by card type e.g. spell, counter trap|string|
|language|get output in specified language|string|

Params

|type|race|language|
|---|---|---|
|Effect Monster|Aqua|fr|
|Flip Effect Monster|Beast|de|
|Flip Tuner Effect Monster|Beast-Warrior|it|
|Gemini Monster|Creator-God|pt|
|Normal Monster|Cybers||
|Normal Tuner Monster|Dinosaur||
|Pendulum Effect Monster|Divine-Beast||
|Pendulum Effect Ritual Monster|Dragon||
|Pendulum Flip Effect Monster|Fairy||
|Pendulum Normal Monster|Fiend||
|Pendulum Tuner Effect Monster|Fish||
|Ritual Effect Monster|Insect||
|Ritual Monster|Machine||
|Spell Card|Plant||
|Spirit Monster|Psychic||
|Toon Monster|Pyro||
|Trap Card|Reptile||
|Tuner Monster|Rock||
|Union Effect Monster|Sea Serpent||
|Fusion Monster|Spellcaster||
|Link Monster|Thunder||
|Pendulum Effect Fusion Monster|Warrior||
|Synchro Monster|Winged Beast||
|Synchro Pendulum Effect Monster|Wyrm||
|Synchro Tuner Monster|Zombie||
|XYZ Monster|Normal||
|XYZ Pendulum Effect Monster|Field||
|Skill Card|Equip||
|Token|Continuous||
||Quick-Play||
||Ritual||
||Normal||
||Continuous||
||Counter||

## Usage

```python
import pygo_API
```

use to include the module

```python
image = pygo_API.Image("normal", "kuriboh").getImage()
```

Saves the image of "Kuriboh" in the variable image as well as caching it.

```python
print(pygo_API.Card(name="kuriboh").getData())
```

Prints the entire data of "kuriboh".

```python
print(pygo_API.Card().random())
```

prints a random card dict

## Examples

### Get All Cards

```python
tcg = pygo_API.Card().getData()

print(tcg)
```

**Warning**: The output is a JSON dict with roughly 670,000 lines, so be careful with generic API requests.

### Get Specific Link Monsters

```python
dragons = pygo_API.Card(fname="dragon", linkmarker="bottom,top,left").getData()
```

Saves all Linkmonsters with "dragon" in their name and Linkarrows pointing to the bottom, top and left to the "dragons" variable.

### Get All Staple Cards

```python
staples = pygo_API.Card(staple="yes").getData()

print(staples)
```

Prints every card considered a staple by YGOProDeck

### Get Cards from TCG Banlist within a Date Range

```python
tcg = pygo_API.Card(banlist="tcg", startdate="2020-01-01", enddate="2024-01-01").getData()
```

Get all cards added to the tcg banlist between first of january 2020 and the first of january 2024

### Search then sort cards by name

```python
tcg = pygo_API.Card(fname="snake-eye", sort="name").getData(fields=["name", "id"])

print(tcg)
```

Print all "snake-eye" cards sortet by name and only show their name and id.

### Get Card Text

```python
print(pygo_API.Card(name="kuriboh").getData(fields=["desc"]))
```

Print out the card text of kuriboh

### Caching

Every API request is cached for the duration of the program or script.

Alternatavly you can use:

```python
pygo_API.Cache().clear_cache()
```

to clear the cache mid code.

The cachfile is stored as the URL encrypted to SHA-256

## Method arguments

### Filter Returned Data

```python
.getData(fields=["name"])
```

The "fields" argument takes only arrays as input and then lets the method return only the keys of that name.

### Sort Output

```python
pygo_API.Card(sort="name")
```

The "sort" argument sorts your output from A-Z with the given dict key.

### Save Image locally

```python
pygo_API.Image(save=True)
```

If the "save" argument is set to "True" the method will save the Image in a local directory as a .jpg file.
