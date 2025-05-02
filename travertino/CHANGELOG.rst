Changelog
=========

**Note:** As of version 0.5.0, Travertino is now hosted and developed as part of the
Toga repository. It's now released along with — and has the same version number as —
each `Toga release <https://github.com/beeware/toga/releases>`_.

For all development beyond 0.5.0, any changes made to Travertino will be logged along
with Toga's overall list of changes for each new release.

.. towncrier release notes start

0.5.0 (2025-03-14)
==================

Features
--------

* Validated properties of styles can now be defined as dataclass class attributes. (`#141 <https://github.com/beeware/travertino/issues/141>`_)
* BaseStyle now supports ``|``, ``|=``, and ``in`` operators. (`#143 <https://github.com/beeware/travertino/issues/143>`_)
* A ``list_property`` declaration has been added to support storing multi-valueds style elements. (`#148 <https://github.com/beeware/travertino/issues/148>`_)
* Support for Python 3.13 was added. (`#149 <https://github.com/beeware/travertino/issues/149>`_)
* Support for Python 3.14 was added. (`#223 <https://github.com/beeware/travertino/issues/223>`_)
* The constants ``START`` and ``END`` have been added. (`#241 <https://github.com/beeware/travertino/issues/241>`_)

Bugfixes
--------

* Assigning a new style object to a node that already has an applicator assigned now properly maintains an association between the applicator and the new style, and triggers a style reapplication. (`#224 <https://github.com/beeware/travertino/issues/224>`_)
* Equality checks between a Font object and a non-Font object will now throw an exception instead of returning False. (`#233 <https://github.com/beeware/travertino/issues/233>`_)

Backward Incompatible Changes
-----------------------------

* The `default` parameter for Choice has been deprecated. (`#139 <https://github.com/beeware/travertino/issues/139>`_)
* Python 3.8 is no longer supported. (`#223 <https://github.com/beeware/travertino/issues/223>`_)
* The mechanisms for assigning styles and applicators to nodes, and applying styles, have been reworked. A node will now attempt to apply its style as soon as it is assigned an applicator. This means you should not assign an applicator to a node until the node is sufficiently initialized to apply its style. To accommodate uses that currently do not follow this order, any exceptions resulting from a failed style application are caught, and a runtime warning is issued. In a future version, this will be an exception. (`#224 <https://github.com/beeware/travertino/issues/224>`_)
* Supplying an applicator to BaseStyle.copy() has been deprecated. If you need to manually assign an applicator to a style, do it separately, after the copy. (`#224 <https://github.com/beeware/travertino/issues/224>`_)
* The API for ``Style.layout()`` has been formally specified as part of the Travertino API. The initial ``node`` argument is no longer required as part of the ``layout()`` method. A ``Style`` instance can interrogate ``self._applicator.node`` to retrieve the node to which the style is being applied. (`#244 <https://github.com/beeware/travertino/issues/244>`_)
* Travertino's font-parsing function ``fonts.font`` has been removed, as has the ``default`` parameter to ``Choices``. Neither was in use by Toga; this should only affect direct use of the Travertino API. (`#3129 <https://github.com/beeware/toga/issues/3129>`__)


Documentation
-------------

* The README badges were updated to display correctly on GitHub. (`#170 <https://github.com/beeware/travertino/issues/170>`_)


Misc
----

* `#88 <https://github.com/beeware/travertino/issues/88>`_, `#89 <https://github.com/beeware/travertino/issues/89>`_, `#90 <https://github.com/beeware/travertino/issues/90>`_, `#91 <https://github.com/beeware/travertino/issues/91>`_, `#92 <https://github.com/beeware/travertino/issues/92>`_, `#93 <https://github.com/beeware/travertino/issues/93>`_, `#94 <https://github.com/beeware/travertino/issues/94>`_, `#95 <https://github.com/beeware/travertino/issues/95>`_, `#96 <https://github.com/beeware/travertino/issues/96>`_, `#97 <https://github.com/beeware/travertino/issues/97>`_, `#98 <https://github.com/beeware/travertino/issues/98>`_, `#99 <https://github.com/beeware/travertino/issues/99>`_, `#100 <https://github.com/beeware/travertino/issues/100>`_, `#101 <https://github.com/beeware/travertino/issues/101>`_, `#102 <https://github.com/beeware/travertino/issues/102>`_, `#103 <https://github.com/beeware/travertino/issues/103>`_, `#104 <https://github.com/beeware/travertino/issues/104>`_, `#105 <https://github.com/beeware/travertino/issues/105>`_, `#106 <https://github.com/beeware/travertino/issues/106>`_, `#107 <https://github.com/beeware/travertino/issues/107>`_, `#108 <https://github.com/beeware/travertino/issues/108>`_, `#109 <https://github.com/beeware/travertino/issues/109>`_, `#110 <https://github.com/beeware/travertino/issues/110>`_, `#111 <https://github.com/beeware/travertino/issues/111>`_, `#112 <https://github.com/beeware/travertino/issues/112>`_, `#113 <https://github.com/beeware/travertino/issues/113>`_, `#114 <https://github.com/beeware/travertino/issues/114>`_, `#115 <https://github.com/beeware/travertino/issues/115>`_, `#116 <https://github.com/beeware/travertino/issues/116>`_, `#117 <https://github.com/beeware/travertino/issues/117>`_, `#118 <https://github.com/beeware/travertino/issues/118>`_, `#120 <https://github.com/beeware/travertino/issues/120>`_, `#121 <https://github.com/beeware/travertino/issues/121>`_, `#122 <https://github.com/beeware/travertino/issues/122>`_, `#123 <https://github.com/beeware/travertino/issues/123>`_, `#124 <https://github.com/beeware/travertino/issues/124>`_, `#125 <https://github.com/beeware/travertino/issues/125>`_, `#126 <https://github.com/beeware/travertino/issues/126>`_, `#127 <https://github.com/beeware/travertino/issues/127>`_, `#128 <https://github.com/beeware/travertino/issues/128>`_, `#129 <https://github.com/beeware/travertino/issues/129>`_, `#130 <https://github.com/beeware/travertino/issues/130>`_, `#131 <https://github.com/beeware/travertino/issues/131>`_, `#132 <https://github.com/beeware/travertino/issues/132>`_, `#133 <https://github.com/beeware/travertino/issues/133>`_, `#134 <https://github.com/beeware/travertino/issues/134>`_, `#135 <https://github.com/beeware/travertino/issues/135>`_, `#136 <https://github.com/beeware/travertino/issues/136>`_, `#137 <https://github.com/beeware/travertino/issues/137>`_, `#138 <https://github.com/beeware/travertino/issues/138>`_, `#140 <https://github.com/beeware/travertino/issues/140>`_, `#142 <https://github.com/beeware/travertino/issues/142>`_, `#144 <https://github.com/beeware/travertino/issues/144>`_, `#145 <https://github.com/beeware/travertino/issues/145>`_, `#146 <https://github.com/beeware/travertino/issues/146>`_, `#147 <https://github.com/beeware/travertino/issues/147>`_, `#150 <https://github.com/beeware/travertino/issues/150>`_, `#151 <https://github.com/beeware/travertino/issues/151>`_, `#152 <https://github.com/beeware/travertino/issues/152>`_, `#154 <https://github.com/beeware/travertino/issues/154>`_, `#155 <https://github.com/beeware/travertino/issues/155>`_, `#156 <https://github.com/beeware/travertino/issues/156>`_, `#157 <https://github.com/beeware/travertino/issues/157>`_, `#158 <https://github.com/beeware/travertino/issues/158>`_, `#159 <https://github.com/beeware/travertino/issues/159>`_, `#160 <https://github.com/beeware/travertino/issues/160>`_, `#161 <https://github.com/beeware/travertino/issues/161>`_, `#162 <https://github.com/beeware/travertino/issues/162>`_, `#163 <https://github.com/beeware/travertino/issues/163>`_, `#164 <https://github.com/beeware/travertino/issues/164>`_, `#165 <https://github.com/beeware/travertino/issues/165>`_, `#166 <https://github.com/beeware/travertino/issues/166>`_, `#167 <https://github.com/beeware/travertino/issues/167>`_, `#168 <https://github.com/beeware/travertino/issues/168>`_, `#169 <https://github.com/beeware/travertino/issues/169>`_, `#171 <https://github.com/beeware/travertino/issues/171>`_, `#172 <https://github.com/beeware/travertino/issues/172>`_, `#173 <https://github.com/beeware/travertino/issues/173>`_, `#174 <https://github.com/beeware/travertino/issues/174>`_, `#175 <https://github.com/beeware/travertino/issues/175>`_, `#176 <https://github.com/beeware/travertino/issues/176>`_, `#177 <https://github.com/beeware/travertino/issues/177>`_, `#178 <https://github.com/beeware/travertino/issues/178>`_, `#179 <https://github.com/beeware/travertino/issues/179>`_, `#180 <https://github.com/beeware/travertino/issues/180>`_, `#181 <https://github.com/beeware/travertino/issues/181>`_, `#182 <https://github.com/beeware/travertino/issues/182>`_, `#183 <https://github.com/beeware/travertino/issues/183>`_, `#184 <https://github.com/beeware/travertino/issues/184>`_, `#185 <https://github.com/beeware/travertino/issues/185>`_, `#186 <https://github.com/beeware/travertino/issues/186>`_, `#187 <https://github.com/beeware/travertino/issues/187>`_, `#188 <https://github.com/beeware/travertino/issues/188>`_, `#189 <https://github.com/beeware/travertino/issues/189>`_, `#190 <https://github.com/beeware/travertino/issues/190>`_, `#191 <https://github.com/beeware/travertino/issues/191>`_, `#192 <https://github.com/beeware/travertino/issues/192>`_, `#193 <https://github.com/beeware/travertino/issues/193>`_, `#194 <https://github.com/beeware/travertino/issues/194>`_, `#195 <https://github.com/beeware/travertino/issues/195>`_, `#196 <https://github.com/beeware/travertino/issues/196>`_, `#197 <https://github.com/beeware/travertino/issues/197>`_, `#199 <https://github.com/beeware/travertino/issues/199>`_, `#200 <https://github.com/beeware/travertino/issues/200>`_, `#202 <https://github.com/beeware/travertino/issues/202>`_, `#204 <https://github.com/beeware/travertino/issues/204>`_, `#205 <https://github.com/beeware/travertino/issues/205>`_, `#206 <https://github.com/beeware/travertino/issues/206>`_, `#207 <https://github.com/beeware/travertino/issues/207>`_, `#208 <https://github.com/beeware/travertino/issues/208>`_, `#209 <https://github.com/beeware/travertino/issues/209>`_, `#210 <https://github.com/beeware/travertino/issues/210>`_, `#211 <https://github.com/beeware/travertino/issues/211>`_, `#212 <https://github.com/beeware/travertino/issues/212>`_, `#213 <https://github.com/beeware/travertino/issues/213>`_, `#214 <https://github.com/beeware/travertino/issues/214>`_, `#215 <https://github.com/beeware/travertino/issues/215>`_, `#216 <https://github.com/beeware/travertino/issues/216>`_, `#217 <https://github.com/beeware/travertino/issues/217>`_, `#218 <https://github.com/beeware/travertino/issues/218>`_, `#219 <https://github.com/beeware/travertino/issues/219>`_, `#220 <https://github.com/beeware/travertino/issues/220>`_, `#221 <https://github.com/beeware/travertino/issues/221>`_, `#224 <https://github.com/beeware/travertino/issues/224>`_, `#225 <https://github.com/beeware/travertino/issues/225>`_, `#226 <https://github.com/beeware/travertino/issues/226>`_, `#227 <https://github.com/beeware/travertino/issues/227>`_, `#228 <https://github.com/beeware/travertino/issues/228>`_, `#229 <https://github.com/beeware/travertino/issues/229>`_, `#230 <https://github.com/beeware/travertino/issues/230>`_, `#231 <https://github.com/beeware/travertino/issues/231>`_, `#232 <https://github.com/beeware/travertino/issues/232>`_, `#234 <https://github.com/beeware/travertino/issues/234>`_, `#235 <https://github.com/beeware/travertino/issues/235>`_, `#236 <https://github.com/beeware/travertino/issues/236>`_, `#237 <https://github.com/beeware/travertino/issues/237>`_, `#238 <https://github.com/beeware/travertino/issues/238>`_, `#239 <https://github.com/beeware/travertino/issues/239>`_, `#240 <https://github.com/beeware/travertino/issues/240>`_, `#242 <https://github.com/beeware/travertino/issues/242>`_, `#245 <https://github.com/beeware/travertino/issues/245>`_, `#247 <https://github.com/beeware/travertino/issues/247>`_, `#248 <https://github.com/beeware/travertino/issues/248>`_


0.3.0 (2023-08-16)
==================

Features
--------

* Layout nodes can now track the minimum permitted layout size in addition to the current actual layout size. (`#78 <https://github.com/beeware/travertino/issues/78>`_)


Backward Incompatible Changes
-----------------------------

* Support for Python 3.7 was removed. (`#80 <https://github.com/beeware/travertino/issues/80>`_)


Misc
----

* `#44 <https://github.com/beeware/travertino/issues/44>`_, `#45 <https://github.com/beeware/travertino/issues/45>`_, `#46 <https://github.com/beeware/travertino/issues/46>`_, `#47 <https://github.com/beeware/travertino/issues/47>`_, `#48 <https://github.com/beeware/travertino/issues/48>`_, `#49 <https://github.com/beeware/travertino/issues/49>`_, `#50 <https://github.com/beeware/travertino/issues/50>`_, `#51 <https://github.com/beeware/travertino/issues/51>`_, `#52 <https://github.com/beeware/travertino/issues/52>`_, `#53 <https://github.com/beeware/travertino/issues/53>`_, `#54 <https://github.com/beeware/travertino/issues/54>`_, `#55 <https://github.com/beeware/travertino/issues/55>`_, `#56 <https://github.com/beeware/travertino/issues/56>`_, `#57 <https://github.com/beeware/travertino/issues/57>`_, `#58 <https://github.com/beeware/travertino/issues/58>`_, `#59 <https://github.com/beeware/travertino/issues/59>`_, `#60 <https://github.com/beeware/travertino/issues/60>`_, `#61 <https://github.com/beeware/travertino/issues/61>`_, `#62 <https://github.com/beeware/travertino/issues/62>`_, `#63 <https://github.com/beeware/travertino/issues/63>`_, `#65 <https://github.com/beeware/travertino/issues/65>`_, `#66 <https://github.com/beeware/travertino/issues/66>`_, `#67 <https://github.com/beeware/travertino/issues/67>`_, `#72 <https://github.com/beeware/travertino/issues/72>`_, `#73 <https://github.com/beeware/travertino/issues/73>`_, `#74 <https://github.com/beeware/travertino/issues/74>`_, `#75 <https://github.com/beeware/travertino/issues/75>`_, `#76 <https://github.com/beeware/travertino/issues/76>`_, `#77 <https://github.com/beeware/travertino/issues/77>`_, `#79 <https://github.com/beeware/travertino/issues/79>`_, `#81 <https://github.com/beeware/travertino/issues/81>`_, `#82 <https://github.com/beeware/travertino/issues/82>`_, `#83 <https://github.com/beeware/travertino/issues/83>`_, `#84 <https://github.com/beeware/travertino/issues/84>`_, `#85 <https://github.com/beeware/travertino/issues/85>`_, `#86 <https://github.com/beeware/travertino/issues/86>`_, `#87 <https://github.com/beeware/travertino/issues/87>`_


0.2.0 (2023-03-24)
==================

Features
--------

* Node now supports the ``clear`` method in order to clear all children. (`#23 <https://github.com/beeware/travertino/issues/23>`_)
* Constants for absolute and relative font sizing were added. (`#43 <https://github.com/beeware/travertino/issues/43>`_)


Bugfixes
--------

* Handling of ``none`` as a property value has been corrected. (`#3 <https://github.com/beeware/travertino/issues/3>`_)


Improved Documentation
----------------------

* Details on towncrier and pre-commit ussage were added to the README. (`#18 <https://github.com/beeware/travertino/issues/18>`_)


Misc
----

* `#22 <https://github.com/beeware/travertino/issues/22>`_, `#24 <https://github.com/beeware/travertino/issues/24>`_, `#25 <https://github.com/beeware/travertino/issues/25>`_, `#26 <https://github.com/beeware/travertino/issues/26>`_, `#30 <https://github.com/beeware/travertino/issues/30>`_, `#34 <https://github.com/beeware/travertino/issues/34>`_, `#35 <https://github.com/beeware/travertino/issues/35>`_, `#36 <https://github.com/beeware/travertino/issues/36>`_, `#37 <https://github.com/beeware/travertino/issues/37>`_, `#38 <https://github.com/beeware/travertino/issues/38>`_, `#39 <https://github.com/beeware/travertino/issues/39>`_, `#40 <https://github.com/beeware/travertino/issues/40>`_, `#41 <https://github.com/beeware/travertino/issues/41>`_, `#42 <https://github.com/beeware/travertino/issues/42>`_


0.1.3 (2020-05-25)
==================

Features
--------

* Introduced some constants used by Pack that have more general uses. (`#5 <https://github.com/beeware/travertino/issues/5>`_)
* Added the ability to add, insert and remove children from a node tree. (`#10 <https://github.com/beeware/travertino/issues/10>`_)
* Added color validation in rgba and hsla constructors (`#17 <https://github.com/beeware/travertino/issues/17>`_)
* Added support for declaring a system default font size. (`#19 <https://github.com/beeware/travertino/issues/19>`_)

Misc
----

* `#15 <https://github.com/beeware/travertino/issues/15>`_, `#16 <https://github.com/beeware/travertino/issues/16>`_


0.1.2
=====

* Added constants for system and message fonts
* Added hash method to fonts and colors

0.1.1
=====

* Added font definitions

0.1.0
=====

Initial release.
