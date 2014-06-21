Chrono
======

A natural language date parser. Chrono extracts date informations from any given text using low-level pattern matching. Thus, it's fast and doesn't has any dependency. 

Chrono supports a number of date and time formats, including :

* 2014-12-13 12:00:00
* 10/13/2013
* Sat Aug 17 2013 18:40:39 
* Saturday, 17 August 2013 - Monday, 19 August 2013

### Installation

The current recommended way is installing directly from Github.

    pip install git+git://github.com/wanasit/chrono-python.git


## USAGE

Just pass a string to function `parse` or `parse_date`. 

```python
import chrono

chrono.parse('12 June')
# return an array of [chrono.ParsedResult]
# [<ParsedResult "12 June" : 2014-06-12 12:00:00 >] 

chrono.parse_date('12 June')
# return a Python's standard datetime.datetime
# datetime.datetime(2014, 6, 12, 12, 0)
```
