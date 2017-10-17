from rubicon.objc import objc_method
from .base import Widget
from ..libs import *


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
        cell.textLabel.text = self.interface.data[indexPath.item]
        return cell

    @objc_method
    def tableView_commitEditingStyle_forRowAtIndexPath_(self, tableView, editingStyle: int, indexPath):
        if editingStyle == UITableViewCellEditingStyleDelete:
            item = self.data[indexPath.row]

            if self.interface.on_delete:
                self.interface.on_delete(self.interface, indexPath.row)

            del self.interface.data[indexPath.row]
            # FIXME When deleting a item form the list the following lines cause a error.
            self.tableView.reloadData()  # Just a hack for now! No animation!
            # paths = NSArray.alloc().initWithObjects_(indexPath, None)
            # tableView.deleteRowsAtIndexPaths_withRowAnimation_(paths, UITableViewRowAnimationFade)

    @objc_method
    def refresh(self):
        if self.interface.on_refresh:
            self.interface.on_refresh(self.interface)
        self.refreshControl.endRefreshing()
        self.tableView.reloadData()

    @objc_method
    def tableView_willSelectRowAtIndexPath_(self, tableView, indexPath):
        if self.interface.on_select:
            self.interface.on_select(self.interface, indexPath.row)


class DetailedList(Widget):
    def create(self):
        self.controller = TogaTableViewController.alloc().init()
        self.controller.interface = self.interface
        self.native = self.controller.tableView

        # Add the layout constraints
        self.add_constraints()

    def enable_refresh(self, value: bool) -> None:
        if value:
            self.controller.refreshControl = UIRefreshControl.alloc().init()
            self.controller.refreshControl.addTarget_action_forControlEvents_(
                self.controller,
                SEL('refresh'),
                UIControlEventValueChanged
            )

    def set_data(self, data):
        self.controller.data = data

    def add(self, item):
        self.controller.tableView.reloadData()
