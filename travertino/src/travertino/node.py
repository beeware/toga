class Node:
    def __init__(self, style, applicator=None, children=None):
        # Parent needs to be primed before style is (potentially) applied with
        # assignment of applicator.
        self._parent = None
        self._root = None

        # Explicitly set the internal attribute first, since the setter for style will
        # access the applicator property.
        self._applicator = None

        self.style = style
        self.applicator = applicator

        if children is None:
            self._children = None
        else:
            self._children = []
            for child in children:
                self.add(child)

    @property
    def style(self):
        """The node's style.

        Assigning a style triggers an application of that style if an applicator has
        already been assigned.
        """
        return self._style

    @style.setter
    def style(self, style):
        self._style = style.copy()
        self.intrinsic = self.style.IntrinsicSize()
        self.layout = self.style.Box(self)

        if self.applicator:
            self.style._applicator = self.applicator

    @property
    def applicator(self):
        """This node's applicator, which handles applying the style.

        Assigning an applicator triggers an application of the node's style.
        """
        return self._applicator

    @applicator.setter
    def applicator(self, applicator):
        if self.applicator:
            # If an existing applicator is present, clear its reference to this node.
            self.applicator.node = None

        if applicator:
            # This needs to happen *before* assigning the applicator to the style,
            # below, because as part of receiving the applicator, the style will apply
            # itself. How this happens will vary with applicator implementation, but
            # will probably need access to the node.
            applicator.node = self

        self._applicator = applicator
        # This triggers style.apply():
        self.style._applicator = applicator

    @property
    def root(self):
        """The root of the tree containing this node.

        Returns:
            The root node. Returns self if this node *is* the root node.
        """
        return self._root if self._root else self

    @property
    def parent(self):
        """The parent of this node.

        Returns:
            The parent of this node. Returns None if this node is the root node.
        """
        return self._parent

    @property
    def children(self):
        """The children of this node.
        This *always* returns a list, even if the node is a leaf
        and cannot have children.

        Returns:
            A list of the children for this widget.
        """
        if self._children is None:
            return []
        else:
            return self._children

    @property
    def can_have_children(self):
        """Determine if the node can have children.

        This does not resolve whether there actually *are* any children;
        it only confirms whether children are theoretically allowed.
        """
        return self._children is not None

    def add(self, child):
        """Add a node as a child of this one.
        Args:
            child: A node to add as a child to this node.

        Raises:
            ValueError: If this node is a leaf, and cannot have children.
        """
        if self._children is None:
            raise ValueError("Cannot add children")

        self._children.append(child)
        child._parent = self
        self._set_root(child, self.root)

    def insert(self, index, child):
        """Insert a node as a child of this one.
        Args:
            index: Index of child position.
            child: A node to insert as a child to this node.

        Raises:
            ValueError: If this node is a leaf, and cannot have children.
        """
        if self._children is None:
            raise ValueError("Cannot insert child")

        self._children.insert(index, child)
        child._parent = self
        self._set_root(child, self.root)

    def remove(self, child):
        """Remove child from this node.
        Args:
            child: The child to remove from this node.

        Raises:
            ValueError: If this node is a leaf, and cannot have children.
        """
        if self._children is None:
            raise ValueError("Cannot remove children")

        self._children.remove(child)
        child._parent = None
        self._set_root(child, None)

    def clear(self):
        """Clear all children from this node."""
        if self._children is None:
            # This is a leaf, so do nothing.
            return

        for child in self._children:
            child._parent = None
            self._set_root(child, None)
        self._children = []

    def refresh(self, viewport):
        """Refresh the layout and appearance of the tree this node is contained in."""
        if self._root:
            self._root.refresh(viewport)
        else:
            if self.applicator:
                ######################################################################
                # 2024-12: Backwards compatibility for Toga <= 0.4.8
                ######################################################################
                # Accommodate the earlier signature of layout(), which included the node
                # as a parameter.
                try:
                    self.style.layout(viewport)
                except TypeError as error:
                    if "layout() missing 1 required positional argument:" in str(error):
                        self.style.layout(self, viewport)
                    else:
                        raise
                ######################################################################
                # End backwards compatibility
                ######################################################################

                self.applicator.set_bounds()

    def _set_root(self, node, root):
        # Propagate a root node change through a tree.
        node._root = root
        for child in node.children:
            self._set_root(child, root)
