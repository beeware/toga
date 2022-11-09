class ParentPosition:
    def __init__(self, adj):
        self.adj = adj

    def is_parent_scrollable(self):
        page_size = self.adj.get_page_size()
        upper = self.adj.get_upper()
        lower = self.adj.get_lower()

        return upper - lower > page_size

    def is_parent_at_top(self):
        value = self.adj.get_value()
        lower = self.adj.get_lower()
        is_at_top = value == lower

        return is_at_top

    def is_parent_at_bottom(self):
        page_size = self.adj.get_page_size()
        value = self.adj.get_value()
        upper = self.adj.get_upper()
        is_at_bottom = value + page_size == upper

        return is_at_bottom

    def is_parent_scrolled(self):
        is_at_top = self._is_parent_at_top()
        is_at_bottom = self._is_parent_at_bottom()

        return not is_at_top and not is_at_bottom

    def is_parent_large(self):
        page_size = self.adj.get_page_size()
        upper = self.adj.get_upper()
        lower = self.adj.get_lower()

        return 2 * page_size < upper - lower

    def is_parent_distant_from_top(self):
        value = self.adj.get_value()
        page_size = self.adj.get_page_size()
        lower = self.adj.get_lower()

        distance_from_top = value - lower

        return distance_from_top >= 0.5 * page_size

    def is_parent_distant_from_bottom(self):
        value = self.adj.get_value()
        page_size = self.adj.get_page_size()
        upper = self.adj.get_upper()

        distance_from_bottom = upper - (value + page_size)

        return distance_from_bottom >= 0.5 * page_size
