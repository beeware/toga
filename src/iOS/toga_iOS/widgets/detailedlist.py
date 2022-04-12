from rubicon.objc import SEL, objc_method, objc_property

from toga_iOS.libs import (
    NSIndexPath,
    UIControlEventValueChanged,
    UIRefreshControl,
    UITableViewCell,
    UITableViewCellEditingStyleDelete,
    UITableViewCellEditingStyleInsert,
    UITableViewCellEditingStyleNone,
    UITableViewCellSeparatorStyleNone,
    UITableViewCellStyleSubtitle,
    UITableViewController,
    UITableViewRowAnimationLeft,
    UITableViewScrollPositionNone
)
from toga_iOS.widgets.base import Widget


class TogaTableViewController(UITableViewController):

    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def numberOfSectionsInTableView_(self) -> int:
        return 1

    @objc_method
    def tableView_numberOfRowsInSection_(self, tableView, section: int) -> int:
        return len(self.interface.data)

    @objc_method
    def tableView_cellForRowAtIndexPath_(self, tableView, indexPath):
        cell = tableView.dequeueReusableCellWithIdentifier_("row")
        if cell is None:
            cell = UITableViewCell.alloc().initWithStyle_reuseIdentifier_(UITableViewCellStyleSubtitle, "row")
        value = self.interface.data[indexPath.item]

        cell.textLabel.text = str(getattr(value, 'title', ''))
        cell.detailTextLabel.text = str(getattr(value, 'subtitle', ''))

        # If the value has an icon attribute, get the _impl.
        # Icons are deferred resources, so we bind to factory.
        try:
            cell.imageView.image = value.icon.bind(self.interface.factory).native
        except AttributeError:
            pass

        return cell

    @objc_method
    def tableView_commitEditingStyle_forRowAtIndexPath_(self, tableView, editingStyle: int, indexPath):
        if editingStyle == UITableViewCellEditingStyleDelete:
            item = self.interface.data[indexPath.row]
            if editingStyle == UITableViewCellEditingStyleDelete:
                if self.interface.on_delete:
                    self.interface.on_delete(self.interface, row=item)

                tableView.beginUpdates()
                self.interface.data.remove(item)
                tableView.deleteRowsAtIndexPaths_withRowAnimation_([indexPath], UITableViewRowAnimationLeft)
                tableView.endUpdates()
            elif editingStyle == UITableViewCellEditingStyleInsert:
                pass
            elif editingStyle == UITableViewCellEditingStyleNone:
                pass

    @objc_method
    def refresh(self):
        self.interface.on_refresh(self.interface)

    @objc_method
    def tableView_willSelectRowAtIndexPath_(self, tableView, indexPath):
        index = indexPath.row
        if index == -1:
            selection = None
        else:
            selection = self.interface.data[index]

        if self.interface.on_select:
            self.interface.on_select(self.interface, row=selection)

    # @objc_method
    # def tableView_heightForRowAtIndexPath_(self, tableView, indexPath) -> float:
    #     return 48.0


class DetailedList(Widget):
    def create(self):
        self.controller = TogaTableViewController.alloc().init()
        self.controller.interface = self.interface
        self.controller.impl = self
        self.native = self.controller.tableView

        self.native.separatorStyle = UITableViewCellSeparatorStyleNone

        # Add the layout constraints
        self.add_constraints()

    def set_on_refresh(self, handler: callable or None) -> None:
        if callable(handler):
            self.controller.refreshControl = UIRefreshControl.alloc().init()
            self.controller.refreshControl.addTarget(
                self.controller,
                action=SEL('refresh'),
                forControlEvents=UIControlEventValueChanged
            )
        else:
            if self.controller.refreshControl:
                self.controller.refreshControl.removeFromSuperview()
            self.controller.refreshControl = None

    def after_on_refresh(self, widget, result):
        self.controller.refreshControl.endRefreshing()
        self.controller.tableView.reloadData()

    def change_source(self, source):
        self.native.reloadData()

    def insert(self, index, item):
        self.native.reloadData()

    def change(self, item):
        self.native.reloadData()

    def remove(self, item, index):
        self.native.reloadData()

    def clear(self):
        self.native.reloadData()

    def get_selection(self):
        return None

    def set_on_select(self, handler):
        # No special handling required
        pass

    def set_on_delete(self, handler):
        # No special handling required
        pass

    def scroll_to_row(self, row):
        self.native.scrollToRowAtIndexPath(
            NSIndexPath.indexPathForRow(row, inSection=0),
            atScrollPosition=UITableViewScrollPositionNone,
            animated=False
        )
