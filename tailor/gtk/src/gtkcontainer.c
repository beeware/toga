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

#include "config.h"

#include "gtkcontainer.h"
#include "gtkcontainerprivate.h"

#include <stdarg.h>
#include <string.h>
#include <stdlib.h>

#include <gobject/gobjectnotifyqueue.c>
#include <gobject/gvaluecollector.h>

#include "gtkadjustment.h"
#include "gtkbuildable.h"
#include "gtkbuilderprivate.h"
#include "gtktypebuiltins.h"
#include "gtkprivate.h"
#include "gtkmain.h"
#include "gtkmarshalers.h"
#include "gtksizerequest.h"
#include "gtksizerequestcacheprivate.h"
#include "gtkwidgetprivate.h"
#include "gtkwindow.h"
#include "gtkassistant.h"
#include "gtkintl.h"
#include "gtkstylecontextprivate.h"
#include "gtkwidgetpath.h"
#include "a11y/gtkcontaineraccessible.h"
#include "a11y/gtkcontaineraccessibleprivate.h"

/**
 * SECTION:gtkcontainer
 * @Short_description: Base class for widgets which contain other widgets
 * @Title: GtkContainer
 *
 * A GTK+ user interface is constructed by nesting widgets inside widgets.
 * Container widgets are the inner nodes in the resulting tree of widgets:
 * they contain other widgets. So, for example, you might have a #GtkWindow
 * containing a #GtkFrame containing a #GtkLabel. If you wanted an image instead
 * of a textual label inside the frame, you might replace the #GtkLabel widget
 * with a #GtkImage widget.
 *
 * There are two major kinds of container widgets in GTK+. Both are subclasses
 * of the abstract GtkContainer base class.
 *
 * The first type of container widget has a single child widget and derives
 * from #GtkBin. These containers are decorators, which
 * add some kind of functionality to the child. For example, a #GtkButton makes
 * its child into a clickable button; a #GtkFrame draws a frame around its child
 * and a #GtkWindow places its child widget inside a top-level window.
 *
 * The second type of container can have more than one child; its purpose is to
 * manage layout. This means that these containers assign
 * sizes and positions to their children. For example, a #GtkHBox arranges its
 * children in a horizontal row, and a #GtkGrid arranges the widgets it contains
 * in a two-dimensional grid.
 *
 * # Height for width geometry management
 *
 * GTK+ uses a height-for-width (and width-for-height) geometry management system.
 * Height-for-width means that a widget can change how much vertical space it needs,
 * depending on the amount of horizontal space that it is given (and similar for
 * width-for-height).
 *
 * There are some things to keep in mind when implementing container widgets
 * that make use of GTK+’s height for width geometry management system. First,
 * it’s important to note that a container must prioritize one of its
 * dimensions, that is to say that a widget or container can only have a
 * #GtkSizeRequestMode that is %GTK_SIZE_REQUEST_HEIGHT_FOR_WIDTH or
 * %GTK_SIZE_REQUEST_WIDTH_FOR_HEIGHT. However, every widget and container
 * must be able to respond to the APIs for both dimensions, i.e. even if a
 * widget has a request mode that is height-for-width, it is possible that
 * its parent will request its sizes using the width-for-height APIs.
 *
 * To ensure that everything works properly, here are some guidelines to follow
 * when implementing height-for-width (or width-for-height) containers.
 *
 * Each request mode involves 2 virtual methods. Height-for-width apis run
 * through gtk_widget_get_preferred_width() and then through gtk_widget_get_preferred_height_for_width().
 * When handling requests in the opposite #GtkSizeRequestMode it is important that
 * every widget request at least enough space to display all of its content at all times.
 *
 * When gtk_widget_get_preferred_height() is called on a container that is height-for-width,
 * the container must return the height for its minimum width. This is easily achieved by
 * simply calling the reverse apis implemented for itself as follows:
 *
 * |[<!-- language="C" -->
 * static void
 * foo_container_get_preferred_height (GtkWidget *widget,
 *                                     gint *min_height,
 *                                     gint *nat_height)
 * {
 *    if (i_am_in_height_for_width_mode)
 *      {
 *        gint min_width;
 *
 *        GTK_WIDGET_GET_CLASS (widget)->get_preferred_width (widget,
 *                                                            &min_width,
 *                                                            NULL);
 *        GTK_WIDGET_GET_CLASS (widget)->get_preferred_height_for_width
 *                                                           (widget,
 *                                                            min_width,
 *                                                            min_height,
 *                                                            nat_height);
 *      }
 *    else
 *      {
 *        ... many containers support both request modes, execute the
 *        real width-for-height request here by returning the
 *        collective heights of all widgets that are stacked
 *        vertically (or whatever is appropriate for this container)
 *        ...
 *      }
 * }
 * ]|
 *
 * Similarly, when gtk_widget_get_preferred_width_for_height() is called for a container or widget
 * that is height-for-width, it then only needs to return the base minimum width like so:
 *
 * |[<!-- language="C" -->
 * static void
 * foo_container_get_preferred_width_for_height (GtkWidget *widget,
 *                                               gint for_height,
 *                                               gint *min_width,
 *                                               gint *nat_width)
 * {
 *    if (i_am_in_height_for_width_mode)
 *      {
 *        GTK_WIDGET_GET_CLASS (widget)->get_preferred_width (widget,
 *                                                            min_width,
 *                                                            nat_width);
 *      }
 *    else
 *      {
 *        ... execute the real width-for-height request here based on
 *        the required width of the children collectively if the
 *        container were to be allocated the said height ...
 *      }
 * }
 * ]|
 *
 * Height for width requests are generally implemented in terms of a virtual allocation
 * of widgets in the input orientation. Assuming an height-for-width request mode, a container
 * would implement the get_preferred_height_for_width() virtual function by first calling
 * gtk_widget_get_preferred_width() for each of its children.
 *
 * For each potential group of children that are lined up horizontally, the values returned by
 * gtk_widget_get_preferred_width() should be collected in an array of #GtkRequestedSize structures.
 * Any child spacing should be removed from the input @for_width and then the collective size should be
 * allocated using the gtk_distribute_natural_allocation() convenience function.
 *
 * The container will then move on to request the preferred height for each child by using
 * gtk_widget_get_preferred_height_for_width() and using the sizes stored in the #GtkRequestedSize array.
 *
 * To allocate a height-for-width container, it’s again important
 * to consider that a container must prioritize one dimension over the other. So if
 * a container is a height-for-width container it must first allocate all widgets horizontally
 * using a #GtkRequestedSize array and gtk_distribute_natural_allocation() and then add any
 * extra space (if and where appropriate) for the widget to expand.
 *
 * After adding all the expand space, the container assumes it was allocated sufficient
 * height to fit all of its content. At this time, the container must use the total horizontal sizes
 * of each widget to request the height-for-width of each of its children and store the requests in a
 * #GtkRequestedSize array for any widgets that stack vertically (for tabular containers this can
 * be generalized into the heights and widths of rows and columns).
 * The vertical space must then again be distributed using gtk_distribute_natural_allocation()
 * while this time considering the allocated height of the widget minus any vertical spacing
 * that the container adds. Then vertical expand space should be added where appropriate and available
 * and the container should go on to actually allocating the child widgets.
 *
 * See [GtkWidget’s geometry management section][geometry-management]
 * to learn more about implementing height-for-width geometry management for widgets.
 *
 * # Child properties
 *
 * GtkContainer introduces child properties.
 * These are object properties that are not specific
 * to either the container or the contained widget, but rather to their relation.
 * Typical examples of child properties are the position or pack-type of a widget
 * which is contained in a #GtkBox.
 *
 * Use gtk_container_class_install_child_property() to install child properties
 * for a container class and gtk_container_class_find_child_property() or
 * gtk_container_class_list_child_properties() to get information about existing
 * child properties.
 *
 * To set the value of a child property, use gtk_container_child_set_property(),
 * gtk_container_child_set() or gtk_container_child_set_valist().
 * To obtain the value of a child property, use
 * gtk_container_child_get_property(), gtk_container_child_get() or
 * gtk_container_child_get_valist(). To emit notification about child property
 * changes, use gtk_widget_child_notify().
 *
 * # GtkContainer as GtkBuildable
 *
 * The GtkContainer implementation of the GtkBuildable interface supports
 * a <packing> element for children, which can contain multiple <property>
 * elements that specify child properties for the child.
 * 
 * An example of child properties in UI definitions:
 * |[
 * <object class="GtkVBox">
 *   <child>
 *     <object class="GtkLabel"/>
 *     <packing>
 *       <property name="pack-type">start</property>
 *     </packing>
 *   </child>
 * </object>
 * ]|
 *
 * Since 2.16, child properties can also be marked as translatable using
 * the same “translatable”, “comments” and “context” attributes that are used
 * for regular properties.
 */


struct _GtkContainerPrivate
{
  GtkWidget *focus_child;

  GdkFrameClock *resize_clock;
  guint resize_handler;

  guint border_width : 16;
  guint border_width_set   : 1;

  guint has_focus_chain    : 1;
  guint reallocate_redraws : 1;
  guint resize_pending     : 1;
  guint restyle_pending    : 1;
  guint resize_mode        : 2;
  guint request_mode       : 2;
};

enum {
  ADD,
  REMOVE,
  CHECK_RESIZE,
  SET_FOCUS_CHILD,
  LAST_SIGNAL
};

enum {
  PROP_0,
  PROP_BORDER_WIDTH,
  PROP_RESIZE_MODE,
  PROP_CHILD
};

#define PARAM_SPEC_PARAM_ID(pspec)              ((pspec)->param_id)
#define PARAM_SPEC_SET_PARAM_ID(pspec, id)      ((pspec)->param_id = (id))


/* --- prototypes --- */
static void     gtk_container_base_class_init      (GtkContainerClass *klass);
static void     gtk_container_base_class_finalize  (GtkContainerClass *klass);
static void     gtk_container_class_init           (GtkContainerClass *klass);
static void     gtk_container_init                 (GtkContainer      *container);
static void     gtk_container_destroy              (GtkWidget         *widget);
static void     gtk_container_set_property         (GObject         *object,
                                                    guint            prop_id,
                                                    const GValue    *value,
                                                    GParamSpec      *pspec);
static void     gtk_container_get_property         (GObject         *object,
                                                    guint            prop_id,
                                                    GValue          *value,
                                                    GParamSpec      *pspec);
static void     gtk_container_add_unimplemented    (GtkContainer      *container,
                                                    GtkWidget         *widget);
static void     gtk_container_remove_unimplemented (GtkContainer      *container,
                                                    GtkWidget         *widget);
static void     gtk_container_real_check_resize    (GtkContainer      *container);
static void     gtk_container_compute_expand       (GtkWidget         *widget,
                                                    gboolean          *hexpand_p,
                                                    gboolean          *vexpand_p);
static gboolean gtk_container_focus                (GtkWidget         *widget,
                                                    GtkDirectionType   direction);
static void     gtk_container_real_set_focus_child (GtkContainer      *container,
                                                    GtkWidget         *widget);

static gboolean gtk_container_focus_move           (GtkContainer      *container,
                                                    GList             *children,
                                                    GtkDirectionType   direction);
static void     gtk_container_children_callback    (GtkWidget         *widget,
                                                    gpointer           client_data);
static void     gtk_container_show_all             (GtkWidget         *widget);
static gint     gtk_container_draw                 (GtkWidget         *widget,
                                                    cairo_t           *cr);
static void     gtk_container_map                  (GtkWidget         *widget);
static void     gtk_container_unmap                (GtkWidget         *widget);
static void     gtk_container_adjust_size_request  (GtkWidget         *widget,
                                                    GtkOrientation     orientation,
                                                    gint              *minimum_size,
                                                    gint              *natural_size);
static void     gtk_container_adjust_baseline_request (GtkWidget      *widget,
						       gint           *minimum_baseline,
						       gint           *natural_baseline);
static void     gtk_container_adjust_size_allocation (GtkWidget       *widget,
                                                      GtkOrientation   orientation,
                                                      gint            *minimum_size,
                                                      gint            *natural_size,
                                                      gint            *allocated_pos,
                                                      gint            *allocated_size);
static void     gtk_container_adjust_baseline_allocation (GtkWidget      *widget,
							  gint           *baseline);
static GtkSizeRequestMode gtk_container_get_request_mode (GtkWidget   *widget);

static gchar* gtk_container_child_default_composite_name (GtkContainer *container,
                                                          GtkWidget    *child);

static GtkWidgetPath * gtk_container_real_get_path_for_child (GtkContainer *container,
                                                              GtkWidget    *child);

/* GtkBuildable */
static void gtk_container_buildable_init           (GtkBuildableIface *iface);
static void gtk_container_buildable_add_child      (GtkBuildable *buildable,
                                                    GtkBuilder   *builder,
                                                    GObject      *child,
                                                    const gchar  *type);
static gboolean gtk_container_buildable_custom_tag_start (GtkBuildable  *buildable,
                                                          GtkBuilder    *builder,
                                                          GObject       *child,
                                                          const gchar   *tagname,
                                                          GMarkupParser *parser,
                                                          gpointer      *data);
static void    gtk_container_buildable_custom_tag_end (GtkBuildable *buildable,
                                                       GtkBuilder   *builder,
                                                       GObject      *child,
                                                       const gchar  *tagname,
                                                       gpointer     *data);

static gboolean gtk_container_should_propagate_draw (GtkContainer   *container,
                                                     GtkWidget      *child,
                                                     cairo_t        *cr);

/* --- variables --- */
static const gchar           vadjustment_key[] = "gtk-vadjustment";
static guint                 vadjustment_key_id = 0;
static const gchar           hadjustment_key[] = "gtk-hadjustment";
static guint                 hadjustment_key_id = 0;
static guint                 container_signals[LAST_SIGNAL] = { 0 };
static gint                  GtkContainer_private_offset;
static GtkWidgetClass       *parent_class = NULL;
extern GParamSpecPool       *_gtk_widget_child_property_pool;
extern GObjectNotifyContext *_gtk_widget_child_property_notify_context;
static GtkBuildableIface    *parent_buildable_iface;


/* --- functions --- */
static inline gpointer
gtk_container_get_instance_private (GtkContainer *self)
{
  return G_STRUCT_MEMBER_P (self, GtkContainer_private_offset);
}

GType
gtk_container_get_type (void)
{
  static GType container_type = 0;

  if (!container_type)
    {
      const GTypeInfo container_info =
      {
        sizeof (GtkContainerClass),
        (GBaseInitFunc) gtk_container_base_class_init,
        (GBaseFinalizeFunc) gtk_container_base_class_finalize,
        (GClassInitFunc) gtk_container_class_init,
        NULL        /* class_finalize */,
        NULL        /* class_data */,
        sizeof (GtkContainer),
        0           /* n_preallocs */,
        (GInstanceInitFunc) gtk_container_init,
        NULL,       /* value_table */
      };

      const GInterfaceInfo buildable_info =
      {
        (GInterfaceInitFunc) gtk_container_buildable_init,
        NULL,
        NULL
      };

      container_type =
        g_type_register_static (GTK_TYPE_WIDGET, I_("GtkContainer"),
                                &container_info, G_TYPE_FLAG_ABSTRACT);

      GtkContainer_private_offset =
        g_type_add_instance_private (container_type, sizeof (GtkContainerPrivate));

      g_type_add_interface_static (container_type,
                                   GTK_TYPE_BUILDABLE,
                                   &buildable_info);

    }

  return container_type;
}

static void
gtk_container_base_class_init (GtkContainerClass *class)
{
  /* reset instance specifc class fields that don't get inherited */
  class->set_child_property = NULL;
  class->get_child_property = NULL;
}

static void
gtk_container_base_class_finalize (GtkContainerClass *class)
{
  GList *list, *node;

  list = g_param_spec_pool_list_owned (_gtk_widget_child_property_pool, G_OBJECT_CLASS_TYPE (class));
  for (node = list; node; node = node->next)
    {
      GParamSpec *pspec = node->data;

      g_param_spec_pool_remove (_gtk_widget_child_property_pool, pspec);
      PARAM_SPEC_SET_PARAM_ID (pspec, 0);
      g_param_spec_unref (pspec);
    }
  g_list_free (list);
}

static void
gtk_container_class_init (GtkContainerClass *class)
{
  GObjectClass *gobject_class = G_OBJECT_CLASS (class);
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (class);

  parent_class = g_type_class_peek_parent (class);

  vadjustment_key_id = g_quark_from_static_string (vadjustment_key);
  hadjustment_key_id = g_quark_from_static_string (hadjustment_key);

  gobject_class->set_property = gtk_container_set_property;
  gobject_class->get_property = gtk_container_get_property;

  widget_class->destroy = gtk_container_destroy;
  widget_class->compute_expand = gtk_container_compute_expand;
  widget_class->show_all = gtk_container_show_all;
  widget_class->draw = gtk_container_draw;
  widget_class->map = gtk_container_map;
  widget_class->unmap = gtk_container_unmap;
  widget_class->focus = gtk_container_focus;

  widget_class->adjust_size_request = gtk_container_adjust_size_request;
  widget_class->adjust_baseline_request = gtk_container_adjust_baseline_request;
  widget_class->adjust_size_allocation = gtk_container_adjust_size_allocation;
  widget_class->adjust_baseline_allocation = gtk_container_adjust_baseline_allocation;
  widget_class->get_request_mode = gtk_container_get_request_mode;

  class->add = gtk_container_add_unimplemented;
  class->remove = gtk_container_remove_unimplemented;
  class->check_resize = gtk_container_real_check_resize;
  class->forall = NULL;
  class->set_focus_child = gtk_container_real_set_focus_child;
  class->child_type = NULL;
  class->composite_name = gtk_container_child_default_composite_name;
  class->get_path_for_child = gtk_container_real_get_path_for_child;

  g_object_class_install_property (gobject_class,
                                   PROP_RESIZE_MODE,
                                   g_param_spec_enum ("resize-mode",
                                                      P_("Resize mode"),
                                                      P_("Specify how resize events are handled"),
                                                      GTK_TYPE_RESIZE_MODE,
                                                      GTK_RESIZE_PARENT,
                                                      GTK_PARAM_READWRITE));
  g_object_class_install_property (gobject_class,
                                   PROP_BORDER_WIDTH,
                                   g_param_spec_uint ("border-width",
                                                      P_("Border width"),
                                                      P_("The width of the empty border outside the containers children"),
                                                      0,
                                                      65535,
                                                      0,
                                                      GTK_PARAM_READWRITE));
  g_object_class_install_property (gobject_class,
                                   PROP_CHILD,
                                   g_param_spec_object ("child",
                                                      P_("Child"),
                                                      P_("Can be used to add a new child to the container"),
                                                      GTK_TYPE_WIDGET,
                                                      GTK_PARAM_WRITABLE));
  container_signals[ADD] =
    g_signal_new (I_("add"),
                  G_OBJECT_CLASS_TYPE (gobject_class),
                  G_SIGNAL_RUN_FIRST,
                  G_STRUCT_OFFSET (GtkContainerClass, add),
                  NULL, NULL,
                  _gtk_marshal_VOID__OBJECT,
                  G_TYPE_NONE, 1,
                  GTK_TYPE_WIDGET);
  container_signals[REMOVE] =
    g_signal_new (I_("remove"),
                  G_OBJECT_CLASS_TYPE (gobject_class),
                  G_SIGNAL_RUN_FIRST,
                  G_STRUCT_OFFSET (GtkContainerClass, remove),
                  NULL, NULL,
                  _gtk_marshal_VOID__OBJECT,
                  G_TYPE_NONE, 1,
                  GTK_TYPE_WIDGET);
  container_signals[CHECK_RESIZE] =
    g_signal_new (I_("check-resize"),
                  G_OBJECT_CLASS_TYPE (gobject_class),
                  G_SIGNAL_RUN_LAST,
                  G_STRUCT_OFFSET (GtkContainerClass, check_resize),
                  NULL, NULL,
                  _gtk_marshal_VOID__VOID,
                  G_TYPE_NONE, 0);
  container_signals[SET_FOCUS_CHILD] =
    g_signal_new (I_("set-focus-child"),
                  G_OBJECT_CLASS_TYPE (gobject_class),
                  G_SIGNAL_RUN_FIRST,
                  G_STRUCT_OFFSET (GtkContainerClass, set_focus_child),
                  NULL, NULL,
                  _gtk_marshal_VOID__OBJECT,
                  G_TYPE_NONE, 1,
                  GTK_TYPE_WIDGET);

  if (GtkContainer_private_offset != 0)
    g_type_class_adjust_private_offset (class, &GtkContainer_private_offset);

  gtk_widget_class_set_accessible_type (widget_class, GTK_TYPE_CONTAINER_ACCESSIBLE);
}

static void
gtk_container_buildable_init (GtkBuildableIface *iface)
{
  parent_buildable_iface = g_type_interface_peek_parent (iface);
  iface->add_child = gtk_container_buildable_add_child;
  iface->custom_tag_start = gtk_container_buildable_custom_tag_start;
  iface->custom_tag_end = gtk_container_buildable_custom_tag_end;
}

static void
gtk_container_buildable_add_child (GtkBuildable  *buildable,
                                   GtkBuilder    *builder,
                                   GObject       *child,
                                   const gchar   *type)
{
  if (type)
    {
      GTK_BUILDER_WARN_INVALID_CHILD_TYPE (buildable, type);
    }
  else if (GTK_IS_WIDGET (child) &&
           gtk_widget_get_parent (GTK_WIDGET (child)) == NULL)
    {
      gtk_container_add (GTK_CONTAINER (buildable), GTK_WIDGET (child));
    }
  else
    g_warning ("Cannot add an object of type %s to a container of type %s",
               g_type_name (G_OBJECT_TYPE (child)), g_type_name (G_OBJECT_TYPE (buildable)));
}

static void
gtk_container_buildable_set_child_property (GtkContainer *container,
                                            GtkBuilder   *builder,
                                            GtkWidget    *child,
                                            gchar        *name,
                                            const gchar  *value)
{
  GParamSpec *pspec;
  GValue gvalue = G_VALUE_INIT;
  GError *error = NULL;

  if (gtk_widget_get_parent (child) != (GtkWidget *)container && !GTK_IS_ASSISTANT (container) && !GTK_IS_ACTION_BAR (container))
    {
      /* This can happen with internal children of complex widgets.
       * Silently ignore the child properties in this case. We explicitly
       * allow it for GtkAssistant, since that is how it works.
       */
      return;
    }

  pspec = gtk_container_class_find_child_property (G_OBJECT_GET_CLASS (container), name);
  if (!pspec)
    {
      g_warning ("%s does not have a property called %s",
                 g_type_name (G_OBJECT_TYPE (container)), name);
      return;
    }

  if (!gtk_builder_value_from_string (builder, pspec, value, &gvalue, &error))
    {
      g_warning ("Could not read property %s:%s with value %s of type %s: %s",
                 g_type_name (G_OBJECT_TYPE (container)),
                 name,
                 value,
                 g_type_name (G_PARAM_SPEC_VALUE_TYPE (pspec)),
                 error->message);
      g_error_free (error);
      return;
    }

  gtk_container_child_set_property (container, child, name, &gvalue);
  g_value_unset (&gvalue);
}

typedef struct {
  GtkBuilder   *builder;
  GtkContainer *container;
  GtkWidget    *child;
  GString      *string;
  gchar        *child_prop_name;
  gchar        *context;
  gboolean      translatable;
} PackingPropertiesData;

static void
attributes_start_element (GMarkupParseContext *context,
                          const gchar         *element_name,
                          const gchar        **names,
                          const gchar        **values,
                          gpointer             user_data,
                          GError             **error)
{
  PackingPropertiesData *parser_data = (PackingPropertiesData*)user_data;
  guint i;

  if (strcmp (element_name, "property") == 0)
    {
      for (i = 0; names[i]; i++)
        if (strcmp (names[i], "name") == 0)
          parser_data->child_prop_name = g_strdup (values[i]);
        else if (strcmp (names[i], "translatable") == 0)
          {
            if (!_gtk_builder_boolean_from_string (values[1],
                                                   &parser_data->translatable,
                                                   error))
              return;
          }
        else if (strcmp (names[i], "comments") == 0)
          ; /* for translators */
        else if (strcmp (names[i], "context") == 0)
          parser_data->context = g_strdup (values[1]);
        else
          g_warning ("Unsupported attribute for GtkContainer Child "
                     "property: %s\n", names[i]);
    }
  else if (strcmp (element_name, "packing") == 0)
    return;
  else
    g_warning ("Unsupported tag for GtkContainer: %s\n", element_name);
}

static void
attributes_text_element (GMarkupParseContext *context,
                         const gchar         *text,
                         gsize                text_len,
                         gpointer             user_data,
                         GError             **error)
{
  PackingPropertiesData *parser_data = (PackingPropertiesData*)user_data;

  if (parser_data->child_prop_name)
    g_string_append_len (parser_data->string, text, text_len);
}

static void
attributes_end_element (GMarkupParseContext *context,
			const gchar         *element_name,
			gpointer             user_data,
			GError             **error)
{
  PackingPropertiesData *parser_data = (PackingPropertiesData*)user_data;

  /* translate the string */
  if (parser_data->string->len && parser_data->translatable)
    {
      const gchar *translated;
      const gchar *domain;

      domain = gtk_builder_get_translation_domain (parser_data->builder);

      translated = _gtk_builder_parser_translate (domain,
                                                  parser_data->context,
                                                  parser_data->string->str);
      g_string_assign (parser_data->string, translated);
    }

  if (parser_data->child_prop_name)
    gtk_container_buildable_set_child_property (parser_data->container,
						parser_data->builder,
						parser_data->child,
						parser_data->child_prop_name,
						parser_data->string->str);

  g_string_set_size (parser_data->string, 0);
  g_free (parser_data->child_prop_name);
  g_free (parser_data->context);
  parser_data->child_prop_name = NULL;
  parser_data->context = NULL;
  parser_data->translatable = FALSE;
}

static const GMarkupParser attributes_parser =
  {
    attributes_start_element,
    attributes_end_element,
    attributes_text_element,
  };

static gboolean
gtk_container_buildable_custom_tag_start (GtkBuildable  *buildable,
                                          GtkBuilder    *builder,
                                          GObject       *child,
                                          const gchar   *tagname,
                                          GMarkupParser *parser,
                                          gpointer      *data)
{
  PackingPropertiesData *parser_data;

  if (parent_buildable_iface->custom_tag_start (buildable, builder, child,
                                                tagname, parser, data))
    return TRUE;

  if (child && strcmp (tagname, "packing") == 0)
    {
      parser_data = g_slice_new0 (PackingPropertiesData);
      parser_data->string = g_string_new ("");
      parser_data->builder = builder;
      parser_data->container = GTK_CONTAINER (buildable);
      parser_data->child = GTK_WIDGET (child);
      parser_data->child_prop_name = NULL;

      *parser = attributes_parser;
      *data = parser_data;
      return TRUE;
    }

  return FALSE;
}

static void
gtk_container_buildable_custom_tag_end (GtkBuildable *buildable,
                                        GtkBuilder   *builder,
                                        GObject      *child,
                                        const gchar  *tagname,
                                        gpointer     *data)
{
  if (strcmp (tagname, "packing") == 0)
    {
      PackingPropertiesData *parser_data = (PackingPropertiesData*)data;
      g_string_free (parser_data->string, TRUE);
      g_slice_free (PackingPropertiesData, parser_data);
      return;
    }

  if (parent_buildable_iface->custom_tag_end)
    parent_buildable_iface->custom_tag_end (buildable, builder,
                                            child, tagname, data);
}

/**
 * gtk_container_child_type:
 * @container: a #GtkContainer
 *
 * Returns the type of the children supported by the container.
 *
 * Note that this may return %G_TYPE_NONE to indicate that no more
 * children can be added, e.g. for a #GtkPaned which already has two
 * children.
 *
 * Returns: a #GType.
 **/
GType
gtk_container_child_type (GtkContainer *container)
{
  GType slot;
  GtkContainerClass *class;

  g_return_val_if_fail (GTK_IS_CONTAINER (container), 0);

  class = GTK_CONTAINER_GET_CLASS (container);
  if (class->child_type)
    slot = class->child_type (container);
  else
    slot = G_TYPE_NONE;

  return slot;
}

/* --- GtkContainer child property mechanism --- */

/**
 * gtk_container_child_notify:
 * @container: the #GtkContainer
 * @child: the child widget
 * @child_property: the name of a child property installed on
 *     the class of @container
 *
 * Emits a #GtkWidget::child-notify signal for the
 * [child property][child-properties]
 * @child_property on widget.
 *
 * This is an analogue of g_object_notify() for child properties.
 *
 * Also see gtk_widget_child_notify().
 *
 * Since: 3.2
 */
void
gtk_container_child_notify (GtkContainer *container,
                            GtkWidget    *child,
                            const gchar  *child_property)
{
  GObject *obj;
  GParamSpec *pspec;

  g_return_if_fail (GTK_IS_CONTAINER (container));
  g_return_if_fail (GTK_IS_WIDGET (child));
  g_return_if_fail (child_property != NULL);

  obj = G_OBJECT (child);

  if (obj->ref_count == 0)
    return;

  g_object_ref (obj);

  pspec = g_param_spec_pool_lookup (_gtk_widget_child_property_pool,
                                    child_property,
                                    G_OBJECT_TYPE (container),
                                    TRUE);

  if (pspec == NULL)
    {
      g_warning ("%s: container class `%s' has no child property named `%s'",
                 G_STRLOC,
                 G_OBJECT_TYPE_NAME (container),
                 child_property);
    }
  else
    {
      GObjectNotifyQueue *nqueue;

      nqueue = g_object_notify_queue_freeze (obj, _gtk_widget_child_property_notify_context);

      g_object_notify_queue_add (obj, nqueue, pspec);
      g_object_notify_queue_thaw (obj, nqueue);
    }

  g_object_unref (obj);
}

static inline void
container_get_child_property (GtkContainer *container,
                              GtkWidget    *child,
                              GParamSpec   *pspec,
                              GValue       *value)
{
  GtkContainerClass *class = g_type_class_peek (pspec->owner_type);

  class->get_child_property (container, child, PARAM_SPEC_PARAM_ID (pspec), value, pspec);
}

static inline void
container_set_child_property (GtkContainer       *container,
                              GtkWidget          *child,
                              GParamSpec         *pspec,
                              const GValue       *value,
                              GObjectNotifyQueue *nqueue)
{
  GValue tmp_value = G_VALUE_INIT;
  GtkContainerClass *class = g_type_class_peek (pspec->owner_type);

  /* provide a copy to work from, convert (if necessary) and validate */
  g_value_init (&tmp_value, G_PARAM_SPEC_VALUE_TYPE (pspec));
  if (!g_value_transform (value, &tmp_value))
    g_warning ("unable to set child property `%s' of type `%s' from value of type `%s'",
               pspec->name,
               g_type_name (G_PARAM_SPEC_VALUE_TYPE (pspec)),
               G_VALUE_TYPE_NAME (value));
  else if (g_param_value_validate (pspec, &tmp_value) && !(pspec->flags & G_PARAM_LAX_VALIDATION))
    {
      gchar *contents = g_strdup_value_contents (value);

      g_warning ("value \"%s\" of type `%s' is invalid for property `%s' of type `%s'",
                 contents,
                 G_VALUE_TYPE_NAME (value),
                 pspec->name,
                 g_type_name (G_PARAM_SPEC_VALUE_TYPE (pspec)));
      g_free (contents);
    }
  else
    {
      class->set_child_property (container, child, PARAM_SPEC_PARAM_ID (pspec), &tmp_value, pspec);
      g_object_notify_queue_add (G_OBJECT (child), nqueue, pspec);
    }
  g_value_unset (&tmp_value);
}

/**
 * gtk_container_child_get_valist:
 * @container: a #GtkContainer
 * @child: a widget which is a child of @container
 * @first_property_name: the name of the first property to get
 * @var_args: return location for the first property, followed
 *     optionally by more name/return location pairs, followed by %NULL
 *
 * Gets the values of one or more child properties for @child and @container.
 **/
void
gtk_container_child_get_valist (GtkContainer *container,
                                GtkWidget    *child,
                                const gchar  *first_property_name,
                                va_list       var_args)
{
  const gchar *name;

  g_return_if_fail (GTK_IS_CONTAINER (container));
  g_return_if_fail (GTK_IS_WIDGET (child));

  g_object_ref (container);
  g_object_ref (child);

  name = first_property_name;
  while (name)
    {
      GValue value = G_VALUE_INIT;
      GParamSpec *pspec;
      gchar *error;

      pspec = g_param_spec_pool_lookup (_gtk_widget_child_property_pool,
                                        name,
                                        G_OBJECT_TYPE (container),
                                        TRUE);
      if (!pspec)
        {
          g_warning ("%s: container class `%s' has no child property named `%s'",
                     G_STRLOC,
                     G_OBJECT_TYPE_NAME (container),
                     name);
          break;
        }
      if (!(pspec->flags & G_PARAM_READABLE))
        {
          g_warning ("%s: child property `%s' of container class `%s' is not readable",
                     G_STRLOC,
                     pspec->name,
                     G_OBJECT_TYPE_NAME (container));
          break;
        }
      g_value_init (&value, G_PARAM_SPEC_VALUE_TYPE (pspec));
      container_get_child_property (container, child, pspec, &value);
      G_VALUE_LCOPY (&value, var_args, 0, &error);
      if (error)
        {
          g_warning ("%s: %s", G_STRLOC, error);
          g_free (error);
          g_value_unset (&value);
          break;
        }
      g_value_unset (&value);
      name = va_arg (var_args, gchar*);
    }

  g_object_unref (child);
  g_object_unref (container);
}

/**
 * gtk_container_child_get_property:
 * @container: a #GtkContainer
 * @child: a widget which is a child of @container
 * @property_name: the name of the property to get
 * @value: a location to return the value
 *
 * Gets the value of a child property for @child and @container.
 **/
void
gtk_container_child_get_property (GtkContainer *container,
                                  GtkWidget    *child,
                                  const gchar  *property_name,
                                  GValue       *value)
{
  GParamSpec *pspec;

  g_return_if_fail (GTK_IS_CONTAINER (container));
  g_return_if_fail (GTK_IS_WIDGET (child));
  g_return_if_fail (property_name != NULL);
  g_return_if_fail (G_IS_VALUE (value));

  g_object_ref (container);
  g_object_ref (child);
  pspec = g_param_spec_pool_lookup (_gtk_widget_child_property_pool, property_name,
                                    G_OBJECT_TYPE (container), TRUE);
  if (!pspec)
    g_warning ("%s: container class `%s' has no child property named `%s'",
               G_STRLOC,
               G_OBJECT_TYPE_NAME (container),
               property_name);
  else if (!(pspec->flags & G_PARAM_READABLE))
    g_warning ("%s: child property `%s' of container class `%s' is not readable",
               G_STRLOC,
               pspec->name,
               G_OBJECT_TYPE_NAME (container));
  else
    {
      GValue *prop_value, tmp_value = G_VALUE_INIT;

      /* auto-conversion of the callers value type
       */
      if (G_VALUE_TYPE (value) == G_PARAM_SPEC_VALUE_TYPE (pspec))
        {
          g_value_reset (value);
          prop_value = value;
        }
      else if (!g_value_type_transformable (G_PARAM_SPEC_VALUE_TYPE (pspec), G_VALUE_TYPE (value)))
        {
          g_warning ("can't retrieve child property `%s' of type `%s' as value of type `%s'",
                     pspec->name,
                     g_type_name (G_PARAM_SPEC_VALUE_TYPE (pspec)),
                     G_VALUE_TYPE_NAME (value));
          g_object_unref (child);
          g_object_unref (container);
          return;
        }
      else
        {
          g_value_init (&tmp_value, G_PARAM_SPEC_VALUE_TYPE (pspec));
          prop_value = &tmp_value;
        }
      container_get_child_property (container, child, pspec, prop_value);
      if (prop_value != value)
        {
          g_value_transform (prop_value, value);
          g_value_unset (&tmp_value);
        }
    }
  g_object_unref (child);
  g_object_unref (container);
}

/**
 * gtk_container_child_set_valist:
 * @container: a #GtkContainer
 * @child: a widget which is a child of @container
 * @first_property_name: the name of the first property to set
 * @var_args: a %NULL-terminated list of property names and values, starting
 *           with @first_prop_name
 *
 * Sets one or more child properties for @child and @container.
 **/
void
gtk_container_child_set_valist (GtkContainer *container,
                                GtkWidget    *child,
                                const gchar  *first_property_name,
                                va_list       var_args)
{
  GObjectNotifyQueue *nqueue;
  const gchar *name;

  g_return_if_fail (GTK_IS_CONTAINER (container));
  g_return_if_fail (GTK_IS_WIDGET (child));

  g_object_ref (container);
  g_object_ref (child);

  nqueue = g_object_notify_queue_freeze (G_OBJECT (child), _gtk_widget_child_property_notify_context);
  name = first_property_name;
  while (name)
    {
      GValue value = G_VALUE_INIT;
      gchar *error = NULL;
      GParamSpec *pspec = g_param_spec_pool_lookup (_gtk_widget_child_property_pool,
                                                    name,
                                                    G_OBJECT_TYPE (container),
                                                    TRUE);
      if (!pspec)
        {
          g_warning ("%s: container class `%s' has no child property named `%s'",
                     G_STRLOC,
                     G_OBJECT_TYPE_NAME (container),
                     name);
          break;
        }
      if (!(pspec->flags & G_PARAM_WRITABLE))
        {
          g_warning ("%s: child property `%s' of container class `%s' is not writable",
                     G_STRLOC,
                     pspec->name,
                     G_OBJECT_TYPE_NAME (container));
          break;
        }

      G_VALUE_COLLECT_INIT (&value, G_PARAM_SPEC_VALUE_TYPE (pspec),
                            var_args, 0, &error);
      if (error)
        {
          g_warning ("%s: %s", G_STRLOC, error);
          g_free (error);

          /* we purposely leak the value here, it might not be
           * in a sane state if an error condition occoured
           */
          break;
        }
      container_set_child_property (container, child, pspec, &value, nqueue);
      g_value_unset (&value);
      name = va_arg (var_args, gchar*);
    }
  g_object_notify_queue_thaw (G_OBJECT (child), nqueue);

  g_object_unref (container);
  g_object_unref (child);
}

/**
 * gtk_container_child_set_property:
 * @container: a #GtkContainer
 * @child: a widget which is a child of @container
 * @property_name: the name of the property to set
 * @value: the value to set the property to
 *
 * Sets a child property for @child and @container.
 **/
void
gtk_container_child_set_property (GtkContainer *container,
                                  GtkWidget    *child,
                                  const gchar  *property_name,
                                  const GValue *value)
{
  GObjectNotifyQueue *nqueue;
  GParamSpec *pspec;

  g_return_if_fail (GTK_IS_CONTAINER (container));
  g_return_if_fail (GTK_IS_WIDGET (child));
  g_return_if_fail (property_name != NULL);
  g_return_if_fail (G_IS_VALUE (value));

  g_object_ref (container);
  g_object_ref (child);

  nqueue = g_object_notify_queue_freeze (G_OBJECT (child), _gtk_widget_child_property_notify_context);
  pspec = g_param_spec_pool_lookup (_gtk_widget_child_property_pool, property_name,
                                    G_OBJECT_TYPE (container), TRUE);
  if (!pspec)
    g_warning ("%s: container class `%s' has no child property named `%s'",
               G_STRLOC,
               G_OBJECT_TYPE_NAME (container),
               property_name);
  else if (!(pspec->flags & G_PARAM_WRITABLE))
    g_warning ("%s: child property `%s' of container class `%s' is not writable",
               G_STRLOC,
               pspec->name,
               G_OBJECT_TYPE_NAME (container));
  else
    {
      container_set_child_property (container, child, pspec, value, nqueue);
    }
  g_object_notify_queue_thaw (G_OBJECT (child), nqueue);
  g_object_unref (container);
  g_object_unref (child);
}

/**
 * gtk_container_add_with_properties:
 * @container: a #GtkContainer
 * @widget: a widget to be placed inside @container
 * @first_prop_name: the name of the first child property to set
 * @...: a %NULL-terminated list of property names and values, starting
 *     with @first_prop_name
 *
 * Adds @widget to @container, setting child properties at the same time.
 * See gtk_container_add() and gtk_container_child_set() for more details.
 */
void
gtk_container_add_with_properties (GtkContainer *container,
                                   GtkWidget    *widget,
                                   const gchar  *first_prop_name,
                                   ...)
{
  g_return_if_fail (GTK_IS_CONTAINER (container));
  g_return_if_fail (GTK_IS_WIDGET (widget));
  g_return_if_fail (gtk_widget_get_parent (widget) == NULL);

  g_object_ref (container);
  g_object_ref (widget);
  gtk_widget_freeze_child_notify (widget);

  g_signal_emit (container, container_signals[ADD], 0, widget);
  if (gtk_widget_get_parent (widget))
    {
      va_list var_args;

      va_start (var_args, first_prop_name);
      gtk_container_child_set_valist (container, widget, first_prop_name, var_args);
      va_end (var_args);
    }

  gtk_widget_thaw_child_notify (widget);
  g_object_unref (widget);
  g_object_unref (container);
}

/**
 * gtk_container_child_set:
 * @container: a #GtkContainer
 * @child: a widget which is a child of @container
 * @first_prop_name: the name of the first property to set
 * @...: a %NULL-terminated list of property names and values, starting
 *     with @first_prop_name
 *
 * Sets one or more child properties for @child and @container.
 */
void
gtk_container_child_set (GtkContainer      *container,
                         GtkWidget         *child,
                         const gchar       *first_prop_name,
                         ...)
{
  va_list var_args;

  va_start (var_args, first_prop_name);
  gtk_container_child_set_valist (container, child, first_prop_name, var_args);
  va_end (var_args);
}

/**
 * gtk_container_child_get:
 * @container: a #GtkContainer
 * @child: a widget which is a child of @container
 * @first_prop_name: the name of the first property to get
 * @...: return location for the first property, followed
 *     optionally by more name/return location pairs, followed by %NULL
 *
 * Gets the values of one or more child properties for @child and @container.
 */
void
gtk_container_child_get (GtkContainer      *container,
                         GtkWidget         *child,
                         const gchar       *first_prop_name,
                         ...)
{
  va_list var_args;

  va_start (var_args, first_prop_name);
  gtk_container_child_get_valist (container, child, first_prop_name, var_args);
  va_end (var_args);
}

/**
 * gtk_container_class_install_child_property:
 * @cclass: a #GtkContainerClass
 * @property_id: the id for the property
 * @pspec: the #GParamSpec for the property
 *
 * Installs a child property on a container class.
 **/
void
gtk_container_class_install_child_property (GtkContainerClass *cclass,
                                            guint              property_id,
                                            GParamSpec        *pspec)
{
  g_return_if_fail (GTK_IS_CONTAINER_CLASS (cclass));
  g_return_if_fail (G_IS_PARAM_SPEC (pspec));
  if (pspec->flags & G_PARAM_WRITABLE)
    g_return_if_fail (cclass->set_child_property != NULL);
  if (pspec->flags & G_PARAM_READABLE)
    g_return_if_fail (cclass->get_child_property != NULL);
  g_return_if_fail (property_id > 0);
  g_return_if_fail (PARAM_SPEC_PARAM_ID (pspec) == 0);  /* paranoid */
  if (pspec->flags & (G_PARAM_CONSTRUCT | G_PARAM_CONSTRUCT_ONLY))
    g_return_if_fail ((pspec->flags & (G_PARAM_CONSTRUCT | G_PARAM_CONSTRUCT_ONLY)) == 0);

  if (g_param_spec_pool_lookup (_gtk_widget_child_property_pool, pspec->name, G_OBJECT_CLASS_TYPE (cclass), FALSE))
    {
      g_warning (G_STRLOC ": class `%s' already contains a child property named `%s'",
                 G_OBJECT_CLASS_NAME (cclass),
                 pspec->name);
      return;
    }
  g_param_spec_ref (pspec);
  g_param_spec_sink (pspec);
  PARAM_SPEC_SET_PARAM_ID (pspec, property_id);
  g_param_spec_pool_insert (_gtk_widget_child_property_pool, pspec, G_OBJECT_CLASS_TYPE (cclass));
}

/**
 * gtk_container_class_find_child_property:
 * @cclass: (type GtkContainerClass): a #GtkContainerClass
 * @property_name: the name of the child property to find
 *
 * Finds a child property of a container class by name.
 *
 * Returns: (transfer none): the #GParamSpec of the child property
 *     or %NULL if @class has no child property with that name.
 */
GParamSpec*
gtk_container_class_find_child_property (GObjectClass *cclass,
                                         const gchar  *property_name)
{
  g_return_val_if_fail (GTK_IS_CONTAINER_CLASS (cclass), NULL);
  g_return_val_if_fail (property_name != NULL, NULL);

  return g_param_spec_pool_lookup (_gtk_widget_child_property_pool,
                                   property_name,
                                   G_OBJECT_CLASS_TYPE (cclass),
                                   TRUE);
}

/**
 * gtk_container_class_list_child_properties:
 * @cclass: (type GtkContainerClass): a #GtkContainerClass
 * @n_properties: location to return the number of child properties found
 *
 * Returns all child properties of a container class.
 *
 * Returns: (array length=n_properties) (transfer container):
 *     a newly allocated %NULL-terminated array of #GParamSpec*.
 *     The array must be freed with g_free().
 */
GParamSpec**
gtk_container_class_list_child_properties (GObjectClass *cclass,
                                           guint        *n_properties)
{
  GParamSpec **pspecs;
  guint n;

  g_return_val_if_fail (GTK_IS_CONTAINER_CLASS (cclass), NULL);

  pspecs = g_param_spec_pool_list (_gtk_widget_child_property_pool,
                                   G_OBJECT_CLASS_TYPE (cclass),
                                   &n);
  if (n_properties)
    *n_properties = n;

  return pspecs;
}

static void
gtk_container_add_unimplemented (GtkContainer     *container,
                                 GtkWidget        *widget)
{
  g_warning ("GtkContainerClass::add not implemented for `%s'", g_type_name (G_TYPE_FROM_INSTANCE (container)));
}

static void
gtk_container_remove_unimplemented (GtkContainer     *container,
                                    GtkWidget        *widget)
{
  g_warning ("GtkContainerClass::remove not implemented for `%s'", g_type_name (G_TYPE_FROM_INSTANCE (container)));
}

static void
gtk_container_init (GtkContainer *container)
{
  GtkContainerPrivate *priv;

  container->priv = gtk_container_get_instance_private (container);
  priv = container->priv;

  priv->focus_child = NULL;
  priv->border_width = 0;
  priv->resize_mode = GTK_RESIZE_PARENT;
  priv->reallocate_redraws = FALSE;
  priv->border_width_set = FALSE;
}

static void
gtk_container_destroy (GtkWidget *widget)
{
  GtkContainer *container = GTK_CONTAINER (widget);
  GtkContainerPrivate *priv = container->priv;

  if (priv->resize_pending)
    _gtk_container_dequeue_resize_handler (container);

  if (priv->restyle_pending)
    priv->restyle_pending = FALSE;

  if (priv->focus_child)
    {
      g_object_unref (priv->focus_child);
      priv->focus_child = NULL;
    }

  /* do this before walking child widgets, to avoid
   * removing children from focus chain one by one.
   */
  if (priv->has_focus_chain)
    gtk_container_unset_focus_chain (container);

  gtk_container_foreach (container, (GtkCallback) gtk_widget_destroy, NULL);

  GTK_WIDGET_CLASS (parent_class)->destroy (widget);
}

static void
gtk_container_set_property (GObject         *object,
                            guint            prop_id,
                            const GValue    *value,
                            GParamSpec      *pspec)
{
  GtkContainer *container = GTK_CONTAINER (object);

  switch (prop_id)
    {
    case PROP_BORDER_WIDTH:
      gtk_container_set_border_width (container, g_value_get_uint (value));
      break;
    case PROP_RESIZE_MODE:
      G_GNUC_BEGIN_IGNORE_DEPRECATIONS;
      gtk_container_set_resize_mode (container, g_value_get_enum (value));
      G_GNUC_END_IGNORE_DEPRECATIONS;
      break;
    case PROP_CHILD:
      gtk_container_add (container, GTK_WIDGET (g_value_get_object (value)));
      break;
    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
      break;
    }
}

static void
gtk_container_get_property (GObject         *object,
                            guint            prop_id,
                            GValue          *value,
                            GParamSpec      *pspec)
{
  GtkContainer *container = GTK_CONTAINER (object);
  GtkContainerPrivate *priv = container->priv;

  switch (prop_id)
    {
    case PROP_BORDER_WIDTH:
      g_value_set_uint (value, priv->border_width);
      break;
    case PROP_RESIZE_MODE:
      g_value_set_enum (value, priv->resize_mode);
      break;
    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
      break;
    }
}

gboolean
_gtk_container_get_border_width_set (GtkContainer *container)
{
  GtkContainerPrivate *priv;

  g_return_val_if_fail (GTK_IS_CONTAINER (container), FALSE);

  priv = container->priv;

  return priv->border_width_set;
}

void
_gtk_container_set_border_width_set (GtkContainer *container,
                                     gboolean      border_width_set)
{
  GtkContainerPrivate *priv;

  g_return_if_fail (GTK_IS_CONTAINER (container));

  priv = container->priv;

  priv->border_width_set = border_width_set ? TRUE : FALSE;
}

/**
 * gtk_container_set_border_width:
 * @container: a #GtkContainer
 * @border_width: amount of blank space to leave outside
 *   the container. Valid values are in the range 0-65535 pixels.
 *
 * Sets the border width of the container.
 *
 * The border width of a container is the amount of space to leave
 * around the outside of the container. The only exception to this is
 * #GtkWindow; because toplevel windows can’t leave space outside,
 * they leave the space inside. The border is added on all sides of
 * the container. To add space to only one side, one approach is to
 * create a #GtkAlignment widget, call gtk_widget_set_size_request()
 * to give it a size, and place it on the side of the container as
 * a spacer.
 **/
void
gtk_container_set_border_width (GtkContainer *container,
                                guint         border_width)
{
  GtkContainerPrivate *priv;

  g_return_if_fail (GTK_IS_CONTAINER (container));

  priv = container->priv;

  if (priv->border_width != border_width)
    {
      priv->border_width = border_width;
      _gtk_container_set_border_width_set (container, TRUE);

      g_object_notify (G_OBJECT (container), "border-width");

      if (gtk_widget_get_realized (GTK_WIDGET (container)))
        gtk_widget_queue_resize (GTK_WIDGET (container));
    }
}

/**
 * gtk_container_get_border_width:
 * @container: a #GtkContainer
 *
 * Retrieves the border width of the container. See
 * gtk_container_set_border_width().
 *
 * Returns: the current border width
 **/
guint
gtk_container_get_border_width (GtkContainer *container)
{
  g_return_val_if_fail (GTK_IS_CONTAINER (container), 0);

  return container->priv->border_width;
}

/**
 * gtk_container_add:
 * @container: a #GtkContainer
 * @widget: a widget to be placed inside @container
 *
 * Adds @widget to @container. Typically used for simple containers
 * such as #GtkWindow, #GtkFrame, or #GtkButton; for more complicated
 * layout containers such as #GtkBox or #GtkGrid, this function will
 * pick default packing parameters that may not be correct.  So
 * consider functions such as gtk_box_pack_start() and
 * gtk_grid_attach() as an alternative to gtk_container_add() in
 * those cases. A widget may be added to only one container at a time;
 * you can’t place the same widget inside two different containers.
 *
 * Note that some containers, such as #GtkScrolledWindow or #GtkListBox,
 * may add intermediate children between the added widget and the
 * container.
 */
void
gtk_container_add (GtkContainer *container,
                   GtkWidget    *widget)
{
  GtkWidget *parent;

  g_return_if_fail (GTK_IS_CONTAINER (container));
  g_return_if_fail (GTK_IS_WIDGET (widget));

  parent = gtk_widget_get_parent (widget);

  if (parent != NULL)
    {
      g_warning ("Attempting to add a widget with type %s to a container of "
                 "type %s, but the widget is already inside a container of type %s, "
                 "please use gtk_widget_reparent()" ,
                 g_type_name (G_OBJECT_TYPE (widget)),
                 g_type_name (G_OBJECT_TYPE (container)),
                 g_type_name (G_OBJECT_TYPE (parent)));
      return;
    }

  g_signal_emit (container, container_signals[ADD], 0, widget);

  _gtk_container_accessible_add (GTK_WIDGET (container), widget);
}

/**
 * gtk_container_remove:
 * @container: a #GtkContainer
 * @widget: a current child of @container
 *
 * Removes @widget from @container. @widget must be inside @container.
 * Note that @container will own a reference to @widget, and that this
 * may be the last reference held; so removing a widget from its
 * container can destroy that widget. If you want to use @widget
 * again, you need to add a reference to it while it’s not inside
 * a container, using g_object_ref(). If you don’t want to use @widget
 * again it’s usually more efficient to simply destroy it directly
 * using gtk_widget_destroy() since this will remove it from the
 * container and help break any circular reference count cycles.
 **/
void
gtk_container_remove (GtkContainer *container,
                      GtkWidget    *widget)
{
  g_return_if_fail (GTK_IS_CONTAINER (container));
  g_return_if_fail (GTK_IS_WIDGET (widget));
  g_return_if_fail (gtk_widget_get_parent (widget) == GTK_WIDGET (container) || GTK_IS_ASSISTANT (container) || GTK_IS_ACTION_BAR (container));

  g_object_ref (container);
  g_object_ref (widget);

  g_signal_emit (container, container_signals[REMOVE], 0, widget);

  _gtk_container_accessible_remove (GTK_WIDGET (container), widget);

  g_object_unref (widget);
  g_object_unref (container);
}

void
_gtk_container_dequeue_resize_handler (GtkContainer *container)
{
  g_return_if_fail (GTK_IS_CONTAINER (container));
  g_return_if_fail (container->priv->resize_pending);

  container->priv->resize_pending = FALSE;
}

/**
 * gtk_container_set_resize_mode:
 * @container: a #GtkContainer
 * @resize_mode: the new resize mode
 *
 * Sets the resize mode for the container.
 *
 * The resize mode of a container determines whether a resize request
 * will be passed to the container’s parent, queued for later execution
 * or executed immediately.
 *
 * Deprecated: 3.12: Resize modes are deprecated. They aren’t necessary
 *     anymore since frame clocks and might introduce obscure bugs if
 *     used.
 **/
void
gtk_container_set_resize_mode (GtkContainer  *container,
                               GtkResizeMode  resize_mode)
{
  GtkContainerPrivate *priv;

  g_return_if_fail (GTK_IS_CONTAINER (container));
  g_return_if_fail (resize_mode <= GTK_RESIZE_IMMEDIATE);

  priv = container->priv;

  if (gtk_widget_is_toplevel (GTK_WIDGET (container)) &&
      resize_mode == GTK_RESIZE_PARENT)
    {
      resize_mode = GTK_RESIZE_QUEUE;
    }

  if (priv->resize_mode != resize_mode)
    {
      priv->resize_mode = resize_mode;

      gtk_widget_queue_resize (GTK_WIDGET (container));
      g_object_notify (G_OBJECT (container), "resize-mode");
    }
}

/**
 * gtk_container_get_resize_mode:
 * @container: a #GtkContainer
 *
 * Returns the resize mode for the container. See
 * gtk_container_set_resize_mode ().
 *
 * Returns: the current resize mode
 *
 * Deprecated: 3.12: Resize modes are deprecated. They aren’t necessary
 *     anymore since frame clocks and might introduce obscure bugs if
 *     used.
 **/
GtkResizeMode
gtk_container_get_resize_mode (GtkContainer *container)
{
  g_return_val_if_fail (GTK_IS_CONTAINER (container), GTK_RESIZE_PARENT);

  return container->priv->resize_mode;
}

/**
 * gtk_container_set_reallocate_redraws:
 * @container: a #GtkContainer
 * @needs_redraws: the new value for the container’s @reallocate_redraws flag
 *
 * Sets the @reallocate_redraws flag of the container to the given value.
 *
 * Containers requesting reallocation redraws get automatically
 * redrawn if any of their children changed allocation.
 **/
void
gtk_container_set_reallocate_redraws (GtkContainer *container,
                                      gboolean      needs_redraws)
{
  g_return_if_fail (GTK_IS_CONTAINER (container));

  container->priv->reallocate_redraws = needs_redraws ? TRUE : FALSE;
}

static void
gtk_container_idle_sizer (GdkFrameClock *clock,
			  GtkContainer  *container)
{
  /* We validate the style contexts in a single loop before even trying
   * to handle resizes instead of doing validations inline.
   * This is mostly necessary for compatibility reasons with old code,
   * because both style_updated and size_allocate functions often change
   * styles and so could cause infinite loops in this function.
   *
   * It's important to note that even an invalid style context returns
   * sane values. So the result of an invalid style context will never be
   * a program crash, but only a wrong layout or rendering.
   */
  if (container->priv->restyle_pending)
    {
      GtkBitmask *empty;
      gint64 current_time;

      empty = _gtk_bitmask_new ();
      current_time = g_get_monotonic_time ();

      container->priv->restyle_pending = FALSE;
      _gtk_style_context_validate (gtk_widget_get_style_context (GTK_WIDGET (container)),
                                   current_time,
                                   0,
                                   empty);

      _gtk_bitmask_free (empty);
    }

  /* we may be invoked with a container_resize_queue of NULL, because
   * queue_resize could have been adding an extra idle function while
   * the queue still got processed. we better just ignore such case
   * than trying to explicitly work around them with some extra flags,
   * since it doesn't cause any actual harm.
   */
  if (container->priv->resize_pending)
    {
      container->priv->resize_pending = FALSE;
      gtk_container_check_resize (container);
    }

  if (!container->priv->restyle_pending && !container->priv->resize_pending)
    {
      _gtk_container_stop_idle_sizer (container);
    }
  else
    {
      gdk_frame_clock_request_phase (clock,
                                     GDK_FRAME_CLOCK_PHASE_LAYOUT);
    }
}

static void
gtk_container_start_idle_sizer (GtkContainer *container)
{
  GdkFrameClock *clock;

  if (container->priv->resize_handler != 0)
    return;

  clock = gtk_widget_get_frame_clock (GTK_WIDGET (container));
  if (clock == NULL)
    return;

  container->priv->resize_clock = clock;
  container->priv->resize_handler = g_signal_connect (clock, "layout",
						      G_CALLBACK (gtk_container_idle_sizer), container);
  gdk_frame_clock_request_phase (clock,
                                 GDK_FRAME_CLOCK_PHASE_LAYOUT);
}

void
_gtk_container_stop_idle_sizer (GtkContainer *container)
{
  if (container->priv->resize_handler == 0)
    return;

  g_signal_handler_disconnect (container->priv->resize_clock,
                               container->priv->resize_handler);
  container->priv->resize_handler = 0;
  container->priv->resize_clock = NULL;
}

static void
gtk_container_queue_resize_handler (GtkContainer *container)
{
  GtkWidget *widget;

  G_GNUC_BEGIN_IGNORE_DEPRECATIONS;
  g_return_if_fail (GTK_IS_RESIZE_CONTAINER (container));
  G_GNUC_END_IGNORE_DEPRECATIONS;

  widget = GTK_WIDGET (container);

  if (gtk_widget_get_visible (widget) &&
      (gtk_widget_is_toplevel (widget) ||
       gtk_widget_get_realized (widget)))
    {
      switch (container->priv->resize_mode)
        {
        case GTK_RESIZE_QUEUE:
          if (!container->priv->resize_pending)
            {
              container->priv->resize_pending = TRUE;
              gtk_container_start_idle_sizer (container);
            }
          break;

        case GTK_RESIZE_IMMEDIATE:
          gtk_container_check_resize (container);
          break;

        case GTK_RESIZE_PARENT:
        default:
          g_assert_not_reached ();
          break;
        }
    }
}

static void
_gtk_container_queue_resize_internal (GtkContainer *container,
                                      gboolean      invalidate_only)
{
  GtkWidget *widget;

  g_return_if_fail (GTK_IS_CONTAINER (container));

  widget = GTK_WIDGET (container);

  do
    {
      _gtk_widget_set_alloc_needed (widget, TRUE);
      _gtk_size_request_cache_clear (_gtk_widget_peek_request_cache (widget));

      G_GNUC_BEGIN_IGNORE_DEPRECATIONS;
      if (GTK_IS_RESIZE_CONTAINER (widget))
        break;
      G_GNUC_END_IGNORE_DEPRECATIONS;

      widget = gtk_widget_get_parent (widget);
    }
  while (widget);

  if (widget && !invalidate_only)
    gtk_container_queue_resize_handler (GTK_CONTAINER (widget));
}

void
_gtk_container_queue_restyle (GtkContainer *container)
{
  GtkContainerPrivate *priv;

  g_return_if_fail (GTK_CONTAINER (container));

  priv = container->priv;

  if (priv->restyle_pending)
    return;

  gtk_container_start_idle_sizer (container);
  priv->restyle_pending = TRUE;
}

/**
 * _gtk_container_queue_resize:
 * @container: a #GtkContainer
 *
 * Determines the “resize container” in the hierarchy above this container
 * (typically the toplevel, but other containers can be set as resize
 * containers with gtk_container_set_resize_mode()), marks the container
 * and all parents up to and including the resize container as needing
 * to have sizes recomputed, and if necessary adds the resize container
 * to the queue of containers that will be resized out at idle.
 */
void
_gtk_container_queue_resize (GtkContainer *container)
{
  _gtk_container_queue_resize_internal (container, FALSE);
}

/**
 * _gtk_container_resize_invalidate:
 * @container: a #GtkContainer
 *
 * Invalidates cached sizes like _gtk_container_queue_resize() but doesn't
 * actually queue the resize container for resize.
 */
void
_gtk_container_resize_invalidate (GtkContainer *container)
{
  _gtk_container_queue_resize_internal (container, TRUE);
}

void
_gtk_container_maybe_start_idle_sizer (GtkContainer *container)
{
  if (container->priv->restyle_pending || container->priv->resize_pending)
    gtk_container_start_idle_sizer (container);
}

void
gtk_container_check_resize (GtkContainer *container)
{
  g_return_if_fail (GTK_IS_CONTAINER (container));

  g_signal_emit (container, container_signals[CHECK_RESIZE], 0);
}

static void
gtk_container_real_check_resize (GtkContainer *container)
{
  GtkWidget *widget = GTK_WIDGET (container);
  GtkAllocation allocation;
  GtkRequisition requisition;

  gtk_widget_get_preferred_size (widget,
                                 &requisition, NULL);
  gtk_widget_get_allocation (widget, &allocation);

  if (requisition.width > allocation.width ||
      requisition.height > allocation.height)
    {
      G_GNUC_BEGIN_IGNORE_DEPRECATIONS;
      if (GTK_IS_RESIZE_CONTAINER (container))
        {
          gtk_widget_size_allocate (widget, &allocation);
          gtk_widget_set_allocation (widget, &allocation);
        }
      else
        gtk_widget_queue_resize (widget);
      G_GNUC_END_IGNORE_DEPRECATIONS;
    }
  else
    {
      gtk_widget_size_allocate (widget, &allocation);
      gtk_widget_set_allocation (widget, &allocation);
    }
}

/* The container hasn't changed size but one of its children
 *  queued a resize request. Which means that the allocation
 *  is not sufficient for the requisition of some child.
 *  We’ve already performed a size request at this point,
 *  so we simply need to reallocate and let the allocation
 *  trickle down via GTK_WIDGET_ALLOC_NEEDED flags.
 */
/**
 * gtk_container_resize_children:
 * @container: a #GtkContainer
 *
 * Deprecated: 3.10
 **/
void
gtk_container_resize_children (GtkContainer *container)
{
  GtkAllocation allocation;
  GtkWidget *widget;

  /* resizing invariants:
   * toplevels have *always* resize_mode != GTK_RESIZE_PARENT set.
   * containers that have an idle sizer pending must be flagged with
   * RESIZE_PENDING.
   */
  g_return_if_fail (GTK_IS_CONTAINER (container));

  widget = GTK_WIDGET (container);
  gtk_widget_get_allocation (widget, &allocation);

  gtk_widget_size_allocate (widget, &allocation);
  gtk_widget_set_allocation (widget, &allocation);
}

static void
gtk_container_adjust_size_request (GtkWidget         *widget,
                                   GtkOrientation     orientation,
                                   gint              *minimum_size,
                                   gint              *natural_size)
{
  GtkContainer *container;

  container = GTK_CONTAINER (widget);

  if (GTK_CONTAINER_GET_CLASS (widget)->_handle_border_width)
    {
      int border_width;

      border_width = container->priv->border_width;

      *minimum_size += border_width * 2;
      *natural_size += border_width * 2;
    }

  /* chain up last so gtk_widget_set_size_request() values
   * will have a chance to overwrite our border width.
   */
  parent_class->adjust_size_request (widget, orientation,
                                     minimum_size, natural_size);
}

static void
gtk_container_adjust_baseline_request (GtkWidget         *widget,
				       gint              *minimum_baseline,
				       gint              *natural_baseline)
{
  GtkContainer *container;

  container = GTK_CONTAINER (widget);

  if (GTK_CONTAINER_GET_CLASS (widget)->_handle_border_width)
    {
      int border_width;

      border_width = container->priv->border_width;

      *minimum_baseline += border_width;
      *natural_baseline += border_width;
    }

  parent_class->adjust_baseline_request (widget, minimum_baseline, natural_baseline);
}

static void
gtk_container_adjust_size_allocation (GtkWidget         *widget,
                                      GtkOrientation     orientation,
                                      gint              *minimum_size,
                                      gint              *natural_size,
                                      gint              *allocated_pos,
                                      gint              *allocated_size)
{
  GtkContainer *container;
  int border_width;

  container = GTK_CONTAINER (widget);

  if (GTK_CONTAINER_GET_CLASS (widget)->_handle_border_width)
    {
      border_width = container->priv->border_width;

      *allocated_size -= border_width * 2;
      *allocated_pos += border_width;
      *minimum_size -= border_width * 2;
      *natural_size -= border_width * 2;
    }

  /* Chain up to GtkWidgetClass *after* removing our border width from
   * the proposed allocation size. This is because it's possible that the
   * widget was allocated more space than it needs in a said orientation,
   * if GtkWidgetClass does any alignments and thus limits the size to the
   * natural size... then we need that to be done *after* removing any margins
   * and padding values.
   */
  parent_class->adjust_size_allocation (widget, orientation,
                                        minimum_size, natural_size, allocated_pos,
                                        allocated_size);
}

static void
gtk_container_adjust_baseline_allocation (GtkWidget         *widget,
					  gint              *baseline)
{
  GtkContainer *container;
  int border_width;

  container = GTK_CONTAINER (widget);

  if (GTK_CONTAINER_GET_CLASS (widget)->_handle_border_width)
    {
      border_width = container->priv->border_width;

      if (*baseline >= 0)
	*baseline -= border_width;
    }

  parent_class->adjust_baseline_allocation (widget, baseline);
}


typedef struct {
  gint hfw;
  gint wfh;
} RequestModeCount;

static void
count_request_modes (GtkWidget        *widget,
		     RequestModeCount *count)
{
  GtkSizeRequestMode mode = gtk_widget_get_request_mode (widget);

  switch (mode)
    {
    case GTK_SIZE_REQUEST_HEIGHT_FOR_WIDTH:
      count->hfw++;
      break;
    case GTK_SIZE_REQUEST_WIDTH_FOR_HEIGHT:
      count->wfh++;
      break;
    case GTK_SIZE_REQUEST_CONSTANT_SIZE:
    default:
      break;
    }
}

static GtkSizeRequestMode 
gtk_container_get_request_mode (GtkWidget *widget)
{
  GtkContainer *container = GTK_CONTAINER (widget);
  RequestModeCount count = { 0, 0 };

  gtk_container_forall (container, (GtkCallback)count_request_modes, &count);

  if (!count.hfw && !count.wfh)
    return GTK_SIZE_REQUEST_CONSTANT_SIZE;
  else
    return count.wfh > count.hfw ? 
        GTK_SIZE_REQUEST_WIDTH_FOR_HEIGHT :
	GTK_SIZE_REQUEST_HEIGHT_FOR_WIDTH;
}

/**
 * gtk_container_class_handle_border_width:
 * @klass: the class struct of a #GtkContainer subclass
 *
 * Modifies a subclass of #GtkContainerClass to automatically add and
 * remove the border-width setting on GtkContainer.  This allows the
 * subclass to ignore the border width in its size request and
 * allocate methods. The intent is for a subclass to invoke this
 * in its class_init function.
 *
 * gtk_container_class_handle_border_width() is necessary because it
 * would break API too badly to make this behavior the default. So
 * subclasses must “opt in” to the parent class handling border_width
 * for them.
 */
void
gtk_container_class_handle_border_width (GtkContainerClass *klass)
{
  g_return_if_fail (GTK_IS_CONTAINER_CLASS (klass));

  klass->_handle_border_width = TRUE;
}

/**
 * gtk_container_forall: (virtual forall)
 * @container: a #GtkContainer
 * @callback: (scope call) (closure callback_data): a callback
 * @callback_data: callback user data
 *
 * Invokes @callback on each child of @container, including children
 * that are considered “internal” (implementation details of the
 * container). “Internal” children generally weren’t added by the user
 * of the container, but were added by the container implementation
 * itself.  Most applications should use gtk_container_foreach(),
 * rather than gtk_container_forall().
 **/
void
gtk_container_forall (GtkContainer *container,
                      GtkCallback   callback,
                      gpointer      callback_data)
{
  GtkContainerClass *class;

  g_return_if_fail (GTK_IS_CONTAINER (container));
  g_return_if_fail (callback != NULL);

  class = GTK_CONTAINER_GET_CLASS (container);

  if (class->forall)
    class->forall (container, TRUE, callback, callback_data);
}

/**
 * gtk_container_foreach:
 * @container: a #GtkContainer
 * @callback: (scope call):  a callback
 * @callback_data: callback user data
 *
 * Invokes @callback on each non-internal child of @container. See
 * gtk_container_forall() for details on what constitutes an
 * “internal” child.  Most applications should use
 * gtk_container_foreach(), rather than gtk_container_forall().
 **/
void
gtk_container_foreach (GtkContainer *container,
                       GtkCallback   callback,
                       gpointer      callback_data)
{
  GtkContainerClass *class;

  g_return_if_fail (GTK_IS_CONTAINER (container));
  g_return_if_fail (callback != NULL);

  class = GTK_CONTAINER_GET_CLASS (container);

  if (class->forall)
    class->forall (container, FALSE, callback, callback_data);
}

/**
 * gtk_container_set_focus_child:
 * @container: a #GtkContainer
 * @child: (allow-none): a #GtkWidget, or %NULL
 *
 * Sets, or unsets if @child is %NULL, the focused child of @container.
 *
 * This function emits the GtkContainer::set_focus_child signal of
 * @container. Implementations of #GtkContainer can override the
 * default behaviour by overriding the class closure of this signal.
 *
 * This is function is mostly meant to be used by widgets. Applications can use
 * gtk_widget_grab_focus() to manualy set the focus to a specific widget.
 */
void
gtk_container_set_focus_child (GtkContainer *container,
                               GtkWidget    *child)
{
  g_return_if_fail (GTK_IS_CONTAINER (container));
  if (child)
    g_return_if_fail (GTK_IS_WIDGET (child));

  g_signal_emit (container, container_signals[SET_FOCUS_CHILD], 0, child);
}

/**
 * gtk_container_get_focus_child:
 * @container: a #GtkContainer
 *
 * Returns the current focus child widget inside @container. This is not the
 * currently focused widget. That can be obtained by calling
 * gtk_window_get_focus().
 *
 * Returns: (transfer none): The child widget which will receive the
 *          focus inside @container when the @conatiner is focussed,
 *          or %NULL if none is set.
 *
 * Since: 2.14
 **/
GtkWidget *
gtk_container_get_focus_child (GtkContainer *container)
{
  g_return_val_if_fail (GTK_IS_CONTAINER (container), NULL);

  return container->priv->focus_child;
}

/**
 * gtk_container_get_children:
 * @container: a #GtkContainer
 *
 * Returns the container’s non-internal children. See
 * gtk_container_forall() for details on what constitutes an "internal" child.
 *
 * Returns: (element-type GtkWidget) (transfer container): a newly-allocated list of the container’s non-internal children.
 **/
GList*
gtk_container_get_children (GtkContainer *container)
{
  GList *children = NULL;

  gtk_container_foreach (container,
                         gtk_container_children_callback,
                         &children);

  return g_list_reverse (children);
}

static void
gtk_container_child_position_callback (GtkWidget *widget,
                                       gpointer   client_data)
{
  struct {
    GtkWidget *child;
    guint i;
    guint index;
  } *data = client_data;

  data->i++;
  if (data->child == widget)
    data->index = data->i;
}

static gchar*
gtk_container_child_default_composite_name (GtkContainer *container,
                                            GtkWidget    *child)
{
  struct {
    GtkWidget *child;
    guint i;
    guint index;
  } data;
  gchar *name;

  /* fallback implementation */
  data.child = child;
  data.i = 0;
  data.index = 0;
  gtk_container_forall (container,
                        gtk_container_child_position_callback,
                        &data);

  name = g_strdup_printf ("%s-%u",
                          g_type_name (G_TYPE_FROM_INSTANCE (child)),
                          data.index);

  return name;
}

gchar*
_gtk_container_child_composite_name (GtkContainer *container,
                                    GtkWidget    *child)
{
  gboolean composite_child;

  g_return_val_if_fail (GTK_IS_CONTAINER (container), NULL);
  g_return_val_if_fail (GTK_IS_WIDGET (child), NULL);
  g_return_val_if_fail (gtk_widget_get_parent (child) == GTK_WIDGET (container), NULL);

  g_object_get (child, "composite-child", &composite_child, NULL);
  if (composite_child)
    {
      static GQuark quark_composite_name = 0;
      gchar *name;

      if (!quark_composite_name)
        quark_composite_name = g_quark_from_static_string ("gtk-composite-name");

      name = g_object_get_qdata (G_OBJECT (child), quark_composite_name);
      if (!name)
        {
          GtkContainerClass *class;

          class = GTK_CONTAINER_GET_CLASS (container);
          if (class->composite_name)
            name = class->composite_name (container, child);
        }
      else
        name = g_strdup (name);

      return name;
    }

  return NULL;
}

typedef struct {
  gboolean hexpand;
  gboolean vexpand;
} ComputeExpandData;

static void
gtk_container_compute_expand_callback (GtkWidget *widget,
                                       gpointer   client_data)
{
  ComputeExpandData *data = client_data;

  /* note that we don't get_expand on the child if we already know we
   * have to expand, so we only recurse into children until we find
   * one that expands and then we basically don't do any more
   * work. This means that we can leave some children in a
   * need_compute_expand state, which is fine, as long as GtkWidget
   * doesn't rely on an invariant that "if a child has
   * need_compute_expand, its parents also do"
   *
   * gtk_widget_compute_expand() always returns FALSE if the
   * child is !visible so that's taken care of.
   */
  data->hexpand = data->hexpand ||
    gtk_widget_compute_expand (widget, GTK_ORIENTATION_HORIZONTAL);

  data->vexpand = data->vexpand ||
    gtk_widget_compute_expand (widget, GTK_ORIENTATION_VERTICAL);
}

static void
gtk_container_compute_expand (GtkWidget         *widget,
                              gboolean          *hexpand_p,
                              gboolean          *vexpand_p)
{
  ComputeExpandData data;

  data.hexpand = FALSE;
  data.vexpand = FALSE;

  gtk_container_forall (GTK_CONTAINER (widget),
                        gtk_container_compute_expand_callback,
                        &data);

  *hexpand_p = data.hexpand;
  *vexpand_p = data.vexpand;
}

static void
gtk_container_real_set_focus_child (GtkContainer     *container,
                                    GtkWidget        *child)
{
  GtkContainerPrivate *priv;

  g_return_if_fail (GTK_IS_CONTAINER (container));
  g_return_if_fail (child == NULL || GTK_IS_WIDGET (child));

  priv = container->priv;

  if (child != priv->focus_child)
    {
      if (priv->focus_child)
        g_object_unref (priv->focus_child);
      priv->focus_child = child;
      if (priv->focus_child)
        g_object_ref (priv->focus_child);
    }


  /* check for h/v adjustments
   */
  if (priv->focus_child)
    {
      GtkAdjustment *hadj;
      GtkAdjustment *vadj;
      GtkAllocation allocation;
      GtkWidget *focus_child;
      gint x, y;

      hadj = g_object_get_qdata (G_OBJECT (container), hadjustment_key_id);
      vadj = g_object_get_qdata (G_OBJECT (container), vadjustment_key_id);
      if (hadj || vadj)
        {

          focus_child = priv->focus_child;
          while (GTK_IS_CONTAINER (focus_child) && gtk_container_get_focus_child (GTK_CONTAINER (focus_child)))
            {
              focus_child = gtk_container_get_focus_child (GTK_CONTAINER (focus_child));
            }

          gtk_widget_translate_coordinates (focus_child, priv->focus_child,
                                            0, 0, &x, &y);

          gtk_widget_get_allocation (priv->focus_child, &allocation);
          x += allocation.x;
          y += allocation.y;

          gtk_widget_get_allocation (focus_child, &allocation);

          if (vadj)
            gtk_adjustment_clamp_page (vadj, y, y + allocation.height);

          if (hadj)
            gtk_adjustment_clamp_page (hadj, x, x + allocation.width);
        }
    }
}

static GList*
get_focus_chain (GtkContainer *container)
{
  return g_object_get_data (G_OBJECT (container), "gtk-container-focus-chain");
}

/* same as gtk_container_get_children, except it includes internals
 */
GList *
_gtk_container_get_all_children (GtkContainer *container)
{
  GList *children = NULL;

  gtk_container_forall (container,
                         gtk_container_children_callback,
                         &children);

  return children;
}

static GtkWidgetPath *
gtk_container_real_get_path_for_child (GtkContainer *container,
                                       GtkWidget    *child)
{
  GtkStyleContext *context;
  GtkWidgetPath *path;
  GList *classes;

  context = gtk_widget_get_style_context (GTK_WIDGET (container));
  path = _gtk_widget_create_path (GTK_WIDGET (container));

  /* Copy any permanent classes to the path */
  classes = gtk_style_context_list_classes (context);

  while (classes)
    {
      GList *cur;

      cur = classes;
      classes = classes->next;

      gtk_widget_path_iter_add_class (path, -1, cur->data);
      g_list_free_1 (cur);
    }

  gtk_widget_path_append_for_widget (path, child);

  return path;
}

static gboolean
gtk_container_focus (GtkWidget        *widget,
                     GtkDirectionType  direction)
{
  GList *children;
  GList *sorted_children;
  gint return_val;
  GtkContainer *container;
  GtkContainerPrivate *priv;

  g_return_val_if_fail (GTK_IS_CONTAINER (widget), FALSE);

  container = GTK_CONTAINER (widget);
  priv = container->priv;

  return_val = FALSE;

  if (gtk_widget_get_can_focus (widget))
    {
      if (!gtk_widget_has_focus (widget))
        {
          gtk_widget_grab_focus (widget);
          return_val = TRUE;
        }
    }
  else
    {
      /* Get a list of the containers children, allowing focus
       * chain to override.
       */
      if (priv->has_focus_chain)
        children = g_list_copy (get_focus_chain (container));
      else
        children = _gtk_container_get_all_children (container);

      if (priv->has_focus_chain &&
          (direction == GTK_DIR_TAB_FORWARD ||
           direction == GTK_DIR_TAB_BACKWARD))
        {
          sorted_children = g_list_copy (children);

          if (direction == GTK_DIR_TAB_BACKWARD)
            sorted_children = g_list_reverse (sorted_children);
        }
      else
        sorted_children = _gtk_container_focus_sort (container, children, direction, NULL);

      return_val = gtk_container_focus_move (container, sorted_children, direction);

      g_list_free (sorted_children);
      g_list_free (children);
    }

  return return_val;
}

static gint
tab_compare (gconstpointer a,
             gconstpointer b,
             gpointer      data)
{
  GtkAllocation child1_allocation, child2_allocation;
  const GtkWidget *child1 = a;
  const GtkWidget *child2 = b;
  GtkTextDirection text_direction = GPOINTER_TO_INT (data);
  gint y1, y2;

  gtk_widget_get_allocation ((GtkWidget *) child1, &child1_allocation);
  gtk_widget_get_allocation ((GtkWidget *) child2, &child2_allocation);

  y1 = child1_allocation.y + child1_allocation.height / 2;
  y2 = child2_allocation.y + child2_allocation.height / 2;

  if (y1 == y2)
    {
      gint x1 = child1_allocation.x + child1_allocation.width / 2;
      gint x2 = child2_allocation.x + child2_allocation.width / 2;

      if (text_direction == GTK_TEXT_DIR_RTL)
        return (x1 < x2) ? 1 : ((x1 == x2) ? 0 : -1);
      else
        return (x1 < x2) ? -1 : ((x1 == x2) ? 0 : 1);
    }
  else
    return (y1 < y2) ? -1 : 1;
}

static GList *
gtk_container_focus_sort_tab (GtkContainer     *container,
                              GList            *children,
                              GtkDirectionType  direction,
                              GtkWidget        *old_focus)
{
  GtkTextDirection text_direction = gtk_widget_get_direction (GTK_WIDGET (container));
  children = g_list_sort_with_data (children, tab_compare, GINT_TO_POINTER (text_direction));

  /* if we are going backwards then reverse the order
   *  of the children.
   */
  if (direction == GTK_DIR_TAB_BACKWARD)
    children = g_list_reverse (children);

  return children;
}

/* Get coordinates of @widget's allocation with respect to
 * allocation of @container.
 */
static gboolean
get_allocation_coords (GtkContainer  *container,
                       GtkWidget     *widget,
                       GdkRectangle  *allocation)
{
  gtk_widget_get_allocation (widget, allocation);

  return gtk_widget_translate_coordinates (widget, GTK_WIDGET (container),
                                           0, 0, &allocation->x, &allocation->y);
}

/* Look for a child in @children that is intermediate between
 * the focus widget and container. This widget, if it exists,
 * acts as the starting widget for focus navigation.
 */
static GtkWidget *
find_old_focus (GtkContainer *container,
                GList        *children)
{
  GList *tmp_list = children;
  while (tmp_list)
    {
      GtkWidget *child = tmp_list->data;
      GtkWidget *widget = child;

      while (widget && widget != (GtkWidget *)container)
        {
          GtkWidget *parent;

          parent = gtk_widget_get_parent (widget);

          if (parent && (gtk_container_get_focus_child (GTK_CONTAINER (parent)) != widget))
            goto next;

          widget = parent;
        }

      return child;

    next:
      tmp_list = tmp_list->next;
    }

  return NULL;
}

static gboolean
old_focus_coords (GtkContainer *container,
                  GdkRectangle *old_focus_rect)
{
  GtkWidget *widget = GTK_WIDGET (container);
  GtkWidget *toplevel = gtk_widget_get_toplevel (widget);
  GtkWidget *old_focus;

  if (GTK_IS_WINDOW (toplevel))
    {
      old_focus = gtk_window_get_focus (GTK_WINDOW (toplevel));
      if (old_focus)
        return get_allocation_coords (container, old_focus, old_focus_rect);
    }

  return FALSE;
}

typedef struct _CompareInfo CompareInfo;

struct _CompareInfo
{
  GtkContainer *container;
  gint x;
  gint y;
  gboolean reverse;
};

static gint
up_down_compare (gconstpointer a,
                 gconstpointer b,
                 gpointer      data)
{
  GdkRectangle allocation1;
  GdkRectangle allocation2;
  CompareInfo *compare = data;
  gint y1, y2;

  get_allocation_coords (compare->container, (GtkWidget *)a, &allocation1);
  get_allocation_coords (compare->container, (GtkWidget *)b, &allocation2);

  y1 = allocation1.y + allocation1.height / 2;
  y2 = allocation2.y + allocation2.height / 2;

  if (y1 == y2)
    {
      gint x1 = abs (allocation1.x + allocation1.width / 2 - compare->x);
      gint x2 = abs (allocation2.x + allocation2.width / 2 - compare->x);

      if (compare->reverse)
        return (x1 < x2) ? 1 : ((x1 == x2) ? 0 : -1);
      else
        return (x1 < x2) ? -1 : ((x1 == x2) ? 0 : 1);
    }
  else
    return (y1 < y2) ? -1 : 1;
}

static GList *
gtk_container_focus_sort_up_down (GtkContainer     *container,
                                  GList            *children,
                                  GtkDirectionType  direction,
                                  GtkWidget        *old_focus)
{
  CompareInfo compare;
  GList *tmp_list;
  GdkRectangle old_allocation;

  compare.container = container;
  compare.reverse = (direction == GTK_DIR_UP);

  if (!old_focus)
      old_focus = find_old_focus (container, children);

  if (old_focus && get_allocation_coords (container, old_focus, &old_allocation))
    {
      gint compare_x1;
      gint compare_x2;
      gint compare_y;

      /* Delete widgets from list that don't match minimum criteria */

      compare_x1 = old_allocation.x;
      compare_x2 = old_allocation.x + old_allocation.width;

      if (direction == GTK_DIR_UP)
        compare_y = old_allocation.y;
      else
        compare_y = old_allocation.y + old_allocation.height;

      tmp_list = children;
      while (tmp_list)
        {
          GtkWidget *child = tmp_list->data;
          GList *next = tmp_list->next;
          gint child_x1, child_x2;
          GdkRectangle child_allocation;

          if (child != old_focus)
            {
              if (get_allocation_coords (container, child, &child_allocation))
                {
                  child_x1 = child_allocation.x;
                  child_x2 = child_allocation.x + child_allocation.width;

                  if ((child_x2 <= compare_x1 || child_x1 >= compare_x2) /* No horizontal overlap */ ||
                      (direction == GTK_DIR_DOWN && child_allocation.y + child_allocation.height < compare_y) || /* Not below */
                      (direction == GTK_DIR_UP && child_allocation.y > compare_y)) /* Not above */
                    {
                      children = g_list_delete_link (children, tmp_list);
                    }
                }
              else
                children = g_list_delete_link (children, tmp_list);
            }

          tmp_list = next;
        }

      compare.x = (compare_x1 + compare_x2) / 2;
      compare.y = old_allocation.y + old_allocation.height / 2;
    }
  else
    {
      /* No old focus widget, need to figure out starting x,y some other way
       */
      GtkAllocation allocation;
      GtkWidget *widget = GTK_WIDGET (container);
      GdkRectangle old_focus_rect;

      gtk_widget_get_allocation (widget, &allocation);

      if (old_focus_coords (container, &old_focus_rect))
        {
          compare.x = old_focus_rect.x + old_focus_rect.width / 2;
        }
      else
        {
          if (!gtk_widget_get_has_window (widget))
            compare.x = allocation.x + allocation.width / 2;
          else
            compare.x = allocation.width / 2;
        }

      if (!gtk_widget_get_has_window (widget))
        compare.y = (direction == GTK_DIR_DOWN) ? allocation.y : allocation.y + allocation.height;
      else
        compare.y = (direction == GTK_DIR_DOWN) ? 0 : + allocation.height;
    }

  children = g_list_sort_with_data (children, up_down_compare, &compare);

  if (compare.reverse)
    children = g_list_reverse (children);

  return children;
}

static gint
left_right_compare (gconstpointer a,
                    gconstpointer b,
                    gpointer      data)
{
  GdkRectangle allocation1;
  GdkRectangle allocation2;
  CompareInfo *compare = data;
  gint x1, x2;

  get_allocation_coords (compare->container, (GtkWidget *)a, &allocation1);
  get_allocation_coords (compare->container, (GtkWidget *)b, &allocation2);

  x1 = allocation1.x + allocation1.width / 2;
  x2 = allocation2.x + allocation2.width / 2;

  if (x1 == x2)
    {
      gint y1 = abs (allocation1.y + allocation1.height / 2 - compare->y);
      gint y2 = abs (allocation2.y + allocation2.height / 2 - compare->y);

      if (compare->reverse)
        return (y1 < y2) ? 1 : ((y1 == y2) ? 0 : -1);
      else
        return (y1 < y2) ? -1 : ((y1 == y2) ? 0 : 1);
    }
  else
    return (x1 < x2) ? -1 : 1;
}

static GList *
gtk_container_focus_sort_left_right (GtkContainer     *container,
                                     GList            *children,
                                     GtkDirectionType  direction,
                                     GtkWidget        *old_focus)
{
  CompareInfo compare;
  GList *tmp_list;
  GdkRectangle old_allocation;

  compare.container = container;
  compare.reverse = (direction == GTK_DIR_LEFT);

  if (!old_focus)
    old_focus = find_old_focus (container, children);

  if (old_focus && get_allocation_coords (container, old_focus, &old_allocation))
    {
      gint compare_y1;
      gint compare_y2;
      gint compare_x;

      /* Delete widgets from list that don't match minimum criteria */

      compare_y1 = old_allocation.y;
      compare_y2 = old_allocation.y + old_allocation.height;

      if (direction == GTK_DIR_LEFT)
        compare_x = old_allocation.x;
      else
        compare_x = old_allocation.x + old_allocation.width;

      tmp_list = children;
      while (tmp_list)
        {
          GtkWidget *child = tmp_list->data;
          GList *next = tmp_list->next;
          gint child_y1, child_y2;
          GdkRectangle child_allocation;

          if (child != old_focus)
            {
              if (get_allocation_coords (container, child, &child_allocation))
                {
                  child_y1 = child_allocation.y;
                  child_y2 = child_allocation.y + child_allocation.height;

                  if ((child_y2 <= compare_y1 || child_y1 >= compare_y2) /* No vertical overlap */ ||
                      (direction == GTK_DIR_RIGHT && child_allocation.x + child_allocation.width < compare_x) || /* Not to left */
                      (direction == GTK_DIR_LEFT && child_allocation.x > compare_x)) /* Not to right */
                    {
                      children = g_list_delete_link (children, tmp_list);
                    }
                }
              else
                children = g_list_delete_link (children, tmp_list);
            }

          tmp_list = next;
        }

      compare.y = (compare_y1 + compare_y2) / 2;
      compare.x = old_allocation.x + old_allocation.width / 2;
    }
  else
    {
      /* No old focus widget, need to figure out starting x,y some other way
       */
      GtkAllocation allocation;
      GtkWidget *widget = GTK_WIDGET (container);
      GdkRectangle old_focus_rect;

      gtk_widget_get_allocation (widget, &allocation);

      if (old_focus_coords (container, &old_focus_rect))
        {
          compare.y = old_focus_rect.y + old_focus_rect.height / 2;
        }
      else
        {
          if (!gtk_widget_get_has_window (widget))
            compare.y = allocation.y + allocation.height / 2;
          else
            compare.y = allocation.height / 2;
        }

      if (!gtk_widget_get_has_window (widget))
        compare.x = (direction == GTK_DIR_RIGHT) ? allocation.x : allocation.x + allocation.width;
      else
        compare.x = (direction == GTK_DIR_RIGHT) ? 0 : allocation.width;
    }

  children = g_list_sort_with_data (children, left_right_compare, &compare);

  if (compare.reverse)
    children = g_list_reverse (children);

  return children;
}

/**
 * gtk_container_focus_sort:
 * @container: a #GtkContainer
 * @children:  a list of descendents of @container (they don't
 *             have to be direct children)
 * @direction: focus direction
 * @old_focus: (allow-none): widget to use for the starting position, or %NULL
 *             to determine this automatically.
 *             (Note, this argument isn’t used for GTK_DIR_TAB_*,
 *              which is the only @direction we use currently,
 *              so perhaps this argument should be removed)
 *
 * Sorts @children in the correct order for focusing with
 * direction type @direction.
 *
 * Returns: a copy of @children, sorted in correct focusing order,
 *   with children that aren’t suitable for focusing in this direction
 *   removed.
 **/
GList *
_gtk_container_focus_sort (GtkContainer     *container,
                           GList            *children,
                           GtkDirectionType  direction,
                           GtkWidget        *old_focus)
{
  GList *visible_children = NULL;

  while (children)
    {
      if (gtk_widget_get_realized (children->data))
        visible_children = g_list_prepend (visible_children, children->data);
      children = children->next;
    }

  switch (direction)
    {
    case GTK_DIR_TAB_FORWARD:
    case GTK_DIR_TAB_BACKWARD:
      return gtk_container_focus_sort_tab (container, visible_children, direction, old_focus);
    case GTK_DIR_UP:
    case GTK_DIR_DOWN:
      return gtk_container_focus_sort_up_down (container, visible_children, direction, old_focus);
    case GTK_DIR_LEFT:
    case GTK_DIR_RIGHT:
      return gtk_container_focus_sort_left_right (container, visible_children, direction, old_focus);
    }

  g_assert_not_reached ();

  return NULL;
}

static gboolean
gtk_container_focus_move (GtkContainer     *container,
                          GList            *children,
                          GtkDirectionType  direction)
{
  GtkContainerPrivate *priv = container->priv;
  GtkWidget *focus_child;
  GtkWidget *child;

  focus_child = priv->focus_child;

  while (children)
    {
      child = children->data;
      children = children->next;

      if (!child)
        continue;

      if (focus_child)
        {
          if (focus_child == child)
            {
              focus_child = NULL;

                if (gtk_widget_child_focus (child, direction))
                  return TRUE;
            }
        }
      else if (gtk_widget_is_drawable (child) &&
               gtk_widget_is_ancestor (child, GTK_WIDGET (container)))
        {
          if (gtk_widget_child_focus (child, direction))
            return TRUE;
        }
    }

  return FALSE;
}


static void
gtk_container_children_callback (GtkWidget *widget,
                                 gpointer   client_data)
{
  GList **children;

  children = (GList**) client_data;
  *children = g_list_prepend (*children, widget);
}

static void
chain_widget_destroyed (GtkWidget *widget,
                        gpointer   user_data)
{
  GtkContainer *container;
  GList *chain;

  container = GTK_CONTAINER (user_data);

  chain = g_object_get_data (G_OBJECT (container),
                             "gtk-container-focus-chain");

  chain = g_list_remove (chain, widget);

  g_signal_handlers_disconnect_by_func (widget,
                                        chain_widget_destroyed,
                                        user_data);

  g_object_set_data (G_OBJECT (container),
                     I_("gtk-container-focus-chain"),
                     chain);
}

/**
 * gtk_container_set_focus_chain:
 * @container: a #GtkContainer
 * @focusable_widgets: (transfer none) (element-type GtkWidget):
 *     the new focus chain
 *
 * Sets a focus chain, overriding the one computed automatically by GTK+.
 *
 * In principle each widget in the chain should be a descendant of the
 * container, but this is not enforced by this method, since it’s allowed
 * to set the focus chain before you pack the widgets, or have a widget
 * in the chain that isn’t always packed. The necessary checks are done
 * when the focus chain is actually traversed.
 **/
void
gtk_container_set_focus_chain (GtkContainer *container,
                               GList        *focusable_widgets)
{
  GList *chain;
  GList *tmp_list;
  GtkContainerPrivate *priv;

  g_return_if_fail (GTK_IS_CONTAINER (container));

  priv = container->priv;

  if (priv->has_focus_chain)
    gtk_container_unset_focus_chain (container);

  priv->has_focus_chain = TRUE;

  chain = NULL;
  tmp_list = focusable_widgets;
  while (tmp_list != NULL)
    {
      g_return_if_fail (GTK_IS_WIDGET (tmp_list->data));

      /* In principle each widget in the chain should be a descendant
       * of the container, but we don't want to check that here. It's
       * expensive and also it's allowed to set the focus chain before
       * you pack the widgets, or have a widget in the chain that isn't
       * always packed. So we check for ancestor during actual traversal.
       */

      chain = g_list_prepend (chain, tmp_list->data);

      g_signal_connect (tmp_list->data,
                        "destroy",
                        G_CALLBACK (chain_widget_destroyed),
                        container);

      tmp_list = g_list_next (tmp_list);
    }

  chain = g_list_reverse (chain);

  g_object_set_data (G_OBJECT (container),
                     I_("gtk-container-focus-chain"),
                     chain);
}

/**
 * gtk_container_get_focus_chain:
 * @container:         a #GtkContainer
 * @focusable_widgets: (element-type GtkWidget) (out) (transfer container): location
 *                     to store the focus chain of the
 *                     container, or %NULL. You should free this list
 *                     using g_list_free() when you are done with it, however
 *                     no additional reference count is added to the
 *                     individual widgets in the focus chain.
 *
 * Retrieves the focus chain of the container, if one has been
 * set explicitly. If no focus chain has been explicitly
 * set, GTK+ computes the focus chain based on the positions
 * of the children. In that case, GTK+ stores %NULL in
 * @focusable_widgets and returns %FALSE.
 *
 * Returns: %TRUE if the focus chain of the container
 * has been set explicitly.
 **/
gboolean
gtk_container_get_focus_chain (GtkContainer *container,
                               GList       **focus_chain)
{
  GtkContainerPrivate *priv;

  g_return_val_if_fail (GTK_IS_CONTAINER (container), FALSE);

  priv = container->priv;

  if (focus_chain)
    {
      if (priv->has_focus_chain)
        *focus_chain = g_list_copy (get_focus_chain (container));
      else
        *focus_chain = NULL;
    }

  return priv->has_focus_chain;
}

/**
 * gtk_container_unset_focus_chain:
 * @container: a #GtkContainer
 *
 * Removes a focus chain explicitly set with gtk_container_set_focus_chain().
 **/
void
gtk_container_unset_focus_chain (GtkContainer  *container)
{
  GtkContainerPrivate *priv;

  g_return_if_fail (GTK_IS_CONTAINER (container));

  priv = container->priv;

  if (priv->has_focus_chain)
    {
      GList *chain;
      GList *tmp_list;

      chain = get_focus_chain (container);

      priv->has_focus_chain = FALSE;

      g_object_set_data (G_OBJECT (container),
                         I_("gtk-container-focus-chain"),
                         NULL);

      tmp_list = chain;
      while (tmp_list != NULL)
        {
          g_signal_handlers_disconnect_by_func (tmp_list->data,
                                                chain_widget_destroyed,
                                                container);

          tmp_list = g_list_next (tmp_list);
        }

      g_list_free (chain);
    }
}

/**
 * gtk_container_set_focus_vadjustment:
 * @container: a #GtkContainer
 * @adjustment: an adjustment which should be adjusted when the focus
 *   is moved among the descendents of @container
 *
 * Hooks up an adjustment to focus handling in a container, so when a
 * child of the container is focused, the adjustment is scrolled to
 * show that widget. This function sets the vertical alignment. See
 * gtk_scrolled_window_get_vadjustment() for a typical way of obtaining
 * the adjustment and gtk_container_set_focus_hadjustment() for setting
 * the horizontal adjustment.
 *
 * The adjustments have to be in pixel units and in the same coordinate
 * system as the allocation for immediate children of the container.
 */
void
gtk_container_set_focus_vadjustment (GtkContainer  *container,
                                     GtkAdjustment *adjustment)
{
  g_return_if_fail (GTK_IS_CONTAINER (container));
  if (adjustment)
    g_return_if_fail (GTK_IS_ADJUSTMENT (adjustment));

  if (adjustment)
    g_object_ref (adjustment);

  g_object_set_qdata_full (G_OBJECT (container),
                           vadjustment_key_id,
                           adjustment,
                           g_object_unref);
}

/**
 * gtk_container_get_focus_vadjustment:
 * @container: a #GtkContainer
 *
 * Retrieves the vertical focus adjustment for the container. See
 * gtk_container_set_focus_vadjustment().
 *
 * Returns: (transfer none): the vertical focus adjustment, or %NULL if
 *   none has been set.
 **/
GtkAdjustment *
gtk_container_get_focus_vadjustment (GtkContainer *container)
{
  GtkAdjustment *vadjustment;

  g_return_val_if_fail (GTK_IS_CONTAINER (container), NULL);

  vadjustment = g_object_get_qdata (G_OBJECT (container), vadjustment_key_id);

  return vadjustment;
}

/**
 * gtk_container_set_focus_hadjustment:
 * @container: a #GtkContainer
 * @adjustment: an adjustment which should be adjusted when the focus is
 *   moved among the descendents of @container
 *
 * Hooks up an adjustment to focus handling in a container, so when a child
 * of the container is focused, the adjustment is scrolled to show that
 * widget. This function sets the horizontal alignment.
 * See gtk_scrolled_window_get_hadjustment() for a typical way of obtaining
 * the adjustment and gtk_container_set_focus_vadjustment() for setting
 * the vertical adjustment.
 *
 * The adjustments have to be in pixel units and in the same coordinate
 * system as the allocation for immediate children of the container.
 */
void
gtk_container_set_focus_hadjustment (GtkContainer  *container,
                                     GtkAdjustment *adjustment)
{
  g_return_if_fail (GTK_IS_CONTAINER (container));
  if (adjustment)
    g_return_if_fail (GTK_IS_ADJUSTMENT (adjustment));

  if (adjustment)
    g_object_ref (adjustment);

  g_object_set_qdata_full (G_OBJECT (container),
                           hadjustment_key_id,
                           adjustment,
                           g_object_unref);
}

/**
 * gtk_container_get_focus_hadjustment:
 * @container: a #GtkContainer
 *
 * Retrieves the horizontal focus adjustment for the container. See
 * gtk_container_set_focus_hadjustment ().
 *
 * Returns: (transfer none): the horizontal focus adjustment, or %NULL if
 *   none has been set.
 **/
GtkAdjustment *
gtk_container_get_focus_hadjustment (GtkContainer *container)
{
  GtkAdjustment *hadjustment;

  g_return_val_if_fail (GTK_IS_CONTAINER (container), NULL);

  hadjustment = g_object_get_qdata (G_OBJECT (container), hadjustment_key_id);

  return hadjustment;
}


static void
gtk_container_show_all (GtkWidget *widget)
{
  g_return_if_fail (GTK_IS_CONTAINER (widget));

  gtk_container_foreach (GTK_CONTAINER (widget),
                         (GtkCallback) gtk_widget_show_all,
                         NULL);
  gtk_widget_show (widget);
}

typedef struct {
  GtkWidget *child;
  int window_depth;
} ChildOrderInfo;

static void
gtk_container_draw_forall (GtkWidget *widget,
                           gpointer   client_data)
{
  struct {
    GtkContainer *container;
    GArray *child_infos;
    cairo_t *cr;
  } *data = client_data;
  ChildOrderInfo info;
  GList *siblings;
  GdkWindow *window;

  if (gtk_container_should_propagate_draw (data->container, widget, data->cr))
    {
      info.child = widget;
      info.window_depth = G_MAXINT;
      if (gtk_widget_get_has_window (widget))
        {
          window = gtk_widget_get_window (widget);
          siblings = gdk_window_peek_children (gdk_window_get_parent (window));
          info.window_depth = g_list_index (siblings, window);
        }
      g_array_append_val (data->child_infos, info);
    }
}

static gint
compare_children_for_draw (gconstpointer  _a,
                           gconstpointer  _b)
{
  const ChildOrderInfo *a = _a;
  const ChildOrderInfo *b = _b;

  return b->window_depth - a->window_depth;
}

static gint
gtk_container_draw (GtkWidget *widget,
                    cairo_t   *cr)
{
  GtkContainer *container = GTK_CONTAINER (widget);
  GArray *child_infos;
  int i;
  ChildOrderInfo *child_info;
  struct {
    GtkContainer *container;
    GArray *child_infos;
    cairo_t *cr;
  } data;

  child_infos = g_array_new (FALSE, TRUE, sizeof (ChildOrderInfo));

  data.container = container;
  data.cr = cr;
  data.child_infos = child_infos;
  gtk_container_forall (container,
                        gtk_container_draw_forall,
                        &data);

  g_array_sort (child_infos, compare_children_for_draw);

  for (i = 0; i < child_infos->len; i++)
    {
      child_info = &g_array_index (child_infos, ChildOrderInfo, i);
      gtk_container_propagate_draw (container,
                                    child_info->child, cr);
    }

  g_array_free (child_infos, TRUE);

  return FALSE;
}

static void
gtk_container_map_child (GtkWidget *child,
                         gpointer   client_data)
{
  if (gtk_widget_get_visible (child) &&
      gtk_widget_get_child_visible (child) &&
      !gtk_widget_get_mapped (child))
    gtk_widget_map (child);
}

static void
gtk_container_map (GtkWidget *widget)
{
  gtk_widget_set_mapped (widget, TRUE);

  gtk_container_forall (GTK_CONTAINER (widget),
                        gtk_container_map_child,
                        NULL);

  if (gtk_widget_get_has_window (widget))
    gdk_window_show (gtk_widget_get_window (widget));
}

static void
gtk_container_unmap (GtkWidget *widget)
{
  gtk_widget_set_mapped (widget, FALSE);

  /* hide our window first so user doesn't see all the child windows
   * vanishing one by one.  (only matters these days if one of the
   * children has an actual native window instead of client-side
   * window, e.g. a GtkSocket would)
   */
  if (gtk_widget_get_has_window (widget))
    gdk_window_hide (gtk_widget_get_window (widget));

  gtk_container_forall (GTK_CONTAINER (widget),
                        (GtkCallback)gtk_widget_unmap,
                        NULL);
}

static gboolean
gtk_container_should_propagate_draw (GtkContainer   *container,
                                     GtkWidget      *child,
                                     cairo_t        *cr)
{
  GdkEventExpose *event;
  GdkWindow *event_window, *child_in_window;

  if (!gtk_widget_is_drawable (child))
    return FALSE;

  /* Only propagate to native child window if we're not handling
     an expose (i.e. in a pure gtk_widget_draw() call */
  event = _gtk_cairo_get_event (cr);
  if (event &&
      (gtk_widget_get_has_window (child) &&
       gdk_window_has_native (gtk_widget_get_window (child))))
    return FALSE;

  /* Never propagate to a child window when exposing a window
     that is not the one the child widget is in. */
  event_window = _gtk_cairo_get_event_window (cr);
  if (gtk_widget_get_has_window (child))
    child_in_window = gdk_window_get_parent (gtk_widget_get_window (child));
  else
    child_in_window = gtk_widget_get_window (child);
  if (event_window != NULL && child_in_window != event_window)
    return FALSE;

  return TRUE;
}


/**
 * gtk_container_propagate_draw:
 * @container: a #GtkContainer
 * @child: a child of @container
 * @cr: Cairo context as passed to the container. If you want to use @cr
 *   in container’s draw function, consider using cairo_save() and
 *   cairo_restore() before calling this function.
 *
 * When a container receives a call to the draw function, it must send
 * synthetic #GtkWidget::draw calls to all children that don’t have their
 * own #GdkWindows. This function provides a convenient way of doing this.
 * A container, when it receives a call to its #GtkWidget::draw function,
 * calls gtk_container_propagate_draw() once for each child, passing in
 * the @cr the container received.
 *
 * gtk_container_propagate_draw() takes care of translating the origin of @cr,
 * and deciding whether the draw needs to be sent to the child. It is a
 * convenient and optimized way of getting the same effect as calling
 * gtk_widget_draw() on the child directly.
 *
 * In most cases, a container can simply either inherit the
 * #GtkWidget::draw implementation from #GtkContainer, or do some drawing
 * and then chain to the ::draw implementation from #GtkContainer.
 **/
void
gtk_container_propagate_draw (GtkContainer   *container,
                              GtkWidget      *child,
                              cairo_t        *cr)
{
  GtkAllocation allocation;
  GdkWindow *window, *w;
  int x, y;

  g_return_if_fail (GTK_IS_CONTAINER (container));
  g_return_if_fail (GTK_IS_WIDGET (child));
  g_return_if_fail (cr != NULL);

  g_assert (gtk_widget_get_parent (child) == GTK_WIDGET (container));

  if (!gtk_container_should_propagate_draw (container, child, cr))
    return;

  cairo_save (cr);

  /* translate coordinates. Ugly business, that. */
  if (!gtk_widget_get_has_window (GTK_WIDGET (container)))
    {
      gtk_widget_get_allocation (GTK_WIDGET (container), &allocation);
      x = -allocation.x;
      y = -allocation.y;
    }
  else
    {
      x = 0;
      y = 0;
    }

  window = gtk_widget_get_window (GTK_WIDGET (container));

  for (w = gtk_widget_get_window (child); w && w != window; w = gdk_window_get_parent (w))
    {
      int wx, wy;
      gdk_window_get_position (w, &wx, &wy);
      x += wx;
      y += wy;
    }

  if (w == NULL)
    {
      x = 0;
      y = 0;
    }

  if (!gtk_widget_get_has_window (child))
    {
      gtk_widget_get_allocation (child, &allocation);
      x += allocation.x;
      y += allocation.y;
    }

  cairo_translate (cr, x, y);

  _gtk_widget_draw (child, cr);

  cairo_restore (cr);
}

gboolean
_gtk_container_get_reallocate_redraws (GtkContainer *container)
{
  return container->priv->reallocate_redraws;
}

/**
 * gtk_container_get_path_for_child:
 * @container: a #GtkContainer
 * @child: a child of @container
 *
 * Returns a newly created widget path representing all the widget hierarchy
 * from the toplevel down to and including @child.
 *
 * Returns: A newly created #GtkWidgetPath
 **/
GtkWidgetPath *
gtk_container_get_path_for_child (GtkContainer *container,
                                  GtkWidget    *child)
{
  GtkWidgetPath *path;

  g_return_val_if_fail (GTK_IS_CONTAINER (container), NULL);
  g_return_val_if_fail (GTK_IS_WIDGET (child), NULL);
  g_return_val_if_fail (container == (GtkContainer *) gtk_widget_get_parent (child), NULL);

  path = GTK_CONTAINER_GET_CLASS (container)->get_path_for_child (container, child);
  if (gtk_widget_path_get_object_type (path) != G_OBJECT_TYPE (child))
    {
      g_critical ("%s %p returned a widget path for type %s, but child is %s",
                  G_OBJECT_TYPE_NAME (container),
                  container,
                  g_type_name (gtk_widget_path_get_object_type (path)),
                  G_OBJECT_TYPE_NAME (child));
    }

  return path;
}
