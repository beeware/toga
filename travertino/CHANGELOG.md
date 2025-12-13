# Changelog

**Note:** As of version 0.5.0, Travertino is now hosted and developed as part of the Toga repository. It's now released along with — and has the same version number as — each [Toga release](https://github.com/beeware/toga/releases).

For all development beyond 0.5.0, any changes made to Travertino will be logged along with Toga's overall list of changes for each new release.

# 0.5.0 (2025-03-14)

## Features

- Validated properties of styles can now be defined as dataclass class attributes. ([#141](https://github.com/beeware/travertino/issues/141))
- BaseStyle now supports `|`, `|=`, and `in` operators. ([#143](https://github.com/beeware/travertino/issues/143))
- A `list_property` declaration has been added to support storing multi-valueds style elements. ([#148](https://github.com/beeware/travertino/issues/148))
- Support for Python 3.13 was added. ([#149](https://github.com/beeware/travertino/issues/149))
- Support for Python 3.14 was added. ([#223](https://github.com/beeware/travertino/issues/223))
- The constants `START` and `END` have been added. ([#241](https://github.com/beeware/travertino/issues/241))

## Bugfixes

- Assigning a new style object to a node that already has an applicator assigned now properly maintains an association between the applicator and the new style, and triggers a style reapplication. ([#224](https://github.com/beeware/travertino/issues/224))
- Equality checks between a Font object and a non-Font object will now throw an exception instead of returning False. ([#233](https://github.com/beeware/travertino/issues/233))

## Backward Incompatible Changes

- The <span class="title-ref">default</span> parameter for Choice has been deprecated. ([#139](https://github.com/beeware/travertino/issues/139))
- Python 3.8 is no longer supported. ([#223](https://github.com/beeware/travertino/issues/223))
- The mechanisms for assigning styles and applicators to nodes, and applying styles, have been reworked. A node will now attempt to apply its style as soon as it is assigned an applicator. This means you should not assign an applicator to a node until the node is sufficiently initialized to apply its style. To accommodate uses that currently do not follow this order, any exceptions resulting from a failed style application are caught, and a runtime warning is issued. In a future version, this will be an exception. ([#224](https://github.com/beeware/travertino/issues/224))
- Supplying an applicator to BaseStyle.copy() has been deprecated. If you need to manually assign an applicator to a style, do it separately, after the copy. ([#224](https://github.com/beeware/travertino/issues/224))
- The API for `Style.layout()` has been formally specified as part of the Travertino API. The initial `node` argument is no longer required as part of the `layout()` method. A `Style` instance can interrogate `self._applicator.node` to retrieve the node to which the style is being applied. ([#244](https://github.com/beeware/travertino/issues/244))
- Travertino's font-parsing function `fonts.font` has been removed, as has the `default` parameter to `Choices`. Neither was in use by Toga; this should only affect direct use of the Travertino API. ([#3129](https://github.com/beeware/toga/issues/3129))

## Documentation

- The README badges were updated to display correctly on GitHub. ([#170](https://github.com/beeware/travertino/issues/170))

## Misc

- [#88](https://github.com/beeware/travertino/issues/88), [#89](https://github.com/beeware/travertino/issues/89), [#90](https://github.com/beeware/travertino/issues/90), [#91](https://github.com/beeware/travertino/issues/91), [#92](https://github.com/beeware/travertino/issues/92), [#93](https://github.com/beeware/travertino/issues/93), [#94](https://github.com/beeware/travertino/issues/94), [#95](https://github.com/beeware/travertino/issues/95), [#96](https://github.com/beeware/travertino/issues/96), [#97](https://github.com/beeware/travertino/issues/97), [#98](https://github.com/beeware/travertino/issues/98), [#99](https://github.com/beeware/travertino/issues/99), [#100](https://github.com/beeware/travertino/issues/100), [#101](https://github.com/beeware/travertino/issues/101), [#102](https://github.com/beeware/travertino/issues/102), [#103](https://github.com/beeware/travertino/issues/103), [#104](https://github.com/beeware/travertino/issues/104), [#105](https://github.com/beeware/travertino/issues/105), [#106](https://github.com/beeware/travertino/issues/106), [#107](https://github.com/beeware/travertino/issues/107), [#108](https://github.com/beeware/travertino/issues/108), [#109](https://github.com/beeware/travertino/issues/109), [#110](https://github.com/beeware/travertino/issues/110), [#111](https://github.com/beeware/travertino/issues/111), [#112](https://github.com/beeware/travertino/issues/112), [#113](https://github.com/beeware/travertino/issues/113), [#114](https://github.com/beeware/travertino/issues/114), [#115](https://github.com/beeware/travertino/issues/115), [#116](https://github.com/beeware/travertino/issues/116), [#117](https://github.com/beeware/travertino/issues/117), [#118](https://github.com/beeware/travertino/issues/118), [#120](https://github.com/beeware/travertino/issues/120), [#121](https://github.com/beeware/travertino/issues/121), [#122](https://github.com/beeware/travertino/issues/122), [#123](https://github.com/beeware/travertino/issues/123), [#124](https://github.com/beeware/travertino/issues/124), [#125](https://github.com/beeware/travertino/issues/125), [#126](https://github.com/beeware/travertino/issues/126), [#127](https://github.com/beeware/travertino/issues/127), [#128](https://github.com/beeware/travertino/issues/128), [#129](https://github.com/beeware/travertino/issues/129), [#130](https://github.com/beeware/travertino/issues/130), [#131](https://github.com/beeware/travertino/issues/131), [#132](https://github.com/beeware/travertino/issues/132), [#133](https://github.com/beeware/travertino/issues/133), [#134](https://github.com/beeware/travertino/issues/134), [#135](https://github.com/beeware/travertino/issues/135), [#136](https://github.com/beeware/travertino/issues/136), [#137](https://github.com/beeware/travertino/issues/137), [#138](https://github.com/beeware/travertino/issues/138), [#140](https://github.com/beeware/travertino/issues/140), [#142](https://github.com/beeware/travertino/issues/142), [#144](https://github.com/beeware/travertino/issues/144), [#145](https://github.com/beeware/travertino/issues/145), [#146](https://github.com/beeware/travertino/issues/146), [#147](https://github.com/beeware/travertino/issues/147), [#150](https://github.com/beeware/travertino/issues/150), [#151](https://github.com/beeware/travertino/issues/151), [#152](https://github.com/beeware/travertino/issues/152), [#154](https://github.com/beeware/travertino/issues/154), [#155](https://github.com/beeware/travertino/issues/155), [#156](https://github.com/beeware/travertino/issues/156), [#157](https://github.com/beeware/travertino/issues/157), [#158](https://github.com/beeware/travertino/issues/158), [#159](https://github.com/beeware/travertino/issues/159), [#160](https://github.com/beeware/travertino/issues/160), [#161](https://github.com/beeware/travertino/issues/161), [#162](https://github.com/beeware/travertino/issues/162), [#163](https://github.com/beeware/travertino/issues/163), [#164](https://github.com/beeware/travertino/issues/164), [#165](https://github.com/beeware/travertino/issues/165), [#166](https://github.com/beeware/travertino/issues/166), [#167](https://github.com/beeware/travertino/issues/167), [#168](https://github.com/beeware/travertino/issues/168), [#169](https://github.com/beeware/travertino/issues/169), [#171](https://github.com/beeware/travertino/issues/171), [#172](https://github.com/beeware/travertino/issues/172), [#173](https://github.com/beeware/travertino/issues/173), [#174](https://github.com/beeware/travertino/issues/174), [#175](https://github.com/beeware/travertino/issues/175), [#176](https://github.com/beeware/travertino/issues/176), [#177](https://github.com/beeware/travertino/issues/177), [#178](https://github.com/beeware/travertino/issues/178), [#179](https://github.com/beeware/travertino/issues/179), [#180](https://github.com/beeware/travertino/issues/180), [#181](https://github.com/beeware/travertino/issues/181), [#182](https://github.com/beeware/travertino/issues/182), [#183](https://github.com/beeware/travertino/issues/183), [#184](https://github.com/beeware/travertino/issues/184), [#185](https://github.com/beeware/travertino/issues/185), [#186](https://github.com/beeware/travertino/issues/186), [#187](https://github.com/beeware/travertino/issues/187), [#188](https://github.com/beeware/travertino/issues/188), [#189](https://github.com/beeware/travertino/issues/189), [#190](https://github.com/beeware/travertino/issues/190), [#191](https://github.com/beeware/travertino/issues/191), [#192](https://github.com/beeware/travertino/issues/192), [#193](https://github.com/beeware/travertino/issues/193), [#194](https://github.com/beeware/travertino/issues/194), [#195](https://github.com/beeware/travertino/issues/195), [#196](https://github.com/beeware/travertino/issues/196), [#197](https://github.com/beeware/travertino/issues/197), [#199](https://github.com/beeware/travertino/issues/199), [#200](https://github.com/beeware/travertino/issues/200), [#202](https://github.com/beeware/travertino/issues/202), [#204](https://github.com/beeware/travertino/issues/204), [#205](https://github.com/beeware/travertino/issues/205), [#206](https://github.com/beeware/travertino/issues/206), [#207](https://github.com/beeware/travertino/issues/207), [#208](https://github.com/beeware/travertino/issues/208), [#209](https://github.com/beeware/travertino/issues/209), [#210](https://github.com/beeware/travertino/issues/210), [#211](https://github.com/beeware/travertino/issues/211), [#212](https://github.com/beeware/travertino/issues/212), [#213](https://github.com/beeware/travertino/issues/213), [#214](https://github.com/beeware/travertino/issues/214), [#215](https://github.com/beeware/travertino/issues/215), [#216](https://github.com/beeware/travertino/issues/216), [#217](https://github.com/beeware/travertino/issues/217), [#218](https://github.com/beeware/travertino/issues/218), [#219](https://github.com/beeware/travertino/issues/219), [#220](https://github.com/beeware/travertino/issues/220), [#221](https://github.com/beeware/travertino/issues/221), [#224](https://github.com/beeware/travertino/issues/224), [#225](https://github.com/beeware/travertino/issues/225), [#226](https://github.com/beeware/travertino/issues/226), [#227](https://github.com/beeware/travertino/issues/227), [#228](https://github.com/beeware/travertino/issues/228), [#229](https://github.com/beeware/travertino/issues/229), [#230](https://github.com/beeware/travertino/issues/230), [#231](https://github.com/beeware/travertino/issues/231), [#232](https://github.com/beeware/travertino/issues/232), [#234](https://github.com/beeware/travertino/issues/234), [#235](https://github.com/beeware/travertino/issues/235), [#236](https://github.com/beeware/travertino/issues/236), [#237](https://github.com/beeware/travertino/issues/237), [#238](https://github.com/beeware/travertino/issues/238), [#239](https://github.com/beeware/travertino/issues/239), [#240](https://github.com/beeware/travertino/issues/240), [#242](https://github.com/beeware/travertino/issues/242), [#245](https://github.com/beeware/travertino/issues/245), [#247](https://github.com/beeware/travertino/issues/247), [#248](https://github.com/beeware/travertino/issues/248)

# 0.3.0 (2023-08-16)

## Features

- Layout nodes can now track the minimum permitted layout size in addition to the current actual layout size. ([#78](https://github.com/beeware/travertino/issues/78))

## Backward Incompatible Changes

- Support for Python 3.7 was removed. ([#80](https://github.com/beeware/travertino/issues/80))

## Misc

- [#44](https://github.com/beeware/travertino/issues/44), [#45](https://github.com/beeware/travertino/issues/45), [#46](https://github.com/beeware/travertino/issues/46), [#47](https://github.com/beeware/travertino/issues/47), [#48](https://github.com/beeware/travertino/issues/48), [#49](https://github.com/beeware/travertino/issues/49), [#50](https://github.com/beeware/travertino/issues/50), [#51](https://github.com/beeware/travertino/issues/51), [#52](https://github.com/beeware/travertino/issues/52), [#53](https://github.com/beeware/travertino/issues/53), [#54](https://github.com/beeware/travertino/issues/54), [#55](https://github.com/beeware/travertino/issues/55), [#56](https://github.com/beeware/travertino/issues/56), [#57](https://github.com/beeware/travertino/issues/57), [#58](https://github.com/beeware/travertino/issues/58), [#59](https://github.com/beeware/travertino/issues/59), [#60](https://github.com/beeware/travertino/issues/60), [#61](https://github.com/beeware/travertino/issues/61), [#62](https://github.com/beeware/travertino/issues/62), [#63](https://github.com/beeware/travertino/issues/63), [#65](https://github.com/beeware/travertino/issues/65), [#66](https://github.com/beeware/travertino/issues/66), [#67](https://github.com/beeware/travertino/issues/67), [#72](https://github.com/beeware/travertino/issues/72), [#73](https://github.com/beeware/travertino/issues/73), [#74](https://github.com/beeware/travertino/issues/74), [#75](https://github.com/beeware/travertino/issues/75), [#76](https://github.com/beeware/travertino/issues/76), [#77](https://github.com/beeware/travertino/issues/77), [#79](https://github.com/beeware/travertino/issues/79), [#81](https://github.com/beeware/travertino/issues/81), [#82](https://github.com/beeware/travertino/issues/82), [#83](https://github.com/beeware/travertino/issues/83), [#84](https://github.com/beeware/travertino/issues/84), [#85](https://github.com/beeware/travertino/issues/85), [#86](https://github.com/beeware/travertino/issues/86), [#87](https://github.com/beeware/travertino/issues/87)

# 0.2.0 (2023-03-24)

## Features

- Node now supports the `clear` method in order to clear all children. ([#23](https://github.com/beeware/travertino/issues/23))
- Constants for absolute and relative font sizing were added. ([#43](https://github.com/beeware/travertino/issues/43))

## Bugfixes

- Handling of `none` as a property value has been corrected. ([#3](https://github.com/beeware/travertino/issues/3))

## Improved Documentation

- Details on towncrier and pre-commit ussage were added to the README. ([#18](https://github.com/beeware/travertino/issues/18))

## Misc

- [#22](https://github.com/beeware/travertino/issues/22), [#24](https://github.com/beeware/travertino/issues/24), [#25](https://github.com/beeware/travertino/issues/25), [#26](https://github.com/beeware/travertino/issues/26), [#30](https://github.com/beeware/travertino/issues/30), [#34](https://github.com/beeware/travertino/issues/34), [#35](https://github.com/beeware/travertino/issues/35), [#36](https://github.com/beeware/travertino/issues/36), [#37](https://github.com/beeware/travertino/issues/37), [#38](https://github.com/beeware/travertino/issues/38), [#39](https://github.com/beeware/travertino/issues/39), [#40](https://github.com/beeware/travertino/issues/40), [#41](https://github.com/beeware/travertino/issues/41), [#42](https://github.com/beeware/travertino/issues/42)

# 0.1.3 (2020-05-25)

## Features

- Introduced some constants used by Pack that have more general uses. ([#5](https://github.com/beeware/travertino/issues/5))
- Added the ability to add, insert and remove children from a node tree. ([#10](https://github.com/beeware/travertino/issues/10))
- Added color validation in rgba and hsla constructors ([#17](https://github.com/beeware/travertino/issues/17))
- Added support for declaring a system default font size. ([#19](https://github.com/beeware/travertino/issues/19))

## Misc

- [#15](https://github.com/beeware/travertino/issues/15), [#16](https://github.com/beeware/travertino/issues/16)

# 0.1.2

- Added constants for system and message fonts
- Added hash method to fonts and colors

# 0.1.1

- Added font definitions

# 0.1.0

Initial release.
