from rubicon.java import JavaClass, JavaInterface

ArrayAdapter = JavaClass("android/widget/ArrayAdapter")
Button = JavaClass("android/widget/Button")
AlertDialog__Builder = JavaClass("android/app/AlertDialog$Builder")
DialogInterface__OnClickListener = JavaInterface("android/content/DialogInterface$OnClickListener")
EditText = JavaClass("android/widget/EditText")
Gravity = JavaClass("android/view/Gravity")
InputType = JavaClass("android/text/InputType")
NumberPicker = JavaClass("android/widget/NumberPicker")
OnClickListener = JavaInterface("android/view/View$OnClickListener")
OnItemSelectedListener = JavaInterface("android/widget/AdapterView$OnItemSelectedListener")
R__layout = JavaClass("android/R$layout")
RelativeLayout = JavaClass("android/widget/RelativeLayout")
RelativeLayout__LayoutParams = JavaClass("android/widget/RelativeLayout$LayoutParams")
ScrollView = JavaClass("android/widget/ScrollView")
Spinner = JavaClass("android/widget/Spinner")
TextView = JavaClass("android/widget/TextView")
TextWatcher = JavaInterface("android/text/TextWatcher")
ViewGroup__LayoutParams = JavaClass("android/view/ViewGroup$LayoutParams")
View__MeasureSpec = JavaClass("android/view/View$MeasureSpec")

# Indicate to `rubicon-java` that `ArrayAdapter` can also be typecast into a
# `SpinnerAdapter`. This is required until `rubicon-java` explores the interfaces
# implemented by a class's subclasses.
ArrayAdapter._alternates.append(b'Landroid/widget/SpinnerAdapter;')
