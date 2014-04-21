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
 * SECTION:gtkfixed
 * @Short_description: A container which allows you to position
 * widgets at fixed coordinates
 * @Title: GtkFixed
 *
 * The #GtkFixed widget is a container which can place child widgets
 * at fixed positions and with fixed sizes, given in pixels. #GtkFixed
 * performs no automatic layout management.
 *
 * For most applications, you should not use this container! It keeps
 * you from having to learn about the other GTK+ containers, but it
 * results in broken applications.  With #GtkFixed, the following
 * things will result in truncated text, overlapping widgets, and
 * other display bugs:
 *
 * - Themes, which may change widget sizes.
 *
 * - Fonts other than the one you used to write the app will of course
 *   change the size of widgets containing text; keep in mind that
 *   users may use a larger font because of difficulty reading the
 *   default, or they may be using Windows or the framebuffer port of
 *   GTK+, where different fonts are available.
 *
 * - Translation of text into other languages changes its size. Also,
 *   display of non-English text will use a different font in many
 *   cases.
 *
 * In addition, the fixed widget can’t properly be mirrored in
 * right-to-left languages such as Hebrew and Arabic. i.e. normally
 * GTK+ will flip the interface to put labels to the right of the
 * thing they label, but it can’t do that with #GtkFixed. So your
 * application will not be usable in right-to-left languages.
 *
 * Finally, fixed positioning makes it kind of annoying to add/remove
 * GUI elements, since you have to reposition all the other
 * elements. This is a long-term maintenance problem for your
 * application.
 *
 * If you know none of these things are an issue for your application,
 * and prefer the simplicity of #GtkFixed, by all means use the
 * widget. But you should be aware of the tradeoffs.
 */

#include "config.h"

#include "gtkfixed.h"

#include "gtkprivate.h"
#include "gtkintl.h"


struct _GtkFixedPrivate
{
  GList *children;
};

enum {
  CHILD_PROP_0,
  CHILD_PROP_X,
  CHILD_PROP_Y
};

static void gtk_fixed_realize       (GtkWidget        *widget);
static void gtk_fixed_get_preferred_width  (GtkWidget *widget,
                                            gint      *minimum,
                                            gint      *natural);
static void gtk_fixed_get_preferred_height (GtkWidget *widget,
                                            gint      *minimum,
                                            gint      *natural);
static void gtk_fixed_size_allocate (GtkWidget        *widget,
                                     GtkAllocation    *allocation);
static gboolean gtk_fixed_draw      (GtkWidget        *widget,
                                     cairo_t          *cr);
static void gtk_fixed_add           (GtkContainer     *container,
                                     GtkWidget        *widget);
static void gtk_fixed_remove        (GtkContainer     *container,
                                     GtkWidget        *widget);
static void gtk_fixed_forall        (GtkContainer     *container,
                                     gboolean          include_internals,
                                     GtkCallback       callback,
                                     gpointer          callback_data);
static GType gtk_fixed_child_type   (GtkContainer     *container);

static void gtk_fixed_set_child_property (GtkContainer *container,
                                          GtkWidget    *child,
                                          guint         property_id,
                                          const GValue *value,
                                          GParamSpec   *pspec);
static void gtk_fixed_get_child_property (GtkContainer *container,
                                          GtkWidget    *child,
                                          guint         property_id,
                                          GValue       *value,
                                          GParamSpec   *pspec);

G_DEFINE_TYPE_WITH_PRIVATE (GtkFixed, gtk_fixed, GTK_TYPE_CONTAINER)

static void
gtk_fixed_class_init (GtkFixedClass *class)
{
  GtkWidgetClass *widget_class;
  GtkContainerClass *container_class;

  widget_class = (GtkWidgetClass*) class;
  container_class = (GtkContainerClass*) class;

  widget_class->realize = gtk_fixed_realize;
  widget_class->get_preferred_width = gtk_fixed_get_preferred_width;
  widget_class->get_preferred_height = gtk_fixed_get_preferred_height;
  widget_class->size_allocate = gtk_fixed_size_allocate;
  widget_class->draw = gtk_fixed_draw;

  container_class->add = gtk_fixed_add;
  container_class->remove = gtk_fixed_remove;
  container_class->forall = gtk_fixed_forall;
  container_class->child_type = gtk_fixed_child_type;
  container_class->set_child_property = gtk_fixed_set_child_property;
  container_class->get_child_property = gtk_fixed_get_child_property;
  gtk_container_class_handle_border_width (container_class);

  gtk_container_class_install_child_property (container_class,
                                              CHILD_PROP_X,
                                              g_param_spec_int ("x",
                                                                P_("X position"),
                                                                P_("X position of child widget"),
                                                                G_MININT, G_MAXINT, 0,
                                                                GTK_PARAM_READWRITE));

  gtk_container_class_install_child_property (container_class,
                                              CHILD_PROP_Y,
                                              g_param_spec_int ("y",
                                                                P_("Y position"),
                                                                P_("Y position of child widget"),
                                                                G_MININT, G_MAXINT, 0,
                                                                GTK_PARAM_READWRITE));
}

static GType
gtk_fixed_child_type (GtkContainer *container)
{
  return GTK_TYPE_WIDGET;
}

static void
gtk_fixed_init (GtkFixed *fixed)
{
  fixed->priv = gtk_fixed_get_instance_private (fixed);

  gtk_widget_set_has_window (GTK_WIDGET (fixed), FALSE);

  fixed->priv->children = NULL;
}

/**
 * gtk_fixed_new:
 *
 * Creates a new #GtkFixed.
 *
 * Returns: a new #GtkFixed.
 */
GtkWidget*
gtk_fixed_new (void)
{
  return g_object_new (GTK_TYPE_FIXED, NULL);
}

static GtkFixedChild*
get_child (GtkFixed  *fixed,
           GtkWidget *widget)
{
  GtkFixedPrivate *priv = fixed->priv;
  GList *children;

  for (children = priv->children; children; children = children->next)
    {
      GtkFixedChild *child;

      child = children->data;

      if (child->widget == widget)
        return child;
    }

  return NULL;
}

/**
 * gtk_fixed_put:
 * @fixed: a #GtkFixed.
 * @widget: the widget to add.
 * @x: the horizontal position to place the widget at.
 * @y: the vertical position to place the widget at.
 *
 * Adds a widget to a #GtkFixed container at the given position.
 */
void
gtk_fixed_put (GtkFixed  *fixed,
               GtkWidget *widget,
               gint       x,
               gint       y)
{
  GtkFixedPrivate *priv = fixed->priv;
  GtkFixedChild *child_info;

  g_return_if_fail (GTK_IS_FIXED (fixed));
  g_return_if_fail (GTK_IS_WIDGET (widget));

  child_info = g_new (GtkFixedChild, 1);
  child_info->widget = widget;
  child_info->x = x;
  child_info->y = y;

  gtk_widget_set_parent (widget, GTK_WIDGET (fixed));

  priv->children = g_list_append (priv->children, child_info);
}

static void
gtk_fixed_move_internal (GtkFixed      *fixed,
                         GtkFixedChild *child,
                         gint           x,
                         gint           y)
{
  g_return_if_fail (GTK_IS_FIXED (fixed));
  g_return_if_fail (gtk_widget_get_parent (child->widget) == GTK_WIDGET (fixed));

  gtk_widget_freeze_child_notify (child->widget);

  if (child->x != x)
    {
      child->x = x;
      gtk_widget_child_notify (child->widget, "x");
    }

  if (child->y != y)
    {
      child->y = y;
      gtk_widget_child_notify (child->widget, "y");
    }

  gtk_widget_thaw_child_notify (child->widget);

  if (gtk_widget_get_visible (child->widget) &&
      gtk_widget_get_visible (GTK_WIDGET (fixed)))
    gtk_widget_queue_resize (GTK_WIDGET (fixed));
}

/**
 * gtk_fixed_move:
 * @fixed: a #GtkFixed.
 * @widget: the child widget.
 * @x: the horizontal position to move the widget to.
 * @y: the vertical position to move the widget to.
 *
 * Moves a child of a #GtkFixed container to the given position.
 */
void
gtk_fixed_move (GtkFixed  *fixed,
                GtkWidget *widget,
                gint       x,
                gint       y)
{
  gtk_fixed_move_internal (fixed, get_child (fixed, widget), x, y);
}

static void
gtk_fixed_set_child_property (GtkContainer *container,
                              GtkWidget    *child,
                              guint         property_id,
                              const GValue *value,
                              GParamSpec   *pspec)
{
  GtkFixed *fixed = GTK_FIXED (container);
  GtkFixedChild *fixed_child;

  fixed_child = get_child (fixed, child);

  switch (property_id)
    {
    case CHILD_PROP_X:
      gtk_fixed_move_internal (fixed,
                               fixed_child,
                               g_value_get_int (value),
                               fixed_child->y);
      break;
    case CHILD_PROP_Y:
      gtk_fixed_move_internal (fixed,
                               fixed_child,
                               fixed_child->x,
                               g_value_get_int (value));
      break;
    default:
      GTK_CONTAINER_WARN_INVALID_CHILD_PROPERTY_ID (container, property_id, pspec);
      break;
    }
}

static void
gtk_fixed_get_child_property (GtkContainer *container,
                              GtkWidget    *child,
                              guint         property_id,
                              GValue       *value,
                              GParamSpec   *pspec)
{
  GtkFixedChild *fixed_child;

  fixed_child = get_child (GTK_FIXED (container), child);
  
  switch (property_id)
    {
    case CHILD_PROP_X:
      g_value_set_int (value, fixed_child->x);
      break;
    case CHILD_PROP_Y:
      g_value_set_int (value, fixed_child->y);
      break;
    default:
      GTK_CONTAINER_WARN_INVALID_CHILD_PROPERTY_ID (container, property_id, pspec);
      break;
    }
}

static void
gtk_fixed_realize (GtkWidget *widget)
{
  GtkAllocation allocation;
  GdkWindow *window;
  GdkWindowAttr attributes;
  gint attributes_mask;

  if (!gtk_widget_get_has_window (widget))
    GTK_WIDGET_CLASS (gtk_fixed_parent_class)->realize (widget);
  else
    {
      gtk_widget_set_realized (widget, TRUE);

      gtk_widget_get_allocation (widget, &allocation);

      attributes.window_type = GDK_WINDOW_CHILD;
      attributes.x = allocation.x;
      attributes.y = allocation.y;
      attributes.width = allocation.width;
      attributes.height = allocation.height;
      attributes.wclass = GDK_INPUT_OUTPUT;
      attributes.visual = gtk_widget_get_visual (widget);
      attributes.event_mask = gtk_widget_get_events (widget);
      attributes.event_mask |= GDK_EXPOSURE_MASK | GDK_BUTTON_PRESS_MASK;

      attributes_mask = GDK_WA_X | GDK_WA_Y | GDK_WA_VISUAL;

      window = gdk_window_new (gtk_widget_get_parent_window (widget),
                               &attributes, attributes_mask);
      gtk_widget_set_window (widget, window);
      gtk_widget_register_window (widget, window);

      gtk_style_context_set_background (gtk_widget_get_style_context (widget),
                                        window);
    }
}

static void
gtk_fixed_get_preferred_width (GtkWidget *widget,
                               gint      *minimum,
                               gint      *natural)
{
  GtkFixed *fixed = GTK_FIXED (widget);
  GtkFixedPrivate *priv = fixed->priv;
  GtkFixedChild *child;
  GList *children;
  gint child_min, child_nat;

  *minimum = 0;
  *natural = 0;

  for (children = priv->children; children; children = children->next)
    {
      child = children->data;

      if (!gtk_widget_get_visible (child->widget))
        continue;

      gtk_widget_get_preferred_width (child->widget, &child_min, &child_nat);

      *minimum = MAX (*minimum, child->x + child_min);
      *natural = MAX (*natural, child->x + child_nat);
    }
}

static void
gtk_fixed_get_preferred_height (GtkWidget *widget,
                                gint      *minimum,
                                gint      *natural)
{
  GtkFixed *fixed = GTK_FIXED (widget);
  GtkFixedPrivate *priv = fixed->priv;
  GtkFixedChild *child;
  GList *children;
  gint child_min, child_nat;

  *minimum = 0;
  *natural = 0;

  for (children = priv->children; children; children = children->next)
    {
      child = children->data;

      if (!gtk_widget_get_visible (child->widget))
        continue;

      gtk_widget_get_preferred_height (child->widget, &child_min, &child_nat);

      *minimum = MAX (*minimum, child->y + child_min);
      *natural = MAX (*natural, child->y + child_nat);
    }
}

static void
gtk_fixed_size_allocate (GtkWidget     *widget,
                         GtkAllocation *allocation)
{
  GtkFixed *fixed = GTK_FIXED (widget);
  GtkFixedPrivate *priv = fixed->priv;
  GtkFixedChild *child;
  GtkAllocation child_allocation;
  GtkRequisition child_requisition;
  GList *children;

  gtk_widget_set_allocation (widget, allocation);

  if (gtk_widget_get_has_window (widget))
    {
      if (gtk_widget_get_realized (widget))
        gdk_window_move_resize (gtk_widget_get_window (widget),
                                allocation->x,
                                allocation->y,
                                allocation->width,
                                allocation->height);
    }

  for (children = priv->children; children; children = children->next)
    {
      child = children->data;

      if (!gtk_widget_get_visible (child->widget))
        continue;

      gtk_widget_get_preferred_size (child->widget, &child_requisition, NULL);
      child_allocation.x = child->x;
      child_allocation.y = child->y;

      if (!gtk_widget_get_has_window (widget))
        {
          child_allocation.x += allocation->x;
          child_allocation.y += allocation->y;
        }

      child_allocation.width = child_requisition.width;
      child_allocation.height = child_requisition.height;
      gtk_widget_size_allocate (child->widget, &child_allocation);
    }
}

static void
gtk_fixed_add (GtkContainer *container,
               GtkWidget    *widget)
{
  gtk_fixed_put (GTK_FIXED (container), widget, 0, 0);
}

static void
gtk_fixed_remove (GtkContainer *container,
                  GtkWidget    *widget)
{
  GtkFixed *fixed = GTK_FIXED (container);
  GtkFixedPrivate *priv = fixed->priv;
  GtkFixedChild *child;
  GtkWidget *widget_container = GTK_WIDGET (container);
  GList *children;

  for (children = priv->children; children; children = children->next)
    {
      child = children->data;

      if (child->widget == widget)
        {
          gboolean was_visible = gtk_widget_get_visible (widget);

          gtk_widget_unparent (widget);

          priv->children = g_list_remove_link (priv->children, children);
          g_list_free (children);
          g_free (child);

          if (was_visible && gtk_widget_get_visible (widget_container))
            gtk_widget_queue_resize (widget_container);

          break;
        }
    }
}

static void
gtk_fixed_forall (GtkContainer *container,
                  gboolean      include_internals,
                  GtkCallback   callback,
                  gpointer      callback_data)
{
  GtkFixed *fixed = GTK_FIXED (container);
  GtkFixedPrivate *priv = fixed->priv;
  GtkFixedChild *child;
  GList *children;

  children = priv->children;
  while (children)
    {
      child = children->data;
      children = children->next;

      (* callback) (child->widget, callback_data);
    }
}

static gboolean
gtk_fixed_draw (GtkWidget *widget,
                cairo_t   *cr)
{
  GtkFixed *fixed = GTK_FIXED (widget);
  GtkFixedPrivate *priv = fixed->priv;
  GtkFixedChild *child;
  GList *list;

  for (list = priv->children;
       list;
       list = list->next)
    {
      child = list->data;

      gtk_container_propagate_draw (GTK_CONTAINER (fixed),
                                    child->widget,
                                    cr);
    }
  
  return FALSE;
}

