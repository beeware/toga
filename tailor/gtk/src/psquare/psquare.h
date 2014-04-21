#ifndef P_SQUARE_H
#define P_SQUARE_H

#include <glib-object.h>
#include <gtk/gtk.h>

G_BEGIN_DECLS

#define P_SQUARE_TYPE            (p_square_get_type())
#define P_SQUARE(obj)            (G_TYPE_CHECK_INSTANCE_CAST((obj), P_SQUARE_TYPE, PSquare))
#define P_SQUARE_CLASS(klass)    (G_TYPE_CHECK_CLASS_CAST((klass), P_SQUARE_TYPE, PSqaureClass))
#define P_IS_SQUARE(obj)         (G_TYPE_CHECK_INSTANCE_TYPE((obj), P_SQUARE_TYPE))
#define P_IS_SQUARE_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE((klass), P_SQUARE_TYPE))

typedef struct _PSquare       PSquare;
typedef struct _PSquareClass  PSquareClass;

struct _PSquare
{
	GtkContainer parent_instance;
};

struct _PSquareClass
{
	GtkContainerClass parent_class;
};

GType p_square_get_type(void) G_GNUC_CONST;
GtkWidget *p_square_new(void);

G_END_DECLS

#endif /* P_SQUARE_H */
