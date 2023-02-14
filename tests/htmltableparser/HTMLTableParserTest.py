from htmltableparser import HTMLTableParser


def test_no_table():
    html = ""

    parser = HTMLTableParser()
    parser.feed(html)

    assert len(parser.tables) == 0


def test_two_empty_tables():
    html = """
    <table></table><table></table>
"""

    parser = HTMLTableParser()
    parser.feed(html)

    assert len(parser.tables) == 2
    assert parser.tables == [
        {'headers': [], 'rows': []},
        {'headers': [], 'rows': []}
    ]


def test_rowspan():
    html = """
<table>
    <thead>
        <tr><th>Col 1</th><th>Col 2</th></tr>
    </thead>
    <tbody>
        <tr><td>Val11</td><td rowspan="2">Val12</td></tr>
        <tr><td>Val2</td></tr>
    </tbody>
</table>
"""

    parser = HTMLTableParser()
    parser.feed(html)

    assert len(parser.tables) == 1
    assert parser.tables[0] == {
        'headers': ['Col 1', 'Col 2'],
        'rows': [
            ['Val11', 'Val12'],
            ['Val2', 'Val12']
        ]
    }


def test_rowspan_on_first_column():
    html = """
<table>
    <thead>
        <tr><th>Col 1</th><th>Col 2</th></tr>
    </thead>
    <tbody>
        <tr><td rowspan="2">Val11</td><td>Val12</td></tr>
        <tr><td>Val2</td></tr>
    </tbody>
</table>
"""

    parser = HTMLTableParser()
    parser.feed(html)

    assert len(parser.tables) == 1
    assert parser.tables[0] == {
        'headers': ['Col 1', 'Col 2'],
        'rows': [
            ['Val11', 'Val12'],
            ['Val11', 'Val2']
        ]
    }


def test_rowspan_on_all_columns():
    html = """
<table>
    <thead>
        <tr><th>Col 1</th><th>Col 2</th></tr>
    </thead>
    <tbody>
        <tr><td rowspan="2">Val11</td><td rowspan="2">Val12</td></tr>
        <tr></tr>
    </tbody>
</table>
"""

    parser = HTMLTableParser()
    parser.feed(html)

    assert len(parser.tables) == 1
    assert parser.tables[0] == {
        'headers': ['Col 1', 'Col 2'],
        'rows': [
            ['Val11', 'Val12'],
            ['Val11', 'Val12']
        ]
    }