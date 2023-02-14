from html.parser import HTMLParser

VERSION = "0.0.1"
class HTMLTableParser(HTMLParser):

    def __init__(self):
        super().__init__()

        self.tables = []
        self.headers = []
        self.rows = []
        self.row = []

        self.col = 0
        self.rowspan = []

        self.in_head = False
        self.in_th = False
        self.in_td = False
        self.in_rowspan = False

    @staticmethod
    def get_attr_value(attrs, attr_name):
        for attr in attrs:
            if attr[0] == attr_name:
                return attr[1]

    def fill_cols_using_rowspan(self):
        while self.col < len(self.rowspan) and self.rowspan[self.col] > 0:
            self.row.append(self.rows[len(self.rows)-1][self.col])
            self.col += 1

    def handle_starttag(self, tag, attrs):
        if tag == 'thead':
            self.in_head = True
        if tag == 'th':
            self.in_th = True
        if tag == 'tr':
            self.col = 0
            self.rowspan = [c - 1 if c > 0 else 0 for c in self.rowspan]
            if sum(self.rowspan) == 0:
                self.rowspan = []
            self.fill_cols_using_rowspan()

        if tag == 'td':
            self.in_td = True
            self.col += 1
            rowspan = self.get_attr_value(attrs, 'rowspan')
            self.rowspan.append(int(rowspan) if rowspan else 0)


    def handle_endtag(self, tag):
        if tag == 'thead':
            self.in_head = False
        if tag == 'th':
            self.in_th = False
        if tag == 'td':
            self.in_td = False
            self.fill_cols_using_rowspan()
            
        if tag == 'tr' and not self.in_head:
            self.rows.append(self.row)
            self.row = []
            
        if tag == 'table':
            self.tables.append({
                'headers': self.headers,
                'rows': self.rows,  
            })
            self.headers = []
            self.rows = []

    def handle_data(self, data):
        data_stripped = data.strip()
        if self.in_th and self.in_head:
            self.headers.append(data_stripped)

        if self.in_td and not self.in_head:
            self.row.append(data_stripped)
