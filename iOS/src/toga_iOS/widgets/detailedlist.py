from rubicon.objc import (
    SEL,
    ObjCBlock,
    ObjCInstance,
    objc_method,
    objc_property,
)
from travertino.size import at_least

from toga_iOS.libs import (
    NSIndexPath,
    UIContextualAction,
    UIContextualActionStyle,
    UIControlEventValueChanged,
    UIRefreshControl,
    UISwipeActionsConfiguration,
    UITableViewCell,
    UITableViewCellSeparatorStyleNone,
    UITableViewCellStyleSubtitle,
    UITableViewController,
    UITableViewScrollPositionNone,
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
        cell = tableView.dequeueReusableCellWithIdentifier("row")
        if cell is None:
            cell = (
                UITableViewCell.alloc()
                .initWithStyle(UITableViewCellStyleSubtitle, reuseIdentifier="row")
                .autorelease()
            )

        value = self.interface.data[indexPath.item]

        try:
            label = getattr(value, self.interface.accessors[0])
            if label is None:
                cell.textLabel.text = self.interface.missing_value
            else:
                cell.textLabel.text = str(label)
        except AttributeError:
            cell.textLabel.text = self.interface.missing_value

        try:
            label = getattr(value, self.interface.accessors[1])
            if label is None:
                cell.detailTextLabel.text = self.interface.missing_value
            else:
                cell.detailTextLabel.text = str(label)
        except AttributeError:
            cell.detailTextLabel.text = self.interface.missing_value

        try:
            cell.imageView.image = getattr(
                value, self.interface.accessors[2]
            )._impl.native
        except AttributeError:
            cell.imageView.image = None

        return cell

    @objc_method
    def tableView_didSelectRowAtIndexPath_(self, tableView, indexPath):
        self.interface.on_select()

    # UITableViewDelegate methods
    @objc_method
    def tableView_trailingSwipeActionsConfigurationForRowAtIndexPath_(
        self, tableView, indexPath
    ):
        if self.impl.primary_action_enabled:
            actions = [
                UIContextualAction.contextualActionWithStyle(
                    (
                        UIContextualActionStyle.Destructive
                        if self.interface._primary_action in self.impl.DESTRUCTIVE_NAMES
                        else UIContextualActionStyle.Normal
                    ),
                    title=self.interface._primary_action,
                    handler=self.impl.primary_action_handler(indexPath.row),
                )
            ]
        else:
            actions = []

        return UISwipeActionsConfiguration.configurationWithActions(actions)

    @objc_method
    def tableView_leadingSwipeActionsConfigurationForRowAtIndexPath_(
        self, tableView, indexPath
    ):
        if self.impl.secondary_action_enabled:
            actions = [
                UIContextualAction.contextualActionWithStyle(
                    (
                        UIContextualActionStyle.Destructive
                        if self.interface._secondary_action
                        in self.impl.DESTRUCTIVE_NAMES
                        else UIContextualActionStyle.Normal
                    ),
                    title=self.interface._secondary_action,
                    handler=self.impl.secondary_action_handler(indexPath.row),
                )
            ]
        else:
            actions = []

        return UISwipeActionsConfiguration.configurationWithActions(actions)

    @objc_method
    def refresh(self):
        self.interface.on_refresh()


class DetailedList(Widget):
    DESTRUCTIVE_NAMES = {"Delete", "Remove"}

    def create(self):
        self.native_controller = TogaTableViewController.alloc().init()
        self.native_controller.interface = self.interface
        self.native_controller.impl = self

        self.native = self.native_controller.tableView
        self.native.separatorStyle = UITableViewCellSeparatorStyleNone
        self.native.delegate = self.native_controller

        self.primary_action_enabled = False
        self.secondary_action_enabled = False

        # Add the layout constraints
        self.add_constraints()

    def set_refresh_enabled(self, enabled):
        if enabled:
            if self.native_controller.refreshControl is None:
                self.native_controller.refreshControl = UIRefreshControl.alloc().init()
                self.native_controller.refreshControl.addTarget(
                    self.native_controller,
                    action=SEL("refresh"),
                    forControlEvents=UIControlEventValueChanged,
                )
        else:
            if self.native_controller.refreshControl:
                self.native_controller.refreshControl.removeFromSuperview()
            self.native_controller.refreshControl = None

    def set_primary_action_enabled(self, enabled):
        self.primary_action_enabled = enabled

    def primary_action_handler(self, row):
        def handle_primary_action(
            action: ObjCInstance,
            sourceView: ObjCInstance,
            actionPerformed: ObjCInstance,
        ) -> None:
            item = self.interface.data[row]
            self.interface.on_primary_action(row=item)
            ObjCBlock(actionPerformed, None, bool)(True)

        return handle_primary_action

    def set_secondary_action_enabled(self, enabled):
        self.secondary_action_enabled = enabled

    def secondary_action_handler(self, row):
        def handle_secondary_action(
            action: ObjCInstance,
            sourceView: ObjCInstance,
            actionPerformed: ObjCInstance,
        ) -> None:
            item = self.interface.data[row]
            self.interface.on_secondary_action(row=item)
            ObjCBlock(actionPerformed, None, bool)(True)

        return handle_secondary_action

    def after_on_refresh(self, widget, result):
        self.native_controller.refreshControl.endRefreshing()
        self.native_controller.tableView.reloadData()

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
        path = self.native.indexPathForSelectedRow
        if path:
            return path.item
        else:
            return None

    def scroll_to_row(self, row):
        self.native.scrollToRowAtIndexPath(
            NSIndexPath.indexPathForRow(row, inSection=0),
            atScrollPosition=UITableViewScrollPositionNone,
            animated=False,
        )

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
