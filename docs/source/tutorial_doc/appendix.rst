.. Supported Syntaces and Grammar

Supported Syntax and Grammar
##########################################################################

Type System
********************************************************************
| Matx adopts weak type system and supports "Any" type. It aims to be compatible with Python programming style. However, we enforce type annotation of the class members and signatures of the functions. In other circumstances, we highly recommend users to annotate the type of any used variables to achieve better performance.
| Reference to `Python annotation <https://docs.python.org/3/library/typing.html />`_.
| Below is the type correspondece table:



+---------------+-------------------------------+--------+
| Python        | MATX                          | Remark |
+===============+===============================+========+
| int           | int64_t                       |        |
+---------------+-------------------------------+--------+
| float         | double                        |        |
+---------------+-------------------------------+--------+
| bool          | int64_t                       |        |
+---------------+-------------------------------+--------+
| str           | runtime::Unicode              |        |
+---------------+-------------------------------+--------+
| bytes         | runtime::String               |        |
+---------------+-------------------------------+--------+
|| list         || runtime::List(generic var)   ||       |
||              || runtime::FTList (scoped var) ||       |
+---------------+-------------------------------+--------+
|| dict         || runtime::Dict(generic var)   ||       |
||              || runtime::FTDict(scoped var)  ||       |
+---------------+-------------------------------+--------+
|| set          || runtime::Set(generic var)    ||       |
||              || runtime::FTSet(scoped var)   ||       |
+---------------+-------------------------------+--------+
| tuple         | runtime::Tuple                |        |
+---------------+-------------------------------+--------+
| class         | runtime::UserData             |        |
+---------------+-------------------------------+--------+
| callable      | runtime::UserData             |        |
+---------------+-------------------------------+--------+
| NDArray(matx) | runtime::NDArray              |        |
+---------------+-------------------------------+--------+
| Any           | runtime::RTValue              |        |
+---------------+-------------------------------+--------+
| None          | runtime::RTValue              |        |
+---------------+-------------------------------+--------+

Python Gammar
********************************************************************


Operator
********************************************************************


User defined class
********************************************************************

Libraries Support
********************************************************************

Script Type Correspondence Table
********************************************************************
