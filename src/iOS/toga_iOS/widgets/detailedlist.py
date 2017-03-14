from rubicon.objc import objc_method

from toga.interface import DetailedList as DetailedListInterface

from .base import WidgetMixin
from ..libs import *
# from ..utils import process_callback


class TogaTableViewController(UITableViewController):
    @objc_method
    def numberOfSectionsInTableView_(self) -> int:
        return 1

    @objc_method
    def tableView_numberOfRowsInSection_(self, tableView, section: int) -> int:
        return len(self.data)

    @objc_method
    def tableView_cellForRowAtIndexPath_(self, tableView, indexPath):
        cell = tableView.dequeueReusableCellWithIdentifier_("row")
        if cell is None:
            cell = UITableViewCell.alloc().initWithStyle_reuseIdentifier_(UITableViewCellStyleDefault, "row")

        cell.textLabel.text = self.interface.data[indexPath.item]['description']
        return cell

    @objc_method
    def tableView_commitEditingStyle_forRowAtIndexPath_(self, tableView, editingStyle: int, indexPath):
        if editingStyle == UITableViewCellEditingStyleDelete:
            item = self.data[indexPath.row]

            if self.interface.on_delete:
                self.interface.on_delete(self.interface)

            del self.data[indexPath.row]

            paths = NSArray.alloc().initWithObjects_(indexPath, None)
            tableView.deleteRowsAtIndexPaths_withRowAnimation_(paths, UITableViewRowAnimationFade)

    @objc_method
    def refresh(self):
        if self.interface.on_refresh:
            self.interface.on_refresh(self.interface)
        self.refreshControl.endRefreshing()
        self.tableView.reloadData()


class DetailedList(DetailedListInterface, WidgetMixin):
    def __init__(self, id=None, data=None, on_delete=None, on_refresh=None, style=None):
        super().__init__(id=id, data=data, on_delete=on_delete, on_refresh=on_refresh, style=style)
        self._create()

    def create(self):
        self._controller = TogaTableViewController.alloc().init()
        self._controller.interface = self
        self._impl = self._controller.tableView

        self._controller.refreshControl = UIRefreshControl.alloc().init()
        self._controller.refreshControl.addTarget_action_forControlEvents_(
            self._controller,
            get_selector('refresh'),
            UIControlEventValueChanged
        )

        self._controller.data = self._config['data']

        # Add the layout constraints
        self._add_constraints()

    def _add(self, item):
        self.data.append(item)
        self._controller.tableView.reloadData()

