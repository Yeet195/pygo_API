# pygo

Python Module to access the YGOProDeck API

## Usage

```python
import pygo
```

use to include the module

```python
image = pygo.APIImageLookUp("normal", "kuriboh").getImage()
```

Saves the image of "Kuriboh" in the variable image as well as caching it.

```python
print(pygo.APILookUp(name="kuriboh").getData())
```

Prints the entire data of "kuriboh".

## Examples

```python
tcg = pygo.APILookUp().getData()

print(tcg)
```

Print all Cards

>### WARNING
>
>The above output is a JSON dict with roughly 670000 lines so be carefull with generic API requests

```python
dragons = pygo.APILookUp(fname="dragon", linkmarker="bottom,top,left").getData()
```

Saves all Linkmonsters with "dragon" in their name and Linkarrows pointing to the bottom, top and left to the "dragons" variable.

```python
staples = pygo.APILookUp(staple="yes").getData()

print(staples)
```

Prints every card considered a staple by YGOProDeck

```python
tcg = pygo.APILookUp(banlist="tcg", startdate="2020-01-01", enddate="2024-01-01").getData()
```

Get all cards added to the tcg banlist between first of january 2020 and the first of january 2024

### Caching

Every API request is cached for the duration of the program or script.

Alternatavly you can use:

```python
pygo.Cache().clear_cache()
```

to clear the cache mid code.

The cachfile is stored as the URL encrypted to SHA-256
