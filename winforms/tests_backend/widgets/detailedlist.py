from .table import TableProbe


class DetailedListProbe(TableProbe):
    supports_actions = False
    supports_refresh = False

    def assert_cell_content(self, row, title, subtitle, icon=None):
        super().assert_cell_content(row, 0, title, icon=icon)
        super().assert_cell_content(row, 1, subtitle)
