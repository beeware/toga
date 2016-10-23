from rubicon.objc import objc_method

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


class List(WidgetMixin):
    def __init__(self, data=None, on_delete=None, on_refresh=None, style=None):
        super().__init__(style=style)
        self.data = data
        self.on_delete = on_delete
        self.on_refresh = on_refresh

        self.startup()

    def startup(self):
        self._impl = TogaTableViewController.alloc().init()
        self._impl.interface = self

        self._impl.refreshControl = UIRefreshControl.alloc().init()
        self._impl.refreshControl.addTarget_action_forControlEvents_(
            self._impl,
            get_selector('refresh'),
            UIControlEventValueChanged
        )

        self._impl.data = self.data

    def add(self, item):
        self.data.append(item)
        self._impl.tableView.reloadData()
