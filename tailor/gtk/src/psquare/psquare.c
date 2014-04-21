#include <gtk/gtk.h>
#include <math.h>
#include "psquare.h"

/* Private class member */
#define P_SQUARE_PRIVATE(obj) (G_TYPE_INSTANCE_GET_PRIVATE((obj), \
	P_SQUARE_TYPE, PSquarePrivate))

typedef struct _PSquarePrivate PSquarePrivate;

struct _PSquarePrivate
{
	GList *children;
};

/* Forward declarations */
static void p_square_get_preferred_width(GtkWidget *widget,
	int *minimal, int *natural);
static void p_square_get_preferred_height(GtkWidget *widget,
	int *minimal, int *natural);
static void p_square_size_allocate(GtkWidget *widget,
	GtkAllocation *allocation);
static GType p_square_child_type(GtkContainer *container);
static void p_square_add(GtkContainer *container, GtkWidget *widget);
static void p_square_remove(GtkContainer *container, GtkWidget *widget);
static void p_square_forall(GtkContainer *container, gboolean include_internals, GtkCallback callback, gpointer callback_data);

/* Define the PSquare type and inherit from GtkContainer */
G_DEFINE_TYPE(PSquare, p_square, GTK_TYPE_CONTAINER);

/* Initialize the PSquare class */
static void
p_square_class_init(PSquareClass *klass)
{
	/* Override GtkWidget methods */
	GtkWidgetClass *widget_class = GTK_WIDGET_CLASS(klass);
	widget_class->get_preferred_width = p_square_get_preferred_width;
	widget_class->get_preferred_height = p_square_get_preferred_height;
	widget_class->size_allocate = p_square_size_allocate;

	/* Override GtkContainer methods */
	GtkContainerClass *container_class = GTK_CONTAINER_CLASS(klass);
	container_class->child_type = p_square_child_type;
	container_class->add = p_square_add;
	container_class->remove = p_square_remove;
	container_class->forall = p_square_forall;

	/* Add private indirection member */
	g_type_class_add_private(klass, sizeof(PSquarePrivate));
}

/* Initialize a new PSquare instance */
static void
p_square_init(PSquare *square)
{
	/* This means that PSquare doesn't supply its own GdkWindow */
	gtk_widget_set_has_window(GTK_WIDGET(square), FALSE);
	/* Set redraw on allocate to FALSE if the top left corner of your widget
	 * doesn't change when it's resized; this saves time */
	/*gtk_widget_set_redraw_on_allocate(GTK_WIDGET(square), FALSE);*/

	/* Initialize private members */
	PSquarePrivate *priv = P_SQUARE_PRIVATE(square);
	priv->children = NULL;
}

/* Return a new PSquare cast to a GtkWidget */
GtkWidget *
p_square_new()
{
	return GTK_WIDGET(g_object_new(p_square_get_type(), NULL));
}

/* Convenience function for counting the number of visible
 * children, for use with g_list_foreach() */
static void
count_visible_children(GtkWidget *widget, unsigned *n_visible_children)
{
	if(gtk_widget_get_visible(widget))
		(*n_visible_children)++;
}

/* Determines the number of columns and rows in this square */
unsigned
get_n_columns_and_rows(PSquare *self)
{
	PSquarePrivate *priv = P_SQUARE_PRIVATE(self);

	/* Count the visible children */
	unsigned n_visible_children = 0;
	g_list_foreach(priv->children, (GFunc)count_visible_children,
		&n_visible_children);
	if(n_visible_children == 0)
		return 0;

	/* Calculate the number of columns */
	return (unsigned)ceil(sqrt((double)n_visible_children));
}

/* Consults all of the square's children, asking for their preferred
 * width (if direction is horizontal) or height (if direction is
 * vertical) and returns an array of GtkRequestedSize for each column
 * (if widths) or row (if heights). Free the array with g_free() when
 * done. */
static GtkRequestedSize *
get_group_sizes(PSquare *self, GtkOrientation direction, unsigned n_groups)
{
	PSquarePrivate *priv = P_SQUARE_PRIVATE(self);

	/* Allocate an array for the size of each column/row */
	GtkRequestedSize *sizes = g_new0(GtkRequestedSize, n_groups);

	/* Get each child's size; set the width of each group
	 * to the maximum size of each child in that group */
	unsigned count = 0;
	GList *iter;
	for(iter = priv->children; iter; iter = g_list_next(iter)) {
		if(!gtk_widget_get_visible(iter->data))
			continue;

		int child_minimal, child_natural;
		unsigned group_num;
		if(direction == GTK_ORIENTATION_HORIZONTAL) {
			gtk_widget_get_preferred_width(iter->data,
				&child_minimal, &child_natural);
			group_num = count % n_groups;
		} else {
			gtk_widget_get_preferred_height(iter->data,
				&child_minimal, &child_natural);
			group_num = count / n_groups;
		}

		sizes[group_num].minimum_size =
			MAX(child_minimal, sizes[group_num].minimum_size);
		sizes[group_num].natural_size =
			MAX(child_natural, sizes[group_num].natural_size);

		count++;
	}

	return sizes;
}

/* Like get_group_sizes(), but gets height for width or width for height */
static GtkRequestedSize *
get_group_sizes_for_sizes(PSquare *self, GtkOrientation direction, GtkRequestedSize *perpendicular_sizes, unsigned n_groups)
{
	PSquarePrivate *priv = P_SQUARE_PRIVATE(self);

	/* Allocate an array for the size of each column/row */
	GtkRequestedSize *sizes = g_new0(GtkRequestedSize, n_groups);

	/* Get each child's size; set the width of each group
	 * to the maximum size of each child in that group */
	unsigned count = 0;
	GList *iter;
	for(iter = priv->children; iter; iter = g_list_next(iter)) {
		if(!gtk_widget_get_visible(iter->data))
			continue;

		int child_minimal, child_natural;
		unsigned group_num;
		if(direction == GTK_ORIENTATION_HORIZONTAL) {
			gtk_widget_get_preferred_width_for_height(iter->data,
				perpendicular_sizes[count / n_groups].minimum_size,
				&child_minimal, &child_natural);
			group_num = count % n_groups;
		} else {
			gtk_widget_get_preferred_height_for_width(iter->data,
				perpendicular_sizes[count % n_groups].minimum_size,
				&child_minimal, &child_natural);
			group_num = count / n_groups;
		}

		sizes[group_num].minimum_size =
			MAX(child_minimal, sizes[group_num].minimum_size);
		sizes[group_num].natural_size =
			MAX(child_natural, sizes[group_num].natural_size);

		count++;
	}

	return sizes;
}

static void
get_size(PSquare *self, GtkOrientation direction, int *minimal, int *natural)
{
	/* Start with the container's border width */
	unsigned border_width =
		gtk_container_get_border_width(GTK_CONTAINER(self));
	*minimal = *natural = border_width * 2;

	/* Find out how many children there are */
	unsigned n_groups = get_n_columns_and_rows(self);
	if(n_groups == 0)
		return;

	/* Find out how much space they want */
	GtkRequestedSize *sizes = get_group_sizes(self, direction, n_groups);

	/* Add the widths and pass that as the container's width */
	unsigned count;
	for(count = 0; count < n_groups; count++) {
		*minimal += sizes[count].minimum_size;
		*natural += sizes[count].natural_size;
	}

	g_free(sizes);
}

/* Distribute the surplus or shortage of space equally between groups */
static void
distribute_extra_space(PSquare *self, GtkRequestedSize *sizes,
	int extra_space, unsigned n_groups)
{
	if(extra_space > 0) {
		extra_space = gtk_distribute_natural_allocation(extra_space,
			n_groups, sizes);
	}

	unsigned count;
	int extra_per_group = extra_space / (int)n_groups;

	for(count = 0; count < n_groups; count++) {
		sizes[count].minimum_size += extra_per_group;
		/* If this results in a negative width, redistribute
		 * pixels from other nonzero-width columns to this one */
		if(sizes[count].minimum_size < 0) {
			unsigned count2;
			for(count2 = (count + 1) % n_groups;
				sizes[count].minimum_size < 0;
				count2++, count2 %= n_groups)
			{
				if(count2 == count || sizes[count2].minimum_size < 0)
					continue;
				sizes[count2].minimum_size--;
				sizes[count].minimum_size++;
			}
		}
	}
}

/* Get the width of the container */
static void
p_square_get_preferred_width(GtkWidget *widget, int *minimal, int *natural)
{
	g_return_if_fail(widget != NULL);
	g_return_if_fail(P_IS_SQUARE(widget));

	get_size(P_SQUARE(widget), GTK_ORIENTATION_HORIZONTAL, minimal, natural);
}

/* Get the height of the container */
static void
p_square_get_preferred_height(GtkWidget *widget, int *minimal, int *natural)
{
	g_return_if_fail(widget != NULL);
	g_return_if_fail(P_IS_SQUARE(widget));

	get_size(P_SQUARE(widget), GTK_ORIENTATION_VERTICAL, minimal, natural);
}

/* Allocate the sizes of the container's children */
static void
p_square_size_allocate(GtkWidget *widget, GtkAllocation *allocation)
{
	g_return_if_fail(widget != NULL || allocation != NULL);
	g_return_if_fail(P_IS_SQUARE(widget));

	PSquarePrivate *priv = P_SQUARE_PRIVATE(widget);

	gtk_widget_set_allocation(widget, allocation);

	/* Calculate the number of columns (and rows) */
	unsigned n_columns, n_rows;
	n_columns = n_rows = get_n_columns_and_rows(P_SQUARE(widget));
	if(n_columns == 0)
		return;

	/* Calculate how much extra space we need */
	unsigned border_width =
		gtk_container_get_border_width(GTK_CONTAINER(widget));
	int extra_width = allocation->width - 2 * border_width;
	int extra_height = allocation->height - 2 * border_width;

	/* Follow the same procedure as in the size request to get
	 * the ideal sizes of each column */
	GtkRequestedSize *widths = get_group_sizes(P_SQUARE(widget),
		GTK_ORIENTATION_HORIZONTAL, n_columns);

	/* Distribute the extra space per column (can be negative) */
	unsigned count;
	for(count = 0; count < n_columns; count++)
		extra_width -= widths[count].minimum_size;
	distribute_extra_space(P_SQUARE(widget), widths, extra_width, n_columns);

	/* Follow the same procedure for height,
	 * now that we know the width */
	GtkRequestedSize *heights = get_group_sizes_for_sizes(P_SQUARE(widget),
		GTK_ORIENTATION_VERTICAL, widths, n_rows);

	/* Distribute the extra space per row (can be negative) */
	for(count = 0; count < n_rows; count++)
		extra_height -= heights[count].minimum_size;
	distribute_extra_space(P_SQUARE(widget), heights, extra_height, n_rows);

	/* Start positioning the items at the container's origin,
	 * less the border width */
	int x = allocation->x + border_width;
	int y = allocation->y + border_width;

	count = 0;
	GList *iter;
	for(iter = priv->children; iter; iter = g_list_next(iter)) {
		if(!gtk_widget_get_visible(iter->data))
			continue;

		/* Give the child its allocation */
		GtkAllocation child_allocation;
		child_allocation.x = x;
		child_allocation.y = y;
		child_allocation.width = widths[count % n_columns].minimum_size;
		child_allocation.height = heights[count / n_columns].minimum_size;
		gtk_widget_size_allocate(iter->data, &child_allocation);

		/* Advance the x coordinate */
		x += child_allocation.width;
		count++;
		/* If we've moved to the next row, return the x coordinate
		 * to the left, and advance the y coordinate */
		if(count % n_columns == 0) {
			x = allocation->x + border_width;
			y += child_allocation.height;
		}
	}

	g_free(widths);
	g_free(heights);
}

/* Return the type of children this container accepts */
static GType
p_square_child_type(GtkContainer *container)
{
	return GTK_TYPE_WIDGET;
}

/* Add a child to the container */
static void
p_square_add(GtkContainer *container, GtkWidget *widget)
{
	g_return_if_fail(container || P_IS_SQUARE(container));
	g_return_if_fail(widget || GTK_IS_WIDGET(widget));
	g_return_if_fail(gtk_widget_get_parent(widget) == NULL);

	PSquarePrivate *priv = P_SQUARE_PRIVATE(container);

	/* Add the child to our list of children.
	 * All the real work is done in gtk_widget_set_parent(). */
	priv->children = g_list_append(priv->children, widget);
	gtk_widget_set_parent(widget, GTK_WIDGET(container));

	/* Queue redraw */
	if(gtk_widget_get_visible(widget))
		gtk_widget_queue_resize(GTK_WIDGET(container));
}

/* Remove a child from the container */
static void
p_square_remove(GtkContainer *container, GtkWidget *widget)
{
	g_return_if_fail(container || P_IS_SQUARE(container));
	g_return_if_fail(widget || GTK_IS_WIDGET(widget));

	PSquarePrivate *priv = P_SQUARE_PRIVATE(container);

	/* Remove the child from our list of children.
	 * Again, all the real work is done in gtk_widget_unparent(). */
	GList *link = g_list_find(priv->children, widget);
	if(link) {
		gboolean was_visible = gtk_widget_get_visible(widget);
		gtk_widget_unparent(widget);

		priv->children = g_list_delete_link(priv->children, link);

		/* Queue redraw */
		if(was_visible)
			gtk_widget_queue_resize(GTK_WIDGET(container));
	}
}

/* Call the function for all the container's children. This function
 * ignores the include_internals argument, because there are no
 * "internal" children. */
static void
p_square_forall(GtkContainer *container, gboolean include_internals,
	GtkCallback callback, gpointer callback_data)
{
	printf("FORALL!\n");
	PSquarePrivate *priv = P_SQUARE_PRIVATE(container);
	g_list_foreach(priv->children, (GFunc)callback, callback_data);
}
