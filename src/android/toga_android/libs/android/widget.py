from rubicon.java import JavaClass, JavaInterface

ArrayAdapter = JavaClass("android/widget/ArrayAdapter")
# `ArrayAdapter` can also be typecast into a `SpinnerAdapter`.
# This is required until `rubicon-java` explores the interfaces
# implemented by a class's subclasses.
ArrayAdapter._alternates.append(b'Landroid/widget/SpinnerAdapter;')

Button = JavaClass("android/widget/Button")
CompoundButton__OnCheckedChangeListener = JavaInterface("android/widget/CompoundButton$OnCheckedChangeListener")
EditText = JavaClass("android/widget/EditText")
HorizontalScrollView = JavaClass("android/widget/HorizontalScrollView")
ImageView = JavaClass("android/widget/ImageView")
ImageView__ScaleType = JavaClass("android/widget/ImageView$ScaleType")
LinearLayout = JavaClass("android/widget/LinearLayout")
LinearLayout__LayoutParams = JavaClass("android/widget/LinearLayout$LayoutParams")
NumberPicker = JavaClass("android/widget/NumberPicker")
OnItemSelectedListener = JavaInterface("android/widget/AdapterView$OnItemSelectedListener")
RelativeLayout = JavaClass("android/widget/RelativeLayout")
RelativeLayout__LayoutParams = JavaClass("android/widget/RelativeLayout$LayoutParams")
ScrollView = JavaClass("android/widget/ScrollView")
SeekBar = JavaClass("android/widget/SeekBar")
SeekBar__OnSeekBarChangeListener = JavaInterface("android/widget/SeekBar$OnSeekBarChangeListener")
Switch = JavaClass("android/widget/Switch")
Spinner = JavaClass("android/widget/Spinner")
TableLayout = JavaClass("android/widget/TableLayout")
TableLayout__Layoutparams = JavaClass("android/widget/TableLayout$LayoutParams")
TableRow = JavaClass("android/widget/TableRow")
TableRow__Layoutparams = JavaClass("android/widget/TableRow$LayoutParams")
TextView = JavaClass("android/widget/TextView")
