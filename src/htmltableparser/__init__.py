from html.parser import HTMLParser

class HTMLTableParser(HTMLParser):

    tables = []
    headers = []
    rows = []
    row = []

    col = 0
    rowspan = []

    in_head = False
    in_th = False
    in_td = False
    in_rowspan = False

    @staticmethod
    def get_attr_value(attrs, attr_name):
        for attr in attrs:
            if attr[0] == attr_name:
                return attr[1]

    def handle_starttag(self, tag, attrs):
        if tag == 'thead':
            self.in_head = True
        if tag == 'th':
            self.in_th = True
        if tag == 'tr':
            self.col = 0
        if tag == 'td':
            if not self.in_rowspan:
                rowspan = self.get_attr_value(attrs, 'rowspan')
                self.rowspan.append(int(rowspan) if rowspan else 0)
            self.in_td = True

    def handle_endtag(self, tag):
        if tag == 'thead':
            self.in_head = False
        if tag == 'th':
            self.in_th = False
        if tag == 'td':
            self.col += 1
            self.in_td = False
            while self.col < len(self.rowspan) and self.rowspan[self.col] > 0:
                self.row.append(self.rows[len(self.rows)-1][self.col])
                self.col += 1
            
        if not self.in_head and tag == 'tr':
            self.rows.append(self.row)
            self.rowspan = [c - 1 if c > 0 else 0 for c in self.rowspan]
            self.in_rowspan = sum(self.rowspan) > 0
            if not self.in_rowspan:
                self.rowspan = []
            self.row = []
            
        if tag == 'table':
            self.tables.append({
                'headers': self.headers,
                'rows': self.rows,  
            })
            self.headers = []
            self.rows = []

    def handle_data(self, data):
        if self.in_head and self.in_th:
            self.headers.append(data)

        if not self.in_head and self.in_td:
            self.row.append(data.strip())
