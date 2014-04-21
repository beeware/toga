/* GTK - The GIMP Toolkit
 * Copyright (C) 1995-1997 Peter Mattis, Spencer Kimball and Josh MacDonald
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library. If not, see <http://www.gnu.org/licenses/>.
 */

/*
 * Modified by the GTK+ Team and others 1997-2000.  See the AUTHORS
 * file for a list of people on the GTK+ Team.  See the ChangeLog
 * files for a list of changes.  These files are distributed with
 * GTK+ at ftp://ftp.gtk.org/pub/gtk/.
 */

/**
 * SECTION:gtkbox
 * @Short_description: A container box
 * @Title: GtkBox
 * @See_also: #GtkFrame, #GtkGrid, #GtkLayout
 *
 * The GtkBox widget organizes child widgets into a rectangular area.
 *
 * The rectangular area of a GtkBox is organized into either a single row
 * or a single column of child widgets depending upon the orientation.
 * Thus, all children of a GtkBox are allocated one dimension in common,
 * which is the height of a row, or the width of a column.
 *
 * GtkBox uses a notion of packing. Packing refers
 * to adding widgets with reference to a particular position in a
 * #GtkContainer. For a GtkBox, there are two reference positions: the
 * start and the end of the box.
 * For a vertical #GtkBox, the start is defined as the top of the box and
 * the end is defined as the bottom. For a horizontal #GtkBox the start
 * is defined as the left side and the end is defined as the right side.
 *
 * Use repeated calls to gtk_box_pack_start() to pack widgets into a
 * GtkBox from start to end. Use gtk_box_pack_end() to add widgets from
 * end to start. You may intersperse these calls and add widgets from
 * both ends of the same GtkBox.
 *
 * Because GtkBox is a #GtkContainer, you may also use gtk_container_add()
 * to insert widgets into the box, and they will be packed with the default
 * values for expand and fill child properties. Use gtk_container_remove()
 * to remove widgets from the GtkBox.
 *
 * Use gtk_box_set_homogeneous() to specify whether or not all children
 * of the GtkBox are forced to get the same amount of space.
 *
 * Use gtk_box_set_spacing() to determine how much space will be
 * minimally placed between all children in the GtkBox. Note that
 * spacing is added between the children, while
 * padding added by gtk_box_pack_start() or gtk_box_pack_end() is added
 * on either side of the widget it belongs to.
 *
 * Use gtk_box_reorder_child() to move a GtkBox child to a different
 * place in the box.
 *
 * Use gtk_box_set_child_packing() to reset the expand,
 * fill and padding child properties.
 * Use gtk_box_query_child_packing() to query these fields.
 *
 * Note that a single-row or single-column #GtkGrid provides exactly
 * the same functionality as #GtkBox.
 */

#include "config.h"

#include "gtkbox.h"
#include "gtkboxprivate.h"
#include "gtkintl.h"
#include "gtkorientable.h"
#include "gtkorientableprivate.h"
#include "gtkprivate.h"
#include "gtktypebuiltins.h"
#include "gtksizerequest.h"
#include "gtkwidgetpath.h"
#include "gtkwidgetprivate.h"
#include "a11y/gtkcontaineraccessible.h"


enum {
  PROP_0,
  PROP_ORIENTATION,
  PROP_SPACING,
  PROP_HOMOGENEOUS,
  PROP_BASELINE_POSITION
};

enum {
  CHILD_PROP_0,
  CHILD_PROP_EXPAND,
  CHILD_PROP_FILL,
  CHILD_PROP_PADDING,
  CHILD_PROP_PACK_TYPE,
  CHILD_PROP_POSITION
};

typedef struct _GtkBoxChild        GtkBoxChild;

struct _GtkBoxPrivate
{
  GList          *children;
  GtkBoxChild    *center;

  GtkOrientation  orientation;
  gint16          spacing;

  guint           default_expand : 1;
  guint           homogeneous    : 1;
  guint           spacing_set    : 1;
  guint           baseline_pos   : 2;
};

/*
 * GtkBoxChild:
 * @widget: the child widget, packed into the GtkBox.
 * @padding: the number of extra pixels to put between this child and its
 *  neighbors, set when packed, zero by default.
 * @expand: flag indicates whether extra space should be given to this child.
 *  Any extra space given to the parent GtkBox is divided up among all children
 *  with this attribute set to %TRUE; set when packed, %TRUE by default.
 * @fill: flag indicates whether any extra space given to this child due to its
 *  @expand attribute being set is actually allocated to the child, rather than
 *  being used as padding around the widget; set when packed, %TRUE by default.
 * @pack: one of #GtkPackType indicating whether the child is packed with
 *  reference to the start (top/left) or end (bottom/right) of the GtkBox.
 */
struct _GtkBoxChild
{
  GtkWidget *widget;

  guint16    padding;

  guint      expand : 1;
  guint      fill   : 1;
  guint      pack   : 1;
};

static void gtk_box_size_allocate         (GtkWidget              *widget,
                                           GtkAllocation          *allocation);
static gboolean gtk_box_draw           (GtkWidget        *widget,
                                        cairo_t          *cr);

static void gtk_box_direction_changed  (GtkWidget        *widget,
                                        GtkTextDirection  previous_direction);

static void gtk_box_set_property       (GObject        *object,
                                        guint           prop_id,
                                        const GValue   *value,
                                        GParamSpec     *pspec);
static void gtk_box_get_property       (GObject        *object,
                                        guint           prop_id,
                                        GValue         *value,
                                        GParamSpec     *pspec);
static void gtk_box_add                (GtkContainer   *container,
                                        GtkWidget      *widget);
static void gtk_box_remove             (GtkContainer   *container,
                                        GtkWidget      *widget);
static void gtk_box_forall             (GtkContainer   *container,
                                        gboolean        include_internals,
                                        GtkCallback     callback,
                                        gpointer        callback_data);
static void gtk_box_set_child_property (GtkContainer   *container,
                                        GtkWidget      *child,
                                        guint           property_id,
                                        const GValue   *value,
                                        GParamSpec     *pspec);
static void gtk_box_get_child_property (GtkContainer   *container,
                                        GtkWidget      *child,
                                        guint           property_id,
                                        GValue         *value,
                                        GParamSpec     *pspec);
static GType gtk_box_child_type        (GtkContainer   *container);
static GtkWidgetPath * gtk_box_get_path_for_child
                                       (GtkContainer   *container,
                                        GtkWidget      *child);


static void               gtk_box_get_preferred_width            (GtkWidget           *widget,
                                                                  gint                *minimum_size,
                                                                  gint                *natural_size);
static void               gtk_box_get_preferred_height           (GtkWidget           *widget,
                                                                  gint                *minimum_size,
                                                                  gint                *natural_size);
static void               gtk_box_get_preferred_width_for_height (GtkWidget           *widget,
                                                                  gint                 height,
                                                                  gint                *minimum_width,
                                                                  gint                *natural_width);
static void               gtk_box_get_preferred_height_for_width (GtkWidget           *widget,
                                                                  gint                 width,
                                                                  gint                *minimum_height,
                                                                  gint                *natural_height);
static void  gtk_box_get_preferred_height_and_baseline_for_width (GtkWidget           *widget,
								  gint                 width,
								  gint                *minimum_height,
								  gint                *natural_height,
								  gint                *minimum_baseline,
								  gint                *natural_baseline);

static void               gtk_box_buildable_init                 (GtkBuildableIface  *iface);

G_DEFINE_TYPE_WITH_CODE (GtkBox, gtk_box, GTK_TYPE_CONTAINER,
                         G_ADD_PRIVATE (GtkBox)
                         G_IMPLEMENT_INTERFACE (GTK_TYPE_ORIENTABLE, NULL)
                         G_IMPLEMENT_INTERFACE (GTK_TYPE_BUILDABLE, gtk_box_buildable_init))

static void
gtk_box_class_init (GtkBoxClass *class)
{
  GObjectClass *object_class = G_OBJECT_CLASS (class);
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (class);
  GtkContainerClass *container_class = GTK_CONTAINER_CLASS (class);

  object_class->set_property = gtk_box_set_property;
  object_class->get_property = gtk_box_get_property;

  widget_class->draw                           = gtk_box_draw;
  widget_class->size_allocate                  = gtk_box_size_allocate;
  widget_class->get_preferred_width            = gtk_box_get_preferred_width;
  widget_class->get_preferred_height           = gtk_box_get_preferred_height;
  widget_class->get_preferred_height_for_width = gtk_box_get_preferred_height_for_width;
  widget_class->get_preferred_height_and_baseline_for_width = gtk_box_get_preferred_height_and_baseline_for_width;
  widget_class->get_preferred_width_for_height = gtk_box_get_preferred_width_for_height;
  widget_class->direction_changed              = gtk_box_direction_changed;

  container_class->add = gtk_box_add;
  container_class->remove = gtk_box_remove;
  container_class->forall = gtk_box_forall;
  container_class->child_type = gtk_box_child_type;
  container_class->set_child_property = gtk_box_set_child_property;
  container_class->get_child_property = gtk_box_get_child_property;
  container_class->get_path_for_child = gtk_box_get_path_for_child;
  gtk_container_class_handle_border_width (container_class);

  g_object_class_override_property (object_class,
                                    PROP_ORIENTATION,
                                    "orientation");

  g_object_class_install_property (object_class,
                                   PROP_SPACING,
                                   g_param_spec_int ("spacing",
                                                     P_("Spacing"),
                                                     P_("The amount of space between children"),
                                                     0,
                                                     G_MAXINT,
                                                     0,
                                                     GTK_PARAM_READWRITE));

  g_object_class_install_property (object_class,
                                   PROP_HOMOGENEOUS,
                                   g_param_spec_boolean ("homogeneous",
							 P_("Homogeneous"),
							 P_("Whether the children should all be the same size"),
							 FALSE,
							 GTK_PARAM_READWRITE));

  g_object_class_install_property (object_class,
                                   PROP_BASELINE_POSITION,
                                   g_param_spec_enum ("baseline-position",
                                                     P_("Baseline position"),
                                                     P_("The position of the baseline aligned widgets if extra space is available"),
                                                     GTK_TYPE_BASELINE_POSITION,
                                                     GTK_BASELINE_POSITION_CENTER,
                                                     GTK_PARAM_READWRITE));

  /**
   * GtkBox:expand:
   *
   * Whether the child should receive extra space when the parent grows.
   *
   * Note that the default value for this property is %FALSE for GtkBox,
   * but #GtkHBox, #GtkVBox and other subclasses use the old default
   * of %TRUE.
   *
   * Note that the #GtkWidget:halign, #GtkWidget:valign, #GtkWidget:hexpand
   * and #GtkWidget:vexpand properties are the preferred way to influence
   * child size allocation in containers.
   *
   * In contrast to #GtkWidget:hexpand, the expand child property does
   * not cause the box to expand itself.
   */
  gtk_container_class_install_child_property (container_class,
					      CHILD_PROP_EXPAND,
					      g_param_spec_boolean ("expand",
								    P_("Expand"),
								    P_("Whether the child should receive extra space when the parent grows"),
								    FALSE,
								    GTK_PARAM_READWRITE));

  /**
   * GtkBox:fill:
   *
   * Whether the child should receive extra space when the parent grows.
   *
   * Note that the #GtkWidget:halign, #GtkWidget:valign, #GtkWidget:hexpand
   * and #GtkWidget:vexpand properties are the preferred way to influence
   * child size allocation in containers.
   */
  gtk_container_class_install_child_property (container_class,
					      CHILD_PROP_FILL,
					      g_param_spec_boolean ("fill",
								    P_("Fill"),
								    P_("Whether extra space given to the child should be allocated to the child or used as padding"),
								    TRUE,
								    GTK_PARAM_READWRITE));

  gtk_container_class_install_child_property (container_class,
					      CHILD_PROP_PADDING,
					      g_param_spec_uint ("padding",
								 P_("Padding"),
								 P_("Extra space to put between the child and its neighbors, in pixels"),
								 0, G_MAXINT, 0,
								 GTK_PARAM_READWRITE));
  gtk_container_class_install_child_property (container_class,
					      CHILD_PROP_PACK_TYPE,
					      g_param_spec_enum ("pack-type",
								 P_("Pack type"),
								 P_("A GtkPackType indicating whether the child is packed with reference to the start or end of the parent"),
								 GTK_TYPE_PACK_TYPE, GTK_PACK_START,
								 GTK_PARAM_READWRITE));
  gtk_container_class_install_child_property (container_class,
					      CHILD_PROP_POSITION,
					      g_param_spec_int ("position",
								P_("Position"),
								P_("The index of the child in the parent"),
								-1, G_MAXINT, 0,
								GTK_PARAM_READWRITE));

  gtk_widget_class_set_accessible_role (widget_class, ATK_ROLE_FILLER);
}

static void
gtk_box_init (GtkBox *box)
{
  GtkBoxPrivate *private;

  box->priv = gtk_box_get_instance_private (box);
  private = box->priv;

  gtk_widget_set_has_window (GTK_WIDGET (box), FALSE);
  gtk_widget_set_redraw_on_allocate (GTK_WIDGET (box), FALSE);

  private->orientation = GTK_ORIENTATION_HORIZONTAL;
  private->children = NULL;

  private->default_expand = FALSE;
  private->homogeneous = FALSE;
  private->spacing = 0;
  private->spacing_set = FALSE;
  private->baseline_pos = GTK_BASELINE_POSITION_CENTER;
}

static void
gtk_box_set_property (GObject      *object,
                      guint         prop_id,
                      const GValue *value,
                      GParamSpec   *pspec)
{
  GtkBox *box = GTK_BOX (object);
  GtkBoxPrivate *private = box->priv;

  switch (prop_id)
    {
    case PROP_ORIENTATION:
      private->orientation = g_value_get_enum (value);
      _gtk_orientable_set_style_classes (GTK_ORIENTABLE (box));
      gtk_widget_queue_resize (GTK_WIDGET (box));
      break;
    case PROP_SPACING:
      gtk_box_set_spacing (box, g_value_get_int (value));
      break;
    case PROP_BASELINE_POSITION:
      gtk_box_set_baseline_position (box, g_value_get_enum (value));
      break;
    case PROP_HOMOGENEOUS:
      gtk_box_set_homogeneous (box, g_value_get_boolean (value));
      break;
    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
      break;
    }
}

static void
gtk_box_get_property (GObject    *object,
                      guint       prop_id,
                      GValue     *value,
                      GParamSpec *pspec)
{
  GtkBox *box = GTK_BOX (object);
  GtkBoxPrivate *private = box->priv;

  switch (prop_id)
    {
    case PROP_ORIENTATION:
      g_value_set_enum (value, private->orientation);
      break;
    case PROP_SPACING:
      g_value_set_int (value, private->spacing);
      break;
    case PROP_BASELINE_POSITION:
      g_value_set_enum (value, private->baseline_pos);
      break;
    case PROP_HOMOGENEOUS:
      g_value_set_boolean (value, private->homogeneous);
      break;
    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
      break;
    }
}

static gboolean
gtk_box_draw (GtkWidget *widget,
              cairo_t   *cr)
{
  GtkStyleContext *context;
  GtkAllocation alloc;

  context = gtk_widget_get_style_context (widget);
  gtk_widget_get_allocation (widget, &alloc);

  gtk_render_background (context, cr, 0, 0, alloc.width, alloc.height);
  gtk_render_frame (context, cr, 0, 0, alloc.width, alloc.height);

  return GTK_WIDGET_CLASS (gtk_box_parent_class)->draw (widget, cr);
}

static void
count_expand_children (GtkBox *box,
                       gint *visible_children,
                       gint *expand_children)
{
  GtkBoxPrivate  *private = box->priv;
  GList       *children;
  GtkBoxChild *child;

  *visible_children = *expand_children = 0;

  for (children = private->children; children; children = children->next)
    {
      child = children->data;

      if (gtk_widget_get_visible (child->widget))
	{
	  *visible_children += 1;
	  if (child->expand || gtk_widget_compute_expand (child->widget, private->orientation))
	    *expand_children += 1;
	}
    }
}

static void
gtk_box_size_allocate_no_center (GtkWidget     *widget,
                                 GtkAllocation *allocation)
{
  GtkBox *box = GTK_BOX (widget);
  GtkBoxPrivate *private = box->priv;
  GtkBoxChild *child;
  GList *children;
  gint nvis_children;
  gint nexpand_children;

  GtkTextDirection direction;
  GtkAllocation child_allocation;
  GtkRequestedSize *sizes;
  gint child_minimum_baseline, child_natural_baseline;
  gint minimum_above, natural_above;
  gint minimum_below, natural_below;
  gboolean have_baseline;
  gint baseline;

  GtkPackType packing;

  gint size;
  gint extra;
  gint n_extra_widgets = 0; /* Number of widgets that receive 1 extra px */
  gint x = 0, y = 0, i;
  gint child_size;


  gtk_widget_set_allocation (widget, allocation);

  count_expand_children (box, &nvis_children, &nexpand_children);

  /* If there is no visible child, simply return. */
  if (nvis_children <= 0)
    return;

  direction = gtk_widget_get_direction (widget);
  sizes = g_newa (GtkRequestedSize, nvis_children);

  if (private->orientation == GTK_ORIENTATION_HORIZONTAL)
    size = allocation->width - (nvis_children - 1) * private->spacing;
  else
    size = allocation->height - (nvis_children - 1) * private->spacing;

  have_baseline = FALSE;
  minimum_above = natural_above = 0;
  minimum_below = natural_below = 0;

  /* Retrieve desired size for visible children. */
  for (i = 0, children = private->children; children; children = children->next)
    {
      child = children->data;

      if (!gtk_widget_get_visible (child->widget))
	continue;

      if (private->orientation == GTK_ORIENTATION_HORIZONTAL)
	gtk_widget_get_preferred_width_for_height (child->widget,
                                                   allocation->height,
                                                   &sizes[i].minimum_size,
                                                   &sizes[i].natural_size);
      else
	gtk_widget_get_preferred_height_and_baseline_for_width (child->widget,
								allocation->width,
								&sizes[i].minimum_size,
								&sizes[i].natural_size,
								NULL, NULL);

      /* Assert the api is working properly */
      if (sizes[i].minimum_size < 0)
	g_error ("GtkBox child %s minimum %s: %d < 0 for %s %d",
		 gtk_widget_get_name (GTK_WIDGET (child->widget)),
		 (private->orientation == GTK_ORIENTATION_HORIZONTAL) ? "width" : "height",
		 sizes[i].minimum_size,
		 (private->orientation == GTK_ORIENTATION_HORIZONTAL) ? "height" : "width",
		 (private->orientation == GTK_ORIENTATION_HORIZONTAL) ? allocation->height : allocation->width);

      if (sizes[i].natural_size < sizes[i].minimum_size)
	g_error ("GtkBox child %s natural %s: %d < minimum %d for %s %d",
		 gtk_widget_get_name (GTK_WIDGET (child->widget)),
		 (private->orientation == GTK_ORIENTATION_HORIZONTAL) ? "width" : "height",
		 sizes[i].natural_size,
		 sizes[i].minimum_size,
		 (private->orientation == GTK_ORIENTATION_HORIZONTAL) ? "height" : "width",
		 (private->orientation == GTK_ORIENTATION_HORIZONTAL) ? allocation->height : allocation->width);

      size -= sizes[i].minimum_size;
      size -= child->padding * 2;

      sizes[i].data = child;

      i++;
    }

  if (private->homogeneous)
    {
      /* If were homogenous we still need to run the above loop to get the
       * minimum sizes for children that are not going to fill
       */
      if (private->orientation == GTK_ORIENTATION_HORIZONTAL)
	size = allocation->width - (nvis_children - 1) * private->spacing;
      else
	size = allocation->height - (nvis_children - 1) * private->spacing;

      extra = size / nvis_children;
      n_extra_widgets = size % nvis_children;
    }
  else
    {
      /* Bring children up to size first */
      size = gtk_distribute_natural_allocation (MAX (0, size), nvis_children, sizes);

      /* Calculate space which hasn't distributed yet,
       * and is available for expanding children.
       */
      if (nexpand_children > 0)
	{
	  extra = size / nexpand_children;
	  n_extra_widgets = size % nexpand_children;
	}
      else
	extra = 0;
    }

  /* Allocate child sizes. */
  for (packing = GTK_PACK_START; packing <= GTK_PACK_END; ++packing)
    {
      for (i = 0, children = private->children;
	   children;
	   children = children->next)
	{
	  child = children->data;

	  /* If widget is not visible, skip it. */
	  if (!gtk_widget_get_visible (child->widget))
	    continue;

	  /* If widget is packed differently skip it, but still increment i,
	   * since widget is visible and will be handled in next loop iteration.
	   */
	  if (child->pack != packing)
	    {
	      i++;
	      continue;
	    }

	  /* Assign the child's size. */
	  if (private->homogeneous)
	    {
	      child_size = extra;

	      if (n_extra_widgets > 0)
		{
		  child_size++;
		  n_extra_widgets--;
		}
	    }
	  else
	    {
	      child_size = sizes[i].minimum_size + child->padding * 2;

	      if (child->expand || gtk_widget_compute_expand (child->widget, private->orientation))
		{
		  child_size += extra;

		  if (n_extra_widgets > 0)
		    {
		      child_size++;
		      n_extra_widgets--;
		    }
		}
	    }

	  sizes[i].natural_size = child_size;

	  if (private->orientation == GTK_ORIENTATION_HORIZONTAL &&
	      gtk_widget_get_valign_with_baseline (child->widget) == GTK_ALIGN_BASELINE)
	    {
	      int child_allocation_width;
	      int child_minimum_height, child_natural_height;

	      if (child->fill)
		child_allocation_width = MAX (1, child_size - child->padding * 2);
	      else
		child_allocation_width = sizes[i].minimum_size;

	      child_minimum_baseline = -1;
	      child_natural_baseline = -1;
	      gtk_widget_get_preferred_height_and_baseline_for_width (child->widget,
								      child_allocation_width,
								      &child_minimum_height, &child_natural_height,
								      &child_minimum_baseline, &child_natural_baseline);

	      if (child_minimum_baseline >= 0)
		{
		  have_baseline = TRUE;
		  minimum_below = MAX (minimum_below, child_minimum_height - child_minimum_baseline);
		  natural_below = MAX (natural_below, child_natural_height - child_natural_baseline);
		  minimum_above = MAX (minimum_above, child_minimum_baseline);
		  natural_above = MAX (natural_above, child_natural_baseline);
		}
	    }

	  i++;
	}
    }

  baseline = gtk_widget_get_allocated_baseline (widget);
  if (baseline == -1 && have_baseline)
    {
      gint height = MAX (1, allocation->height);

      /* TODO: This is purely based on the minimum baseline, when things fit we should
	 use the natural one? */

      switch (private->baseline_pos)
	{
	case GTK_BASELINE_POSITION_TOP:
	  baseline = minimum_above;
	  break;
	case GTK_BASELINE_POSITION_CENTER:
	  baseline = minimum_above + (height - (minimum_above + minimum_below)) / 2;
	  break;
	case GTK_BASELINE_POSITION_BOTTOM:
	  baseline = height - minimum_below;
	  break;
	}
    }

  /* Allocate child positions. */
  for (packing = GTK_PACK_START; packing <= GTK_PACK_END; ++packing)
    {
      if (private->orientation == GTK_ORIENTATION_HORIZONTAL)
	{
	  child_allocation.y = allocation->y;
	  child_allocation.height = MAX (1, allocation->height);
	  if (packing == GTK_PACK_START)
	    x = allocation->x;
	  else
	    x = allocation->x + allocation->width;
	}
      else
	{
	  child_allocation.x = allocation->x;
	  child_allocation.width = MAX (1, allocation->width);
	  if (packing == GTK_PACK_START)
	    y = allocation->y;
	  else
	    y = allocation->y + allocation->height;
	}

      for (i = 0, children = private->children;
	   children;
	   children = children->next)
	{
	  child = children->data;

	  /* If widget is not visible, skip it. */
	  if (!gtk_widget_get_visible (child->widget))
	    continue;

	  /* If widget is packed differently skip it, but still increment i,
	   * since widget is visible and will be handled in next loop iteration.
	   */
	  if (child->pack != packing)
	    {
	      i++;
	      continue;
	    }

	  child_size = sizes[i].natural_size;

	  /* Assign the child's position. */
	  if (private->orientation == GTK_ORIENTATION_HORIZONTAL)
	    {
	      if (child->fill)
		{
		  child_allocation.width = MAX (1, child_size - child->padding * 2);
		  child_allocation.x = x + child->padding;
		}
	      else
		{
		  child_allocation.width = sizes[i].minimum_size;
		  child_allocation.x = x + (child_size - child_allocation.width) / 2;
		}

	      if (packing == GTK_PACK_START)
		{
		  x += child_size + private->spacing;
		}
	      else
		{
		  x -= child_size + private->spacing;

		  child_allocation.x -= child_size;
		}

	      if (direction == GTK_TEXT_DIR_RTL)
		child_allocation.x = allocation->x + allocation->width - (child_allocation.x - allocation->x) - child_allocation.width;

	    }
	  else /* (private->orientation == GTK_ORIENTATION_VERTICAL) */
	    {
	      if (child->fill)
		{
		  child_allocation.height = MAX (1, child_size - child->padding * 2);
		  child_allocation.y = y + child->padding;
		}
	      else
		{
		  child_allocation.height = sizes[i].minimum_size;
		  child_allocation.y = y + (child_size - child_allocation.height) / 2;
		}

	      if (packing == GTK_PACK_START)
		{
		  y += child_size + private->spacing;
		}
	      else
		{
		  y -= child_size + private->spacing;

		  child_allocation.y -= child_size;
		}
	    }
	  gtk_widget_size_allocate_with_baseline (child->widget, &child_allocation, baseline);

	  i++;
	}
    }
}

static void
gtk_box_size_allocate_with_center (GtkWidget     *widget,
                                   GtkAllocation *allocation)
{
  GtkBox *box = GTK_BOX (widget);
  GtkBoxPrivate *priv = box->priv;
  GtkBoxChild *child;
  GList *children;
  gint nvis[2];
  gint nexp[2];
  GtkTextDirection direction;
  GtkAllocation child_allocation;
  GtkRequestedSize *sizes[2];
  GtkRequestedSize center_req;
  gint child_minimum_baseline, child_natural_baseline;
  gint minimum_above, natural_above;
  gint minimum_below, natural_below;
  gboolean have_baseline;
  gint baseline;
  gint idx[2];
  gint center_pos;
  gint center_size;
  gint box_size;
  gint side[2];
  GtkPackType packing;
  gint min_size[2];
  gint nat_size[2];
  gint extra[2];
  gint n_extra_widgets[2];
  gint x = 0, y = 0, i;
  gint child_size;

  gtk_widget_set_allocation (widget, allocation);

  nvis[0] = nvis[1] = 0;
  nexp[0] = nexp[1] = 0;
  for (children = priv->children; children; children = children->next)
    {
      child = children->data;

      if (child != priv->center &&
          gtk_widget_get_visible (child->widget))
        {
          nvis[child->pack] += 1;
          if (child->expand || gtk_widget_compute_expand (child->widget, priv->orientation))
            nexp[child->pack] += 1;
        }
    }

  direction = gtk_widget_get_direction (widget);
  sizes[0] = g_newa (GtkRequestedSize, nvis[0]);
  sizes[1] = g_newa (GtkRequestedSize, nvis[1]);

  if (priv->orientation == GTK_ORIENTATION_HORIZONTAL)
    box_size = allocation->width;
  else
    box_size = allocation->height;

  have_baseline = FALSE;
  minimum_above = natural_above = 0;
  minimum_below = natural_below = 0;

  min_size[0] = nat_size[0] = nvis[0] * priv->spacing;
  min_size[1] = nat_size[1] = nvis[1] * priv->spacing;

  /* Retrieve desired size for visible children. */
  idx[0] = idx[1] = 0;
  for (children = priv->children; children; children = children->next)
    {
      GtkRequestedSize *req;

      child = children->data;

      if (!gtk_widget_get_visible (child->widget))
	continue;

      if (child == priv->center)
        req = &center_req;
      else
        req = &(sizes[child->pack][idx[child->pack]]);

      if (priv->orientation == GTK_ORIENTATION_HORIZONTAL)
        gtk_widget_get_preferred_width_for_height (child->widget,
                                                   allocation->height,
                                                   &req->minimum_size,
                                                   &req->natural_size);
      else
        gtk_widget_get_preferred_height_and_baseline_for_width (child->widget,
                                                                allocation->width,
                                                                &req->minimum_size,
                                                                &req->natural_size,
                                                                NULL, NULL);

      if (child != priv->center)
        {
          min_size[child->pack] += req->minimum_size + 2 * child->padding;
          nat_size[child->pack] += req->natural_size + 2 * child->padding;

          idx[child->pack] += 1;
        }

      req->data = child;
    }

  /* Determine size of center */
  if (priv->center->expand)
    center_size = MAX (box_size - 2 * MAX (nat_size[0], nat_size[1]), center_req.minimum_size);
  else
    center_size = MAX (MIN (center_req.natural_size, box_size - min_size[0] - min_size[1]), center_req.minimum_size);

  if (priv->homogeneous)
    {
      extra[0] = ((box_size - center_size) / 2 - nvis[0] * priv->spacing) / nvis[0];
      extra[1] = ((box_size - center_size) / 2 - nvis[1] * priv->spacing) / nvis[1];
      extra[0] = MIN (extra[0], extra[1]);
      n_extra_widgets[0] = 0;
    }
  else
    {
      for (packing = GTK_PACK_START; packing <= GTK_PACK_END; packing++)
        {
          gint s;
          /* Distribute the remainder naturally on each side */
          s = MIN ((box_size - center_size) / 2 - min_size[packing], box_size - center_size - min_size[0] - min_size[1]);
          s = gtk_distribute_natural_allocation (MAX (0, s), nvis[packing], sizes[packing]);

          /* Calculate space which hasn't distributed yet,
           * and is available for expanding children.
           */
          if (nexp[packing] > 0)
            {
              extra[packing] = s / nexp[packing];
              n_extra_widgets[packing] = s % nexp[packing];
            }
           else
	     extra[packing] = 0;
        }
    }

  /* Allocate child sizes. */
  for (packing = GTK_PACK_START; packing <= GTK_PACK_END; ++packing)
    {
      for (i = 0, children = priv->children; children; children = children->next)
        {
          child = children->data;

          /* If widget is not visible, skip it. */
          if (!gtk_widget_get_visible (child->widget))
            continue;

          /* Skip the center widget */
          if (child == priv->center)
            continue;

          /* If widget is packed differently, skip it. */
          if (child->pack != packing)
            continue;

          /* Assign the child's size. */
          if (priv->homogeneous)
            {
              child_size = extra[0];

              if (n_extra_widgets[0] > 0)
                {
                  child_size++;
                  n_extra_widgets[0]--;
                }
            }
          else
            {
              child_size = sizes[packing][i].minimum_size + child->padding * 2;

              if (child->expand || gtk_widget_compute_expand (child->widget, priv->orientation))
                {
                  child_size += extra[packing];

                  if (n_extra_widgets[packing] > 0)
                    {
                      child_size++;
                      n_extra_widgets[packing]--;
                    }
                }
            }

          sizes[packing][i].natural_size = child_size;

          if (priv->orientation == GTK_ORIENTATION_HORIZONTAL &&
              gtk_widget_get_valign_with_baseline (child->widget) == GTK_ALIGN_BASELINE)
            {
              gint child_allocation_width;
	      gint child_minimum_height, child_natural_height;

              if (child->fill)
                child_allocation_width = MAX (1, child_size - child->padding * 2);
              else
                child_allocation_width = sizes[packing][i].minimum_size;

              child_minimum_baseline = -1;
              child_natural_baseline = -1;
              gtk_widget_get_preferred_height_and_baseline_for_width (child->widget,
                                                                      child_allocation_width,
                                                                      &child_minimum_height, &child_natural_height,
                                                                      &child_minimum_baseline, &child_natural_baseline);

              if (child_minimum_baseline >= 0)
                {
                  have_baseline = TRUE;
                  minimum_below = MAX (minimum_below, child_minimum_height - child_minimum_baseline);
                  natural_below = MAX (natural_below, child_natural_height - child_natural_baseline);
                  minimum_above = MAX (minimum_above, child_minimum_baseline);
                  natural_above = MAX (natural_above, child_natural_baseline);
                }
            }

          i++;
        }
    }

  baseline = gtk_widget_get_allocated_baseline (widget);
  if (baseline == -1 && have_baseline)
    {
      gint height = MAX (1, allocation->height);

     /* TODO: This is purely based on the minimum baseline, when things fit we should
      * use the natural one?
      */
      switch (priv->baseline_pos)
        {
        case GTK_BASELINE_POSITION_TOP:
          baseline = minimum_above;
          break;
        case GTK_BASELINE_POSITION_CENTER:
          baseline = minimum_above + (height - (minimum_above + minimum_below)) / 2;
          break;
        case GTK_BASELINE_POSITION_BOTTOM:
          baseline = height - minimum_below;
          break;
        }
    }

  /* Allocate child positions. */
  for (packing = GTK_PACK_START; packing <= GTK_PACK_END; ++packing)
    {
      if (priv->orientation == GTK_ORIENTATION_HORIZONTAL)
        {
          child_allocation.y = allocation->y;
          child_allocation.height = MAX (1, allocation->height);
          if (packing == GTK_PACK_START)
            x = allocation->x;
          else
            x = allocation->x + allocation->width;
        }
      else
        {
          child_allocation.x = allocation->x;
          child_allocation.width = MAX (1, allocation->width);
          if (packing == GTK_PACK_START)
            y = allocation->y;
          else
            y = allocation->y + allocation->height;
        }

      for (i = 0, children = priv->children; children; children = children->next)
        {
          child = children->data;

          /* If widget is not visible, skip it. */
          if (!gtk_widget_get_visible (child->widget))
            continue;

          /* Skip the center widget */
          if (child == priv->center)
            continue;

          /* If widget is packed differently, skip it. */
          if (child->pack != packing)
            continue;

          child_size = sizes[packing][i].natural_size;

          /* Assign the child's position. */
          if (priv->orientation == GTK_ORIENTATION_HORIZONTAL)
            {
              if (child->fill)
                {
                  child_allocation.width = MAX (1, child_size - child->padding * 2);
                  child_allocation.x = x + child->padding;
                }
              else
                {
                  child_allocation.width = sizes[packing][i].minimum_size;
                  child_allocation.x = x + (child_size - child_allocation.width) / 2;
                }

              if (packing == GTK_PACK_START)
                {
                  x += child_size + priv->spacing;
                }
              else
                {
                  x -= child_size + priv->spacing;
                  child_allocation.x -= child_size;
                }

              if (direction == GTK_TEXT_DIR_RTL)
                child_allocation.x = allocation->x + allocation->width - (child_allocation.x - allocation->x) - child_allocation.width;

            }
          else /* (private->orientation == GTK_ORIENTATION_VERTICAL) */
            {
              if (child->fill)
                {
                  child_allocation.height = MAX (1, child_size - child->padding * 2);
                  child_allocation.y = y + child->padding;
                }
              else
                {
                  child_allocation.height = sizes[packing][i].minimum_size;
                  child_allocation.y = y + (child_size - child_allocation.height) / 2;
                }

              if (packing == GTK_PACK_START)
                {
                  y += child_size + priv->spacing;
                }
              else
                {
                  y -= child_size + priv->spacing;
                  child_allocation.y -= child_size;
                }
            }
          gtk_widget_size_allocate_with_baseline (child->widget, &child_allocation, baseline);

          i++;
        }

      if (priv->orientation == GTK_ORIENTATION_HORIZONTAL)
        side[packing] = x;
      else
        side[packing] = y;
    }

  /* Allocate the center widget */
  if (priv->orientation == GTK_ORIENTATION_HORIZONTAL)
    center_pos = allocation->x + (box_size - center_size) / 2;
  else
    center_pos = allocation->y + (box_size - center_size) / 2;

  if (center_pos < side[GTK_PACK_START])
    center_pos = side[GTK_PACK_START];
  else if (center_pos + center_size > side[GTK_PACK_END])
    center_pos = side[GTK_PACK_END] - center_size;

  if (priv->orientation == GTK_ORIENTATION_HORIZONTAL)
    {
      child_allocation.x = center_pos;
      child_allocation.width = center_size;
    }
  else
    {
      child_allocation.y = center_pos;
      child_allocation.height = center_size;
    }
  gtk_widget_size_allocate_with_baseline (priv->center->widget, &child_allocation, baseline);
}

static void
gtk_box_size_allocate (GtkWidget     *widget,
                       GtkAllocation *allocation)
{
  GtkBox *box = GTK_BOX (widget);

  if (box->priv->center &&
      gtk_widget_get_visible (box->priv->center->widget))
    gtk_box_size_allocate_with_center (widget, allocation);
  else
    gtk_box_size_allocate_no_center (widget, allocation);
}

static GType
gtk_box_child_type (GtkContainer   *container)
{
  return GTK_TYPE_WIDGET;
}

static void
gtk_box_set_child_property (GtkContainer *container,
                            GtkWidget    *child,
                            guint         property_id,
                            const GValue *value,
                            GParamSpec   *pspec)
{
  gboolean expand = 0;
  gboolean fill = 0;
  guint padding = 0;
  GtkPackType pack_type = 0;

  if (property_id != CHILD_PROP_POSITION)
    gtk_box_query_child_packing (GTK_BOX (container),
				 child,
				 &expand,
				 &fill,
				 &padding,
				 &pack_type);
  switch (property_id)
    {
    case CHILD_PROP_EXPAND:
      gtk_box_set_child_packing (GTK_BOX (container),
				 child,
				 g_value_get_boolean (value),
				 fill,
				 padding,
				 pack_type);
      break;
    case CHILD_PROP_FILL:
      gtk_box_set_child_packing (GTK_BOX (container),
				 child,
				 expand,
				 g_value_get_boolean (value),
				 padding,
				 pack_type);
      break;
    case CHILD_PROP_PADDING:
      gtk_box_set_child_packing (GTK_BOX (container),
				 child,
				 expand,
				 fill,
				 g_value_get_uint (value),
				 pack_type);
      break;
    case CHILD_PROP_PACK_TYPE:
      gtk_box_set_child_packing (GTK_BOX (container),
				 child,
				 expand,
				 fill,
				 padding,
				 g_value_get_enum (value));
      break;
    case CHILD_PROP_POSITION:
      gtk_box_reorder_child (GTK_BOX (container),
			     child,
			     g_value_get_int (value));
      break;
    default:
      GTK_CONTAINER_WARN_INVALID_CHILD_PROPERTY_ID (container, property_id, pspec);
      break;
    }
}

static void
gtk_box_get_child_property (GtkContainer *container,
			    GtkWidget    *child,
			    guint         property_id,
			    GValue       *value,
			    GParamSpec   *pspec)
{
  gboolean expand = FALSE;
  gboolean fill = FALSE;
  guint padding = 0;
  GtkPackType pack_type = 0;
  GList *list;

  if (property_id != CHILD_PROP_POSITION)
    gtk_box_query_child_packing (GTK_BOX (container),
				 child,
				 &expand,
				 &fill,
				 &padding,
				 &pack_type);
  switch (property_id)
    {
      guint i;
    case CHILD_PROP_EXPAND:
      g_value_set_boolean (value, expand);
      break;
    case CHILD_PROP_FILL:
      g_value_set_boolean (value, fill);
      break;
    case CHILD_PROP_PADDING:
      g_value_set_uint (value, padding);
      break;
    case CHILD_PROP_PACK_TYPE:
      g_value_set_enum (value, pack_type);
      break;
    case CHILD_PROP_POSITION:
      i = 0;
      for (list = GTK_BOX (container)->priv->children; list; list = list->next)
	{
	  GtkBoxChild *child_entry;

	  child_entry = list->data;
	  if (child_entry->widget == child)
	    break;
	  i++;
	}
      g_value_set_int (value, list ? i : -1);
      break;
    default:
      GTK_CONTAINER_WARN_INVALID_CHILD_PROPERTY_ID (container, property_id, pspec);
      break;
    }
}

typedef struct _CountingData CountingData;
struct _CountingData {
  GtkWidget *widget;
  gboolean found;
  guint before;
  guint after;
};

static void
count_widget_position (GtkWidget *widget,
                       gpointer   data)
{
  CountingData *count = data;

  if (!gtk_widget_get_visible (widget))
    return;

  if (count->widget == widget)
    count->found = TRUE;
  else if (count->found)
    count->after++;
  else
    count->before++;
}

static gint
gtk_box_get_visible_position (GtkBox    *box,
                              GtkWidget *child)
{
  CountingData count = { child, FALSE, 0, 0 };

  /* foreach iterates in visible order */
  gtk_container_foreach (GTK_CONTAINER (box),
                         count_widget_position,
                         &count);

  /* the child wasn't found, it's likely an internal child of some
   * subclass, return -1 to indicate that there is no sibling relation
   * to the regular box children
   */
  if (!count.found)
    return -1;

  if (box->priv->orientation == GTK_ORIENTATION_HORIZONTAL &&
      gtk_widget_get_direction (GTK_WIDGET (box)) == GTK_TEXT_DIR_RTL)
    return count.after;
  else
    return count.before;
}

static GtkWidgetPath *
gtk_box_get_path_for_child (GtkContainer *container,
                            GtkWidget    *child)
{
  GtkWidgetPath *path, *sibling_path;
  GtkBox *box;
  GtkBoxPrivate *private;
  GList *list, *children;

  box = GTK_BOX (container);
  private = box->priv;

  path = _gtk_widget_create_path (GTK_WIDGET (container));

  if (gtk_widget_get_visible (child))
    {
      gint position;

      sibling_path = gtk_widget_path_new ();

      /* get_children works in visible order */
      children = gtk_container_get_children (container);
      if (private->orientation == GTK_ORIENTATION_HORIZONTAL &&
          gtk_widget_get_direction (GTK_WIDGET (box)) == GTK_TEXT_DIR_RTL)
        children = g_list_reverse (children);

      for (list = children; list; list = list->next)
        {
          if (!gtk_widget_get_visible (list->data))
            continue;

          gtk_widget_path_append_for_widget (sibling_path, list->data);
        }

      g_list_free (children);

      position = gtk_box_get_visible_position (box, child);

      if (position >= 0)
        gtk_widget_path_append_with_siblings (path, sibling_path, position);
      else
        gtk_widget_path_append_for_widget (path, child);

      gtk_widget_path_unref (sibling_path);
    }
  else
    gtk_widget_path_append_for_widget (path, child);

  return path;
}

static void
gtk_box_buildable_add_child (GtkBuildable *buildable,
                             GtkBuilder   *builder,
                             GObject      *child,
                             const gchar  *type)
{
  if (type && strcmp (type, "center") == 0)
    gtk_box_set_center_widget (GTK_BOX (buildable), GTK_WIDGET (child));
  else if (!type)
    gtk_container_add (GTK_CONTAINER (buildable), GTK_WIDGET (child));
  else
    GTK_BUILDER_WARN_INVALID_CHILD_TYPE (GTK_BOX (buildable), type);
}

static void
gtk_box_buildable_init (GtkBuildableIface *iface)
{
  iface->add_child = gtk_box_buildable_add_child;
}

static void
gtk_box_invalidate_order_foreach (GtkWidget *widget)
{
  _gtk_widget_invalidate_style_context (widget, GTK_CSS_CHANGE_POSITION | GTK_CSS_CHANGE_SIBLING_POSITION);
}

static void
gtk_box_invalidate_order (GtkBox *box)
{
  gtk_container_foreach (GTK_CONTAINER (box),
                         (GtkCallback) gtk_box_invalidate_order_foreach,
                         NULL);
}

static void
gtk_box_direction_changed (GtkWidget        *widget,
                           GtkTextDirection  previous_direction)
{
  gtk_box_invalidate_order (GTK_BOX (widget));
}

static void
box_child_visibility_notify_cb (GObject *obj,
                                GParamSpec *pspec,
                                gpointer user_data)
{
  GtkBox *box = user_data;

  gtk_box_invalidate_order (box);
}

static GtkBoxChild *
gtk_box_pack (GtkBox      *box,
              GtkWidget   *child,
              gboolean     expand,
              gboolean     fill,
              guint        padding,
              GtkPackType  pack_type)
{
  GtkBoxPrivate *private = box->priv;
  GtkBoxChild *child_info;

  g_return_val_if_fail (GTK_IS_BOX (box), NULL);
  g_return_val_if_fail (GTK_IS_WIDGET (child), NULL);
  g_return_val_if_fail (gtk_widget_get_parent (child) == NULL, NULL);

  child_info = g_new (GtkBoxChild, 1);
  child_info->widget = child;
  child_info->padding = padding;
  child_info->expand = expand ? TRUE : FALSE;
  child_info->fill = fill ? TRUE : FALSE;
  child_info->pack = pack_type;

  private->children = g_list_append (private->children, child_info);

  gtk_widget_freeze_child_notify (child);

  gtk_box_invalidate_order (box);
  gtk_widget_set_parent (child, GTK_WIDGET (box));

  g_signal_connect (child, "notify::visible",
                    G_CALLBACK (box_child_visibility_notify_cb), box);

  gtk_widget_child_notify (child, "expand");
  gtk_widget_child_notify (child, "fill");
  gtk_widget_child_notify (child, "padding");
  gtk_widget_child_notify (child, "pack-type");
  gtk_widget_child_notify (child, "position");
  gtk_widget_thaw_child_notify (child);

  return child_info;
}

static void
gtk_box_get_size (GtkWidget      *widget,
		  GtkOrientation  orientation,
		  gint           *minimum_size,
		  gint           *natural_size,
		  gint           *minimum_baseline,
		  gint           *natural_baseline)
{
  GtkBox *box;
  GtkBoxPrivate *private;
  GList *children;
  gint nvis_children;
  gint minimum, natural;
  gint minimum_above, natural_above;
  gint minimum_below, natural_below;
  gboolean have_baseline;
  gint min_baseline, nat_baseline;
  gint center_min, center_nat;

  box = GTK_BOX (widget);
  private = box->priv;

  have_baseline = FALSE;
  minimum = natural = 0;
  minimum_above = natural_above = 0;
  minimum_below = natural_below = 0;
  min_baseline = nat_baseline = -1;

  nvis_children = 0;

  center_min = center_nat = 0;

  for (children = private->children; children; children = children->next)
    {
      GtkBoxChild *child = children->data;

      if (gtk_widget_get_visible (child->widget))
        {
          gint child_minimum, child_natural;
          gint child_minimum_baseline = -1, child_natural_baseline = -1;

	  if (orientation == GTK_ORIENTATION_HORIZONTAL)
	    gtk_widget_get_preferred_width (child->widget,
                                            &child_minimum, &child_natural);
	  else
	    gtk_widget_get_preferred_height_and_baseline_for_width (child->widget, -1,
								    &child_minimum, &child_natural,
								    &child_minimum_baseline, &child_natural_baseline);

          if (private->orientation == orientation)
	    {
              if (private->homogeneous)
                {
                  if (child == private->center)
                    {
                      center_min = child_minimum + child->padding * 2;
                      center_nat = child_natural + child->padding * 2;
                    }
                  else
                    {
                      gint largest;

                      largest = child_minimum + child->padding * 2;
                      minimum = MAX (minimum, largest);

                      largest = child_natural + child->padding * 2;
                      natural = MAX (natural, largest);
                    }
                }
              else
                {
                  minimum += child_minimum + child->padding * 2;
                  natural += child_natural + child->padding * 2;
                }
	    }
	  else
	    {
	      if (child_minimum_baseline >= 0)
		{
		  have_baseline = TRUE;
		  minimum_below = MAX (minimum_below, child_minimum - child_minimum_baseline);
		  natural_below = MAX (natural_below, child_natural - child_natural_baseline);
		  minimum_above = MAX (minimum_above, child_minimum_baseline);
		  natural_above = MAX (natural_above, child_natural_baseline);
		}
	      else
		{
		  /* The biggest mins and naturals in the opposing orientation */
		  minimum = MAX (minimum, child_minimum);
		  natural = MAX (natural, child_natural);
		}
	    }

          nvis_children += 1;
        }
    }

  if (nvis_children > 0 && private->orientation == orientation)
    {
      if (private->homogeneous)
	{
          if (center_min > 0)
            {
              minimum = minimum * (nvis_children - 1) + center_min;
              natural = natural * (nvis_children - 1) + center_nat;
            }
          else
            {
	      minimum *= nvis_children;
	      natural *= nvis_children;
            }
	}
      minimum += (nvis_children - 1) * private->spacing;
      natural += (nvis_children - 1) * private->spacing;
    }

  minimum = MAX (minimum, minimum_below + minimum_above);
  natural = MAX (natural, natural_below + natural_above);

  if (have_baseline)
    {
      switch (private->baseline_pos)
	{
	case GTK_BASELINE_POSITION_TOP:
	  min_baseline = minimum_above;
	  nat_baseline = natural_above;
	  break;
	case GTK_BASELINE_POSITION_CENTER:
	  min_baseline = minimum_above + (minimum - (minimum_above + minimum_below)) / 2;
	  nat_baseline = natural_above + (natural - (natural_above + natural_below)) / 2;
	  break;
	case GTK_BASELINE_POSITION_BOTTOM:
	  min_baseline = minimum - minimum_below;
	  nat_baseline = natural - natural_below;
	  break;
	}
    }

  if (minimum_size)
    *minimum_size = minimum;

  if (natural_size)
    *natural_size = natural;

  if (minimum_baseline)
    *minimum_baseline = min_baseline;

  if (natural_baseline)
    *natural_baseline = nat_baseline;
}

static void
gtk_box_get_preferred_width (GtkWidget *widget,
                             gint      *minimum_size,
                             gint      *natural_size)
{
  gtk_box_get_size (widget, GTK_ORIENTATION_HORIZONTAL, minimum_size, natural_size, NULL, NULL);
}

static void
gtk_box_get_preferred_height (GtkWidget *widget,
                              gint      *minimum_size,
                              gint      *natural_size)
{
  gtk_box_get_size (widget, GTK_ORIENTATION_VERTICAL, minimum_size, natural_size, NULL, NULL);
}

static void
gtk_box_compute_size_for_opposing_orientation (GtkBox *box,
					       gint    avail_size,
					       gint   *minimum_size,
					       gint   *natural_size,
					       gint   *minimum_baseline,
					       gint   *natural_baseline)
{
  GtkBoxPrivate       *private = box->priv;
  GtkBoxChild      *child;
  GList            *children;
  gint              nvis_children;
  gint              nexpand_children;
  gint              computed_minimum = 0, computed_natural = 0;
  gint              computed_minimum_above = 0, computed_natural_above = 0;
  gint              computed_minimum_below = 0, computed_natural_below = 0;
  gint              computed_minimum_baseline = -1, computed_natural_baseline = -1;
  GtkRequestedSize *sizes;
  GtkPackType       packing;
  gint              size, extra, i;
  gint              child_size, child_minimum, child_natural;
  gint              child_minimum_baseline, child_natural_baseline;
  gint              n_extra_widgets = 0;
  gboolean          have_baseline;

  count_expand_children (box, &nvis_children, &nexpand_children);

  if (nvis_children <= 0)
    return;

  sizes = g_newa (GtkRequestedSize, nvis_children);
  size = avail_size - (nvis_children - 1) * private->spacing;

  /* Retrieve desired size for visible children */
  for (i = 0, children = private->children; children; children = children->next)
    {
      child = children->data;

      if (gtk_widget_get_visible (child->widget))
	{
	  if (private->orientation == GTK_ORIENTATION_HORIZONTAL)
	    gtk_widget_get_preferred_width (child->widget,
                                            &sizes[i].minimum_size,
                                            &sizes[i].natural_size);
	  else
	    gtk_widget_get_preferred_height (child->widget,
                                             &sizes[i].minimum_size,
                                             &sizes[i].natural_size);

	  /* Assert the api is working properly */
	  if (sizes[i].minimum_size < 0)
	    g_error ("GtkBox child %s minimum %s: %d < 0",
		     gtk_widget_get_name (GTK_WIDGET (child->widget)),
		     (private->orientation == GTK_ORIENTATION_HORIZONTAL) ? "width" : "height",
		     sizes[i].minimum_size);

	  if (sizes[i].natural_size < sizes[i].minimum_size)
	    g_error ("GtkBox child %s natural %s: %d < minimum %d",
		     gtk_widget_get_name (GTK_WIDGET (child->widget)),
		     (private->orientation == GTK_ORIENTATION_HORIZONTAL) ? "width" : "height",
		     sizes[i].natural_size,
		     sizes[i].minimum_size);

	  size -= sizes[i].minimum_size;
	  size -= child->padding * 2;

	  sizes[i].data = child;

	  i += 1;
	}
    }

  if (private->homogeneous)
    {
      /* If were homogenous we still need to run the above loop to get the
       * minimum sizes for children that are not going to fill
       */
      size = avail_size - (nvis_children - 1) * private->spacing;
      extra = size / nvis_children;
      n_extra_widgets = size % nvis_children;
    }
  else
    {
      /* Bring children up to size first */
      size = gtk_distribute_natural_allocation (MAX (0, size), nvis_children, sizes);

      /* Calculate space which hasn't distributed yet,
       * and is available for expanding children.
       */
      if (nexpand_children > 0)
	{
	  extra = size / nexpand_children;
	  n_extra_widgets = size % nexpand_children;
	}
      else
	extra = 0;
    }

  have_baseline = FALSE;
  /* Allocate child positions. */
  for (packing = GTK_PACK_START; packing <= GTK_PACK_END; ++packing)
    {
      for (i = 0, children = private->children;
	   children;
	   children = children->next)
	{
	  child = children->data;

	  /* If widget is not visible, skip it. */
	  if (!gtk_widget_get_visible (child->widget))
	    continue;

	  /* If widget is packed differently skip it, but still increment i,
	   * since widget is visible and will be handled in next loop iteration.
	   */
	  if (child->pack != packing)
	    {
	      i++;
	      continue;
	    }

	  if (child->pack == packing)
	    {
	      /* Assign the child's size. */
	      if (private->homogeneous)
		{
		  child_size = extra;

		  if (n_extra_widgets > 0)
		    {
		      child_size++;
		      n_extra_widgets--;
		    }
		}
	      else
		{
		  child_size = sizes[i].minimum_size + child->padding * 2;

		  if (child->expand || gtk_widget_compute_expand (child->widget, private->orientation))
		    {
		      child_size += extra;

		      if (n_extra_widgets > 0)
			{
			  child_size++;
			  n_extra_widgets--;
			}
		    }
		}

	      if (child->fill)
		{
		  child_size = MAX (1, child_size - child->padding * 2);
		}
	      else
		{
		  child_size = sizes[i].minimum_size;
		}


	      child_minimum_baseline = child_natural_baseline = -1;
	      /* Assign the child's position. */
	      if (private->orientation == GTK_ORIENTATION_HORIZONTAL)
		gtk_widget_get_preferred_height_and_baseline_for_width (child->widget, child_size,
									&child_minimum, &child_natural,
									&child_minimum_baseline, &child_natural_baseline);
	      else /* (private->orientation == GTK_ORIENTATION_VERTICAL) */
		gtk_widget_get_preferred_width_for_height (child->widget,
                                                           child_size, &child_minimum, &child_natural);

	      if (child_minimum_baseline >= 0)
		{
		  have_baseline = TRUE;
		  computed_minimum_below = MAX (computed_minimum_below, child_minimum - child_minimum_baseline);
		  computed_natural_below = MAX (computed_natural_below, child_natural - child_natural_baseline);
		  computed_minimum_above = MAX (computed_minimum_above, child_minimum_baseline);
		  computed_natural_above = MAX (computed_natural_above, child_natural_baseline);
		}
	      else
		{
		  computed_minimum = MAX (computed_minimum, child_minimum);
		  computed_natural = MAX (computed_natural, child_natural);
		}
	    }
	  i += 1;
	}
    }

  if (have_baseline)
    {
      computed_minimum = MAX (computed_minimum, computed_minimum_below + computed_minimum_above);
      computed_natural = MAX (computed_natural, computed_natural_below + computed_natural_above);
      switch (private->baseline_pos)
	{
	case GTK_BASELINE_POSITION_TOP:
	  computed_minimum_baseline = computed_minimum_above;
	  computed_natural_baseline = computed_natural_above;
	  break;
	case GTK_BASELINE_POSITION_CENTER:
	  computed_minimum_baseline = computed_minimum_above + MAX((computed_minimum - (computed_minimum_above + computed_minimum_below)) / 2, 0);
	  computed_natural_baseline = computed_natural_above + MAX((computed_natural - (computed_natural_above + computed_natural_below)) / 2, 0);
	  break;
	case GTK_BASELINE_POSITION_BOTTOM:
	  computed_minimum_baseline = computed_minimum - computed_minimum_below;
	  computed_natural_baseline = computed_natural - computed_natural_below;
	  break;
	}
    }

  if (minimum_baseline)
    *minimum_baseline = computed_minimum_baseline;
  if (natural_baseline)
    *natural_baseline = computed_natural_baseline;

  if (minimum_size)
    *minimum_size = computed_minimum;
  if (natural_size)
    *natural_size = MAX (computed_natural, computed_natural_below + computed_natural_above);
}

static void
gtk_box_compute_size_for_orientation (GtkBox *box,
				      gint    avail_size,
				      gint   *minimum_size,
				      gint   *natural_size)
{
  GtkBoxPrivate    *private = box->priv;
  GList         *children;
  gint           nvis_children = 0;
  gint           required_size = 0, required_natural = 0, child_size, child_natural;
  gint           largest_child = 0, largest_natural = 0;

  for (children = private->children; children != NULL;
       children = children->next)
    {
      GtkBoxChild *child = children->data;

      if (gtk_widget_get_visible (child->widget))
        {

          if (private->orientation == GTK_ORIENTATION_HORIZONTAL)
	    gtk_widget_get_preferred_width_for_height (child->widget,
                                                       avail_size, &child_size, &child_natural);
	  else
	    gtk_widget_get_preferred_height_for_width (child->widget,
						       avail_size, &child_size, &child_natural);


	  child_size    += child->padding * 2;
	  child_natural += child->padding * 2;

	  if (child_size > largest_child)
	    largest_child = child_size;

	  if (child_natural > largest_natural)
	    largest_natural = child_natural;

	  required_size    += child_size;
	  required_natural += child_natural;

          nvis_children += 1;
        }
    }

  if (nvis_children > 0)
    {
      if (private->homogeneous)
	{
	  required_size    = largest_child   * nvis_children;
	  required_natural = largest_natural * nvis_children;
	}

      required_size     += (nvis_children - 1) * private->spacing;
      required_natural  += (nvis_children - 1) * private->spacing;
    }

  if (minimum_size)
    *minimum_size = required_size;

  if (natural_size)
    *natural_size = required_natural;
}

static void
gtk_box_get_preferred_width_for_height (GtkWidget *widget,
                                        gint       height,
                                        gint      *minimum_width,
                                        gint      *natural_width)
{
  GtkBox        *box     = GTK_BOX (widget);
  GtkBoxPrivate *private = box->priv;

  if (private->orientation == GTK_ORIENTATION_VERTICAL)
    gtk_box_compute_size_for_opposing_orientation (box, height, minimum_width, natural_width, NULL, NULL);
  else
    gtk_box_compute_size_for_orientation (box, height, minimum_width, natural_width);
}

static void
gtk_box_get_preferred_height_and_baseline_for_width (GtkWidget *widget,
						     gint       width,
						     gint      *minimum_height,
						     gint      *natural_height,
						     gint      *minimum_baseline,
						     gint      *natural_baseline)
{
  GtkBox        *box     = GTK_BOX (widget);
  GtkBoxPrivate *private = box->priv;

  if (width < 0)
    gtk_box_get_size (widget, GTK_ORIENTATION_VERTICAL, minimum_height, natural_height, minimum_baseline, natural_baseline);
  else
    {
      if (private->orientation == GTK_ORIENTATION_HORIZONTAL)
	gtk_box_compute_size_for_opposing_orientation (box, width, minimum_height, natural_height, minimum_baseline, natural_baseline);
      else
	{
	  if (minimum_baseline)
	    *minimum_baseline = -1;
	  if (natural_baseline)
	    *natural_baseline = -1;
	  gtk_box_compute_size_for_orientation (box, width, minimum_height, natural_height);
	}
    }
}

static void
gtk_box_get_preferred_height_for_width (GtkWidget *widget,
                                        gint       width,
                                        gint      *minimum_height,
                                        gint      *natural_height)
{
  gtk_box_get_preferred_height_and_baseline_for_width (widget, width, minimum_height, natural_height, NULL, NULL);
}

/**
 * gtk_box_new:
 * @orientation: the box’s orientation.
 * @spacing: the number of pixels to place by default between children.
 *
 * Creates a new #GtkBox.
 *
 * Returns: a new #GtkBox.
 *
 * Since: 3.0
 **/
GtkWidget*
gtk_box_new (GtkOrientation orientation,
             gint           spacing)
{
  return g_object_new (GTK_TYPE_BOX,
                       "orientation", orientation,
                       "spacing",     spacing,
                       NULL);
}

/**
 * gtk_box_pack_start:
 * @box: a #GtkBox
 * @child: the #GtkWidget to be added to @box
 * @expand: %TRUE if the new child is to be given extra space allocated
 *     to @box. The extra space will be divided evenly between all children
 *     that use this option
 * @fill: %TRUE if space given to @child by the @expand option is
 *     actually allocated to @child, rather than just padding it.  This
 *     parameter has no effect if @expand is set to %FALSE.  A child is
 *     always allocated the full height of a horizontal #GtkBox and the full width
 *     of a vertical #GtkBox. This option affects the other dimension
 * @padding: extra space in pixels to put between this child and its
 *   neighbors, over and above the global amount specified by
 *   #GtkBox:spacing property.  If @child is a widget at one of the
 *   reference ends of @box, then @padding pixels are also put between
 *   @child and the reference edge of @box
 *
 * Adds @child to @box, packed with reference to the start of @box.
 * The @child is packed after any other child packed with reference
 * to the start of @box.
 */
void
gtk_box_pack_start (GtkBox    *box,
		    GtkWidget *child,
		    gboolean   expand,
		    gboolean   fill,
		    guint      padding)
{
  gtk_box_pack (box, child, expand, fill, padding, GTK_PACK_START);
}

/**
 * gtk_box_pack_end:
 * @box: a #GtkBox
 * @child: the #GtkWidget to be added to @box
 * @expand: %TRUE if the new child is to be given extra space allocated
 *   to @box. The extra space will be divided evenly between all children
 *   of @box that use this option
 * @fill: %TRUE if space given to @child by the @expand option is
 *   actually allocated to @child, rather than just padding it.  This
 *   parameter has no effect if @expand is set to %FALSE.  A child is
 *   always allocated the full height of a horizontal #GtkBox and the full width
 *   of a vertical #GtkBox.  This option affects the other dimension
 * @padding: extra space in pixels to put between this child and its
 *   neighbors, over and above the global amount specified by
 *   #GtkBox:spacing property.  If @child is a widget at one of the
 *   reference ends of @box, then @padding pixels are also put between
 *   @child and the reference edge of @box
 *
 * Adds @child to @box, packed with reference to the end of @box.
 * The @child is packed after (away from end of) any other child
 * packed with reference to the end of @box.
 */
void
gtk_box_pack_end (GtkBox    *box,
		  GtkWidget *child,
		  gboolean   expand,
		  gboolean   fill,
		  guint      padding)
{
  gtk_box_pack (box, child, expand, fill, padding, GTK_PACK_END);
}

/**
 * gtk_box_set_homogeneous:
 * @box: a #GtkBox
 * @homogeneous: a boolean value, %TRUE to create equal allotments,
 *   %FALSE for variable allotments
 *
 * Sets the #GtkBox:homogeneous property of @box, controlling
 * whether or not all children of @box are given equal space
 * in the box.
 */
void
gtk_box_set_homogeneous (GtkBox  *box,
			 gboolean homogeneous)
{
  GtkBoxPrivate *private;

  g_return_if_fail (GTK_IS_BOX (box));

  private = box->priv;

  if ((homogeneous ? TRUE : FALSE) != private->homogeneous)
    {
      private->homogeneous = homogeneous ? TRUE : FALSE;
      g_object_notify (G_OBJECT (box), "homogeneous");
      gtk_widget_queue_resize (GTK_WIDGET (box));
    }
}

/**
 * gtk_box_get_homogeneous:
 * @box: a #GtkBox
 *
 * Returns whether the box is homogeneous (all children are the
 * same size). See gtk_box_set_homogeneous().
 *
 * Returns: %TRUE if the box is homogeneous.
 **/
gboolean
gtk_box_get_homogeneous (GtkBox *box)
{
  g_return_val_if_fail (GTK_IS_BOX (box), FALSE);

  return box->priv->homogeneous;
}

/**
 * gtk_box_set_spacing:
 * @box: a #GtkBox
 * @spacing: the number of pixels to put between children
 *
 * Sets the #GtkBox:spacing property of @box, which is the
 * number of pixels to place between children of @box.
 */
void
gtk_box_set_spacing (GtkBox *box,
		     gint    spacing)
{
  GtkBoxPrivate *private;

  g_return_if_fail (GTK_IS_BOX (box));

  private = box->priv;

  if (spacing != private->spacing)
    {
      private->spacing = spacing;
      _gtk_box_set_spacing_set (box, TRUE);

      g_object_notify (G_OBJECT (box), "spacing");

      gtk_widget_queue_resize (GTK_WIDGET (box));
    }
}

/**
 * gtk_box_get_spacing:
 * @box: a #GtkBox
 *
 * Gets the value set by gtk_box_set_spacing().
 *
 * Returns: spacing between children
 **/
gint
gtk_box_get_spacing (GtkBox *box)
{
  g_return_val_if_fail (GTK_IS_BOX (box), 0);

  return box->priv->spacing;
}

/**
 * gtk_box_set_baseline_position:
 * @box: a #GtkBox
 * @position: a #GtkBaselinePosition
 *
 * Sets the baseline position of a box. This affects
 * only horizontal boxes with at least one baseline aligned
 * child. If there is more vertical space available than requested,
 * and the baseline is not allocated by the parent then
 * @position is used to allocate the baseline wrt the
 * extra space available.
 *
 * Since: 3.10
 */
void
gtk_box_set_baseline_position (GtkBox             *box,
			       GtkBaselinePosition position)
{
  GtkBoxPrivate *private;

  g_return_if_fail (GTK_IS_BOX (box));

  private = box->priv;

  if (position != private->baseline_pos)
    {
      private->baseline_pos = position;

      g_object_notify (G_OBJECT (box), "baseline-position");

      gtk_widget_queue_resize (GTK_WIDGET (box));
    }
}

/**
 * gtk_box_get_baseline_position:
 * @box: a #GtkBox
 *
 * Gets the value set by gtk_box_set_baseline_position().
 *
 * Returns: the baseline position
 *
 * Since: 3.10
 **/
GtkBaselinePosition
gtk_box_get_baseline_position (GtkBox         *box)
{
  g_return_val_if_fail (GTK_IS_BOX (box), GTK_BASELINE_POSITION_CENTER);

  return box->priv->baseline_pos;
}


void
_gtk_box_set_spacing_set (GtkBox  *box,
                          gboolean spacing_set)
{
  GtkBoxPrivate *private;

  g_return_if_fail (GTK_IS_BOX (box));

  private = box->priv;

  private->spacing_set = spacing_set ? TRUE : FALSE;
}

gboolean
_gtk_box_get_spacing_set (GtkBox *box)
{
  GtkBoxPrivate *private;

  g_return_val_if_fail (GTK_IS_BOX (box), FALSE);

  private = box->priv;

  return private->spacing_set;
}

/**
 * gtk_box_reorder_child:
 * @box: a #GtkBox
 * @child: the #GtkWidget to move
 * @position: the new position for @child in the list of children
 *   of @box, starting from 0. If negative, indicates the end of
 *   the list
 *
 * Moves @child to a new @position in the list of @box children.
 * The list contains widgets packed #GTK_PACK_START
 * as well as widgets packed #GTK_PACK_END, in the order that these
 * widgets were added to @box.
 *
 * A widget’s position in the @box children list determines where
 * the widget is packed into @box.  A child widget at some position
 * in the list will be packed just after all other widgets of the
 * same packing type that appear earlier in the list.
 */
void
gtk_box_reorder_child (GtkBox    *box,
		       GtkWidget *child,
		       gint       position)
{
  GtkBoxPrivate *priv;
  GList *old_link;
  GList *new_link;
  GtkBoxChild *child_info = NULL;
  gint old_position;

  g_return_if_fail (GTK_IS_BOX (box));
  g_return_if_fail (GTK_IS_WIDGET (child));

  priv = box->priv;

  old_link = priv->children;
  old_position = 0;
  while (old_link)
    {
      child_info = old_link->data;
      if (child_info->widget == child)
	break;

      old_link = old_link->next;
      old_position++;
    }

  g_return_if_fail (old_link != NULL);

  if (position == old_position)
    return;

  priv->children = g_list_delete_link (priv->children, old_link);

  if (position < 0)
    new_link = NULL;
  else
    new_link = g_list_nth (priv->children, position);

  priv->children = g_list_insert_before (priv->children, new_link, child_info);

  gtk_widget_child_notify (child, "position");
  if (gtk_widget_get_visible (child)
      && gtk_widget_get_visible (GTK_WIDGET (box)))
    {
      gtk_box_invalidate_order (box);
      gtk_widget_queue_resize (child);
    }
}

/**
 * gtk_box_query_child_packing:
 * @box: a #GtkBox
 * @child: the #GtkWidget of the child to query
 * @expand: (out): pointer to return location for expand child
 *     property
 * @fill: (out): pointer to return location for fill child
 *     property
 * @padding: (out): pointer to return location for padding
 *     child property
 * @pack_type: (out): pointer to return location for pack-type
 *     child property
 *
 * Obtains information about how @child is packed into @box.
 */
void
gtk_box_query_child_packing (GtkBox      *box,
			     GtkWidget   *child,
			     gboolean    *expand,
			     gboolean    *fill,
			     guint       *padding,
			     GtkPackType *pack_type)
{
  GtkBoxPrivate *private;
  GList *list;
  GtkBoxChild *child_info = NULL;

  g_return_if_fail (GTK_IS_BOX (box));
  g_return_if_fail (GTK_IS_WIDGET (child));

  private = box->priv;

  list = private->children;
  while (list)
    {
      child_info = list->data;
      if (child_info->widget == child)
	break;

      list = list->next;
    }

  if (list)
    {
      if (expand)
	*expand = child_info->expand;
      if (fill)
	*fill = child_info->fill;
      if (padding)
	*padding = child_info->padding;
      if (pack_type)
	*pack_type = child_info->pack;
    }
}

/**
 * gtk_box_set_child_packing:
 * @box: a #GtkBox
 * @child: the #GtkWidget of the child to set
 * @expand: the new value of the expand child property
 * @fill: the new value of the fill child property
 * @padding: the new value of the padding child property
 * @pack_type: the new value of the pack-type child property
 *
 * Sets the way @child is packed into @box.
 */
void
gtk_box_set_child_packing (GtkBox      *box,
			   GtkWidget   *child,
			   gboolean     expand,
			   gboolean     fill,
			   guint        padding,
			   GtkPackType  pack_type)
{
  GtkBoxPrivate *private;
  GList *list;
  GtkBoxChild *child_info = NULL;

  g_return_if_fail (GTK_IS_BOX (box));
  g_return_if_fail (GTK_IS_WIDGET (child));

  private = box->priv;

  list = private->children;
  while (list)
    {
      child_info = list->data;
      if (child_info->widget == child)
	break;

      list = list->next;
    }

  gtk_widget_freeze_child_notify (child);
  if (list)
    {
      gboolean expanded;

      expanded = expand != FALSE;

      /* avoid setting expand if unchanged, since queue_compute_expand
       * can be expensive-ish
       */
      if (child_info->expand != expanded)
        {
          child_info->expand = expand != FALSE;
          gtk_widget_queue_compute_expand (GTK_WIDGET (box));
          gtk_widget_child_notify (child, "expand");
        }

      child_info->fill = fill != FALSE;
      gtk_widget_child_notify (child, "fill");
      child_info->padding = padding;
      gtk_widget_child_notify (child, "padding");
      if (pack_type != GTK_PACK_END)
        pack_type = GTK_PACK_START;
      if (child_info->pack != pack_type)
        {
	  child_info->pack = pack_type;
          gtk_widget_child_notify (child, "pack-type");
          gtk_box_invalidate_order (box);
        }

      if (gtk_widget_get_visible (child)
          && gtk_widget_get_visible (GTK_WIDGET (box)))
	gtk_widget_queue_resize (child);
    }
  gtk_widget_thaw_child_notify (child);
}

void
_gtk_box_set_old_defaults (GtkBox *box)
{
  GtkBoxPrivate *private;

  g_return_if_fail (GTK_IS_BOX (box));

  private = box->priv;

  private->default_expand = TRUE;
}

static void
gtk_box_add (GtkContainer *container,
	     GtkWidget    *widget)
{
  GtkBoxPrivate *priv = GTK_BOX (container)->priv;

  gtk_box_pack_start (GTK_BOX (container), widget,
                      priv->default_expand,
                      TRUE,
                      0);
}

static void
gtk_box_remove (GtkContainer *container,
		GtkWidget    *widget)
{
  GtkBox *box = GTK_BOX (container);
  GtkBoxPrivate *priv = box->priv;
  GtkBoxChild *child;
  GList *children;

  children = priv->children;
  while (children)
    {
      child = children->data;

      if (child->widget == widget)
	{
	  gboolean was_visible;

          if (priv->center == child)
            priv->center = NULL;

          g_signal_handlers_disconnect_by_func (widget,
                                                box_child_visibility_notify_cb,
                                                box);

	  was_visible = gtk_widget_get_visible (widget);
	  gtk_widget_unparent (widget);

	  priv->children = g_list_remove_link (priv->children, children);
	  g_list_free (children);
	  g_free (child);

	  /* queue resize regardless of gtk_widget_get_visible (container),
	   * since that's what is needed by toplevels.
	   */
	  if (was_visible)
            {
              gtk_box_invalidate_order (box);
	      gtk_widget_queue_resize (GTK_WIDGET (container));
            }

	  break;
	}

      children = children->next;
    }
}

static void
gtk_box_forall (GtkContainer *container,
		gboolean      include_internals,
		GtkCallback   callback,
		gpointer      callback_data)
{
  GtkBox *box = GTK_BOX (container);
  GtkBoxPrivate *priv = box->priv;
  GtkBoxChild *child;
  GList *children;

  children = priv->children;
  while (children)
    {
      child = children->data;
      children = children->next;

      if (child == priv->center)
        continue;

      if (child->pack == GTK_PACK_START)
	(* callback) (child->widget, callback_data);
    }

  if (priv->center)
    (* callback) (priv->center->widget, callback_data);

  children = g_list_last (priv->children);
  while (children)
    {
      child = children->data;
      children = children->prev;

      if (child == priv->center)
        continue;

      if (child->pack == GTK_PACK_END)
	(* callback) (child->widget, callback_data);
    }
}

GList *
_gtk_box_get_children (GtkBox *box)
{
  GtkBoxPrivate *priv;
  GtkBoxChild *child;
  GList *children;
  GList *retval = NULL;

  g_return_val_if_fail (GTK_IS_BOX (box), NULL);

  priv = box->priv;

  children = priv->children;
  while (children)
    {
      child = children->data;
      children = children->next;

      retval = g_list_prepend (retval, child->widget);
    }

  return g_list_reverse (retval);
}

/**
 * gtk_box_set_center_widget:
 * @box: a #GtkBox
 * @widget: (allow-none): the widget to center
 *
 * Sets a center widget; that is a child widget that will be
 * centered with respect to the full width of the box, even
 * if the children at either side take up different amounts
 * of space.
 *
 * Since: 3.12
 */
void
gtk_box_set_center_widget (GtkBox    *box,
                           GtkWidget *widget)
{
  GtkBoxPrivate *priv = box->priv;

  g_return_if_fail (GTK_IS_BOX (box));

  if (widget)
    priv->center = gtk_box_pack (box, widget, FALSE, TRUE, 0, GTK_PACK_START);
  else if (priv->center)
    gtk_box_remove (GTK_CONTAINER (box), priv->center->widget);
}

/**
 * gtk_box_get_center_widget:
 * @box: a #GtkBox
 *
 * Retrieves the center widget of the box.
 *
 * Returns: the center widget
 *
 * Since: 3.12
 */
GtkWidget *
gtk_box_get_center_widget (GtkBox *box)
{
  GtkBoxPrivate *priv = box->priv;

  g_return_val_if_fail (GTK_IS_BOX (box), NULL);

  if (priv->center)
    return priv->center->widget;

  return NULL;
}
