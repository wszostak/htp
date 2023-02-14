HTML Table Parser
=================

It is very simple implementation just for parsing data from my Solar system app. 

Usage
-----

```python
from htp import HTMLTableParser

html = """
<table>
	<thead>
		<tr><th>Col name</th></tr>
	</thead>
	<tbody>
		<tr><td rowspan="2">Val11</td><td>Val12</td></tr>
		<tr><td>Val2</td></tr>
	</tbody>
</table>
"""

parser = HTMLTableParser()
parser.feed(html)
print(parser.tables)
```

In result we get:

```python
[{'headers': ['Col name'], 'rows': [['Val11', 'Val12'], ['Val2', 'Val12']]}]
```